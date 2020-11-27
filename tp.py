import random, math
from cmu_112_graphics import *
import copy

class Card(object):
    def __init__(self, name, effectS, speedM, intM, pointM):
        self.name = name
        self.effectS = effectS
        self.speedM = speedM
        self.intM = intM
        self.pointM = pointM
    def giveScore(self, app, player):
        return (self.speedM, self.intM, self.pointM)
    def __eq__(self, other):
        return isinstance(other, Card) 
    
class Weapon(Card):
    def __init__(self, name, effectS, shieldName):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 0
        self.shieldName = shieldName
    def giveScore(self, app, p):
        foundCard = False
        if p == 1: op = 0
        else: op = 1
        for card in app.cards[op]:
            if card.name == self.shieldName: foundCard = True
        if foundCard: self.pointM = 2
        else: self.pointM = 5
        return (self.speedM, self.intM, self.pointM)

class Shield(Card):
    def __init__(self, name, effectS, weaponName):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 0
        self.weaponName = weaponName
    def giveScore(self, app, p):
        foundCard = False
        if p == 1: op = 0
        else: op = 1
        for card in app.cards[op]:
            if card.name == self.weaponName: foundCard = True
        if foundCard: self.pointM = 5
        else: self.pointM = 2
        return (self.speedM, self.intM, self.pointM)


def appStarted(app):
    app.pile = []
    app.p1turn = True
    app.cards = [[],[]]
    app.margin = 200
    app.cellmargin = 20
    laserBlaster = Weapon('laser blaster', '+5 if opponent does not have a laser blaster shield, otherwise +2 points', 'laser blaster shield')
    buzzsaw = Weapon('buzzsaw', '+5 if opponent does not have a buzzsaw shield, otherwise +2 points', 'buzzsaw shield')
    rocketLauncher = Weapon('rocket launcher', '+5 if opponent does not have a rocket launcher shield, otherwise +2 points', 'rocket launcher shield')
    machineGun = Weapon('machine gun', '+5 if opponent does not have a machine gun shield, otherwise +2 points', 'machine gun shield')
    laserBlasterShield = Shield('laser blaster shield', '+5 if opponent has a laser blaster, otherwise +2 points', 'laser blaster')
    buzzsawShield = Shield('buzzsaw shield', '+5 if opponent has a buzzsaw, otherwise +2 points', 'buzzsaw')
    rocketLauncherShield = Shield('rocket launcher shield', '+5 if opponent has a rocket launcher, otherwise +2 points', 'rocket launcher')
    machineGunShield = Shield('machine gun shield', '+5 if opponent has a machine gun, otherwise +2 points', 'machine gun')
    jetpack = Card('jetpack', '+2 Speed', 2, 0, 0)
    rocketBoots = Card('rocket boots', '+3 Speed, -1 Intelligence', 3, -1, 0)
    w15112 = Card('15-112', '+2 Intelligence', 0, 2, 0)
    neuralNetworks = Card('neural networks', '-1 Speed, +3 Intelligence', -1, 3, 0)
    armor = Card('armor', '+3 Points', 0, 0, 3)
    stickyBoots = Card('sticky boots', '+3 Points, -1 Speed', -1, 0, 3)
    notSmart = Card('not smart', '+5 if opponent does not have a buzzsaw shield, otherwise +2 points', 0, -1, 4)
    #Stuff = Card('Stuff', '1 + the amount of Stuff you have Points')
    Overclock = Card('Overclock', '+5 Points, -1 Speed, -1 Intelligence', -1, -1, 5)
    app.deck = [laserBlaster, buzzsaw, rocketLauncher, machineGun, 
                laserBlasterShield, buzzsawShield, 
                rocketLauncherShield, machineGunShield, jetpack, 
                jetpack, rocketBoots, rocketBoots,
                w15112, w15112, neuralNetworks, neuralNetworks,
                armor, armor, stickyBoots, stickyBoots, notSmart, 
                notSmart, Overclock, Overclock] 
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
    app.gameMode = 0
    #0 is 2 player, 1 is random, 2 is minimax
    newPile(app)

