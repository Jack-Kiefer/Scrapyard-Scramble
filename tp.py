import random, math
from cmu_112_graphics import *
import copy
import time

class Card(object):
    def __init__(self, name, effectS, speedM, intM, pointM):
        self.name = name
        self.effectS = effectS
        self.speedM = speedM
        self.intM = intM
        self.pointM = pointM
    def giveScore(self, app, player, i):
        return (self.speedM, self.intM, self.pointM)
    def __eq__(self, other):
        return isinstance(other, Card) and self.name == other.name
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
    def giveScore(self, app, p, i):
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
    def giveScore(self, app, p, i):
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
        self.pointM = 1
    def giveScore(self, app, p, i):
        self.pointM = 1
        for card in app.cards[p]:
            if card.name == self.name: 
                self.pointM += 1
        return (self.speedM, self.intM, self.pointM)

class Boost(Card):
    def __init__(self, name, effectS, type):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 0
        self.type = type
    def giveScore(self, app, p, i):
        if self.type == 's':
            self.pointM = 0
            for card in app.cards[p]:
                if isinstance(card, Shield):
                    self.pointM += 2
            return (self.speedM, self.intM, self.pointM)
        else:
            self.pointM = 0
            for card in app.cards[p]:
                if isinstance(card, Weapon):
                    self.pointM += 2
            return (self.speedM, self.intM, self.pointM)

class Copy(Card):
    def __init__(self, name, effectS):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 0
    def giveScore(self, app, p, i):
        if p == 1: 
            op = 0
            lastIndex = i
        else: 
            op = 1
            lastIndex = i - 1
        if lastIndex == -1:
            return (self.speedM, self.intM, self.pointM)
        speedM = app.cards[op][lastIndex].speedM
        intM = app.cards[op][lastIndex].intM
        pointM = app.cards[op][lastIndex].pointM
        self.speedM = speedM
        self.pointM = pointM
        self.intM = intM
        return (self.speedM, self.intM, self.pointM)



