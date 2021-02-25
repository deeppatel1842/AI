import numpy as np
import random
import operator
import pandas as pd

# To create the locations. Here the x and y are the latitude and longitude respectively, obtained using Google Maps.
class Location:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
    
    def distance(self, location):
        xDis = abs(self.x - location.x)
        yDis = abs(self.y - location.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance
    
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

# Fitness is inverse of route distanse. We have to minimize route distance, therefore we will maximizing fitness. This function we tell how good each route is.
class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromL = self.route[i]
                toL = None
                if i + 1 < len(self.route):
                    toL = self.route[i + 1]
                else:
                    toL = self.route[0]
                pathDistance += fromL.distance(toL)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness

# Produces routes randomly.
def createRoute(locationList):
    route = random.sample(locationList, len(locationList))
    return route

# Produces a population
def initialPopulation(popSize, locationList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(locationList))
    return population

# This function returns a list with route ids and their respective fitness scores
def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

# This function returns a list of route ids, which we use to create the mating pool
def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

# To create the mating pool, we are simply extracting the selected individuals from our population
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

# Creating the next generation (Crossover)
def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

# Creates offspring population
def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

# We use swap mutation i.e. with specified low probability, two cities will swap places in our route
def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

# Creating a mutated population
def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop


# Creates a new generation by combining all the above function. We first rank the routes using rankRoutes, then determine our potential parents which allows us to create mating pool. Then to create new generstion we  use breed population and apply then mutate it.
def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

# The final Genetic ALgorithm function
def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial Route")
    for i in range(len(pop[0])):
        print((pop[0])[i].name,end = " -> ")
    print((pop[0])[0].name)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
    
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute



if __name__ == "__main__":
    placesList = []

    Udaipur = Location(27.42, 75.33, "Udaipur")
    placesList.append(Udaipur)
    
    Jaipur = Location(26.55, 75.52, "Jaipur")
    placesList.append(Jaipur)
    
    Jaislmer = Location(26.55, 70.57, "Jaislmer")
    placesList.append(Jaislmer)
    
    SawaiMadhopur = Location(25.58,76.3, "SawaiMadhopur")
    placesList.append(SawaiMadhopur)
    
    Pokaran = Location(26.55,71.58, "Pokaran")
    placesList.append(Pokaran)
    
    Ajmer = Location(26.27, 74.42, "Ajmer")
    placesList.append(Ajmer)
    
    Chittorgarh = Location(24.54, 74.42, "Chittorgarh")
    placesList.append(Chittorgarh)
    
    Jodhpur = Location(26.18,73.04, "Jodhpur")
    placesList.append(Jodhpur)
    
    Bikaner = Location(28.01,73.22, "Bikaner")
    placesList.append(Bikaner )
    
    Ratangarh = Location(28.05, 74.39, "Ratangarh")
    placesList.append(Ratangarh)
    
    Mountabu = Location(24.40,72.45, "Mountabu")
    placesList.append(Mountabu)
    
    Bhartpur = Location(27.15, 77.30, "Bhartpur")
    placesList.append(Bhartpur)
    
    Alwar = Location(27.34,76.38, "Alwar")
    placesList.append(Alwar)
    
    Kishangarh = Location(27.53,70.37, "Kishangarh")
    placesList.append(Kishangarh)
    
    Nimbahera = Location(24.37, 74.45, "Nimbahera")
    placesList.append(Nimbahera)
    
    Bundi = Location(25.27, 75.41, "Bundi")
    placesList.append(Bundi)
    
    Rajgarh = Location(28.39, 75.26, "Rajgarh")
    placesList.append(Rajgarh)
    
    Nathdwara = Location(25.56, 73.52, "Nathdwara")
    placesList.append(Nathdwara)
    
    Nagaur = Location(27.00, 73.40, "Nagaur")
    placesList.append(Nagaur)
      
    
    
    # Here we loop through 500 generations
    bestRoute = geneticAlgorithm(population=placesList, popSize=100, eliteSize=20, mutationRate=0.01, generations=100)
    
    for i in range(len(bestRoute)):
        print((bestRoute[i]).name , end=" -> ")

    print((bestRoute[0]).name)
