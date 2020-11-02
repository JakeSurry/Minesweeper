#Import Modules
import random 
import pygame
import sys
sys.setrecursionlimit(10**6)
pygame.mixer.pre_init()
pygame.init()
#Initial Board Size Prompt
while True:
	for i in range(3):
		print("")
	boardLenInput = input("How big would you like the board? (small, medium, large) ")
	if boardLenInput == "small":
		boardLen = 10
		break
	elif boardLenInput == "medium":
		boardLen = 20
		break
	elif boardLenInput == "large":
		boardLen = 35
		break
	else:
		for i in range(3):
				print("")
		print("Please enter a valid option!")
#Initial Bomb Amount Prompt
while True:
	for i in range(3):
		print("")
	bombAmnt = input("How many bombs would you like? (max " + str(int(boardLen**2/2)) + ") ")
	try:
		bombAmnt = int(bombAmnt)
	except ValueError:
		for i in range(3):
				print("")
		print("Please enter a number!")
		continue
	if bombAmnt > boardLen**2/2:
		for i in range(3):
				print("")
		print("Please enter a number below " + str(int(boardLen**2/2)))
	else:
		break
#Initialize Boards
squareLen = 700/boardLen
squareBorder = int(squareLen/10)
boardSide = []
board = []
for i in range(boardLen):
	boardSide.append(0)
for i in range(boardLen): 
	board.append(boardSide[:])
topBoard = []
for i in range(boardLen):
	boardSide.append(0)
for i in range(boardLen): 
	topBoard.append(boardSide[:])
#Initialize Display
display = pygame.display.set_mode((700, 800))
pygame.display.set_caption("Minesweeper")
pygame.display.update()
#Initialize Assets
font = pygame.font.Font("Assets/atari-classic-font/AtariClassicExtrasmooth-LxZy.ttf", int(squareLen - squareLen/5*2))
largeFont = pygame.font.Font("Assets/atari-classic-font/AtariClassicSmooth-XzW2.ttf", 40)
flag = pygame.image.load("Assets/flag.png")
bomb = pygame.image.load("Assets/bomb.png")
wrong = pygame.image.load("Assets/x.png")
digSound = pygame.mixer.Sound("Assets/dirt.mp3")
flagSound = pygame.mixer.Sound("Assets/flag.mp3")
bombSound = pygame.mixer.Sound("Assets/bomb.mp3")
digSound.set_volume(.2)
flagSound.set_volume(.1)
bombSound.set_volume(.1)
#Resize Images
flag = pygame.transform.scale(flag, (int(squareLen), int(squareLen)))
dispFlag = pygame.transform.scale(flag, (50, 50))
bomb = pygame.transform.scale(bomb, (int(squareLen), int(squareLen)))
wrong = pygame.transform.scale(wrong, (int(squareLen), int(squareLen)))
#Initialize Variables
clock = pygame.time.Clock()
gameStart = False
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 153, 0)
purple = (102, 0, 204)
burgundy = (153, 0, 0)
cyan = (0, 153, 153)
grey = (160, 160, 160)
gameLoop = "notOver"
mousePos = ()
leftClick = 1
rightClick = 3
timerStart = False
start_time = 0
dispTime = "0:00.000"
minute = 0
totalFlagCount = 0
win = None
#Function To Find Squares Neighboring The Original Square Argument
def getSquares(x, y):
	nearSquares = []
	if x != boardLen - 1:
		nearSquares.append((x+1, y))
		if y != boardLen - 1:
			nearSquares.append((x+1, y+1))
	if y != boardLen - 1:
		nearSquares.append((x, y+1))
		if x != 0:
			nearSquares.append((x-1, y+1))
	if x != 0:
		nearSquares.append((x-1, y))
		if y != 0:
			nearSquares.append((x-1, y-1))
	if y != 0:
		nearSquares.append((x, y-1))
		if x != boardLen - 1:
			nearSquares.append((x+1, y-1))
	return nearSquares