def appStarted(app):
    app.titleScreen = True
    app.highlight = 0
    app.pile = []
    app.p1turn = True
    app.cards = [[],[]]
    app.margin = 200
    app.cellmargin = 20
    laserBlaster = Weapon('Laser Blaster', '+5 if opponent does not have a laser blaster shield, otherwise +2 points', 'Laser Blaster Shield')
    buzzsaw = Weapon('Buzzsaw', '+5 if opponent does not have a buzzsaw shield, otherwise +2 points', 'Buzzsaw Shield')
    rocketLauncher = Weapon('Rocket Launcher', '+5 if opponent does not have a rocket launcher shield, otherwise +2 points', 'Rocket Launcher Shield')
    machineGun = Weapon('Machine Gun', '+5 if opponent does not have a machine gun shield, otherwise +2 points', 'Machine Gun Shield')
    explosivePizza = Weapon('Explosive Pizza', '+5 if opponent does not have a explosive pizza shield, otherwise +2 points', 'Explosive Pizza Shield')
    laserDog = Weapon('Laser Dog', '+5 if opponent does not have a laser dog shield, otherwise +2 points', 'Laser Dog Shield')
    laserBlasterShield = Shield('Laser Blaster Shield', '+5 if opponent has a laser blaster, otherwise +2 points', 'Laser Blaster')
    buzzsawShield = Shield('Buzzsaw Shield', '+5 if opponent has a buzzsaw, otherwise +2 points', 'Buzzsaw')
    rocketLauncherShield = Shield('Rocket Launcher Shield', '+5 if opponent has a rocket launcher, otherwise +2 points', 'Rocket Launcher')
    machineGunShield = Shield('Machine Gun Shield', '+5 if opponent has a machine gun, otherwise +2 points', 'Machine Gun')
    explosivePizzaShield = Shield('Explosive Pizza Shield', '+5 if opponent has an explosive pizza, otherwise +2 points', 'Explosive Pizza')
    laserDogShield = Shield('Laser Dog Shield', '+5 if opponent has a laser dog, otherwise +2 points', 'Laser Dog')
    defenseBoost1 = Boost('Defense Boost', '+2 Points for each shield you have', 's')
    defenseBoost2 = Boost('Defense Boost', '+2 Points for each shield you have', 's')
    attackBoost1 = Boost('Attack Boost', '+2 Points for each weapon you have', 'w')
    attackBoost2 = Boost('Attack Boost', '+2 Points for each weapon you have', 'w')
    jetpack1 = Card('Jetpack', '+2 Speed', 2, 0, 0)
    jetpack2 = Card('Jetpack', '+2 Speed', 2, 0, 0)
    rocketBoots1 = Card('Rocket Boots', '+3 Speed, -1 Intelligence', 3, -1, 0)
    rocketBoots2 = Card('Rocket Boots', '+3 Speed, -1 Intelligence', 3, -1, 0)
    neuralNetworks1 = Card('Neural Networks', '+2 Intelligence', 0, 2, 0)
    neuralNetworks2 = Card('Neural Networks', '+2 Intelligence', 0, 2, 0)
    minimaxAlgorithm1 = Card('Minimax Algorithm', '+3 Intelligence, -1 Speed', -1, 3, 0)
    minimaxAlgorithm2 = Card('Minimax Algorithm', '+3 Intelligence, -1 Speed', -1, 3, 0)
    armor1 = Card('Armor', '+3 Points', 0, 0, 3)
    armor2 = Card('Armor', '+3 Points', 0, 0, 3)
    stickyBoots1 = Card('Sticky Boots', '+4 Points, -1 Speed', -1, 0, 4)
    stickyBoots2 = Card('Sticky Boots', '+4 Points, -1 Speed', -1, 0, 4)
    quickProgramming1 = Card('Quick Programming', '-1 Intelligence, +4 Points', 0, -1, 4)
    quickProgramming2 = Card('Quick Programming', '-1 Intelligence, +4 Points', 0, -1, 4)
    Overclock = Card('Overclock', '+5 Points, -1 Speed, -1 Intelligence', -1, -1, 5)
    powerBoost = Card('Power Boost', '+1 Speed, +1 Intelligence, +1 Point', 1, 1, 1)
    extraArm1 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 2 arms)')
    extraArm2 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 2 arms)')
    extraArm3 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 2 arms)')
    extraArm4 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 2 arms)')
    extraArm5 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 2 arms)')
    counterPart1 = Copy('Counter Part', 'Copy the last played card')
    counterPart2 = Copy('Counter Part', 'Copy the last played card')
    counterPart3 = Copy('Counter Part', 'Copy the last played card')
    app.deck = [laserBlaster, buzzsaw, rocketLauncher, machineGun, explosivePizza, laserDog, laserBlasterShield, 
                buzzsawShield, rocketLauncherShield, machineGunShield, explosivePizzaShield, laserDogShield,
                defenseBoost1, defenseBoost2, attackBoost1, attackBoost2, jetpack1, jetpack2, rocketBoots1,
                rocketBoots2, neuralNetworks1, neuralNetworks2, minimaxAlgorithm1, minimaxAlgorithm2,
                armor1, armor2, stickyBoots1, stickyBoots2, quickProgramming1, quickProgramming2, 
                Overclock, powerBoost, extraArm1, extraArm2, extraArm3, extraArm4, extraArm5, counterPart1,
                counterPart2, counterPart3]
    app.image1 = app.loadImage('https://c.pxhere.com/photos/58/22/disposal_dump_garbage_junk_landfill_litter_pile_scrap_metal-1365482.jpg!d')
    app.image1 = app.scaleImage(app.image1, 1.5)
    #app.image2 = app.loadImage('https://www.clipartmax.com/png/middle/4-47442_transparent-arrow-clip-art-at-clker-arrow-clipart-transparent-background.png')
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
    app.waiting = False
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
        app.waiting = True
        app.time = time.time()
    calculateScore(app, 0)
    calculateScore(app, 1)
    if not app.waiting:
        for c in range(6):
            if isinstance(app.pile[c], Card):
                app.hrow = c // 3
                app.hcol = c % 3

def timerFired(app):
    if app.waiting:
        if time.time() - app.time > 1:
            moveI = generateMove(app)
            pickCard(app, moveI)
            app.waiting = False
            calculateScore(app, 0)
            calculateScore(app, 1)
            for c in range(6):
                if isinstance(app.pile[c], Card):
                    app.hrow = c // 3
                    app.hcol = c % 3


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
            #print(app.cards)
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
                app.cards[1].pop()
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
                app.cards[0].pop()
                #print(" "*depth,app.cards[0])

        #print(" "*depth,"mini=",mini)
        return mini

