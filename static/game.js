const game = document.querySelector('#game');
const cells = [...document.querySelectorAll('.cell')];
const statusLine = document.querySelector('#status');
const whoStarts = document.querySelector('#who-starts');
const agentType = document.querySelector('#agent-type');
let starter = 'X';
let board = '.........';
let active = false;
let busy = false;
let generation = 0;

function message(text, error = false) {
  statusLine.textContent = text;
  statusLine.classList.toggle('error', error);
}

function render(line = []) {
  whoStarts.textContent = `Who Starts: ${starter === 'X' ? 'Agent' : 'Human'}`;
  whoStarts.disabled = active || busy;
  cells.forEach((cell, i) => {
    const mark = board[i];
    cell.textContent = mark === '.' ? '' : mark;
    cell.dataset.mark = mark;
    cell.disabled = !active || busy || mark !== '.';
    cell.classList.toggle('winner', line.includes(i));
    cell.setAttribute('aria-label', `Row ${Math.floor(i / 3) + 1}, column ${i % 3 + 1}, ${mark === '.' ? 'empty' : mark}`);
  });
}

async function requestMove() {
  const thisGame = generation;
  busy = true;
  message('Agent is thinking…');
  render();
  let response;
  try {
    response = await fetch(game.dataset.apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ board, agent: agentType.value }),
    });
  } catch {
    if (thisGame !== generation) return;
    busy = false;
    active = false;
    message('Cannot reach the server.', true);
    render();
    return;
  }
  if (thisGame !== generation) return;
  try {
    const data = await response.json();
    if (thisGame !== generation) return;
    if (!response.ok) throw new Error(data.error || 'Server error. Start a new game.');
    board = data.board;
    busy = false;
    active = data.status === 'playing';
    const messages = { playing: 'Your turn', agent_wins: 'Agent wins!', human_wins: 'You win!', draw: "It's a draw!" };
    message(messages[data.status]);
    render(data.winning_line || []);
  } catch (error) {
    if (thisGame !== generation) return;
    busy = false;
    active = false;
    message(error.message || 'Server error. Start a new game.', true);
    render();
  }
}

whoStarts.addEventListener('click', () => {
  if (active || busy) return;
  starter = starter === 'X' ? 'O' : 'X';
  render();
});

document.querySelector('#new-game').addEventListener('click', () => {
  generation += 1;
  board = '.........';
  busy = false;
  active = true;
  if (starter === 'X') requestMove();
  else {
    message('Your turn');
    render();
  }
});

cells.forEach((cell, i) => cell.addEventListener('click', () => {
  if (!active || busy || board[i] !== '.') return;
  board = board.slice(0, i) + 'O' + board.slice(i + 1);
  requestMove();
}));
render();
