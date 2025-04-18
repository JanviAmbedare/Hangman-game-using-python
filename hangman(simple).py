import random
import requests
import json
import time


word_dict = ["software", "python","algorithm","database","developer","package","bugger", "error"]
word_guess = random.choice(word_dict)
word = word_guess
response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
content = json.loads(response.content.decode("utf-8"))
meaning = content[0]['meanings'][0]['definitions'][0]['definition']

display_word = list("_" * len(word_guess))
hint = meaning
word_guessed = set()
attempts = 7
#hangman display
hangman = ["""
+------+
   |   |
       |
       |
       |
       =====""","""
+------+
   |   |
   O   |
       |
       |
       =====""","""
+------+
   |   |
   O   |
   |   |
       |
       =====""","""
+------+
   |   |
   O   |
  /|   |
       |
       =====""","""
+------+
   |   |
   O   |
  /|\  |
       |
       =====""" , """ 
+------+
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
hangman_count = -1

# Reveal 2 letters at random
num_reveals = 0
revealed_indices = random.sample(range(len(word_guess)), num_reveals)
for idx in revealed_indices:
    display_word[idx] = word_guess[idx]
    word_guessed.add(word_guess[idx])

print("="*40," Welcome to Word Guessing Game!", "="*40)
print("NOTE : On correct guess there will be no deduction of attempts.")
print("Type 'hint' to receive a hint (costs 1 attempt).")
print("\nWord: " + " ".join(display_word))

while attempts > 0 and "_" in display_word:
    lett = input("\nEnter a letter or type 'hint': ").lower().strip()

    if lett == "hint":
        if attempts > 1:
            print(f"\nHint: {hint}")
            attempts -= 1
            print(f"Attempts remaining: {attempts}")
            print("\n" + "="*100)
            
        else:
            print("\nNot enough attempts left for a hint.")
        continue

    if not lett.isalpha() or len(lett) != 1:
        print("\nInvalid input! Please enter a single letter.")
        continue

    # Check if letter has already been guessed
    if lett in word_guessed:
        # Allow repeat input only if the letter is still hidden
        if lett in word_guess and "_" in [display_word[i] for i in range(len(word_guess)) if word_guess[i] == lett]:
            print("\nYou already guessed this letter, but it's still needed.")
        else:
            print("\nLetter already revealed. Try another.")
            continue
    else:
        word_guessed.add(lett)

    if lett in word_guess:
        print("\n✅ Good guess!")
        print()
        for i, letter in enumerate(word_guess):
            if letter == lett:
                display_word[i] = lett
    else:
        print("\n❌ Wrong guess!")
        hangman_count=hangman_count+1
        
        print(hangman[hangman_count])
        attempts -= 1

    print("\nWord: " + " ".join(display_word))
    print(f"Attempts remaining: {attempts}")
    print(f"Guessed letters: {', '.join(sorted(word_guessed))}")
    print("\n" + "="*100)

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


if "_" not in display_word:
    try:
        while True:
            for i in celebration_boy:
                print("\n🎉 Congratulations! You guessed the word! 🎉\n\n")
                print(i)
                time.sleep(0.5)
                print("\033c")
            for i in celebration_boy[::-1]:
                print("\n🎉 Congratulations! You guessed the word! 🎉\n\n")
                print(i)
                time.sleep(0.5)
                print("\033c")
    except KeyboardInterrupt:
        pass
    
    
else:
    print(hangman[6])
    print(f"\n💀 Game Over! The word was: {word_guess}.")