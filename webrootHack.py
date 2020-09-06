# Webroot Hack 2018 submission Team Scott Zhao, Samarth Aggarwal
# Copyright 2018 Scott Zhao (https://github.com/zhaomh1998)
# Copyright 2018 Samarth Aggarwal (https://github.com/samarth1998)
# Runs on https://www.codingame.com/ engine
import sys
import math
import numpy as np
import random
import time

pos = np.zeros((10000,4,2))
grid = np.zeros((15, 30))
dangerGrid = np.zeros((15, 30))
roundCount = 0
futureGrid = np.zeros((15, 30))
lastDirection = 1
lastDirectionForMain = 1
deployCount = 3
dirr = 1
noDeployFlag = 0
# Don't run into a player's light trail! Use your helper bots at strategic moments or as a last resort to be the last drone standing!

player_count = int(input())  # the number of at the start of this game
my_id = int(input())  # your bot's id


def ct(direction, currentXPos, currentYPos):
    global grid
    if direction == 3:
        if (grid[int(currentXPos)%15][int(currentYPos - 1)%30]):
            print("DEPLOY")
        else:
            print("LEFT")
    elif direction == 4:
        if (grid[int(currentXPos)%15][int(currentYPos + 1)%30]):
            print("DEPLOY")
        else:
            print("RIGHT")
    elif direction == 1:
        if (grid[int(currentXPos - 1)%15][int(currentYPos)%30]):
            print("DEPLOY")
        else:
            print("UP")
    elif direction == 2:
        if (grid[int(currentXPos + 1)%15][int(currentYPos)%30]):
            print("DEPLOY")
        else:
            print("DOWN")
    elif direction == 0:
        print("DEPLOY")
def calculateDangerZones():
    global helper_bots, dangerGrid, player_count, pos, grid, roundCount
    for i in range(player_count):
        #print("MyID=", my_id, file=sys.stderr)
        if(my_id == i):
            continue;
        #print("Player", i, "Current position ", pos[roundCount][i], file = sys.stderr)
        playerX = int(pos[roundCount][i][0])
        playerY = int(pos[roundCount][i][1])
        dangerGrid[(playerX+1)%15][playerY%30] = 1
        dangerGrid[playerX-1][playerY%30] = 1
        dangerGrid[playerX%15][(playerY+1)%30] = 1
        dangerGrid[playerX%15][(playerY-1)%30] = 1
        #print(dangerGrid, file=sys.stderr)
def detect2(currX, currY):
    global helper_bots, dangerGrid, player_count, pos, grid, roundCount
    availableMoves = np.array([[1, 0], [2, 0], [3, 0], [4, 0]])
    for i in range(1,17):
        if(grid[int(currX - i)%15][int(currY)%30]): #Up
            availableMoves[0][1] = i - 1
            break;

    for i in range(1,17):
        if(grid[int(currX + i)%15][int(currY)%30]): #Down
            availableMoves[1][1] = i - 1 
            break;

    for i in range(1,32):
        if(grid[int(currX)%15][int(currY - i)%30]): #Left
            availableMoves[2][1] = i - 1
            break;
            
    for i in range(1,32):
        if(grid[int(currX)%15][int(currY + i)%30]): #Right
            availableMoves[3][1] = i - 1
            break;
    #print("Original avil array", availableMoves, file=sys.stderr)  #Original available array
    
    #If going this direction will result in entering a danger zone
    if(dangerGrid[int(currX - 1)%15][int(currY)%30] and not(availableMoves[0][1] == 0)):  #If 1 step up in in danger zone and we could go up
        availableMoves[0][1] = 1
        print("Replaced danger zone going up", file=sys.stderr)
    if(dangerGrid[int(currX + 1)%15][int(currY)%30] and not(availableMoves[1][1] == 0)):  #If 1 step down in in danger zone and we could go down
        availableMoves[1][1] = 1
        print("Replaced danger zone going down", file=sys.stderr)
    if(dangerGrid[int(currX)%15][int(currY - 1)%30] and not(availableMoves[2][1] == 0)):  #If 1 step left in in danger zone and we could go left
        availableMoves[2][1] = 1
        print("Replaced danger zone going left", file=sys.stderr)
    if(dangerGrid[int(currX)%15][int(currY + 1)%30] and not(availableMoves[3][1] == 0)):  #If 1 step right in in danger zone and we could go right
        availableMoves[3][1] = 1
        print("Replaced danger zone going right", file=sys.stderr)
    #print("Replaced avil array", availableMoves, file=sys.stderr)  #Original available array

    if(np.sum(availableMoves[:,1]) == 0): #No way to go
        return 0
    else:
        return availableMoves[availableMoves[:,1].argmax()][0]
def recordMove(player, x, y):
    global helper_bots, dangerGrid, player_count, pos, grid, roundCount
    pos[roundCount][i] = [y, x]
    grid[y, x] = 1
