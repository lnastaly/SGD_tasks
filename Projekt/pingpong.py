import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
CYAN = (0, 255, 255)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_COLORS = [WHITE, RED, GREEN, BLUE, YELLOW, PINK, CYAN]
BALL_RADIUS = 8
FPS = 60
WINNING_SCORE = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping-Pong")

font = pygame.font.SysFont("Arial", 36)

score_sound = pygame.mixer.Sound("score.mp3")

class Paddle:
    def __init__(self, x, color=WHITE):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 5
        self.color = color

    def move(self, up=True):
        if up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        self.rect.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.rect = pygame.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = 4 * random.choice([-1, 1])
        self.dy = 4 * random.choice([-1, 1])
        self.rect = pygame.Rect(self.x - BALL_RADIUS, self.y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
            self.dy *= -1

        self.rect.x = self.x - BALL_RADIUS
        self.rect.y = self.y - BALL_RADIUS

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), BALL_RADIUS)

def show_start_screen():
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    info_font = pygame.font.SysFont("Arial", 28)

    while True:
        screen.fill(BLACK)

        title_text = title_font.render("Ping-Pong", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        info_text = info_font.render("Press any button to continue", True, WHITE)
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT * 3 // 4))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def draw_menu(options, selected_index):
    screen.fill(BLACK)
    title_font = pygame.font.SysFont("Arial", 60, bold=True)

    title_text = title_font.render("Ping-Pong", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 60))

    for i, option in enumerate(options):
        color = WHITE if i != selected_index else (100, 255, 100)
        text = font.render(option, True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 160 + i * 60))

    pygame.display.flip()

