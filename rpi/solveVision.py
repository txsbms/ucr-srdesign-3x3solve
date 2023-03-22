from picamera2 import Picamera2, Preview
import copy as cp
import random as rd
import serial
import time
import textwrap
import cv2
import numpy as np
import math

#################################################
#                                               #
#       CUBE SOLVING ALGORITHM FUNCTIONS        #
#                                               #
#################################################

# RearrangeCube takes a "cube" (in the same format as the global variable in
# this script) and returns a list which of lines that can be printed to visually
# represent the cube.
def RearrangeCube(cube):
    cubeLine1 = []
    cubeLine2 = []
    cubeLine3 = []
    cubeLine4 = []
    cubeLine5 = []
    cubeLine6 = []
    cubeLine7 = []
    cubeLine8 = []
    cubeLine9 = []

    for i in range(3):
        cubeLine1.append(cube[0][i])
        cubeLine7.append(cube[5][i])

    for i in range(3, 6):
        cubeLine2.append(cube[0][i])
        cubeLine8.append(cube[5][i])

    for i in range(6, 9):
        cubeLine3.append(cube[0][i])
        cubeLine9.append(cube[5][i])

    for i in range(1, 5):
        for j in range(3):
            cubeLine4.append(cube[i][j])

        for j in range(3, 6):
            cubeLine5.append(cube[i][j])

        for j in range(6, 9):
            cubeLine6.append(cube[i][j])

    return [cubeLine1, cubeLine2, cubeLine3,
            cubeLine4, cubeLine5, cubeLine6,
            cubeLine7, cubeLine8, cubeLine9]

# CubePrint relies on RearrangeCube and outputs the result of it line by line.
def CubePrint(cube):
    printedCube = RearrangeCube(cube)
    for i in range(9):
        if ((i < 3) or (i > 5)):
            print('   ', end='')
        for j in range(len(printedCube[i])):
            print(printedCube[i][j], end='')
        print('')
    return

# FacePrint prints a given face of a cube; mainly for debug purposes.
def FacePrint(face):
    for i in range(9):
        print(face[i], end='')
        if ((i + 1) % 3 == 0):
            print('')
    return

# Rotates the face of a cube counter-clockwise for a given move.
# Useful for all moves in the cube's moveset (FRUBLD).
def CCWRotate(face):
    for i in range(2):
        tmpA = face[0]
        face[0] = face[1]
        face[1] = face[2]
        face[2] = face[5]
        face[5] = face[8]
        face[8] = face[7]
        face[7] = face[6]
        face[6] = face[3]
        face[3] = tmpA
    return face

# Same as CCWRotate but clockwise.
def CWRotate(face):
    for i in range(2):
        tmpA = face[0]
        face[0] = face[3]
        face[3] = face[6]
        face[6] = face[7]
        face[7] = face[8]
        face[8] = face[5]
        face[5] = face[2]
        face[2] = face[1]
        face[1] = tmpA
    return face

# Corresponds to F on a cube.
def moveF():
    global cube
    global movesDone
    CWRotate(cube[2])
    tmpA = [cube[0][6], cube[0][7], cube[0][8]]
    cube[0][6] = cube[1][8]
    cube[0][7] = cube[1][5]
    cube[0][8] = cube[1][2]

    cube[1][8] = cube[5][2]
    cube[1][5] = cube[5][1]
    cube[1][2] = cube[5][0]

    cube[5][2] = cube[3][0]
    cube[5][1] = cube[3][3]
    cube[5][0] = cube[3][6]

    cube[3][0] = tmpA[0]
    cube[3][3] = tmpA[1]
    cube[3][6] = tmpA[2]

    movesDone.append('F')
    return

# Corresponds to F' on a cube.
def moveFP():
    global cube
    global movesDone
    CCWRotate(cube[2])
    tmpA = [cube[0][6], cube[0][7], cube[0][8]]
    cube[0][6] = cube[3][0]
    cube[0][7] = cube[3][3]
    cube[0][8] = cube[3][6]

    cube[3][0] = cube[5][2]
    cube[3][3] = cube[5][1]
    cube[3][6] = cube[5][0]

    cube[5][2] = cube[1][8]
    cube[5][1] = cube[1][5]
    cube[5][0] = cube[1][2]

    cube[1][8] = tmpA[0]
    cube[1][5] = tmpA[1]
    cube[1][2] = tmpA[2]

    movesDone.append('F\'')
    return

# Corresponds to F2 on a cube.
def moveF2():
    global cube
    global movesDone
    for i in range(2):
        moveF()

    movesDone.pop()
    movesDone.pop()
    movesDone.append('F2')
    return

# Corresponds to R on a cube.
def moveR():
    global cube
    global movesDone
    CWRotate(cube[3])
    tmpA = [cube[0][2], cube[0][5], cube[0][8]]
    cube[0][2] = cube[2][2]
    cube[0][5] = cube[2][5]
    cube[0][8] = cube[2][8]

    cube[2][2] = cube[5][2]
    cube[2][5] = cube[5][5]
    cube[2][8] = cube[5][8]

    cube[5][2] = cube[4][6]
    cube[5][5] = cube[4][3]
    cube[5][8] = cube[4][0]

    cube[4][6] = tmpA[0]
    cube[4][3] = tmpA[1]
    cube[4][0] = tmpA[2]

    movesDone.append('R')
    return

# Corresponds to R' on a cube.
def moveRP():
    global cube
    global movesDone
    CCWRotate(cube[3])
    tmpA = [cube[0][2], cube[0][5], cube[0][8]]
    cube[0][2] = cube[4][6]
    cube[0][5] = cube[4][3]
    cube[0][8] = cube[4][0]

    cube[4][6] = cube[5][2]
    cube[4][3] = cube[5][5]
    cube[4][0] = cube[5][8]

    cube[5][2] = cube[2][2]
    cube[5][5] = cube[2][5]
    cube[5][8] = cube[2][8]

    cube[2][2] = tmpA[0]
    cube[2][5] = tmpA[1]
    cube[2][8] = tmpA[2]

    movesDone.append('R\'')
    return

# Corresponds to R2 on a cube.
def moveR2():
    global cube
    global movesDone
    for i in range(2):
        moveR()

    movesDone.pop()
    movesDone.pop()
    movesDone.append('R2')
    return

# Corresponds to U on a cube.
def moveU():
    global cube
    global movesDone
    CWRotate(cube[0])
    tmpA = [cube[1][0], cube[1][1], cube[1][2]]
    cube[1][0] = cube[2][0]
    cube[1][1] = cube[2][1]
    cube[1][2] = cube[2][2]

    cube[2][0] = cube[3][0]
    cube[2][1] = cube[3][1]
    cube[2][2] = cube[3][2]

    cube[3][0] = cube[4][0]
    cube[3][1] = cube[4][1]
    cube[3][2] = cube[4][2]

    cube[4][0] = tmpA[0]
    cube[4][1] = tmpA[1]
    cube[4][2] = tmpA[2]

    movesDone.append('U')
    return

# Corresponds to U' on a cube.
def moveUP():
    global cube
    global movesDone
    CCWRotate(cube[0])
    tmpA = [cube[1][0], cube[1][1], cube[1][2]]
    cube[1][0] = cube[4][0]
    cube[1][1] = cube[4][1]
    cube[1][2] = cube[4][2]

    cube[4][0] = cube[3][0]
    cube[4][1] = cube[3][1]
    cube[4][2] = cube[3][2]

    cube[3][0] = cube[2][0]
    cube[3][1] = cube[2][1]
    cube[3][2] = cube[2][2]

    cube[2][0] = tmpA[0]
    cube[2][1] = tmpA[1]
    cube[2][2] = tmpA[2]

    movesDone.append('U\'')
    return

# Corresponds to U2 on a cube.
def moveU2():
    global cube
    global movesDone
    for i in range(2):
        moveU()

    movesDone.pop()
    movesDone.pop()
    movesDone.append('U2')
    return

# Corresponds to B on a cube.
def moveB():
    global cube
    global movesDone
    CWRotate(cube[4])
    tmpA = [cube[0][0], cube[0][1], cube[0][2]]
    cube[0][0] = cube[3][2]
    cube[0][1] = cube[3][5]
    cube[0][2] = cube[3][8]

    cube[3][2] = cube[5][8]
    cube[3][5] = cube[5][7]
    cube[3][8] = cube[5][6]

    cube[5][8] = cube[1][6]
    cube[5][7] = cube[1][3]
    cube[5][6] = cube[1][0]

    cube[1][6] = tmpA[0]
    cube[1][3] = tmpA[1]
    cube[1][0] = tmpA[2]

    movesDone.append('B')
    return

