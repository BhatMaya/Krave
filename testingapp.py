from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class MyLayout(BoxLayout): 
	def __init__(self): 
		super().__init__()
		self.button = Button(text='Press me')
		self.button.bind(on_press=function)

		def new_label(self, button):
			self.label = Label('my new label')
			self.add_widget(self.label)

		self.add_widget(self.button)


class MyApp(App): 
	def build(self): 
		return MyLayout()


if __name__ == '__main__':
	MyApp().run()