from definite_integral import DefiniteIntegral
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import patches
import sympy as sp
import visualization
import code

def get_user_input():
    print("Welcome to the Definite Integral Approximation Visualizer!")
    while True:
        try:
            user_input = input('Enter a function (or press Enter for default f(x)=x^2): ').replace("^", "**")
            if user_input.strip() == "":
                func = "x**2"
                var = 'x'
                start = 0
                stop = 1
                n = 3
                quality = 1000
                print(f"Using default values: f(x)={func}, start={start}, stop={stop}, n={n}, quality={quality}")
            else:
                func = user_input
                var = input('Enter the variable used in the function (e.g., x): ').strip()
                start = input('Enter the start of the interval: ')
                stop = input('Enter the end of the interval: ')
                n = int(input('Enter the number of subintervals (n): '))
                quality = int(input('Enter the quality of the plot (number of points < 5000)'))

            I = DefiniteIntegral(func, var, start, stop, n)
            if input('Type "DEBUG" to enter DEBUG  MODE or Press Enter to continue...') == 'DEBUG':
                debug_shell(I, quality)
                
            return I, quality
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def debug_shell(I, quality):
    """
    Opens an interactive Python shell with useful variables preloaded.
    """
    banner = (
        "\n--- DEBUG MODE ---\n"
        "You can inspect variables here.\n"
        "Available names: I, quality, Definite_Integral, np, sp\n"
        "Example commands:\n"
        "  print(I.integral_value)\n"
        "  print(I.approximations)\n"
        "  I.left_endpoint_approximation()\n"
        "Press Ctrl+D or type exit() to continue.\n"
    )

    # namespace available inside the debug prompt
    namespace = {
        "I": I,
        "quality": quality,
        "Definite_Integral": DefiniteIntegral,
        "np": np,
        "sp": sp,
    }

    code.interact(banner=banner, local=namespace)

if __name__ == "__main__":
    while True:
        I, quality = get_user_input()
        visualization.plot_approximations(I, quality)