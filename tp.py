import random, math
# CITATION: I am using CMU 112 graphics framework from https://www.cs.cmu.edu/~112/notes/notes-graphics.html
from cmu_112_graphics import *
import copy
import time

#This is the main file for Scrapyard Scramble. Run this file.

class Card(object):
    def __init__(self, name, effectS, speedM, intM, pointM, image):
        self.name = name
        self.effectS = effectS
        self.speedM = speedM
        self.intM = intM
        self.pointM = pointM
        self.image = image
    def giveScore(self, app, player, i):
        return (self.speedM, self.intM, self.pointM)
    def __eq__(self, other):
        return isinstance(other, Card) and self.name == other.name
    def __repr__(self):
        return self.name
    
class Weapon(Card):
    def __init__(self, name, effectS, shieldName, image):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 0
        self.shieldName = shieldName
        self.image = image
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
    def __init__(self, name, effectS, weaponName, image):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 0
        self.weaponName = weaponName
        self.image = image
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
    def __init__(self, name, effectS, image):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 1
        self.image = image
    def giveScore(self, app, p, i):
        self.pointM = 1
        for card in app.cards[p]:
            if card.name == self.name: 
                self.pointM += 1
        return (self.speedM, self.intM, self.pointM)

class Boost(Card):
    def __init__(self, name, effectS, type, image):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 0
        self.type = type
        self.image = image
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
    def __init__(self, name, effectS, image):
        self.name = name
        self.effectS = effectS
        self.speedM = 0
        self.intM = 0
        self.pointM = 0
        self.image = image
    def giveScore(self, app, p, i):
        try:
            if not app.givingHint:
                if p == 1: 
                    op = 0
                    lastIndex = i
                else: 
                    op = 1
                    lastIndex = i - 1
            else:
                if p == 1: 
                    op = 0
                    lastIndex = i - 1
                else: 
                    op = 1
                    lastIndex = i
            if lastIndex == -1:
                return (self.speedM, self.intM, self.pointM)
            speedM = app.cards[op][lastIndex].speedM
            intM = app.cards[op][lastIndex].intM
            pointM = app.cards[op][lastIndex].pointM
            self.speedM = speedM
            self.pointM = pointM
            self.intM = intM
        except:
            self.speedM = 0
            self.pointM = 0
            self.intM = 0
        return (self.speedM, self.intM, self.pointM)

def appStarted(app):
    app.seenRules = False
    appStartedHelper(app)

