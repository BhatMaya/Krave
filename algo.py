from main import Restaurant, restaurant_options, additionalPosSearchTerms, additionalNegSearchTerms

### these fields will now be determined in testUI.py:

# needDelivery = True
# priceRange = ['$','$$']



# secondrestaurantoptions = restaurant_options

# final_restaurant_list = {}

# for key, value in secondrestaurantoptions.items():
#     if key.price in priceRange:  # Check if the restaurant's price is within the allowed range
#         print(key.name, 'is in price range.')
#         value = value + 1.5  # Increase the value if the price is in range
#         if key.rating >= 3.5:  # Check the restaurant's rating
#             value = value + 1.5  # Further increase if the rating is 3.5 or higher
#             final_restaurant_list[key] = value  # Add to the final list
#         else:
#             value = value - 0.3  # Decrease if the rating is below 3.5
#             if key.rating >= 3:
#                 final_restaurant_list[key] = value  # Add to the final list if the rating is 3 or higher
#             else:
#                 value = value - 2.5  # Further decrease if the rating is below 3
#                 final_restaurant_list[key] = value  # Add to the final list
#     else:
#         value = value - 0.5  # Decrease the value if the price is not in the allowed range
#         if maxPrice + '$' == str(key.price):  # Check if the price has one more $ sign
#             if key.rating >= 3.5:
#                 value = value + 0.5  # Slightly increase if the rating is 3.5 or higher
#                 final_restaurant_list[key] = value
#             else:
#                 value = value - 0.3  # Decrease if the rating is below 3.5
#                 if key.rating >= 3:
#                     final_restaurant_list[key] = value
#                 else:
#                     value = value - 2.5  # Further decrease if the rating is below 3
#                     final_restaurant_list[key] = value
#         else:
#             if key.rating >= 3.5:
#                 value = value + 0.2  # Slightly increase if the rating is 3.5 or higher
#                 final_restaurant_list[key] = value
#             else:
#                 value = value - 0.5  # Decrease if the rating is below 3.5
#                 if key.rating >= 3:
#                     final_restaurant_list[key] = value
#                 else:
#                     value = value - 2.5  # Further decrease if the rating is below 3
#                     final_restaurant_list[key] = value
   
#     # now time to go through additional search terms POSITIVE:
#     for cuisine, relatedTerms in additionalPosSearchTerms.items():
#         for term in relatedTerms:
#             if term.upper() in key.name.upper():
#                 value = value + 0.5
#                 print('good term given weight')
#                 final_restaurant_list[key] = value

#     # now time for negative:
#     for cuisine, relatedTerms in additionalNegSearchTerms.items():
#         for term in relatedTerms:
#             if term.upper() in key.name.upper():
#                 value = value - 3
#                 print('wrong term filtered out')
#                 final_restaurant_list[key] = value
#     if needDelivery:
#         if key.delivers == False:  
#             value = 0
#             print(key.name, 'does not deliver')



# for (key, value) in final_restaurant_list.items():
#     print(key, '  raw score : ', value)
#     if value <= 0:
#         value = 0
#     else:
#         if value >= 10:
#             value = value * 8.5
#             if (value >= 100):
#                 value = value - (value % 100) - 1
#         else:
#             value = value * 10
#         print('krave score: ', value)
#     final_restaurant_list[key] = value


# sorted_final_restaurant_list = {k: v for k, v in sorted(final_restaurant_list.items(), key=lambda item: item[1], reverse=True)}


# print('Full List: ')
# for key, value in sorted_final_restaurant_list.items():
#     print(key.name, ': ', value)
   
# print('TOP 5: ')
# for i, (key, value) in enumerate(sorted_final_restaurant_list.items()):
#     if i < 5:  # Print only the first 5 items
#         print(key.name, ': ', value)
#     else:
#         break

# print('')

def rank_restaurants(price_range, needs_delivery, restaurant_options, additional_pos_search_terms, additional_neg_search_terms):
    max_price = price_range[-1]
    final_restaurant_list = {}

    for key, value in restaurant_options.items():
        if key.price in price_range:
            print(f"{key.name} is in price range.")
            value += 1.5
            if key.rating >= 3.5:
                value += 1.5
                final_restaurant_list[key] = value
            else:
                value -= 0.3
                if key.rating >= 3:
                    final_restaurant_list[key] = value
                else:
                    value -= 2.5
                    final_restaurant_list[key] = value
        else:
            value -= 0.5
            if max_price + '$' == key.price:
                if key.rating >= 3.5:
                    value += 0.5
                    final_restaurant_list[key] = value
                else:
                    value -= 0.3
                    if key.rating >= 3:
                        final_restaurant_list[key] = value
                    else:
                        value -= 2.5
                        final_restaurant_list[key] = value
            else:
                if key.rating >= 3.5:
                    value += 0.2
                    final_restaurant_list[key] = value
                else:
                    value -= 0.5
                    if key.rating >= 3:
                        final_restaurant_list[key] = value
                    else:
                        value -= 2.5
                        final_restaurant_list[key] = value

        for cuisine, related_terms in additional_pos_search_terms.items():
            for term in related_terms:
                if term.upper() in key.name.upper():
                    value += 0.5
                    print('Good term given weight')
                    final_restaurant_list[key] = value

        for cuisine, related_terms in additional_neg_search_terms.items():
            for term in related_terms:
                if term.upper() in key.name.upper():
                    value -= 3
                    print('Wrong term filtered out')
                    final_restaurant_list[key] = value

        if needs_delivery and not key.delivers:
            value = 0
            print(f"{key.name} does not deliver")
            final_restaurant_list[key] = value

    for key, value in final_restaurant_list.items():
        print(f"{key.name}  raw score : {value}")
        if value <= 0:
            value = 0
        else:
            if value >= 10:
                value *= 8.5
                if value >= 100:
                    value = value - (value % 100) - 1
            else:
                value *= 10
        print(f"Krave score: {value}")
        final_restaurant_list[key] = value

    sorted_final_restaurant_list = {k: v for k, v in sorted(final_restaurant_list.items(), key=lambda item: item[1], reverse=True)}

    return sorted_final_restaurant_list




    

### this will now be called from testUI.py for the results display: 

# sortedList = rank_restaurants(priceRange, needDelivery, restaurant_options, additionalPosSearchTerms, additionalNegSearchTerms)
# print('Full List:')
# for key, value in sortedList.items():
#     print(f"{key.name}: {value}")

# print('TOP 5:')
# for i, (key, value) in enumerate(sortedList.items()):
#     if i < 5:
#         print(f"{key.name}: {value}")
#     else:
#         break