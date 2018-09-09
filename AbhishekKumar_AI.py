"""
PROGRAM SPECIFICATION

This program plays tic tac toe against the user. 



The state of the game is determined by the configuration of x's and o's on the board, and the difficulty level.

The display always shows the game board, consisting of two vertical and two horizontal line segments, a rectangular 'reset' button, and three circular difficulty buttons labeled 'easy', 'medium', and 'hard'. Exactly one of the round difficulty buttons will have a smaller circle within it, indicating the current difficulty level. If the game is over, a message is also displayed saying whether 'x' won, 'o' won, or the game was a tie.

The program plays according to the usual rules and has three difficulty settings:  easy, medium, or hard.

The human always plays x and goes first. Whenever it is the human player’s turn, he may place an x in an empty cell by clicking inside that cell. The computer will move automatically when it is o’s turn. When the game is over, a message is displayed saying whether x won, o won, or the game was a tie. No moves can be made when the game is over.

In easy mode the computer moves at random; in medium mode the computer uses a simple strategy : win if you can; otherwise block if you must; otherwise, move in the center if possible; otherwise move in a corner if possible; otherwise move at random. In hard difficulty the computer plays perfectly: it cannot be beaten, and will win from any position where the computer can force a win.

The player may restart the game at any time by hitting the reset button. When this is done, all cells become empty. The difficulty level does not change when new game is pressed. The player can also change the difficulty level at any time, by clicking the appropriate button, and this action does not change the contents of the game board. That is, the player can change the difficulty setting in the middle of a game.

The game board is displayed at all times, showing the contents of each cell. Also displayed is a reset button, and three buttons for easy, medium, and hard difficulties respectively. One of these buttons will be highlighted at any time

"""



"""
DATA MODEL

A *cell* is a natural number in {1..9}. Cells represent
squares on the tic tac toe board as pictured below:

   1|2|3
   -----
   4|5|6
   -----
   7|8|9

A *player* is 0 or 1. 0 represents 'o' and 1 represents 'x'.

An *image* is a drawable object from graphics.py. This includes points,
lines, and circles, and texts, written as below:

   *) Point(x,y) is a point with coordinates x and y (horizontal and vertical
   distance from the top  left corner of the graphics window)

   *) Line(p,q) is a line segment from point p to point q. 

   *) Circle(p,r) is a circle with center point p and radius r.
   
   *) Text(p,str)is the string str centered at point p


A *sprite* is a set of images. 

A *position* is a set of cells, representing the set of cells occupied by
a player at some stage of the game. 

A *gameState* is a pair of positions. The game state (xs,os) represents
the game state in which xs is the set of cells occupied by 'x', and os
is the set of cells occupied by 'o'.

A *difficulty* is 'easy', 'medium', or 'hard'. 

A *pairOfInts* is a pair of integers.

"""

# display : Position * Position * Difficulty -> Sprite
#
# display(xs,os,d) is the sprite consisting of the hash marks in the play
# area, the reset button, and all x's and o's on the board, and the 
# difficulty buttons, as well as the results message in case the game is over.

def display(xs,os,d):
	basicDisplay = grid() | XOImages(xs,os) | resetButton() | difficulty() | easyInnerButton() | mediumInnerButton() | hardInnerButton()
	if gameOver(xs,os): return basicDisplay | GameOverMessage(xs,os)
	else: return basicDisplay

# seg: int*int*int*int -> Line
#
# seg(x1,y1,x2,y2) is the so-called "Line" with endpoints Point(x1,y1) 
# and Point(x2,y2).

def seg(x1,y1,x2,y2): return Line(Point(x1,y1),Point(x2,y2))

# grid(): sprite
# grid() is a sprite of the four hashmarks of the tic tac toe game board.

def grid():
	L1=seg(250,100,250,400)
	L2=seg(350,100,350,400)
	L3=seg(150,200,450,200)
	L4=seg(150,300,450,300)
	return {L1,L2,L3,L4}

# center: cell -> Point
# center(c) is the center point of cell c on the display

