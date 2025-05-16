# shut-the-box-strats
A Python-based simulator for the classic Shut Box dice game, used for testing multiple playing strategies and statistical analysis of the results.

## Features

- Multiple playing strategies:
  - Over 7 Strategy
  - Don't Play 1 or 2 Strategy
  - Over 7 and Don't Play 1 or 2 Combo Strategy
  - Random Choice Strategy
  - Highest Number Strategy
  - Lowest Number Strategy
  - Lowest Pairing Strategy
- Statistical analysis of strategy performance
- Visualization of results using matplotlib
- Support for running multiple game simulations

## Requirements

- Python 3.x
- matplotlib
- numpy

## Installation

1. Install the required dependencies:
```bash
pip install matplotlib numpy
```

2. Run the main simulation:
```bash
python main.py
```

This will:
- Simulate 100,000 games for each strategy
- Generate visualizations showing:
  - Score distributions
  - Average scores
  - Killer roll analysis
  - Win rates

## Game Rules

1. The game starts with numbers 1-12 available
2. On each turn:
   - Roll two dice
   - Select any combination of available numbers that sum to the roll
   - Mark those numbers as "shut"
3. The game ends when:
   - All numbers are shut (victory)
   - No valid combinations are available for the current roll (loss)
4. The score is the sum of remaining unshut numbers

## Project Structure

- `main.py`: Main simulation and visualization code
- `strategies.py`: Contains various playing strategies
- `README.md`: This documentation file
