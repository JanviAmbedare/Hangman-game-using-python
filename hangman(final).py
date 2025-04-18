import random
import requests
import json
import time


def fetch_word():
#Fetch a random word and its meaning.
    word_dict = ["king","queen","castle","kingdom","mirror","software", "python","algorithm","database","developer","package","bugger", "error"]
    word = random.choice(word_dict)
    
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    if response.status_code == 200:
        content = json.loads(response.content.decode("utf-8"))
        meaning = content[0]['meanings'][0]['definitions'][0]['definition']
    else:
        meaning = "No definition found."

    return word, meaning

def initialize_game_state(word):

    display_word = list("_" * len(word))
    word_guessed = set()
    attempts = 7
    hangman_count = -1
    hangman_stages = ["""
            +-------+
                |   |
                    |
                    |
                    |
                    =====""","""
            +-------+
                |   |
                O   |
                    |
                    |
                    =====""","""
            +-------+
                |   |
                O   |
                |   |
                    |
                    =====""","""
            +-------+
                |   |
                O   |
               /|   |
                    |
                    =====""","""
            +-------+
                |   |
                O   |
               /|\  |
                    |
                    =====""" , """ 
            +-------+
                |   |
                O   |
               /|\  |
               /    |
                    =====""","""
            +------+
                |   |
                O   |
               /|\  |
               / \  |
                    ====="""
                    ]    
    return display_word, word_guessed, attempts, hangman_count, hangman_stages

def display_hangman(hangman_stages, count):
#Displays the current hangman stage.
    print(hangman_stages[count])

def update_display_word(word, display_word, letter):
#Updates the display word when a correct letter is guessed.
    for i, char in enumerate(word):
        if char == letter:
            display_word[i] = letter

def handle_hint(hint, attempts):
#Handles hint logic, reducing attempts by 1 if available.
    if attempts > 1:
        print(f"\nHint: {hint}")
        attempts -= 1
    else:
        print("\nNot enough attempts left for a hint.")
    return attempts

def get_user_input():
#Gets and validates user input.
    while True:
        guess = input("\nEnter a letter or type 'hint': ").lower().strip() 
        if guess == "hint" or (guess.isalpha() and len(guess) == 1):
            return guess
        print("\nInvalid input! Please enter a single letter.")

def celebrate_victory():
#Displays celebration animation for a win.
    celebration_boy = ["""

                        
                O   
              _/|\_
               / \ 
                     ""","""

                        
             ___O___   
                |  
               / \ 
                    ""","""

                        
            \__O__/   
               |    
              / \ 
                    ""","""
                    
            ..     ..
             \__O__/   
                |
               / \ 
                    ""","""
          ...       ...          
            ..     ..
             \__O__/   
                |
               / \ 
                    """]
    
    for i in range(2):
        for boy in celebration_boy + celebration_boy[::-1]:
            print("\n🎉 Congratulations! You guessed the word! 🎉\n")
            print(boy)
            time.sleep(0.5) 
            print("\033c") 
            
        
def play_game():

    while True: 
        word, hint = fetch_word()
        display_word, word_guessed, attempts, hangman_count, hangman_stages = initialize_game_state(word)

        print("=" * 40, " Welcome to Word Guessing Game! ", "=" * 40)
        print("NOTE: Correct guesses do NOT reduce attempts.")
        print("Type 'hint' to receive a hint (costs 1 attempt).")
        print("\nWord:", " ".join(display_word))

        while attempts > 0 and "_" in display_word:
            guess = get_user_input()

            if guess == "hint":
                attempts = handle_hint(hint, attempts)
                continue

            if guess in word_guessed:
                print("\nLetter already guessed :/ ---> Try another one :)")
                continue

            word_guessed.add(guess)

            if guess in word:
                print("\n Good guess!")
                update_display_word(word, display_word, guess)
            else:
                print("\n Wrong guess!")
                hangman_count += 1
                display_hangman(hangman_stages, hangman_count)
                attempts -= 1

            print("\nWord:", " ".join(display_word))
            print(f"Attempts remaining: {attempts}")
            print(f"Guessed letters: {', '.join(sorted(word_guessed))}")
            print("\n" + "=" * 100)

        if "_" not in display_word:
            celebrate_victory()
        else:
            print(hangman_stages[-1])
            print(f"\n Game Over! The word was: {word}.")

        # Ask if the user wants to play again
        while True:
            play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
            if play_again == "yes":
                break  # Restart the game
            elif play_again == "no":
                print("\nThanks for playing! Goodbye! :) ")
                return  # Exit the function and end the game
            else:
                print("Invalid input! Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    play_game()