def appStartedHelper(app):
    app.titleScreen = True
    app.highlight = 0
    app.pile = []
    app.p1turn = True
    app.cards = [[],[]]
    app.margin = 200
    app.cellmargin = 20
    #Citation: https://image.freepik.com/free-vector/cartoon-robot-guards-human-exoskeleton-armor_1441-2671.jpg
    app.armorImage = app.loadImage("images/Armor.png")
    #Citation: https://pngio.com/images/png-a1920880.html
    app.attackBoostImage = app.loadImage("images/AttackBoost.png")
    #Citation: https://www.deviantart.com/venjix5/art/Spinner-N-Bot-Buzzsaw-754401368
    app.buzzsawImage = app.loadImage("images/Buzzsaw.png")
    #Citation: https://cdn0.iconfinder.com/data/icons/communication-and-multimedia/48/communication_and_multimedia_flat_icons-10-512.png
    app.buzzsawShieldImage = app.loadImage("images/BuzzsawShield.png")
    #Citation: https://thumbs.dreamstime.com/z/robot-pointing-finger-cartoon-191439876.jpg
    app.counterPartImage = app.loadImage("images/CounterPart.png")
    #Citation: https://pngio.com/images/png-a1920880.html
    app.defenseBoostImage = app.loadImage("images/DefenseBoost.png")
    #Citation: https://image.shutterstock.com/image-vector/cartoon-boom-comic-book-explosion-260nw-84002389.jpg and https://image.shutterstock.com/image-vector/pizzaflat-coloring-styleillustration-children-260nw-761800429.jpg
    app.explosivePizzaImage = app.loadImage("images/ExplosivePizza.png")
    #Citation: https://cdn0.iconfinder.com/data/icons/communication-and-multimedia/48/communication_and_multimedia_flat_icons-10-512.png
    app.explosivePizzaShieldImage = app.loadImage("images/ExplosivePizzaShield.png")
    #Citation: https://cdn1.vectorstock.com/i/1000x1000/24/55/comic-cartoon-robot-arm-vector-6802455.jpg
    app.extraArmImage = app.loadImage("images/ExtraArm.png")
    #Citation: https://image.shutterstock.com/image-vector/cartoon-rocket-pack-260nw-124043488.jpg and https://www.cleanpng.com/png-robotics-clip-art-robot-cliparts-black-191716/preview.html
    app.jetpackImage = app.loadImage("images/Jetpack.png")
    #Citation: https://cdn0.iconfinder.com/data/icons/communication-and-multimedia/48/communication_and_multimedia_flat_icons-10-512.png
    app.laserBlasterShieldImage = app.loadImage("images/LaserBlasterShield.png")
    #Citation: https://pixers.us/posters/retro-laser-gun-or-raygun-vector-illustration-15810779
    app.laserBlasterImage = app.loadImage("images/LaserBlaster.png")
    #Citation: https://www.jamiesale-cartoonist.com/wp-content/uploads/dog-12.png and 
    app.laserDogImage = app.loadImage("images/LaserDog.png")
    #Citation: https://cdn0.iconfinder.com/data/icons/communication-and-multimedia/48/communication_and_multimedia_flat_icons-10-512.png
    app.laserDogShieldImage = app.loadImage("images/LaserDogShield.png")
    #Citation: https://p.kindpng.com/picc/s/55-557274_free-to-use-public-domain-guns-clip-art.png
    app.machineGunImage = app.loadImage("images/MachineGun.png")
    #Citation: https://cdn0.iconfinder.com/data/icons/communication-and-multimedia/48/communication_and_multimedia_flat_icons-10-512.png
    app.machineGunShieldImage = app.loadImage("images/MachineGunShield.png")
    #Citation: https://media.geeksforgeeks.org/wp-content/uploads/minmax.png
    app.minimaxAlgorithmImage = app.loadImage("images/MinimaxAlgorithm.png")
    #Citation: https://lh3.googleusercontent.com/proxy/63VqxYMIIlPbTNmMbHC8DA4oN5xKiEy-oXnKcJ7Q9QIUTTz5Sh7iLjMw2gNg8co7-Pr1mt1qNlYhOFmTqyk3sB1gmqq3xiEqdADihByDCtx73EslzMsPYuXb-jIwHykJSHo-eC9Gd3EFdiM2XKXIzU4kM6ucCgd6
    app.neuralNetworkImage = app.loadImage("images/NeuralNetwork.png")
    #Citation: https://smallimg.pngkey.com/png/small/522-5224285_-soloveika-computer-clipart.png and https://lh3.googleusercontent.com/proxy/YtomkqZNE4YrWwWZbng8pN0Sv6NxrILYtjMpbO5YdQpjm2qOg4MNJeSphHbgox_rbcxbJrbVhBFPbQCkCkSz6h2w_fbSjHykb7ZERqKIkqoVvuiwpSSrJ-eC78NbYezVdAYURSHRXBl71X0
    app.overclockImage = app.loadImage("images/Overclock.png")
    #Citation: https://www.istockphoto.com/illustrations/power-plug
    app.powerBoostImage = app.loadImage("images/PowerBoost.png")
    #Citation: http://clipart-library.com/computer-programmer-cliparts.html
    app.quickProgrammingImage = app.loadImage("images/QuickProgramming.png")
    #Citation: https://rocket-boots.github.io/rocket-boots/images/boots1_flat_300.png
    app.rocketBootsImage = app.loadImage("images/RocketBoots.png")
    #Citation: https://www.iconfinder.com/icons/4093446/battle_launcher_military_rocket_war_weapon_icon
    app.rocketLauncherImage = app.loadImage("images/RocketLauncher.png")
    #Citation: https://www.iconfinder.com/icons/4093446/battle_launcher_military_rocket_war_weapon_icon
    app.rocketLauncherShieldImage = app.loadImage("images/rocketLauncherShield.png")
    #Citation: https://www.clipartkey.com/mpngs/m/13-133416_clip-art-hiking-boots-clipart-hiking-boot-clip.png and https://www.iconspng.com/image/97727/shiny-slime
    app.stickyBootsImage = app.loadImage("images/StickyBoots.png")
    laserBlaster = Weapon('Laser Blaster', '+5 points if opponent does not have a Laser Blaster Shield, otherwise +2 points', 'Laser Blaster Shield', app.laserBlasterImage)
    buzzsaw = Weapon('Buzzsaw', '+5 points if opponent does not have a Buzzsaw Shield, otherwise +2 points', 'Buzzsaw Shield', app.buzzsawImage)
    rocketLauncher = Weapon('Rocket Launcher', '+5 points if opponent does not have a Rocket Launcher Shield, otherwise +2 points', 'Rocket Launcher Shield', app.rocketLauncherImage)
    machineGun = Weapon('Machine Gun', '+5 points if opponent does not have a Machine Gun Shield, otherwise +2 points', 'Machine Gun Shield', app.machineGunImage)
    explosivePizza = Weapon('Explosive Pizza', '+5 points if opponent does not have a Explosive Pizza Shield, otherwise +2 points', 'Explosive Pizza Shield', app.explosivePizzaImage)
    laserDog = Weapon('Laser Dog', '+5 points if opponent does not have a Laser Dog Dhield, otherwise +2 points', 'Laser Dog Shield', app.laserDogImage)
    laserBlasterShield = Shield('Laser Blaster Shield', '+5 points if opponent has a Laser Blaster, otherwise +2 points', 'Laser Blaster', app.laserBlasterShieldImage)
    buzzsawShield = Shield('Buzzsaw Shield', '+5 points if opponent has a Buzzsaw, otherwise +2 points', 'Buzzsaw', app.buzzsawShieldImage)
    rocketLauncherShield = Shield('Rocket Launcher Shield', '+5 points if opponent has a rocket launcher, otherwise +2 points', 'Rocket Launcher', app.rocketLauncherShieldImage)
    machineGunShield = Shield('Machine Gun Shield', '+5 points if opponent has a machine gun, otherwise +2 points', 'Machine Gun', app.machineGunShieldImage)
    explosivePizzaShield = Shield('Explosive Pizza Shield', '+5 points if opponent has an explosive pizza, otherwise +2 points', 'Explosive Pizza', app.explosivePizzaShieldImage)
    laserDogShield = Shield('Laser Dog Shield', '+5 points if opponent has a laser dog, otherwise +2 points', 'Laser Dog', app.laserDogShieldImage)
    defenseBoost1 = Boost('Defense Boost', '+2 Points for each shield you have', 's', app.defenseBoostImage)
    defenseBoost2 = Boost('Defense Boost', '+2 Points for each shield you have', 's', app.defenseBoostImage)
    attackBoost1 = Boost('Attack Boost', '+2 Points for each weapon you have', 'w', app.attackBoostImage)
    attackBoost2 = Boost('Attack Boost', '+2 Points for each weapon you have', 'w', app.attackBoostImage)
    jetpack1 = Card('Jetpack', '+2 Speed', 2, 0, 0, app.jetpackImage)
    jetpack2 = Card('Jetpack', '+2 Speed', 2, 0, 0, app.jetpackImage)
    rocketBoots1 = Card('Rocket Boots', '+3 Speed and -1 Intelligence', 3, -1, 0, app.rocketBootsImage)
    rocketBoots2 = Card('Rocket Boots', '+3 Speed and -1 Intelligence', 3, -1, 0, app.rocketBootsImage)
    neuralNetworks1 = Card('Neural Networks', '+2 Intelligence', 0, 2, 0, app.neuralNetworkImage)
    neuralNetworks2 = Card('Neural Networks', '+2 Intelligence', 0, 2, 0, app.neuralNetworkImage)
    minimaxAlgorithm1 = Card('Minimax Algorithm', '+3 Intelligence and -1 Speed', -1, 3, 0, app.minimaxAlgorithmImage)
    minimaxAlgorithm2 = Card('Minimax Algorithm', '+3 Intelligence and -1 Speed', -1, 3, 0, app.minimaxAlgorithmImage)
    armor1 = Card('Armor', '+3 Points', 0, 0, 3, app.armorImage)
    armor2 = Card('Armor', '+3 Points', 0, 0, 3, app.armorImage)
    stickyBoots1 = Card('Sticky Boots', '+4 Points and -1 Speed', -1, 0, 4, app.stickyBootsImage)
    stickyBoots2 = Card('Sticky Boots', '+4 Points and -1 Speed', -1, 0, 4, app.stickyBootsImage)
    quickProgramming1 = Card('Quick Programming', '-1 Intelligence and +4 Points', 0, -1, 4, app.quickProgrammingImage)
    quickProgramming2 = Card('Quick Programming', '-1 Intelligence and +4 Points', 0, -1, 4, app.quickProgrammingImage)
    Overclock = Card('Overclock', '+5 Points, -1 Speed, and -1 Intelligence', -1, -1, 5, app.overclockImage)
    powerBoost = Card('Power Boost', '+1 Speed, +1 Intelligence, and +1 Point', 1, 1, 1, app.powerBoostImage)
    extraArm1 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 1 arm)', app.extraArmImage)
    extraArm2 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 1 arm)', app.extraArmImage)
    extraArm3 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 1 arm)', app.extraArmImage)
    extraArm4 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 1 arm)', app.extraArmImage)
    extraArm5 = Arm('Extra Arm', '+1 Point for each arm you have (you start with 1 arm)', app.extraArmImage)
    counterPart1 = Copy('Counter Part', 'Gain the Points, Speed, and Intelligence of the last played card', app.counterPartImage)
    counterPart2 = Copy('Counter Part', 'Gain the Points, Speed, and Intelligence of the last played card', app.counterPartImage)
    counterPart3 = Copy('Counter Part', 'Gain the Points, Speed, and Intelligence of the last played card', app.counterPartImage)
    app.deck = [laserBlaster, buzzsaw, rocketLauncher, machineGun, explosivePizza, laserDog, laserBlasterShield, 
                buzzsawShield, rocketLauncherShield, machineGunShield, explosivePizzaShield, laserDogShield,
                defenseBoost1, defenseBoost2, attackBoost1, attackBoost2, jetpack1, jetpack2, rocketBoots1,
                rocketBoots2, neuralNetworks1, neuralNetworks2, minimaxAlgorithm1, minimaxAlgorithm2,
                armor1, armor2, stickyBoots1, stickyBoots2, quickProgramming1, quickProgramming2, 
                Overclock, powerBoost, extraArm1, extraArm2, extraArm3, extraArm4, extraArm5, counterPart1,
                counterPart2, counterPart3]
    app.image1 = app.loadImage('https://c.pxhere.com/photos/58/22/disposal_dump_garbage_junk_landfill_litter_pile_scrap_metal-1365482.jpg!d')
    app.image1 = app.scaleImage(app.image1, 1.5)
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
    app.timer = False
    app.p1time = 180
    app.p2time = 180
    app.packCounter = 0
    app.time1 = time.time()
    app.givingHint = False
    app.hint = None
    app.rulesScreen = False
    app.card1 = None
    app.card2 = None
    app.time2 = 0
    app.finalScore = [0, 0]
    app.scoreModifiers = [0, 0]
    app.speedModifiers = [0, 0]
    app.intelModifiers = [0, 0]
    app.finalScoreModifiers = [0, 0]
    #0 is 2 player, 1 is random, 2 is minimax with max depth 2, 3 is minimax with full depth
    newPile(app)
    calculateModifiers(app)

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
    app.hint = None
    if not app.waiting:
        for c in range(6):
            if isinstance(app.pile[c], Card):
                app.hrow = c // 3
                app.hcol = c % 3
                calculateModifiers(app)

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
                    calculateModifiers(app)
    if app.timer and not app.titleScreen and not app.rulesScreen:
        if app.p1time <= 0:
            app.gameOver = True
            app.winner = 2
        elif app.p2time <= 0:
            app.gameOver = True
            app.winner = 1
        elif app.p1turn:
            app.p1time -= (time.time() - app.time1)
            app.time1 = time.time()
        else:
            app.p2time -= (time.time() - app.time1)
            app.time1 = time.time()
    if app.rulesScreen:
        if time.time() - app.time2 > 2:
            app.time2 = time.time()
            rand1 = random.randint(0, 33)
            card1 = app.deck[rand1]
            while True:
                rand2 = random.randint(0, 33)
                card2 = app.deck[rand2]
                if card1.name != card2.name:
                    break
            app.card1 = card1
            app.card2 = card2

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
    x , move = minimaxHelper(app, 1, 0)
    app.pile = pile
    app.cards = cards
    calculateScore(app, 0)
    calculateScore(app, 1)
    return move

