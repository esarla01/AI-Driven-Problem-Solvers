
# Assignment 4: Naive Bayesian Classification

# INSTRUCTIONS: Type "python radar2.py" in your terminal to run the
# program and make sure you have the pdf.txt and data.txt files.

import math

FILEPDF = 'pdf.txt'
FILEDATA = 'data.txt'
NUM_OBJECTS = 10

class NaiveBayes:
    # conditional probabilities for each speed
    birds = {}; aircrafts = {}

    # all lines in the data file (each line represents an object)
    everyObject = []

    # mean of classes
    mean_bird = 0;
    mean_aircraft = 0;

    # stdev of classes
    stdev_bird = 0;
    stdev_aircraft = 0;

    # probability of being a bird and aircraft of each object (list of tuples)
    classOfObjects = []


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

        # Calculate the probabilities of predicting each class for a given object
    def calculate_class_probabilities(self):

        for object in self.everyObject: # x represents an object (contains a list of speed values for that object)
            SprobBirds = 0
            SprobAircrafts = 0
            # predict the gaussian probability for BIRDS class
            for speed in object:
                SprobBirds += 0.9 * self.birds.get((round(speed * 2) / 2) * 2) + 0.1 * self.aircrafts.get((round(speed * 2) / 2) * 2)

                # predict the gaussian probability for AIRCRAFTS class
            for speed in object: #
                SprobAircrafts += 0.1 * self.birds.get((round(speed * 2) / 2) * 2) + 0.9 * self.aircrafts.get((round(speed * 2) / 2) * 2)

            self.classOfObjects.append((0.5 * SprobBirds , SprobAircrafts * 0.5))


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



