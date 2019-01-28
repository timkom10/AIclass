#Tim Komperda
import copy#used for making new nodes
from queue import PriorityQueue#used for advanced functions that require a heuristic
import time#used for timing
from collections import Counter#used to count the number of things in a PriorityQueue

class Puzzlenode(object):#this is the class I made for a puzzlenode(I think it is incredibly inefficient but it took me way too long to just figure it out.

	def __init__(self, position=None, parent=None,depth=0,lastaction=None, totalcost=0, misplacedtile=0):#the initialization of this class contains every single bit of information besides manhattan distances used for the searches
		self.position= position#position is the current iteration of the puzzle
		self.parent= parent #parent is the previous iteration useful for path tracing
		self.depth=depth#keeps track of depth
		self.action=lastaction#keeps track of the last action
		self.tcost=totalcost#keeps track of the totalcost of every move
		self.goal=[[1,2,3],[8,0,4],[7,6,5]]#goal state
		self.movelist=[]#shows moves available, filled by self.moves()
		self.miscount=misplacedtile#just gave it a cool name
		self.miscount=self.pos_check(self.position)#I made this so that way that the tile count would be more automatic and so that I would not need to include this in the code at the beginning for greedy search and A*1

	def __lt__(self,other):#this is used to make Puzzlenode comparable for some reason priorityqueue cannot just sort between misplaced tiles and total cost so this was used in order to satisfy the PriorityQueue
		return self.depth<other.depth#I figured that organizing by depth at ties makes somewhat sense

	def __gt__(self,other):#This is also used to make Puzzlenode comparable, I haven't coded enough in Python to really know if this was necessary
		return self.depth>other.depth#organizing by depth because it seemed innocent enough without making greedy search an A* algo

	def pos_check(self,pos):#this is the function used to find misplaced tiles#this is pretty good, and I like how I did this
		count=0#initiates a count variable
		for x in range(3):#iterates through 0 to 2 for rows
			for y in range(3):#iterates through 0 to 2 for columns
				if pos[x][y]!=self.goal[x][y]:#checks to see if the two are different #I did this because you said to count by number of misplaced tiles rather than tiles that are in the correct position
					count+=1#adds one if the tile is misplaced
		return count#returns the amount of misplaced tiles
