import pygame
import random
import sys
import os

from collections import deque
from agents import load_agents

# visible radius = 3
# sensor_radius = 5
# sensor_probability = 0.3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except:
    pass

MAX_TURNS = 60
MATCHES_PER_PAIR = 3
CELL_SIZE = 50
GRID_SIZE = 15
WIDTH, HEIGHT = CELL_SIZE * GRID_SIZE, CELL_SIZE * GRID_SIZE + 50
FPS = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (200, 50, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("C(aXORu)ttie Tournament!")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 50)

mice_img = pygame.transform.scale(pygame.image.load("assets/mice.png"), (50, 50))
rock_img = pygame.transform.scale(pygame.image.load("assets/rock.png"), (50, 50))
bed_img = pygame.transform.scale(pygame.image.load("assets/catBed.png"), (50, 50))
background = pygame.transform.scale(pygame.image.load("assets/grasss.png"), (750,800))
orangeCat = pygame.transform.scale(pygame.image.load("assets/cat1.png"), (52,52))
grayCat = pygame.transform.scale(pygame.image.load("assets/cat2.png"), (52,52))

#to check if every agent got a way to run away of rocks!
def bfs(start, rocks):
    visited = set()
    queue = deque([start])
    visited.add(start)
    while queue:
        x, y = queue.popleft()
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if (nx, ny) not in rocks and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return visited

#to find the objects around
def get_detected_objects(agent_pos, objects, sensor_radius, sensor_probability):
        detected = []
        for obj in objects:
            distance = abs(obj[0] - agent_pos[0]) + abs(obj[1] - agent_pos[1])
            
            if distance <= 3:
                detected.append(obj)
            elif distance <= sensor_radius and random.random() < sensor_probability:
                detected.append(obj)
        return detected

#generates random position
def random_pos(exclude):
    while True:
        pos = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        if pos not in exclude:
            return pos

def generate_map(start1, start2):
    while True:
        mice = set()
        rocks = set()
        beds = set()
        for _ in range(15):
            mice.add(random_pos(mice | rocks | beds | {start1, start2}))
        for _ in range(20):
            rocks.add(random_pos(mice | rocks | beds | {start1, start2}))
        for _ in range(10):
            beds.add(random_pos(mice | rocks | beds | {start1, start2}))

        # agents should have at least 1 way to run away of rocks! 
        # checks it with bfs algorithm
        area1 = bfs(start1, rocks)
        area2 = bfs(start2, rocks)
        mice1 = mice & area1
        mice2 = mice & area2
        if len(mice1) >= 5 and len(mice2) >= 5:
            return mice, rocks, beds

def draw_game(agent1, agent2, mice, rocks, beds, turn):
    screen.blit(background, (0, 0))
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if (x, y) in rocks:
                screen.blit(rock_img, rect)
            elif (x, y) in beds:
                screen.blit(bed_img, rect)
            elif (x, y) in mice:
                screen.blit(mice_img, rect)
    screen.blit(grayCat, (agent1.position[0]*CELL_SIZE+5, agent1.position[1]*CELL_SIZE+5))
    screen.blit(orangeCat, (agent2.position[0]*CELL_SIZE+5, agent2.position[1]*CELL_SIZE+5))

    info = f"{agent1.name}: {agent1.score} | {agent2.name}: {agent2.score} | turn: {'1' if turn == 0 else '2'}"
    text = font.render(info, True, BLACK)
    screen.blit(text, (10, HEIGHT - 40))
    pygame.display.flip()


