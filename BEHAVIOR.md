# Behavior

The page has a title, subtitle `Agent: X, Human: O`, New Game button, Who Starts toggle, Agent Type dropdown, nine-cell board, and a status line below it.

On load, show an empty disabled board and `Press New Game to start.` Send no API request. Who Starts defaults to Agent. Agent Type defaults to Random. Q-table is visible but disabled with `coming soon`.

Who Starts toggles Agent/Human only before a game or after it ends. Lock it while a game or request is active. Agent Type remains enabled during a game; currently Random is its only supported option.

New Game starts an empty board. If Agent starts, send the empty board with agent=random and show the returned X. If Human starts, show `Your turn` and send nothing until a square is clicked. New Game may abandon an active game and invalidates any outstanding response.

A human click on an empty square places O locally, then sends the full board and chosen agent to POST /api/move. Lock all cells and show `Agent is thinking…` while waiting. Rapid repeated clicks cannot place multiple O marks. Occupied cells stay disabled.

On a successful response, display the returned board. Playing means `Your turn`. End states mean `Agent wins!`, `You win!`, or `It's a draw!`. Highlight the returned winning squares and disable every cell after the game ends. New Game and Who Starts remain available.

Show API error messages in red. A network failure shows exactly `Cannot reach the server.` in red. Invalid/non-JSON server responses also show an error in red. End the interrupted game and allow New Game; never leave the page stuck waiting.

No scoreboard, storage, learning or trained-agent selector is required for this submission. The scoreboard in the presentation is a practice exercise, not part of the main game specification.
