
class Processor:

	def __init__(self, cores, speed): 
		self.cores = cores
		self.speed = speed


	@staticmethod
	def processing(): 
		print('Processor -> processing')




class RAM: 

	def __init__(self, capacity, speed): 
		self.capacity = capacity
		self.speed = speed

	@staticmethod
	def storing(): 
		print('RAM -> storing')


class Motherboard: 

	def __init__(self, dimm_slots, pci_slots): 
		self.dimm_slots = dimm_slots
		self.pci_slots = pci_slots

	@staticmethod
	def controlling():
		print('Motherboard -> controlling')



class Computer: 

	def __init__(self, processor, ram, motherboard): 
		self.processor = processor
		self.ram = ram
		self.motherboard = motherboard

	@staticmethod 

	def boot(): 
		print('Computer -> booting')



computer = Computer(Processor(4,3), RAM(8, 2666), Motherboard(4,3))

computer.boot()
computer.processor.processing()
computer.ram.storing()
computer.motherboard.controlling()




