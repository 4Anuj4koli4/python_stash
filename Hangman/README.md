# Hangman

A lightweight command-line Hangman game built with Python's standard library.
Each round randomly selects a word and gives you six incorrect guesses to solve
it.

## Features

- Random word selection for each round
- Progress display with hidden and revealed letters
- Sorted list of letters already guessed
- Six-attempt limit
- Input validation for invalid and repeated guesses
- No external packages or setup required

## Requirements

- Python 3.8 or newer
- A terminal or command prompt

The game uses only the built-in `random` module, so there are no dependencies
to install.

## Run the game

From the project directory, run:

```bash
python hangman.py
```

On some systems, use:

```bash
python3 hangman.py
```

## How to play

1. The game chooses a word and displays one underscore for each letter.
2. Enter one letter when prompted.
3. Correct guesses reveal every matching occurrence in the word.
4. Incorrect guesses reduce the number of attempts remaining.
5. Guess the complete word before all six incorrect attempts are used.

Guesses are converted to lowercase and surrounding spaces are ignored. Entries
must contain exactly one alphabetic character. Invalid or repeated guesses do
not use an attempt.

## Example

```text
Word: _ _ _ _ _ _
Guessed letters: a e
Attempts left: 4
Guess a letter: p
Good guess!
```

The exact word and progress will vary because the word is selected randomly.

## Word list

The current built-in words are:

```text
python, friday, program, letter, master
```

To customize the game, edit the `words` list near the top of `hangman.py`.

## License

This project is provided for learning and personal use.
