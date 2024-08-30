from main import Restaurant, process_temp_list
from algo import rank_restaurants

# global variables (nD and pR will later be determined by user input)
needDelivery = False
priceRange = ['$','$$']
final_map = {}

# Picture class 
class Picture:
    def __init__(self, image, tags):
        self.image = image
        self.tags = tags

# creates tag_points map 
class UserPreferences:
    def __init__(self):
        self.tag_points = {}

    def like_picture(self, picture):
        for tag in picture.tags:
            if tag in self.tag_points:
                self.tag_points[tag] += 1
            else:
                self.tag_points[tag] = 1



    def generate_related_terms_map(self):
    	related_terms = {
            "tacos": ['taqueria', 'al pastor', 'birria'],
            "mexican": ["casita", "la", "tacos", "el", 'agua', 'verde', 'roja', 'loco'],
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
            "curry": ['katsu', 'jalfrezi', 'vindaloo', 'butter chicken', 'india', 'chili', 'taj', 'palace', 'royal', 'mahal', 'north'],
            "breakfast": ['pancake', 'waffle', 'house'],
            "fries": ['crispy', 'fry', 'burger', 'bottomless'],
            "indian": ['taj', 'palace', 'royal', 'mahal', 'mirchi', 'chaat', 'dosa', 'masala', 'north', 'chili', 'south', 'thali', 'taste'],
            "korean": [],
            "pho": ['pho'],
            "banh mi": []
        }

       global final_map
       for tag, weight in self.user_prefs.tag_points.items():
           if tag in related_terms:
               final_map[tag] = {
                   "weight": weight,
                   "related_terms": related_terms[tag]
               }


        print("Related terms map:")
        print(final_map)