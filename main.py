from matplotlib import pyplot as plt
import numpy as np
import sympy as sp
import code
from typing import Callable

class DefiniteIntegral:
    """Class to represent a definite integral and compute Riemann sum approximations."""
    def __init__(self, func: str | Callable, variable: str, start: float | int | str, stop: float | int | str, num: int):
        self.variable = sp.symbols(variable)
        self.start_sym = sp.sympify(start)
        self.stop_sym = sp.sympify(stop)
        self.start = float(self.start_sym.evalf()) if not isinstance(start, (int, float)) else start
        self.stop = float(self.stop_sym.evalf()) if not isinstance(stop, (int, float)) else stop
        self.num = num
        self.endpoints = np.linspace(self.start, self.stop, self.num + 1)

        if isinstance(func, str):
            self.expr = sp.sympify(func)
            self.func = sp.lambdify(self.variable, self.expr, 'numpy')
        elif callable(func):
            self.func = func
            try:
                self.expr = sp.Lambda(self.variable, func(self.variable))
            except Exception:
                self.expr = sp.Lambda(self.variable, sp.Symbol(f"f({self.variable})"))

        expr_display = self.expr.args[1] if isinstance(self.expr, sp.Lambda) else self.expr

        self.expr_latex = sp.latex(expr_display)
        self.antiderivative = sp.integrate(expr_display, self.variable)
        self.integral_value = sp.integrate(expr_display, (self.variable, self.start_sym, self.stop_sym))
        # numeric (float) evaluation of the integral value when possible
        try:
            self.integral_value_float = float(sp.N(self.integral_value))
        except Exception:
            try:
                self.integral_value_float = float(self.integral_value.evalf())
            except Exception:
                self.integral_value_float = None
        self.antiderivative_latex = sp.latex(self.antiderivative)
        self.integral_value_latex = sp.latex(self.integral_value)
        start_tex = sp.latex(self.start_sym)
        stop_tex = sp.latex(self.stop_sym)
        self.full_evaluation_latex = (
            f"$\\int_{{{start_tex}}}^{{{stop_tex}}} {sp.latex(expr_display)}\\,d{self.variable} = "
            f"\\left.{self.antiderivative_latex}\\right|_{{{start_tex}}}^{{{stop_tex}}} = {self.integral_value_latex}$"
        )

        self.approximations = np.array([
            self.left_endpoint_approximation()['approximation'],
            self.right_endpoint_approximation()['approximation'],            
            self.mid_point_approximation()['approximation'],
            self.trapezoid_approximation()['approximation'],
            self.simpson_approximation()['approximation']]).astype(float)
        
        self.approximation_methods = ['Left\nEndpoint','Right\nEndpoint','Midpoint','Trapezoid\nRule',"Simpson's\nRule"]


    def left_endpoint_approximation(self) -> dict:

        x_left = self.endpoints[:-1]
        y_left = self.func(x_left)
        total = np.sum(y_left * (self.endpoints[1] - self.endpoints[0]))

        return {
            'method': 'Left Endpoint',
            'x_left': x_left,
            'y' : y_left,
            'approximation': total,}
    
    def right_endpoint_approximation(self) -> dict:

        x_right = self.endpoints[1:]
        y_right = self.func(x_right)
        total = np.sum(y_right * (self.endpoints[1] - self.endpoints[0]))

        return {
            'method': 'Right Endpoint',
            'x_right': x_right,
            'y': y_right,
            'approximation': total}
    
    def mid_point_approximation(self) -> dict:
        x_mid = (self.endpoints[:-1] + self.endpoints[1:]) / 2
        y_mid = self.func(x_mid)
        total = np.sum(y_mid * (self.endpoints[1] - self.endpoints[0]))
        
        return {
            'method': 'Midpoint',
            'x_mid': x_mid,
            'y': y_mid,
            'approximation': total,}
    
    def trapezoid_approximation(self) -> dict:
        x = self.endpoints
        y = self.func(x)
        dx = x[1] - x[0]
        total = (dx / 2) * np.sum(y[:-1] + y[1:])
        return {
            'method': 'Trapezoid',
            'x': x,
            'y': y,
            'approximation': total,}
    

    def simpson_approximation(self) -> dict:
        # Make sure n is even
        simpsons_num = self.num
        if simpsons_num % 2 != 0:
            Warning("'n' value must be even for Simpson's rule. Rounding up to next even integer.")
            simpsons_num += 1

        # Compute proper endpoints for Simpson's rule
        x = np.linspace(self.start, self.stop, simpsons_num + 1)
        y = self.func(x)

        dx = x[1] - x[0]

        total = (dx / 3) * (
            y[0]
            + 4 * np.sum(y[1:-1:2])
            + 2 * np.sum(y[2:-2:2])
            + y[-1]
        )

        return {
            'method': "Simpson's Rule",
            'x': x,
            'y': y,
            'approximation': total,
            'n_used': simpsons_num
        }

   
   
    def __str__(self)->str:
        return f"Definite Integral of {self.expr} from {self.start} to {self.stop} with {self.num} subintervals."


    def __repr__(self) -> str:
        return (f"Definite_Integral(func={self.expr}, variable={self.variable}, "
                f"start={self.start}, stop={self.stop}, num={self.num})")