# Corresponds to B' on a cube.
def moveBP():
    global cube
    global movesDone
    CCWRotate(cube[4])
    tmpA = [cube[0][0], cube[0][1], cube[0][2]]
    cube[0][0] = cube[1][6]
    cube[0][1] = cube[1][3]
    cube[0][2] = cube[1][0]

    cube[1][6] = cube[5][8]
    cube[1][3] = cube[5][7]
    cube[1][0] = cube[5][6]

    cube[5][8] = cube[3][2]
    cube[5][7] = cube[3][5]
    cube[5][6] = cube[3][8]

    cube[3][2] = tmpA[0]
    cube[3][5] = tmpA[1]
    cube[3][8] = tmpA[2]

    movesDone.append('B\'')
    return

# Corresponds to B2 on a cube.
def moveB2():
    global cube
    global movesDone
    for i in range(2):
        moveB()

    movesDone.pop()
    movesDone.pop()
    movesDone.append('B2')
    return

# Corresponds to L on a cube.
def moveL():
    global cube
    global movesDone
    CWRotate(cube[1])
    tmpA = [cube[0][0], cube[0][3], cube[0][6]]
    cube[0][0] = cube[4][8]
    cube[0][3] = cube[4][5]
    cube[0][6] = cube[4][2]

    cube[4][8] = cube[5][0]
    cube[4][5] = cube[5][3]
    cube[4][2] = cube[5][6]

    cube[5][0] = cube[2][0]
    cube[5][3] = cube[2][3]
    cube[5][6] = cube[2][6]

    cube[2][0] = tmpA[0]
    cube[2][3] = tmpA[1]
    cube[2][6] = tmpA[2]

    movesDone.append('L')
    return

# Corresponds to L' on a cube.
def moveLP():
    global cube
    global movesDone
    CCWRotate(cube[1])
    tmpA = [cube[0][0], cube[0][3], cube[0][6]]
    cube[0][0] = cube[2][0]
    cube[0][3] = cube[2][3]
    cube[0][6] = cube[2][6]

    cube[2][0] = cube[5][0]
    cube[2][3] = cube[5][3]
    cube[2][6] = cube[5][6]

    cube[5][0] = cube[4][8]
    cube[5][3] = cube[4][5]
    cube[5][6] = cube[4][2]

    cube[4][8] = tmpA[0]
    cube[4][5] = tmpA[1]
    cube[4][2] = tmpA[2]

    movesDone.append('L\'')
    return

# Corresponds to L2 on a cube.
def moveL2():
    global cube
    global movesDone
    for i in range(2):
        moveL()

    movesDone.pop()
    movesDone.pop()
    movesDone.append('L2')
    return

# Corresponds to D on a cube.
def moveD():
    global cube
    global movesDone
    CWRotate(cube[5])
    tmpA = [cube[1][6], cube[1][7], cube[1][8]]
    cube[1][6] = cube[4][6]
    cube[1][7] = cube[4][7]
    cube[1][8] = cube[4][8]

    cube[4][6] = cube[3][6]
    cube[4][7] = cube[3][7]
    cube[4][8] = cube[3][8]

    cube[3][6] = cube[2][6]
    cube[3][7] = cube[2][7]
    cube[3][8] = cube[2][8]

    cube[2][6] = tmpA[0]
    cube[2][7] = tmpA[1]
    cube[2][8] = tmpA[2]

    movesDone.append('D')
    return

# Corresponds to D' on a cube.
def moveDP():
    global cube
    global movesDone
    CCWRotate(cube[5])
    tmpA = [cube[1][6], cube[1][7], cube[1][8]]
    cube[1][6] = cube[2][6]
    cube[1][7] = cube[2][7]
    cube[1][8] = cube[2][8]

    cube[2][6] = cube[3][6]
    cube[2][7] = cube[3][7]
    cube[2][8] = cube[3][8]

    cube[3][6] = cube[4][6]
    cube[3][7] = cube[4][7]
    cube[3][8] = cube[4][8]

    cube[4][6] = tmpA[0]
    cube[4][7] = tmpA[1]
    cube[4][8] = tmpA[2]

    movesDone.append('D\'')
    return

# Corresponds to D2 on a cube.
def moveD2():
    global cube
    global movesDone
    for i in range(2):
        moveD()

    movesDone.pop()
    movesDone.pop()
    movesDone.append('D2')
    return

# Prints all moves stored in global variable movesDone to console.
def PrintMoves():
    global movesDone
    for i in range(len(movesDone) - 1):
        print(movesDone[i], end=' ')
    print(movesDone[len(movesDone) - 1])
    return

# Prints all moves stored in global variable allMoves to console.
def PrintAllMoves():
    global allMoves
    for i in range(len(allMoves) - 1):
        print(allMoves[i], end=' ')
    print(allMoves[len(allMoves) - 1])
    return

# Performs 21 random moves on the cube. Does not repeat moves.
# ie. F F' is not valid, nor is U2 U.
def ScrambleCube():
    ResetMovesDone()
    moveSetScr = [moveF, moveR, moveU, moveB, moveL, moveD,
               moveFP, moveRP, moveUP, moveBP, moveLP, moveDP,
               moveF2, moveR2, moveU2, moveB2, moveL2, moveD2]
    moveSetScrF = [moveR, moveU, moveL, moveD, moveB,
                 moveRP, moveUP, moveLP, moveDP, moveBP,
                 moveR2, moveU2, moveL2, moveD2, moveB2]
    moveSetScrR = [moveF, moveU, moveL, moveD, moveB,
                 moveFP, moveUP, moveLP, moveDP, moveBP,
                 moveF2, moveU2, moveL2, moveD2, moveB2]
    moveSetScrU = [moveR, moveF, moveL, moveD, moveB,
                 moveRP, moveFP, moveLP, moveDP, moveBP,
                 moveR2, moveF2, moveL2, moveD2, moveB2]
    moveSetScrL = [moveR, moveU, moveF, moveD, moveB,
                 moveRP, moveUP, moveFP, moveDP, moveBP,
                 moveR2, moveU2, moveF2, moveD2, moveB2]
    moveSetScrD = [moveR, moveU, moveL, moveF, moveB,
                 moveRP, moveUP, moveLP, moveFP, moveBP,
                 moveR2, moveU2, moveL2, moveF2, moveB2]
    moveSetScrB = [moveR, moveU, moveL, moveF, moveD,
                 moveRP, moveUP, moveLP, moveFP, moveDP,
                 moveR2, moveU2, moveL2, moveF2, moveD2]

    for i in range(21):
        if (len(movesDone) == 0):
            rd.choice(moveSetScr)()
        elif(movesDone[-1][0] == 'F'):
            rd.choice(moveSetScrF)()
        elif(movesDone[-1][0] == 'R'):
            rd.choice(moveSetScrR)()
        elif(movesDone[-1][0] == 'U'):
            rd.choice(moveSetScrU)()
        elif(movesDone[-1][0] == 'L'):
            rd.choice(moveSetScrL)()
        elif(movesDone[-1][0] == 'D'):
            rd.choice(moveSetScrD)()
        elif(movesDone[-1][0] == 'B'):
            rd.choice(moveSetScrB)()
        else:
            rd.choice(moveSetScr)()
    return

# Clears global variable movesDone.
def ResetMovesDone():
    global movesDone
    movesDone = []
    return

# Executes moves specified in set.
def ExecuteMoves(moveList):
    for i in range(len((moveList))):
        moveList[i]()
    return

# Checks to see how many edges are solved in the "Yellow Cross" step.
# Returns number of edges solved.
def NumEdgesSolved():
    global cube
    cnt = 0
    if ((cube[5][3] == 'Y') and (cube[1][7] == 'O')):
        cnt += 1
    if ((cube[5][1] == 'Y') and (cube[2][7] == 'G')):
        cnt += 1
    if ((cube[5][5] == 'Y') and (cube[3][7] == 'R')):
        cnt += 1
    if ((cube[5][7] == 'Y') and (cube[4][7] == 'B')):
        cnt += 1
    return cnt

def MissingEdgeColor():
    global cube
    if (cube[5][7] != 'Y'):
        return 'B'
    elif(cube[5][5] != 'Y'):
        return 'R'
    elif(cube[5][3] != 'Y'):
        return 'O'
    elif(cube[5][1] != 'Y'):
        return 'G'
    return 'Error'

def FindMissingEdge():
    global cube
    for i in range(5):
        for j in range(1, 8, 2):
            if (cube[i][j] == 'Y'):
                return list([i, j])
    return 0

