import random
import requests
import json
import time
import os

used_words = set()  # Stores words that have been used

def fetch_word():
    global used_words
    word_dict = ["king", "queen", "castle", "kingdom", "mirror", "software", 
                 "python", "algorithm", "database", "developer", "package", 
                 "bugger", "error"]

    # Reset the used words if all words are used
    if len(used_words) == len(word_dict):
        used_words.clear()

    # Get a unique word
    while True:
        word = random.choice(word_dict)
        if word not in used_words:
            used_words.add(word)
            break
    
    try:
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        if response.status_code == 200:
            content = json.loads(response.content.decode("utf-8"))
            meaning = content[0]['meanings'][0]['definitions'][0]['definition']
        else:
            meaning = "No definition found."
    except:
        meaning = "No definition found."

    return word, meaning

def display_word_revels(word_guess, num_revels, display_word, word_guessed):
    random_index = random.sample(range(len(word_guess)), num_revels)
    for idx in random_index:
        display_word[idx] = word_guess[idx]  # Reveal letter
        word_guessed.add(word_guess[idx])  # Track guessed letters
    return "".join(display_word)

def initialize_game_state(word, difficulty):
    display_word = list("_" * len(word))
    word_guessed = set()
    attempts = 7
    hangman_count = -1

    # Reveal percentage based on difficulty
    reveal_percentage = {"easy": 0.4, "medium": 0.25, "hard": 0}
    num_revels = max(1, int(len(word) * reveal_percentage[difficulty]))

    # Reveal letters at the start
    revealed_word = display_word_revels(word, num_revels, display_word, word_guessed)

    hangman_stages = [
        """
        +-------+
            |   |
                |
                |
                |
                =====""", """
        +-------+
            |   |
            O   |
                |
                |
                =====""", """
        +-------+
            |   |
            O   |
            |   |
                |
                =====""", """
        +-------+
            |   |
            O   |
           /|   |
                |
                =====""", """
        +-------+
            |   |
            O   |
           /|\  |
                |
                =====""", """
        +-------+
            |   |
            O   |
           /|\ |
           /    |
                =====""", """
        +------+
            |   |
            O   |
           /|\  |
           / \  |
                ====="""
    ]    
    return display_word, word_guessed, attempts, hangman_count, hangman_stages, revealed_word

def get_difficulty():
    while True:
        difficulty = input("Choose difficulty (Easy, Medium, Hard): ").strip().lower()
        if difficulty in ["easy", "medium", "hard"]:
            return difficulty
        print("Invalid choice! Please enter 'Easy', 'Medium', or 'Hard'.")

def update_display_word(word, display_word, letter):
    for i, char in enumerate(word):
        if char == letter:
            display_word[i] = letter

def handle_hint(hint, attempts):
    if attempts > 1:
        print(f"\nHint: {hint}")
        attempts -= 1
    else:
        print("\nNot enough attempts left for a hint.")
    return attempts

def get_user_input(word, display_word, word_guessed):
    """Ensures valid user input and allows re-entering letters until fully revealed."""
    while True:
        guess = input("\nEnter a letter or type 'hint': ").lower().strip()

        if guess == "hint":
            return guess  

        if not (guess.isalpha() and len(guess) == 1):
            print("\n❌ Invalid input! Please enter a **single letter**.")
            continue

        if guess in word and display_word.count(guess) < word.count(guess):
            return guess  # Allow letter if it is not fully revealed

        if guess in word_guessed:
            print("\n⚠️ You already revealed all occurrences of this letter! Try a different one.")
            continue  

        return guess  # Return valid, new letter

def celebrate_victory():
    celebration_boy = [
        """
        
        
            O   
          _/|\_
           / \ 
        """, """
        
        
         ___O___   
            |  
           / \ 
        """, """
        
        
         \__O__/   
            |    
           / \ 
        """, """
        
        ..     ..
         \__O__/   
            |
           / \ 
        """, """
     ...       ...          
       ..     ..
        \__O__/   
           |
          / \ 
    """
    ]

    for _ in range(2):
        for boy in celebration_boy + celebration_boy[::-1]:
            print("\n🎉 Congratulations! You guessed the word! 🎉\n")
            print(boy)
            time.sleep(0.5)
            os.system('cls' if os.name == 'nt' else 'clear')

def play_game():
    while True:
        difficulty = get_difficulty()  # Ask for difficulty level
        word, hint = fetch_word()
        display_word, word_guessed, attempts, hangman_count, hangman_stages, revealed_word = initialize_game_state(word, difficulty)

        print("=" * 40, " Welcome to Word Guessing Game! ", "=" * 40)
        print("NOTE: Correct guesses do NOT reduce attempts.")
        print("Type 'hint' to receive a hint (costs 1 attempt).")
        print("\nWord:", " ".join(display_word))

        while attempts > 0 and "_" in display_word:
            guess = get_user_input(word, display_word, word_guessed)  # Pass word & display_word

            if guess == "hint":
                attempts = handle_hint(hint, attempts)
                continue

            word_guessed.add(guess)

            if guess in word:
                print("\n Good guess!")
                update_display_word(word, display_word, guess)
            else:
                print("\n Wrong guess!")
                hangman_count += 1
                print(hangman_stages[hangman_count])
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

        while True:
            play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
            if play_again == "yes":
                break  
            elif play_again == "no":
                print("\nThanks for playing! Goodbye! :) ")
                return  
            else:
                print("Invalid input! Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    play_game()