#
	def __str__(self):#if str(puzzlenode) is used this will return what is necessary
		if self.parent==None:#if there is no parent then just set parent to a string that says none
			parent='None'#string that says parent is none
		else:#otherwise
			parent=self.parent.position#parent is the list of the parent
		return 'Puzzlenode( {}, {}, {}, {}, {}, {})'.format(self.position, parent, self.depth, self.action, self.tcost, self.miscount)#returns the function as it would be input for a move function, except for the parent function. Parent is done as a list because it is much easier to understand then explain it as a place in memory at least for me

	def moves(self):#gives me move options
		for row in range(3):#searching for zeros row
			for col in range (3):#searching for zeros column
				if self.position[row][col]==0:#if find zero
					self.row0=row#save row of zero to row0
					self.col0=col#save column of zero to col0
		if self.row0>0:#if zero is not in the top row
			self.movelist.append("Down")#appends that a Down move is available, and it appends the number that can go Down as a list
		if self.row0<2:#if zero is not in the bottom row
			self.movelist.append("Up")#appends that a Up move is available, and it appends the number that can do this move as a list
		if self.col0>0:#if zero is not on the right column
			self.movelist.append("Right")#appends that a Right move is available, and it appends the number that can do this move as a list
		if self.col0<2:#if zero is not in the left column
			self.movelist.append("Left")#appends that a Left move is available, and it appends the number that can do this move as a list
		return self.movelist#returns the list of moves and what numbers move

	def isGoal(self):#determines if the goal state has been acheived
		if self.position==self.goal:# if the position is the same as the defined(hardcoded) goalstate
			return True#return True
		else:# if not
			return False#return False

	def moveDown(self):#move Down action method
			position=copy.deepcopy(self.position)#making a copy of the original list/picture
			position[self.row0][self.col0]=self.position[self.row0-1][self.col0]#moving the numbered picture that is not zero Down to zero's position
			position[self.row0-1][self.col0]=0# zero is now in the old numbered space
			#print(position)#print line used for checking
			count=self.pos_check(position)#this is used to check the amount of misplaced tiles and shows why I have to pass a list to make this method work because I wanted to make it sortable from here
			return Puzzlenode(position,self,self.depth+1,"Down",self.tcost+self.position[self.row0-1][self.col0],count)#returns the next Puzzlenode with every stat possible

	def moveUp(self):#moves up number moves down 0 method
			position=copy.deepcopy(self.position)#making a copy of the original list/picture
			position[self.row0][self.col0]=self.position[self.row0+1][self.col0]#moving the numbered picture that is not zero Up to zero's position
			position[self.row0+1][self.col0]=0#zero takes the spot of the numbered space
			#print(position)#print line used for checking
			count=self.pos_check(position)#this is used to get the amount of misplaced tiles also look at moveDown comment
			return Puzzlenode(position,self,self.depth+1,"Up",self.tcost+self.position[self.row0+1][self.col0],count)#returns the next Puzzlenode

	def moveRight(self):#move Right action method
			position=copy.deepcopy(self.position)#making a copy of the list/picture
			position[self.row0][self.col0]=self.position[self.row0][self.col0-1]#moving the numbered picture that is not zero Right to zero's position
			position[self.row0][self.col0-1]=0#zero takes the spot of the moved number space
			count=self.pos_check(position)#this is used to get the amount of misplaced tiles also look at moveDown comment
			#print(position)#print line used for checking
			return Puzzlenode(position,self,self.depth+1,"Right",self.tcost+self.position[self.row0][self.col0-1],count)#returns the next Puzzlenode

	def moveLeft(self):#move Left action method
			position=copy.deepcopy(self.position)#making a copy of the list/picture
			position[self.row0][self.col0]=self.position[self.row0][self.col0+1]#moving the numbered picture that is not zero Left to zero's position
			position[self.row0][self.col0+1]=0#moving the zero to the numbered position
			count=self.pos_check(position)#this is used to get the amount of misplaced tiles also look at moveDown comment
			#print(position)#print line used for checking to see behaviour
			return Puzzlenode(position,self,self.depth+1,"Left",self.tcost+self.position[self.row0][self.col0+1],count)#returns next Puzzlenode

	def goaltopath(self,path):#gathers a list of the previous nodes used to get to the goal state (recursively)
		if self.parent==None:#if this is the original node
			path.append(str(self))#appends self to the path list
			return path#return the path
		else:#otherwise
			path.append(str(self))#appends self to the path list
			return self.parent.goaltopath(path)#calls funcition with parent node so that it goes all the way to start node

	def manhattan(self,pos):#this function calculates for the manhattan distance# this could probably be done more efficiently, I just would need to work through it with someone else or take more time on it
		coorlist=[() for i in range(9)]#this is a list of tuples that I just wanted to populate based on each numbered tile
		sum=0#this is the manhattan distance variable
		for x in range(3):#iterates through 0th to 2nd row
			for y in range(3):#iterates through 0th to 2nd column
				for i in range(9):#this iterates from 0 to 8 to check what number tile it is
					if pos[x][y]==i:#used to match the tile number to an index
						coorlist[i]=(x,y)#this gives coordinates for where the index value is located on the current position of the puzzle
		for i in range(3):#iterates through 0th to 2nd row 
			for j in range(3):#iterates through the 0th to 2nd column
				sum+=(abs(coorlist[self.goal[i][j]][0]-i)+abs(coorlist[self.goal[i][j]][1]-j))#the magic function# this takes the absolute value of the difference of the current positions number as iterated through via the goal state's row and the row of the goal state plus the current position's number that the goal state is at's column and the number's goal state column #harder to explain then to see really
		return sum#returns the manhattan distance


