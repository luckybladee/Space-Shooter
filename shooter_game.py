from random import randint
from pygame import *

rel_time = False
num_fire = 0
hp = 5
score = 0 
lost = 0
max_lost = 3
goal = 15 
level = 1
new_level = False

font.init()
font2 = font.Font(None, 80)
font = font.Font(None, 30)
win = font.render('Victory!', True, (255, 100, 255))
lose = font2.render('You Lost!', True, (180, 0, 0))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and  self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    direction = 'left'

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_width - 85:
            self.direction = 'left'
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Space shooter')
background = transform.scale(image.load('spece1.jpg'), (win_width, win_height))

player = Player('2058494.png', 5, win_height - 80, 5)
monsters = sprite.Group()
for i in range (1,6):
    monster = Enemy('190276.png', randint(0, win_width - 80), 100, randint(1, 2))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range (1,3):
    asteroid = Enemy('asteroid.png', randint(0, win_width - 80), 100, randint(1, 3))
    asteroids.add(asteroid)

bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
#Adamage_sound = mixer.Sound('damage.mp3')

game = True
finish = False

clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                if num_fire < 10 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
            if num_fire >= 10 and rel_time == False:
                last_time = timer()
                rel_time = True
    

    if finish != True:
        #фон
        window.blit(background, (0, 0))

        #столкновения
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            if level == 2:
                monster = Enemy('190276.png', randint(80, win_width - 80), 50, randint(1, 2))
            elif level == 3:
                monster = Enemy('190276.png', randint(80, win_width - 80), 50, randint(1, 2))
            elif level == 3:
                monster = Enemy('190276.png', randint(80, win_width - 80), 50, randint(3, 4))
            else:
                monster = Enemy('190276.png', randint(80, win_width - 80), 50, randint(4, 6))
            monsters.add(monster)
        
        #повышение уровня
        if score > goal:
            level += 1
            new_level = True
            if level == 2 and new_level:
                goal = 30
                for i in range(1, 2):
                        asteroid = Enemy('asteroid.png', randint(0, win_width - 80), 100, randint(1, 3))
                        asteroids.add(asteroid)

                for i in range(3, 6):
                    monster = Enemy('190276.png', randint(80, win_width - 80), 100, randint(1, 2))
                    monsters.add(monster)
                    new_level = False

            if level == 3 and new_level:
                goal = 40
                for i in range(9,10):
                    monster = Enemy('190276.png', randint(80, win_width - 80), 100, randint(1, 2))
                    monsters.add(monster)
                    new_level = False
            
            if level == 4 and new_level:
                goal = 50
                for i in range(9,10):
                    monster = Enemy('190276.png', randint(80, win_width - 80), 100, randint(3, 4))
                    monsters.add(monster)
                    new_level = False
            
            if level == 5 and new_level:
                goal = 60
                extra_level = font.render('EXTRA LEVEL', (50, 50, 50))
                window.blit(extra_level, (90, 85))
                for i in range(12):
                    monster = Enemy('190276.png', randint(80, win_width - 80), 100, randint(5, 6))
                    monsters.add(monster)
                    new_level = False

        player.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        #перезарядка
        if rel_time == True:
            now_time = timer()

            if now_time - last_time == 0:
                reload = font.render('RELOADING', 1, (150, 0, 10))
                window.blit(reload, (90, 60))
            else:
                num_fire = 0
                rel_time = False


        #победа
        if score >= goal and level >= 5:
            window.blit(win, (300, 200))
            mixer.music.stop()
            finish = True

        #проигрыш
        if sprite.spritecollide(player, monsters, True) or lost >= max_lost:
            damage_sound.play()
            hp -= 1
            if hp <= 0 :
                finish = True
                window.blit(lose, (300, 200))
                damage_sound.play()  
                mixer.music.stop()

        text_hp = font.render('Hp:' + str(hp), 1, (255, 255, 0))
        window.blit(text_hp, (10, 80))
        
        text = font.render("Score: " + str(score), 1, (0, 255, 255))
        window.blit(text, (10, 40))

        text_lose = font.render('Lost: ' + str(lost),  1, (255, 0, 255))
        window.blit(text_lose, (10, 60))

        text_level = font2.render("Level: " + str(level), 1, (0, 50, 255))
        window.blit(text_level, (300, 10))

        display.update()
        clock.tick(FPS)