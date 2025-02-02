import gymnasium as gym
import numpy as np
from gymnasium import spaces

class SnakeBattleEnv(gym.Env):
    """Custom environment where two AI snakes compete for food."""
    def __init__(self, grid_size=15):
        super(SnakeBattleEnv, self).__init__()
        self.grid_size = grid_size

        # Action Space: 4 Possible Moves for Each Snake
        self.action_space = spaces.MultiDiscrete([4, 4])  # [Snake1 Action, Snake2 Action]

        # Observation Space: 3D Grid Representation
        self.observation_space = spaces.Box(low=0, high=1, shape=(grid_size, grid_size, 3), dtype=np.float32)

        self.reset()

    def reset(self, seed=None, options=None):
        """Resets the game and returns the initial observation."""
        self.snake1 = [(5, 5)]
        self.snake2 = [(10, 10)]
        self.food = self._spawn_food()
        self.done = False
        return self._get_observation(), {}

    def step(self, actions):
        """Executes actions for both snakes and updates the game state."""
        reward1, reward2 = 0, 0

        # Move Snakes
        self.snake1.insert(0, self._move(self.snake1[0], actions[0]))
        self.snake2.insert(0, self._move(self.snake2[0], actions[1]))

        # Check for food
        if self.snake1[0] == self.food:
            reward1 += 10
            self.food = self._spawn_food()
        else:
            self.snake1.pop()

        if self.snake2[0] == self.food:
            reward2 += 10
            self.food = self._spawn_food()
        else:
            self.snake2.pop()

        # Check collisions
        if self._is_collision(self.snake1[0], self.snake1) or self._is_collision(self.snake1[0], self.snake2):
            reward1 -= 10
            self.done = True

        if self._is_collision(self.snake2[0], self.snake2) or self._is_collision(self.snake2[0], self.snake1):
            reward2 -= 10
            self.done = True

        return self._get_observation(), reward1, self.done, False, {}

    def _move(self, position, action):
        """Moves the snake based on the action (0=UP, 1=RIGHT, 2=DOWN, 3=LEFT)."""
        x, y = position
        if action == 0 and y > 0: y -= 1
        elif action == 1 and x < self.grid_size - 1: x += 1
        elif action == 2 and y < self.grid_size - 1: y += 1
        elif action == 3 and x > 0: x -= 1
        return (x, y)

    def _is_collision(self, position, snake):
        """Checks if a snake collides with itself or the wall."""
        x, y = position
        return (x < 0 or y < 0 or x >= self.grid_size or y >= self.grid_size or position in snake[1:])

    def _spawn_food(self):
        """Generates a new food location ensuring it's not inside a snake."""
        while True:
            food = (np.random.randint(0, self.grid_size), np.random.randint(0, self.grid_size))
            if food not in self.snake1 and food not in self.snake2:
                return food

    def _get_observation(self):
        """Creates a 3D NumPy array representation of the grid."""
        obs = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.float32)
        for x, y in self.snake1:
            obs[y, x, 0] = 1  # Snake 1 in Red Channel
        for x, y in self.snake2:
            obs[y, x, 1] = 1  # Snake 2 in Green Channel
        obs[self.food[1], self.food[0], 2] = 1  # Food in Blue Channel
        return obs
