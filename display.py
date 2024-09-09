from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from backend import Picture,  needDelivery, priceRange, generate_sorted_restaurants, generate_related_terms_map, like_picture, dislike_picture, set_truth_value, set_distance
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
            Picture("burger.png", ["burger"]),
            Picture("chinese.png", ["chinese", "rice"]),
            Picture("burger2.png", ["burger"]),
            Picture("sandwich.png", ["sandwich", "healthy"]),
            Picture("salad.png", ['salad', 'healthy']),
            Picture("thai.png", ["thai", "curry", "rice"]),
            Picture("breakfast .png", ["breakfast"]),
            Picture("fries .png", ["fries", "burger"]),
            Picture("indian curry rice .png", ["indian", "curry"]),
            Picture("indian curry rice 2.png", ["indian", "curry"]),
            Picture("korean .png", ["korean"]),
            Picture("italian restaurant .png", ["italian", "pasta"]),
            Picture("noodles thai .png", ["noodles", "thai"]),
            Picture("mexican chipotle byo .png", ["mexican", "chipotle"]),
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
            self.show_yes_no_page()

    # def show_results_screen(self):
    #     self.manager.current = 'results'
    #     self.manager.get_screen('results').display_results()
    def show_yes_no_page(self): 
        self.manager.current = 'yesno'
        self.manager.get_screen('yesno').display_page()

    def disable_buttons(self):
        self.like_button.disabled = True
        self.dislike_button.disabled = True



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
            label.bind(on_press=lambda btn, r=restaurant, d=distance, s=score: self.show_popup(r.name, r.rating, d, s))
            podium_layout.add_widget(label)

        self.layout.add_widget(podium_layout)

    def show_popup(self, text, rating, distance, score):
        tag = text  # Extract tag from button text
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

    def show_yes_no_page(self): 
        self.manager.current = 'yesno'
        self.manager.get_screen('yesno').display_page()


class YesNoPage(Screen): 
    #constructor 
    def __init__(self, **kwargs): 
        super(YesNoPage,self).__init__(**kwargs)
        self.layout = FloatLayout()
        self.add_widget(self.layout)


    #displaying the yes/no page

    def display_page(self):
        self.layout.clear_widgets
        self.add_widget(Label(text=f"Needs Delivery?", size_hint=(3,3), pos_hint={"center_x":0.1, "center_y":0.8}, bold=True))
        self.add_widget(Label(text=f"Distance?", size_hint=(3,3), pos_hint={"center_x":0.08, "center_y": 0.6}, bold=True))
        # button widgets & formatting 
        button_layout = BoxLayout(size_hint=(0.2, 0.1), pos_hint={"center_x": 0.3, "center_y": 0.8})
        button_layout.orientation = 'horizontal'
        button_layout.spacing = 10

        self.yes_delivery = Button(
            text='Yes',
            size_hint=(0.4, 1),
            background_color=(0, 0.5, 0, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True

        )
        button_layout.add_widget(self.yes_delivery)
        self.yes_delivery.bind(on_press=self.click_yes_button)
        

        self.no_delivery = Button(
            text='No',
            size_hint=(0.4, 1),
            background_color=(0.5, 0, 0, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True

        )

        button_layout.add_widget(self.no_delivery)
        self.no_delivery.bind(on_press=self.click_no_button)




        self.layout.add_widget(button_layout)


        confirm_button = Button(text="Confirm", size_hint=(None, None), size = (300,300), bold=True)
        confirm_button.pos_hint={"center_x": 0.5, "center_y": 0.1}
        self.add_widget(confirm_button)


        def on_confirm_press(instance): 
            if (main_button.text == "<1 mile"):
                set_distance(1)
            elif (main_button.text == "3 miles"):
                set_distance(3)
            elif (main_button.text == "5 miles"):
                set_distance(5)
            elif (main_button.text == "7 miles"):
                set_distance(7)
            elif (main_button.text == "10 miles"):
                set_distance(10)
            else:
                print("no distance given")

            self.show_results_screen()


        confirm_button.bind(on_press=on_confirm_press)




        #########add the dropdown menu##########

        #creating the main layout
        dropdown_layout = FloatLayout()

        dropdown = DropDown()

        #create the buttons that will go inside the dropdown(5,10,15,20+ miles)
        for option in ["<1 mile" ,"3 miles", "5 miles", "7 miles", "10 miles"]: 
            btn = Button(text=option, size_hint_y=None, height=44, bold = True)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        #creating the main button
        main_button = Button(text='Select a distance', size_hint=(None,None), size=(300,60), bold=True)
        main_button.pos_hint={"center_x": 0.3, "center_y": 0.6}

        def on_button_click(instance):
            dropdown.open(instance)



        main_button.bind(on_release=on_button_click)


        dropdown.bind(on_select=lambda instance, x: setattr(main_button, 'text', x))
        dropdown_layout.add_widget(main_button)
        self.layout.add_widget(dropdown_layout)






    def click_yes_button(self, instance): 
        self.yes_delivery.background_color=(0, 1, 0, 1)
        self.no_delivery.background_color=(0.5, 0, 0, 1)
        set_truth_value(True)

    def click_no_button(self, instance): 
        self.no_delivery.background_color=(1, 0, 0, 1)
        self.yes_delivery.background_color=(0, 0.5, 0, 1)
        set_truth_value(False)

    def show_results_screen(self):
        self.manager.current = 'results'
        self.manager.get_screen('results').display_results() 



    










# main app run 
class FoodRatingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ResultsScreen(name='results'))
        sm.add_widget(YesNoPage(name='yesno'))
        return sm

if __name__ == '__main__':
    FoodRatingApp().run()
