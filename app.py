# app.py
from flask import Flask, jsonify, render_template
from snake_env import SnakeEnv
from stable_baselines3 import PPO
import os

app = Flask(__name__, static_folder='.', template_folder='.')

# Initialize the environment and load the initial observation
env = SnakeEnv()
obs = env.reset()

# Load AI models. Ensure your model files are named snake1_ppo.zip and snake2_ppo.zip.
MODEL1_PATH = 'snake1_ppo.zip'
MODEL2_PATH = 'snake2_ppo.zip'
if os.path.exists(MODEL1_PATH) and os.path.exists(MODEL2_PATH):
    model1 = PPO.load(MODEL1_PATH)
    model2 = PPO.load(MODEL2_PATH)
    print("AI models loaded successfully.")
else:
    model1 = None
    model2 = None
    print("Warning: AI model files not found. Falling back to random actions.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state')
def game_state():
    global obs, env
    # Get actions from AI models (or random if models are not available)
    if model1 is not None and model2 is not None:
        action1, _ = model1.predict(obs)
        action2, _ = model2.predict(obs)
    else:
        import random
        action1 = random.choice([0, 1, 2, 3])
        action2 = random.choice([0, 1, 2, 3])

    obs, reward, done, info = env.step([action1, action2])
    if done:
        obs = env.reset()

    # Prepare the game state for the front-end
    state = {
        'snake1': [{'x': x, 'y': y} for x, y in env.snake1],
        'snake2': [{'x': x, 'y': y} for x, y in env.snake2],
        'food': {'x': env.food[0], 'y': env.food[1]}
    }
    return jsonify(state)

if __name__ == '__main__':
    # Run on 0.0.0.0 so that Replit can access it externally, on port 8080.
    app.run(host='0.0.0.0', port=8080)
