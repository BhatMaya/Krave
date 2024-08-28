from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class Picture:
    def __init__(self, image, tags):
        self.image = image
        self.tags = tags

class UserPreferences:
    def __init__(self):
        self.tag_points = {}

    def like_picture(self, picture):
        for tag in picture.tags:
            if tag in self.tag_points:
                self.tag_points[tag] += 1
            else:
                self.tag_points[tag] = 1

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.user_prefs = UserPreferences()

        self.pictures = [
            Picture("tacos.png", ["tacos", "mexican", "latin"]),
            Picture("pizza.png", ["pizza", "italian"]),
            Picture("burger.png", ["burger", "sit-down"]),
            Picture("chinese.png", ["chinese", "rice"]),
            Picture("burger2.png", ["burger"]),
            Picture("sandwich.png", ["sandwich", "byo", "healthy"]),
            Picture("salad.png", ['salad', 'healthy', 'byo']),
            Picture("thai.png", ["thai", "curry", "rice"])
        ]

        self.current_picture_index = 0

        layout = FloatLayout()

        # Image Widget
        self.image_widget = Image(source=self.pictures[self.current_picture_index].image, size_hint=(0.8, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.6})
        self.add_border(self.image_widget)
        layout.add_widget(self.image_widget)

        # Buttons
        button_layout = BoxLayout(size_hint=(0.8, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.1})
        button_layout.orientation = 'horizontal'
        button_layout.spacing = 10

        self.dislike_button = Button(
            text='Dislike',
            size_hint=(0.4, 1),
            background_color=(1, 0, 0, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        self.dislike_button.bind(on_press=self.dislike_current_picture)
        button_layout.add_widget(self.dislike_button)

        self.like_button = Button(
            text='Like',
            size_hint=(0.4, 1),
            background_color=(0, 1, 0, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        self.like_button.bind(on_press=self.like_current_picture)
        button_layout.add_widget(self.like_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def add_border(self, widget):
        with widget.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Gray border
            self.border = RoundedRectangle(size=widget.size, pos=widget.pos, radius=[20])
            widget.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, instance, value):
        self.border.size = instance.size
        self.border.pos = instance.pos

    def swipe_animation(self, direction):
        if direction == "left":
            animation = Animation(x=-self.image_widget.width, duration=0.5)
        else:
            animation = Animation(x=self.image_widget.parent.width, duration=0.5)

        animation.bind(on_complete=self.show_next_picture)
        animation.start(self.image_widget)

    def like_current_picture(self, instance):
        current_picture = self.pictures[self.current_picture_index]
        self.user_prefs.like_picture(current_picture)
        self.swipe_animation('right')

    def dislike_current_picture(self, instance):
        current_picture = self.pictures[self.current_picture_index]
        for tag in current_picture.tags:
            if tag in self.user_prefs.tag_points:
                self.user_prefs.tag_points[tag] = max(self.user_prefs.tag_points[tag] - 0.5, 0)
        self.swipe_animation('left')

    def show_next_picture(self, *args):
        if self.current_picture_index + 1 < len(self.pictures):
            self.current_picture_index += 1
            self.image_widget.source = self.pictures[self.current_picture_index].image
            self.image_widget.pos = (self.image_widget.parent.width * 0.1, self.image_widget.pos[1])
        else:
            self.show_results_screen()

    def show_results_screen(self):
        self.manager.current = 'results'
        self.manager.get_screen('results').display_results(self.user_prefs.tag_points)

    def disable_buttons(self):
        self.like_button.disabled = True
        self.dislike_button.disabled = True

    def generate_related_terms_map(self):
        related_terms = {
            "tacos": [],
            "mexican": ["casita", "la", "tacos", "el"],
            "pizza": ["stone", 'pagliacci', 'domino', 'papa', 'mod'],
            "italian": ['pizzeria', 'luigi', 'italiano', 'traditional'],
            "burger": ['cow', 'fat', 'big', 'chick', 'chicken', 'hungry'],
            "chinese": ['dan', 'din', 'chiang', 'xian', 'noodle', 'dumpling', 'hong kong', 'shangai'],
            "rice": [],
            "sit-down": ['house', 'tavern'],
            "sandwich": ['sub', 'deli'],
            "byo": ['bowl', 'salad', 'chipotle', 'sandwich', 'sub', 'mod'],
            "healthy": [],
            "salad": ['green', 'wild'],
            "thai": ['khao', 'kai', '65', 'thai', 'bai tong', 'ginger', 'basil', 'bangkok', 'noodle'],
            "curry": []
        }

        final_map = {}
        for tag, weight in self.user_prefs.tag_points.items():
            if tag in related_terms:
                final_map[tag] = {
                    "weight": weight,
                    "related_terms": related_terms[tag]
                }

        print("Related terms map:")
        print(final_map)

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

    def display_results(self, tag_points):
        self.layout.clear_widgets()

        sorted_tags = sorted(tag_points.items(), key=lambda x: x[1], reverse=True)
        top_three = sorted_tags[:3]

        podium_layout = FloatLayout()
        for idx, (tag, weight) in enumerate(top_three):
            podium_pos = {"center_x": 0.5, "center_y": 0.7 - idx * 0.3}
            label = Button(
                text=f'{idx + 1}. {tag} ({weight:.1f})',
                size_hint=(0.8, 0.1),
                pos_hint=podium_pos,
                background_color=(0.2, 0.2, 0.8, 1),  # Dark blue background
                background_normal='',
                color=(1, 1, 1, 1),  # White text
                font_size='24sp',
                bold=True
            )
            label.bind(on_press=lambda btn: self.show_popup(btn.text))
            podium_layout.add_widget(label)

        self.layout.add_widget(podium_layout)

    def show_popup(self, text):
        tag = text.split(' ')[1]  # Extract tag from button text
        content = FloatLayout()
        content.add_widget(Label(text=f"More information about {tag}", size_hint=(0.8, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.5}))

        popup = Popup(
            title=f"{tag} Details",
            content=content,
            size_hint=(0.8, 0.8),
            background_color=(0.5, 0.5, 0.5, 1)  # Gray background
        )
        popup.open()

class FoodRatingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ResultsScreen(name='results'))
        return sm

if __name__ == '__main__':
    FoodRatingApp().run()
