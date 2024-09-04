from stats import standardizationProcess, standardDeviation

def rank_restaurants(price_range, needs_delivery, restaurant_options, additional_pos_search_terms, additional_neg_search_terms):
    restaurant_options = standardizationProcess(restaurant_options)
    max_price = price_range[-1]
    final_restaurant_list = {}

    stdAdjustment = standardDeviation(restaurant_options) * 0.1

    for key, value in restaurant_options.items():
        # if needs delivery & restaurant doesn't deliver, eliminate as option 
        replaceVal = value
        if needs_delivery and not key.delivers:
            replaceVal = 0
            final_restaurant_list[key] = replaceVal
        else:
            # price deductions 
            if key.price not in price_range:
                replaceVal = value - 0.2
                if max_price + '$' != key.price:
                    replaceVal = replaceVal - 0.7 # maybe 0.6 we'll see
            # rating deductions 
            if key.rating < 4.5: 
                replaceVal = replaceVal - 0.025
            if key.rating < 4:
                replaceVal = replaceVal - 0.05
            if key.rating < 3.5:
                replaceVal = replaceVal - 0.15
            if key.rating < 3:
                replaceVal = replaceVal - 0.3
            # may remove, but for now if rating is 1 star eliminate it 
            if key.rating == 1: 
                replaceVal == 0

            # negative search terms filtering
            for cuisine, related_terms in additional_neg_search_terms.items():
                for term in related_terms:
                    if term.upper() in key.name.upper():
                        replaceVal -= 2

            # positive search terms filtering 
            for cuisine, related_terms in additional_pos_search_terms.items():
                for term in related_terms:
                    if (term.upper() in key.name.upper()) and replaceVal < 10:
                        replaceVal += 0.2 * (10 - replaceVal)

            replaceVal = replaceVal - stdAdjustment
        final_restaurant_list[key] = round(replaceVal * 10, 3)

    sorted_final_restaurant_list = {k: v for k, v in sorted(final_restaurant_list.items(), key=lambda item: item[1], reverse=True)}
    print(sorted_final_restaurant_list)

    return sorted_final_restaurant_list