# Solves the "Yellow Cross".
# First creates a deep copy of global variable cube.
# Performs a random sequence of 5 moves (non-repeating) until an edge is solved.
# Prints moves used to solve this step and pushes them to global variable solveMoves.
def Cross():
    global cube, movesDone, solveMoves
    global moveSetAll, moveSetF, moveSetR, moveSetB, moveSetL, moveSetU
    global crossMoves

    cubeCopy = cp.deepcopy(cube)
    cnt = 0

    ResetMovesDone()
    print("Solving Cross...")
    for i in range(1, 4):
        while not (NumEdgesSolved() == i):
            cube = cp.deepcopy(cubeCopy)
            ResetMovesDone()
            cnt += 1
            for j in range(5):
                if (len(movesDone) == 0):
                    rd.choice(moveSetAll)()
                elif(movesDone[-1][0] == 'F'):
                    rd.choice(moveSetF)()
                elif(movesDone[-1][0] == 'R'):
                    rd.choice(moveSetR)()
                elif(movesDone[-1][0] == 'U'):
                    rd.choice(moveSetU)()
                elif(movesDone[-1][0] == 'L'):
                    rd.choice(moveSetL)()
                elif(movesDone[-1][0] == 'B'):
                    rd.choice(moveSetB)()
                else:
                    print("Error in solution for Yellow Cross " + str(i))
                if (NumEdgesSolved() == i):
                    break
            #print("Attempted Yellow Cross Step " + str(i) + " (" + str(cnt) + "): ", end='')
            #print(movesDone)

        #print("Partial solution found: ", end='')
        #for j in range(len(movesDone)):
            #print(movesDone[j], end=' ')
        #print('')

        cubeCopy = cp.deepcopy(cube)
        crossMoves = crossMoves + movesDone
        ResetMovesDone()
        cnt = 0

    #print("Executing Yellow Cross Step " + str(i + 3) + ".")
    mec = MissingEdgeColor()
    fme0 = FindMissingEdge()[0]
    fme1 = FindMissingEdge()[1]

    if (mec == 'G'):
        # Green Edge
        if (FindMissingEdge() == 0):
            pass
        elif (fme0 == 0):
            # White
            if (fme1 == 1):
                ExecuteMoves([moveU2, moveF2])
            elif (fme1 == 3):
                ExecuteMoves([moveUP, moveF2])
            elif (fme1 == 5):
                ExecuteMoves([moveU, moveF2])
            elif (fme1 == 7):    
                ExecuteMoves([moveF2])
        elif (fme0 == 1):
            # Orange
            if (fme1 == 1):
                ExecuteMoves([moveL, moveFP, moveLP])
            elif (fme1 == 3):
                ExecuteMoves([moveL2, moveFP, moveL2])
            elif (fme1 == 5):
                ExecuteMoves([moveFP])
        elif (fme0 == 2):
            # Green
            if (fme1 == 1):
                ExecuteMoves([moveLP, moveU, moveL, moveFP])
            elif (fme1 == 3):
                ExecuteMoves([moveF, moveLP, moveU, moveL, moveFP])
            elif (fme1 == 5):
                ExecuteMoves([moveFP, moveLP, moveU, moveL, moveFP])
            elif (fme1 == 7):    
                ExecuteMoves([moveF2, moveLP, moveU, moveL, moveFP])
        elif (fme0 == 3):
            # Red
            if (fme1 == 1):
                ExecuteMoves([moveRP, moveF, moveR])
            elif (fme1 == 3):
                ExecuteMoves([moveF])
            elif (fme1 == 5):
                ExecuteMoves([moveR2, moveF, moveR2])
        elif (fme0 == 4):
            # Blue
            if (fme1 == 1):
                ExecuteMoves([moveU2, moveR, moveUP, moveRP, moveF])
            elif (fme1 == 3):
                ExecuteMoves([moveB, moveU, moveBP, moveRP, moveF, moveR])
            elif (fme1 == 5):
                ExecuteMoves([moveBP, moveUP, moveB, moveL, moveFP, moveLP])
    elif (mec == 'R'):
        # Red Edge
        if (FindMissingEdge() == 0):
            pass
        elif (fme0 == 0):
            # White
            if (fme1 == 3):
                ExecuteMoves([moveU2, moveR2])
            elif (fme1 == 7):
                ExecuteMoves([moveUP, moveR2])
            elif (fme1 == 1):
                ExecuteMoves([moveU, moveR2])
            elif (fme1 == 5):    
                ExecuteMoves([moveR2])
        elif (fme0 == 1):
            # Orange
            if (fme1 == 1):
                ExecuteMoves([moveU2, moveB, moveUP, moveBP, moveR])
            elif (fme1 == 3):
                ExecuteMoves([moveL, moveU, moveLP, moveBP, moveR, moveB])
            elif (fme1 == 5):
                ExecuteMoves([moveLP, moveUP, moveL, moveF, moveRP, moveFP])
        elif (fme0 == 2):
            # Green
            if (fme1 == 1):
                ExecuteMoves([moveF, moveRP, moveFP])
            elif (fme1 == 3):
                ExecuteMoves([moveF2, moveRP, moveF2])
            elif (fme1 == 5):
                ExecuteMoves([moveRP])
        elif (fme0 == 3):
            # Red
            if (fme1 == 1):
                ExecuteMoves([moveFP, moveU, moveF, moveRP])
            elif (fme1 == 3):
                ExecuteMoves([moveR, moveFP, moveU, moveF, moveRP])
            elif (fme1 == 5):
                ExecuteMoves([moveRP, moveFP, moveU, moveF, moveRP])
            elif (fme1 == 7):    
                ExecuteMoves([moveR2, moveFP, moveU, moveF, moveRP])
        elif (fme0 == 4):
            # Blue
            if (fme1 == 1):
                ExecuteMoves([moveBP, moveR, moveB])
            elif (fme1 == 3):
                ExecuteMoves([moveR])
            elif (fme1 == 5):
                ExecuteMoves([moveB2, moveR, moveB2])
    elif (mec == 'B'):
        # Blue Edge
        if (FindMissingEdge() == 0):
            pass
        elif (fme0 == 0):
            # White
            if (fme1 == 7):
                ExecuteMoves([moveU2, moveB2])
            elif (fme1 == 5):
                ExecuteMoves([moveUP, moveB2])
            elif (fme1 == 3):
                ExecuteMoves([moveU, moveB2])
            elif (fme1 == 1):    
                ExecuteMoves([moveB2])
        elif (fme0 == 1):
            # Orange
            if (fme1 == 1):
                ExecuteMoves([moveLP, moveB, moveL])
            elif (fme1 == 3):
                ExecuteMoves([moveB])
            elif (fme1 == 5):
                ExecuteMoves([moveL2, moveB, moveL2])
        elif (fme0 == 2):
            # Green
            if (fme1 == 1):
                ExecuteMoves([moveU2, moveL, moveUP, moveLP, moveB])
            elif (fme1 == 3):
                ExecuteMoves([moveF, moveU, moveFP, moveLP, moveB, moveL])
            elif (fme1 == 5):
                ExecuteMoves([moveFP, moveUP, moveF, moveR, moveBP, moveRP])
        elif (fme0 == 3):
            # Red
            if (fme1 == 1):
                ExecuteMoves([moveR, moveBP, moveRP])
            elif (fme1 == 3):
                ExecuteMoves([moveR2, moveBP, moveR2])
            elif (fme1 == 5):
                ExecuteMoves([moveBP])
        elif (fme0 == 4):
            # Blue
            if (fme1 == 1):
                ExecuteMoves([moveRP, moveU, moveR, moveBP])
            elif (fme1 == 3):
                ExecuteMoves([moveB, moveRP, moveU, moveR, moveBP])
            elif (fme1 == 5):
                ExecuteMoves([moveBP, moveRP, moveU, moveR, moveBP])
            elif (fme1 == 7):    
                ExecuteMoves([moveB2, moveRP, moveU, moveR, moveBP])
    elif (mec == 'O'):
        # Orange Edge
        if (FindMissingEdge() == 0):
            pass
        elif (fme0 == 0):
            # White
            if (fme1 == 5):
                ExecuteMoves([moveU2, moveL2])
            elif (fme1 == 1):
                ExecuteMoves([moveUP, moveL2])
            elif (fme1 == 7):
                ExecuteMoves([moveU, moveL2])
            elif (fme1 == 3):    
                ExecuteMoves([moveL2])
        elif (fme0 == 1):
            # Orange
            if (fme1 == 1):
                ExecuteMoves([moveBP, moveU, moveB, moveLP])
            elif (fme1 == 3):
                ExecuteMoves([moveL, moveBP, moveU, moveB, moveLP])
            elif (fme1 == 5):
                ExecuteMoves([moveLP, moveBP, moveU, moveB, moveLP])
            elif (fme1 == 7):    
                ExecuteMoves([moveL2, moveBP, moveU, moveB, moveLP])
        elif (fme0 == 2):
            # Green
            if (fme1 == 1):
                ExecuteMoves([moveFP, moveL, moveF])
            elif (fme1 == 3):
                ExecuteMoves([moveL])
            elif (fme1 == 5):
                ExecuteMoves([moveF2, moveL, moveF2])
        elif (fme0 == 3):
            # Red
            if (fme1 == 1):
                ExecuteMoves([moveU2, moveF, moveUP, moveFP, moveL])
            elif (fme1 == 3):
                ExecuteMoves([moveR, moveU, moveRP, moveFP, moveL, moveF])
            elif (fme1 == 5):
                ExecuteMoves([moveRP, moveUP, moveR, moveB, moveLP, moveBP])
        elif (fme0 == 4):
            # Blue
            if (fme1 == 1):
                ExecuteMoves([moveB, moveLP, moveBP])
            elif (fme1 == 3):
                ExecuteMoves([moveB2, moveLP, moveB2])
            elif (fme1 == 5):
                ExecuteMoves([moveLP])  

        #print("Partial solution found: ", end='')
        #for j in range(len(movesDone)):
        #    print(movesDone[j], end=' ')
        #print('')

    crossMoves = crossMoves + movesDone

    print("Cross solution found.")
    #print("Yellow Cross solution found: ", end='')
    #for i in range(len(crossMoves)):
        #print(crossMoves[i], end='')
        #if (i != (len(crossMoves) - 1)):
            #print(' ', end='')
    #print('')

    solveMoves = solveMoves + crossMoves
    return

