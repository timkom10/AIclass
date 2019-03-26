import random#importing random because randomness is needed
class names(object):#defining the class name
	def __init__(self,fname,n=2):#only have the file name and markov order for this 
		self.lines=[]#where I store every line of code
		self.n=n#the markov order saved for use
		self.hashtable=dict()#dictionaries in python are hashtables # Who knew!
		infile=open(fname)#grabbing the file
		self.infile= infile.readlines()#reads all the lines of the file
		for line in self.infile:#loop to get the initial n values to be hyphens so that we have somewhere to start
			self.lines.append(('-'*n)+line.lower())#initial n values are now hyphens with the regular lowercase name afterwards, because it was easier this way
		infile.close()#close the file becasue we dont need it anymore
		for line in self.lines:#cycling through out list of lines
			x=self.n#moving value to parse through each part of a name
			while x<len(line):#so that it can check the whole name
				self.hashtable[line[x-self.n:x]]=[0]*27#puts zeros in a list with a length of 27 where 26 are the alphabet and 27 is the '\n' becasuse that was already there
				x+=1#plus one to go to the next one
	def hash(self):#this puts values into the hashtable
		for line in self.lines:#goes through our list of Names
			x=self.n#moving value to parse through each part of a name
			while x<len(line):#so that it checks the whole name
				if line[x]=='\n':#because '\n' does not have a value that is exactly 27 above 'a'
					self.hashtable[line[x-self.n:x]][26]+=1#increases value by one
				else:#else
					self.hashtable[line[x-self.n:x]][ord(line[x].lower())-ord('a')]+=1#increase the index based on how far it is away from 'a' which works really well
				x+=1#increases the parse number
	def probabilityBuild(self):#builds the probabilities from the values
		for x in self.hashtable:#for every key in the hashdictionary
			z=0#counter
			for y in range(27):#becasue 27 different values that could appear
				z+=self.hashtable[x][y]#counts how many appear
			for y in range(27):#beacues 27 different values that could appear
				a=self.hashtable[x][y]#the current value there
				self.hashtable[x][y]=float(a)/z#the ratio from the total that are there so there will always be less than 1
	def buildName(self, minlen, maxlen):#Builds names
		name='-'*self.n#this is the start of the name in the same way as the others are in my list
		while name[len(name)-1]!='\n':#keeps building name until it hits a end character
			x=random.random()#random number
			key=name[len(name)-self.n:len(name)]#the key from where we currently are
			letter=0#how far in the alphabet are we?
			while x>0:#while random number is above zero
				x-=self.hashtable[key][letter]#subtract the current ratio from the random number
				letter+=1#increase the index by 1
			if letter==27:#if the index is the last one
				name=name+'\n'#then put the newline character at the end of the name
			else:#else
				name=name+chr(96+letter)#add 96 to get the letter that matches
		if len(name)>=minlen+self.n+1 and len(name)<=maxlen+self.n+1:#if the name fits into the min and max guidelines
			if name not in self.lines:#if the name is not in our submitted list
				name=name[self.n:len(name)-1]#chops off all the dashes because we dont care about those
				name=name[0].capitalize()+name[1:len(name)]#capitalizes the first letter so its an actual name
				return name#returns the name
			else:#or else
				return self.buildName(minlen,maxlen)#do it again
		else:#or else
			return self.buildName(minlen,maxlen)#or else

boys='C:\\Users\\timdk\\Downloads\\namesBoys.txt'#my path to the Boys names
girls='C:\\Users\\timdk\\Downloads\\namesGirls.txt'#my path to the Girls names
	
while True:	
	#male or female
	while True:
		try:
			g=input("Would you like a list of boys names or girls names? Enter boys for boys' names, girls for girls' names, or manual if you have a file you would like to use instead: ")
			if g=='boys' or g=='Boys':
				s=boys
				break
			elif g=='girls' or g=='Girls':
				s=girls
				break
			elif g=='manual' or g=='Manual':#reccomend you use this one because it is highly unlikely you have the same file path as I do
				s=input('Enter the file path for your name list: ')
				break
			else:
				raise ValueError
		except:
			print('That is an invalid answer for this input! Please try again!')
			continue
	#order of model
	while True:
		try:
			n=int(input('What order of Markov Chain would you like? Please enter a positive integer: '))
			if n>0:
				break
			else:
				raise ValueError
		except:
			print('Thats not a valid number for this input! Please try again!')
			continue
	name=names(s,n)
	name.hash()
	name.probabilityBuild()
	#min name length
	while True:
		try:
			minName=int(input('What is the minimum length of the name(s) you want to create? Please enter a positive integer: '))
			if minName>=1:
				break
			else:
				raise ValueError
		except:
			print("That's not a valid number for this input! Please try again")
			continue
	#max name length
	while True:
		try:
			maxName=int(input('What is the maximum length of the name(s) you want to create? Please enter a positive integer that is greater than or equal to the minimum length: '))
			if maxName>=minName:
				break
			else:
				raise ValueError
		except:
			print("That's not a valid number for this input! Please try again!")
			continue
	#number of names to generate
	while True:
		try:
			number=int(input('How many name(s) do you want? Enter a positive integer: '))
			if number>=1:
				break
			else:
				raise ValueError
		except:
			print("That's not a valid number for this input! Please try again!")
			continue
	for x in range(number):
		print(name.buildName(minName,maxName))
	a=input('Would you like to go again? Enter Y for yes and N for no: ')
	if a=='N' or a=='n':
		break
	else:
		continue
