import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
WIN_SCORE = 10

# Game objects
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def reset_game():
    global paddle1_y, paddle2_y, ball_x, ball_y, ball_dx, ball_dy, score1, score2, game_over
    paddle1_y = paddle2_y = HEIGHT // 2 - 50
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx, ball_dy = 5, 3
    score1 = score2 = 0
    game_over = False

# Initialize game
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            # Check if play again button is clicked
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
            if button_rect.collidepoint(mouse_pos):
                reset_game()
    
    if not game_over:
        # Controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= 7
        if keys[pygame.K_s] and paddle1_y < HEIGHT - 100:
            paddle1_y += 7
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= 7
        if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - 100:
            paddle2_y += 7
        
        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy
        
        # Ball collision with top/bottom
        if ball_y <= 0 or ball_y >= HEIGHT - 20:
            ball_dy = -ball_dy
        
        # Ball collision with paddles
        if (ball_x <= 30 and paddle1_y <= ball_y <= paddle1_y + 100) or \
           (ball_x >= WIDTH - 50 and paddle2_y <= ball_y <= paddle2_y + 100):
            ball_dx = -ball_dx
        
        # Score and reset ball
        if ball_x < 0:
            score2 += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            if score2 >= WIN_SCORE:
                game_over = True
        elif ball_x > WIDTH:
            score1 += 1
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            if score1 >= WIN_SCORE:
                game_over = True
    
    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (10, paddle1_y, 20, 100))
    pygame.draw.rect(screen, RED, (WIDTH - 30, paddle2_y, 20, 100))
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, 20, 20))
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # Draw scores
    score1_text = font.render(str(score1), True, BLUE)
    score2_text = font.render(str(score2), True, RED)
    screen.blit(score1_text, (WIDTH // 4, 50))
    screen.blit(score2_text, (3 * WIDTH // 4, 50))
    
    # Show winner and play again button if game over
    if game_over:
        winner = "BLUE WINS!" if score1 >= WIN_SCORE else "RED WINS!"
        winner_text = font.render(winner, True, WHITE)
        screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - 50))
        
        # Draw play again button
        button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
        pygame.draw.rect(screen, GREEN, button_rect)
        play_again = small_font.render("PLAY AGAIN", True, BLACK)
        screen.blit(play_again, (WIDTH//2 - play_again.get_width()//2, HEIGHT//2 + 65))
    
    pygame.display.flip()
    clock.tick(60)
