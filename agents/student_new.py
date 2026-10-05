from .agent import Agent
import random

GRID_SIZE = 15 

# this agent moves randomly

class RandomAgent(Agent):
    name = "random"
    def __init__(self):
        super().__init__(self.name)
        
    def move(self, mice, rocks, beds):
        x, y = self.position
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
                self.position = new_pos
                break

    
