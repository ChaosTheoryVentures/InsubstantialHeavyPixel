# snake_env.py
import random

class SnakeEnv:
    def __init__(self, grid_size=15):
        self.grid_size = grid_size
        self.reset()

    def reset(self):
        # Initialize snake starting positions
        self.snake1 = [(2, 2)]
        self.snake2 = [(self.grid_size - 3, self.grid_size - 3)]
        self.food = self._spawn_food()
        self.done = False
        return self._get_obs()

    def _get_obs(self):
        # In this simplified example, the observation is a dictionary.
        obs = {
            'snake1': self.snake1,
            'snake2': self.snake2,
            'food': self.food
        }
        return obs

    def step(self, actions):
        # actions: list of two integers (0: up, 1: right, 2: down, 3: left)
        action1, action2 = actions
        self._move_snake(1, action1)
        self._move_snake(2, action2)
        self._check_food(1)
        self._check_food(2)
        self.done = self._check_collisions()
        reward = 0  # Rewards are not used for visualization.
        obs = self._get_obs()
        return obs, reward, self.done, {}

    def _move_snake(self, snake_number, action):
        if snake_number == 1:
            head = self.snake1[0]
            new_head = self._get_new_head(head, action)
            self.snake1.insert(0, new_head)
            self.snake1.pop()  # Remove tail
        elif snake_number == 2:
            head = self.snake2[0]
            new_head = self._get_new_head(head, action)
            self.snake2.insert(0, new_head)
            self.snake2.pop()  # Remove tail

    def _get_new_head(self, head, action):
        x, y = head
        if action == 0:    # up
            y -= 1
        elif action == 1:  # right
            x += 1
        elif action == 2:  # down
            y += 1
        elif action == 3:  # left
            x -= 1

        # Clamp the new head within grid bounds
        x = max(0, min(self.grid_size - 1, x))
        y = max(0, min(self.grid_size - 1, y))
        return (x, y)

    def _check_food(self, snake_number):
        if snake_number == 1:
            head = self.snake1[0]
            if head == self.food:
                # Grow snake1 by repeating the tail segment
                self.snake1.append(self.snake1[-1])
                self.food = self._spawn_food()
        elif snake_number == 2:
            head = self.snake2[0]
            if head == self.food:
                self.snake2.append(self.snake2[-1])
                self.food = self._spawn_food()

    def _spawn_food(self):
        while True:
            food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if food not in self.snake1 and food not in self.snake2:
                return food

    def _check_collisions(self):
        # End the game if the snakes' heads collide or if a snake collides with its own body or the other snake.
        head1 = self.snake1[0]
        head2 = self.snake2[0]
        if head1 == head2:
            return True
        if head1 in self.snake1[1:] or head1 in self.snake2:
            return True
        if head2 in self.snake2[1:] or head2 in self.snake1:
            return True
        return False
