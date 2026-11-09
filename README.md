# Flask Tic-Tac-Toe — submission without Agent

Prepared for **הגשת שרת Flask TTT נטול Agent**, due **16 November 2026**. This is the separate submission version following the newly supplied presentation. It contains a Flask server and complete client with a random-move placeholder. There is no learning Agent, Q-table, training code or model dependency.

The random placeholder follows the presentation's explicit generation example. The earlier Q-learning project remains separate.

## Run

From this folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. If that port is occupied:

```sh
python -m flask --app app run --port 5056
```

The app uses Flask's local development server with debug disabled by default.

## Files

- `app.py`: complete page route and random-placeholder API, with a TODO for future learned-agent integration.
- `templates/index.html`: Jinja page, all controls and nine board buttons.
- `static/style.css`, `static/game.js`: styling and client behavior.
- `CONTRACT.md`, `BEHAVIOR.md`, `DESIGN.md`: the agreement, behavior checklist, design assumptions and decisions used for this version.
- `test_app.py`: automated API and page checks.

Run `python -m unittest discover -v` for the tests.

## Check the page

1. Reload: empty disabled board; no API request until New Game.
2. Default Agent starts: New Game shows one X and then Your turn.
3. Finish a game or reload, toggle to Human and press New Game: empty active board; no move request before a human click.
4. During play, Who Starts is locked; Agent Type stays enabled, with Q-table disabled.
5. Click rapidly: only one human move before each server reply.
6. On a win, highlight the winning squares and disable the board. New Game still works.
7. Stop Flask and click a square: Cannot reach the server. appears in red. Start Flask again and press New Game to recover.

## GitHub submission

Publish this folder as the repository `ttt-flask-submission`. Submit the repository URL to the assignment; a localhost game link is not the requested submission.

Include app.py, templates/, static/, requirements.txt, the specifications and tests. Do not upload .venv/, caches, credentials or the separate Q-learning project. The included .gitignore excludes local environment files.

If uploading through GitHub's website, create the repository, choose Add file → Upload files, and drag this folder's **contents** into it. Keep app.py at the repository root and preserve the templates and static folders. Commit the files, then copy the repository's URL.