#Generate Board Function
def genBoard(board):
	#Resets Board
	for x in range(boardLen):
		for y in range(boardLen):
			board[x][y] = 0
	#Generates Bombs
	for i in range(bombAmnt):
		while True:
			bomb_row = random.randint(0, boardLen - 1)
			bomb_column = random.randint(0, boardLen - 1)
			if board[bomb_row][bomb_column] != "b":
				board[bomb_row][bomb_column] = "b"
				break
	#Set Values Of Squares On Bottem Board
	for x in range(boardLen):
		for y in range(boardLen):
			if board[x][y] == "b":
				for (nx, ny) in getSquares(x, y):
					if board[nx][ny] != "b":
						board[nx][ny] += 1
#Function To Detect Squares Around A Clicked Blank Square And Uncovers Them As Well
def recursion(x, y):
	for (nx, ny) in getSquares(x, y):
		if topBoard[nx][ny] == 0:
			if board[nx][ny] == 0:
				topBoard[nx][ny] = 1
				recursion(nx, ny)
			elif board[nx][ny] != "b":
				topBoard[nx][ny] = 1
#Function To Draw Number On Square With Appropriate Colour 
def number(colour):
	num = font.render(str(board[x][y]), False, colour, black)
	numRect = num.get_rect()
	numRect = (x * squareLen + squareLen/5, y * squareLen + squareLen/5)
	display.blit(num, numRect)
	rectBorder(x, y, white)
#Function To Draw Boarder Around Square With Appropriate Colour
def rectBorder(x, y, colour):
	pygame.draw.rect(display, colour, (x * squareLen, y * squareLen, squareLen, squareBorder))
	pygame.draw.rect(display, colour, (x * squareLen, y * squareLen + squareLen - squareBorder, squareLen, squareBorder))
	pygame.draw.rect(display, colour, (x * squareLen, y * squareLen, squareBorder, squareLen))
	pygame.draw.rect(display, colour, (x * squareLen + squareLen - squareBorder, y * squareLen, squareBorder, squareLen))
