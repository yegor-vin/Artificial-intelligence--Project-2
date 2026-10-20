import random



def main():

    populations = [2,3]
    matrixWidth = int(input("Enter garden width: "))
    matrixHeight = int(input("Enter garden height: "))
    numberOfStones = int (input("Enter number of stones: "))
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
        gardenMatrix[x][y] = -1

    maxFitness = matrixWidth * matrixHeight - numberOfStones

    matrixPerimeter = (matrixWidth + matrixHeight) * 2
    maxNumberOfGenes = matrixPerimeter // 2 + numberOfStones

    for populationSize in populations:
       population = generateChromosomes(maxNumberOfGenes, populationSize, matrixPerimeter)

       fitnessValues = performRake(gardenMatrix, population, matrixWidth, matrixHeight, matrixPerimeter)







def generateChromosomes(genesNumber, populationSize, perimeter):
    generatedChromosomes = [
    [0] * genesNumber
    for _ in range(populationSize)
    ]


    for i in range(0, populationSize):
        for j in range(0,genesNumber):
            generatedChromosomes[i][j] = random.randint(1, perimeter)

    return generatedChromosomes





def performRake(garden, population, width, height, perimeter):
    gardenCopy = [row.copy() for row in garden]

    results = []
    for chromosome in population:
        for gene in chromosome:

            if 1 <= gene <= height:
                x, y = (0, gene)
                if gardenCopy[x][y] == 1 or gardenCopy[x][y] == -1:
                    continue

                for i in range(0, width):
                    gardenCopy[x + i][y] = 1
                    nextX = x+i+1
                    nextY = y+1
                    prevY = y-1
                    if nextX < width and (gardenCopy[nextX][y] == -1 or gardenCopy[nextX][y] == 1):
                        if nextY < height and (gardenCopy[x+i][y+1] != -1 and gardenCopy[x+i][y+1] != 1):
                            y += 1
                            gardenCopy[x+i][y] = 1
                        elif prevY > 0 and (gardenCopy[x+i][y-1] != -1 and gardenCopy[x+i][y-1] != 1):
                            y -= 1
                            gardenCopy[x+i][y] = 1


            elif height < gene <= perimeter // 2:
                x, y = (gene - height, height)
                if gardenCopy[x][y] == 1 or gardenCopy[x][y] == -1:
                    continue


                for i in range(0, height):
                    gardenCopy[x][y-i] = 1
                    nextY = y-i-1
                    nextX = x + 1
                    prevX = x -1
                    if nextY > 0 and (gardenCopy[x][nextY] == -1 or gardenCopy[x][nextY] == 1):
                        if prevX > 0 and (gardenCopy[x-1][y-i] != -1 and gardenCopy[x-1][y-i] != 1):
                            x -= 1
                            gardenCopy[x][y-i] = 1
                        elif nextX < width and (gardenCopy[x+1][y - i] != -1 and gardenCopy[x+1][y - i] != 1):
                            x += 1
                            gardenCopy[x][y-i] = 1



            elif perimeter // 2 < gene <=  (perimeter // 2) + height:
                x, y = (width - 1, abs((gene - perimeter // 2) - height))
                if gardenCopy[x][y] == 1 or gardenCopy[x][y] == -1:
                    continue


                for i in range(0, width):
                    gardenCopy[x - i][y] = 1
                    nextX = x-i-1
                    nextY = y+1
                    prevY = y-1
                    if nextX > 0 and (gardenCopy[nextX][y] == -1 or gardenCopy[nextX][y] == 1):
                        if nextY < height and (gardenCopy[x - i][y + 1] != -1 and gardenCopy[x - i][y + 1] != 1):
                            y += 1
                            gardenCopy[x - i][y] = 1
                        elif prevY > 0 and (gardenCopy[x - i][y - 1] != -1 and gardenCopy[x - i][y - 1] != 1):
                            y -= 1
                            gardenCopy[x - i][y] = 1

            elif (perimeter // 2) + height < gene <= perimeter:
                x, y = (abs(perimeter - gene), 0)
                if gardenCopy[x][y] == 1 or gardenCopy[x][y] == -1:
                    continue

                for i in range(0, height):
                    gardenCopy[x][y+i] = 1
                    nextY = y+i+1
                    nextX = x+1
                    prevX = x-1
                    if nextY < height and  (gardenCopy[x][nextY] == -1 or gardenCopy[x][nextY] == 1):
                        if prevX > 0 and (gardenCopy[x-1][y+i] != -1 and gardenCopy[x-1][y+i] != 1):
                            x -= 1
                            gardenCopy[x][y+i] = 1
                        elif nextX < width and (gardenCopy[x+1][y + i] != -1 and gardenCopy[x+1][y + i] != 1):
                            x += 1
                            gardenCopy[x][y+i] = 1

        computeFitness(gardenCopy, width, height)







def computeFitness(garden, width, height):
    counter = 0
    for i in range(0, height):
        for j in range(0, width):
            if garden[i][j] == 1:
                counter += 1

    return counter








main()