import sympy as sp
import numpy as np
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

        # Domain validation (recommended)
        # if np.any(np.isnan(y)) or np.any(np.isinf(y)):
        #     raise ValueError("Function is undefined at some Simpson sample points.")

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

if __name__ == "__main__":
    def _test_integral(di: DefiniteIntegral):
        print(di)
        methods = [
            di.left_endpoint_approximation,
            di.right_endpoint_approximation,
            di.mid_point_approximation,
            di.trapezoid_approximation,
            di.simpson_approximation,
        ]
        for m in methods:
            try:
                res = m()
            except Exception as e:
                print(f"{m.__name__}: Error: {e}")
            else:
                print(f"{res['method']}: {res['Division by Zero']}")
        print(f"Exact integral: {di.integral_value}\n")
    
    test = DefiniteIntegral("1/x", "x", 0, 1, 4)
    print(test.left_endpoint_approximation())

