from main import Restaurant
import statistics 

# returns array split_vals of length 3, where split[i] is the next value to split restaurant_options at 
def defineQuartiles(weights):
    split_vals = []
    weights.sort()
    length = len(weights)
    split_vals.append((weights[int(length/4)]))
    split_vals.append((weights[int(length/2)]))
    split_vals.append((weights[int(length/2 + (length/4))]))
    return split_vals


# returns the first, second, third, and fourth quartile of restaurant_options map as their own maps 
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
    return firstQuartile, secondQuartile, thirdQuartile, fourthQuartile 


# reassigns value of each restaurant in a quartile to a standardized start val based on quartile data 
def revalue(firstQuartile, secondQuartile, thirdQuartile, fourthQuartile): 
    subVal1 = getSubtractionVal(thirdQuartile, fourthQuartile)
    subVal2 = getSubtractionVal(secondQuartile, thirdQuartile)
    subVal3 = getSubtractionVal(firstQuartile, secondQuartile)
    for key, value in fourthQuartile.items():
        fourthQuartile[key] = 10
    subtractFrom = 10;
    subVal = subVal1
    for key, value in thirdQuartile.items():
        thirdQuartile[key] = subtractFrom - subVal
    subtractFrom = subtractFrom - subVal
    subVal = subVal2
    for key, value in secondQuartile.items():
        secondQuartile[key] = subtractFrom - subVal
    subtractFrom = subtractFrom - subVal
    subVal = subVal3
    for key, value in firstQuartile.items():
        firstQuartile[key] = subtractFrom - subVal

    return firstQuartile, secondQuartile, thirdQuartile, fourthQuartile

def recombine(firstQuartile, secondQuartile, thirdQuartile, fourthQuartile):
    restaurant_options = {}
    for key, value in firstQuartile.items():
        restaurant_options[key] = value
    for key, value in secondQuartile.items():
        restaurant_options[key] = value
    for key, value in thirdQuartile.items():
        restaurant_options[key] = value
    for key, value in fourthQuartile.items():
        restaurant_options[key] = value
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
testRestaurants[r1] = 2
testRestaurants[r2] = 2
testRestaurants[r3] = 4
testRestaurants[r4] = 6
testRestaurants[r5] = 6
testRestaurants[r6] = 9
testRestaurants[r7] = 10



# can later loop through restaurant_options to get a list of just the values like this 
data = [1, 2, 2, 4, 6, 6, 9, 10]

## aside from initially putting the vals of restaurant_options into a list of just the values ("data"), this is the order 
##      we will use these methods in. we can also change defineQuartiles to work w the OG full map instead of a list 
split_vals = defineQuartiles(data)
first, second, third, fourth = splitQuartiles(testRestaurants, split_vals)
first, second, third, fourth = revalue(first, second, third, fourth)
standardized_vals_restaurant_list = recombine(first, second, third, fourth)
print(standardized_vals_restaurant_list)