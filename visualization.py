from matplotlib import pyplot as plt
import numpy as np
import sympy as sp
from definite_integral import DefiniteIntegral


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
if __name__ == "__main__": 
    test_integral = DefiniteIntegral("5*sin(x/3) + x", "x", 1, 10, 10)
    
    plot_approximations(I=test_integral, quality=900)