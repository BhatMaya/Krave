import requests 

class Restaurant:
    def __init__(self, name, address, price, rating, latitude, longitude, is_closed, distance, delivers):
        self.name = name
        self.address = address
        self.price = price
        self.rating = float(rating)
        self.latitude = latitude
        self.longitude = longitude
        self.is_closed = is_closed
        self.distance = distance
        self.delivers = delivers
        self.cuisines = []


    def __repr__(self):
        return f"{self.name} ({self.price}) - {self.rating} stars - {self.address} - {'Closed' if self.is_closed else 'Open'} - {self.distance} meters away"

    def __eq__(self, other):
        if isinstance(other, Restaurant):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


def process_temp_list(temp_list, distance):
    # global api_url, headers, params
    api_url = 'https://api.yelp.com/v3/businesses/search'
    api_key = 'mx5lelJJcAekm2elNILMonEbvbMAUeQCrltMXawwfpzM3g-ygJ9kUy0atWWlEFh8ll2MCTXj7DAtAMP72Zkx4-0i1vD2Vy-y93AEQ1LwRdcqd1b-Hk82LlubQYzkZnYx'
    HEADERS = {'Authorization': f'Bearer {api_key}'}

    latitude = 47.656610017739375 #47.60456
    longitude = -122.31540319155656 #-122.03368
    meters = round(1609.344*distance)


    params = {
        'term': 'restaurant',
        'latitude': latitude,
        'longitude': longitude,
        'radius': meters,  # Radius in meters (5 miles)
        'limit': 25  # Number of results to return (maximum is 50)
    }


    restaurant_options = {}
    additionalPosSearchTerms = {}
    additionalNegSearchTerms = {}

    for key, value in temp_list.items():
        if value['weight'] != 0:
            if len(value['related_terms']) != 0:
                additionalPosSearchTerms[key] = value['related_terms']
            
            params['term'] = key
            print(params)  # For testing
            
            # Make a request to the Yelp API
            response = requests.get(api_url, headers=HEADERS, params=params)
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                for business in data.get('businesses', []):
                    restaurant = Restaurant(
                        name=business['name'],
                        address=business['location']['address1'],
                        price=str(business.get('price', 'N/A')),
                        rating=business.get('rating', 0),
                        latitude=business['coordinates']['latitude'],
                        longitude=business['coordinates']['longitude'],
                        is_closed=business.get('is_closed', True),
                        distance=business.get('distance', 0),
                        delivers='delivery' in business.get('transactions', [])
                    )
                    
                    if restaurant in restaurant_options:
                        restaurant_options[restaurant] *= value['weight']
                    else:
                        restaurant_options[restaurant] = value['weight']
            else:
                print(f"Error {response.status_code} while fetching data from Yelp API")
        else:
            if len(value['related_terms']) != 0:
                additionalNegSearchTerms[key] = value['related_terms']
    

    return restaurant_options, additionalPosSearchTerms, additionalNegSearchTerms




def get_details(name, address):

    api_url = 'https://api.yelp.com/v3/businesses/search'
    api_key = 'mx5lelJJcAekm2elNILMonEbvbMAUeQCrltMXawwfpzM3g-ygJ9kUy0atWWlEFh8ll2MCTXj7DAtAMP72Zkx4-0i1vD2Vy-y93AEQ1LwRdcqd1b-Hk82LlubQYzkZnYx'
    HEADERS = {'Authorization': f'Bearer {api_key}'}

    rstr_name = name
    location = address


    attributes = []
    cuisine = []

    params = {
        'term': rstr_name,  
        'location': address
    }

    
    response = requests.get(api_url, headers=HEADERS, params=params)
    search_results = response.json()

    
    if search_results['businesses']:
        restaurant_id = search_results['businesses'][0]['id']  # Get the business ID of the first result
        details_url = f'https://api.yelp.com/v3/businesses/{restaurant_id}'

        # Step 2: Get detailed business info
        response = requests.get(details_url, headers=HEADERS)
        restaurant_details = response.json()

        # Step 3: Populate cuisine array
        cuisine = [category['title'] for category in restaurant_details.get('categories', [])]

        # Step 4: Populate attributes array (you can add more attributes here as needed)
        attributes = []

        # Example: Check if restaurant is good for kids
        if restaurant_details.get('attributes', {}).get('GoodForKids', None):
            attributes.append('Good for Kids')

        # Example: Check if restaurant has vegetarian-friendly options (infer from categories)
        if any('Vegetarian' in category['title'] for category in restaurant_details.get('categories', [])):
            attributes.append('Vegetarian Friendly')

        # Example: Check if restaurant has WiFi
        if restaurant_details.get('attributes', {}).get('WiFi', None):
            attributes.append('WiFi Available')

        # You can add more attribute checks based on your needs
        # Step 5: Print the populated lists
        print(f'Cuisine: {cuisine}')
        print(f'Attributes: {attributes}')
    else:
        print('No restaurant found with the given name and address.')

    return cuisine, attributes


    



        

    
        


