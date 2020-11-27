from dataclasses import make_dataclass
import random, math
from cmu_112_graphics import *

def appStarted(app):
    app.pile = []
    app.p1turn = True
    app.cards = [[],[]]
    app.margin = 200
    app.cellmargin = 20
    app.deck = ['laser blaster', 'buzzsaw', 'rocket launcher', 'machine gun', 
                'laser blaster shield', 'buzzsaw shield', 
                'rocket launcher shield', 'machine gun shield', 'jetpack', 
                'jetpack', 'rocket boots', 'rocket boots',
                '15-112', '15-112', 'neural networks', 'neural networks',
                'armor', 'armor', 'sticky boots', 'sticky boots', 'not smart', 
                'not smart', 'Stuff', 'Stuff','Stuff', 'Stuff', 'Stuff', 
                'Overclock','Overclock']
    app.effectDict = {
        'laser blaster': '+5 if opponent does not have a laser blaster shield, otherwise +2 points',
        'buzzsaw': '+5 if opponent does not have a buzzsaw shield, otherwise +2 points',
        'rocket launcher': '+5 if opponent does not have a rocket launcher shield, otherwise +2 points',
        'machine gun': '+5 if opponent does not have a machine gun shield, otherwise +2 points',
        'laser blaster shield': '+5 if opponent has a laser blaster, otherwise +2 points',
        'buzzsaw shield': '+5 if opponent has a buzzsaw, otherwise +2 points',
        'rocket launcher shield': '+5 if opponent has a rocket launcher, otherwise +2 points',
        'machine gun shield': '+5 if opponent has a machine gun, otherwise +2 points',
        'jetpack': '+2 Speed',
        'rocket boots': '+3 Speed, -1 Intelligence',
        '15-112': '+2 Intelligence',
        'neural networks': '-1 Speed, +3 Intelligence',
        'armor': '+3 Points',
        'sticky boots': '+3 Points, -1 Speed',
        'not smart': '+3 Points, -1 Intelligence',
        'Stuff': '1 + the amount of Stuff you have Points',
        'Overclock': '+5 Points, -1 Speed, -1 Intelligence'
    }
    app.powerScources = ['Electric', 'Wind', 'Nuclear', 'Gas', 'Steam']
    app.cols = 3
    app.rows = 2
    app.hrow = 0
    app.hcol = 0
    app.speed = [0,0]
    app.intel = [0,0]
    app.score = [0,0]
    app.gameOver = False
    app.winner = None
    app.gameMode = True
    newPile(app)

def pickCard(app, i):
    if app.p1turn:
        app.cards[0] += [app.pile.pop(i)]
    else:
        app.cards[1] += [app.pile.pop(i)]
    app.p1turn = not app.p1turn
    if len(app.pile) == 1 and len(app.deck) >= 6:
        newPile(app)
    if not app.gameMode and not app.p1turn:
        pickCard(app, random.randint(0, len(app.pile)-1))
    calculateScore(app, 0)
    calculateScore(app, 1)
    if len(app.deck) < 6 and len(app.pile) == 1:
        endGame(app)

def calculateScore(app, p):
    if p == 1: op = 0
    else: op = 1
    app.score[p] = 0
    app.speed[p] = 0
    app.intel[p] = 0
    for name in app.cards[p]:
        if name == 'laser blaster':
            if 'laser blaster shield' not in app.cards[op]:
                app.score[p] += 5
            else:
                app.score[p] += 2
        elif name == 'buzzsaw':
            if 'buzzsaw shield' not in app.cards[op]:
                app.score[p] += 5
            else:
                app.score[p] += 2
        elif name == 'rocket launcher':
            if 'rocket launcher shield' not in app.cards[op]:
                app.score[p] += 5
            else:
                app.score[p] += 2
        elif name == 'machine gun':
            if 'machine gun shield' not in app.cards[op]:
                app.score[p] += 5
            else:
                app.score[p] += 2
        elif name == 'laser blaster shield':
            if 'laser blaster' in app.cards[op]:
                app.score[p] += 5
            else:
                app.score[p] += 2
        elif name == 'buzzsaw shield':
            if 'buzzsaw' in app.cards[op]:
                app.score[p] += 5
            else:
                app.score[p] += 2
        elif name == 'rocket launcher shield':
            if 'rocket launcher' in app.cards[op]:
                app.score[p] += 5
            else:
                app.score[p] += 2
        elif name == 'machine gun shield':
            if 'machine gun' in app.cards[op]:
                app.score[p] += 5
            else:
                app.score[p] += 2
        elif name == 'jetpack':
            app.speed[p] += 2
        elif name == 'rocket boots':
            app.speed[p] += 3
            app.intel[p] -= 1
        elif name == '15-112':
            app.intel[p] += 2
        elif name == 'neural networks':
            app.intel[p] += 3
            app.speed[p] -= 1
        elif name == 'armor':
            app.score[p] += 3
        elif name == 'sticky boots':
            app.score[p] += 4
            app.speed[p] -= 1
        elif name == 'not smart':
            app.score[p] += 4
            app.intel[p] -= 1
        elif name == 'Overclock':
            app.score[p] += 5
            app.intel[p] -= 1
            app.speed[p] -= 1
        elif name == 'Stuff':
            total = app.cards[p].count('Stuff')
            app.score[p] += total + 1