# CITATION: Minimax algorithm inspired by one from the Game AI mini-lecture on 11/5/20   
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
        if turn == 1: 
            return (app.score[1] - app.score[0], 0)
        else: 
            return app.score[1] - app.score[0]
    elif turn == 1:
        maxi = -100
        move = None
        for i in range(len(app.pile)):
            if app.pile[i] != None:
                temp = copy.copy(app.pile[i])
                app.cards[1] += [temp]
                app.pile[i] = None
                result = minimaxHelper(app, 0, depth + 1)
                if result > maxi:
                    maxi = result
                    move = i
                app.pile[i] = temp
                app.cards[1].pop()
        return (maxi, move)
    else:
        mini = 100
        for i in range(len(app.pile)):
            if app.pile[i] != None:
                temp = copy.copy(app.pile[i])
                app.cards[0] = app.cards[0] + [temp]
                app.pile[i] = None
                score, move = minimaxHelper(app, 1, depth + 1)
                if score < mini:
                    mini = score
                app.pile[i] = temp
                app.cards[0].pop()
        return mini

def giveHint(app):
    if app.p1turn and app.gameMode > 0:
        app.givingHint = True
        pile = copy.deepcopy(app.pile)
        cards = copy.deepcopy(app.cards)
        app.cards = [app.cards[1], app.cards[0]]
        x, move = minimaxHelper(app, 1, 0)
        app.pile = pile
        app.cards = cards
        app.givingHint = False
        calculateScore(app, 0)
        calculateScore(app, 1)
        app.hint = move


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
    calculateFinalScore(app)