def bfs(p):#p for puzzlenode breadth first search
	checked=set()#creates a state checker so that repeat states do not happen
	queue=[]#creates a queue
	queue.append(p)#puts the passed node into the queue
	while True:#basically I want it to loop until it finds something
		q=queue.pop(0)#takes the first thing in the queue
		checked.add(str(q.position))#adds a string version of the position so it can be hashed into a set
		#print(q)#used to track behaviour
		if q.isGoal():#checks if the current state is the goal state
			#print(len(queue))#originally I put this in the else loop to see how this works but then I figured that it was more efficient here and told me the max size of the queue
			return q.goaltopath([])# return the list of how to get to the goal from the start node
		else:#otherwise
			q.moves()#makes the list of moves(I could probably do something to make this more efficient maybe, but for now its staying here)
			if "Down" in q.movelist and str(q.moveDown().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				queue.append(q.moveDown()) #adds the iteration to the queue
			if "Up" in q.movelist and str(q.moveUp().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				queue.append(q.moveUp())#adds the iteration to the queue
			if "Right" in q.movelist and str(q.moveRight().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				queue.append(q.moveRight())#adds the iteration to the queue
			if "Left" in q.movelist and str(q.moveLeft().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				queue.append(q.moveLeft())#adds the iteration to the queue
		


def dfs(p):#p for puzzlenode depth first search
	checked=set()#creates a state checker so that repeat states do not happen
	queue=[]#creates a queue
	queue.append(p)#puts the passed node into the queue
	while True:#I want to loop until the goal is reached
		q=queue.pop()#removes the most recnt item added
		checked.add(str(q.position))#adds iteration in string to set
		print(q.position)#print statement to track behaviour
		if q.isGoal():#checks if current iteration is the goal
			return q.goaltopath([])#if goal is reached then it reaches back to show the path to the goaL
		else:#otherwise
			q.moves()#makes list of available moves (see bfs for extra note)
			if "Down" in q.movelist and str(q.moveDown().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				queue.append(q.moveDown()) #adds iteration ot the queue
			if "Up" in q.movelist and str(q.moveUp().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				queue.append(q.moveUp())#adds iteration to the queue\
			if "Right" in q.movelist and str(q.moveRight().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				queue.append(q.moveRight())#adds iteration ot the queue
			if "Left" in q.movelist and str(q.moveLeft().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				queue.append(q.moveLeft())	#adds the iteration to the queue
		#print(len(checked))#this was used to check how many positions were checked until it took longer than five minutes for easy
		

def ucs(p):#p for puzzlenode uniform cost search
	checked=set()#creates a state checker so that repeat states do not occur
	pqueue=PriorityQueue()#a queue that is a heap, but functions like a queue, this sorts easily and returns what I need
	pqueue.put((p.tcost,p))#entering g(n) and the node so that it can start the loop
	while True:#I made this a while true because its easier to make it like this without making bad mistakes# in hindsight I could do while queue.isNotEmpty(), but I don't know if this will break it or just make it make more sense
		q=pqueue.get()#gets the tuple that has the smallest total cost
		z=q[1]#gets the actual Puzzlenode
		checked.add(str(z.position))#adds the position into the state checker so that we don't see another one of these states
		#print(q)#print statement for checking behaviour
		if z.isGoal():#checks if current iteration is the goal
			#print(Counter(priority for priority, _elem in pqueue.queue))#has a by each priority count it counts each number of puzzlenodes with the priority count
			return z.goaltopath([])#if goal is reached then it reaches back to show the path to the goaL
		else:#otherwise
			z.moves()#makes the movelist which has all the possible moves
			if "Down" in z.movelist and str(z.moveDown().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveDown().tcost,z.moveDown())) #adds iteration ot the queue
				#print("put down")#used to track which moves were added
			if "Up" in z.movelist and str(z.moveUp().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveUp().tcost,z.moveUp()))#adds iteration to the queue
				#print("put Up")#used to track which moves were added
			if "Right" in z.movelist and str(z.moveRight().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveRight().tcost,z.moveRight()))#adds iteration ot the queue
				#print("put Right")#used to track which moves were added
			if "Left" in z.movelist and str(z.moveLeft().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveLeft().tcost,z.moveLeft()))	#adds the iteration to the queue
				#print("put left")#used to track which moves were added


def greedy(p):#p for puzzlenode best-first search
	checked=set()#creates a state checker so that repeat states do not occur
	pqueue=PriorityQueue()#a sorting queue#more info at ucs function
	pqueue.put((p.miscount,p))#entering h(n) which happens to be the amount of tiles that are misplaced and takes the puzzlenode
	while True:#while true loop as explained for the past 3 times
		q=pqueue.get()#gets the tuple that has the smallest h(n)
		z=q[1]#gets the puzzle node from the tuple
		checked.add(str(z.position))#adds the position into the state checker
		#print(z)#prints the current puzzlenode
		if z.isGoal():#checks to see if its the goalstate
			#print(Counter(priority for priority, _elem in pqueue.queue))#counts number of puzzlenodes per h(n)
			return z.goaltopath([])#returns the path from the goal node to the start node
		else:#if goalstate not yet
			z.moves()#makes the movelist that has all the possible moves
			if "Down" in z.movelist and str(z.moveDown().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveDown().miscount,z.moveDown())) #adds iteration ot the queue
				#print("put down")#used to track which moves were added
			if "Up" in z.movelist and str(z.moveUp().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveUp().miscount,z.moveUp()))#adds iteration to the queue
				#print("put Up")#used to track which moves were added
			if "Right" in z.movelist and str(z.moveRight().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveRight().miscount,z.moveRight()))#adds iteration ot the queue
				#print("put Right")#used to track which moves were added
			if "Left" in z.movelist and str(z.moveLeft().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveLeft().miscount,z.moveLeft()))	#adds the iteration to the queue
				#print("put left")#used to track which moves were added
				

