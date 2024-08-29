
def rank_restaurants(price_range, needs_delivery, restaurant_options, additional_pos_search_terms, additional_neg_search_terms):
    max_price = price_range[-1]
    final_restaurant_list = {}

    for key, value in restaurant_options.items():
        if key.price in price_range:
            # print(f"{key.name} is in price range.")
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
                    # print('Good term given weight')
                    final_restaurant_list[key] = value

        for cuisine, related_terms in additional_neg_search_terms.items():
            for term in related_terms:
                if term.upper() in key.name.upper():
                    value -= 3
                    # print('Wrong term filtered out')
                    final_restaurant_list[key] = value

        if needs_delivery and not key.delivers:
            value = 0
            # print(f"{key.name} does not deliver")
            final_restaurant_list[key] = value

    for key, value in final_restaurant_list.items():
        # print(f"{key.name}  raw score : {value}")
        if value <= 0:
            value = 0
        else:
            if value >= 10:
                value *= 8.5
                while value >= 100:
                    value = value - (value % 100) - 1
            else:
                value *= 10
        final_restaurant_list[key] = value

    sorted_final_restaurant_list = {k: v for k, v in sorted(final_restaurant_list.items(), key=lambda item: item[1], reverse=True)}

    return sorted_final_restaurant_list