def LocCorHelper(x1, y1, x2, y2, x3, y3, colors):
    checkVals = set()
    checkVals.update(cube[x1][y1], cube[x2][y2], cube[x3][y3])
    if (set(colors) == checkVals):
        #print("Corner located at ["+str(x1)+"]["+str(y1)+"], ["+str(x2)+"][" \
        #      +str(y2)+"], ["+str(x3)+"]["+str(y3)+"]")
        checkVals.clear()
        return 1
    checkVals.clear()
    return 0

# LocateCorner returns position of corner given string of colors desired.
# For instance, in a solved cube, "GRW" will return [08, 22, 30]
# This corresponds to cube[0][8], cube[2][2], cube[3][0]
def LocateCorner(colors):
    # Coordinates of all corner locations:
    # --------------  Top  Layer  -------------
    # locA = cube[0][0], cube[1][0], cube[4][2]
    # locB = cube[0][2], cube[3][2], cube[4][0]
    # locC = cube[0][6], cube[1][2], cube[2][0]
    # locD = cube[0][8], cube[2][2], cube[3][0]
    # -------------- Bottom Layer -------------
    # locE = cube[5][0], cube[1][8], cube[2][6]
    # locF = cube[5][2], cube[2][8], cube[3][6]
    # locG = cube[5][6], cube[1][6], cube[4][8]
    # locH = cube[5][8], cube[3][8], cube[4][6]

    global cube

    if (LocCorHelper(0, 0, 1, 0, 4, 2, colors)):
        return "001042"
    elif (LocCorHelper(0, 2, 3, 2, 4, 0, colors)):
        return "023240"
    elif (LocCorHelper(0, 6, 1, 2, 2, 0, colors)):
        return "061220"
    elif (LocCorHelper(0, 8, 2, 2, 3, 0, colors)):
        return "082230"
    elif (LocCorHelper(5, 0, 1, 8, 2, 6, colors)):
        return "501826"
    elif (LocCorHelper(5, 2, 2, 8, 3, 6, colors)):
        return "522836"
    elif (LocCorHelper(5, 6, 1, 6, 4, 8, colors)):
        return "561648"
    elif (LocCorHelper(5, 8, 3, 8, 4, 6, colors)):
        return "583846"
    else:
        print("Error in locating corner!")
        return 0

# Kicks a corner piece up from the bottom layer to the top layer.
def KickCorner(locStr):
    global cube, movesDone, solveMoves
    global cornerMoves

    ResetMovesDone()

    if (locStr == "501826"):
        ExecuteMoves([moveF, moveU, moveFP])
    elif (locStr == "522836"):
        ExecuteMoves([moveR, moveU, moveRP])
    elif (locStr == "561648"):
        ExecuteMoves([moveL, moveU, moveLP])
    elif (locStr == "583846"):
        ExecuteMoves([moveB, moveU, moveBP])
    else:
        return

    cornerMoves = cornerMoves + movesDone
    return

# Moves a corner piece down to the bottom layer in the correct orientation.
def MoveCornerDown(locStr):
    global cube, movesDone, solveMoves, cornerMoves

    ResetMovesDone()

    if (locStr == "001042"):
        if (cube[0][0] == 'Y'):
            ExecuteMoves([moveL, moveU2, moveLP, moveUP, moveL, moveU, moveLP])
        elif (cube[4][2] == 'Y'):
            ExecuteMoves([moveU, moveL, moveUP, moveLP])
        else:
            ExecuteMoves([moveL, moveU, moveLP])
    if (locStr == "023240"):
        if (cube[0][2] == 'Y'):
            ExecuteMoves([moveB, moveU2, moveBP, moveUP, moveB, moveU, moveBP])
        elif (cube[3][2] == 'Y'):
            ExecuteMoves([moveU, moveB, moveUP, moveBP])
        else:
            ExecuteMoves([moveB, moveU, moveBP])
    if (locStr == "061220"):
        if (cube[0][6] == 'Y'):
            ExecuteMoves([moveF, moveU2, moveFP, moveUP, moveF, moveU, moveFP])
        elif (cube[1][2] == 'Y'):
            ExecuteMoves([moveU, moveF, moveUP, moveFP])
        else:
            ExecuteMoves([moveF, moveU, moveFP])
    if (locStr == "082230"):
        if (cube[0][8] == 'Y'):
            ExecuteMoves([moveR, moveU2, moveRP, moveUP, moveR, moveU, moveRP])
        elif (cube[2][2] == 'Y'):
            ExecuteMoves([moveU, moveR, moveUP, moveRP])
        else:
            ExecuteMoves([moveR, moveU, moveRP])

    cornerMoves = cornerMoves + movesDone
    return

# Checks if corner is solved.
def IsCornerSolved(colors, locStr):
    global cube
    if ((colors == "YOG") and (locStr == "501826") and (cube[5][0] == "Y")):
        return True
    elif ((colors == "YGR") and (locStr == "522836") and (cube[5][2] == "Y")):
        return True
    elif ((colors == "YRB") and (locStr == "583846") and (cube[5][8] == "Y")):
        return True
    elif ((colors == "YBO") and (locStr == "561648") and (cube[5][6] == "Y")):
        return True
    else:
        return False

# Corners solves the remaining corners of the yellow face.
# First a corner piece of interest is located and a predetermined set of moves
# is applied to it to position it in the correct location.
# Prints moves used to solve this step and pushes them to global variable solveMoves.
def Corners():
    global cube, movesDone, solveMoves, cornerMoves

    ResetMovesDone()
    locStr = LocateCorner("YOG")
    if not IsCornerSolved("YOG", locStr):
        if (locStr[0] == "5"):
            KickCorner(locStr)
        locStr = LocateCorner("YOG")
        if (locStr == "001042"):
            moveUP()
            cornerMoves = cornerMoves + ["U\'"]
        elif (locStr == "023240"):
            moveU2()
            cornerMoves = cornerMoves + ["U2"]
        elif (locStr == "082230"):
            moveU()
            cornerMoves = cornerMoves + ["U"]
        locStr = LocateCorner("YOG")
        MoveCornerDown(locStr)
    print("Yellow-Orange-Green corner solved.")

    ResetMovesDone()
    locStr = LocateCorner("YGR")
    if not IsCornerSolved("YGR", locStr):
        if (locStr[0] == "5"):
            KickCorner(locStr)
        locStr = LocateCorner("YGR")
        if (locStr == "061220"):
            moveUP()
            cornerMoves = cornerMoves + ["U\'"]
        elif (locStr == "001042"):
            moveU2()
            cornerMoves = cornerMoves + ["U2"]
        elif (locStr == "023240"):
            moveU()
            cornerMoves = cornerMoves + ["U"]
        locStr = LocateCorner("YGR")
        MoveCornerDown(locStr)
    print("Yellow-Green-Red corner solved.")

    ResetMovesDone()
    locStr = LocateCorner("YRB")
    if not IsCornerSolved("YRB", locStr):
        if (locStr[0] == "5"):
            KickCorner(locStr)
        locStr = LocateCorner("YRB")
        if (locStr == "082230"):
            moveUP()
            cornerMoves = cornerMoves + ["U\'"]
        elif (locStr == "061220"):
            moveU2()
            cornerMoves = cornerMoves + ["U2"]
        elif (locStr == "001042"):
            moveU()
            cornerMoves = cornerMoves + ["U"]
        locStr = LocateCorner("YRB")
        MoveCornerDown(locStr)
    print("Yellow-Red-Blue corner solved.")

    ResetMovesDone()
    locStr = LocateCorner("YBO")
    if not IsCornerSolved("YBO", locStr):
        if (locStr[0] == "5"):
            KickCorner(locStr)
        locStr = LocateCorner("YBO")
        if (locStr == "023240"):
            moveUP()
            cornerMoves = cornerMoves + ["U\'"]
        elif (locStr == "082230"):
            moveU2()
            cornerMoves = cornerMoves + ["U2"]
        elif (locStr == "061220"):
            moveU()
            cornerMoves = cornerMoves + ["U"]
        locStr = LocateCorner("YBO")
        MoveCornerDown(locStr)
    print("Yellow-Blue-Orange corner solved.")

    #print("Corners solution found: ", end='')
    #for i in range(len(cornerMoves)):
    #    print(cornerMoves[i], end='')
    #    if (i != (len(cornerMoves) - 1)):
    #        print(' ', end='')
    #print('')

    solveMoves = crossMoves + cornerMoves

    return

