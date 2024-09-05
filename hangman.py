import random
import os  # Necesario para limpiar la pantalla
from words import word_list
from codecarbon import EmissionsTracker  # Importamos codecarbon
import pandas as pd  # Para leer el archivo emissions.csv con pandas


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
                print(guess, "No está en la palabra.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Bien ahí,", guess, "sí está en la palabra!")
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
                print("Ya intentaste esa palabra antes", guess)
            elif guess != word:
                print(guess, "No es la palabra.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Ingresaste un carácter no válido.")
        print(display_hangman(tries))
        print(word_completion)

        # Mostrar las letras que ya se han ingresado
        print("Letras ingresadas: ", " - ".join(guessed_letters))
        print("\n")
    if guessed:
        print("¡Felicidades, adivinaste la palabra!")
    else:
        print("Te quedaste sin intentos :(  \nLa palabra era " + word + ".")


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

def mostrar_emisiones():
    """Función para leer y mostrar el contenido del archivo emissions.csv usando pandas"""
    try:
        df = pd.read_csv('emissions.csv')
        # Lista de columnas a mostrar
        columnas = [
            'timestamp', 'duration', 'emissions', 'emissions_rate', 'cpu_power',
            'gpu_power', 'ram_power', 'cpu_energy', 'gpu_energy', 'ram_energy',
            'energy_consumed', 'country_name', 'country_iso_code', 'region',
            'os', 'python_version', 'codecarbon_version', 'tracking_mode'
        ]
        # Verificar si las columnas existen en el DataFrame
        columnas_existentes = [col for col in columnas if col in df.columns]
        if columnas_existentes:
            print("\n--- Emisiones de Carbono Registradas ---\n")
            print(df[columnas_existentes])
        else:
            print("Las columnas solicitadas no están presentes en el archivo.")
    except FileNotFoundError:
        print("No se encontró el archivo 'emissions.csv'.")

def main():
    # Iniciar el rastreador de emisiones con log_level a 'CRITICAL'
    tracker = EmissionsTracker(log_level="CRITICAL")
    tracker.start()
    
    try:
        while True:
            limpiar_pantalla()
            word = get_word()
            play(word)
            if input("¿Jugar otra vez? (S/N) ").upper() != "S":
                break
    finally:
        # Detener el rastreador de emisiones
        tracker.stop()

        # Mostrar el contenido de emissions.csv
        mostrar_emisiones()

if __name__ == "__main__":
    main()
