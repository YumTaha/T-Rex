import pygame
from sys import exit
from random import randint, choice, uniform

game_status = True
previous_score = 0

theme = 'white'
current_score = 0

class Dino(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dino_index = 0
        self.position = 'up'

        dino_walk1 = pygame.transform.rotozoom(pygame.image.load(f'items/{theme}_theme/walk_2.png').convert_alpha(), 0, 0.7)
        dino_walk2 = pygame.transform.rotozoom(pygame.image.load(f'items/{theme}_theme/walk_3.png').convert_alpha(), 0, 0.7)
        self.dino_walk = [dino_walk1, dino_walk2]

        self.dino_jump = pygame.transform.rotozoom(pygame.image.load(f'items/{theme}_theme/walk_0.png').convert_alpha(), 0, 0.7)
        
        dino_down1 = pygame.transform.rotozoom(pygame.image.load(f'items/{theme}_theme/down_1.png').convert_alpha(), 0, 0.9)
        dino_down2 = pygame.transform.rotozoom(pygame.image.load(f'items/{theme}_theme/down_2.png').convert_alpha(), 0, 0.9)
        self.dino_down = [dino_down1, dino_down2]

        self.image = self.dino_walk[self.dino_index]
        if self.position == 'up': self.rect = self.image.get_rect(midbottom= (150 , 463))
        else: self.rect = self.image.get_rect(midbottom= (250 , 490))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and self.rect.bottom >=463: self.gravity = -20
        if keys[pygame.K_DOWN] : self.position = 'down'
        else: self.position = 'up'

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 463 and self.position == 'up': self.rect.bottom = 463
        elif self.rect.bottom >= 490 and self.position == 'down': self.rect.bottom = 490

    def dino_animation(self):
        if self.rect.bottom <463: self.image = self.dino_jump
        else:
            self.dino_index += 0.1
            if self.dino_index >=len(self.dino_walk) : self.dino_index = 0
            if self.position == 'up' : self.image = self.dino_walk[int(self.dino_index)]
            else: self.image = self.dino_down[int(self.dino_index)]

    def update(self):
            self.player_input()
            self.dino_animation()
            self.apply_gravity()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type, **kwargs):
        super().__init__(**kwargs)
        if type == 'fly':
            self.frames = [pygame.transform.rotozoom(pygame.image.load(f'items/{theme}_theme/fly_{i}.png').convert_alpha(), 0, 1.5) for i in range(1,3)]
            ypos = choice([380, 410])
        else:
            self.frames = [pygame.transform.rotozoom(pygame.image.load(f'items/{theme}_theme/small_trees_{randint(1,8)}.png').convert_alpha(), 0, 1.5)]
            ypos = 463

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright= (randint(1000, 1500), ypos))
        
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.rect.x -= 8
        self.animation_state()
        self.destroy()

    def destroy(self):

        if self.rect.x <= -50:
            self.kill()

class Clouds(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        cloud = pygame.image.load(f'items/{theme}_theme/cloud.png').convert_alpha()
        self.image = cloud
        self.rect = self.image.get_rect(bottomright= (1000, randint(50,400)))
        
    def update(self):
        self.rect.x -= 3
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def get_score():
    global current_score
    current_score = (pygame.time.get_ticks() - start_time) // 1000 # convert to seconds
    time_str = f"{current_score:0004d}"
    time_sur = font.render(time_str, False, (255, 255, 255)) if theme=='grey' else font.render(time_str, False, (84, 84, 84))
    time_rec = time_sur.get_rect(midleft=(820, 25))
    screen.blit(time_sur, time_rec)

def collision():
    if pygame.sprite.spritecollide(dino.sprite, obstacle_group, False): return False
    else: return True

pygame.init()


start_time = 0



screen = pygame.display.set_mode((900,500))
pygame.display.set_caption('T-Rex')
icon = pygame.image.load('items/grey_theme/dead.png').convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/Pixeltype.ttf', 40)


#creating objects
dino = pygame.sprite.GroupSingle()
dino.add(Dino())
cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

#animation timer
obstacle_timer = pygame.USEREVENT + 2
pygame.time.set_timer(obstacle_timer, 1200)

groundy = 0

while True:
    background_surf = pygame.image.load(f'items/{theme}_theme/background.png').convert()
    background_surf = pygame.transform.rotozoom(background_surf, 0, 1.5)

    ground_surf = pygame.image.load(f'items/{theme}_theme/ground.png').convert_alpha()

    theme_changer = pygame.image.load(f'items/{theme}_theme/button.png').convert_alpha()
    theme_changer = pygame.transform.rotozoom(theme_changer, 0, 0.3)
    theme_changer_rect = theme_changer.get_rect(topleft= (0,0))



    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN and theme_changer_rect.collidepoint(event.pos):
            theme = 'grey' if theme == 'white' else 'white'

        if game_status:
            if event.type == obstacle_timer:
                cloud_group.add(Clouds())
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['tree','tree','tree', 'fly'])))

    
    
    
    
    if game_status:

        if groundy>-1200: groundy-=8
        else: groundy = 0

        screen.blit(background_surf, (0, 0))
        screen.blit(theme_changer, theme_changer_rect)
        screen.blit(ground_surf, (groundy, 400))
        screen.blit(ground_surf, (1200+groundy, 400))
        get_score()

        dino.draw(screen)
        dino.update()
        cloud_group.draw(screen)
        cloud_group.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        game_status = collision()

    else:

        previous_score = current_score

        # Initialize the surface (gameover)
        screen.fill(f'{theme}')
        restart_surf = pygame.image.load(f'items/{theme}_theme/restart.png').convert_alpha()
        restart_surf = pygame.transform.rotozoom(restart_surf, 0, 0.5)
        restart_rect = restart_surf.get_rect(center = (450, 200))

        font_over = pygame.font.Font('fonts/Pixeltype.ttf', 90)

        # game over texts
        color = 'black' if theme == 'white' else 'white'
        textover_surf = font_over.render(f'SCORE: {current_score}', False, f'{color}')
        textover_rect = textover_surf.get_rect(center = (450, 100))

        
        # Display
        screen.blit(restart_surf, restart_rect)
        screen.blit(textover_surf, textover_rect)

        if event.type == pygame.MOUSEBUTTONDOWN and restart_rect.collidepoint(event.pos):
            game_status = True
            obstacle_group.empty()




        start_time = pygame.time.get_ticks()
        
        if event.type == pygame.K_ESCAPE:
            pygame.quit()
            exit()


    pygame.display.update()
    clock.tick(60)

