# Python Intermediate Object Oriented Programming #2 - Attributes
# Think of classes as an instance/blueprint for an actual object that will be created using the class


class House: 
	
	#the init() method is called as soon as the instance is created- meaning that we don't have to call it- python will call it for us
	def __init__(self, doors, windows, floors): 
		self.doors = doors
		self.windows = windows
		self.floors = floors

house1 = House(2, 6, 3)
print(house1.doors, house1.windows, house1.floors)
