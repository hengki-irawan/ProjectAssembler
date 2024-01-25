# The Higher or Lower Game
import random
from data import *
from art import *


local_data = data

# pick a random index
def random_index():
    return random.randint(0, len(local_data) - 1)  


def comparison(sample):
    return sample['name'] + ', ' + sample['description'] + ', from ' + sample['country'] 


def displayComparison(option1, option2):
    return f"Compare A: {comparison(option1)} \n{vs_logo}\nCompare B: {comparison(option2)}"


def higher_or_lower():
    print(banner_logo)
    sample_A = local_data.pop(random_index())  #using pop to avoid the same question appear twice
    sample_B = local_data.pop(random_index())
    sample_C = local_data.pop(random_index())
    should_continue = True
    total_score = 0
    while should_continue and total_score < 50:
        print(displayComparison(sample_A, sample_B)) 
        guess = input(" Who has more followers? Type 'A' or 'B': ").upper()
        if (
            (guess == 'A' and sample_A["follower_count"] > sample_B["follower_count"]) or
            (guess == 'B' and sample_B["follower_count"] > sample_A["follower_count"])
        ):
            total_score += 1
            sample_A = sample_B
            sample_B = sample_C
            sample_C = local_data.pop(random_index()) 
        else:
            should_continue = False
            print('Game over!')
    print(f"Your score is {total_score}")


def play_game():
    while True:
        score = higher_or_lower()
        play_again = input("Do you want to play again? Type 'yes' or 'no': ").lower()
        if play_again != 'yes':
            print('Thanks for playing. Goodbye!')
            break

play_game()