#game starts!
def match(agent1, agent2, swap_positions=False):
    
    if swap_positions:
        agent1.start_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
        agent2.start_pos = (0, 0)
        
    else:
        agent1.start_pos = (0, 0)
        agent2.start_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
        
        
    agent1.position = agent1.start_pos
    agent2.position = agent2.start_pos
    agent1.skip = 0
    agent2.skip = 0
    agent1.score = 0
    agent2.score = 0

    mice, rocks, beds = generate_map(
        agent1.start_pos,
        agent2.start_pos
    )

    turn = 0
    counter = 0
    while True:
        clock.tick(FPS)
        draw_game(agent1, agent2, mice, rocks, beds, turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        current = agent1 if turn == 0 else agent2
        other = agent2 if turn == 0 else agent1

        if current.skip > 0:
            current.skip -= 1
        else:
            sensor_radius = 5
            sensor_probability = 0.3

            detected_mice = get_detected_objects(
                current.position,
                mice,
                sensor_radius,
                sensor_probability
            )

            detected_rocks = get_detected_objects(
                current.position,
                rocks,
                sensor_radius,
                sensor_probability
            )

            detected_beds = get_detected_objects(
                current.position,
                beds,
                sensor_radius,
                sensor_probability
            )

            current.move(
                detected_mice,
                detected_rocks,
                detected_beds
            )

            # Agent hits a rock
            if current.position in rocks:
                return other, f"{current.name} hit a rock"

            # Agent steps on a bed
            if current.position in beds:
                current.skip = 2

            # Agent finds a mouse
            if current.position in mice:
                current.score += 1
                mice.remove(current.position)

        # Agent reaches 5 points
        if current.score >= 5:
            return current, f"{current.name} reached 5 points"

        turn = 1 - turn
        counter += 1

        # Maximum number of turns reached
        if counter >= MAX_TURNS:
            if current.score > other.score:
                return current, "Maximum turns reached"

            elif current.score < other.score:
                return other, "Maximum turns reached"

            else:
                return None, "Maximum turns reached - draw"


def tournament(agent_classes):
    wins = {cls.__name__: 0 for cls in agent_classes}
    total_scores = {cls.__name__: 0 for cls in agent_classes}

    for i in range(len(agent_classes)):
        for j in range(i + 1, len(agent_classes)):
            class1 = agent_classes[i]
            class2 = agent_classes[j]

            print(f"\n===== {class1.__name__} vs {class2.__name__} =====")

            for game in range(MATCHES_PER_PAIR):
                agent1 = class1()
                agent2 = class2()

                agent1.name = class1.__name__
                agent2.name = class2.__name__

                winner, reason = match(
                    agent1,
                    agent2,
                    swap_positions=(game % 2 == 1)
                )
                
                total_scores[agent1.name] += agent1.score
                total_scores[agent2.name] += agent2.score
                if winner is agent1:
                    wins[agent1.name] += 1
                    print(
                        f"Game {game + 1}: "
                        f"{agent1.name} won "
                        f"({agent1.score}-{agent2.score}) "
                        f"- {reason}"
                    )

                elif winner is agent2:
                    wins[agent2.name] += 1
                    print(
                        f"Game {game + 1}: "
                        f"{agent2.name} won "
                        f"({agent2.score}-{agent1.score}) "
                        f"- {reason}"
                    )

                else:
                    print(
                        f"Game {game + 1}: "
                        f"Draw "
                        f"({agent1.score}-{agent2.score}) "
                        f"- {reason}"
                    )

    ranking = sorted(
        agent_classes,
        key=lambda cls: (
            wins[cls.__name__],
            total_scores[cls.__name__]
        ),
        reverse=True
    )

    final_winner = ranking[0]

    return final_winner, wins, total_scores


def show_results(wins, scores, final_winner):
    ranking = sorted(
        wins,
        key=lambda name: (
            wins[name],
            scores[name]
        ),
        reverse=True
    )

    screen.blit(background, (0, 0))

    title = big_font.render("Tournament Winner", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    winner_text = font.render(
        f"Winner: {final_winner.__name__}",
        True,
        RED
    )
    screen.blit(
        winner_text,
        (WIDTH // 2 - winner_text.get_width() // 2, 70)
    )

    title2 = big_font.render("Final Ranking", True, BLACK)
    screen.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 130))

    y = 180

    for i, name in enumerate(ranking, start=1):
        text = font.render(
            f"{i}. {name} - Wins: {wins[name]} | Score: {scores[name]}",
            True,
            BLACK
        )

        screen.blit(text, (50, y))
        y += 30

    pygame.display.flip()

    print("\n===== Tournament Results =====")
    print(f"Winner: {final_winner.__name__}")

    for i, name in enumerate(ranking, start=1):
        print(
            f"{i}. {name} - "
            f"Wins: {wins[name]} | "
            f"Score: {scores[name]}"
        )

    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

if __name__ == "__main__":
    agents = load_agents()
    final_winner, wins, scores = tournament(agents)
    show_results(wins, scores, final_winner)