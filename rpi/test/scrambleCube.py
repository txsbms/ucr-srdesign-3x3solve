import random as rd
import serial
import time
import textwrap

# Scramble Functions

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
    moveSetScr = [moveF, moveR, moveU, moveB, moveL,
               moveFP, moveRP, moveUP, moveBP, moveLP,
               moveF2, moveR2, moveU2, moveB2, moveL2,]
    moveSetScrF = [moveR, moveU, moveL, moveB,
                 moveRP, moveUP, moveLP, moveBP,
                 moveR2, moveU2, moveL2, moveB2]
    moveSetScrR = [moveF, moveU, moveL, moveB,
                 moveFP, moveUP, moveLP, moveBP,
                 moveF2, moveU2, moveL2, moveB2]
    moveSetScrU = [moveR, moveF, moveL, moveB,
                 moveRP, moveFP, moveLP, moveBP,
                 moveR2, moveF2, moveL2, moveB2]
    moveSetScrL = [moveR, moveU, moveF, moveB,
                 moveRP, moveUP, moveFP, moveBP,
                 moveR2, moveU2, moveF2, moveB2]
    moveSetScrD = [moveR, moveU, moveL, moveF, moveB,
                 moveRP, moveUP, moveLP, moveFP, moveBP,
                 moveR2, moveU2, moveL2, moveF2, moveB2]
    moveSetScrB = [moveR, moveU, moveL, moveF,
                 moveRP, moveUP, moveLP, moveFP,
                 moveR2, moveU2, moveL2, moveF2]

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

# Global Variables
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

# main
cube = [ ['W', 'W', 'W',
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
          'Y', 'Y', 'Y']]


ScrambleCube()
CubePrint(cube)

scrambleMoves = movesDone
solveMoves = scrambleMoves

numMoves = len(solveMoves)
for i in range(numMoves):
    if (len(solveMoves[i]) == 1):
        solveMoves[i] = solveMoves[i] + '1'

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
