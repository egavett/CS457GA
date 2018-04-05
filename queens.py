import random
import operator

class Solution(object):
    def __init__(self, fitness, solutionString):
        self.fitness = fitness  # the number of conflicts; -1 for unevaluated
        self.solutionString = solutionString

'''
Inversion Methods
use invertNum and invertSolution to crossover strings by inverting some or all of their values
'''

def invertNum(num, n):
    """
    Return the inversion of a digit in a solution string
    num: the integer to be inverted
    n: the degree of the n-queens problem
    """
    return num - n - 1 

def invertSolution(solution, n):
    """Return the inverstion of a given string"""
    newSolution = ""
    for c in solution:
        num = int(c)
        num = invertNum(num, n)
        newSolution += str(num)
    return newSolution

'''
Crossover mehtods
Use crossoverSolutions to splice two solutions together at a specified index
Use attemptMutation to preform possible mutation on a solution string
'''
def attemptMutation(solution,n):
    s = list(solution)
    for i in range(1, n*2, 2):  # only touch characters that were randomly generated
        if random.random() < 0.01:
            s[i] = str(random.randint(0,n-1))
    
    solution = "".join(s)
    return solution

def crossoverSolutions(parent1, parent2, i):
    """
    Crossover two parents by spliting both at index i and splicing the remains together
    """
    children = []
    children.append(Solution(-1, parent1[:i]+parent2[i:]))
    children.append(Solution(-1, parent2[:i]+parent1[i:]))
    return children

'''
Fitness Fuction
'''
def evaluateSolution(solution, n):
    """
    Evaluate a solution by counting the number of conflicts that occur  
    """
    score = 0 
    board = [[0 for _ in range(n)] for _ in range(n)]
    pieces = [solution[i:i+2] for i in range(0, len(solution), 2)] 

    for piece in pieces:
        # place the piece on the board
        x, y = int(piece[0]), int(piece[1])
        if board[x][y] == 0:    # check if a piece has already been placed on the square
            board[x][y] += 1
            # check for conflicts
            for i in range(n):
                # row conflicts
                if i != x and board[i][y] != 0:
                    score += 1
                # column conflicts
                if i != y and board[x][i] != 0:
                    score += 1
                # diagonal conflicts
                diff = abs(y-i) # the difference between the current row and the row the queen is on
                if diff != 0:   # not necessary on the row the queen is in
                    if x-diff >= 0: # stay on the board
                        if board[x-diff][i] != 0:
                            score += 1
                    if x+diff < n:  # stay on the board
                        if board[x+diff][i] != 0:
                            score += 1
        else:
            score += 1
    return score

'''
Generation Method
Ensures that each row in the solution has only one queen
'''
def generateSolution(n):
    solution = ""
    for i in range(n):
        solution += str(i)  #current row
        solution += str(random.randint(0,n-1))  # random column
    return solution


'''
Main
'''
# 4-Queens problem, but solution is general
n = 4 

# Generate initial solutions
solutionCount = 4 * n
solutions = []
for _ in range(solutionCount): 
    solutions.append(Solution(-1, generateSolution(n)))

# Repeat process until a valid solution is found
generation = 0
while(True):
    print("Current Generation: " + str(generation))

    # Evaluate solutions
    for sol in solutions:
        sol.fitness = evaluateSolution(sol.solutionString, n)
    solutions.sort(key = operator.attrgetter('fitness'))

    # Console output
    print("Sorted fitnesses of current generation")
    for s in solutions:
        print(s.fitness)
    print("--------------------------------------")
    # Check if solution found
    if solutions[0].fitness == 0:
        break

    # Apply Crossover; select best four parents
    parent1, parent2 = solutions[0], solutions[1]
    parent3, parent4 = solutions[0], solutions[1]
    del solutions   # clear unneeded solutions; manage memory
    solutions = [parent1, parent2, parent3, parent4]
    for i in range(2, n*2, 2):  # all even numbers 2-2n
        solutions.extend((crossoverSolutions(parent1.solutionString, parent2.solutionString, i)))
        solutions.extend((crossoverSolutions(parent3.solutionString, parent4.solutionString, i)))

    # Apply Mutation 
    for sol in solutions:
        sol.solutionString = attemptMutation(sol.solutionString, n)
    generation += 1

# Output results
print()
print("Solution found after " + str(generation) + " generations.")
result = solutions[0].solutionString
print("The solution string is: " + result)

# Output as a chessboard
board = [[0 for _ in range(n)] for _ in range(n)]
pieces = [result[i:i+2] for i in range(0, len(result), 2)] 
for piece in pieces:
    x, y = int(piece[0]), int(piece[1])
    board[x][y] += 1

print("Chessboard view:")
for row in board:
    print(row)