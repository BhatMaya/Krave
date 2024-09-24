from .main import Restaurant, process_temp_list
from .algo import rank_restaurants

# global variables (nD and pR will later be determined by user input)
needDelivery = False
priceRange = []
final_map = {}
tag_points = {}
distance = 0

# Picture class 
class Picture:
    def __init__(self, image, tags):
        self.image = image
        self.tags = tags

def like_picture(picture):
    for tag in picture.tags:
        if tag in tag_points:
            tag_points[tag] += 1
        else:
            tag_points[tag] = 1

def dislike_picture(picture): 

    for tag in picture.tags:
        if tag in tag_points:
            tag_points[tag] = max(tag_points[tag] - 0.5, 0)
        else: 
            tag_points[tag] = 0 

def set_truth_value(delivery_choice): 
    needDelivery = delivery_choice
    print(needDelivery)


def set_distance(distance_choice): 
    global distance 

    distance = distance_choice
    print(distance)

def set_price_range(price_choice): 
    global priceRange 
    if (price_choice not in priceRange):
        priceRange.append(price_choice)
    if (price_choice == 'empty'):
        priceRange = []
    print(priceRange)

def remove_price_range(price_choice): 
    global priceRange
    if(price_choice in priceRange): 
        priceRange.remove(price_choice)
    print(priceRange)





def generate_related_terms_map():
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
        "indian": ['taj', 'palace', 'royal', 'mahal', 'mirchi', 'chaat', 'dosa', 'masala', 'north', 'chili', 'south', 'thali', 'taste', 'tandoori', 'jewel', 'bombay', 'india', 'maharaja', 'spice', 'bengal', 'roti'],
        "korean": [],
        "pho": ['pho'],
        "banh mi": [],
        "italian": ['pasta', 'pizzeria'],
        "pasta": [],
        "noodles": [],
        "chipotle": ['qdoba'],
        "byo": [],
    }

    global final_map
    global tag_points
    for tag, weight in tag_points.items():
        if tag in related_terms:
            final_map[tag] = {
                "weight": weight,
                "related_terms": related_terms[tag]
            }

    print("Related terms map:")
    print(final_map)



def generate_sorted_restaurants(): 

	
    global final_map	
    global distance
    global priceRange

    print("distance before passing to main", distance)
    restaurant_options, additionalPosSearchTerms, additionalNegSearchTerms = process_temp_list(final_map, distance)

    print(priceRange)
    sorted_tags = rank_restaurants(priceRange, needDelivery, restaurant_options, additionalPosSearchTerms, additionalNegSearchTerms, distance)

    return sorted_tags
