# API contract

GET `/` returns the HTML game. POST `/api/move` exchanges JSON.

Request: `{"board":"O........","agent":"random"}`. Both fields are required. `board` is exactly nine characters in row-major order, indexed 0–8: X is the agent placeholder, O is the human, . is empty. `agent` is the case-sensitive string `random`. No learned agent is included; `qtable` is reserved and rejected for now.

Success (200): `{"board":"O...X....","agent_move":4,"status":"playing","winning_line":null}`.

- `board`: complete resulting board string.
- `agent_move`: integer 0–8, or null if the submitted board is already terminal.
- `status`: exactly `playing`, `agent_wins`, `human_wins`, or `draw`.
- `winning_line`: three square indexes for a winning row, column or diagonal; otherwise null. Where more than one line wins, return the first in the server's line order.

A finished human board returns its result without adding X. Otherwise add exactly one X to an empty square, uniformly at random. This is a placeholder, not an Agent class or trained model.

Missing fields, malformed JSON, invalid board or unknown agent return status 400 with `{"error":"message"}`. GET `/api/move` returns 405. Invalid boards include wrong types/length/symbols, impossible counts, simultaneous winners, and impossible winning counts. A nonterminal position with more X than O is the human's turn and is rejected.

Either side may start. The unchanged slide contract carries no starter field; the server accepts positions reachable with either starter and checks that it can be X's turn. The browser locks Who Starts during a game. Each request includes the full board; there is no server-side game session.
