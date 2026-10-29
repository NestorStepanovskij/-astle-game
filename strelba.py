import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Soul Knight: Rebirth")
clock = pygame.time.Clock()

# ------------------- ИГРОК -------------------
player = pygame.Rect(400, 300, 40, 40)
PLAYER_SPEED = 4
facing = (1, 0)  # направление последнего движения (dx, dy)

# ------------------- ПУЛИ -------------------
bullets = []          # [(rect, dx, dy), ...]
BULLET_SPEED = 10
BULLET_SIZE = 8
SHOOT_COOLDOWN = 200  # мс
last_shot = 0

# ------------------- ГЛАВНЫЙ ЦИКЛ -------------------
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # --- Движение игрока ---
    dx = dy = 0
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= PLAYER_SPEED
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += PLAYER_SPEED
    if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= PLAYER_SPEED
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += PLAYER_SPEED

    if dx != 0 or dy != 0:
        # запоминаем направление (по диагонали тоже работает)
        facing = (dx, dy)

    player.x += dx
    player.y += dy
    player.clamp_ip(screen.get_rect())  # не выходим за экран

    # --- Стрельба ---
    now = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and now - last_shot > SHOOT_COOLDOWN:
        bullet = pygame.Rect(player.centerx - BULLET_SIZE // 2,
                             player.centery - BULLET_SIZE // 2,
                             BULLET_SIZE, BULLET_SIZE)
        bullets.append([bullet, facing[0], facing[1]])
        last_shot = now

    # --- Обновление пуль ---
    alive_bullets = []
    for rect, bx, by in bullets:
        rect.x += bx * BULLET_SPEED
        rect.y += by * BULLET_SPEED

        # Вышла за экран — удаляем
        if not screen.get_rect().colliderect(rect):
            continue

        alive_bullets.append([rect, bx, by])
    bullets = alive_bullets

    # ------------------- ОТРИСОВКА -------------------
    screen.fill((30, 30, 40))
    pygame.draw.rect(screen, (60, 180, 255), player)
    for rect, _, _ in bullets:
        pygame.draw.rect(screen, (255, 220, 60), rect)

    pygame.display.flip()

pygame.quit()
sys.exit()