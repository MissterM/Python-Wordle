import json
import pygame
import random
import urllib.request

# English 5-letter words
wordlist = []
word_site = "https://raw.githubusercontent.com/charlesreid1/five-letter-words/master/sgb-words.txt"
response = urllib.request.urlopen(word_site)
txt = response.read()
WORDS = txt.splitlines()
for x in WORDS:
    wordlist.append(x.decode())

# Letters coordinate on the keyboard
letternum = {"q": (0, 0), "w": (1, 0), "e": (2, 0), "r": (3, 0), "t": (4, 0), "y": (5, 0), "u": (6, 0), "i": (7, 0),
             "o": (8, 0), "p": (9, 0), "a": (0, 1), "s": (1, 1), "d": (2, 1), "f": (3, 1), "g": (4, 1), "h": (5, 1),
             "j": (6, 1), "k": (7, 1), "l": (8, 1), "z": (0, 2), "x": (1, 2), "c": (2, 2), "v": (3, 2), "b": (4, 2),
             "n": (5, 2), "m": (6, 2)
             }

rectangles = []  # Just for developer to know buttons coordinate
tablex = 0  # x of the current grid position
tabley = 0  # y of the current grid position
pword = ""  # Player word
endofthegame = False  # Whether is end of the game
menu = False  # Whether player is in menu
ranword = random.choice(wordlist)  # Word to guess
repeatletters = []  # Letters which position player already guessed


# Pygame config
WIDTH, HEIGHT = 1200, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")
pygame.init()

# Colors
GRAY = (30, 30, 30)
LIGHT_GRAY = (100, 100, 100)
VERY_LIGHT_GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
YELLOW = (150, 130, 23)
GREEN = (33, 85, 31)
BLACK = (23, 23, 24)
RED = (180, 20, 20)

# Fonts
my_font = pygame.font.SysFont("Comic Sans MS", 50)
my_font2 = pygame.font.SysFont("Comic Sans MS", 17)
my_font3 = pygame.font.SysFont("Comic Sans MS", 30)
font2 = pygame.font.SysFont("Helvetica Neue", 25, bold=True)
font3 = pygame.font.SysFont("Helvetica Neue", 22, bold=True)
font4 = pygame.font.SysFont("Helvetica Neue", 50, bold=True)
font5 = pygame.font.SysFont("Helvetica Neue", 35, bold=True)

# Words/sentences to write
text_surface = my_font.render("WORDLE", False, WHITE)
text_surface2 = my_font2.render("Created by MissterM", False, WHITE)
q1 = font2.render("Q", False, WHITE)
w1 = font2.render("W", False, WHITE)
e1 = font2.render("E", False, WHITE)
r1 = font2.render("R", False, WHITE)
t1 = font2.render("T", False, WHITE)
y1 = font2.render("Y", False, WHITE)
u1 = font2.render("U", False, WHITE)
i1 = font2.render("I", False, WHITE)
o1 = font2.render("O", False, WHITE)
p1 = font2.render("P", False, WHITE)
a1 = font2.render("A", False, WHITE)
s1 = font2.render("S", False, WHITE)
d1 = font2.render("D", False, WHITE)
f1 = font2.render("F", False, WHITE)
g1 = font2.render("G", False, WHITE)
h1 = font2.render("H", False, WHITE)
j1 = font2.render("J", False, WHITE)
k1 = font2.render("K", False, WHITE)
l1 = font2.render("L", False, WHITE)
z1 = font2.render("Z", False, WHITE)
x1 = font2.render("X", False, WHITE)
c1 = font2.render("C", False, WHITE)
v1 = font2.render("V", False, WHITE)
b1 = font2.render("B", False, WHITE)
n1 = font2.render("N", False, WHITE)
m1 = font2.render("M", False, WHITE)
q2 = font4.render("Q", False, WHITE)
w2 = font4.render("W", False, WHITE)
e2 = font4.render("E", False, WHITE)
r2 = font4.render("R", False, WHITE)
t2 = font4.render("T", False, WHITE)
y2 = font4.render("Y", False, WHITE)
u2 = font4.render("U", False, WHITE)
i2 = font4.render("I", False, WHITE)
o2 = font4.render("O", False, WHITE)
p2 = font4.render("P", False, WHITE)
a2 = font4.render("A", False, WHITE)
s2 = font4.render("S", False, WHITE)
d2 = font4.render("D", False, WHITE)
f2 = font4.render("F", False, WHITE)
g2 = font4.render("G", False, WHITE)
h2 = font4.render("H", False, WHITE)
j2 = font4.render("J", False, WHITE)
k2 = font4.render("K", False, WHITE)
l2 = font4.render("L", False, WHITE)
z2 = font4.render("Z", False, WHITE)
x2 = font4.render("X", False, WHITE)
c2 = font4.render("C", False, WHITE)
v2 = font4.render("V", False, WHITE)
b2 = font4.render("B", False, WHITE)
n2 = font4.render("N", False, WHITE)
m2 = font4.render("M", False, WHITE)
enter = font3.render("ENTER", False, WHITE)
reset1 = font3.render("RESET", False, WHITE)
backspace = pygame.image.load('backspace2.png')
staticon = pygame.image.load('statistics.png')
playicon = pygame.image.load('playicon.png')
alert1 = font4.render("You have to use 5 letters!", False, WHITE)
alert2 = font4.render("This word does not exist!", False, WHITE)
alert3 = font5.render("You guessed the word! Congrats!", False, WHITE)
alert4 = font5.render("Unfortunately, you did not guess the word!", False, WHITE)
alert5 = font5.render("That word was:", False, WHITE)


