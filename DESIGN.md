# Design and review decisions

No separate design slide was attached. The layout retains the existing project's cream background, green text/buttons and rounded board squares; X is rust-colored and O is green. These visual choices are implementation assumptions, not teacher-supplied colors.

Order: title → Agent/Human subtitle → New Game, Who Starts and Agent Type controls → 3×3 board → status line. Controls wrap on narrow screens. A winning line uses a pale green background. Errors use dark red. Buttons have visible keyboard focus, and every cell has a row/column/mark label. Status changes are announced to assistive technology.

The presentation's controls take precedence over the earlier page: New Game is a button, Who Starts is a toggle and Agent Type is a dropdown. No author name is invented from the example slide.

Review decisions: follow the exact new status strings; require the new agent request field; support either starter without adding an undocumented field; use a random placeholder only; keep the earlier Q-learning project separate. Treat “without Agent” as excluding a learning Agent and model file, while retaining the random placeholder explicitly requested by the presentation.