def calculateFinalScore(app):
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
    app.finalScore = (Score0, Score1)

def endGame(app):
    app.gameOver = True
    calculateFinalScore(app)
    calculateScore(app, 0)
    calculateScore(app, 1)
    if app.finalScore[0] > app.finalScore[1]:
        app.winner = 1
    elif app.finalScore[1] > app.finalScore[0]:
        app.winner = 2
    else:
        app.winner = 'tie'


def keyPressed(app, event):
    if not app.waiting:
        if app.rulesScreen:
            app.rulesScreen = False
            app.time1 = time.time()
        elif app.titleScreen:
            if event.key == "Up":
                if app.highlight != 0:
                    app.highlight -= 1
                else:
                    app.highlight = 4
            if event.key == "Down":
                if app.highlight != 4:
                    app.highlight += 1
                else:
                    app.highlight = 0
            if event.key == "Space":
                if app.highlight == 4:
                    app.timer = True
                else:
                    app.titleScreen = False
                    if app.seenRules:
                        app.rulesScreen = False
                        app.time1 = time.time()
                    else:
                        app.rulesScreen = True
                        app.seenRules = True
                        app.time2 = time.time() - 2
                    app.gameMode = app.highlight
                    if app.gameMode == 2:
                        app.maxDepth = 2
        else:
            if event.key == 'r' or app.gameOver:
                appStartedHelper(app)
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
                    calculateModifiers(app)
                elif event.key == "Down":
                    if app.hrow != 1 and isinstance(app.pile[i + 3], Card):
                        app.hrow += 1
                    elif (app.pile[1] == None and isinstance(app.pile[0], Card) and 
                    app.pile[3] == None and isinstance(app.pile[2], Card) and 
                    app.pile[5] == None and isinstance(app.pile[4], Card)):
                        app.hrow = 1
                        app.hcol = 1
                    calculateModifiers(app)
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
                    calculateModifiers(app)
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
                    calculateModifiers(app)
                elif event.key == 'Space':
                    pickCard(app, i)
                elif event.key == 'h':
                    giveHint(app)
                elif event.key == '1':
                    app.gameMode = 1
                elif event.key == '2':
                    app.gameMode = 2
                    app.maxDepth = 100
                elif event.key == '3':
                    app.gameMode = 2
                    app.maxDepth = 2

