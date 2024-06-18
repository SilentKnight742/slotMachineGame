import random
MAX_LINES = 5
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLUMNS = 3

symbols = {
    "A" : {"count" : 1, "value" : 20},
    "B" : {"count" : 3, "value" : 15},
    "C" : {"count" : 5, "value" : 10},
    "D" : {"count" : 7, "value" : 8},
    "E" : {"count" : 9, "value" : 5}
}

multipliers = {
    "A" : 3,
    "B" : 2.5,
    "C" : 2,
    "D" : 1.5,
    "E" : 1.2
}

#5 types of lines: each row and 2 diagonals
lines = [
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)],
]

def check_winnings_best_lines(columns, lines, numLines, bet, values, multipliers):
    totalWinnings = 0
    bestLines = []
    lineWinnings = []
    for line in lines:
        symbol = columns[line[0][0]][line[0][1]]
        for position in line:
            if symbol != columns[position[0]][position[1]]:
                break
        else:
            winnings = values[symbol]*bet*multipliers[symbol]
            lineWinnings.append((winnings, line))
    lineWinnings.sort(reverse=True, key=lambda x: x[0])
    selectedWinnings = lineWinnings[:numLines]
    for winnings, line in selectedWinnings:
        totalWinnings += winnings
        bestLines.append(line)
    return totalWinnings, bestLines

def getSlotMachineSpin(rows, cols, symbols):
    allSymbols = []
    for symbol, symbolInfo in symbols.items():
        for _ in range(symbolInfo["count"]):
            allSymbols.append(symbol)
    columns = []
    for _ in range(cols):
        column = []
        currentSymbols = allSymbols[:]
        for _ in range(rows):
            value = random.choice(currentSymbols)
            currentSymbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

def printSlotMachine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()

def getNumberOfLines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                return lines
            else:
                print(f"Please enter a number between 1 and {MAX_LINES}.")
        else:
            print("Please enter a valid number.")

def getBet():
    while True:
        bet = input(f"What would you like to bet on each line? (min ${MIN_BET}, max ${MAX_BET}): ")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                return bet
            else:
                print(f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid number.")

def depositMoney():
    while True:
        deposit = input("How much money would you like to deposit? $")
        if deposit.isdigit():
            deposit = int(deposit)
            if deposit > 0:
                return deposit
            else:
                print("Deposit amount must be greater than 0.")
        else:
            print("Please enter a valid number.") 

def playSlotMachine():
    print("Welcome to Nigga Slayer Casino, deposit money to get started!")
    balance = depositMoney()
    while balance >= MIN_BET:
        print(f"Current balance: ${balance}")
        numLines = getNumberOfLines()
        bet = getBet()
        totalBet = bet*numLines
        if totalBet > balance:
            keepPlaying = input("You do not have enough money. Do you want to keep playing? (y/n): ").lower()
            if keepPlaying != 'y':
                break
            checkDeposit = input("Do you want to deposit more money? (y/n): ").lower()
            if checkDeposit != 'y':
                continue
            deposit = depositMoney()
            balance += deposit
            print(f"New balance: ${balance}")
            continue
        print(f"Betting ${bet} on {numLines} lines. Total bet is ${totalBet}.")
        slots = getSlotMachineSpin(ROWS, COLUMNS, symbols)
        printSlotMachine(slots)
        winnings, bestLines = check_winnings_best_lines(slots, lines, numLines, bet, {k: v["value"] for k, v in symbols.items()}, multipliers)
        balance += winnings - totalBet
        print(f"You won ${winnings}!")
        if winnings > 0:
            print(f"You won on lines {bestLines}")
        if balance < MIN_BET:
            keepPlaying = input("You do not have enough money to keep going. Do you want to keep playing? (y/n): ").lower()
            if keepPlaying != 'y':
                break
            deposit = depositMoney()
            balance += deposit
            print(f"New balance: ${balance}")
            continue
        keepPlaying = input("Do you want to keep playing? (y/n): ").lower()
        if keepPlaying != 'y':
            break
    
    print(f"You are leaving with ${balance}")

playSlotMachine()