def center(c):
    x = 200 + 100*((c-1)%3)
    y = 150 + 100*((c-1)//3)
    return Point(x,y)

# XOImages:position*position->Sprite
# This is the sprite of the x's and o's on the board. 
# I did this using text, so it does not look cool. 

def XOImages(xs,os):
    Ximages = {Text(center(c),'x') for c in xs} 
    Oimages = {Text(center(c),'o') for c in os}
    return (Ximages | Oimages)

def resetButton():
    Reset1 = Line(Point(10,10),Point(10,110))
    Reset2 = Line(Point(110,10),Point(110,110))
    Reset3 = Line(Point(10,10),Point(110,10))
    Reset4 = Line(Point(10,110),Point(110,110))
    Text1 = Text(Point(60,60),'RESET')
    ResetButton = {Reset1,Reset2,Reset3,Reset4,Text1}
    return ResetButton
    
def difficulty():
    Circle1 = {Circle(Point(500,400),10)}
    Circle2 = {Circle(Point(500,430),10)}
    Circle3 = {Circle(Point(500,460),10)}
    Text2 = Text(Point(550,400),'easy')
    Text3 = Text(Point(550,430),'medium')
    Text4 = Text(Point(550,460),'hard')
    Text_Level = {Text2,Text3,Text4}
    Circle_Buttons = Circle1 | Circle2 | Circle3 | Text_Level
    return Circle_Buttons

# GameOverMessege: position*position->sprite
#
# When the game is over, a message giving the result of the game ("Congratulations! X is the winner", "Congratulations! O is the winner", or "TIE GAME")
# will be displayed until the reset button is clicked.
# If the reset button is clicked, the game is reset to its initial state with all cells blank.

def GameOverMessage(xs,os):
    X_win = Text(Point(300,50),'Congratulations! X is the winner')
    Tie_Game = Text(Point(300,50),'TIE GAME')
    O_win = Text(Point(300,50),'Congratulations! O is the winner')
    normal = Text(Point(300,50),'')
    if(gameOver(xs,os) == True and threeInRow(xs) == True):
        return {X_win,} 
    if(gameOver(xs,os) == True and threeInRow(os) == True):
        return {O_win,}
    if(not threeInRow(xs) == True and not threeInRow(os) == True and boardFull(xs,os) == True):
        return {Tie_Game,}
    else:
        return {normal,}
   
# computerMove: Position*Position*Difficulty -> Cell
#
# computerMove(xs,os,d) is the move the computer makes in game state (xs,os)
# when difficulty is set to d.

def computerMove(xs,os,dif):
   if dif == 'easy': return eComputerMove(xs,os)
   if dif=='medium': return mComputerMove(xs,os)
   if dif=='hard'  : return hComputerMove(xs,os)

# eComputerMove: position*position -> Cell
#
# eComputerMove(xs,os) is a random cell that is unoccupied in state (xs,os)

def eComputerMove(xs,os):
    emptyCells = [c for c in range(1,10) if not c in xs|os]
    return choice(emptyCells)

# winner: position*position*Cell -> Bool
# winner(xs,os,c) iff that in state (xs,os), o wins by moving in c.

def winner(xs,os,c):
    if not occupied(c,xs,os) and threeInRow(os|{c}) == True:
        return True
    else:
        return False
# blocker: position*position*Cell -> Bool
# blocker(xs,os,c) iff that in state (xs,os), there is a row in which x has 
# two marks and c is unoccupied. 

def blocker(xs,os,c):
    if not occupied(c,xs,os) and threeInRow(xs|{c})== True:
        return True
    else:
        return False
    
# mComputerMove: position * position * difficulty -> Cell 
# If the game is not over, mComputerMove(xs,os) is the move the computer 
# makes in state (xs,os) on meduium difficulty.


def mComputerMove(xs,os):
   winners = [c for c in range(1,10) if winner(xs,os,c)]
   if len(winners)>0:
       return winners[0]

   blockers = [c for c in range(1,10) if blocker(xs,os,c)]
   if len(blockers)>0:
       return blockers[0]

   if not occupied(5,xs,os):
       return 5 

   corners = [w for w in [1,3,7,9] if not occupied(w,xs,os)]
   if len(corners)>0:
       return corners[0]

   open = [c for c in range(1,10) if not occupied(c,xs,os)]
   return open[0]

# hComputerMove : position*position -> cell
# hComputerMove(xs,os) is a move with the highest value the computer
# can force in the end state from game state (xs,os).

# successors: gameState -> set<gameState>
#
# successors(S) is the set of all game states that may be obtained 
# from S by  making a single move which is legal in S. 

def successors(S):
  xs = S[0]
  os = S[1]
  return [newXsOs(xs,os,c) for c in range(1,10) if legalMove(c,xs,os)]

def xwins(S):
        xs = S[0]
        if threeInRow(xs):return True
        else: False
#xs = S[0]
     #   return threeInRow(xs)
#else: return False

def owins(S):
          os = S[1]
          if threeInRow(os): return True
          else: return False


def tiegame(S):
        xs = S[0]
        os = S[1]
        if  boardFull(xs,os) and not threeInRow(xs) and not threeInRow(os):
                return True
        else: return False

def osMove(S):
        xs = S[0]
        os = S[1]
        #xn=len(xs)
        #on=len(os)
        if not gameOver(xs,os) and len(xs|os)%2!=0:
            return True
        else: return False

        
def xsMove(S):
        xs = S[0]
        os = S[1]
        if not gameOver(xs,os) and len(xs|os)%2==0:
            return True
        else: return False

def val(S):
    if xwins(S): return -1
    elif owins(S): return 1
    elif tiegame(S): return 0
    elif osMove(S): return max({val(x) for x in successors(S)})
    elif xsMove(S): return min({val(x) for x in successors(S)}) 


# hComputerMove : position*position -> cell
# hComputerMove(xs,os) is a move with the highest value the computer
# can force in the end state from game state (xs,os).

def hComputerMove(xs,os):
    Mvs = [c for c in range(1,10) if legalMove(c,xs,os)]
    wins   = [c for c in Mvs if val(newXsOs(xs,os,c)) == 1]
    ties   = [c for c in Mvs if val(newXsOs(xs,os,c)) == 0]
    losses = [c for c in Mvs if val(newXsOs(xs,os,c)) == -1]
    return (wins+ties+losses)[0]


# easyClicked:pairOfInts -> Bool
#
# easyClicked(pt) iff point Point(pt[0],pt[1]) is in the 'easy' button

def easyClicked(pt):
    radius = 10
    dist = ((pt[0]-500)**2+(pt[1]-400)**2)**0.5
    if dist<radius: return True
    
def easyOriginalCircle():
       EasyCircle={Circle(Point(500,400),10)}
       return EasyCircle

def easyInnerButton():
        if dif=='easy': return {Circle(Point(500,400),5)}
        else: return easyOriginalCircle()

       
# mediumClicked:pairOfInts -> Bool
#
# mediumClicked(pt) if Point(pt[0],pt[1]) is in the 'medium' button. 

def mediumClicked(pt):
    radius =10
    dist = ((pt[0]-500)**2+(pt[1]-430)**2)**0.5
    if dist<radius: return True

def mediumOriginalCircle():
       MediumCircle={Circle(Point(500,430),10)}
       return MediumCircle

def mediumInnerButton():
        if dif=='medium': return {Circle(Point(500,430),5)}
        else: return mediumOriginalCircle()

# hardClicked: pairOfInts -> Bool
#
# hardClicked(pt) if Point(pt[0],pt[1]) is in the 'hard' button

def hardClicked(pt):
    radius =10
    dist = ((pt[0]-500)**2+(pt[1]-460)**2)**0.5
    if dist<radius: return True

def hardOriginalCircle():
       HardCircle={Circle(Point(500,460),10)}
       return HardCircle

def hardInnerButton():
        if dif=='hard': return {Circle(Point(500,460),5)}
        else: return hardOriginalCircle()   

        
# inResetButton: pairOfInts -> Bool
#
# inResetButton(pt) if Point(pt[0],pt[1]) is in the interior of the 
# 'reset' button
# YOUR CODE GOES HERE

def inResetButton(pt):
    return ((pt[0]>10 and pt[0]<110) and (pt[1]>10 and pt[1]<110))

# gameOver : Position * Position -> Bool
#
# gameOver(xs,os) iff the game is over in state (xs,os)
# YOUR CODE GOES HERE

def gameOver(xs,os):
    return boardFull(xs,os) or threeInRow(xs) or threeInRow(os)

# if legalMove(c,xs,os), then newXsOs(xs,os,c) is the game state obtained from the state (xs, os) by moving in cell c.
# newXsOs : position x position x cell -> gameState
def newXsOs(xs,os,c):
    if even(len(xs|os)):
        return (xs|{c}, os)
    else:
        return (xs, os|{c})

# even(n) means that integer n is even.
# even : number -> Bool
def even(n):
    return n%2 == 0

# legalMove : Cell * Position * Position -> Bool
#
# legalMove(c,xs,os) if c is a legal move in game state (xs,os), that is, if
# the game is not over and c is not occupied.

def legalMove(c,xs,os):
    return (not occupied(c,xs,os) and not gameOver(xs,os))    

# occupied(c,xs,os) means that cell c is occupied in game state (xs,os).
# occupied: cell x position x position -> Bool
def occupied(c,xs,os):
    return (c in xs or c in os)

# gameover(xs,os) means that the game is over in state (xs,os).
# gameOver: position x position -> Bool
def gameOver(xs,os):
    return boardFull(xs,os) or threeInRow(xs) or threeInRow(os)

# boardFull(xs,os) means the board is full in state (xs,os).
# boardFull: position x position  -> Bool
def boardFull(xs,os):
    return len(xs|os) == 9

# threeInRow(pos) means that position pos contains (as members) all of the cells in some row, either vertically, horizontally, or diagonally. 
# threeInRow : position -> Bool
def threeInRow(pos):
    return any([r<=pos for r in Rows])

# A row is a set of three  cells that form a line on the board either vertically, horizontally, or diagonally. 
# Rows is the set of all such rows.
# Rows: P(P(cell))
Rows = [{1,2,3},{4,5,6},{7,8,9},{1,4,7},{2,5,8},{3,6,9},{1,5,9},{3,5,7}]

# inCell(c,x,y) if and only if point p is in the interior of cell c.
# YOUR CODE GOES HERE

def inCell(c,x,y):
    if (c==1):
        return any([x>100 and x<250 and y>100 and y<200])
    if (c==2):
        return any([x>250 and x<350 and y>100 and y<200])
    if (c==3):
        return any([x>350 and x<450 and y>100 and y<200])
    if (c==4):
        return any([x>150 and x<250 and y>200 and y<300])
    if (c==5):
        return any([x>250 and x<350 and y>200 and y<300])
    if (c==6):
        return any([x>350 and x<450 and y>200 and y<300])
    if (c==7):
        return any([x>150 and x<250 and y>300 and y<400])
    if (c==8):
        return any([x>250 and x<350 and y>300 and y<400])
    if (c==9):
        return any([x>350 and x<450 and y>300 and y<400])



######################################################################
# Tic Tac Toe

# Import graphics library by John Zelle,Wartburg Univ.
#downloadable at http://mcsp.wartburg.edu/zelle/python/

from graphics import *
from time import *
from random import *

# Create a window to play in
displayWidth = 600
displayHeight = 500
gameWindow = GraphWin("My game", displayWidth , displayHeight)


# Initialize the program
# The state variables in this program are xs and os. The game state
# (xs,os) reflects the state of the board at any point in program
# execution.

(xs,os) = (set(),set())
dif = 'easy'
click = None


######################################################################
# The main loop

while(True):

    print(xs,os,dif,click)
    # Draw the display
    images = display(xs,os,dif)
    for x in images: x.draw(gameWindow)

    # If it is the computer's move, make a move then wait 1 second
    if not gameOver(xs,os) and not even(len(xs|os)):
        os = os | {computerMove(xs,os,dif)}
        sleep(0.5)

    # If it is not the computer's move..
    else:
        # wait for a mouse click, and store its
        # coordinates in click
        c = gameWindow.getMouse()
        click = (c.getX(),c.getY())

        # If a difficulty button was clicked, set difficulty appropriately
        if easyClicked(click): dif = 'easy'
        if mediumClicked(click): dif = 'medium'
        if hardClicked(click): dif = 'hard'


        # if the reset button has been clicked, reset the
        # game state
        if inResetButton(click):
            (xs,os) = (set(),set())


        # If a cell has been clicked and it is legal to move there,
        # add an appropriate mark to that cell.
        for c in range(1,10):
            if inCell(c,click[0],click[1]) and legalMove(c,xs,os):
                (xs,os) = newXsOs(xs,os,c)
            
    # undraw the screen
    for I in images: I.undraw()
    
