from .agent import Agent
import random

GRID_SIZE = 15 

# this agent move with A* algorithm

class gray(Agent):
    name = "gray"
    
    def __init__(self):
        super().__init__(self.name)
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def a_star(self, start, goal, rocks):
        open_set = set([start])
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if not (0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE):
                    continue
                if neighbor in rocks:
                    continue

                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    open_set.add(neighbor)
        return None
    
    def move(self, mice, rocks, beds):
        x, y = self.position
        if not mice:
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_pos = (x+dx, y+dy)
                if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
                    if new_pos not in rocks:
                        self.position = new_pos
                        break
            return

        if self.skip > 0:
            self.skip -= 1
            return

        paths = []
        for mouse in mice:
            path = self.a_star(self.position, mouse, rocks)
            if path:
                paths.append((len(path), path))

        if not paths:
            return

        _, best_path = min(paths, key=lambda x: x[0])
        if len(best_path) > 1:
            next_step = best_path[1]
            self.position = next_step