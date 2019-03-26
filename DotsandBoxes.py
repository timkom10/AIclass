
import random#used for generating random scores
import time #used to time everything
import copy#used to make a different object so that the algorithm could try out different moves
class Dotbox(object):#the Dotbox game class
	def __init__(self, size=5, position=[],papts=0, pbpts=0,turn=0):#initializing the game
		self.size=size#the size of the puzzle
		self.position=position#the current state of the game
		self.pa=papts#player 1's points
		self.pb=pbpts#player 2's points
		self.turn=turn#current turn number
		if not self.position or self.gameover():#if the game is not over or the position is not empty
			for x in range(0,self.size):#amount of rows
				self.position.append([])#makes a row
				for y in range(0,self.size):#amount of columns
					print(x,y)#prints going through 
					self.position[x].append(' ')#puts an empty spot
		self.mknewgame()#calls the actual making switching some of the empty spots to dots or points
		
	def gameover(self):#the check of whether the game is over
		if not self.position:#if the list is empty
			return True#returns the game is over
		else:#or...
			for x in self.position:#for each row
				for y in x:#for each column
					if y==' ':#if there is a space
						return False# then the game is not over
		if self.pa>self.pb:#if Player1 has more points thann Player2
			print('Player 1 Wins! P1score:'+str(self.pa)+" ; P2score:"+str(self.pb))#prints that player1 wins
		elif self.pb>self.pa:#if Player2 has more points than Player1
			print("Player 2 Wins! P1score:"+str(self.pa)+" ; P2score:"+str(self.pb))#prints that Player2 wins
		else:#or if there is a tie
			print("IT WAS A TIE! SCORE: both players with "+str(self.pa)+" points")#prints that there is a tie
		return True#returns that the game is over
		
	def mknewgame(self):#makes a new game
		if (not self.position) or self.gameover() or self.position[0][0]==' ':#if the position is empty or the game is over or the dots have not been put in yet
			for x in range(0,self.size):#through the rows
				for y in range(0,self.size):#through the columns
					#print(x,y)#check print statement
					if (x%2==0 and y%2==0):#if rows and colums are even
						self.position[x][y]='.'#place dot
						#print('.')#check print statement
					elif (x%2==1 and y%2==1):#if rows and columns are odd
						self.position[x][y]=(random.randint(1,5))#place value of box
						#print('num')#check print statement
					elif (x%2==0 and y%2==1):#if rows are even and columns are odd
						self.position[x][y]=' '#empty space where horizontal lines will go
						#print('-')#check print statement
					elif (x%2==1 and y%2==0):#if rows are odd and columns are even
						self.position[x][y]=' '#empty space where vertical lines will go
						#print('|')#check print statemnt
				print(self.position[x])#prints how the board looks in a nice matter
			self.pa=0#resets the points for player 1(a)
			self.pb=0#resets the points for player 2(b)
			turn=0#resets what turn it is
		
	def __str__(self):#for string representation
		return str(self.position)#just returns the string of the position #I'll be honest looking back this is unneccessary but its two lines of code so ¯\_(ツ)_/¯
		
	def move(self,x,y):#makes the move and switches between move of player 1 and player 2
		self.turn+=1#increases the turn to show which player's turn it is
		if self.gameover():#if the game is over
			return "Game Over"#then print game over
		if self.turn%2==1:#if the turn is odd
			self.movepa(x,y)#then its player 1's turn
		else:#else
			self.movepb(x,y)#then its player2's turn
		# for x in self.position:#used for printing out the position when playing against another player rather than the computer
			# print(x)#commented out for computer because then the screen gets crowded too much
			
	def movepa(self,x,y):#player1's move funciton
		while True:#infinite loop so that players can't get away with stalling and making a bad move to try to get a box
			try:#try except for ease
				if(x%2==0 and y%2==1) and self.position[x][y]==' ':#if rows are even and columns are odd and there is an empty space
					#print('here1')#check print statement
					self.position[x][y]='-'#then put a horizontal
					if x>0 and x<self.size-1:#if x is not on the top row or the bottom row
						#print('here2')#check print statement
						self.box(self.position[x-1][y],x-1,y,(x,y))#check the box above this horizontal line
						self.box(self.position[x+1][y],x+1,y,(x,y))#check the box below this horizontal line
					elif x==0:#or if its the top row
						#print('here2.1')#check print statmeent
						self.box(self.position[x+1][y],x+1,y,(x,y))#checks the box below the horiziontal line
						#print('here2.3')#check print statement
					elif x==self.size-1:#or if its the bottom row
						#print('here2.2')#check print statement
						self.box(self.position[x-1][y],x-1,y,(x,y))#checks the box above the horizontal line
					#print('here3')#checks print statement
					return#breaks out of loop
				elif(x%2==1 and y%2==0) and self.position[x][y]==' ':#or if the rows are odd and the columns are even and there is an empty space
					#print('here4')#check print statement
					self.position[x][y]='|'#puts a single horizontal line
					if y>0 and y<self.size-1:#if the line is not in the firs or last column
						#print('here5')#check print statement	
						self.box(self.position[x][y-1],x,y-1,(x,y))#checks the box to the left of the line
						self.box(self.position[x][y+1],x,y+1,(x,y))#checks the box to the right of this line
						#print('here5.3')#check print statement
					elif y==0:#or if the line is on the left column
						#print('here5.1')#check print statement
						self.box(self.position[x][y+1],x,y+1,(x,y))#checks the box to the right of this line
						#print('here5.4')#check print statement
					elif y==self.size-1:#cheks if the line is on the right column
						#print('here5.2')#check print statement
						self.box(self.position[x][y-1],x,y-1,(x,y))#checks the box to the left of the line
						#print('here5.5')#check print statement
					#print('here6')#check print statement
					return#return breaks out of loops
				else: #if its not a correct move to make a the moment
					#print('hmmmm')#check print stateent
					raise ValueError#raises error to loop until a value is found
			except:#except spot
				print('invalid move try again')#check print statement for chcekcing
				x=int(input("input your new x"))#asks for the new x values
				y=int(input("input your new y"))#asks for the new y values
				
	def movepb(self,x,y):#player 2's move set
		while True:#infiniteloop
			try:#try block so it loops well
				if(x%2==0 and y%2==1) and self.position[x][y]==' ':#if the rows are even and colums are odd
					#print('here7')#print check statement
					self.position[x][y]='='# then the spot becomes two horizontallines to differentiate from the singleline of player 1
					if x>0 and x<self.size-1:#if the horiziontalline is not on top or on the bttom
						#print('here9')#check print statemnt
						self.box(self.position[x-1][y],x-1,y,(x,y))#checks the box below the line
						self.box(self.position[x+1][y],x+1,y,(x,y))#checks the box above the line
						#print('here9.3')#check print statement
					elif x==0:#if the line is at the top 
						#print('here9.1')#checks print statement
						self.box(self.position[x+1][y],x+1,y,(x,y))#checks the box below the line
						#print('here9.4')#checks print statement
					elif x==self.size-1:#or is the line is at the bottom
						#print('here9.2')#checks print statement
						self.box(self.position[x-1][y],x-1,y,(x,y))#checks the box above the line
						#print('here9.5')#check print statement
					#print('here11')#check print statement
					return#breaks out of loop
				elif(x%2==1 and y%2==0) and self.position[x][y]==' ':#if the rows are odd and the colmns are even.
					#print('here8')#checks print statement
					self.position[x][y]='||'#puts the veritacl double line to differetiate
					if y>0 and y<self.size-1:#if the line is not on the left column or right column
						#print('here10')#print check line
						self.box(self.position[x][y-1],x,y-1,(x,y))#checks the box to the left of the line
						self.box(self.position[x][y+1],x,y+1,(x,y))#checks teh box to the right of th eline.
						#print('here10.3')$check print statement
					elif y==0:#if the line is on the left column
						#print('here10.1')#check print statement
						self.box(self.position[x][y+1],x,y+1,(x,y))#checks the box to the right of th reline
						#print('here.4')$check print statement
					elif y==self.size-1:#or if the box is in the right column
						#print('here10.2')#check print statement
						self.box(self.position[x][y-1],x,y-1,(x,y))#hcksas====
						#print('here10.5')
					#print('here 12')
					return#returns and breaks out of the loop
				else: #or
					raise ValueError # raise an error to try again
			except:#excepvalue to loop
				print('invalid move try again')#print used to tell user that they enterred a wrong value
				x=int(input("input your new x"))#asks for new x coordinate
				y=int(input("input your new y"))#asks for a new y coordinate
				
	def copy(self):#copy used to make a new instance with the same positions so minimax can go through
		position=copy.deepcopy(self.position)#makes a deepcopy so that it doesn't touch the memory value
		return Dotbox(self.size,position,self.pa,self.pb,self.turn)#returns the copy instance
		
	def box(self,value,x,y,last):#the check for points method and saves the last move made
		#print('boxproblem')#check print statement
		numlines=0#instantiates for how many lines are surronding it
		available=[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]#shows what is still open
		if self.position[x-1][y] !=' ':#if the line above is filled
			numlines+=1#the number of lines surrounding it goes up one
			available.remove((x-1,y))#removes from available
		if self.position[x+1][y] !=' ':#if the line below is filled
			numlines+=1#the number of lines surrounding it goes up one
			available.remove((x+1,y))#removes from available
		if self.position[x][y-1] !=' ':#if the line to the left is filled
			numlines+=1#the number of lines surrounding it goes up one
			available.remove((x,y-1))#removes from available
		if self.position[x][y+1] !=' ':#if the line to the right is filled
			numlines+=1#the number of lines surrounding it goes up one
			available.remove((x,y+1))#removes from available
		if numlines==4:#if all lines are filled
			if self.position[last[0]][last[1]]=='-' or self.position[last[0]][last[1]]=='|':#if the last move was a single vertical or horiziontal line
				self.pa+=value#then player 1 gets points
				print("Player 1 scores "+str(value)+" point(s)!")#print statement so player knows
				self.gameover()#checks if the game is over
			elif self.position[last[0]][last[1]]=='=' or self.position[last[0]][last[1]]=='||':#or if the last move was a double vertical or horiziontal line
				self.pb+=value#then player 2 gets points 
				print("Player 2 scores "+str(value)+" point(s)!")#print statement so player knows
				self.gameover()#checks if game is over
		return#return to end method
		
	def availablemoves(self):#method to show what coordinate moves are available
		available=[]#instantiates a list
		for x in range(0,self.size):#for all rows
			for y in range(0,self.size):#for all columns
				if self.position[x][y]==' ':#if the spot is empty
					available.append((x,y))#then add the coordinates in a tuple to the list
		#print('heres whats available')#check print statement
		return available#retuns the list
		