def endGame(app):
    app.gameOver = True
    if app.speed[0] > app.speed[1]:
        app.score[0] += 10
    elif app.score[1] > app.score[0]:
        app.score[1] += 10

    if app.intel[0] > app.intel[1]:
        app.score[0] += 10
    elif app.intel[1] > app.intel[0]:
        app.score[1] += 10

    if app.score[0] > app.score[1]:
        app.winner = 1
    elif app.score[1] > app.score[0]:
        app.winner = 2
    else:
        app.winner = 'tie'


def keyPressed(app, event):
    if event.key == 'r':
        appStarted(app)
    if not app.gameOver:
        if event.key == "Up": 
            if app.hrow != 0:
                app.hrow -= 1
        elif event.key == "Down":
            app.hrow += 1
            if app.hcol + 3*app.hrow > len(app.pile)-1:
                app.hrow -= 1
        elif event.key == "Left":
            if app.hcol != 0:
                app.hcol -= 1
        elif event.key == "Right":
            if app.hcol < 2:
                app.hcol += 1
            if app.hcol + 3*app.hrow > len(app.pile)-1:
                app.hcol -= 1
        elif event.key == 'Space':
            i = app.hcol + 3*app.hrow
            pickCard(app, i)
            app.hrow, app.hcol = 0, 0
        elif event.key == 'p':
            app.gameMode = not app.gameMode


def newPile(app):
    for c in range(6):
        i = random.randint(0, len(app.deck)-1)
        app.pile += [app.deck.pop(i)]
        
def getCellBounds(app, row, col):
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth/ app.cols
    cellHeight = gridHeight/ app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth - app.cellmargin
    y0 = app.margin + row * cellHeight 
    y1 = app.margin + (row+1) * cellHeight - app.cellmargin
    return (x0, y0, x1, y1)

def drawCards(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            x0, y0, x1, y1 = getCellBounds(app, row, col)
            i = col + 3*row
            if row == app.hrow and col == app.hcol:
                outline = 'red'
            else: outline ='Black'
            if len(app.pile) >= i+1:
                canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=10)
                canvas.create_text((x1+x0)//2, (y1+y0)//2, text=app.pile[i])
    if app.p1turn: text = "Player 1's Turn"
    else:text = "Player 2's Turn"
    canvas.create_text(app.width//2, 150, text=text)
    canvas.create_text(900, 860, text=f'Score = {app.score[1]}')
    canvas.create_text(100, 860, text=f'Score = {app.score[0]}')
    canvas.create_text(900, 880, text=f'Speed = {app.speed[1]}')
    canvas.create_text(100, 880, text=f'Speed = {app.speed[0]}')
    canvas.create_text(900, 900, text=f'Intelegence = {app.intel[1]}')
    canvas.create_text(100, 900, text=f'Intelegence = {app.intel[0]}')
    i = app.hcol + 3*app.hrow
    h = app.pile[i]
    d = app.effectDict[h]
    canvas.create_text(app.width//2, 900, text=d)

def drawPicks(app,canvas):
    for i in range(len(app.cards[0])):
        canvas.create_text(250, 20*(i+1), text=app.cards[0][i])
    for i in range(len(app.cards[1])):
        canvas.create_text(750, 20*(i+1), text=app.cards[1][i])


def redrawAll(app,canvas):
    drawPicks(app,canvas)
    if not app.gameOver:
        drawCards(app, canvas)
    else:
        if app.winner == 'tie':
            text = 'It is a tie!'
        else: 
            text = f'Player {app.winner} Wins!'
        canvas.create_text(app.width//2, app.height//2, text=text)
        canvas.create_text(app.width//2, app.height//2 + 20, 
                        text=f'Score was {app.score[0]} to {app.score[1]}')


def playGame():
    width = 1000
    height = 1000
    runApp(width=width, height=height)

#################################################
# main
#################################################

def main():
    playGame()

if __name__ == '__main__':
    main()