def pickCard(app, i):
    #Adds cards to player's cards
    if app.p1turn: 
        app.cards[0] += [app.pile[i]]
        app.pile[i] = None
    else:
        app.cards[1] += [app.pile[i]]
        app.pile[i] = None
    #switches turn
    app.p1turn = not app.p1turn
    #Makes new pile if the pile has 1 card left
    noneCount = app.pile.count(None)
    if noneCount == 5 and len(app.deck) >= 6:
        newPile(app)
    if app.gameMode > 0 and not app.p1turn:
        moveI = generateMove(app)
        pickCard(app, moveI)
    calculateScore(app, 0)
    calculateScore(app, 1)
    if len(app.deck) < 6 and noneCount == 5:
        endGame(app)

def generateMove(app):
    if app.gameMode == 1:
        num = random.randint(0, len(app.pile) - 1)
        if app.pile[num] == None: return generateMove(app)
        else: return num
    if app.gameMode == 2:
        return minimax(app)

def minimax(app):
    pile = app.pile.copy()



def calculateScore(app, p):
    if p == 1: op = 0
    else: op = 1
    app.score[p] = 0
    app.speed[p] = 0
    app.intel[p] = 0
    for card in app.cards[p]:
        speed, intel, score = card.giveScore(app, p)
        app.score[p] += score
        app.intel[p] += intel
        app.speed[p] += speed

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
        i = app.hcol + 3*app.hrow
        if event.key == "Up": 
            if app.hrow != 0 and isinstance(app.pile[i - 3], Card):
                app.hrow -= 1
        elif event.key == "Down":
            if app.hrow != 1 and isinstance(app.pile[i + 3], Card):
                app.hrow += 1
        elif event.key == "Left":
            if app.hcol != 0:
                if isinstance(app.pile[i - 1], Card):
                    app.hcol -= 1
                else:
                    if isinstance(app.pile[i - 2], Card) and i-2 >= 0:
                        app.hcol -= 2
        elif event.key == "Right":
            if app.hcol != 2:
                if isinstance(app.pile[i + 1], Card):
                    app.hcol += 1
                else:
                    if isinstance(app.pile[i + 2], Card):
                        app.hcol += 2
        elif event.key == 'Space':
            pickCard(app, i)
            for c in range(6):
                if isinstance(app.pile[c], Card):
                    app.hrow = c // 3
                    app.hcol = c % 3

        elif event.key == '1':
            app.gameMode = 1
        elif event.key == '2':
            app.gameMode = 2


def newPile(app):
    app.pile = []
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
            if len(app.pile) >= i+1 and app.pile[i] != None:
                canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=10)
                canvas.create_text((x1+x0)//2, (y1+y0)//2, text=app.pile[i].name)
    if app.p1turn: text = "Player 1's Turn"
    else:text = "Player 2's Turn"
    canvas.create_text(app.width//2, 150, text=text)
    canvas.create_text(900, 860, text=f'Score = {app.score[1]}')
    canvas.create_text(100, 860, text=f'Score = {app.score[0]}')
    canvas.create_text(900, 880, text=f'Speed = {app.speed[1]}')
    canvas.create_text(100, 880, text=f'Speed = {app.speed[0]}')
    canvas.create_text(900, 900, text=f'Intelegence = {app.intel[1]}')
    canvas.create_text(100, 900, text=f'Intelegence = {app.intel[0]}')
    #Draw text at bottom
    i = app.hcol + 3*app.hrow
    h = app.pile[i].name
    d = app.pile[i].effectS
    canvas.create_text(app.width//2, 900, text=d)

def drawPicks(app,canvas):
    for i in range(len(app.cards[0])):
        canvas.create_text(250, 20*(i+1), text=app.cards[0][i].name)
    for i in range(len(app.cards[1])):
        canvas.create_text(750, 20*(i+1), text=app.cards[1][i].name)

def drawEnd(app, canvas):
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

def redrawAll(app,canvas):
    drawPicks(app,canvas)
    drawEnd(app, canvas)


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



