import pygame


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("miner vs bats")

try:
    icon = pygame.image.load('images/icon.png.png')
    bg = pygame.image.load('images/bg1.png.png').convert_alpha()
    enemy = pygame.image.load('images/bat.png').convert_alpha()
    bullet = pygame.image.load('images/bullet.png').convert_alpha()
    lose_bg = pygame.image.load('images/lose_background.webp').convert_alpha()
    money = pygame.image.load('images/money.png').convert_alpha()
    health = pygame.image.load('images/player_health.png').convert_alpha()

    go_left = [
        pygame.image.load('player_left/player.2.png').convert_alpha(),
        pygame.image.load('player_left/player.3.png').convert_alpha(),
        pygame.image.load('player_left/player.6.png').convert_alpha(),
    ]
    go_right = [
        pygame.image.load('player_right/player4.png').convert_alpha(),
        pygame.image.load('player_right/player5.png').convert_alpha(),
        pygame.image.load('player_right/player7.png').convert_alpha(),
    ]
    stay = [pygame.image.load('images/player.1.png').convert_alpha()]
except pygame.error as e:
    print("Ошибка загрузки изображения:", e)
    exit()

pygame.display.set_icon(icon)

player_width = go_right[0].get_width() // 4  
player_height = go_right[0].get_height() // 4  

go_right = [pygame.transform.scale(image, (player_width, player_height)) for image in go_right]
go_left = [pygame.transform.scale(image, (player_width, player_height)) for image in go_left]
stay = [pygame.transform.scale(image, (player_width, player_height)) for image in stay]

player_health = 3
money_count = 0
win_count = 10
game_win = False
money_objects = []
bullets = []
bullets_left = 15
enemy_in_game = []
bg_x = 0
player_anim_count = 0
player_speed = 7
player_x = 150
player_y = 230
is_jump = False
jump_count = 11
gameplay = True
running = True
sound = pygame.mixer.Sound('Sounds/game_song.mp3')
lose_sound = pygame.mixer.Sound('Sounds/lose_sound.mp3')
if not pygame.mixer.get_busy():
    sound.play(-1)
win_sound = pygame.mixer.Sound('Sounds/game_win_sound.mp3')
if not pygame.mixer.get_busy():
    sound.play(-1)
money_sound = pygame.mixer.Sound('Sounds/money_collect_sound.mp3')

puls_text = pygame.font.Font('shrift.ttf',10)
text = pygame.font.Font('shrift.ttf', 40)
lose_text = text.render("Waster!", False, "Red")
win_text = text.render("You Win!", False, "Red")
restart_text = text.render("Restart Game", False, "Yellow")
restart_text_rect = restart_text.get_rect(topleft=(180, 200))


enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

money_timer = pygame.USEREVENT + 2
pygame.time.set_timer(money_timer, 3500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer and gameplay:
            enemy_in_game.append(enemy.get_rect(topleft=(650, 200)))
        if event.type == money_timer and gameplay:
            money_objects.append(money.get_rect(topleft=(650, 150)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_k and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 20, player_y)))
            bullets_left -= 1

    if gameplay:
        if not pygame.mixer.get_busy():
            sound.play(-1)
        lose_sound.stop()
        health_text = puls_text.render(f'Healths: {player_health}', True, (255, 255, 255))
        bullet_text = puls_text.render(f'Puls: {bullets_left}', True, (255, 255, 255))
        money_text = puls_text.render(f'Moneys To Win: {win_count - money_count}', True,(255,255,255))
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 640, 0))
        screen.blit(bullet, (10, 10))  
        screen.blit(bullet_text, (60, 15))
        screen.blit(health,(10,50))
        screen.blit(health_text,(60,60))
        screen.blit(money,(10,90))
        screen.blit(money_text,(60,100))
        

        bg_x -= 2
        if bg_x <= -640:
            bg_x = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 50 or keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
            screen.blit(go_left[player_anim_count], (player_x, player_y))
        elif keys[pygame.K_RIGHT] and player_x < 570 or keys[pygame.K_d] and player_x < 570:
            player_x += player_speed
            screen.blit(go_right[player_anim_count], (player_x, player_y))
        else:
            screen.blit(stay[0], (player_x, player_y))

        if not is_jump:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                is_jump = True
        else:
            if jump_count >= -11:
                neg = 1 if jump_count > 0 else -1
                player_y -= (jump_count ** 2) * 0.2 * neg
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 11

        player_anim_count = (player_anim_count + 1) % 3

        for enemy_rect in enemy_in_game:
            enemy_rect.x -= 10
            screen.blit(enemy, (enemy_rect.x, enemy_rect.y))
            if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(enemy_rect):
                player_health -=1
                enemy_in_game.remove(enemy_rect)
            if player_health <= 0:
                gameplay = False
                

        for money_rect in money_objects[:]:
            money_rect.x -= 20
            screen.blit(money, (money_rect.x, money_rect.y))
            if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(money_rect):
                money_count += 1
                money_sound.play()
                money_objects.remove(money_rect)
        
        if money_count >= win_count:
            gameplay = False
            game_win = True

    
    if game_win:
        if sound.get_num_channels():
            sound.stop()
        if not pygame.mixer.get_busy():
            win_sound.play()
        screen.blit(lose_bg, (0, 0))
        screen.blit(win_text, (220, 100))
        screen.blit(restart_text, restart_text_rect)
        bullets.clear()
        money_count = 0
        bullets_left = 6


    elif not gameplay:
        if sound.get_num_channels():
            sound.stop()
        if not pygame.mixer.get_busy():
            lose_sound.play()
        screen.blit(lose_bg, (0, 0))
        screen.blit(lose_text, (220, 100))
        screen.blit(restart_text, restart_text_rect)
        money_count = 0
        bullets.clear()
        bullets_left = 15

    mouse = pygame.mouse.get_pos()
    if restart_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        gameplay = True
        player_x = 150
        player_health = 3
        enemy_in_game.clear()
        money_objects.clear()
        money_count = 0
        game_win = False

    if bullets:
        for i, el in enumerate(bullets[:] ):
            screen.blit(bullet, (el.x, el.y))
            el.x += 5
            if el.x > (player_x + 300):
                bullets.remove(el)
                continue
            for index, enemy_x in enumerate(enemy_in_game[:] ):
                if el.colliderect(enemy_x):
                    enemy_in_game.remove(enemy_x)
                    bullets.remove(el)
                    break

    pygame.display.update()
    clock.tick(30)
