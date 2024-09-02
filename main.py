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


    def __repr__(self):
        return f"{self.name} ({self.price}) - {self.rating} stars - {self.address} - {'Closed' if self.is_closed else 'Open'} - {self.distance} meters away"

    def __eq__(self, other):
        if isinstance(other, Restaurant):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


def process_temp_list(temp_list):
    # global api_url, headers, params
    api_url = 'https://api.yelp.com/v3/businesses/search'
    api_key = '87qjzUYSUt1gI7_aZKUsEtOkafLQirJaXPiSdMVdNKJYS7f0HvaasYRJtx10VCjaPhAS4DxZVmC2VSUVjKfMUaZ9gw47usy_hOsQ15lJH4G5m24PfiRj-7ydD7K7ZnYx'
    HEADERS = {'Authorization': f'Bearer {api_key}'}

    latitude = 47.656610017739375 
    longitude = -122.31540319155656 


    params = {
        'term': 'restaurant',
        'latitude': latitude,
        'longitude': longitude,
        'radius': 1200,  # Radius in meters (5 miles)
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




