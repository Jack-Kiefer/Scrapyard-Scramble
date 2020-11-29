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
    def __repr__(self):
        return self.name
    
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
    
class Arm(Card):
    def __init__(self, name, effectS):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 2
    def giveScore(self, app, p):
        self.pointM = 2
        for card in app.cards[p]:
            if card.name == self.name: 
                self.pointM += 1
        return (self.speedM, self.intM, self.pointM)

def appStarted(app):
    app.titleScreen = True
    app.highlight = 0
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
    stickyBoots = Card('sticky boots', '+4 Points, -1 Speed', -1, 0, 4)
    notSmart = Card('not smart', '-1 Intelligence, +4 Points', 0, -1, 4)
    powerBoost = Card('power boost', '+1 Speed, +1 Intelligence', 1, 1, 0)
    extraArm = Arm('extra arm', '+1 Point for each arm you have (you start with 2 arms)')
    Overclock = Card('Overclock', '+5 Points, -1 Speed, -1 Intelligence', -1, -1, 5)
    app.deck = [laserBlaster, buzzsaw, rocketLauncher, machineGun, 
                laserBlasterShield, buzzsawShield, 
                rocketLauncherShield, machineGunShield, jetpack, 
                jetpack, jetpack, rocketBoots, rocketBoots,
                w15112, w15112, w15112, neuralNetworks, neuralNetworks,
                armor, armor, stickyBoots, stickyBoots, notSmart, 
                notSmart, Overclock, Overclock, extraArm,extraArm,extraArm,extraArm,extraArm] 
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
    app.maxDepth = 100
    #0 is 2 player, 1 is random, 2 is minimax with max depth 2, 3 is minimax with full depth
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
    if len(app.deck) < 6 and noneCount == 5:
        endGame(app)
        return
    if noneCount == 5 and len(app.deck) >= 6:
        newPile(app)
    if app.gameMode > 0 and not app.p1turn:
        moveI = generateMove(app)
        pickCard(app, moveI)
    calculateScore(app, 0)
    calculateScore(app, 1)


def generateMove(app):
    if app.gameMode == 1:
        num = random.randint(0, len(app.pile) - 1)
        if app.pile[num] == None: return generateMove(app)
        else: return num
    if app.gameMode == 2 or app.gameMode == 3:
        return minimax(app)

def minimax(app):
    pile = copy.deepcopy(app.pile)
    cards = copy.deepcopy(app.cards)
    x, move = minimaxHelper(app, 1, 0)
    #print(app.pile)
    #print(app.cards)
    app.pile = pile
    app.cards = cards
    #print(app.cards)
    calculateScore(app, 0)
    calculateScore(app, 1)
    return move
            
