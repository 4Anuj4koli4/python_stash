import random

words = ["python", "friday", "program", "letter", "master"]

word = random.choice(words)
guessed_letters = set()
wrong_guesses = 0
max_wrong_guesses = 6

while wrong_guesses < max_wrong_guesses:

    # Display the current state of the word
    display = ""

    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    print("\nWord:", display)
    print("Guessed letters:", " ".join(sorted(guessed_letters)))
    print("Attempts left:", max_wrong_guesses - wrong_guesses)

    # Check if the word is complete
    if all(letter in guessed_letters for letter in word):
        print("\n🎉 You won!")
        print("The word was:", word)
        break

    guess = input("Guess a letter: ").lower().strip()

    # Validate input
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter exactly one letter.")
        continue

    if guess in guessed_letters:
        print("You already guessed that letter.")
        continue

    guessed_letters.add(guess)

    if guess in word:
        print("Good guess!")
    else:
        wrong_guesses += 1
        print("Wrong guess!")

else:
    print("\n💀 You lost!")
    print("The word was:", word)