from main import Restaurant, restaurant_options, additionalPosSearchTerms, additionalNegSearchTerms

needDelivery = False 
priceRange = ['$','$$']
maxPrice = priceRange[-1]

secondrestaurantoptions = restaurant_options

final_restaurant_list = {}

# for key, value in secondrestaurantoptions.items():
#     if key.price in priceRange:
#         print(key.name, 'is in price range.')
#         value = value + 1.5
#         if key.rating >= 3.5: 
#         	value = value + 1.5
#         	final_restaurant_list[key] = value
#         else:
#         	value = value - 0.3
#         	if key.rating >= 3:
#         		final_restaurant_list[key] = value 
#         	else: 
#         		value = value - 2.5
#         		final_restaurant_list[key] = value
#     else:
#         value = value - 0.5 
#         if maxPrice+'$' == str(key.price):  # this is how i'm trying to say it's ONE more $ sign, idk if it's right 
#             if key.rating >= 3.5: 
#             	value = value + 0.5
#             	final_restaurant_list[key] = value
#             else:
#             	value = value - 0.3
#             	if key.rating >= 3:
# 	            	final_restaurant_list[key] = value
# 	            else:
# 	            	value = value - 2.5 
# 	            	final_restaurant_list[key] = value  	
# 		else:
# 	    	if key.rating >= 3.5: 
# 	        	value = value + 0.2
# 	            final_restaurant_list[key] = value
# 	    	else:
# 	        	value = value - 0.5
# 	            if key.rating >= 3:
# 	                final_restaurant_list[key] = value 
# 	            else: 
# 	            	value = value - 2.5
# 	            	final_restaurant_list[key] = value

for key, value in secondrestaurantoptions.items():
    if key.price in priceRange:  # Check if the restaurant's price is within the allowed range
        print(key.name, 'is in price range.')
        value = value + 1.5  # Increase the value if the price is in range
        if key.rating >= 3.5:  # Check the restaurant's rating
            value = value + 1.5  # Further increase if the rating is 3.5 or higher
            final_restaurant_list[key] = value  # Add to the final list
        else:
            value = value - 0.3  # Decrease if the rating is below 3.5
            if key.rating >= 3:
                final_restaurant_list[key] = value  # Add to the final list if the rating is 3 or higher
            else: 
                value = value - 2.5  # Further decrease if the rating is below 3
                final_restaurant_list[key] = value  # Add to the final list
    else:
        value = value - 0.5  # Decrease the value if the price is not in the allowed range
        if maxPrice + '$' == str(key.price):  # Check if the price has one more $ sign
            if key.rating >= 3.5: 
                value = value + 0.5  # Slightly increase if the rating is 3.5 or higher
                final_restaurant_list[key] = value
            else:
                value = value - 0.3  # Decrease if the rating is below 3.5
                if key.rating >= 3:
                    final_restaurant_list[key] = value
                else: 
                    value = value - 2.5  # Further decrease if the rating is below 3
                    final_restaurant_list[key] = value
        else:
            if key.rating >= 3.5:
                value = value + 0.2  # Slightly increase if the rating is 3.5 or higher
                final_restaurant_list[key] = value
            else:
                value = value - 0.5  # Decrease if the rating is below 3.5
                if key.rating >= 3:
                    final_restaurant_list[key] = value
                else: 
                    value = value - 2.5  # Further decrease if the rating is below 3
                    final_restaurant_list[key] = value
    
    # now time to go through additional search terms POSITIVE: 
    for cuisine, relatedTerms in additionalPosSearchTerms.items():
        for term in relatedTerms:
            if term.upper() in key.name.upper():
                value = value + 0.5
                print('good term given weight')
                final_restaurant_list[key] = value

    # now time for negative:
    for cuisine, relatedTerms in additionalNegSearchTerms.items():
        for term in relatedTerms:
            if term.upper() in key.name.upper():
                value = value - 3
                print('wrong term filtered out')
                final_restaurant_list[key] = value



for (key, value) in final_restaurant_list.items(): 
	print(key, '  raw score : ', value)
	if value <= 0:
		value = 0 
	else:
		if value >= 10:
			value = value * 8.5
			if (value >= 100):
				value = value - (value % 100) - 1
		else:
			value = value * 10
		print('krave score: ', value)
	final_restaurant_list[key] = value


sorted_final_restaurant_list = {k: v for k, v in sorted(final_restaurant_list.items(), key=lambda item: item[1], reverse=True)}

# print(final_restaurant_list)
# print(secondary_options) 


print('Full List: ')
for key, value in sorted_final_restaurant_list.items():
    print(key.name, ': ', value)
    
print('TOP 5: ')
for i, (key, value) in enumerate(sorted_final_restaurant_list.items()):
    if i < 5:  # Print only the first 5 items
        print(key.name, ': ', value)
    else:
        break

print('')



    