def minimaxHelper(app, turn, depth):
    if app.pile.count(None) == 5 or depth == app.maxDepth:
        calculateScore(app, 0)
        calculateScore(app, 1)
        if app.speed[0] > app.speed[1]:
            app.score[0] += 10
        elif app.speed[1] > app.speed[0]:
            app.score[1] += 10
        if app.intel[0] > app.intel[1]:
            app.score[0] += 10
        elif app.intel[1] > app.intel[0]:
            app.score[1] += 10
        #print(" "*depth,"scorediff=",app.score[1] - app.score[0])
        if turn == 1: return (app.score[1] - app.score[0], 0)
        else: return app.score[1] - app.score[0]
    elif turn == 1:
        maxi = -100
        move = None
        for i in range(len(app.pile)):
            #print(app.pile[i])
            if app.pile[i] != None:
                temp = copy.copy(app.pile[i])
                app.cards[1] += [temp]
                app.pile[i] = None
                result = minimaxHelper(app, 0, depth + 1)
                if result > maxi:
                    #print(minimaxHelper(app, 0))
                    maxi = result
                    move = i
                app.pile[i] = temp
                for k in range(len(app.cards[1])):
                    if temp.name == app.cards[1][k].name:
                        app.cards[1].pop(k)
                        break
        #print(" "*depth,"maxi=",(maxi, move))
        return (maxi, move)
    else:
        mini = 100
        for i in range(len(app.pile)):
            if app.pile[i] != None:
                temp = copy.copy(app.pile[i])
                #print(" "*depth,"temp=", temp)
                app.cards[0] = app.cards[0] + [temp]
                app.pile[i] = None
                score, move = minimaxHelper(app, 1, depth + 1)
                if score < mini:
                    #print(score)
                    mini = score
                app.pile[i] = temp
                #print(" "*depth,app.cards[0])
                for k in range(len(app.cards[0])):
                    if temp.name == app.cards[0][k].name:
                        app.cards[0].pop(k)
                        break
                #print(" "*depth,app.cards[0])

        #print(" "*depth,"mini=",mini)
        return mini

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
    elif app.speed[1] > app.speed[0]:
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
    if app.titleScreen:
        if event.key == "Up":
            if app.highlight != 0:
                app.highlight -= 1
        if event.key == "Down":
            if app.highlight != 3:
                app.highlight += 1
        if event.key == "Space":
            app.titleScreen = False
            app.gameMode = app.highlight
            if app.gameMode == 2:
                app.maxDepth = 2
    else:
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
                        else:
                            if app.hrow == 0:
                                if isinstance(app.pile[i + 2], Card):
                                    print('yes')
                                    app.hrow += 1
                                    app.hcol -= 1
                                elif isinstance(app.pile[i + 1], Card) and app.hcol == 2:
                                    app.hrow += 1
                                    app.hcol -= 2
                            elif app.hrow == 1:
                                if isinstance(app.pile[i - 4], Card):
                                    app.hrow -= 1
                                    app.hcol -= 1
                                elif isinstance(app.pile[i - 5], Card) and app.hcol == 2:
                                    app.hrow -= 1
                                    app.hcol -= 2


            elif event.key == "Right":
                if app.hcol != 2:
                    if isinstance(app.pile[i + 1], Card):
                        app.hcol += 1
                    else:
                        if app.hcol == 0 and isinstance(app.pile[i + 2], Card):
                            app.hcol += 2
                        else:
                            if app.hrow == 0:
                                if isinstance(app.pile[i + 4], Card):
                                    app.hrow += 1
                                    app.hcol += 1
                                elif app.hcol == 0 and isinstance(app.pile[i + 5], Card):
                                    app.hrow += 1
                                    app.hcol += 2
                            elif app.hrow == 1:
                                if isinstance(app.pile[i - 2], Card):
                                    app.hrow -= 1
                                    app.hcol += 1
                                elif isinstance(app.pile[i - 1], Card) and app.hcol == 0:
                                    app.hrow -= 1
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
                app.maxDepth = 100
            elif event.key == '3':
                app.gameMode = 2
                app.maxDepth = 2


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
    i = app.hcol + 3*app.hrow
    h = app.pile[i].name
    d = app.pile[i].effectS
    canvas.create_text(app.width//2, 900, text=d)

def drawScores(app, canvas):
    if app.p1turn: text = "Player 1's Turn"
    else:text = "Player 2's Turn"
    canvas.create_text(app.width//2, 150, text=text)
    canvas.create_text(900, 860, text=f'Score = {app.score[1]}')
    canvas.create_text(100, 860, text=f'Score = {app.score[0]}')
    canvas.create_text(900, 880, text=f'Speed = {app.speed[1]}')
    canvas.create_text(100, 880, text=f'Speed = {app.speed[0]}')
    canvas.create_text(900, 900, text=f'Intelligence = {app.intel[1]}')
    canvas.create_text(100, 900, text=f'Intelligence = {app.intel[0]}')

def drawPicks(app,canvas):
    for i in range(len(app.cards[0])):
        canvas.create_text(250, 20*(i+1), text=app.cards[0][i].name)
    for i in range(len(app.cards[1])):
        canvas.create_text(750, 20*(i+1), text=app.cards[1][i].name)

def drawTitleScreen(app, canvas):
    canvas.create_text(app.width//2, app.height//4, text='Scrapyard Scramble', font="Times 48 bold")
    modes = ["2 Player", "Easy", "Medium", "Hard"]
    for row in range(4):
        x = 130 * row
        if row == app.highlight:
            canvas.create_rectangle(app.width//2 - 180, app.height//2 - 180 + x, app.width//2 + 180, app.height//2 - 80 + x, width=5, outline='red')
        else:
            canvas.create_rectangle(app.width//2 - 180, app.height//2 - 180 + x, app.width//2 + 180, app.height//2 - 80 + x, width=5)
        canvas.create_text(app.width//2, app.height//2 + x - 130, text=modes[row], font="Times 20 bold")

def drawEnd(app, canvas):
    if app.titleScreen:
        drawTitleScreen(app, canvas)
    else:
        drawScores(app,canvas)
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



