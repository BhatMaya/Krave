# Python Intermediate Object Oriented Programming #3 - Class Methods and Static Methods



class House: 

	roof = True
	
	#the init() method is called as soon as the instance is created- meaning that we don't have to call it- python will call it for us
	def __init__(self, doors, windows, floors): 
		self.doors = doors
		self.windows = windows
		self.floors = floors

	@classmethod #turning this method into a class method
	def myMethod(cls, roof):
		cls.roof = roof

#doesn't deal with the instance of the class OR with the class itself
	@staticmethod
	def leave_house(time_of_day): 
		print(f'Leaving house at {time_of_day}')

house1 = House(2, 6, 3)
house2 = House(2, 6, 3)

House.myMethod(False)
print(House.roof)
House.leave_house('2 PM')
house1.leave_house('3 PM')