def color_selection_screen():
    small_font = pygame.font.SysFont("Arial", 24)
    p1_index = 0
    p2_index = 1 if len(PADDLE_COLORS) > 1 else 0

    while True:
        screen.fill(BLACK)

        p1_label = font.render("Player 1 Color", True, WHITE)
        screen.blit(p1_label, (WIDTH // 2 - p1_label.get_width() // 2, 100))

        p1_color_rect = pygame.Rect(WIDTH // 2 - 50, 150, 100, 30)
        pygame.draw.rect(screen, PADDLE_COLORS[p1_index], p1_color_rect)
        pygame.draw.rect(screen, WHITE, p1_color_rect, 2)

        p1_left = small_font.render("A", True, WHITE)
        p1_right = small_font.render("D", True, WHITE)
        screen.blit(p1_left, (WIDTH // 2 - 100, 155))
        screen.blit(p1_right, (WIDTH // 2 + 80, 155))

        p2_label = font.render("Player 2 Color", True, WHITE)
        screen.blit(p2_label, (WIDTH // 2 - p2_label.get_width() // 2, 250))

        p2_color_rect = pygame.Rect(WIDTH // 2 - 50, 300, 100, 30)
        pygame.draw.rect(screen, PADDLE_COLORS[p2_index], p2_color_rect)
        pygame.draw.rect(screen, WHITE, p2_color_rect, 2)

        p2_left = small_font.render("Left", True, WHITE)
        p2_right = small_font.render("Right", True, WHITE)
        screen.blit(p2_left, (WIDTH // 2 - 100, 305))
        screen.blit(p2_right, (WIDTH // 2 + 70, 305))

        continue_text = small_font.render("Press Enter to continue", True, WHITE)
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT - 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    p1_index = (p1_index - 1) % len(PADDLE_COLORS)
                elif event.key == pygame.K_d:
                    p1_index = (p1_index + 1) % len(PADDLE_COLORS)
                elif event.key == pygame.K_LEFT:
                    p2_index = (p2_index - 1) % len(PADDLE_COLORS)
                elif event.key == pygame.K_RIGHT:
                    p2_index = (p2_index + 1) % len(PADDLE_COLORS)
                elif event.key == pygame.K_RETURN:
                    return PADDLE_COLORS[p1_index], PADDLE_COLORS[p2_index]


def show_main_menu():
    menu_options = ["Single Player", "Local Multiplayer", "How to Play", "Exit"]
    selected = 0
    while True:
        draw_menu(menu_options, selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if menu_options[selected] == "Single Player":
                        return "single"
                    elif menu_options[selected] == "Local Multiplayer":
                        return "local"
                    elif menu_options[selected] == "How to Play":
                        show_how_to_play()
                    elif menu_options[selected] == "Exit":
                        pygame.quit()
                        sys.exit()

def show_how_to_play():
    while True:
        screen.fill(BLACK)

        lines = [
            "To win the game,",
            "a player needs to either earn 10 points",
            "or cause the opponent to lose 3 lives",
            "",
            "Controls:",
            "Player 1: W (up), S (down)",
            "Player 2: UP arrow (up), DOWN arrow (down)",
            "Pause: P",
            "",
            "Press BACKSPACE to return to menu"
        ]

        for i, line in enumerate(lines):
            rendered = font.render(line, True, WHITE)
            screen.blit(rendered, (WIDTH // 2 - rendered.get_width() // 2, 100 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    return

def pause_menu():
    options = ["Resume", "Restart Game", "Return to Main Menu"]
    selected = 0
    title_font = pygame.font.SysFont("Arial", 48)

    while True:
        screen.fill(BLACK)

        title_text = title_font.render("Paused", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = WHITE if i != selected else (100, 255, 100)
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "Resume"
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected]


def victory_screen(winner):
    options = ["Play Again!", "Return to Main Menu"]
    selected = 0
    title_font = pygame.font.SysFont("Arial", 48)

    while True:
        screen.fill(BLACK)

        win_text = title_font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 100))

        for i, option in enumerate(options):
            color = WHITE if i != selected else (100, 255, 100)
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[selected]

def draw_lives(lives, max_lives, x, y, color):
    square_size = 20
    spacing = 10
    for i in range(max_lives):
        if i < lives:
            square_color = color
        else:
            square_color = GRAY
        rect = pygame.Rect(x + i * (square_size + spacing), y, square_size, square_size)
        pygame.draw.rect(screen, square_color, rect)


def draw(p1_paddle, p2_paddle, ball, score1, score2, lives1, lives2, color1, color2):
    screen.fill(BLACK)
    p1_paddle.draw(screen)
    p2_paddle.draw(screen)
    ball.draw(screen)

    for y in range(0, HEIGHT, 20):
        pygame.draw.line(screen, WHITE, (WIDTH // 2, y), (WIDTH // 2, y + 10))

    text1 = font.render(str(score1), True, WHITE)
    text2 = font.render(str(score2), True, WHITE)
    screen.blit(text1, (WIDTH // 4 - text1.get_width() // 2, 20))
    screen.blit(text2, (WIDTH * 3 // 4 - text2.get_width() // 2, 20))

    draw_lives(lives1, 3, 50, 60, color1)
    draw_lives(lives2, 3, WIDTH - 50 - 3 * 30, 60, color2)

    pygame.display.flip()

def run_single_player(player_color=WHITE, ai_color=WHITE):
    player_lives = 3
    ai_lives = 3
    clock = pygame.time.Clock()
    player_paddle = Paddle(10, player_color)
    ai_paddle = Paddle(WIDTH - 20, ai_color)
    ball = Ball()
    player_score = 0
    ai_score = 0

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                choice = pause_menu()
                if choice == "Resume":
                    continue
                elif choice == "Restart Game":
                    return run_single_player(player_color, ai_color)
                elif choice == "Return to Main Menu":
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_paddle.move(up=True)
        if keys[pygame.K_s]:
            player_paddle.move(up=False)

        if ball.rect.centery > ai_paddle.rect.centery + 10:
            ai_paddle.move(up=False)
        elif ball.rect.centery < ai_paddle.rect.centery - 10:
            ai_paddle.move(up=True)

        ball.move()

        if ball.rect.colliderect(player_paddle.rect) and ball.dx < 0:
            ball.dx *= -1
            p1_score += 1
        if ball.rect.colliderect(ai_paddle.rect) and ball.dx > 0:
            ball.dx *= -1
            p2_score += 1

        if ball.x < 0:
            ai_score += 1
            player_lives -= 1
            score_sound.play()
            if player_lives == 0:
                winner = "AI"
                choice = victory_screen(winner)
                if choice == "Play Again!":
                    return run_single_player(player_color, ai_color)
                else:
                    return
            ball.reset()

        elif ball.x > WIDTH:
            player_score += 1
            ai_lives -= 1
            score_sound.play()
            if ai_lives == 0:
                winner = "Player"
                choice = victory_screen(winner)
                if choice == "Play Again!":
                    return run_single_player(player_color, ai_color)
                else:
                    return
            ball.reset()

        if player_score == WINNING_SCORE or ai_score == WINNING_SCORE:
            winner = "Player" if player_score == WINNING_SCORE else "AI"
            choice = victory_screen(winner)
            if choice == "Play Again!":
                return run_single_player(player_color, ai_color)
            else:
                return

        draw(player_paddle, ai_paddle, ball, player_score, ai_score, player_lives, ai_lives, player_color, ai_color)


def run_local_multiplayer(p1_color=WHITE, p2_color=WHITE):
    p1_lives = 3
    p2_lives = 3
    clock = pygame.time.Clock()
    p1_paddle = Paddle(10, p1_color)
    p2_paddle = Paddle(WIDTH - 20, p2_color)
    ball = Ball()
    p1_score = 0
    p2_score = 0

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                choice = pause_menu()
                if choice == "Resume":
                    continue
                elif choice == "Restart Game":
                    return run_local_multiplayer(p1_color, p2_color)
                elif choice == "Return to Main Menu":
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            p1_paddle.move(up=True)
        if keys[pygame.K_s]:
            p1_paddle.move(up=False)
        if keys[pygame.K_UP]:
            p2_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            p2_paddle.move(up=False)

        ball.move()

        if ball.rect.colliderect(p1_paddle.rect) and ball.dx < 0:
            ball.dx *= -1
        if ball.rect.colliderect(p2_paddle.rect) and ball.dx > 0:
            ball.dx *= -1

        if ball.x < 0:
            p2_score += 1
            p1_lives -= 1
            score_sound.play()
            if p1_lives == 0:
                winner = "Player 2"
                choice = victory_screen(winner)
                if choice == "Play Again!":
                    return run_local_multiplayer(p1_paddle.color, p2_paddle.color)
                else:
                    return
            ball.reset()

        elif ball.x > WIDTH:
            p1_score += 1
            p2_lives -= 1
            score_sound.play()
            if p2_lives == 0:
                winner = "Player 1"
                choice = victory_screen(winner)
                if choice == "Play Again!":
                    return run_local_multiplayer(p1_paddle.color, p2_paddle.color)
                else:
                    return
            ball.reset()

        if p1_score == WINNING_SCORE or p2_score == WINNING_SCORE:
            winner = "Player 1" if p1_score == WINNING_SCORE else "Player 2"
            choice = victory_screen(winner)
            if choice == "Play Again!":
                return run_local_multiplayer(p1_color, p2_color)
            else:
                return

        draw(p1_paddle, p2_paddle, ball, p1_score, p2_score, p1_lives, p2_lives, p1_color, p2_color)

def main():
    show_start_screen()

    while True:
        choice = show_main_menu()
        if choice == "local":
            color1, color2 = color_selection_screen()
            run_local_multiplayer(color1, color2)
        elif choice == "single":
            color1, color2 = color_selection_screen()
            run_single_player(color1, color2)

if __name__ == "__main__":
    main()
