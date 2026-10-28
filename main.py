from game import startGame


def main():
    outputMatrix = startGame()

    for row in outputMatrix:
        for el in row:
            print(el, end=" ")
        print("\n")


main()