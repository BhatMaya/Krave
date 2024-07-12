from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Add label at the top
        label = Label(text='Krave', font_size=40, color=(0.5, 0, 0.5, 1), size_hint=(1, 0.2))
        layout.add_widget(label)

        # Create a horizontal layout for the middle part
        middle_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))

        # Add buttons and canvas widget
        button_left = Button(text='<', font_size=40, on_press=self.change_to_red, size_hint=(0.1, 1))
        self.canvas_widget = CanvasWidget(size_hint=(0.8, 1))
        button_right = Button(text='>', font_size=40, on_press=self.change_to_green, size_hint=(0.1, 1))

        middle_layout.add_widget(button_left)
        middle_layout.add_widget(self.canvas_widget)
        middle_layout.add_widget(button_right)

        layout.add_widget(middle_layout)
        self.add_widget(layout)

    def change_to_red(self, instance):
        self.canvas_widget.change_color('red')

    def change_to_green(self, instance):
        self.canvas_widget.change_color('green')

class CanvasWidget(Widget):
    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        with self.canvas:
            self.color = Color(0, 0, 0, 1)  # Default black color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def change_color(self, color):
        if color == 'red':
            self.color.rgba = (1, 0, 0, 1)  # Red color
        elif color == 'green':
            self.color.rgba = (0, 1, 0, 1)  # Green color

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

class KraveApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    KraveApp().run()