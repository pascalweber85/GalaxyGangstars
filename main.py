import pygame
import os
pygame.font.init()
pygame.mixer.init()





WIDTH, HEIGHT = 1400, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Gangstars")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 5, HEIGHT)

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 10
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 75, 75

YELLOW_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets", "spaceship1.png"))
GREEN_SPACESHIP_IMAGE = pygame.image.load(os.path.join("assets", "spaceship2.png"))
# YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
# GREEN_SPACESHIP_IMAGE = pygame.transform.scale(GREEN_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (WIDTH, HEIGHT))


def draw_window(yellow, green, yellow_bullets, green_bullets, yellow_health, green_health):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    yellow_health_text = HEALTH_FONT.render(f"HP: {yellow_health}", 1, WHITE)
    green_health_text = HEALTH_FONT.render(f"HP: {green_health}", 1, WHITE)
    WIN.blit(yellow_health_text, (WIDTH - 90, 10))
    WIN.blit(green_health_text, (0 + 10, 10))

    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(GREEN_SPACESHIP_IMAGE, (green.x, green.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()


def handle_movement(keys_pressed, yellow, green):
    # player 1
    if keys_pressed[pygame.K_a] and yellow.x > 0:  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x < (0.5 * WIDTH - SPACESHIP_WIDTH):  # RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y > 0:  # UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y < HEIGHT - SPACESHIP_HEIGHT:  # DOWN
        yellow.y += VELOCITY

    # player 2
    if keys_pressed[pygame.K_LEFT] and green.x > (0.5 * WIDTH):  # LEF5T
        green.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and green.x < WIDTH - SPACESHIP_WIDTH:  # RIGHT
        green.x += VELOCITY
    if keys_pressed[pygame.K_UP] and green.y > 0:  # UP
        green.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and green.y < HEIGHT - SPACESHIP_HEIGHT:  # DOWN
        green.y += VELOCITY


def handle_bullets(yellow_bullets, green_bullets, yellow, green):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            green_bullets.remove(bullet)
        elif bullet.x < 0:
            green_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_width()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(1225, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    green_bullets = []

    yellow_health = 10
    green_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y + green.height //2 - 2, 10, 5)
                    green_bullets.append(bullet)

            if event.type == YELLOW_HIT:
                green_health -= 1

            if event.type == GREEN_HIT:
                yellow_health -= 1


        winner_text = ""

        if yellow_health <= 0:
            winner_text = "PASSI WINS!"

        if green_health <= 0:
            winner_text = "TAXI WINS!"

        if winner_text != "":
            draw_winner(winner_text)
            break




        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, yellow, green)

        handle_bullets(yellow_bullets, green_bullets, yellow, green)

        draw_window(yellow, green, yellow_bullets, green_bullets, yellow_health, green_health)

    pygame.quit()


if __name__ == "__main__":
    main()
