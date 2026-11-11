import os
import Reflection
import Refraction

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    clear_screen()
    print("#####################################################################")
    print("  Welcome! This project is about REFLECTION and REFRACTION of Light.")
    print("#####################################################################")
    print("Below is the menu to choose between REFLECTION and REFRACTION of Light, provide your choice accordingly. Thank You!")
    while True:
        choice = input("Choose an option (A: Reflection, B: Refraction, Q: Quit): ").upper()
        if choice == 'A':
            Reflection.handle_reflection()
        elif choice == 'B':
            Refraction.get_refraction()
        elif choice == 'Q':
            print("Exiting the program!")
            break
        else:
            print("Invalid choice, please try again.")

main()