#Main Game Loop
while gameLoop == "notOver":
	#Gets Event
	for event in pygame.event.get():
		#Detects Quit Button
		if event.type == pygame.QUIT:
			gameLoop = "Over"
		#Detects Mouse Press And Mouse Possition
		if event.type == pygame.MOUSEBUTTONDOWN:
			mousePos = pygame.mouse.get_pos()
			#Starts Timer On First Click
			if timerStart == False:
				start_time = pygame.time.get_ticks()
				timerStart = True
			#Translates Mouse Position To Game Board List, Then Detects Which Square Was Pressed
			for x in range(len(topBoard)):
				for y in range(len(topBoard)):
					if  x * squareLen <= mousePos[0] <= x * squareLen + squareLen and y * squareLen <= mousePos[1] <= y * squareLen + squareLen:
						#Detects Left Click And Uncovers Square, As Long As It Isn't A Flag
						if event.button == leftClick and topBoard[x][y] != 2 and topBoard[x][y] != 1:
							#Generates Board Based Off Of Mouse Position On First Click
							if gameStart == False:
								while True:
									genBoard(board)
									if board[x][y] == 0:
										break
								gameStart = True
							#Uncovers Square
							topBoard[x][y] = 1
							#Detects If Square Is A Bomb
							if board[x][y] == "b":
								bombSound.play()
								for x in range(len(board)):
									for y in range(len(board)):
										#Uncovers Square As Long As It Isn't A Flag
										if topBoard[x][y] != 2:
											topBoard[x][y] = 1
										#Detects Misplaced Flags, Then Tags Them
										else:
											if board[x][y] != "b":
												topBoard[x][y] = 3
								#Ends Game
								win = False
								gameLoop = "Over"
							#Detects If Square Is A Blank Square, Then Calls Recursion Funciton
							elif board[x][y] == 0:
								recursion(x, y)
								digSound.play()
							else:
								digSound.play()
						#Detects Right Click, And Whether Or Not Square Is Flagged
						elif event.button == rightClick and topBoard[x][y] != 1:
							#Removes FLag
							if topBoard[x][y] == 2:
								topBoard[x][y] = 0
								flagSound.play()
							#Plants Flag
							else:
								topBoard[x][y] = 2
								flagSound.play()
	#Draws Both Boards
	for x in range(len(board)):
		for y in range(len(board)):
			#Draws Blank Squares
			if board[x][y] == 0:
				pygame.draw.rect(display, black, (x * squareLen, y * squareLen, squareLen, squareLen))
				rectBorder(x, y, white)
			#Draws Number Squares With Appropriate Colour
			elif board[x][y] != "b":
				pygame.draw.rect(display, black, (x * squareLen, y * squareLen, squareLen, squareLen))
				if board[x][y] == 1:
					number(blue)
				elif board[x][y] == 2:
					number(green)
				elif board[x][y] == 3:
					number(red)
				elif board[x][y] == 4:
					number(purple)
				elif board[x][y] == 5:
					number(burgundy)
				elif board[x][y] == 6:
					number(white)
				elif board[x][y] == 7:
					number(cyan)
				elif board[x][y] == 8:
					number(grey)
			#Draws Bombs
			else:
				display.blit(bomb, (x * squareLen, y * squareLen))
				rectBorder(x, y, white)
			#Draws Top Board Squares
			if topBoard[x][y] == 0: 
				pygame.draw.rect(display, white, (x * squareLen, y * squareLen, squareLen, squareLen))
				rectBorder(x, y, black)
			#Draws Flags
			elif topBoard[x][y] == 2:
				display.blit(flag, (x * squareLen, y * squareLen))
				rectBorder(x, y, black)
			#Draws Incorrect Flags
			elif topBoard[x][y] == 3:
				display.blit(wrong, (x * squareLen, y * squareLen))
				rectBorder(x, y, black)
	#Draws Timer Background
	pygame.draw.rect(display, white, (10, 710, 680, 80))
	#Begines Timer
	if timerStart == True:
		#Translates Ticks Into Seconds
		totalSec = (pygame.time.get_ticks() - start_time) / 1000
		sec = totalSec % 60
		minute = int((totalSec - sec) / 60)
		#Generates Timer Text 
		if len(str(int(sec))) == 1:
			dispTime = str(minute) + ":" + "0" + str(round(sec, 3))
		elif len(str(int(sec))) == 2:
			dispTime = str(minute) + ":" + str(round(sec, 3)) 
	#Draws Timer
	time = largeFont.render(str(dispTime), False, black, white)
	timeRect = time.get_rect()
	timeRect = (40, 730)
	display.blit(time, timeRect)
	#Checks If Player Won
	totalCount = 0
	totalFlagCount = 0
	for i in range(len(topBoard)):
		count = topBoard[i].count(1)
		flagCount = topBoard[i].count(2)
		totalCount += count
		totalFlagCount += flagCount
	if totalCount == boardLen*boardLen - bombAmnt and totalFlagCount == bombAmnt:
		win = True
		gameLoop = "over"
	#Draws Flag Counter
	pygame.draw.rect(display, black, (414, 710, 15, 90))
	pygame.draw.rect(display, black, (455, 725, 5, 50))
	pygame.draw.rect(display, black, (510, 725, 5, 50))
	pygame.draw.rect(display, black, (455, 720, 60, 5))
	pygame.draw.rect(display, black, (455, 775, 60, 5))
	display.blit(dispFlag, (460, 725))
	flagCounter = largeFont.render(":" + str(totalFlagCount), False, black, white)
	flagCounterRect = flagCounter.get_rect()
	flagCounterRect = (520, 730)
	display.blit(flagCounter, flagCounterRect)
	#Updates Screen
	pygame.display.update()
#Checks If Player Won
if win:
	#Displays Win Message
	winMessage = largeFont.render("You Win!", False, green, black)
	winMessageRect = winMessage.get_rect()
	winMessageRect = (200, 350)
	display.blit(winMessage, winMessageRect)
	pygame.display.update()
	pygame.time.wait(5000)
#Checks If Player Lost
elif win == False:
	#Waits For Three Seconds
	pygame.time.wait(3000)
#Quits Program
pygame.display.quit()
pygame.quit()