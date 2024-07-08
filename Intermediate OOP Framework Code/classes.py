# Python Intermediate Object Oriented Programming #1 - Classes
# Think of classes as an instance/blueprint for an actual object that will be created using the class


class House: 
	pass # tells python to skip over the contents of the class for now 

# creating an instance
house1 = House()

house1.doors = 2
house1.windows = 4 
house1.floors = 2

print(house1.doors)
print(house1.windows)
print(house1.floors)