# Checks to see how many edges are solved in the second layer.
# Returns number of second layer pieces solved.
def NumSecondLayer():
    global cube
    cnt = 0
    if ((cube[1][3] == 'O') and (cube[4][5] == 'B')):
        cnt += 1
    if ((cube[1][5] == 'O') and (cube[2][3] == 'G')):
        cnt += 1
    if ((cube[2][5] == 'G') and (cube[3][3] == 'R')):
        cnt += 1
    if ((cube[3][5] == 'R') and (cube[4][3] == 'B')):
        cnt += 1
    return cnt

# Will return color of open second-layer edge.
# Returns as a string: ie. "0141" == cube[0][1] cube[4][1]
# If no edges are able to be moved, returns 0.
def LocateSecondEdge():
    global cube
    if not ((cube[0][1] == 'W') or (cube[4][1] == 'W')):
        #print("Second Layer: Eligible edge located at [0][1], [4][1].")
        return "0141"
    if not ((cube[0][3] == 'W') or (cube[1][1] == 'W')):
        #print("Second Layer: Eligible edge located at [0][3], [1][1].")
        return "0311"
    if not ((cube[0][5] == 'W') or (cube[3][1] == 'W')):
        #print("Second Layer: Eligible edge located at [0][5], [3][1].")
        return "0531"
    if not ((cube[0][7] == 'W') or (cube[2][1] == 'W')):
        #print("Second Layer: Eligible edge located at [0][7], [2][1].")
        return "0721"
    return 0

# Will return the location of an unsolved edge in the same format
#   as the function above.
def LocateUnsolvedEdge():
    global cube
    if not ((cube[1][3] == 'O') and (cube[4][5] == 'B')):
        #print("Second Layer: Out-of-position edge located at [1][3], [4][5].")
        return "1345"
    if not ((cube[1][5] == 'O') and (cube[2][3] == 'G')):
        #print("Second Layer: Out-of-position edge located at [1][5], [2][3].")
        return "1523"
    if not ((cube[2][5] == 'G') and (cube[3][3] == 'R')):
        #print("Second Layer: Out-of-position edge located at [2][5], [3][3].")
        return "2533"
    if not ((cube[3][5] == 'R') and (cube[4][3] == 'B')):
        #print("Second Layer: Out-of-position edge located at [3][5], [4][3].")
        return "3543"
    return 0

def SecondLayerRight(color):
    if (color == 'O'):
        ExecuteMoves([moveU, moveF, moveUP, moveFP, moveUP, moveLP, moveU, moveL])
    elif (color == 'G'):
        ExecuteMoves([moveU, moveR, moveUP, moveRP, moveUP, moveFP, moveU, moveF])
    elif (color == 'R'):
        ExecuteMoves([moveU, moveB, moveUP, moveBP, moveUP, moveRP, moveU, moveR])
    elif (color == 'B'):
        ExecuteMoves([moveU, moveL, moveUP, moveLP, moveUP, moveBP, moveU, moveB])
    else:
        return 0

def SecondLayerLeft(color):
    if (color == 'O'):
        ExecuteMoves([moveUP, moveBP, moveU, moveB, moveU, moveL, moveUP, moveLP])
    elif (color == 'G'):
        ExecuteMoves([moveUP, moveLP, moveU, moveL, moveU, moveF, moveUP, moveFP])
    elif (color == 'R'):
        ExecuteMoves([moveUP, moveFP, moveU, moveF, moveU, moveR, moveUP, moveRP])
    elif (color == 'B'):
        ExecuteMoves([moveUP, moveRP, moveU, moveR, moveU, moveB, moveUP, moveBP])
    else:
        return 0

# Checks if any eligible edges are open in the top layer
# # Marks the edge that is to be solved and move it into position
# # Applies move to left or move to right
# If no eligible edges, swaps a top edge with an edge on the side
# Makes sure the edge on the side is not already solved
def SecondLayer():
    global cube, movesDone, solveMoves, secondLayerMoves
    sideColors = ""
    ResetMovesDone()

    while (NumSecondLayer() < 4):
        ResetMovesDone()
        if not (LocateSecondEdge() == 0):
            if (LocateSecondEdge() == "0141"):
                sideColors = cube[0][1] + cube[4][1]
                if (sideColors[1] == 'O'):
                    moveUP()
                    if (sideColors[0] == 'G'):
                        SecondLayerRight('O')
                    else:
                        SecondLayerLeft('O')
                elif (sideColors[1] == 'R'):
                    moveU()
                    if (sideColors[0] == 'B'):
                        SecondLayerRight('R')
                    else:
                        SecondLayerLeft('R')
                elif (sideColors[1] == 'G'):
                    moveU2()
                    if (sideColors[0] == 'R'):
                        SecondLayerRight('G')
                    else:
                        SecondLayerLeft('G')
                else:
                    if (sideColors[0] == 'O'):
                        SecondLayerRight('B')
                    else:
                        SecondLayerLeft('B')
            elif (LocateSecondEdge() == "0311"):
                sideColors = cube[0][3] + cube[1][1]
                if (sideColors[1] == 'G'):
                    moveUP()
                    if (sideColors[0] == 'R'):
                        SecondLayerRight('G')
                    else:
                        SecondLayerLeft('G')
                elif (sideColors[1] == 'B'):
                    moveU()
                    if (sideColors[0] == 'O'):
                        SecondLayerRight('B')
                    else:
                        SecondLayerLeft('B')
                elif (sideColors[1] == 'R'):
                    moveU2()
                    if (sideColors[0] == 'B'):
                        SecondLayerRight('R')
                    else:
                        SecondLayerLeft('R')
                else:
                    if (sideColors[0] == 'G'):
                        SecondLayerRight('O')
                    else:
                        SecondLayerLeft('O')
            elif (LocateSecondEdge() == "0531"):
                sideColors = cube[0][5] + cube[3][1]
                if (sideColors[1] == 'B'):
                    moveUP()
                    if (sideColors[0] == 'O'):
                        SecondLayerRight('B')
                    else:
                        SecondLayerLeft('B')
                elif (sideColors[1] == 'G'):
                    moveU()
                    if (sideColors[0] == 'R'):
                        SecondLayerRight('G')
                    else:
                        SecondLayerLeft('G')
                elif (sideColors[1] == 'O'):
                    moveU2()
                    if (sideColors[0] == 'G'):
                        SecondLayerRight('O')
                    else:
                        SecondLayerLeft('O')
                else:
                    if (sideColors[0] == 'B'):
                        SecondLayerRight('R')
                    else:
                        SecondLayerLeft('R')
            elif (LocateSecondEdge() == "0721"):
                sideColors = cube[0][7] + cube[2][1]
                if (sideColors[1] == 'R'):
                    moveUP()
                    if (sideColors[0] == 'B'):
                        SecondLayerRight('R')
                    else:
                        SecondLayerLeft('R')
                elif (sideColors[1] == 'O'):
                    moveU()
                    if (sideColors[0] == 'G'):
                        SecondLayerRight('O')
                    else:
                        SecondLayerLeft('O')
                elif (sideColors[1] == 'B'):
                    moveU2()
                    if (sideColors[0] == 'O'):
                        SecondLayerRight('B')
                    else:
                        SecondLayerLeft('B')
                else:
                    if (sideColors[0] == 'R'):
                        SecondLayerRight('G')
                    else:
                        SecondLayerLeft('G')
            else:
                return 0
        else:
            # If no eligible edges, swap a top edge with an edge on the side
            # Make sure the edge on the side is not already solved
            if (LocateUnsolvedEdge() == "1345"):
                SecondLayerRight('B')
            elif (LocateUnsolvedEdge() == "1523"):
                SecondLayerRight('O')
            elif (LocateUnsolvedEdge() == "2533"):
                SecondLayerRight('G')
            elif (LocateUnsolvedEdge() == "3543"):
                SecondLayerRight('R')
            else:
                return 0

        #print("Partial solution found: ", end='')
        #for j in range(len(movesDone)):
        #    print(movesDone[j], end=' ')
        #print('')
        #CubePrint(cube)

        secondLayerMoves = secondLayerMoves + movesDone

    print("Second layer solution found.")
    #print("Second layer solution found: ", end='')
    #for j in range(len(secondLayerMoves)):
    #    print(secondLayerMoves[j], end=' ')
    #print('')
    solveMoves = solveMoves + secondLayerMoves

