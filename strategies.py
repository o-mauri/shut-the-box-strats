import random

def randomChoiceStrategy(valid, gameState):
    return random.choice(valid)

def highestNumberStrategy(valid, gameState):
    highest = 0
    combo = []
    for combo in valid:
        if max(combo) > highest:
            highest = max(combo)
            combo = combo
    return combo

def lowestNumberStrategy(valid, gameState):
    lowest = 999
    combo = []
    for combo in valid:
        if min(combo) < lowest:
            lowest = min(combo)
            combo = combo
    return combo

def lowestPairingStrategy(valid, gameState):
    lowest = 999
    combo = []
    for combo in valid:
        if max(combo) < lowest:
            lowest = max(combo)
            combo = combo
    return combo


def over7Strategy(valid, gameState):
    roll = sum(valid[0])
    if roll >= 7:
        if [roll] in valid:
            return [roll]
        
    return random.choice(valid)

def dontPlay1or2Strategy(valid, gameState):
    preferred = []
    for combo in valid:
        if 1 not in combo and 2 not in combo:
            preferred.append(combo)
    if len(preferred) > 0:
        return random.choice(preferred)
    else:
        return random.choice(valid)

def over7DontPlay1Combo(valid, gameState):
    roll = sum(valid[0])
    if roll >= 7:
        if [roll] in valid:
            return [roll]
    return dontPlay1or2Strategy(valid, gameState)