def updatePos(originalX, originalY, direc):
    global helper_bots, dangerGrid, player_count, pos, grid, roundCount, futureGrid, lastDirection, deployCount, noDeployFlag
    noDeployFlag = 0
    if(not(deployCount)):
        noDeployFlag = 1
        return 0, 0
    if(direc == 1):
        return int(originalX-1)%15, int(originalY)%30
    elif(direc == 2):
        return int(originalX+1)%15, int(originalY)%30
    elif(direc == 3):
        return int(originalX)%15, int(originalY-1)%30
    elif(direc == 4):
        return int(originalX)%15, int(originalY+1)%30
    elif(direc == 0):
        print("deployCount", deployCount, file=sys.stderr)
        if(deployCount):  #If still have deployments
            #print("Deploying, Lastdirection= ", lastDirection, file=sys.stderr)
            deployCount = deployCount - 1
            return updatePos(originalX, originalY, lastDirection)
        else:
            print("FLAGGED", file=sys.stderr)
            noDeployFlag = 1
            print("FLAG=", noDeployFlag, file=sys.stderr)
            return 0, 0
def calculateSurviveRounds(currX, currY, directionToGo):
    global helper_bots, dangerGrid, player_count, pos, grid, roundCount, futureGrid, lastDirection, deployCount, noDeployFlag
    deployCount = helper_bots           #Resetting deploy count
    print("Remaining deploys: ", deployCount, file=sys.stderr)
    futureGrid = np.array(grid)         #Resetting future grid to current grid
    futureDirr = 1    #Initialize
    nextX, nextY= updatePos(currX, currY, directionToGo)
    print("Flag =", noDeployFlag, file=sys.stderr)
    for i in range(50):
        if(noDeployFlag):
            print("Breaking with i", i, file=sys.stderr)
            break;
        futureGrid[nextX][nextY] = 1  #Update grid after a future move
        if(futureDirr):
            lastDirection = futureDirr
        futureDirr = detectNewGrid(nextX, nextY, futureGrid)
        #print("New Grid: ", nextX, nextY, "Direction=", futureDirr, file=sys.stderr)
        nextX, nextY = updatePos(nextX, nextY, futureDirr)
        #print("After update: ", nextX, nextY, file=sys.stderr)
    return i
def detectNewGrid(currX, currY, gridUsing):
    global helper_bots, dangerGrid, player_count, pos, grid, roundCount, futureGrid, lastDirection, deployCount
    availMoves = np.array([[1, 0], [2, 0], [3, 0], [4, 0]])
    for i in range(1,17):
        if(gridUsing[int(currX - i)%15][int(currY)%30]): #Up
            availMoves[0][1] = i - 1
            break;

    for i in range(1,17):
        if(gridUsing[int(currX + i)%15][int(currY)%30]): #Down
            availMoves[1][1] = i - 1 
            break;

    for i in range(1,32):
        if(gridUsing[int(currX)%15][int(currY - i)%30]): #Left
            availMoves[2][1] = i - 1
            break;
            
    for i in range(1,32):
        if(gridUsing[int(currX)%15][int(currY + i)%30]): #Right
            availMoves[3][1] = i - 1
            break;
    #print(availableMoves, file=sys.stderr)  #Original available array

    if(dangerGrid[int(currX - 1)%15][int(currY)%30] and not(availMoves[0][1] == 0)):  #If 1 step up in in danger zone and we could go up
        availMoves[0][1] = 1
    if(dangerGrid[int(currX + 1)%15][int(currY)%30] and not(availMoves[1][1] == 0)):  #If 1 step down in in danger zone and we could go down
        availMoves[1][1] = 1
    if(dangerGrid[int(currX)%15][int(currY - 1)%30] and not(availMoves[2][1] == 0)):  #If 1 step left in in danger zone and we could go left
        availMoves[2][1] = 1
    if(dangerGrid[int(currX)%15][int(currY + 1)%30] and not(availMoves[3][1] == 0)):  #If 1 step right in in danger zone and we could go right
        availMoves[3][1] = 1

    if(np.sum(availMoves[:,1]) == 0):
        return 0
    else:
        return availMoves[availMoves[:,1].argmax()][0]

# game loop
while True:
    helper_bots = int(input())  # your number of charges left to deploy helper bots
    deployCount = helper_bots
    dangerGrid = np.zeros((15, 30))  #Resets danger grid
    for i in range(player_count):
        # x: your bot's coordinates on the grid (0,0) is top-left
        x, y = [int(j) for j in input().split()]
        recordMove(i, x, y)
    removal_count = int(input())  # the amount walls removed this turn by helper bots
    for i in range(removal_count):
        # remove_x: the coordinates of a wall removed this turn
        remove_x, remove_y = [int(j) for j in input().split()]
    calculateDangerZones()
    currentX = pos[roundCount][my_id][0]
    currentY = pos[roundCount][my_id][1]
    if(dirr):
        lastDirectionForMain = dirr
    dirr = detect2(currentX, currentY)
    print(dirr, file=sys.stderr)
    surviveCurrentAlg = calculateSurviveRounds(currentX, currentY, dirr)
    surviveStraight = calculateSurviveRounds(currentX, currentY, lastDirectionForMain)
    print("Current Position: ", currentX, currentY, "direction: ", dirr, "Last Direction: ", lastDirectionForMain, file = sys.stderr)
    print("Survive Rounds not turning", surviveStraight, file=sys.stderr)
    print("Survive Rounds Current Algorithm ", surviveCurrentAlg, file=sys.stderr)
    if(surviveCurrentAlg < surviveStraight):
        ct(lastDirectionForMain, currentX, currentY)
    else:
        ct(dirr, currentX, currentY)
    roundCount = roundCount + 1