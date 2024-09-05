import random
import os  # Necesario para limpiar la pantalla
from words import word_list


def get_word():
    word = random.choice(word_list)
    return word.upper()


def limpiar_pantalla():
    # Limpia la terminal según el sistema operativo
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para macOS y Linux
        os.system('clear')

def play(word):
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    print("Juguemos al Ahorcado!")
    print(display_hangman(tries))
    print(word_completion)
    while not guessed and tries > 0:
        guess = input("Ingresa una letra: ").upper()
        limpiar_pantalla()  # Limpiar pantalla después de cada entrada
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("Ya ha ingresado esa letra previamente", guess)
            elif guess not in word:
                print(guess, "No esta en la palabra.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Bien ahí,", guess, "si esta en la palabra!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("Ganaste!", guess)
            elif guess != word:
                print(guess, "No esta en la palabra.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Ingresaste un caracter no valido.")
        print(display_hangman(tries))
        print(word_completion)

        # Mostrar las letras que ya se han ingresado
        print("Letras ingresadas: ", " - ".join(guessed_letters))
        print("\n")
    if guessed:
        print("Felicidades, adivinaste la palabra!")
    else:
        print("Te quedaste sin intentos :(  \n La palabra era " + word + ".")


def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]


def main():
    limpiar_pantalla()
    word = get_word()
    play(word)
    while input("Play Again? (S/N) ").upper() == "S":
        limpiar_pantalla()
        word = get_word()
        play(word)


if __name__ == "__main__":
    main()
