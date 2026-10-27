import random

SELECTION_METHODS = ["tournament", "rank"]
POPULATIONS= [5]


def startGame():

    matrixWidth = int(input("Enter garden width: "))
    matrixHeight = int(input("Enter garden height: "))
    numberOfStones = int (input("Enter number of stones: "))
    selectionNumber = int(input("Enter selection number 0 - tournament, 1 - rank: "))

    if selectionNumber != 0 and selectionNumber != 1:
        while True:
            print("Invalid selection number. try again")
            selectionNumber = int(input("Enter selection number 0 - tournament, 1 - rank: "))
            if selectionNumber == 0 or selectionNumber == 1:
                break


    stonesCoords = []

    for i in range(numberOfStones):
        while True:
            enteredCoord = input(f"Enter coordinates of stone {i + 1} (x y): ")
            partsOfCoord = enteredCoord.split()


            try:
                x = int(partsOfCoord[0])
                y = int(partsOfCoord[1])
            except ValueError:
                print("Integers must be entered")
                continue

            incorrectCoord = (not 0 <= x < matrixWidth or not 0 <= y < matrixHeight or len(partsOfCoord) != 2)

            if incorrectCoord:
                print("Invalid coordinate")
                continue

            stonesCoords.append((x, y))
            break


    gardenMatrix = [[0 for _ in range(matrixWidth)] for _ in range(matrixHeight)]

    for s in stonesCoords:
        x, y = s
        gardenMatrix[y][x] = -1

    maxFitness = matrixWidth * matrixHeight - numberOfStones

    matrixPerimeter = (matrixWidth + matrixHeight) * 2
    maxNumberOfGenes = matrixPerimeter // 2 + numberOfStones
    numberOfGenes =  1 if matrixWidth == 1 and matrixHeight == 1 else random.randint(4, maxNumberOfGenes)
    selection = SELECTION_METHODS[selectionNumber]


    for populationSize in POPULATIONS:
       population = generateChromosomes(numberOfGenes, populationSize, matrixPerimeter)
       fitnessValues, gardens = performRake(gardenMatrix, population, matrixWidth, matrixHeight, matrixPerimeter)

       bestResult = geneticAlgorithm(population, fitnessValues, maxFitness, selection, matrixPerimeter, gardenMatrix, matrixWidth, matrixHeight)


    print(bestResult, maxFitness)
    return




def geneticAlgorithm(population, fitness, maxFitness, selection, perimeter, gardenMatrix, width ,height):
    bestFitness = max(fitness)
    generation = 0

    if bestFitness == maxFitness:
        return population[fitness.index(bestFitness)]

    while bestFitness != maxFitness:
        if generation == 20:
            return bestFitness
        if selection == "tournament":
            selectedPopulation = selectTournament(fitness, population, 2)
        else:
            selectedPopulation = selectRank(fitness, population)

        crossedPopulation = crossover(selectedPopulation)
        mutation(crossedPopulation, perimeter)
        fitness = performRake(gardenMatrix, crossedPopulation, width , height, perimeter)

        if bestFitness < max(fitness):
            bestFitness = max(fitness)

        population = crossedPopulation
        generation += 1



    return bestFitness





def mutation(population, perimeter):
    mutationProb = 0.1
    for chromosome in population:
        for i in range(len(chromosome)):
            if random.random() < mutationProb:
                chromosome[i] = random.randint(0, perimeter - 1)




def crossover(population):
    newPopulation = []
    crossProb = 0.7

    for i in range(0, len(population), 2):
        if i == len(population) - 1:
            newPopulation.append(population[i])

        elif random.random() < crossProb:
            cut1, cut2 = sorted(random.sample(range(1, len(population[i])), 2))

            child1 = population[i][:cut1] + population[i + 1][cut1:cut2] + population[i][cut2:]
            child2 = population[i + 1][:cut1] + population[i][cut1:cut2] + population[i + 1][cut2:]
            newPopulation.extend([child1, child2])
        else:
            newPopulation.extend([population[i], population[i + 1]])

    for population in newPopulation:
        print(population, end="\n\n")
    print("executed and left--crossover")

    return newPopulation