def IsCubeSolved():
    global cube
    if (cube == [['W', 'W', 'W',
              'W', 'W', 'W',
              'W', 'W', 'W'],
             ['O', 'O', 'O',
              'O', 'O', 'O',
              'O', 'O', 'O'],
             ['G', 'G', 'G',
              'G', 'G', 'G',
              'G', 'G', 'G'],
             ['R', 'R', 'R',
              'R', 'R', 'R',
              'R', 'R', 'R'],
             ['B', 'B', 'B',
              'B', 'B', 'B',
              'B', 'B', 'B'],
             ['Y', 'Y', 'Y',
              'Y', 'Y', 'Y',
              'Y', 'Y', 'Y']]):
        return True
    elif (cube == [['W', 'W', 'W',
              'W', 'W', 'W',
              'W', 'W', 'W'],
             ['G', 'G', 'G',
              'O', 'O', 'O',
              'O', 'O', 'O'],
             ['R', 'R', 'R',
              'G', 'G', 'G',
              'G', 'G', 'G'],
             ['B', 'B', 'B',
              'R', 'R', 'R',
              'R', 'R', 'R'],
             ['O', 'O', 'O',
              'B', 'B', 'B',
              'B', 'B', 'B'],
             ['Y', 'Y', 'Y',
              'Y', 'Y', 'Y',
              'Y', 'Y', 'Y']]):
        return True
    elif (cube == [['W', 'W', 'W',
              'W', 'W', 'W',
              'W', 'W', 'W'],
             ['R', 'R', 'R',
              'O', 'O', 'O',
              'O', 'O', 'O'],
             ['B', 'B', 'B',
              'G', 'G', 'G',
              'G', 'G', 'G'],
             ['O', 'O', 'O',
              'R', 'R', 'R',
              'R', 'R', 'R'],
             ['G', 'G', 'G',
              'B', 'B', 'B',
              'B', 'B', 'B'],
             ['Y', 'Y', 'Y',
              'Y', 'Y', 'Y',
              'Y', 'Y', 'Y']]):
        return True
    elif (cube == [['W', 'W', 'W',
              'W', 'W', 'W',
              'W', 'W', 'W'],
             ['B', 'B', 'B',
              'O', 'O', 'O',
              'O', 'O', 'O'],
             ['O', 'O', 'O',
              'G', 'G', 'G',
              'G', 'G', 'G'],
             ['G', 'G', 'G',
              'R', 'R', 'R',
              'R', 'R', 'R'],
             ['R', 'R', 'R',
              'B', 'B', 'B',
              'B', 'B', 'B'],
             ['Y', 'Y', 'Y',
              'Y', 'Y', 'Y',
              'Y', 'Y', 'Y']]):
        return True
    else:
        return False

def LLCrossCheck():
    global cube
    if ((cube[0][1] == 'W') and (cube[0][3] == 'W') and (cube[0][5] == 'W') and cube[0][7] == 'W'):
        return True
    else:
        return False

def LLCross():
    global cube, movesDone, solveMoves
    ResetMovesDone()

    if (LLCrossCheck()):
        pass
    elif ((cube[0][3] == 'W') and (cube[0][5] == 'W')):
        ExecuteMoves([moveF, moveR, moveU, moveRP, moveUP, moveFP])
    elif ((cube[0][1] == 'W') and (cube[0][7] == 'W')):
        moveU()
        ExecuteMoves([moveF, moveR, moveU, moveRP, moveUP, moveFP])
    elif ((cube[0][1] == 'W') and (cube[0][3] == 'W')):
        ExecuteMoves([moveF, moveR, moveU, moveRP, moveUP, moveR, moveU, moveRP, moveUP, moveFP])
    elif ((cube[0][3] == 'W') and (cube[0][7] == 'W')):
        moveU()
        ExecuteMoves([moveF, moveR, moveU, moveRP, moveUP, moveR, moveU, moveRP, moveUP, moveFP])
    elif ((cube[0][7] == 'W') and (cube[0][5] == 'W')):
        moveU2()
        ExecuteMoves([moveF, moveR, moveU, moveRP, moveUP, moveR, moveU, moveRP, moveUP, moveFP])
    elif ((cube[0][1] == 'W') and (cube[0][5] == 'W')):
        moveUP()
        ExecuteMoves([moveF, moveR, moveU, moveRP, moveUP, moveR, moveU, moveRP, moveUP, moveFP])
    elif not ((cube[0][1] == 'W') or (cube[0][3] == 'W') or (cube[0][5] == 'W') or cube[0][7] == 'W'):
        ExecuteMoves([moveF, moveR, moveU, moveRP, moveUP, moveFP, moveB, moveL, moveU,
                      moveLP, moveUP, moveL, moveU, moveLP, moveUP, moveBP])

    print("Last layer simplified.")
    #print("Last layer cross solution found: ", end='')
    #for j in range(len(movesDone)):
    #  print(movesDone[j], end=' ')
    #print('')
    solveMoves = solveMoves + movesDone
    return

def OLLCheck():
    global cube
    for i in range(9):
        if not (cube[0][i] == 'W'):
            return False
    else:
        return True

def CrossOLL():
    global cube, movesDone, solveMoves

    ResetMovesDone()
    while not (OLLCheck()):
        if ((cube[4][2] == 'W') and (cube[4][0] == 'W') and (cube[2][0] == 'W') and (cube[2][2] == 'W')):
            ExecuteMoves([moveR, moveU2, moveRP, moveUP, moveR, moveU, moveRP, moveUP, moveR, moveUP, moveRP])
            print("OLL Case 1 found.")
        elif ((cube[1][0] == 'W') and (cube[1][2] == 'W') and (cube[2][2] == 'W') and (cube[4][0] == 'W')):
            ExecuteMoves([moveR, moveU2, moveR2, moveUP, moveR2, moveUP, moveR2, moveU2, moveR])
            print("OLL Case 2 found.")
        elif ((cube[4][2] == 'W') and (cube[4][0] == 'W') and (cube[0][6] == 'W') and (cube[0][8] == 'W')):
            ExecuteMoves([moveU, moveR, moveU, moveRP, moveU, moveR, moveU2, moveRP])
            print("OLL Case 3 found. OLL will re-execute.")
        elif ((cube[4][2] == 'W') and (cube[2][0] == 'W') and (cube[0][2] == 'W') and (cube[0][8] == 'W')):
            ExecuteMoves([moveL, moveF, moveRP, moveFP, moveLP, moveF, moveR, moveFP])
            print("OLL Case 4 found.")
        elif ((cube[0][2] == 'W') and (cube[0][6] == 'W') and (cube[1][0] == 'W') and (cube[2][2] == 'W')):
            ExecuteMoves([moveFP, moveL, moveF, moveRP, moveFP, moveLP, moveF, moveR])
            print("OLL Case 5 found.")
        elif ((cube[1][0] == 'W') and (cube[0][2] == 'W') and (cube[2][0] == 'W') and (cube[3][0] == 'W')):
            ExecuteMoves([moveR, moveU2, moveRP, moveUP, moveR, moveUP, moveRP])
            print("OLL Case 6 found.")
        elif ((cube[4][2] == 'W') and (cube[3][2] == 'W') and (cube[2][2] == 'W') and (cube[0][6] == 'W')):
            ExecuteMoves([moveR, moveU, moveRP, moveU, moveR, moveU2, moveRP])
            print("OLL Case 7 found.")
        else:
            moveU()

    #print("Orientation of last layer found: ", end='')
    #for j in range(len(movesDone)):
    #  print(movesDone[j], end=' ')
    #print('')
    solveMoves = solveMoves + movesDone
    return


def LLOffset(i):
    for j in range(i):
        moveU()
    return

