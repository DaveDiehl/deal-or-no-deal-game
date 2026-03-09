# Deal or No Deal — Console Game Simulator

A text-console simulator that faithfully recreates the TV show *Deal or No Deal* experience, complete with the Banker's escalating offers, dramatic case reveals, the swap-or-keep finale, and a proveout/what-if mode.

---

## Setup

```bash
# Clone and enter the repo
git clone https://github.com/DaveDiehl/deal-or-no-deal-game.git
cd deal-or-no-deal-game

# Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Running the Game

```bash
python3 -m src.main
```

---

## Running the Tests

```bash
pytest -v
```

---

## Game Rules

### Overview
26 briefcases are placed on stage, each hiding one of 26 standard dollar amounts ranging from **$0.01** to **$1,000,000**. You pick one case to be yours — it stays hidden until the very end.

### Standard Dollar Amounts
```
$0.01    $1       $5       $10      $25      $50
$75      $100     $200     $300     $400     $500
$750     $1,000   $5,000   $10,000  $25,000  $50,000
$75,000  $100,000 $200,000 $300,000 $400,000 $500,000
$750,000 $1,000,000
```

### Round Structure
Each round you open a set number of cases, eliminating those amounts from play:

| Round | Cases to Open |
|-------|--------------|
| 1     | 6            |
| 2     | 5            |
| 3     | 4            |
| 4     | 3            |
| 5     | 2            |
| 6–9   | 1 each       |

### The Banker's Offer
After each round, the Banker calls with an offer. The offer is calculated as:

```
offer = round(average_of_remaining_amounts × scaling_factor)
```

Scaling factors by round: 0.10, 0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00, 1.10

The Round 9 factor (1.10) means the Banker can offer **more** than the average of remaining amounts.

- Type **DEAL** to accept the offer and end the game.
- Type **NO DEAL** to keep playing.

### Swap-or-Keep Finale
If you reject all 9 offers, two cases remain: yours and one other. You may:
- **KEEP** — open your original case and win whatever is inside.
- **SWAP** — trade your case for the other one and win that amount instead.

### Proveout Mode
If you accept one of the Banker's first 8 offers, the game enters **proveout mode** — showing what would have happened if you had kept playing: which cases would have been opened each round, what the Banker's hypothetical offers would have been, and whether your deal was a **GOOD DEAL** or a **BAD DEAL** compared to your case's actual value.

---

## Project Structure

```
deal-or-no-deal-game/
  src/
    briefcase.py      # Briefcase model
    banker.py         # Banker offer calculations
    game.py           # GameBoard and GameController (state machine)
    display.py        # All console output formatting (returns strings)
    input_handler.py  # Console input with retry logic
    proveout.py       # Proveout / what-if simulation
    main.py           # Entry point
  tests/
    test_briefcase.py
    test_banker.py
    test_game.py
    test_display.py
    test_proveout.py
    test_integration.py
    conftest.py
```