def aStar1(p):#p for puzzlenode A*1
	checked=set()#creates a state checker so that repeat states do not occur
	pqueue=PriorityQueue()#sorting queue# more info at ucs function
	pqueue.put((p.miscount+p.tcost,p))#entering f(n)=h(n)+g(n) where h(n) is the amount of misplaced tiles and g(n) is the total cost of moves and the puzzle node as a tuple for the next queue
	while True:# while true loop as explained above
		q=pqueue.get()#gets the tuple that has the smallest f(n)
		z=q[1]#gets the puzzlenode from the tuple
		checked.add(str(z.position))#adds to the checked state set
		#print(z)#used to display which puzzlenode the algo is at
		if z.isGoal():#checks to see if z is the goal
			#print(Counter(priority for priority, _elem in pqueue.queue))#counts each puzzlenode per f(n) value
			return z.goaltopath([])#returns the path from the goal node to start node
		else:#if not the goal state
			z.moves()#makes the movelist that has all the possilbe moves
			if "Down" in z.movelist and str(z.moveDown().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveDown().tcost+z.moveDown().miscount,z.moveDown())) #adds iteration ot the queue
				#print("put down")#used to track which moves were added
			if "Up" in z.movelist and str(z.moveUp().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveUp().tcost+z.moveUp().miscount,z.moveUp()))#adds iteration to the queue\
				#print("put Up")#used to track which moves were added
			if "Right" in z.movelist and str(z.moveRight().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveRight().tcost+z.moveRight().miscount,z.moveRight()))#adds iteration ot the queue
				#print("put Right")#used to track which moves were added
			if "Left" in z.movelist and str(z.moveLeft().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveLeft().tcost+z.moveLeft().miscount,z.moveLeft()))	#adds the iteration to the queue
				#print("put left")#used to track which moves were added
		#print(Counter(priority for priority, _elem in pqueue.queue))#used to show how many iterations happened
		