def selectTournament(fitness, population, k=2):
    newPopulation = []
    for _ in range(len(population)):
        index = random.sample(range(len(population)), k=k)
        best = max(index, key=lambda i: fitness[i])
        newPopulation.append(population[best][:])
    return newPopulation

def selectRank(fitness, population):
    newPopulation = []
    ordered = sorted(range(len(population)), key=lambda i: fitness[i])
    ranks = [i + 1 for i in range(len(ordered))]
    for _ in range(len(population)):
        chosen = random.choices(ordered, weights=ranks, k=1)[0]
        newPopulation.append(population[chosen][:])
    return newPopulation


def generateChromosomes(genesNumber, populationSize, perimeter):
    generatedChromosomes = [
    [0] * genesNumber
    for _ in range(populationSize)
    ]

    for i in range(0, populationSize):
        for j in range(0,genesNumber):
            generatedChromosomes[i][j] = random.randint(0, perimeter - 1)

    return generatedChromosomes


def rakeLine(g, x, y, dx, dy, width, height, mark, chromosome, t):
    while True:
        g[y][x] = mark
        nextX, nextY = x + dx, y + dy

        if not (0 <= nextX < width and 0 <= nextY < height):
            return False, t

        if g[nextY][nextX] == 0:
            x, y = nextX, nextY
            continue


        options = []
        for tdx, tdy in ((-dy, dx), (dy, -dx)):
            tx, ty = x + tdx, y + tdy
            if not (0 <= tx < width and 0 <= ty < height) or g[ty][tx] == 0:
                options.append((tdx, tdy))

        if not options:
            return True, t

        if len(options) == 2:
            dx, dy = options[chromosome[t % len(chromosome)] % 2]
            t += 1
        else:
            dx, dy = options[0]

        tx, ty = x + dx, y + dy
        if not (0 <= tx < width and 0 <= ty < height):
            return False, t
        x, y = tx, ty



def performRake(garden, population, width, height, perimeter):

    results = []
    resultGardens = []

    for chromosome in population:
        passNumber = 0
        gardenCopy = [row.copy() for row in garden]
        t = 0
        stuck = False
        for gene in chromosome:

            if 0 <= gene < height:
                x, y = (0, gene)

                if gardenCopy[y][x] != 0:
                    continue

                passNumber += 1

                stuck, t = rakeLine(gardenCopy, x, y, 1, 0, width, height,
                                    passNumber, chromosome, t)

            elif height <= gene < perimeter // 2:
                x, y = (gene - height, height - 1)


                if gardenCopy[y][x] != 0:
                    continue

                passNumber += 1

                stuck, t = rakeLine(gardenCopy, x, y, 1, 0, width, height,
                                    passNumber, chromosome, t)

            elif perimeter // 2 <= gene <  (perimeter // 2) + height:
                x, y = (width - 1,abs((gene - perimeter // 2) - height) - 1)


                if gardenCopy[y][x] != 0:
                    continue

                passNumber += 1

                stuck, t = rakeLine(gardenCopy, x, y, 1, 0, width, height,
                                    passNumber, chromosome, t)

            elif (perimeter // 2) + height <= gene < perimeter:
                x, y = ( abs(perimeter - gene) - 1, 0)


                if gardenCopy[y][x] != 0:
                    continue

                passNumber += 1

                stuck, t = rakeLine(gardenCopy, x, y, 1, 0, width, height,
                                    passNumber, chromosome, t)

        results.append(computeFitness(gardenCopy, width, height))
        resultGardens.append(gardenCopy)
    return results, resultGardens




def computeFitness(garden, width, height):
    counter = 0
    for i in range(0, height):
        for j in range(0, width):
            if garden[i][j] != 0 and garden[i][j] != -1:
                counter += 1
    return counter


startGame()