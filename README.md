# Zen Garden – Genetic Algorithm

Artificial Intelligence, Assignment 2a (FIIT STU)

A monk rakes a Zen garden in straight strips. He enters from the edge, walks straight until he leaves the garden or hits an obstacle (a stone or already raked sand), and then turns left or right. If he cannot turn, the game ends. This program uses a **genetic algorithm** to find the entry points and turn decisions that rake as many cells as possible, ideally the whole garden.

## Requirements

- Python 3.12 or newer
- matplotlib (for the fitness graphs)

Install the dependencies with [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

or with pip:

```bash
pip install matplotlib
```

## Running

```bash
python main.py
```

The program asks for the garden and the GA settings, in this order:

1. garden width
2. garden height
3. selection method: `0` = tournament, `1` = rank
4. mutation method: `0` = random, `1` = multiplicative
5. number of stones
6. coordinates of each stone as `x y` (x = column, y = row, both counted from 0)

### Example: garden from the assignment

12 × 10 garden with 6 stones (114 free cells):

```
Enter garden width: 12
Enter garden height: 10
Enter selection number 0 - tournament, 1 - rank: 0
Enter mutation number 0 - random, 1 - multiplicative: 0
Enter number of stones: 6
Enter coordinates of stone 1 (x y): 5 1
Enter coordinates of stone 2 (x y): 1 2
Enter coordinates of stone 3 (x y): 4 3
Enter coordinates of stone 4 (x y): 2 4
Enter coordinates of stone 5 (x y): 8 6
Enter coordinates of stone 6 (x y): 9 6
```

## Output

- **Console:** the best raked garden found. Each cell holds the number of the pass that raked it; `-1` is a stone and `0` is a cell that was not raked.
- **`fitness-<selection>-<mutation>.png`:** max, mean and min fitness per generation, one panel per population size.
- **`comparison-<selection>-<mutation>.png`:** max and mean fitness of all population sizes in one graph.

Example of a fully raked garden (114/114 cells):

```
14 13 12 11 11 16  4  4  2  6  9  9
13 13 12 11 11 -1  4  4  2  6  8  8
12 -1 12 11 11 11  4  4  2  6  8  8
12 12 12 11 -1 11  4  4  2  6  6  6
12 12 -1 11 11 11  4  4  2  2  2  2
 1  1  1  1  1  1  1  1  1  1  1  1
 3  3  3  3  3  3  3  3 -1 -1  7  7
15 15 15 15 15 15 15  3 10 10  7  7
15 15 15 15 15 15 15  3 10 10  7  7
 5  5  5  5  5  5  5  3 10 10  7  7
```

## How it works

- **Genes.** A chromosome is a list of integers from `0` to `P − 1`, where `P = 2·(W + H)` is the number of entry points on the perimeter. Each value names a start cell and direction, numbered counterclockwise: left edge (moving right), bottom edge (moving up), right edge (moving left), top edge (moving down). The same genes also supply the turn decisions: when both turns are free, the monk takes option `chromosome[t] % 2`, and `t` moves to the next gene.
- **Chromosome length:** `max(3, int(0.85 · (W + H + stones)))`, i.e. 23 genes for the example garden. The assignment's limit is 28.
- **Fitness:** the number of raked cells. The optimum is `W·H − stones`.
- **Elitism:** the 2 best chromosomes pass unchanged to the next generation.
- **Selection:** tournament (k = 2) or rank selection.
- **Crossover:** two-point crossover, probability 0.7.
- **Mutation:** probability 0.1 per gene. *Random* mutation replaces the gene with a new random entry point. *Multiplicative* mutation multiplies it by a factor from 0.7 to 1.3, which moves the entry point a little along the edge.
- **Stop condition:** the whole garden is raked, or 1000 generations have passed.

The GA runs once for each population size in `POPULATIONS` (30, 50 and 100). The best garden over all runs is printed.

## Parameters

| Parameter | Value | Where |
| --- | --- | --- |
| Selection method | tournament / rank | input |
| Mutation method | random / multiplicative | input |
| Population sizes | 30, 50, 100 | `POPULATIONS` in `game.py` |
| Chromosome length | 0.85 · (W + H + stones) | `startGame` |
| Max generations | 1000 | `geneticAlgorithm` |
| Elites | 2 | `geneticAlgorithm` |
| Tournament size | 2 | `geneticAlgorithm` |
| Crossover probability | 0.7 | `crossover` |
| Mutation probability | 0.1 per gene | `mutationFn` |

## Project structure

| File | Content |
| --- | --- |
| `main.py` | entry point; runs the game and prints the best garden |
| `game.py` | input, garden, monk simulation, fitness, selection, crossover, mutation, GA loop |
| `fitnessVisual.py` | fitness graphs (matplotlib) |
| `pyproject.toml`, `uv.lock` | project dependencies |

The full description of the algorithm, the experiments and the results is in the documentation (`Zen_Garden_Documentation.docx`).
