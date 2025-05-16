import random
from strategies import randomChoiceStrategy, highestNumberStrategy, lowestNumberStrategy, over7Strategy, dontPlay1or2Strategy, over7DontPlay1Combo, lowestPairingStrategy
import matplotlib.pyplot as plt
import numpy as np

def strategyChoice(valid, gameState, strategyFunction):
    return strategyFunction(valid, gameState)


# Roll two dice
def rollDice():
    die1 = random.randint(1,6)
    die2 = random.randint(1,6)
    return die1 + die2

# Get all combinations of numbers that add up to the target
def getCombinations(number):
    def find_combinations(target, start, current, result):
        if target == 0:
            result.append(current[:])
            return
        if target < 0:
            return
        
        for i in range(start, 0, -1):
            if i <= target and i not in current:  # Only use numbers that haven't been used yet
                current.append(i)
                find_combinations(target - i, i - 1, current, result)
                current.pop()
    
    result = []
    find_combinations(number, number, [], result)
    return result

# Get all valid strategies for the current roll andgame state
def getValidStrategies(combinations, gameState):
    validStrategies = []
    for combination in combinations:
        validCombo = True
        for num in combination:
            if gameState[num] == True:
                validCombo = False
                break
        if validCombo:
            validStrategies.append(combination)
    return validStrategies

# Play a single turn of the game
def gameTurn(gameState, strategy):
    total = rollDice()
    combinations = getCombinations(total)
    valid = getValidStrategies(combinations, gameState)
    if len(valid) == 0:
        return False, gameState, total
    else:
        selection = strategyChoice(valid, gameState, strategy)
        for num in selection:
            gameState[num] = True
        return True, gameState, total
    
def checkVictory(gameState):
    for i in range(1, 13):
        if gameState[i] == False:
            return False
    return True

def countScore(gameState):
    score = 0
    for i in range(1, 13):
        if gameState[i] == False:
            score += i
    return score

def playGame(strategy):
    gameState = {
        1 : False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: False,
        8: False,
        9: False,
        10: False,
        11: False,
        12: False
    }

    alive = True
    victory = False
    turn = 0
    while alive:
        turn +=1
        alive, gameState, killerRoll = gameTurn(gameState, strategy)
        if alive:
            victory = checkVictory(gameState)
            if victory:
                return True, 0, None

    return False, countScore(gameState), killerRoll




def playManyGames(numGames, strategy, withPrint = False):
    print("Starting simulation with ", numGames, " games and ", strategy.__name__, " strategy")
    wins = 0
    scores = []
    killerRolls = []

    for i in range(numGames):
        if i % round(numGames/100) == 0:
            print(round(i/numGames*100), "% finished")

        victory, score, killerRoll = playGame(strategy)
        scores.append(score)
        if victory:
            wins += 1
        else:
            killerRolls.append(killerRoll)
        if withPrint:
            print("--------------------------------")
            print("Game ", i+1, " finished")
            print("Wins: ", wins)
            print("Average score: ", sum(scores) / len(scores))
            print("Win rate: ", wins / numGames)
            print("--------------------------------")

    print("--------------------------------")
    print("Games: ", numGames)
    print("Wins: ", wins)
    print("Average score: ", sum(scores) / len(scores))
    print("Win rate: ", wins * 100 / numGames, "%")
    print("--------------------------------")
    return wins, scores, killerRolls


def generate_percentage_coords(arr):
    arr = np.array(arr)
    total = len(arr)
    
    # Get all values between min and max inclusive
    x = np.arange(np.min(arr), np.max(arr) + 1)
    
    # Calculate the percentage each value occurs
    y = np.array([np.count_nonzero(arr == val) / total * 100 for val in x])
    
    return x.tolist(), y.tolist()

def normalize_killer_rolls(killerRolls):
    # Get the raw percentages
    x, y = generate_percentage_coords(killerRolls)
    
    # Calculate theoretical probabilities for each dice roll
    # For two dice, the probability of rolling n is (6 - |7-n|) / 36
    theoretical_probs = []
    for roll in x:
        prob = (6 - abs(7 - roll)) / 36
        theoretical_probs.append(prob * 100)  # Convert to percentage
    
    # Normalize by dividing observed percentages by theoretical probabilities
    normalized_y = [observed / theoretical for observed, theoretical in zip(y, theoretical_probs)]
    
    return x, normalized_y

def runTest():
    numGames = 100000
    
    # Define strategies to test
    strategies = [
        (over7Strategy, "Over 7"),
        (dontPlay1or2Strategy, "Don't play 1 or 2"),
        (over7DontPlay1Combo, "Over 7 and don't play 1 or 2")
    ]
    
    # Initialize results storage
    results = []
    
    # Run simulations for each strategy
    for strategy, title in strategies:
        wins, scores, kr = playManyGames(numGames, strategy)
        x, y = generate_percentage_coords(scores)
        krx, kry = normalize_killer_rolls(kr)
        avg = sum(scores) / len(scores)
        results.append({
            'title': title,
            'wins': wins,
            'scores': scores,
            'x': x,
            'y': y,
            'krx': krx,
            'kry': kry,
            'avg': avg
        })
    
    # Create subplots
    fig, axs = plt.subplots(len(strategies), 2)
    
    # Plot results for each strategy
    for i, result in enumerate(results):
        # Score distribution plot
        axs[i, 0].bar(result['x'], result['y'])
        axs[i, 0].axvline(x=result['avg'], color='green', linestyle='--', label=f'Avg: {result["avg"]:.1f}')
        axs[i, 0].set_title(result['title'])
        axs[i, 0].legend()
        
        # Killer rolls plot
        axs[i, 1].bar(result['krx'], result['kry'], color='red')
        axs[i, 1].set_title(f"{result['title']} Killer Rolls")
        axs[i, 1].legend()
    
    plt.tight_layout()
    plt.show()

runTest()


