import requests

api_key2 = 'd1e6067d83cdf4'
# Get the user's public IP address
ip_response = requests.get('https://api.ipify.org?format=json')
user_ip = ip_response.json()['ip']
print(user_ip)
print(ip_response)

# Make the API request to get geolocation
geo_response = requests.get(f'http://ipinfo.io/{user_ip}/json?token={api_key2}')

# Check if the request was successful
if geo_response.status_code == 200:
    data = geo_response.json()
    loc = data.get('loc', '').split(',')
    if len(loc) == 2:
        latitude = loc[0]
        longitude = loc[1]
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
    else:
        print("Location data not available")
else:
    print("Error: Could not retrieve data")


###############################################
api_url = 'https://api.yelp.com/v3/businesses/search'
api_key = 'TEDWqCrmKb_w37qkJjS426xfoUGpBF1EQBdjxcJtKeXHgJEvAmCW4zFKrHFDvuUGN_ELrNQgEOzaK9taFY-DwvpjiPx1d7xtM5cZ3vnXA2gfEeCgAsAa32_cZY1rZnYx'

HEADERS = {'Authorization': f'Bearer {api_key}'}


latitude = loc[0]#47.656610017739375#47.6163
longitude = loc[1]#-122.31540319155656#-122.0356


params = {
    'term': 'mexican',
    'latitude': latitude,
    'longitude': longitude,
    'radius': 2000,  # Radius in meters (5 miles)
    'limit': 20  # Number of results to return (maximum is 50)
}
   
# Make a request to the Yelp API
response = requests.get(api_url, headers=HEADERS, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    for business in data.get('businesses', []):
        if business.get('price') == "$":
            print(business['name'], business['location']['address1'])
        if business.get('price') == "$$":
            print(business['name'], business['location']['address1'])
   
   
       
else:
    print(f'Error: {response.status_code}')

