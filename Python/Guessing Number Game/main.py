import random

WELCOME_MESSAGE = "Welcome to the Number Guessing Game!!\nI'm thinking of a number between 1 and 100."
numToGuess = random.randint(1, 100)


def picked_attempt(level):
    numAttempt = {
        "hard": 5,
        "easy": 10
    }
    picked_num_attempt = 0
    if level == 'easy':
        picked_num_attempt = numAttempt[level]
    else:
        picked_num_attempt = numAttempt['hard']
    return picked_num_attempt


def guessValidator():
    print(WELCOME_MESSAGE)
    difficultyLevel = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()

    total_attempt = picked_attempt(difficultyLevel)

    while total_attempt > 0:
        playerGuess = int(input("Make a guess: "))

        if playerGuess > numToGuess:
            print("Too high.")
        elif playerGuess < numToGuess:
            print("Too low.")
        else:
            print(f"You got it! The number was {numToGuess}")
            break  # Break out of the loop if the guess is correct

        total_attempt -= 1
        if total_attempt > 0:
            print("Guess again")
            print(f"You have {total_attempt} attempt(s) remaining to guess the number.")
        else:
            print("You've run out of guesses, you lose!")
            print(f"The number was {numToGuess}")

# Call the function to start the game
guessValidator()
