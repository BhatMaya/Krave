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
from backend import Picture,  needDelivery, priceRange, generate_sorted_restaurants, generate_related_terms_map, like_picture, dislike_picture
from main import Restaurant, process_temp_list
from algo import rank_restaurants



# main UI screen for swiping: contains pictures, swiping algo, map generation 
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # u.user_prefs = UserPreferences()

        self.pictures = [
            Picture("tacos.png", ["tacos", "mexican", "latin"]),
            Picture("pizza.png", ["pizza", "italian"]),
            Picture("burger.png", ["burger", "sit-down"]),
            Picture("chinese.png", ["chinese", "rice"]),
            Picture("burger2.png", ["burger"]),
            Picture("sandwich.png", ["sandwich", "byo", "healthy"]),
            Picture("salad.png", ['salad', 'healthy', 'byo']),
            Picture("thai.png", ["thai", "curry", "rice"]),
            Picture("breakfast .png", ["breakfast"]),
            Picture("fries .png", ["fries", "burger"]),
            Picture("indian curry rice .png", ["indian", "curry", "rice"]),
            Picture("indian curry rice 2.png", ["indian", "curry", "rice"]),
            Picture("korean .png", ["korean"]),
            Picture("italian restaurant .png", ["italian", "sit-down", "pasta"]),
        ]

        self.current_picture_index = 0

        layout = FloatLayout()

        # creating image widgets & formatting 
        self.image_widget = Image(source=self.pictures[self.current_picture_index].image, size_hint = (None, None),size=(500,500), allow_stretch=True, keep_ratio=True, pos_hint={"center_x": 0.5, "center_y": 0.6})
        self.add_border(self.image_widget)
        layout.add_widget(self.image_widget)

        # button widgets & formatting 
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


    def like_current_picture(self, instance):
        current_picture = self.pictures[self.current_picture_index]
        like_picture(current_picture)
        self.show_next_picture()

    def dislike_current_picture(self, instance):
        current_picture = self.pictures[self.current_picture_index]
        dislike_picture(current_picture)
        self.show_next_picture()

    def show_next_picture(self, *args):
        if self.current_picture_index + 1 < len(self.pictures):
            self.current_picture_index += 1
            self.image_widget.source = self.pictures[self.current_picture_index].image
            self.image_widget.pos = (self.image_widget.parent.width * 0.1, self.image_widget.pos[1])
        else:
            generate_related_terms_map()
            self.show_results_screen()

    def show_results_screen(self):
        self.manager.current = 'results'
        self.manager.get_screen('results').display_results()

    def disable_buttons(self):
        self.like_button.disabled = True
        self.dislike_button.disabled = True

    # def generate_related_terms_map(self):
    #     related_terms = {
    #         "tacos": ['taqueria', 'al pastor', 'birria'],
    #         "mexican": ["casita", "la", "tacos", "el", 'agua', 'verde', 'roja', 'loco'],
    #         "pizza": ["stone", 'pagliacci', 'domino', 'papa', 'mod'],
    #         "italian": ['pizzeria', 'luigi', 'italiano', 'traditional'],
    #         "burger": ['cow', 'fat', 'big', 'chick', 'chicken', 'hungry'],
    #         "chinese": ['dan', 'din', 'chiang', 'xian', 'noodle', 'dumpling', 'hong kong', 'shangai'],
    #         "rice": [],
    #         "sit-down": ['house', 'tavern'],
    #         "sandwich": ['sub', 'deli'],
    #         "byo": ['bowl', 'salad', 'chipotle', 'sandwich', 'sub', 'mod'],
    #         "healthy": [],
    #         "salad": ['green', 'wild'],
    #         "thai": ['khao', 'kai', '65', 'thai', 'bai tong', 'ginger', 'basil', 'bangkok', 'noodle'],
    #         "curry": ['katsu', 'jalfrezi', 'vindaloo', 'butter chicken', 'india', 'chili', 'taj', 'palace', 'royal', 'mahal', 'north'],
    #         "breakfast": ['pancake', 'waffle', 'house'],
    #         "fries": ['crispy', 'fry', 'burger', 'bottomless'],
    #         "indian": ['taj', 'palace', 'royal', 'mahal', 'mirchi', 'chaat', 'dosa', 'masala', 'north', 'chili', 'south', 'thali', 'taste'],
    #         "korean": [],
    #         "pho": ['pho'],
    #         "banh mi": [],
    #         "italian": ['pasta', 'pizzeria'],
    #         "pasta": [],
    #     }

    #     global final_map
    #     for tag, weight in self.user_prefs.tag_points.items():
    #         if tag in related_terms:
    #             final_map[tag] = {
    #                 "weight": weight,
    #                 "related_terms": related_terms[tag]
    #             }


    #     print("Related terms map:")
    #     print(final_map)



# results screen: calls to api based on user prefs from swipe screen, runs algo on it, and displays 
class ResultsScreen(Screen):
    
    # constructor 
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)

    # calls api using main.py method, ranks restaurants with algo.py method, and displays results 
    def display_results(self):
        self.layout.clear_widgets()

        global final_map

        # restaurant_options, additionalPosSearchTerms, additionalNegSearchTerms = process_temp_list(final_map)

        # sorted_tags = rank_restaurants(priceRange, needDelivery, restaurant_options, additionalPosSearchTerms, additionalNegSearchTerms)
        final_list = generate_sorted_restaurants()
        top_three = {}

        # pull first 3 restaurants from list 
        count = 0
        for key, value in final_list.items():
            count=count+1
            if count > 3:
                break
            else:
                print(f"{key.name}: {value}")
                top_three[key] = value


        podium_layout = FloatLayout()
        count2 = 0
        for restaurant, score in (top_three.items()):
            
            podium_pos = {"center_x": 0.5, "center_y": 0.85 -  count2 * 0.2}
            count2 = count2 + 1
            label = Button(
                text=f'{restaurant.name}. {score} ',
                size_hint=(0.8, 0.1),
                pos_hint=podium_pos,
                background_color=(0.2, 0.2, 0.8, 1),  # Dark blue background
                background_normal='',
                color=(1, 1, 1, 1),  # White text
                font_size='24sp',
                bold=True
            )
            rating = restaurant.rating
            distance = restaurant.distance
            label.bind(on_press=lambda btn: self.show_popup(btn.text, rating, distance, score))
            podium_layout.add_widget(label)

        self.layout.add_widget(podium_layout)

    def show_popup(self, text, rating, distance, score):
        tag = text[:-5]  # Extract tag from button text
        content = FloatLayout()
        content.add_widget(Label(text=f"Distance: {distance}", size_hint=(0.8, 0.8), pos_hint={"center_x": 0.2, "center_y": 0.7}))
        content.add_widget(Label(text=f"Rating: {rating}", size_hint=(0.8, 0.8), pos_hint={"center_x": 0.2, "center_y": 0.6}))

        popup = Popup(
            title=f"{tag}",
            content=content,
            size_hint=(0.8, 0.8),
            background_color=(0.5, 0.5, 0.5, 1)  # Gray background
        )
        popup.open()

# main app run 
class FoodRatingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ResultsScreen(name='results'))
        return sm

if __name__ == '__main__':
    FoodRatingApp().run()