def playvscpu(self):#for facing against a computer#self==dotbox() I tried to make this a method but gave up due to errors and the funciton works well
	depth=0#starts out at a depth of 0 so that it takes shorter but minimax searches deeper each time
	while self.gameover()!=True:#while the game is not over
		for x in self.position:#for each row
			print(x)#print each row so that you see it like a box
		print(self.availablemoves())#prints the available moves
		x=int(input("Player 1: Enter an x coordinate for your move: "))#player 1 x input 
		y=int(input("Player 1: Enter an y coordinate for your move: "))#player 1 y input
		self.move(x,y)#moves for player 1
		depth+=2#increases depth
		aimove=dotVsAi(self,depth,-100000000000000000,10000000000000000, True)#calls the minimax algorithm w/ alpha beta pruning
		print(self.position)#prints the position that the minimax picked
		print(aimove)#prints the expected value and  the move the computer will make
		self.move(aimove[1][0],aimove[1][1])#actually  makes the move
		print("The score currently is Player1: "+str(self.pa)+" CPU: "+str(self.pb))#presents score
		
def dotVsAi(self,depth,a,b, maxplayer):#minimax algorithm with alpha beta pruning #self=dotbox#
	#print('cputurn')#check print statement
	if depth==0 or self.gameover():#if the game is over at a specific position or if it hits max depth
		#print('depth = 0')#check print statement
		return [self.pb-self.pa]#returns the cpu score - the player score
	if maxplayer==True:#if it is going through the max part
		#print('hit maxplayer if')#check print statement
		maxeval=-100000000#makes the max eval very low so that it does not mess with data
		move=[0,0]#makes a list for moves
		ava=self.availablemoves()#shorter call for available moves
		for x in ava:#for all available moves
			#print('max'+str(x))#check print statement
			self2=self.copy()#make a copy of the position
			self2.move(x[0],x[1])#make the new position
			evalu=dotVsAi(self2, depth-1,a,b,False)#and go deeper into the function recursively
			print(evalu)#prints the value that the algorithm picks and what move comes from it
			maxeval= max(maxeval,evalu[0])#compares the current best with the current move
			a=max(a,evalu[0])#checks against alpha
			if a>=b:#if alpha is greater then or equal to beta then we can prune everything else to save time
				#print('PRUNEmax')#check print statment
				break#actual pruning
			if maxeval==evalu[0]:#if the value was just changed
				#print('new max')#check print statemt
				move[0]=x[0]#insert the new best x-coordinate
				move[1]=x[1]#insert the new best y-coordinate
		#print(move)#check print statement
		print(maxeval)#prints the best move for this subtree
		if move==[0,0]:#if there is no best move
			#print(ava)#print check statmeent
			rand=random.randint(0,len(ava)-1)#pick a random number that is in the list
			#print(rand)#print check statemnt
			move[0]=ava[rand][0]#picks the random selected x-coordinate
			move[1]=ava[rand][1]#picks the random selected y-coordinate
		print(move)#prints the move selected overall
		return [maxeval,move]#returns the max value and the move that is associated with it
			
	else:#if tis the mins player in searching
		#print('hit minplayer if')#check print statement
		mineval=100000000#makes the min very large so that it will get changed
		move=[0,0]#makes a list for x and y coordinate
		ava=self.availablemoves()#list of available moves
		for x in ava:#iterates through available moves
			self2=self.copy()#makes a copy of the position
			#print('min'+str(x))#check print statement
			self2.move(x[0],x[1])#makes the new posiiton
			evalu=dotVsAi(self2,depth-1,a,b,True)#checks and goes deeper recursively into new posiiton
			print(evalu)#prints new value
			mineval=min(mineval,evalu[0])#compares the current with the best lowest number so far and picks the lower
			b=min(b,evalu[0])#checks against beta
			if a>=b:#if alpha is greater than or equal on a max move then opponnent will not pick any of these
				#print('PRUNEmin')#chck print statment
				break#actual pruning
			if mineval==evalu[0]:#if the value was just changed
				print('new min')#new check print statment
				move[0]=x[0]#changes the x-coordinate value
				move[1]=x[1]#changes the y-coordinate value
		if move==[0,0]:#if there was no best decidable move
			#print(ava)#check print statmeant
			rand=random.randint(0,len(ava)-1)#picks random nymber that has an index in list
			#print(rand)#prints the number
			move[0]=ava[rand][0]#saves the selected x-coordinate
			move[1]=ava[rand][1]#saves the selected y-coordinate
		#print(move)#prints the move selected overall
		return [mineval,move]#returns the min value and the move that is associated with it
x=Dotbox(5)#intiallizing the dotbox game at size =4 boxes
playvscpu(x)#starts the game
