"""
---Blackjack---
The deck is unlimited in size
There is no jokers.
The Jack/Queen/King all count as 10
The Ace can count as 11 or 1
The cards in the list of cards hae equal probability of being drawn.
Cards are not removed from the deck as they are drawn.
"""

import random
from art import logo

def randomCard():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # 11 is Ace
    return random.choice(cards)

def finalScore(cardsOnHand):
    # Calculate total score of final hands
    total_score = sum(cardsOnHand)

    if total_score == 21 and len(cardsOnHand) == 2:
        return 21

    if 11 in cardsOnHand and total_score > 21:
        cardsOnHand.remove(11)
        cardsOnHand.append(1)
        return sum(cardsOnHand)
    else:
        return total_score

def gettingWinner(player_score, dealer_score):
    if player_score == dealer_score:
        return "It's a draw!"
    elif dealer_score == 21:
        return "You lose!, dealer has Blackjack"
    elif player_score == 21:
        return "You win!"
    elif player_score > 21:
        return "You went over. You lose!"
    elif dealer_score > 21:
        return "You win!, dealer went over"
    elif player_score > dealer_score:
        return "You win!"
    else:
        return "You lose!"
    

def replay():
    end_question = input("Type 'y' to restart the game, type 'n' to end it: ").lower()
    if end_question ==  'y':
        blackjack()
    else:
        print("Thank you for playing!") 


def blackjack():
    print(logo)

    player = [randomCard(), randomCard()]
    dealer = [randomCard(), randomCard()]
    player_score = finalScore(player)
    dealer_score = finalScore(dealer)

    print(f"Your cards: {player}, current score: {player_score}.")
    print(f"Computer's first card: {dealer[0]}")

    should_continue = True
    while should_continue:
        if player_score == 21 or dealer_score == 21 or player_score > 21:
            should_continue = False
            result = gettingWinner(player_score, dealer_score)
            print(result)
        else:
            another_card = input("\n    Type 'y' to get another card, type 'n' to pass: ").lower()
            if another_card == 'y':
                player.append(randomCard())
                player_score = finalScore(player)
                print(f"Your cards: {player}, current score: {player_score}.")
            else:
                player_score = finalScore(player)
                should_continue = False

    while finalScore(dealer) != 21 and finalScore(dealer) < 17:
        dealer.append(randomCard())
        dealer_score = finalScore(dealer)

    print(gettingWinner(player_score, dealer_score))
    print(f"Your final hand: {player}, final score: {player_score}.\nComputer's final hand: {dealer}, final score: {dealer_score}.")
    
    replay()


blackjack()