def left_endpoints(ax,I:DefiniteIntegral,quality:int):
    x_left = I.left_endpoint_approximation()['x_left']
    y = I.left_endpoint_approximation()['y']
    dx = x_left[1] - x_left[0]
    rects = []
    for i in range(len(x_left)):
        rect = plt.Rectangle((x_left[i], 0), dx, y[i], edgecolor='blue', facecolor='cyan', alpha=0.5)
        rects.append(rect)
        ax.add_patch(rect)
    ax.set_title(f'Left Endpoint Approximation\n= {I.left_endpoint_approximation()["approximation"]}')
    return ax

def right_endpoints(ax,I:DefiniteIntegral,quality:int):
    x_right = I.right_endpoint_approximation()['x_right']
    y = I.right_endpoint_approximation()['y']
    dx = x_right[1] - x_right[0]
    rects = []
    for i in range(len(x_right)):
        rect = plt.Rectangle((x_right[i]-dx, 0), dx, y[i], edgecolor='red', facecolor='orange', alpha=0.5)
        rects.append(rect)
        ax.add_patch(rect)
    ax.set_title(f'Right Endpoint Approximation\n= {I.right_endpoint_approximation()["approximation"]}')
    return ax

def trapezoids(ax,I:DefiniteIntegral,quality:int):
    x = I.endpoints
    y = I.func(x)
    polygons = []
    for i in range(len(x)-1):
        polygon = plt.Polygon([[x[i],0],[x[i],y[i]],[x[i+1],y[i+1]],[x[i+1],0]], edgecolor='green', facecolor='lightgreen', alpha=0.5)
        polygons.append(polygon)
        ax.add_patch(polygon)
    ax.set_title(f'Trapezoid Approximation\n= {I.trapezoid_approximation()["approximation"]}')
    return ax

def midpoints(ax,I:DefiniteIntegral,quality:int):
    x_mid = I.mid_point_approximation()['x_mid']
    y = I.mid_point_approximation()['y']
    dx = x_mid[1] - x_mid[0]
    rects = []
    for i in range(len(x_mid)):
        rect = plt.Rectangle((x_mid[i]-dx/2, 0), dx, y[i], edgecolor='purple', facecolor='violet', alpha=0.5)
        rects.append(rect)
        ax.add_patch(rect)
    ax.set_title(f'Midpoint Approximation\n= {I.mid_point_approximation()["approximation"]}')
    return ax\
    
def simpsons(ax,I:DefiniteIntegral,quality:int):
    x = I.simpson_approximation()['x']
    y = I.simpson_approximation()['y']
    parabolas = []
    for i in range(0, len(x)-1, 2):
        xs = np.linspace(x[i], x[i+2], quality)
        coeffs = np.polyfit([x[i], (x[i]+x[i+2])/2, x[i+2]], [y[i], y[i+1], y[i+2]], 2)
        ys = np.polyval(coeffs, xs)
        ax.fill_between(xs, ys, color='yellow', alpha=0.5, edgecolor='gold')
    ax.set_title(f"Simpson's Rule Approximation\n= {I.simpson_approximation()['approximation']} n={I.simpson_approximation()['n_used']}")
    return ax


def plot_approximations(I:DefiniteIntegral, quality:int):
    approximation_methods = (left_endpoints, right_endpoints, midpoints, trapezoids, simpsons)
    fig, axs = plt.subplots(2, 3, figsize=(16,11),constrained_layout=True)
    x = np.linspace(I.start, I.stop, quality)
    y = I.func(x)
    for ax, method in zip(axs.flatten(), approximation_methods):
        ax.plot(x, y, label=f'f({I.variable})', color='black')
        method(ax, I, quality)
        ax.legend()
    

    
    signed_errors = I.approximations-I.integral_value_float
    signed_errors[np.isinf(signed_errors)] = 0.0
    signed_errors[np.isnan(signed_errors)] = 0.0
    ax6 = axs[1,2]
    ax6.bar(I.approximation_methods, signed_errors, color='purple', alpha=0.7)
    ax6.axhline(0, color='black')
    ax6.set_title('Signed Errors of Approximations')
    ax6.set_ylabel('Signed Error')
    
    fig.suptitle(I.full_evaluation_latex + ' = ' + str(I.integral_value_float), fontsize=12,bbox=dict(facecolor='white', edgecolor='black'))
    plt.show()

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
        plot_approximations(I, quality)