def PermLL():
    global cube, movesDone, solveMoves

    cubeCopy = cp.deepcopy(cube)
    ResetMovesDone()

    for i in range(4):
        #print("Executing PLL Loop", end=' ')
        #print(i + 1, end='')
        #print(".")

        #0
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        if (IsCubeSolved()):
            print("PLL Case 0 found.")
            break

        #1
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR, moveUP, moveR, moveU, moveR, moveU, moveR, moveUP, moveRP, moveUP, moveR2])
        if (IsCubeSolved()):
            print("PLL Case 1 found.")
            break

        #2
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR2, moveU, moveR, moveU, moveRP, moveUP, moveRP, moveUP, moveRP, moveU, moveRP])
        if (IsCubeSolved()):
            print("PLL Case 2 found.")
            break
        
        #3
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR, moveUP, moveR, moveU, moveR, moveU, moveR, moveUP, moveRP, moveUP, moveR2, moveB, moveUP, moveB, moveU, moveB, moveU, moveB, moveUP, moveBP, moveUP, moveB2])
        if (IsCubeSolved()):
            print("PLL Case 3 found.")
            break

        #4
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR2, moveU, moveR, moveU, moveRP, moveUP, moveRP, moveUP, moveRP, moveU, moveRP, moveB2, moveU, moveB, moveU, moveBP, moveUP, moveBP, moveUP, moveBP, moveU, moveBP])
        if (IsCubeSolved()):
            print("PLL Case 4 found.")
            break

        #5
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR2, moveF2, moveRP, moveBP, moveR, moveF2, moveRP, moveB, moveRP])
        if (IsCubeSolved()):
            print("PLL Case 5 found.")
            break

        #6
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR, moveBP, moveR, moveF2, moveRP, moveB, moveR, moveF2, moveR2])
        if (IsCubeSolved()):
            print("PLL Case 6 found.")
            break

        #7
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR, moveBP, moveRP, moveF, moveR, moveB, moveRP, moveFP, moveR, moveB, moveRP, moveF, moveR, moveBP, moveRP, moveFP])
        if (IsCubeSolved()):
            print("PLL Case 7 found.")
            break

        #8
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR, moveU, moveRP, moveUP, moveRP, moveF, moveR2, moveUP, moveRP, moveUP, moveR, moveU, moveRP, moveFP])
        if (IsCubeSolved()):
            print("PLL Case 8 found.")
            break

        #9
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveRP, moveUP, moveFP, moveR, moveU, moveRP, moveUP, moveRP, moveF, moveR2, moveUP, moveRP, moveUP, moveR, moveU, moveRP, moveU, moveR])
        if (IsCubeSolved()):
            print("PLL Case 9 found.")
            break

        #10
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveRP, moveU, moveRP, moveUP, moveBP, moveRP, moveB2, moveUP, moveBP, moveU, moveBP, moveR, moveB, moveR])
        if (IsCubeSolved()):
            print("PLL Case 10 found.")
            break

        #11
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveF, moveR, moveUP, moveRP, moveUP, moveR, moveU, moveRP, moveFP, moveR, moveU, moveRP, moveUP, moveRP, moveF, moveR, moveFP])
        if (IsCubeSolved()):
            print("PLL Case 11 found.")
            break

        #12
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveFP, moveU, moveBP, moveU2, moveF, moveUP, moveFP, moveU2, moveF, moveB, moveUP])
        if (IsCubeSolved()):
            print("PLL Case 12 found.")
            break

        #13
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR, moveU, moveRP, moveFP, moveR, moveU, moveRP, moveUP, moveRP, moveF, moveR2, moveUP, moveRP, moveUP])
        if (IsCubeSolved()):
            print("PLL Case 13 found.")
            break

        #14
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveRP, moveU2, moveR, moveU2, moveRP, moveF, moveR, moveU, moveRP, moveUP, moveRP, moveFP, moveR2, moveUP])
        if (IsCubeSolved()):
            print("PLL Case 14 found.")
            break

        #15
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR, moveU, moveRP, moveFP, moveR, moveU2, moveRP, moveU2, moveRP, moveF, moveR, moveU, moveR, moveU2, moveRP, moveUP])
        if (IsCubeSolved()):
            print("PLL Case 15 found.")
            break

        #16
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR2, moveU, moveR, moveU, moveRP, moveUP, moveRP, moveUP, moveRP, moveU, moveRP, moveUP, moveR, moveBP, moveR, moveF2, moveRP, moveB, moveR, moveF2, moveR2, moveU])
        if (IsCubeSolved()):
            print("PLL Case 16 found.")
            break

        #17
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveUP, moveR, moveUP, moveR, moveU, moveR, moveU, moveR, moveUP, moveRP, moveUP, moveR2, moveUP, moveR2, moveF2, moveRP, moveBP, moveR, moveF2, moveRP, moveB, moveRP, moveU2])
        if (IsCubeSolved()):
            print("PLL Case 17 found.")
            break

        #18
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveU2, moveR, moveUP, moveR, moveU, moveR, moveU, moveR, moveUP, moveRP, moveUP, moveR2, moveR2, moveF2, moveRP, moveBP, moveR, moveF2, moveRP, moveB, moveRP, moveU2])
        if (IsCubeSolved()):
            print("PLL Case 18 found.")
            break

        #19
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveUP, moveR2, moveU, moveR, moveU, moveRP, moveUP, moveRP, moveUP, moveRP, moveU, moveRP, moveR, moveBP, moveR, moveF2, moveRP, moveB, moveR, moveF2, moveR2, moveU])
        if (IsCubeSolved()):
            print("PLL Case 19 found.")
            break

        #20
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveRP, moveU, moveR, moveUP, moveRP, moveFP, moveUP, moveF, moveR, moveU, moveRP, moveF, moveRP, moveFP, moveR, moveUP, moveR])
        if (IsCubeSolved()):
            print("PLL Case 20 found.")
            break

        #21
        cube = cp.deepcopy(cubeCopy)
        ResetMovesDone()
        LLOffset(i)
        ExecuteMoves([moveR, moveU, moveRP, moveU, moveR, moveU, moveRP, moveFP, moveR, moveU, moveRP, moveUP, moveRP, moveF, moveR2, moveUP, moveRP, moveU2, moveR, moveUP, moveRP])
        if (IsCubeSolved()):
            print("PLL Case 21 found.")
            break
        else:
            cube = cp.deepcopy(cubeCopy)

    if (IsCubeSolved()):
        #print("Solution found.")
        #print("Permutation of last layer found: ", end='')
        #for j in range(len(movesDone)):
        #    print(movesDone[j], end=' ')
        #print('')
        solveMoves = solveMoves + movesDone
    else:
        print("ERROR: No solution found.")
        CubePrint(cube)
    return

def CubeMustSolve():
    if (cube == [['W', 'W', 'W',
                'W', 'W', 'W',
                'W', 'W', 'W'],
                ['O', 'O', 'O',
                'O', 'O', 'O',
                'O', 'O', 'O'],
                ['G', 'G', 'G',
                'G', 'G', 'G',
                'G', 'G', 'G'],
                ['R', 'R', 'R',
                'R', 'R', 'R',
                'R', 'R', 'R'],
                ['B', 'B', 'B',
                'B', 'B', 'B',
                'B', 'B', 'B'],
                ['Y', 'Y', 'Y',
                'Y', 'Y', 'Y',
                'Y', 'Y', 'Y']]):
        return True
    else:
        return False

def FinalUMove():
    global cube, movesDone, solveMoves
    ResetMovesDone()

    cnt = 0

    while not (CubeMustSolve()):
        moveU()
        cnt = cnt + 1
        if (cnt > 3):
            break
    
    solveMoves = solveMoves + movesDone
    return
    
#################################################
#                                               #
#          COMPUTER VISION FUNCTIONS            #
#                                               #
#################################################

## COORDINATES
x0 = 493
y0 = 694
x1 = 788
y1 = 692
x2 = 1085
y2 = 677
x3 = 498
y3 = 981
x5 = 1093
y5 = 969
x6 = 501
y6 = 1278
x7 = 776
y7 = 1266
x8 = 1085
y8 = 1273

## CONSTANTS
delayLargeVal = 3.5 #seconds
delayVal = 1.5 #seconds

def SendSerial(payLoad):
    payLoad = textwrap.wrap(payLoad, 5)

    if __name__ == '__main__':
        print("Opening Serial Port...")
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        time.sleep(2)
        
        for i in range(len(payLoad)):
            ser.write(payLoad[i].encode('ASCII'))
            time.sleep(0.05)
        line = ser.readline().decode('ASCII').rstrip()
        print(line)
    

def getColor(R,G,B):
    print("RGB:",R,G,B)
    if ((math.dist([R],[G]) <= 45) and (math.dist([B],[G]) <= 45) and (math.dist([R],[B]) <= 45) and (R > 130) and (B > 130) and (G > 130)):
        return 'W'
    elif ((G >= R + 30) and (G >= B + 30)):
        return 'G'
    elif ((R < 50) and (B > G + 20)):
        return 'B'
    elif ((math.dist([R],[G]) <= 43) and (G >= B + 80)):
        return 'Y'
    elif ((R > G) and (R > B) and (((G <= 80) and (B <= 80) and (R <= 183)) or (G < B))):
        return 'R'
    elif ((R > G) and (R > B) and (math.dist([B],[G]) >= 15)):
        return 'O'
    else:
        return 'X'

