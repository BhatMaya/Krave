# Python Intermediate Object Oriented Programming #3 - Class Variables



class House: 

	roof = False
	
	#the init() method is called as soon as the instance is created- meaning that we don't have to call it- python will call it for us
	def __init__(self, doors, windows, floors): 
		self.doors = doors
		self.windows = windows
		self.floors = floors

	def clean_roof(self): 
		if House.roof: 
			print('Cleaning roof')
		else: 
			print('No roof to be cleaned')

house1 = House(2, 6, 3)
print(house1.doors, house1.windows, house1.floors)
house1.clean_roof

print(House.roof)
house1.roof = True #overrides the classes state 
print(house1.roof)

print(house1.__dict__) #prints out all the instance attributes of house1 (doors, windows, floors)
house1.clean_roof()
