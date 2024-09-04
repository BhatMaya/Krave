from main import Restaurant
import statistics 


# returns weights, the list of values/frequencies to give to defineQuartiles 
def prepForStats(restaurant_options):
    weights = []
    for key, value in restaurant_options.items():
        weights.append(value)
    weights.sort()
    return weights

# returns array split_vals of length 3, where split[i] is the next value to split restaurant_options at 
def defineQuartiles(weights):
    split_vals = []
    weights.sort()
    length = len(weights)
    split_vals.append((weights[int(length/4)]))
    split_vals.append((weights[int(length/2)]))
    split_vals.append((weights[int(length/2 + (length/4))]))
    return split_vals


# returns a list of the quartile of restaurant_options map as their own maps 
def splitQuartiles(restaurant_options, split_vals):
    firstQuartile = {}
    secondQuartile = {}
    thirdQuartile = {}
    fourthQuartile = {}
    for key, value in restaurant_options.items():
        if value < split_vals[0]:
            firstQuartile[key] = value
        if value >= split_vals[0] and value < split_vals[1]:
            secondQuartile[key] = value
        if value >= split_vals[1] and value < split_vals[2]:
            thirdQuartile[key] = value
        if value >= split_vals[2]:
            fourthQuartile[key] = value     
    listedQuartiles = []
    if (len(firstQuartile) != 0):
        listedQuartiles.append(firstQuartile)
    
    if (len(secondQuartile) != 0):
        listedQuartiles.append(secondQuartile)
    
    if (len(thirdQuartile) != 0):
        listedQuartiles.append(thirdQuartile)
    
    if (len(fourthQuartile) != 0):
        listedQuartiles.append(fourthQuartile)
    
    return listedQuartiles 


# reassigns value of each restaurant in a quartile to a standardized start val based on quartile data
# returns the revalued list of quartiles 
def revalue(listedQuartiles): 
    i = len(listedQuartiles) - 1
    subVals = []
    while i > 0:
        subVals.append(getSubtractionVal(listedQuartiles[i-1], listedQuartiles[i]))
        i = i - 1
    
    i = len(listedQuartiles) - 1
    replaceVal = 10
    subVals.append(0)
    while i >= 0:
        replaceVal = replaceVal - subVals[i]
        for key, value in listedQuartiles[i].items():
            listedQuartiles[i][key] = replaceVal
        i = i - 1
    return listedQuartiles 

# recombines the list of quartiles into the final standardizes restaurant_options map 
def recombine(listedQuartiles):
    restaurant_options = {}
    i = 0
    while i < len(listedQuartiles):
        for key, value in listedQuartiles[i].items():
            restaurant_options[key] = value
        i = i + 1
    return restaurant_options


#given two adjacent quartiles, returns a decimal value to decrement the starting val of the restaurants in the lower quartile by 
def getSubtractionVal(lowerQ, higherQ): 
    lQmean = 0;
    if (len(lowerQ)!=0):
        for key, value in lowerQ.items():
            lQmean += value
        lQmean = lQmean / len(lowerQ)
    hQmean = 0;
    if (len(higherQ) != 0):
        for key, value in higherQ.items():
            hQmean += value
        hQmean = hQmean / len(higherQ)

    ## 
    if (hQmean != 0):
        subVal = 1 - (lQmean/hQmean)
        return subVal
    else:
        return -1  
        #this is meant to be taken as an error code cause the higher quartile should never be 0 (i think). 









##Unit Testing 
r0 = Restaurant("r0", "address", "price", 0.5, "latitude", "longitude", "isclosed", "distance", "delivers")
r1 = Restaurant("r1", "address", "price", 0.5, "latitude", "longitude", "isclosed", "distance", "delivers")
r2 = Restaurant("r2", "address", "price", 0.5, "latitude", "longitude", "isclosed", "distance", "delivers")
r3 = Restaurant("r3", "address", "price", 0.5, "latitude", "longitude", "isclosed", "distance", "delivers")
r4 = Restaurant("r4", "address", "price", 0.5, "latitude", "longitude", "isclosed", "distance", "delivers")
r5 = Restaurant("r5", "address", "price", 0.5, "latitude", "longitude", "isclosed", "distance", "delivers")
r6 = Restaurant("r6", "address", "price", 0.5, "latitude", "longitude", "isclosed", "distance", "delivers")
r7 = Restaurant("r7", "address", "price", 0.5, "latitude", "longitude", "isclosed", "distance", "delivers")
testRestaurants = {}
testRestaurants[r0] = 1
testRestaurants[r1] = 1
testRestaurants[r2] = 1
testRestaurants[r3] = 1
testRestaurants[r4] = 3
testRestaurants[r5] = 3
testRestaurants[r6] = 3
testRestaurants[r7] = 3



# can later loop through restaurant_options to get a list of just the values like this 
data = prepForStats(testRestaurants)

## aside from initially putting the vals of restaurant_options into a list of just the values ("data"), this is the order 
##      we will use these methods in. we can also change defineQuartiles to work w the OG full map instead of a list 
split_vals = defineQuartiles(data)
quartilesList = splitQuartiles(testRestaurants, split_vals)
quartilesList = revalue(quartilesList)
standardized_vals_restaurant_list = recombine(quartilesList)
print(standardized_vals_restaurant_list)