# Function which is adding stats
def jsonadd(dicttoadd):
    with open("stats.json", "r+") as file:
        data = json.load(file)
        data[dicttoadd] += 1
        file.seek(0)
        json.dump(data, file)


# Function which is reseting stats
def jsonreset(dicttoreset):
    with open("stats.json", "r+") as file1:
        data1 = json.load(file1)
        data1[dicttoreset] = 0
        file1.seek(0)
        json.dump(data1, file1)


# Function which is getting stats
def jsontoget(dicttoget):
    with open("stats.json", "r+") as file2:
        data2 = json.load(file2)
        valueofthedict = data2[dicttoget]
        file2.seek(0)
        json.dump(data2, file2)

    return valueofthedict


# Getting stats to write
playedgames = jsontoget("played")
wins = jsontoget("wins")
loses = jsontoget("loses")
wins1 = jsontoget("wins in the 1. round")
wins2 = jsontoget("wins in the 2. round")
wins3 = jsontoget("wins in the 3. round")
wins4 = jsontoget("wins in the 4. round")
wins5 = jsontoget("wins in the 5. round")
wins6 = jsontoget("wins in the 6. round")
currentwinstreak = jsontoget("current win streak")
currentlosestreak = jsontoget("current lose streak")
maxwinstreak = jsontoget("max win streak")
maxlosestreak = jsontoget("max lose streak")

# Stats to write
stats1 = my_font3.render(f"Played games: {playedgames}", False, YELLOW)
stats2 = my_font3.render(f"Wins: {wins} / {round((wins / (playedgames if playedgames > 0 else 1) * 100), 1)}%", False, GREEN)
stats3 = my_font3.render(f"Loses: {loses} / {round((loses / (playedgames if playedgames > 0 else 1) * 100), 1)}%", False, RED)
stats4 = my_font3.render("Wins in the:", False, WHITE)
stats5 = my_font3.render(f"First round: {wins1}", False, WHITE)
stats6 = my_font3.render(f"Second round: {wins2}", False, WHITE)
stats7 = my_font3.render(f"Third round: {wins3}", False, WHITE)
stats8 = my_font3.render(f"Fourth round: {wins4}", False, WHITE)
stats9 = my_font3.render(f"Fifth round: {wins5}", False, WHITE)
stats10 = my_font3.render(f"Sixth round: {wins6}", False, WHITE)
stats11 = my_font3.render(f"Average: {round(((wins1*1 + wins2*2 + wins3*3 + wins4*4 + wins5*5 + wins6*6) / (wins if wins > 0 else 1)), 2)} round", False, WHITE)
stats12 = my_font3.render(f"Current win streak: {currentwinstreak}", False, GREEN)
stats13 = my_font3.render(f"Current lose streak: {currentlosestreak}", False, RED)
stats14 = my_font3.render(f"Max win streak: {maxwinstreak}", False, YELLOW)
stats15 = my_font3.render(f"Max lose streak: {maxlosestreak}", False, YELLOW)


