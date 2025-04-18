import requests
import json
import random
hangman = ["""
+----+
     |
     |
     |
     ====""","""
+----+
  |  |
     |
     |
     ====""","""
+----+
   | |
   o |
     |
     ====""","""
+----+
   | |
   o |
  /| |
     ====""","""
+----+
   | |
   o |
  /|\|
     ====""" , """ 
+----+
   | |
   o |
  /|\|
  /  ====""","""
+----+
   | |
   o |
  /|\|
  / \ ===="""
          ]           

words = ['king', 'queen','kingdom']
mapping = {}
for word in words:
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    content = json.loads(response.content.decode("utf-8")) 
    mapping[word] = content[0]['meanings'][0]['definitions'][0]['definition']
    

content = json.loads(response.content.decode("utf-8"))
guessed_letters = []  
attempts = 7
hangman_count = -1
print("HINT:",content[0]['meanings'][0]['definitions'][0]['definition'])

while attempts > 0:
    
    display = ""
    for letter in word:
        if letter in guessed_letters:

            display += letter + " "
        else:
            display += "_ "

    print("\nWord:", display.strip())
    print(f"Attempts left: {attempts}")

  
    guess = input("Guess a letter: ").lower()
    if guess in guessed_letters:
        print("You already guessed that letter!")
        continue

    guessed_letters.append(guess)

    # Check if guess is correct
    if guess in word:
        print("Correct guess!")
    else:
        print(" Wrong guess!")
        hangman_count=hangman_count+1
        
        print(hangman[hangman_count])
        attempts -= 1  

    win = True
    for letter in word:
        if letter not in guessed_letters:
            win = False
            break

    if win:
        print("\nCongratulations! You guessed the word:", word)
        break

if attempts == 0:
    print("\nGame Over! The word was:",word)