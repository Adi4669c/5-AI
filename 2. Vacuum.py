#2 Vacuum Cleaner

import random

# ==========================================
# 1. SIMPLE REFLEX VACUUM AGENT
# ==========================================
class SimpleReflexVacuumAgent:
    """
    Decides actions based solely on current location status:
    - If Dirty -> SUCK
    - If Clean -> Move randomly
    """
    def act(self, location, status):
        if status == 'DIRTY':
            return 'SUCK'
        else:
            return random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])


# ==========================================
# 2. GOAL-BASED VACUUM AGENT
# ==========================================
class GoalBasedVacuumAgent:
    """
    Maintains an internal state model of the environment and plans 
    actions to achieve the target goal state (all locations clean).
    """
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.internal_model = {}  # Keeps track of cleaned/dirty locations

    def update_model(self, pos, status):
        self.internal_model[pos] = status

    def is_goal_achieved(self):
        # Goal state: Every known cell is CLEAN and all grid squares explored
        if len(self.internal_model) < self.grid_size[0] * self.grid_size[1]:
            return False
        return all(status == 'CLEAN' for status in self.internal_model.values())

    def choose_action(self, current_pos, current_status):
        self.update_model(current_pos, current_status)

        # Priority 1: If current spot is dirty, clean it immediately
        if current_status == 'DIRTY':
            return 'SUCK'

        # Goal check
        if self.is_goal_achieved():
            return 'STOP'

        # Priority 2: Navigate toward nearest known dirty spot or unexplored location
        r, c = current_pos
        neighbors = {
            'UP': (r - 1, c),
            'DOWN': (r + 1, c),
            'LEFT': (r, c - 1),
            'RIGHT': (r, c + 1)
        }

        # Filter valid moves within boundary
        valid_moves = {
            move: pos for move, pos in neighbors.items()
            if 0 <= pos[0] < self.grid_size[0] and 0 <= pos[1] < self.grid_size[1]
        }

        # Prefer moves to unexplored or dirty neighbors
        for move, pos in valid_moves.items():
            if self.internal_model.get(pos) == 'DIRTY' or pos not in self.internal_model:
                return move

        # Fallback: Move to any valid adjacent cell to keep exploring
        return random.choice(list(valid_moves.keys()))


# ==========================================
# 3. ENVIRONMENT SIMULATION
# ==========================================
class Environment:
    def __init__(self, rows=2, cols=2):
        self.rows = rows
        self.cols = cols
        # Randomly initialize dirt state for each cell
        self.grid = {
            (r, c): random.choice(['CLEAN', 'DIRTY'])
            for r in range(rows) for c in range(cols)
        }

    def get_status(self, pos):
        return self.grid[pos]

    def clean(self, pos):
        self.grid[pos] = 'CLEAN'

    def display(self, agent_pos):
        print("\n--- Current Grid State ---")
        for r in range(self.rows):
            row_str = ""
            for c in range(self.cols):
                status = self.grid[(r, c)]
                pos_str = f"[{'A:' if (r, c) == agent_pos else ''}{status[:1]}]"
                row_str += f"{pos_str:^8}"
            print(row_str)


# ==========================================
# 4. RUN SIMULATIONS
# ==========================================
def run_reflex_demo():
    print("\n" + "="*40)
    print("      SIMPLE REFLEX AGENT DEMO")
    print("="*40)
    
    env = Environment(rows=2, cols=2)
    agent = SimpleReflexVacuumAgent()
    current_pos = (0, 0)

    for step in range(1, 6):
        status = env.get_status(current_pos)
        action = agent.act(current_pos, status)
        print(f"Step {step} | Pos: {current_pos} | Status: {status} -> Action: {action}")

        if action == 'SUCK':
            env.clean(current_pos)
        else:
            r, c = current_pos
            if action == 'UP': current_pos = (max(0, r - 1), c)
            elif action == 'DOWN': current_pos = (min(env.rows - 1, r + 1), c)
            elif action == 'LEFT': current_pos = (r, max(0, c - 1))
            elif action == 'RIGHT': current_pos = (r, min(env.cols - 1, c + 1))


def run_goal_based_demo():
    print("\n" + "="*40)
    print("      GOAL-BASED AGENT DEMO")
    print("="*40)

    env = Environment(rows=2, cols=2)
    agent = GoalBasedVacuumAgent(grid_size=(2, 2))
    current_pos = (0, 0)
    step = 1

    while step <= 10:
        status = env.get_status(current_pos)
        action = agent.choose_action(current_pos, status)
        print(f"Step {step} | Pos: {current_pos} | Status: {status} -> Action: {action}")

        if action == 'STOP':
            print("\nGoal Achieved! All rooms are clean.")
            break
        elif action == 'SUCK':
            env.clean(current_pos)
        else:
            r, c = current_pos
            if action == 'UP': current_pos = (r - 1, c)
            elif action == 'DOWN': current_pos = (r + 1, c)
            elif action == 'LEFT': current_pos = (r, c - 1)
            elif action == 'RIGHT': current_pos = (r, c + 1)
        
        step += 1


if __name__ == "__main__":
    run_reflex_demo()
    run_goal_based_demo()
