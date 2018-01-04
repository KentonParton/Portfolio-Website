
#           Wall len,   complete , corners, T-juctions, doors, 600mm W, 900mm W, 1200mm W, 1500mm W, 1800mm W
#inputArray = ["5000", "complete" , "2",    "3",       "0",   "0",      "0",     "0",      "0",       "0"]


#inputArray = ["2000","complete", "0","3","0","0","0","0","0","0"]


def runFunctions(inputArray):

    doorList = []
    windowList = []
    junctionList = []
    shutterList = []
    dimensions = []
    errorMsg = []

    countShutterList = []


    # List of all the elements
    containerList = [doorList, windowList, junctionList, shutterList, errorMsg, dimensions]

    # Calculates distance in millimeters of all doors
    doors(inputArray, containerList, doorList)

    # Calculates distance in millimeters of all windows
    windows(inputArray, containerList, windowList)

    #print 'junctionList = ' + str(junctionList)

    # Calculates length of total number of junctions for startSum
    junctions(inputArray, junctionList, containerList)

    #print containerList

    # Calculates the starting value for wallCombinations, dimensions
    startingSum(inputArray, containerList, dimensions)

    checkValue(inputArray,containerList, errorMsg)


    if containerList[-2] == []:
        # Calculates most efficient use of shutters to make up the wall length
        wallCombinations(inputArray, containerList, shutterList, dimensions, errorMsg)
    else:
        pass

    # print 'containerList = ' + str(containerList)
    return containerList



def doors(inputArray, containerList, doorList):

    """ Helper Function
    Calculates the length of all the doors

    Params:
        inputArray,containerList, doorList

    Return:
        containerList [List]
    """

    # Number of doors entered
    numDoors = int(inputArray[4])

    # Extend doorList by 600 for every door entered
    for i in range(numDoors):
        doorList.extend([900])

    # print "doorList = ", doorList
    return containerList


def windows(inputArray, containerList, windowList):

    """ Helper Function
    Calculates the length of all the windows

    Params:
        inputArray,containerList, windowList

    Return:
        containerList [List]
    """
    windowLengths = [600, 900, 1200, 1500, 1800]

    n = 5 # starting at 5 because that is the index of the first window index in inputArray

    for j in windowLengths:
        # Number of windows entered
        numWindows = int(inputArray[n])
        # print "numWindows"+ str(numWindows)

        # Extend windowList by 600 for every window entered
        for i in range(numWindows):
            windowList.extend([j])
            #print "windowList" + str(windowList)

        n+=1

    # print "Window list" + str(windowList)
    # print "windowList = ", windowList
    return containerList


def junctions(inputArray, junctionList, containerList):

    """ Helper Function
    Calculates the total length of all junction shutters (Corner and T-Junctions) in each wall.

    Params:
        inputArray,junctionList, containerList

    Return:
        containerList [List]
    """
    # print 'junctionList = ' + str(junctionList)

    cornerValue = int(inputArray[2])
    tValue = int(inputArray[3])

    junctionSum = (cornerValue * 250) + (tValue * 350)


    junctionList.extend([junctionSum])

    # print 'junctionList = ' + str(junctionList)

    return containerList


def startingSum(inputArray, containerList, dimensions):

    """ Helper Function
    Calculates the new value once the base cases(regular wall or t-wall) and doors and windows have been deducted

    Params:
        inputArray,containerList, dimensions

    Return:
        containerList [List]
    """
    numCorners = int(inputArray[2])
    #print 'containerList = ' + str(containerList)
    i = 0
    startSum = 0

    for i in range (len(containerList)):
        j = 0
        for j in range (len(containerList[i])):
            # Adds all the value of: doorList, windowList and junctionList
            startSum = startSum + int(containerList[i][j])

            j = j + 1
        i = i + 1

    if inputArray[1] == 'complete':
        #Base cases
        if numCorners == '0':
            startSum = startSum+200
        elif numCorners == '1':
            startSum = startSum+100
        # if numConers = 2 nothing must be deducted
    else:
        startSum = startSum+100

    # Reduce the wallLength given by user and reduce it by the startSum, this length will be used in wallCombinations
    startSum = [int(inputArray[0]) - startSum]

    # Adds the new value to dimensions list where we can use it for function wallCombinations
    dimensions.extend((startSum))

    # print "startSum = ", startSum
    return containerList


