# Importing necessary modules from Kivy
from kivy.app import App  # Main Kivy app class
from kivy.uix.boxlayout import BoxLayout  # Layout class for arranging widgets
from kivy.uix.image import Image  # Widget class for displaying images
from kivy.uix.button import Button  # Widget class for creating buttons

class Picture: 
    def __init__(self, image, tags): 
        self.image = image  # this could be the path to the image or the image object 
        self.tags = tags  # a list of strings like [tacos, mexican, latin]

class UserPreferences: 
    def __init__(self): 
        """
        Initialize a UserPreferences object with an empty dictionary to store tags and their point values
        """
        self.tag_points = {}  # dictionary that holds the tag-point mappings

    def like_picture(self, picture): 
        """
        Update the tag_points dict whenever a picture is liked

        param: a Picture object that a user likes 
        """
        for tag in picture.tags: 
            if tag in self.tag_points:  # if the tag is already in the dictionary 
                self.tag_points[tag] += 1  # increment the point value by 1
            else:  
                self.tag_points[tag] = 1  # add the tag with the initial point value of 1

class FoodRatingApp(App): 
    def build(self): 
        """Building the App's UI and initializing its state"""

        self.user_prefs = UserPreferences()  # creating an instance of UserPreferences to track the points

        # list of dummy Picture objects
        self.pictures = [
            Picture("tacos.png", ["tacos", "mexican", "latin"]),
            Picture("pizza.png", ["pizza", "italian"]),
            Picture("burger.png", ["burger", "sit-down"]),
            Picture("chinese.png", ["chinese", "rice"]),
            Picture("burger2.png", ["burger"]),
            Picture("sandwich.png", ["sandwich", "byo", "healthy"]),
            Picture("salad.png", ['salad', 'healthy', 'byo'])
        ]

        self.current_picture_index = 0  # this keeps track of the current picture that is being shown

        layout = BoxLayout(orientation='vertical')
        self.image_widget = Image(source=self.pictures[self.current_picture_index].image)
        layout.add_widget(self.image_widget)

        self.like_button = Button(text='Like')
        self.like_button.bind(on_press=self.like_current_picture)  # Bind the button press to a function
        layout.add_widget(self.like_button)

        self.dislike_button = Button(text='Dislike')
        self.dislike_button.bind(on_press=self.dislike_current_picture)
        layout.add_widget(self.dislike_button)

        return layout  # Return the layout object

    def like_current_picture(self, instance): 
        """
        This function will handle the event for when the user likes the picture

        param: instance of when the button is triggered
        """
        current_picture = self.pictures[self.current_picture_index]  # get the current picture object 
        self.user_prefs.like_picture(current_picture)  # update with current picture's tags
        self.show_next_picture()

    def dislike_current_picture(self, instance): 
        """
        This function will handle the event for when the user dislikes the picture

        param: instance of when the button is triggered
        """
        current_picture = self.pictures[self.current_picture_index]
        for tag in current_picture.tags: 
            if tag in self.user_prefs.tag_points: 
                self.user_prefs.tag_points[tag] = max(self.user_prefs.tag_points[tag] - 0.5, 0)
        self.show_next_picture()

    def show_next_picture(self): 
        """
        Moves to the next picture if available; otherwise, indicates that all pictures have been rated.
        """
        if self.current_picture_index + 1 < len(self.pictures): 
            self.current_picture_index += 1
            self.image_widget.source = self.pictures[self.current_picture_index].image
        else: 
            print("All pictures have been rated")
            print(self.user_prefs.tag_points)
            self.generate_related_terms_map()
            self.disable_buttons()

    def disable_buttons(self): 
        """Disables the like and dislike buttons."""
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
            "salad": ['green', 'wild']
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

if __name__ == '__main__': 
    FoodRatingApp().run()