def calculateScore(app, p):
    if p == 1: op = 0
    else: op = 1
    app.score[p] = 0
    app.speed[p] = 0
    app.intel[p] = 0
    for i in range(len(app.cards[p])):
        speed, intel, score = app.cards[p][i].giveScore(app, p, i)
        app.speed[p] += speed
        app.intel[p] += intel
        app.score[p] += score


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
    if not app.waiting:
        if app.titleScreen:
            if event.key == "Up":
                if app.highlight != 0:
                    app.highlight -= 1
                else:
                    app.highlight = 3
            if event.key == "Down":
                if app.highlight != 3:
                    app.highlight += 1
                else:
                    app.highlight = 0
            if event.key == "Space":
                app.titleScreen = False
                app.gameMode = app.highlight
                if app.gameMode == 2:
                    app.maxDepth = 2
        else:
            if event.key == 'r' or (app.gameOver and event.key != 'Space'):
                appStarted(app)
            elif not app.gameOver:
                i = app.hcol + 3*app.hrow
                if event.key == "Up": 
                    if app.hrow != 0 and isinstance(app.pile[i - 3], Card):
                        app.hrow -= 1
                    elif (app.pile[0] == None and isinstance(app.pile[1], Card) and 
                    app.pile[2] == None and isinstance(app.pile[3], Card) and 
                    app.pile[4] == None and isinstance(app.pile[5], Card)):
                        app.hrow = 0
                        app.hcol = 1
                elif event.key == "Down":
                    if app.hrow != 1 and isinstance(app.pile[i + 3], Card):
                        app.hrow += 1
                    elif (app.pile[1] == None and isinstance(app.pile[0], Card) and 
                    app.pile[3] == None and isinstance(app.pile[2], Card) and 
                    app.pile[5] == None and isinstance(app.pile[4], Card)):
                        app.hrow = 1
                        app.hcol = 1
                elif event.key == "Left":
                    if app.hcol != 0:
                        if isinstance(app.pile[i - 1], Card):
                            app.hcol -= 1
                        else:
                            if (isinstance(app.pile[i - 2], Card) and i-2 >= 0 and 
                                app.hcol == 2):
                                app.hcol -= 2
                            else:
                                if app.hrow == 0:
                                    if isinstance(app.pile[i + 2], Card):
                                        app.hrow += 1
                                        app.hcol -= 1
                                    elif (isinstance(app.pile[i + 1], Card) and 
                                        app.hcol == 2):
                                        app.hrow += 1
                                        app.hcol -= 2
                                elif app.hrow == 1:
                                    if isinstance(app.pile[i - 4], Card):
                                        app.hrow -= 1
                                        app.hcol -= 1 
                                    elif (isinstance(app.pile[i - 5], Card) and 
                                        app.hcol == 2):
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
                                    elif (app.hcol == 0 and 
                                        isinstance(app.pile[i + 5], Card)):
                                        app.hrow += 1
                                        app.hcol += 2
                                elif app.hrow == 1:
                                    if isinstance(app.pile[i - 2], Card):
                                        app.hrow -= 1
                                        app.hcol += 1
                                    elif (isinstance(app.pile[i - 1], Card) and 
                                        app.hcol == 0):
                                        app.hrow -= 1
                                        app.hcol += 2
                elif event.key == 'Space':
                    pickCard(app, i)
                    

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
                card = app.pile[i]
                drawCard(app, canvas, x0, y0, x1, y1, outline, card)
    canvas.create_rectangle(50, 850, 950, 950, fill="white")
    if not app.waiting:
        i = app.hcol + 3*app.hrow
        h = app.pile[i].name
        d = app.pile[i].effectS
        canvas.create_text(app.width//2, 900, text=d, font="Times 30")
    else:
        canvas.create_text(app.width//2, 900, text="Thinking...", font="Times 30")

def drawCard(app, canvas, x0, y0, x1, y1, outline, card):
    canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=10, fill="white")
    canvas.create_rectangle(x0+10, y0+30, x1-10, y1-130)
    canvas.create_text((x1+x0)//2, y0 + 15, text=card.name)
    canvas.create_text((x1+x0)//2, y1 - 100, text=card.effectS)

def drawArrow(app, canvas, x, y, d):
    if d == 1:
        canvas.create_line(x - 30, y, x + 30, y, width=3)
        canvas.create_line(x + 10, y - 10, x + 30, y,  width=3)
        canvas.create_line(x + 10, y + 10, x + 30, y,  width=3)
    else:
        canvas.create_line(x - 30, y, x + 30, y, width=3)
        canvas.create_line(x - 10, y - 10, x - 30, y,  width=3)
        canvas.create_line(x - 10, y + 10, x - 30, y,  width=3)


def drawScores(app, canvas):
    canvas.create_text(app.width//2, 40, text="Score", font="Times 36 bold")
    canvas.create_text(app.width//2, 93, text="Speed", font="Times 36 bold")
    canvas.create_text(app.width//2, 150, text="Intelligence", font="Times 36 bold")
    canvas.create_text(app.width//2 + 200, 40, text=str(app.score[1]), font="Times 36 bold")
    canvas.create_text(app.width//2 + 200, 93, text=str(app.speed[1]), font="Times 36 bold")
    canvas.create_text(app.width//2 + 200, 150, text=str(app.intel[1]), font="Times 36 bold")
    canvas.create_text(app.width//2 - 200, 40, text=str(app.score[0]), font="Times 36 bold")
    canvas.create_text(app.width//2 - 200, 93, text=str(app.speed[0]), font="Times 36 bold")
    canvas.create_text(app.width//2 - 200, 150, text=str(app.intel[0]), font="Times 36 bold")
    if app.score[1] >= app.score[0]:
        drawArrow(app, canvas, app.width//2 + 140, 40, 1)
    if app.speed[1] >= app.speed[0]:
        drawArrow(app, canvas, app.width//2 + 140, 93, 1)
    if app.intel[1] >= app.intel[0]:
        drawArrow(app, canvas, app.width//2 + 140, 150, 1)
    if app.score[0] >= app.score[1]:
        drawArrow(app, canvas, app.width//2 - 140, 40, -1)
    if app.speed[0] >= app.speed[1]:
        drawArrow(app, canvas, app.width//2 - 140, 93, -1)
    if app.intel[0] >= app.intel[1]:
        drawArrow(app, canvas, app.width//2 - 140, 150, -1)
    Score0 = copy.copy(app.score[0])
    Score1 = copy.copy(app.score[1])
    if app.speed[0] > app.speed[1]:
        Score0 += 10
    elif app.speed[1] > app.speed[0]:
        Score1 += 10
    if app.intel[0] > app.intel[1]:
        Score0 += 10
    elif app.intel[1] > app.intel[0]:
        Score1 += 10
    canvas.create_text(100, 100, text=str(Score0), font="Times 100 bold")
    canvas.create_text(900, 100, text=str(Score1), font="Times 100 bold")

def drawPicks(app,canvas):
    if len(app.cards[0]) > 0:
        canvas.create_rectangle(20, 200, 180, 220 + 20*len(app.cards[0]), fill="white")
    if len(app.cards[1]) > 0:
        canvas.create_rectangle(820, 200, 980, 220 + 20*len(app.cards[1]), fill="white")
    for i in range(len(app.cards[0])):
        canvas.create_text(100, 200 + 20*(i+1), text=app.cards[0][i].name)
    for i in range(len(app.cards[1])):
        canvas.create_text(900, 200 + 20*(i+1), text=app.cards[1][i].name)
    

def drawTitleScreen(app, canvas):
    canvas.create_text(app.width//2, 170, text='Scrapyard Scramble', 
                        font="Times 100")
    modes = ["2 Player", "Easy", "Medium", "Hard"]
    for row in range(4):
        x = 130 * row
        if row == app.highlight:
            canvas.create_rectangle(app.width//2 - 180, app.height//2 - 180 + x,
             app.width//2 + 180, app.height//2 - 80 + x, width=5, outline='red', 
             fill="white")
        else:
            canvas.create_rectangle(app.width//2 - 180, app.height//2 - 180 + x,
            app.width//2 + 180, app.height//2 - 80 + x, width=5, fill="white")
        canvas.create_text(app.width//2, app.height//2 + x - 130, 
            text=modes[row], font="Times 30 bold")

def drawEnd(app, canvas):
    if app.titleScreen:
        drawTitleScreen(app, canvas)
    else:
        drawPicks(app,canvas)
        drawScores(app,canvas)
        if not app.gameOver:
            drawCards(app, canvas)
        else:
            if app.gameMode == 0:
                if app.winner == 'tie':
                    text = 'It is a tie!'
                else: 
                    text = f'Player {app.winner} Wins!'
                canvas.create_text(app.width//2, app.height//2, text=text, font="Times 50 bold", fill="white")
                canvas.create_text(app.width//2, app.height//2 + 50,
                             text="Press any key to return to the main menu", font="Times 50 bold", fill="white")
            else:
                if app.winner == 1:
                    canvas.create_text(app.width//2, app.height//2, text="You Win!", font="Times 50 bold", fill="white")
                    canvas.create_text(app.width//2, app.height//2 + 50,
                             text="Press any key to return to the main menu", font="Times 50 bold", fill="white")
                elif app.winner == 2:
                    canvas.create_text(app.width//2, app.height//2, text="You Lose. :(", font="Times 50 bold", fill="white")
                    canvas.create_text(app.width//2, app.height//2 + 50,
                             text="Press any key to return to the main menu", font="Times 50 bold", fill="white")
                else:
                    canvas.create_text(app.width//2, app.height//2, text="It is a tie!", font="Times 50 bold", fill="white")
                    canvas.create_text(app.width//2, app.height//2 + 50,
                             text="Press any key to return to the main menu", font="Times 50 bold", fill="white")
def redrawAll(app,canvas):
    canvas.create_image(500, 500, image=ImageTk.PhotoImage(app.image1)) 
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