def calculateModifiers(app):
    score = copy.copy(app.score)
    speed = copy.copy(app.speed)
    intel = copy.copy(app.intel)
    finalScore = copy.copy(app.finalScore)
    i = app.hcol + 3*app.hrow
    if app.pile[i] != None:
        if app.p1turn: 
            p = 0
        else:
            p = 1
        app.cards[p] = app.cards[p] + [app.pile[i]]
        calculateScore(app, 0)
        calculateScore(app, 1)
        app.scoreModifiers = [app.score[0] - score[0], app.score[1] - score[1]]
        app.speedModifiers = [app.speed[0] - speed[0], app.speed[1] - speed[1]]
        app.intelModifiers = [app.intel[0] - intel[0], app.intel[1] - intel[1]]
        app.finalScoreModifiers = [app.finalScore[0] - finalScore[0], app.finalScore[1] - finalScore[1]]
        app.cards[p].pop()
        calculateScore(app, 0)
        calculateScore(app, 1)

def newPile(app):
    app.pile = []
    for c in range(6):
        i = random.randint(0, len(app.deck)-1)
        app.pile += [app.deck.pop(i)]
    app.packCounter += 1

#Citation: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html with minor changes to space out cards
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

def drawCardModifiers(app, canvas):
        if app.scoreModifiers[0] > 0:
            canvas.create_text(250, 40, text=f'+{app.scoreModifiers[0]}', fill="red", font="Times 20")
        elif app.scoreModifiers[0] < 0:
            canvas.create_text(250, 40, text=f'{app.scoreModifiers[0]}', fill="red", font="Times 20")
        if app.speedModifiers[0] > 0:
            canvas.create_text(250, 93, text=f'+{app.speedModifiers[0]}', fill="red", font="Times 20")
        elif app.speedModifiers[0] < 0:
            canvas.create_text(250, 93, text=f'{app.speedModifiers[0]}', fill="red", font="Times 20")
        if app.intelModifiers[0] > 0:
            canvas.create_text(250, 150, text=f'+{app.intelModifiers[0]}', fill="red", font="Times 20")
        elif app.intelModifiers[0] < 0:
            canvas.create_text(250, 150, text=f'{app.intelModifiers[0]}', fill="red", font="Times 20")
        if app.scoreModifiers[1] > 0:
            canvas.create_text(750, 40, text=f'+{app.scoreModifiers[1]}', fill="red", font="Times 20")
        elif app.scoreModifiers[1] < 0:
            canvas.create_text(750, 40, text=f'{app.scoreModifiers[1]}', fill="red", font="Times 20")
        if app.speedModifiers[1] > 0:
            canvas.create_text(750, 93, text=f'+{app.speedModifiers[1]}', fill="red", font="Times 20")
        elif app.speedModifiers[1] < 0:
            canvas.create_text(750, 93, text=f'{app.speedModifiers[1]}', fill="red", font="Times 20")
        if app.intelModifiers[1] > 0:
            canvas.create_text(750, 150, text=f'+{app.intelModifiers[1]}', fill="red", font="Times 20")
        elif app.intelModifiers[1] < 0:
            canvas.create_text(750, 150, text=f'{app.intelModifiers[1]}', fill="red", font="Times 20")
        
        if app.finalScoreModifiers[0] >= 0:
            canvas.create_text(190, 100, text=f'+{app.finalScoreModifiers[0]}', fill="red", font="Times 30")
        elif app.finalScoreModifiers[0] < 0:
            canvas.create_text(190, 100, text=f'{app.finalScoreModifiers[0]}', fill="red", font="Times 30")

        if app.finalScoreModifiers[1] >= 0:
            canvas.create_text(810, 100, text=f'+{app.finalScoreModifiers[1]}', fill="red", font="Times 30")
        elif app.finalScoreModifiers[1] < 0:
            canvas.create_text(810, 100, text=f'{app.finalScoreModifiers[1]}', fill="red", font="Times 30")


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
    canvas.create_rectangle(10, 850, 990, 950, fill="white")
    canvas.create_rectangle(400, 790, 600, 840, fill="white")
    if not app.waiting:
        i = app.hcol + 3*app.hrow
        h = app.pile[i].name
        d = app.pile[i].effectS
        canvas.create_text(app.width//2, 900, text=d, font="Times 30")
        canvas.create_text(app.width//2, 815, text=f'Pile {app.packCounter}/6', font="Times 30", fill="black")
    else:
        canvas.create_text(app.width//2, 815, text=f'Pile {app.packCounter}/6', font="Times 30", fill="black")
        canvas.create_text(app.width//2, 900, text="Thinking...", font="Times 30")

def drawCard(app, canvas, x0, y0, x1, y1, outline, card):
    canvas.create_rectangle(x0, y0, x1, y1, outline=outline, width=10, fill="white")
    a, b, c, d = x0+10, y0+35, x1-10, y1-130
    canvas.create_rectangle(a-1, b-1, c, d)
    canvas.create_text((x1+x0)//2, y0 + 20, text=card.name, font="Arial 14 bold")
    canvas.create_text((x1+x0)//2, y1 - 80, text=card.effectS, width=150, justify="center", font="Arial 16")
    canvas.create_image((a + (c-a)//2), b + ((d-b)//2), image=ImageTk.PhotoImage(card.image)) 

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
    drawCardModifiers(app, canvas)
    canvas.create_text(app.width//2, 40, text="Score", font="Times 36 bold")
    canvas.create_text(app.width//2, 93, text="Speed", font="Times 36 bold")
    canvas.create_text(app.width//2, 150, text="Intelligence", font="Times 36 bold")
    canvas.create_text(app.width//2 + 200, 40, text=str(app.score[1]), font="Times 36 bold")
    canvas.create_text(app.width//2 + 200, 93, text=str(app.speed[1]), font="Times 36 bold")
    canvas.create_text(app.width//2 + 200, 150, text=str(app.intel[1]), font="Times 36 bold")
    canvas.create_text(app.width//2 - 200, 40, text=str(app.score[0]), font="Times 36 bold")
    canvas.create_text(app.width//2 - 200, 93, text=str(app.speed[0]), font="Times 36 bold")
    canvas.create_text(app.width//2 - 200, 150, text=str(app.intel[0]), font="Times 36 bold")
    if app.score[1] > app.score[0]:
        drawArrow(app, canvas, app.width//2 + 140, 40, 1)
    if app.speed[1] > app.speed[0]:
        drawArrow(app, canvas, app.width//2 + 140, 93, 1)
    if app.intel[1] > app.intel[0]:
        drawArrow(app, canvas, app.width//2 + 140, 150, 1)
    if app.score[0] > app.score[1]:
        drawArrow(app, canvas, app.width//2 - 140, 40, -1)
    if app.speed[0] > app.speed[1]:
        drawArrow(app, canvas, app.width//2 - 140, 93, -1)
    if app.intel[0] > app.intel[1]:
        drawArrow(app, canvas, app.width//2 - 140, 150, -1)
    canvas.create_text(100, 100, text=str(app.finalScore[0]), font="Times 100 bold")
    canvas.create_text(900, 100, text=str(app.finalScore[1]), font="Times 100 bold")

def drawPicks(app,canvas):
    if len(app.cards[0]) > 0:
        canvas.create_rectangle(20, 200, 180, 220 + 20*len(app.cards[0]), fill="white")
    if len(app.cards[1]) > 0:
        canvas.create_rectangle(820, 200, 980, 220 + 20*len(app.cards[1]), fill="white")
    for i in range(len(app.cards[0])):
        canvas.create_text(100, 200 + 20*(i+1), text=app.cards[0][i].name)
    for i in range(len(app.cards[1])):
        canvas.create_text(900, 200 + 20*(i+1), text=app.cards[1][i].name)

def drawHint(app, canvas):
    if app.gameMode > 0:
        canvas.create_rectangle(30, 520, 170, 680, fill="white")
        canvas.create_text(100, 550, text="Press h for a hint!", font="Arial 20", width="100", justify="center", fill="black")
        if app.hint != None:
            card = app.pile[app.hint]
            canvas.create_text(100, 620, text=f"Pick {card.name}!", font="Arial 20", width="100", justify="center", fill="black")
    else:
        if app.p1turn: p=1
        else: p=2
        canvas.create_rectangle(30, 540, 170, 620, fill="white")
        canvas.create_text(100, 580, text=f"Player {p}'s turn", font="Arial 20", width="100", justify="center", fill="black")
    
def drawTimer(app, canvas):
    if app.timer:
        canvas.create_oval(50, 700, 150, 800, fill="white")
        canvas.create_oval(850, 700, 950, 800, fill="white")
        if int(app.p1time)%60 < 10:
            p1time = f'{int(app.p1time//60)}:0{int(app.p1time)%60}'
        else:
            p1time = f'{int(app.p1time//60)}:{int(app.p1time)%60}'
        if int(app.p2time)%60 < 10:
            p2time = f'{int(app.p2time//60)}:0{int(app.p2time)%60}'
        else:
            p2time = f'{int(app.p2time//60)}:{int(app.p2time)%60}'
        if app.p1time < 60:
            canvas.create_text(100, 750, text=p1time, font="Times 38 bold", fill="red")
        else:
            canvas.create_text(100, 750, text=p1time, font="Times 38 bold", fill="black")
        if app.p2time < 60:
            canvas.create_text(900, 750, text=p2time, font="Times 38 bold", fill="red")
        else:
            canvas.create_text(900, 750, text=p2time, font="Times 38 bold", fill="black")

def drawTitleScreen(app, canvas):
    canvas.create_text(app.width//2, 100, text='Scrapyard Scramble', 
                        font="Times 100")
    canvas.create_text(app.width//2, 190, text='By Jack Kiefer', 
                        font="Times 30")      
    canvas.create_text(app.width//2, 270, text='Choose a Game Mode:', 
                        font="Times 50")     
    if app.timer:
        modes = ["2 Player", "Easy", "Medium", "Hard", "Timer: On"]
    else:
        modes = ["2 Player", "Easy", "Medium", "Hard", "Timer: Off"]
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
    if app.highlight == 4:
        outline = "red"
    else:
        outline = "black"
    canvas.create_rectangle(app.width//2 - 100, app.height//2 + 360,
             app.width//2 + 100, app.height//2 + 420, width=5, outline=outline, fill="white")
    canvas.create_text(app.width//2 , app.height//2 + 390, text = modes[4], font="Times 22 bold")
    canvas.create_rectangle(700, 600, 950, 770, fill="white")
    canvas.create_text(825, 630, text="Controls:", font="Times 26 bold")
    canvas.create_text(825, 700, text="Use arrow keys to move highlighted box and press space to select a card.", 
                                font="Times 23", width=225, justify="center")

def drawRulesScreen(app, canvas):
    canvas.create_rectangle(100, 100, 900, 900, fill="white")
    x = 650
    y = 150
    if app.card1 != None:
        drawCard(app, canvas, x, y, x + 180, y + 280, "black", app.card1)
    x = 650
    y = 500
    if app.card2 != None:
        drawCard(app, canvas, x, y, x + 180, y + 280, "black", app.card2)
    canvas.create_text(380, 150, text ="Rules", font="Times 60 bold")
    canvas.create_line(150, 200, 600, 200, width=3)
    canvas.create_text(125, 300, text ='- Players alternate picking cards from 6-card "Scrap Piles" and the last card from each pile is discarded.', font="Times 38", anchor="w", width=500)
    canvas.create_text(125, 465, text ='- The object of the game is to have the most points after 6 "Scrap Piles."', font="Times 38", anchor="w", width=500)
    canvas.create_text(125, 650, text ="- At the end of the game the player with the most Speed gets 10 points. The same goes for the player with the most Intelligence.", font="Times 38", anchor="w", width=500)
    canvas.create_text(140, 800, text ='[Press any key to continue]', font="Times 38", anchor="w", width=500)

def drawEnd(app, canvas):
    if app.rulesScreen:
        drawRulesScreen(app, canvas)
    elif app.titleScreen:
        drawTitleScreen(app, canvas)
    else:
        drawScores(app,canvas)
        if not app.gameOver:
            drawPicks(app,canvas)
            drawCards(app, canvas)
            drawTimer(app,canvas)
            drawHint(app, canvas)
        else:
            canvas.create_rectangle(150, 300, 850, 900, fill = "white")
            if app.gameMode == 0:
                if app.winner == 'tie':
                    text = 'It is a tie!'
                else: 
                    text = f'Player {app.winner} Wins!'
                canvas.create_text(app.width//2, app.height//2, text=text, font="Times 50 bold", fill="black")
                canvas.create_text(app.width//2, app.height//2 + 250, width="600", justify="center",
                             text="[Press any key to return to the main menu]", font="Times 50 bold", fill="black")
            else:
                if app.winner == 1:
                    canvas.create_text(app.width//2, app.height//2, text="You Win!", font="Times 50 bold", fill="black")
                    canvas.create_text(app.width//2, app.height//2 + 250, width="600", justify="center",
                             text="[Press any key to return to the main menu]", font="Times 50 bold", fill="black")
                elif app.winner == 2:
                    canvas.create_text(app.width//2, app.height//2, text="You Lose. :(", font="Times 50 bold", fill="black")
                    canvas.create_text(app.width//2, app.height//2 + 150, width="600",justify="center",
                             text="[Press any key to return to the main menu]", font="Times 50 bold", fill="black")
                else:
                    canvas.create_text(app.width//2, app.height//2, text="It is a tie!", font="Times 50 bold", fill="black")
                    canvas.create_text(app.width//2, app.height//2 + 150, width="600",justify="center",
                             text="[Press any key to return to the main menu]", font="Times 50 bold", fill="black")
def redrawAll(app,canvas):
    canvas.create_image(500, 500, image=ImageTk.PhotoImage(app.image1)) 
    drawEnd(app, canvas)


#Citation: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html 
def playGame():
    width = 1000
    height = 1000
    runApp(width=width, height=height)


def main():
    playGame()

if __name__ == '__main__':
    main()