def aStar2(p):#p for puzzlenode A*2
	checked=set()#creates a state checker set
	pqueue=PriorityQueue()#sorting queue# more info at ucs function
	pqueue.put((p.manhattan(p.position)+p.tcost,p))#entering f(n)=h(n)+g(n) where h(n) is the manhattan distance and g(n) is the total cost of moves and the puzzle node as a tuple into the queue
	while True:#while true again. yeah its lazy and I get it, but it took me way too long to get to this point so I guess I'll do better next time
		q=pqueue.get()#gets the lowest f(n) tuple with its puzzlenode
		z=q[1]#gets the puzzle node out of the tuple
		checked.add(str(z.position))#adds the current node position to the checked set so that the state does not occur again
		#print(z)#used to display which puzzlenode the algorithm is at
		if z.isGoal():#checks to see if the current node is the goal
			#print(Counter(priority for priority, _elem in pqueue.queue))#prints the amount of puzzlenodes per f(n) value
			return z.goaltopath([])#returns the goal state
		else:#if not the goal state
			z.moves()#makes the movelist to see what moves are available
			if "Down" in z.movelist and str(z.moveDown().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveDown().tcost+z.moveDown().manhattan(z.moveDown().position),z.moveDown())) #adds iteration ot the queue
				#print("put down")#used to track which moves were added
			if "Up" in z.movelist and str(z.moveUp().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveUp().tcost+z.moveUp().manhattan(z.moveUp().position),z.moveUp()))#adds iteration to the queue\
				#print("put Up")#used to track which moves were added
			if "Right" in z.movelist and str(z.moveRight().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveRight().tcost+z.moveRight().manhattan(z.moveRight().position),z.moveRight()))#adds iteration ot the queue
				#print("put Right")#used to track which moves were added
			if "Left" in z.movelist and str(z.moveLeft().position) not in checked:#checks if the move is available and makes sure that this moves iteration is not in the checked set
				pqueue.put((z.moveLeft().tcost+z.moveLeft().manhattan(z.moveLeft().position),z.moveLeft()))	#adds the iteration to the queue
				#print("put left")#used to track which moves were added
		#print(Counter(priority for priority, _elem in pqueue.queue))#used to show how many iterations occurred
		

g=Puzzlenode([[1,2,3],[8,0,4],[7,6,5]])#the goal state
e=Puzzlenode([[1,3,4],[8,6,2],[7,0,5]])#the easy starting state
m=Puzzlenode([[2,8,1],[0,4,3],[7,6,5]])#the medium starting state
h=Puzzlenode([[5,6,7],[4,0,8],[3,2,1]])#the hard starting state
while True:
	try:
		d=str(input("which difficulty do you want solved? Enter g for goal state, e for easy state, m for medium state, or h for hard state: "))
		u=g
		if d=='g'or d=='G':
			u=g
			break
		elif d=='e' or d=='E':
			u=e
			break
		elif d=='m' or d=="M":
			u=m
			break
		elif d=='h' or d=="H":
			u=h
			break
		else:
			raise ValueError
	except ValueError:
		print("I do not have that input")
		continue
while True:
	try:
		x=str(input("What search algorithm would you like to use? Enter bfs for breadth first search, dfs for depth first search, ucs for uniform cost search, greedy for best first search, a*1 for A* search with h(n)=number of misplaced tiles, or a*2 for A* search with h(n)= manhattan distance of pieces: "))
		if x=='bfs':
			start=time.time()#starts timing
			print(bfs(u))#the current
			end=time.time()
			print("It took {} seconds for bfs to search through the {} state".format(end-start,d))
			break
		elif x=='dfs':
			start=time.time()#starts timing
			print(dfs(u))#the current
			end=time.time()
			print("It took {} seconds for dfs to search through the {} state".format(end-start,d))
			break
		elif x=='ucs':
			start=time.time()#starts timing
			print(ucs(u))#the current
			end=time.time()
			print("It took {} seconds for ucs to search through the {} state".format(end-start,d))
			break
		elif x=='greedy':
			start=time.time()#starts timing
			print(greedy(u))#the current
			end=time.time()
			print("It took {} seconds for greedy search to search through the {} state".format(end-start,d))
			break
		elif x=='a*1':
			start=time.time()#starts timing
			print(aStar1(u))#the current
			end=time.time()
			print("It took {} seconds for A*1 to search through the {} state".format(end-start,d))
			break
		elif x=='a*2':
			start=time.time()#starts timing
			print(aStar2(u))#the current
			end=time.time()
			print("It took {} seconds for A*2 to search through the {} state".format(end-start,d))
			break
		else:
			raise ValueError
	except ValueError:
		print("I do not have that algorithm")
		continue
print('Run program again for another algorithm!')