def checkValue(inputArray,containerList, errorMsg):

    inputLength = [int(inputArray[0])]

    n = 0 # incrimentor
    m = 0 # incrimentor

    # if there is a remainder result in an errorMsg
    if inputLength[m] % 50 > 0:

        errorMsg.extend(["multiple"])
        # print( "multiple" )

        return containerList

    # if the inputLength is smaller in value than the total of door, window and walltype lenth, result in an errorMsg.
    elif int(containerList[-1][0]) < 0:

        errorMsg.extend(["invalidInput"])
        # print("invalidInput")
        return containerList

    return containerList

def wallCombinations(inputArray, containerList, shutterList, dimensions, errorMsg):

    """
    Calculates best combination of shutters to build the wall.

    Params:
            [List] dimensions
            (int) sum

    Return: [List] Combinations
    """

    # Different length shutters
    combinations = [600,400,350,300,250]

    # cloning the original wall input length
    dimensions_Clone = dimensions[:]

    # will contain the combination of different shutter combinations

    n = 0
    m = 0
    startValue = 0 # Start with an amount of 0, we will increase this value till it equals our dimensions vlaue

    try:
        # loops through wall lengths submitted by user
        for i in range (len(dimensions)): # loops through param dimensions

            while startValue != dimensions[m]: # we will stop when startValue is equal to our dimensions value

                # If a combination has been added and there is a remained or 250....
                if dimensions[m] - startValue < 250:

                    # Remove that combination value from the list and move to the next indexed combination
                    startValue = startValue - combinations[n]
                    # Remove the combination that was added
                    shutterList.pop()
                    n = n + 1

                else:
                    # If a new combination has been added and there is a remained or more than 250, add the combination to startValue...
                    startValue = startValue + combinations[n]
                    # ...and append the value to shutterList
                    shutterList.append(combinations[n])

                if n == 5: # if it doesn't find a combination, remove last value from list

                    shutterList.pop() # remove last value from list
                    n = 1
                    startValue = startValue - combinations[n-1] # sum - 600

            #print (shutterList)

            n = 0
            m = m + 1

        # print(shutterList)
        return containerList

    except IndexError:
        # if the wallLength is accepted by the checkValue but cannot be computed an"IndexValue" value will be returned
        errorMsg.extend(["indexError"])

        return containerList

# will want to use this to display the number of each shutter needed to construct the wall
def countShutters (inputArray, containerList):

    """Helper Function
    Counts number of each shutter element

    Params:
            inputArray, containerList
    """
    windowXl = 0
    windowL = 0
    windowM = 0
    windowS = 0
    windowXs = 0
    shutterXl = 0
    shutterL = 0
    shutterM = 0
    shutterS = 0
    shutterXs = 0
    shutterC = int(inputArray[2])
    shutterT = int(inputArray[3])

    shutterD = int(inputArray[4])

    # Counts the number of each window shutter type
    for i in containerList[1]:
        if i == 600:
            windowXs +=1

        elif i == 900:
            windowS +=1

        elif i == 1200:
            windowM +=1

        elif i == 1500:
            windowL +=1

        elif i == 1800:
            windowXl +=1

    # Counts the number of each particular shutter in containerList.
    for j in containerList[3]:

        if j == 600:
            shutterXl += 1


        elif j == 400:
            shutterL +=1


        elif j == 350:
            shutterM +=1


        elif j == 300:
            shutterS +=1


        elif j == 250:
            shutterXs +=1

    # Using a list inside a list so that countShutterList is indexable when it is returned in general.js, without using a list inside a list it cannot be indexed correctly
    countShutterList = [
        ['shutterXl', shutterXl],
        ['shutterL', shutterL],
        ['shutterM', shutterM],
        ['shutterS', shutterS],
        ['shutterXs', shutterXs],
        ['shutterC', shutterC],
        ['shutterT', shutterT],
        ['shutterD', shutterD],
        ['windowXl', windowXl],
        ['windowL', windowL],
        ['windowM', windowM],
        ['windowS', windowS],
        ['windowXs', windowXs]
    ]
    # print(countShutterList)
    return countShutterList



# to run this code on its own un-comment the lines below


# to run this code on its own un-comment the lines below
#containerList = [[600, 600], [600], [250, 250], [], [600,600,400,350,250], [], [300]]
#countShutterList = [20, 1, 1, 0, 3, 0, 1, 2]
#countLen(countShutterList)
#runFunctions(inputArray)
#countShutters(inputArray, containerList)
