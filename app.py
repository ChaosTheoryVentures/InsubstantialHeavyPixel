from flask import Flask, render_template, jsonify
from stable_baselines3 import PPO
import numpy as np
from snake_env import SnakeBattleEnv

app = Flask(__name__)

# Load AI models
model1 = PPO.load("snake1_ppo")
model2 = PPO.load("snake2_ppo")

# Create environment
env = SnakeBattleEnv(grid_size=15)
obs, _ = env.reset()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state')
def game_state():
    """Runs AI and sends updated game state to frontend."""
    global obs

    # Get AI actions
    action1, _ = model1.predict(obs)
    action2, _ = model2.predict(obs)

    # Step in the environment
    obs, _, done, _, _ = env.step([action1, action2])

    # Reset if game ends
    if done:
        obs, _ = env.reset()

    # Convert state to JSON
    state = {
        "snake1": env.snake1,  # Green Snake
        "snake2": env.snake2,  # Blue Snake
        "food": env.food       # Red Food
    }
    return jsonify(state)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
