import random

### Generate initial generation
def initPop(popSize, generationSize):
  newGen = []
  j = 0

  while j < generationSize:
    newPop = [0] * popSize
    i = 0
    while i < popSize / 20:
      num = random.randrange(popSize)
      if newPop[num] == 0:
        newPop[num] = 1
        i += 1
    newGen.append(newPop)
    j += 1

  return newGen

  
### Generate fitness (Function Eval)
def fitnessScore(generation, utility, weight):
  scores = []

  for i in range(len(generation)):
    totalWeight = 0
    totalValue = 0

    for j in range(len(generation[i])):
      if generation[i][j] == 1:
        totalWeight += weight[j]
        totalValue += utility[j]

    if totalWeight > 500:
      score = 1
    else:
      score = totalValue

    scores.append(score)

  return scores


### Normalize
def normalize(fitness):
  fitnessCopy = []
  rate = []
  total = 0

  for i in range(len(fitness)):
    fitnessCopy.append(fitness[i] * fitness[i])

  total = sum(fitnessCopy)

  for i in fitnessCopy:
    rate.append(i / total) 
  
  return rate


### getCDF
def getCDF(weights):
  for i in range(1, len(weights)):
    weights[i] += weights[i-1]

  return weights


## Mutation
def mutate(child, popSize):
  randomBit = 0
  if (random.randint(1,10000) == 1): # 1/10,000 chance for mutation
      randomBit = random.randint(0,popSize-1)
      child[randomBit] = 1 if child[randomBit] == 0 else 0

  return child

### Generation building
def nextGen(cdf, generation, popSize, genSize):
  newGeneration = []
  size = int(genSize / 2)

  for j in range(size):
    child1 = []
    child2 = []

    # Find parents
    parent1 = random.uniform(0,1)
    parent2 = random.uniform(0,1)

    for i in range(len(cdf)):
      if cdf[i] > parent1:
        parent1 = i
      
      if cdf[i] > parent2:
        parent2 = i

    # Splicing
    splice = random.randrange(1, popSize - 1)
    child1 = generation[parent1][:splice] + generation[parent2][splice:]
    child2 = generation[parent2][:splice] + generation[parent1][splice:]

    # Mutation
    child1 = mutate(child1, popSize)
    child2 = mutate(child2, popSize)

    newGeneration.append(child1)
    newGeneration.append(child2)

  return newGeneration

#############################################

fitness = []
generation = []
popSize = 400
genSize = 1000
flag = True
utility = []
weight = []
cdf = []


### Pull from text file
with open("Program2Input.txt", "r") as file:
  for line in file:
    for value in line.split():
      if flag:
        utility.append(float(value))
        flag = False
      else:
        weight.append(float(value))
        flag = True


### Initial population
generation = initPop(popSize, genSize)
fitness = fitnessScore(generation, utility, weight)
cdf = getCDF(normalize(fitness))

f = open("output.txt", "w")

change = 0
avgFitness = 0
genNum = 0
counter = 0
targetGen = 0
totalWeight = 0
totalUtility = 0

while 1:
  generation = nextGen(cdf, generation, popSize, genSize)
  fitness = fitnessScore(generation, utility, weight)
  cdf = getCDF(normalize(fitness))

  prevFitness = avgFitness
  avgFitness = (sum(fitness)/len(fitness))
  change = ((avgFitness - prevFitness) / avgFitness) * 100

  if (change < 1):
    counter += 1
  else:
    counter = 0

# Find max fitness
# Get max fitness index
# Use index to find generation
  print("Gen: {}   {}".format(genNum, avgFitness))
  if counter == 10:
    maxFit = max(fitness)
    f.write("Max Fitness: {}\n".format(maxFit))
    for i in range(len(fitness)):
      if fitness[i] == maxFit:
        targetGen = i
  # Use generation to get item indexes
    for i in range(len(generation[0])):
      if generation[targetGen][i] == 1:
  # Use item indexes to file-out item values
        f.write("Weight: {}   Utility: {}\n".format(weight[i], utility[i]))
        totalWeight += weight[i]
        totalUtility += utility[i]
    f.write("\nTotal Weight: {}\nTotal Utility: {}\n".format(totalWeight, totalUtility))
    break
  genNum += 1
f.close()