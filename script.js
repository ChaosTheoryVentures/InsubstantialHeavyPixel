// script.js
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const cellSize = 40; // Each grid cell is 40x40 pixels

function drawGame(state) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw the food (red square)
  if (state.food) {
    ctx.fillStyle = 'red';
    ctx.fillRect(state.food.x * cellSize, state.food.y * cellSize, cellSize, cellSize);
  }

  // Draw snake 1 (green)
  if (state.snake1 && state.snake1.length) {
    ctx.fillStyle = 'green';
    state.snake1.forEach(segment => {
      ctx.fillRect(segment.x * cellSize, segment.y * cellSize, cellSize, cellSize);
    });
  }

  // Draw snake 2 (blue)
  if (state.snake2 && state.snake2.length) {
    ctx.fillStyle = 'blue';
    state.snake2.forEach(segment => {
      ctx.fillRect(segment.x * cellSize, segment.y * cellSize, cellSize, cellSize);
    });
  }
}

function fetchGameState() {
  fetch('/game_state')
    .then(response => response.json())
    .then(state => {
      drawGame(state);
    })
    .catch(error => {
      console.error('Error fetching game state:', error);
    });
}

// Poll the game state every 200ms
setInterval(fetchGameState, 200);