# Menu screen config
def menuscreen():
    WIN.fill((7, 7, 7))
    WIN.blit(text_surface, (WIDTH / 2 - 120, 20))
    WIN.blit(stats1, (100, 100))
    WIN.blit(stats2, (100, 150))
    WIN.blit(stats3, (100, 200))
    WIN.blit(stats4, (100, 250))
    WIN.blit(stats5, (150, 300))
    WIN.blit(stats6, (150, 350))
    WIN.blit(stats7, (150, 400))
    WIN.blit(stats8, (150, 450))
    WIN.blit(stats9, (150, 500))
    WIN.blit(stats10, (150, 550))
    WIN.blit(stats11, (150, 600))
    WIN.blit(stats12, (100, 650))
    WIN.blit(stats13, (100, 700))
    WIN.blit(stats14, (100, 750))
    WIN.blit(stats15, (100, 800))
    rect6 = pygame.Rect(WIDTH - 60, 20, 40, 40)
    pygame.draw.rect(WIN, VERY_LIGHT_GRAY, rect6, 0, 5)
    WIN.blit(playicon, (WIDTH - 47, 29))


# Play screen config
def background():
    # Background
    pygame.draw.rect(WIN, (7, 7, 7), pygame.Rect(0, 0, 4000, 4000))

    # Header
    WIN.blit(text_surface, (WIDTH / 2 - 120, 20))

    # Claims
    WIN.blit(text_surface2, (10, HEIGHT - 30))

    # Chart
    for x in range(6):
        for v in range(5):
            pygame.draw.rect(WIN, GRAY, pygame.Rect(WIDTH / 2 - 195 + (v * 75), HEIGHT / 2 - 333 + (x * 75), 70, 70), 2)

    # Keyboard buttons
    for x in range(-270, 265, 54):
        rect0 = pygame.Rect(WIDTH / 2 + x, HEIGHT / 2 + 200, 45, 65)
        pygame.draw.rect(WIN, LIGHT_GRAY, rect0, 0, 5)

        # Just for developer to know buttons coordinates
        rectangles.append(((WIDTH / 2 + x, WIDTH / 2 + x + 45), (HEIGHT / 2 + 200, HEIGHT / 2 + 265)))

    for x in range(-245, 239, 54):
        rect1 = pygame.Rect(WIDTH / 2 + x, HEIGHT / 2 + 272, 45, 65)
        pygame.draw.rect(WIN, LIGHT_GRAY, rect1, 0, 5)

        # Just for developer to know buttons coordinates
        rectangles.append(((WIDTH / 2 + x, WIDTH / 2 + x + 45), (HEIGHT / 2 + 272, HEIGHT / 2 + 337)))

    for x in range(-192, 186, 54):
        rect2 = pygame.Rect(WIDTH / 2 + x, HEIGHT / 2 + 344, 45, 65)
        pygame.draw.rect(WIN, LIGHT_GRAY, rect2, 0, 5)

        # Just for developer to know buttons coordinates
        rectangles.append(((WIDTH / 2 + x, WIDTH / 2 + x + 45), (HEIGHT / 2 + 344, HEIGHT / 2 + 409)))

    # Enter
    rect3 = pygame.Rect(WIDTH / 2 - 270, HEIGHT / 2 + 344, 70, 65)
    pygame.draw.rect(WIN, LIGHT_GRAY, rect3, 0, 5)

    # Backspace
    rect4 = pygame.Rect(WIDTH / 2 + 187, HEIGHT / 2 + 344, 70, 65)
    pygame.draw.rect(WIN, LIGHT_GRAY, rect4, 0, 5)

    # Reset
    rect5 = pygame.Rect(WIDTH - 100, HEIGHT - 60, 80, 40)
    pygame.draw.rect(WIN, RED, rect5, 0, 5)

    # Stats
    rect6 = pygame.Rect(WIDTH - 60, 20, 40, 40)
    pygame.draw.rect(WIN, VERY_LIGHT_GRAY, rect6, 0, 5)

    # Just for developer to know buttons coordinates
    rectangles.append(((WIDTH / 2 - 270, WIDTH / 2 - 225), (HEIGHT / 2 + 344, HEIGHT / 2 + 409)))
    rectangles.append(((WIDTH / 2 + 187, WIDTH / 2 + 232), (HEIGHT / 2 + 344, HEIGHT / 2 + 409)))

    # Letters on keyboard
    WIN.blit(q1, (WIDTH / 2 - 255, HEIGHT / 2 + 225))
    WIN.blit(w1, (WIDTH / 2 - 201, HEIGHT / 2 + 225))
    WIN.blit(e1, (WIDTH / 2 - 145, HEIGHT / 2 + 225))
    WIN.blit(r1, (WIDTH / 2 - 92, HEIGHT / 2 + 225))
    WIN.blit(t1, (WIDTH / 2 - 37, HEIGHT / 2 + 225))
    WIN.blit(y1, (WIDTH / 2 + 16, HEIGHT / 2 + 225))
    WIN.blit(u1, (WIDTH / 2 + 69, HEIGHT / 2 + 225))
    WIN.blit(i1, (WIDTH / 2 + 127, HEIGHT / 2 + 225))
    WIN.blit(o1, (WIDTH / 2 + 179, HEIGHT / 2 + 225))
    WIN.blit(p1, (WIDTH / 2 + 233, HEIGHT / 2 + 225))
    WIN.blit(a1, (WIDTH / 2 - 228, HEIGHT / 2 + 298))
    WIN.blit(s1, (WIDTH / 2 - 174, HEIGHT / 2 + 298))
    WIN.blit(d1, (WIDTH / 2 - 120, HEIGHT / 2 + 298))
    WIN.blit(f1, (WIDTH / 2 - 66, HEIGHT / 2 + 298))
    WIN.blit(g1, (WIDTH / 2 - 12, HEIGHT / 2 + 298))
    WIN.blit(h1, (WIDTH / 2 + 42, HEIGHT / 2 + 298))
    WIN.blit(j1, (WIDTH / 2 + 96, HEIGHT / 2 + 298))
    WIN.blit(k1, (WIDTH / 2 + 150, HEIGHT / 2 + 298))
    WIN.blit(l1, (WIDTH / 2 + 204, HEIGHT / 2 + 298))
    WIN.blit(z1, (WIDTH / 2 - 174, HEIGHT / 2 + 370))
    WIN.blit(x1, (WIDTH / 2 - 120, HEIGHT / 2 + 370))
    WIN.blit(c1, (WIDTH / 2 - 66, HEIGHT / 2 + 370))
    WIN.blit(v1, (WIDTH / 2 - 12, HEIGHT / 2 + 370))
    WIN.blit(b1, (WIDTH / 2 + 42, HEIGHT / 2 + 370))
    WIN.blit(n1, (WIDTH / 2 + 95, HEIGHT / 2 + 370))
    WIN.blit(m1, (WIDTH / 2 + 149, HEIGHT / 2 + 370))
    WIN.blit(enter, (WIDTH / 2 - 265, HEIGHT / 2 + 371))
    WIN.blit(backspace, (WIDTH / 2 + 208, HEIGHT / 2 + 370))

    WIN.blit(staticon, (WIDTH - 52, 29))  # Stats
    WIN.blit(reset1, (WIDTH - 88, HEIGHT - 47))  # Reset


