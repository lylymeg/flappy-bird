import pygame
import random
import sys

pygame.init()

# Dimensions et paramètres
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Light")
clock = pygame.time.Clock()

# Couleurs
SKY_BLUE = (35, 45, 60)
BIRD_COLOR = (0, 255, 157)   # Vert néon
PIPE_COLOR = (0, 162, 255)   # Bleu
WHITE = (255, 255, 255)
RED = (255, 75, 75)
GRAY = (150, 150, 150)

# Physique & Tuyaux
GRAVITY = 0.25
JUMP_STRENGTH = -6.5
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # Millisecondes entre chaque paire de tuyaux

# Polices
font_large = pygame.font.SysFont("Arial", 40, bold=True)
font_medium = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

def create_pipe_pair():
    gap_y = random.randint(100, HEIGHT - 100 - PIPE_GAP)
    top_rect = pygame.Rect(WIDTH, 0, 50, gap_y)
    bottom_rect = pygame.Rect(WIDTH, gap_y + PIPE_GAP, 50, HEIGHT - (gap_y + PIPE_GAP))
    return {
        "top": top_rect,
        "bottom": bottom_rect,
        "passed": False
    }

def reset_game():
    return {
        "bird": pygame.Rect(80, HEIGHT // 2, 24, 24),
        "movement": 0,
        "pipes": [],
        "score": 0,
        "game_over": False
    }

game = reset_game()
high_score = 0
last_pipe_time = pygame.time.get_ticks()

running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game["game_over"]:
                    game["movement"] = JUMP_STRENGTH
                else:
                    game = reset_game()
                    last_pipe_time = current_time

    screen.fill(SKY_BLUE)

    if not game["game_over"]:
        # 1. Génération des tuyaux
        if current_time - last_pipe_time > PIPE_FREQUENCY:
            game["pipes"].append(create_pipe_pair())
            last_pipe_time = current_time

        # 2. Physique de l'oiseau
        game["movement"] += GRAVITY
        game["bird"].y += int(game["movement"])

        # 3. Déplacement des tuyaux, score & collisions
        active_pipes = []
        for pipe_pair in game["pipes"]:
            top_p = pipe_pair["top"]
            bot_p = pipe_pair["bottom"]

            top_p.x -= PIPE_SPEED
            bot_p.x -= PIPE_SPEED

            # Collision tuyau
            if game["bird"].colliderect(top_p) or game["bird"].colliderect(bot_p):
                game["game_over"] = True

            # Ingestion du score quand la paire de tuyaux est dépassée
            if top_p.right < game["bird"].left and not pipe_pair["passed"]:
                game["score"] += 1
                pipe_pair["passed"] = True

            # Garde uniquement les tuyaux encore visibles
            if top_p.right > 0:
                active_pipes.append(pipe_pair)

        game["pipes"] = active_pipes

        # Collision sol / plafond
        if game["bird"].top <= 0 or game["bird"].bottom >= HEIGHT:
            game["game_over"] = True

        if game["score"] > high_score:
            high_score = game["score"]

        # Dessin des tuyaux
        for pipe_pair in game["pipes"]:
            pygame.draw.rect(screen, PIPE_COLOR, pipe_pair["top"], border_radius=6)
            pygame.draw.rect(screen, PIPE_COLOR, pipe_pair["bottom"], border_radius=6)

        # Dessin de l'oiseau
        pygame.draw.ellipse(screen, BIRD_COLOR, game["bird"])

        # Affichage du score
        score_txt = font_medium.render(f"Score: {game['score']}", True, WHITE)
        screen.blit(score_txt, (20, 20))

    else:
        # Écran Game Over
        go_txt = font_large.render("GAME OVER", True, RED)
        final_score_txt = font_medium.render(f"Score: {game['score']}", True, WHITE)
        best_score_txt = font_medium.render(f"Meilleur score: {high_score}", True, BIRD_COLOR)
        replay_txt = font_small.render("Appuie sur ESPACE pour rejouer", True, GRAY)

        screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, 180))
        screen.blit(final_score_txt, (WIDTH // 2 - final_score_txt.get_width() // 2, 250))
        screen.blit(best_score_txt, (WIDTH // 2 - best_score_txt.get_width() // 2, 290))
        screen.blit(replay_txt, (WIDTH // 2 - replay_txt.get_width() // 2, 370))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()