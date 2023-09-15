
# Assignment 4: Naive Bayesian Classification

# INSTRUCTIONS: Type "python radar.py" in your terminal to run the 
# program and make sure you have the pdf.txt and data.txt files.

import math
import pprint

FILEPDF = 'pdf.txt'
FILEDATA = 'data.txt'
NUM_OBJECTS = 10

class NaiveBayes:
    # conditional probabilities for each speed
    birds = {}; aircrafts = {}

    # all lines in the data file (each line represents an object)
    everyObject = []

    # probability of being a bird and aircraft of each object (list of tuples)
    classOfObjects = []

    # Variance PDF in the Form of dictionaries below (key: variance, value: number of that variance value )

    # all of the variance values for all bird objects
    var_birds = {}

    # all of the variance values for all bird objects
    var_aircrafts = {}


    # read pdf file to extract the conditional probability data from the pdf
    def read_pdf(self):
        f = open(FILEPDF, 'r')

        # read the data for birds
        line = f.readline()
        birds_value = line.split(',')
        for i in range(len(birds_value)): # stores the probability of the object being a bird given the speed (note that speed interval is 0-200 but the array is 400 slots)
            self.birds[i] = float(birds_value[i])

        # read the data for aircrafts
        line = f.readline()
        aircrafts_value = line.split(',')
        for i in range(len(aircrafts_value)):   # stores the probability of the object being an aircraft given the speed (note that speed interval is 0-200 but the array is 400 slots)
            self.aircrafts[i] = float(aircrafts_value[i])

        f.close()

    # read data file to get the object that will be fed to the naive bayesian classifier
    def read_data(self):
        f = open(FILEDATA, 'r')
        line = f.readline()

        for i in (range(NUM_OBJECTS)): # go over each line in the data file
            data_line = line.split(',')
            new_data_line = []
            for j in range(len(data_line)):     # convert every speed data in each line to integer except 'NaN's
                if (data_line[j] != 'NaN' and data_line[j] != 'NaN\n' ):
                    new_data_line.append(float(data_line[j]))

            self.everyObject.append(new_data_line)  # append the data lines (represent objects) the list for all objects
            line = f.readline()

        f.close()


    # sliding window feeder

    def varianceOfRow(self, row):
        varianceList = []
        # fills in the varinace list with a window length of 3
        for i in range(len(row) - 2):
            # slice the array into smaller array of three elemwents
            sliced = row[i : i+3]
            # feed the speed values to variance calculator
            variance = self.calculate_variance(sliced)
            # add to the variance list
            varianceList.append(variance)
        return varianceList

    def calculate_mean(self, elts):
        mean = 0; sum = 0
        for i in range(len(elts)):
            sum  += elts[i]

        mean = sum / len(elts)
        return mean

    def calculate_variance(self, elts):

        # extract the mean of the set
        mean = self.calculate_mean(elts)

        # return the variance of the set
        variance = 0
        for i in range(len(elts)):
            variance += (elts[i] - mean) * (elts[i] - mean)

        return math.sqrt(float(variance / len(elts)))


    def variancePdf_maker(self):
        # variance pdf for birds

        variance_birds = [] # all variances of birds in a list
        birds_num = [0, 2, 3, 4, 9] # position of all the bird objects in everyObject list
        # add the variance of each row to variance birds
        for num in birds_num:
            variance_birds += self.varianceOfRow(self.everyObject[num])

        # record the variance in var_birds
        for var in variance_birds:
            if var in self.var_birds.keys():
                self.var_birds[var] += 1
            else:
                self.var_birds[var] = 1


        # variance pdf for aircrafts

        variance_aircrafts = [] # all variances of aircrafts in a list
        aircrafts_num = [1, 5, 6, 7, 8] # position of all the aircraft objects in everyObject list
        # add the variance of each row to a variance aircrafts
        for num in aircrafts_num:
            variance_aircrafts += self.varianceOfRow(self.everyObject[num])

        # record the variance in var_aircrafts
        for var in variance_aircrafts:
            if var in self.var_aircrafts.keys():
                self.var_aircrafts[var] += 1
            else:
                self.var_aircrafts[var] = 1



    def normalizePdf(self):

        # normalize bird_pdf
        sum1 = 0 # find the number of variances
        for var in self.var_birds.keys():
            sum1 += self.var_birds[var]

        # divide each frequency of variance by the sum
        for var in self.var_birds.keys():
            self.var_birds[var] = float(self.var_birds[var] / sum1)

        # normalize aircraft_pdf
        sum2 = 0 # find the number of variances
        for var in self.var_aircrafts.keys():
            sum2 += self.var_aircrafts[var]

        # divide each frequency of variance by the sum
        for var in self.var_aircrafts.keys():
            self.var_aircrafts[var] = float(self.var_aircrafts[var] / sum2)


    # Calculate the probabilities of predicting each class for a given object
    def calculate_class_probabilities(self):
        self.variancePdf_maker()
        self.normalizePdf()

        for object in self.everyObject: # x represents an object (contains a list of speed values for that object)
            SprobBirds = 0
            SprobAircrafts = 0
            # predict the gaussian probability for BIRDS class
            for speed in object:
                SprobBirds += 0.9 * self.birds.get((round(speed * 2) / 2) * 2) + 0.1 * self.aircrafts.get((round(speed * 2) / 2) * 2)

                # predict the gaussian probability for AIRCRAFTS class
            for speed in object: # 
                SprobAircrafts += 0.1 * self.birds.get((round(speed * 2) / 2) * 2) + 0.9 * self.aircrafts.get((round(speed * 2) / 2) * 2)

            VprobBirds = 0
            VprobAircrafts = 0
            # predict the gaussian probability for BIRDS class
            for var in self.varianceOfRow(object):
                # in case that variance is not available: assign 0
                if   var not in self.var_aircrafts.keys():
                    self.var_aircrafts[var] = 0

                if  var not in self.var_birds.keys():
                    self.var_birds[var] = 0
                VprobBirds += (0.9 * self.var_birds.get(var) + 0.1 * self.var_aircrafts.get(var))

            # predict the gaussian probability for AIRCRAFTS class
            for var in self.varianceOfRow(object):
                # in case that variance is not available: assign 0
                if var not in self.var_birds.keys():
                    self.var_birds[var] = 0

                if var not in self.var_aircrafts.keys():
                    self.var_aircrafts[var] = 0

                VprobAircrafts += (0.1 * self.var_birds.get(var) + 0.9 * self.var_aircrafts.get(var))

            self.classOfObjects.append((0.5 * (SprobBirds * VprobBirds) , (SprobAircrafts * VprobAircrafts) * 0.5))

    # determine the class of the objects based on probability comparison
    def determine_class(self):
        self.calculate_class_probabilities()
        i = 1
        for x in self.classOfObjects:
            if x[0] >  x[1]: # x[0] is probability of being a bird and x[1] is probability of being an aircraft
                print("Object", i,  "is a bird!")
            else:

                print("Object", i, "is an aircraft!")
            i = i + 1


nb = NaiveBayes()
nb.read_data()
nb.read_pdf()
nb.determine_class()

