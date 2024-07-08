
class Car: 
	def __init__(self, wheels, doors, engine): 
		self.wheels = wheels
		self.doors = doors
		self.engine = engine

	@staticmethod

	def drive():
		print('Driving')

	@staticmethod

	def brake(): 
		print('Braking')



class Suzuki(Car): #this means that it is inheriting everything from the Car class

	def __init__(self, wheels, doors, engine, foorwheeldrive): 
		super().__init__(wheels, doors, engine)
		self.foorwheeldrive = foorwheeldrive
	
	@staticmethod 
	def drive(): 
		print('Driving Suzuki')


suzuki = Suzuki(4, 4, 'fast', True)
car = Car(4, 4, 'fast')

car.drive()
suzuki.drive()

print(suzuki.foorwheeldrive)