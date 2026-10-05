from .agent import Agent
from collections import deque
import random

GRID_SIZE = 15 

# this agent move with bfs algorithm

class BfsAgent(Agent):
    name = "BFS"
    
    def __init__(self):

        super().__init__( self.name)
    
    def bfs_path(self, start, goal, rocks):
        queue = deque([[start]])
        visited = set([start])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if (x, y) == goal:
                return path
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and neighbor not in rocks and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None
    
    def move(self, mice, rocks, beds):
        if self.skip > 0:
            self.skip -= 1
            return

        if not mice:
            directions = [(-1,0), (1,0), (0,-1), (0,1)]
            random.shuffle(directions)
            for dx, dy in directions:
                new_pos = (self.position[0]+dx, self.position[1]+dy)
                if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
                    if new_pos not in rocks:
                        self.position = new_pos
                        break
            return
        
        paths = []
        for mouse in mice:
            path = self.bfs_path(self.position, mouse, rocks)
            if path:
                paths.append((len(path), path))

        if not paths:
            return

        _, best_path = min(paths, key=lambda x: x[0])
        if len(best_path) > 1:
            next_step = best_path[1]
            self.position = next_step