def ReadFace(picam2):
    global x0, y0, x1, y1, x2, y2, x3, y3, x5, y5, x6, y6, x7, y7

    picam2.capture_file("cube.jpg")
    im = cv2.imread('cube.jpg')

    b,g,r = im[y0,x0]
    face0 = getColor(r,g,b)
    b,g,r = im[y1,x1]
    face1 = getColor(r,g,b)
    b,g,r = im[y2,x2]
    face2 = getColor(r,g,b)
    b,g,r = im[y3,x3]
    face3 = getColor(r,g,b)
    b,g,r = im[y5,x5]
    face5 = getColor(r,g,b)
    b,g,r = im[y6,x6]
    face6 = getColor(r,g,b)
    b,g,r = im[y7,x7]
    face7 = getColor(r,g,b)
    b,g,r = im[y8,x8]
    face8 = getColor(r,g,b)
    
    face4 = 'X'

    return [face0, face1, face2, face3, face4, face5, face6, face7, face8]

def MapCube():
    ## CUBE
    cube = [['?','?','?',
            '?','W','?',
            '?','?','?'],
            ['?','?','?',
            '?','O','?',
            '?','?','?'],
            ['?','?','?',
            '?','G','?',
            '?','?','?'],
            ['?','?','?',
            '?','R','?',
            '?','?','?'],
            ['?','?','?',
            '?','B','?',
            '?','?','?'],
            ['?','?','?',
            '?','Y','?',
            '?','?','?']]
            
    ## INIT CAMERA
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1920)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start()

    currFace = ReadFace(picam2)
    cube[5][0] = currFace[0]
    cube[5][1] = currFace[1]
    cube[5][2] = currFace[2]
    cube[5][3] = currFace[3]
    cube[5][5] = currFace[5]
    cube[5][6] = currFace[6]
    cube[5][7] = currFace[7]
    cube[5][8] = currFace[8]
    print(currFace)
    CubePrint(cube)

    # F, BP
    SendSerial("F1,BP")
    time.sleep(delayVal)

    currFace = ReadFace(picam2)
    cube[3][6] = currFace[0]
    cube[3][3] = currFace[1]
    cube[3][0] = currFace[2]
    cube[3][8] = currFace[6]
    cube[3][5] = currFace[7]
    cube[3][2] = currFace[8]
    print(currFace)
    CubePrint(cube)

    # F, BP
    SendSerial("F1,BP")
    time.sleep(delayVal)

    currFace = ReadFace(picam2)
    cube[0][8] = currFace[0]
    cube[0][7] = currFace[1]
    cube[0][6] = currFace[2]
    cube[0][2] = currFace[6]
    cube[0][1] = currFace[7]
    cube[0][0] = currFace[8]
    print(currFace)
    CubePrint(cube)

    # F, BP
    SendSerial("F1,BP,U1,UP")
    time.sleep(delayVal)

    currFace = ReadFace(picam2)
    cube[1][2] = currFace[0]
    cube[1][5] = currFace[1]
    cube[1][8] = currFace[2]
    cube[1][0] = currFace[6]
    cube[1][3] = currFace[7]
    cube[1][6] = currFace[8]
    print(currFace)
    CubePrint(cube)

    # F, BP, LP, R
    SendSerial("F1,BP,LP,R1,U1,UP")
    time.sleep(delayVal)

    currFace = ReadFace(picam2)
    cube[4][8] = currFace[0]
    cube[4][6] = currFace[2]
    cube[4][5] = currFace[3]
    cube[4][3] = currFace[5]
    cube[4][2] = currFace[6]
    cube[4][0] = currFace[8]
    print(currFace)
    CubePrint(cube)

    # LP, R
    SendSerial("LP,R1")
    time.sleep(delayVal)

    currFace = ReadFace(picam2)
    cube[0][3] = currFace[3]
    cube[0][5] = currFace[5]
    print(currFace)
    CubePrint(cube)

    # LP, R
    SendSerial("LP,R1,U1,UP")
    time.sleep(delayVal)

    currFace = ReadFace(picam2)
    cube[2][0] = currFace[0]
    cube[2][2] = currFace[2]
    cube[2][3] = currFace[3]
    cube[2][5] = currFace[5]
    cube[2][6] = currFace[6]
    cube[2][8] = currFace[8]
    print(currFace)
    CubePrint(cube)

    # R2, F, B
    SendSerial("R2,F1,B1,U1,UP")
    time.sleep(delayVal)
    
    currFace = ReadFace(picam2)
    cube[1][7] = currFace[7]
    cube[3][7] = currFace[1]
    print(currFace)
    CubePrint(cube)

    # BP, FP, RP, LP, FP, BP, LP, RP
    SendSerial("BP,FP,RP,LP,FP,BP,LP,RP,U1,UP")
    time.sleep(delayLargeVal)
   
    currFace = ReadFace(picam2)
    cube[2][7] = currFace[5]
    cube[4][7] = currFace[3]
    print(currFace)
    CubePrint(cube)

    # R, L, B, F, F2, B2, FP, BP, LP, RP
    SendSerial("R1,L1,B2,F2,LP,RP,U1,UP")
    time.sleep(delayLargeVal)
    
    currFace = ReadFace(picam2)
    cube[2][1] = currFace[5]
    cube[4][1] = currFace[3]
    print(currFace)
    CubePrint(cube)

    # R, L, B, F, L2, R2, L, R, F, B
    SendSerial("R1,L1,B1,F1,LP,RP,F1,B1,U1,UP")
    time.sleep(delayLargeVal)
    
    currFace = ReadFace(picam2)
    cube[1][1] = currFace[7]
    cube[3][1] = currFace[1]
    print(currFace)
    CubePrint(cube)

    # BP, FP, RP, LP, R2, L2, B2, F2
    SendSerial("BP,FP,R1,L1,B2,F2,U1,UP")
    time.sleep(delayLargeVal)

    CubePrint(cube)

    return cube

#################################################
#                                               #
#      GLOBAL VARIABLES AND MAIN FUNCTION       #
#                                               #
#################################################

movesDone = []
solveMoves = []
crossMoves = []
cornerMoves = []
secondLayerMoves = []

moveSetAll = [moveF, moveR, moveB, moveL, moveU,
                moveFP, moveRP, moveBP, moveLP, moveUP,
                moveF2, moveR2, moveB2, moveL2, moveU2]
moveSetF = [moveR, moveB, moveL, moveU,
             moveRP, moveBP, moveLP, moveUP,
             moveR2, moveB2, moveL2, moveU2]
moveSetR = [moveF, moveB, moveL, moveU,
             moveFP, moveBP, moveLP, moveUP,
             moveF2, moveB2, moveL2, moveU2]
moveSetB = [moveR, moveF, moveL, moveU,
             moveRP, moveFP, moveLP, moveUP,
             moveR2, moveF2, moveL2, moveU2]
moveSetL = [moveR, moveB, moveF, moveU,
             moveRP, moveBP, moveFP, moveUP,
             moveR2, moveB2, moveF2, moveU2]
moveSetU = [moveR, moveB, moveL, moveF,
             moveRP, moveBP, moveLP, moveFP,
             moveR2, moveB2, moveL2, moveF2]

cube = MapCube()

input("Press ENTER to continue.")
start_time = time.time()

Cross()
Corners()
SecondLayer()
LLCross()
CrossOLL()
PermLL()
FinalUMove()
print("Cube solved:")
CubePrint(cube)

print("\nFull solution: ", end='')
for i in range(len(solveMoves)):
    print(solveMoves[i], end='')
    if (i != (len(solveMoves) - 1)):
        print(' ', end='')
print('')

numMoves = len(solveMoves)
for i in range(numMoves):
    if (len(solveMoves[i]) == 1):
        solveMoves[i] = solveMoves[i] + '1'
        
print("\nSolve Time: %s seconds\n" % (time.time() - start_time))

serialPayload = ""
serialPayloadB = ""
for i in range(len(solveMoves)):
    serialPayload = serialPayload + solveMoves[i] + ","
serialPayload = serialPayload + '\n'
for i in range(len(serialPayload)):
    if serialPayload[i] == '\'':
        serialPayloadB = serialPayloadB + 'P'
    elif (i < (len(serialPayload) - 2)):
        serialPayloadB = serialPayloadB + serialPayload[i]
    else:
        pass

serialPayloadB = textwrap.wrap(serialPayloadB, 20)

if __name__ == '__main__':
    print("Opening Serial Port...")
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    time.sleep(2)
    
    for i in range(len(serialPayloadB)):
        ser.write(serialPayloadB[i].encode('ASCII'))
        time.sleep(0.05)
    line = ser.readline().decode('ASCII').rstrip()
    print(line)

print("\nTotal runtime: %s seconds" % (time.time() - start_time))
print("...with a %s-move solution" % (numMoves))
