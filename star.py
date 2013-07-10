""" mail pilot 
  
    
    """
    
import pygame, random
pygame.init()

screen = pygame.display.set_mode((840, 480))

class Ship(pygame.sprite.Sprite):
  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.loadImages()
        
        self.frame = 0
        self.delay = 3
        self.pause = 0

        self.image = self.imgList[0]
        self.rect = self.image.get_rect()
        
    def loadImages(self):
        imgMaster = pygame.image.load("ship.bmp")
        imgMaster = imgMaster.convert()
        
        if not pygame.mixer:
            print("problem with sound")
        else:
            pygame.mixer.init()
            self.sndStar = pygame.mixer.Sound("star.ogg")
            self.sndCrash = pygame.mixer.Sound("crash.ogg")
            self.sndBg = pygame.mixer.Sound("bg.ogg")
            self.sndBonus = pygame.mixer.Sound("bonus.ogg")
            self.sndBg.play(-1)
        self.imgList = []
        
        imgSize = (64,29)
        offset = ((0, 0), (0,29), (0, 58), (0, 87))

        for i in range(4):
            tmpImg = pygame.Surface(imgSize)
            tmpImg.blit(imgMaster, (0, 0), (offset[i], imgSize))
            transColor = tmpImg.get_at((1, 1))
            tmpImg.set_colorkey(transColor)
            self.imgList.append(tmpImg)
    
    def update(self):
        self.pause += 1
        if self.pause >= self.delay:
            self.pause = 0
            self.frame += 1
            if self.frame >= len(self.imgList):
                self.frame = 0
                
            self.image = self.imgList[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = (320, 240)
            
            mousex, mousey = pygame.mouse.get_pos()
            self.rect.center = (50, mousey)
class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("star.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 8
    
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousey > self.rect.centery:
            self.dy = 1
        else:  
            self.dy = -1
        self.rect.centerx -= self.dx
        self.rect.centery -= self.dy
        if self.rect.right <= 0: #screen.get_width():
            self.reset()
            
    def reset(self):
        self.rect.centerx = 960
        self.rect.centery = random.randrange(0, screen.get_height())
        
class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bonus.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()
        
        self.dx = 8
    
    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousey > self.rect.centery:
            self.dy = 2
        else:  
            self.dy = -2
        self.rect.centerx -= self.dx
        self.rect.centery -= self.dy
        if self.rect.right <= 0: #screen.get_width():
            self.reset()
            
    def reset(self):
        self.rect.centerx = 960
        self.rect.centery = random.randrange(0, screen.get_height())
      
class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("enemy.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.reset()

    def update(self):
        mousex, mousey = pygame.mouse.get_pos()
        if mousey > self.rect.centery:
            self.dy = -2
        else:  
            self.dy = 2
        self.rect.centerx -= self.dx
        self.rect.centery -= self.dy
        if self.rect.right <= 0:
            self.reset()
    
    def reset(self):
        self.rect.bottom = 0
        self.rect.centery = random.randrange(0, screen.get_height())
        self.rect.centerx = 960
        self.dy = random.randrange(-2, 2)
        self.dx = random.randrange(5, 10)
    
class Space(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("space.gif")
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.dx = -6
        self.reset()
        
    def update(self):
        self.rect.left += self.dx
        if self.rect.left <= -1042:
            self.reset() 
    
    def reset(self):
        self.rect.left = +0
class Scoreboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lives = 5
        self.score = 0
        self.font = pygame.font.SysFont("None", 50)
        
    def update(self):
        self.text = "Lives: %d, Stars: %d" % (self.lives, self.score)
        self.image = self.font.render(self.text, 1, (255, 255, 0))
        self.rect = self.image.get_rect()
    
def game():
    pygame.display.set_caption("SpaceNova")

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    ship = Ship()
    bonus = Bonus()
    star = Star()
    alien1 = Alien()
    alien2 = Alien()
    space = Space()
    scoreboard = Scoreboard()

    friendSprites = pygame.sprite.OrderedUpdates(space, star, ship, bonus)
    alienSprites = pygame.sprite.Group(alien1, alien2)
    scoreSprite = pygame.sprite.Group(scoreboard)

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        pygame.mouse.set_visible(False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        
        #check collisions
        
        if ship.rect.colliderect(star.rect):
            ship.sndStar.play()
            star.reset()
            scoreboard.score += 1
            
        if ship.rect.colliderect(bonus.rect):
            ship.sndBonus.play()
            bonus.reset()
            scoreboard.lives += 1

        hitAlien = pygame.sprite.spritecollide(ship, alienSprites, False)
        if hitAlien:
            ship.sndCrash.play()
            scoreboard.lives -= 1
            if scoreboard.lives <= 0:
                keepGoing = False
            for theAlien in hitAlien:
                theAlien.reset()
        
        friendSprites.update()
        alienSprites.update()
        scoreSprite.update()
        
        friendSprites.draw(screen)
        alienSprites.draw(screen)
        scoreSprite.draw(screen)
        
        pygame.display.flip()
    
    ship.sndBg.stop()
    #return mouse cursor
    pygame.mouse.set_visible(True) 
    return scoreboard.score
    
def instructions(score):
    pygame.display.set_caption("SpaceNova!")

    ship = Ship()
    space = Space()
    
    allSprites = pygame.sprite.Group(space, ship)
    insFont = pygame.font.SysFont(None, 50)
    insLabels = []
    instructions = (
    "Mail Pilot.     Last score: %d" % score ,
    "Instructions:  You are driving a Space Ship",
    "trying to avoid aliens and collecting stars",
    "to save your planet.",
    "The aliens will move towards you",
    "the stars will try to avoid you",    
    "Hitting the aliens will drain your life",
    "Pink stars give you more life points",
    "Control the Ship with your mouse",
    "",
    "Good Luck!",
    "",
    "Click to start, escape to quit..."
    )
    
    for line in instructions:
        tempLabel = insFont.render(line, 1, (255, 255, 0))
        insLabels.append(tempLabel)
 
    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
                donePlaying = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                keepGoing = False
                donePlaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                    donePlaying = True
    
        allSprites.update()
        allSprites.draw(screen)

        for i in range(len(insLabels)):
            screen.blit(insLabels[i], (50, 30*i))

        pygame.display.flip()
        
    ship.sndBg.stop()    
    pygame.mouse.set_visible(True)
    return donePlaying
        
def main():
    donePlaying = False
    score = 0
    while not donePlaying:
        donePlaying = instructions(score)
        if not donePlaying:
            score = game()


if __name__ == "__main__":
    main()
    
    
