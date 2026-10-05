# Multi-Agent Grid Simulation & Strategy Evaluation

A Python-based multi-agent simulation where autonomous agents compete in a grid environment to collect resources while avoiding hazards.

The project compares different decision-making strategies under **partial and probabilistic sensing** using a tournament-based evaluation system.

## Features

* Multi-agent grid-based simulation
* Multiple decision-making strategies:

  * Breadth-First Search (BFS)
  * A* Search
  * Random movement
* Partial and probabilistic environment sensing
* Procedurally generated game environments
* Reachability validation using BFS
* Resource collection and hazard avoidance
* Turn-based agent interaction
* Round-robin tournament evaluation
* Fair starting-position rotation between repeated matches
* Pygame visualization
* Automatic final ranking based on wins and total score

## How It Works

Each match takes place on a `15 × 15` grid containing:

* Mice — collectible resources
* Rocks — hazards that eliminate an agent
* Beds — obstacles that cause an agent to skip turns

Each agent receives limited information about nearby objects.

Objects within the visible radius are detected deterministically, while objects within the extended sensor range are detected probabilistically.

This creates an environment where agents must make decisions with incomplete information.

## Agent Strategies

### A* Agent

Uses the A* search algorithm to navigate toward detected objectives while considering obstacles.

### BFS Agent

Uses Breadth-First Search to find paths through the grid.

### Random Agent

Selects movements randomly and serves as a baseline strategy for comparison.

## Tournament System

Agents compete using a **round-robin tournament**.

Each pair of agents plays multiple matches, with starting positions alternated between games to reduce positional bias.

For each match:

* Reaching 5 mice ends the game with a win.
* Landing on a rock eliminates the agent.
* If the maximum number of turns is reached, the agent with the higher score wins.
* Equal scores at the turn limit result in a draw.

The final ranking is determined by:

1. Number of wins
2. Total score as a tie-breaker

## Environment Generation

Each game generates a new random environment containing:

* 15 mice
* 20 rocks
* 10 beds

Before a map is accepted, BFS verifies that both starting positions have reachable areas containing at least 5 mice.

This prevents the random map generator from creating heavily unbalanced starting conditions.

## Project Structure

```text
cattieGameAI/
│
├── agents/
│   ├── agent.py
│   ├── load_agents.py
│   ├── astar_agent.py
│   ├── bfs_agent.py
│   ├── random_agent.py
│   └── __init__.py
│
├── assets/
│   ├── cat1.png
│   ├── cat2.png
│   ├── mice.png
│   ├── rock.png
│   ├── catBed.png
│   └── grasss.png
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies

* Python
* Pygame
* BFS
* A* Search
* Multi-Agent Systems
* Probabilistic Sensing

## Installation

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## Run

From the project root:

```bash
python main.py
```

The simulation will run the tournament and display the final ranking after all matches are completed.

## Example Tournament Output

```text
===== AstarAgent vs RandomAgent =====
Game 1: AstarAgent won (3-0) - RandomAgent hit a rock
Game 2: AstarAgent won (2-0) - RandomAgent hit a rock
Game 3: AstarAgent won (0-0) - RandomAgent hit a rock

===== AstarAgent vs BfsAgent =====
Game 1: BfsAgent won (5-1) - BfsAg
```