# Function which is resetting current game
def reset():

    global tablex
    global tabley
    global pword
    global ranword
    global endofthegame
    global repeatletters

    pword = ""
    repeatletters.clear()
    tablex = 0
    tabley = 0
    ranword = random.choice(wordlist)
    endofthegame = False
    background()


# Function which is adding functionality to buttons
def buttons(ev, rword):

    global tablex
    global tabley
    global pword
    global ranword
    global endofthegame
    global menu
    global repeatletters
    writex = 425 + (tablex * 75)  # 75 = 70 - width of one grid + 5 - gap between two grids
    writey = 137 + (tabley * 75)  # 75 = 70 - width of one grid + 5 - gap between two grids

    if ev.type == pygame.MOUSEBUTTONDOWN:
        x, y = ev.pos  # Position of the mouse

        # Stats/Play
        if y in range(20, 60) and x in range(1140, 1180):
            if menu:
                reset()
                menu = False
            else:
                menuscreen()
                menu = True

        # Reset
        if y in range(840, 880) and x in range(1100, 1180):
            reset()

        if not endofthegame:

            # Enter
            if x in range(330, 398) and y in range(794, 859):

                # Whether player fill every grid in the row
                if len(pword) == 5:

                    # Whether player word exist
                    if pword not in wordlist:
                        WIN.blit(alert2, (WIDTH / 2 - 257, HEIGHT / 2 + 135))
                        pygame.display.update()
                        pygame.time.wait(1500)
                        pygame.draw.rect(WIN, (7, 7, 7), pygame.Rect(300, 580, 600, 60), 0)
                    else:

                        for v in range(len(pword)):
                            indx = pword[v]
                            keyx = letternum[indx][0]
                            keyy = letternum[indx][1]
                            if keyy == 0:
                                startx = -270
                                startletter = -255
                            elif keyy == 1:
                                startx = -245
                                startletter = -228
                            elif keyy == 2:
                                startx = -192
                                startletter = -174

                            # Changing grids and buttons color

                            # Whether letter is in word to guess but not in the same position
                            if pword[v] in rword and not pword[v] == rword[v]:
                                pygame.draw.rect(WIN, YELLOW, pygame.Rect(WIDTH / 2 - 195 + (v * 75), writey - 20, 70, 70), 0)
                                WIN.blit(font4.render(pword[v].upper(), False, WHITE), (WIDTH / 2 - 173 + (v * 75), writey))

                                # Whether letter position is already guessed
                                if pword[v] not in repeatletters:
                                    pygame.draw.rect(WIN, YELLOW, pygame.Rect(WIDTH / 2 + startx + (keyx * 54), HEIGHT / 2 + 200 + (keyy * 72), 45, 65), 0, 5)
                                    WIN.blit(font2.render(pword[v].upper(), False, WHITE), (WIDTH / 2 + startletter + (keyx * 54), HEIGHT / 2 + 225 + (keyy * 73)))

                            # Whether letter position is the same in the both words
                            elif pword[v] == rword[v]:
                                pygame.draw.rect(WIN, GREEN, pygame.Rect(WIDTH / 2 - 195 + (v * 75), writey - 20, 70, 70), 0)
                                WIN.blit(font4.render(pword[v].upper(), False, WHITE), (WIDTH / 2 - 173 + (v * 75), writey))
                                pygame.draw.rect(WIN, GREEN, pygame.Rect(WIDTH / 2 + startx + (keyx * 54), HEIGHT / 2 + 200 + (keyy * 72), 45, 65), 0, 5)
                                WIN.blit(font2.render(pword[v].upper(), False, WHITE), (WIDTH / 2 + startletter + (keyx * 54), HEIGHT / 2 + 225 + (keyy * 73)))
                                repeatletters.append(pword[v])

                            else:
                                pygame.draw.rect(WIN, BLACK, pygame.Rect(WIDTH / 2 - 195 + (v * 75), writey - 20, 70, 70), 0)
                                WIN.blit(font4.render(pword[v].upper(), False, WHITE), (WIDTH / 2 - 173 + (v * 75), writey))
                                pygame.draw.rect(WIN, BLACK, pygame.Rect(WIDTH / 2 + startx + (keyx * 54), HEIGHT / 2 + 200 + (keyy * 72), 45, 65), 0, 5)
                                WIN.blit(font2.render(pword[v].upper(), False, WHITE), (WIDTH / 2 + startletter + (keyx * 54), HEIGHT / 2 + 225 + (keyy * 73)))

                        tabley += 1  # Go to the next row
                        tablex = 0  # Start again from first grid

                        # Whether player won
                        if pword == rword:
                            jsonadd("played")
                            jsonadd("wins")
                            jsonadd("current win streak")
                            jsonadd(f"wins in the {tabley}. round")
                            jsonreset("current lose streak")
                            if jsontoget("current win streak") > jsontoget("max win streak"):
                                jsonadd("max win streak")

                            WIN.blit(alert3, (WIDTH / 2 - 240, HEIGHT / 2 + 140))
                            endofthegame = True

                        # Whether player is losing 6th time
                        elif tabley == 6:
                            jsonadd("played")
                            jsonadd("loses")
                            jsonadd("current lose streak")
                            jsonreset("current win streak")
                            if jsontoget("current lose streak") > jsontoget("max lose streak"):
                                jsonadd("max lose streak")
                            WIN.blit(alert4, (WIDTH / 2 - 300, HEIGHT / 2 + 125))
                            WIN.blit(alert5, (WIDTH / 2 - 151, HEIGHT / 2 + 160))
                            WIN.blit(font5.render(f"{ranword}", False, GREEN), (WIDTH / 2 + 65, HEIGHT / 2 + 160))

                        pword = ""

                else:
                    WIN.blit(alert1, (WIDTH / 2 - 257, HEIGHT / 2 + 135))
                    pygame.display.update()
                    pygame.time.wait(1500)
                    pygame.draw.rect(WIN, (7, 7, 7), pygame.Rect(300, 580, 600, 60), 0)

            # Backspace
            if x in range(787, 856) and y in range(794, 859):

                # Whether player wrote any letter to the row
                if len(pword) > 0:
                    pword = "".join(pword[:-1])
                    pygame.draw.rect(WIN, (7, 7, 7), pygame.Rect(writex - 93, writey - 17, 65, 65), 0)
                    tablex -= 1

            # Rest of letters
            if len(pword) < 5 and tabley < 6:

                # First keyboard row (q-p)
                if y in range(650, 715):
                    if x in range(330, 375):
                        pword += "q"
                        WIN.blit(q2, (writex, writey))
                        tablex += 1
                    if x in range(384, 429):
                        pword += "w"
                        WIN.blit(w2, (writex - 2, writey))
                        tablex += 1
                    if x in range(438, 483):
                        pword += "e"
                        WIN.blit(e2, (writex + 4, writey))
                        tablex += 1
                    if x in range(492, 537):
                        pword += "r"
                        WIN.blit(r2, (writex + 2, writey))
                        tablex += 1
                    if x in range(546, 591):
                        pword += "t"
                        WIN.blit(t2, (writex + 3, writey))
                        tablex += 1
                    if x in range(600, 645):
                        pword += "y"
                        WIN.blit(y2, (writex + 3, writey))
                        tablex += 1
                    if x in range(654, 699):
                        pword += "u"
                        WIN.blit(u2, (writex + 2, writey))
                        tablex += 1
                    if x in range(708, 753):
                        pword += "i"
                        WIN.blit(i2, (writex + 9, writey))
                        tablex += 1
                    if x in range(762, 807):
                        pword += "o"
                        WIN.blit(o2, (writex + 1, writey))
                        tablex += 1
                    if x in range(816, 861):
                        pword += "p"
                        WIN.blit(p2, (writex + 4, writey))
                        tablex += 1

                # Second keyboard row (a-l)
                elif y in range(722, 787):
                    if x in range(355, 400):
                        pword += "a"
                        WIN.blit(a2, (writex + 2, writey))
                        tablex += 1
                    if x in range(409, 454):
                        pword += "s"
                        WIN.blit(s2, (writex + 2, writey))
                        tablex += 1
                    if x in range(463, 508):
                        pword += "d"
                        WIN.blit(d2, (writex + 2, writey))
                        tablex += 1
                    if x in range(517, 562):
                        pword += "f"
                        WIN.blit(f2, (writex + 4, writey))
                        tablex += 1
                    if x in range(571, 616):
                        pword += "g"
                        WIN.blit(g2, (writex + 1, writey))
                        tablex += 1
                    if x in range(625, 670):
                        pword += "h"
                        WIN.blit(h2, (writex + 2, writey))
                        tablex += 1
                    if x in range(679, 724):
                        pword += "j"
                        WIN.blit(j2, (writex + 5, writey))
                        tablex += 1
                    if x in range(733, 778):
                        pword += "k"
                        WIN.blit(k2, (writex + 3, writey))
                        tablex += 1
                    if x in range(787, 832):
                        pword += "l"
                        WIN.blit(l2, (writex + 5, writey))
                        tablex += 1

                # Third keyboard row (z-m)
                elif y in range(794, 859):
                    if x in range(409, 454):
                        pword += "z"
                        WIN.blit(z2, (writex + 2, writey))
                        tablex += 1
                    if x in range(463, 508):
                        pword += "x"
                        WIN.blit(x2, (writex + 2, writey))
                        tablex += 1
                    if x in range(517, 562):
                        pword += "c"
                        WIN.blit(c2, (writex + 3, writey))
                        tablex += 1
                    if x in range(571, 616):
                        pword += "v"
                        WIN.blit(v2, (writex + 2, writey))
                        tablex += 1
                    if x in range(625, 670):
                        pword += "b"
                        WIN.blit(b2, (writex + 2, writey))
                        tablex += 1
                    if x in range(679, 724):
                        pword += "n"
                        WIN.blit(n2, (writex + 2, writey))
                        tablex += 1
                    if x in range(732, 777):
                        pword += "m"
                        WIN.blit(m2, (writex , writey))
                        tablex += 1


# Start game
def main():
    run = True
    clock = pygame.time.Clock()

    # Draw play screen
    background()

    while run:

        # FPS
        clock.tick(60)

        # Update the screen
        pygame.display.flip()

        for event in pygame.event.get():

            # Check whether player is trying to quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # Check whether player is using the button
            buttons(event, ranword)


if __name__ == "__main__":
    main()
