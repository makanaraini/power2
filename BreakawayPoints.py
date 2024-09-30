import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from sympy import sympify, Poly

def plot_root_locus(numerator, denominator, xlim=(-10, 2), ylim=(-10, 10)):
    """
    This function plots the root locus of a system, along with poles, zeros, 
    asymptotes, and centroid.

    Parameters:
    numerator (list): The numerator coefficients of the transfer function.
    denominator (list): The denominator coefficients of the transfer function.
    xlim (tuple): Limits for the x-axis of the plot (default: (-10, 2)).
    ylim (tuple): Limits for the y-axis of the plot (default: (-10, 10)).
    """
    
    # Error handling for transfer function creation
    try:
        # Create the transfer function
        sys = ctrl.TransferFunction(numerator, denominator)
    except Exception as e:
        print(f"Error creating transfer function: {e}")
        return
    
    # Error handling for empty or zero systems
    if not numerator or not denominator:
        print("Numerator or denominator cannot be empty.")
        return
    
    if all(x == 0 for x in numerator):
        print("Numerator cannot be all zeros.")
        return
    
    if all(x == 0 for x in denominator):
        print("Denominator cannot be all zeros.")
        return
    
    # Plot the root locus
    plt.figure()
    try:
        ctrl.root_locus(sys)
    except Exception as e:
        print(f"Error plotting root locus: {e}")
        return

    # Get poles and zeros without plotting
    try:
        poles = ctrl.poles(sys)
        zeros = ctrl.zeros(sys)
    except Exception as e:
        print(f"Error retrieving poles and zeros: {e}")
        return

    # Plot poles as 'x' and zeros as 'o'
    plt.scatter(poles.real, poles.imag, marker='x', color='red', s=100, label='Poles')
    plt.scatter(zeros.real, zeros.imag, marker='o', color='blue', s=100, label='Zeros')

    # Plot asymptotes and centroid
    n_poles = len(poles)
    n_zeros = len(zeros)
    n_diff = n_poles - n_zeros

    if n_diff > 0:
        # Asymptotes centroid (real part of poles minus zeros divided by the difference)
        centroid = (sum(poles.real) - sum(zeros.real)) / n_diff
        angles = [(2*i + 1) * np.pi / n_diff for i in range(n_diff)]  # Asymptote angles

        for angle in angles:
            x = np.linspace(xlim[0], xlim[1], 100)  # Generate points for the asymptote lines
            plt.plot(x, np.tan(angle) * (x - centroid), 'k--', lw=1, label="Asymptotes")

        plt.scatter([centroid], [0], color='green', marker='P', s=100, label='Centroid')

    # Highlight real axis segments
    for real_pole in poles.real:
        plt.axvline(real_pole, color='grey', linestyle='--', lw=0.7)

    # Customize the plot
    plt.title('Enhanced Root Locus of the System')
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.axhline(0, color='black', lw=1)  # Real axis line
    plt.axvline(0, color='black', lw=1)  # Imaginary axis line
    plt.grid(True)
    plt.legend(loc='best')
    plt.xlim(xlim)  # Adjust the x-axis limits based on function parameters
    plt.ylim(ylim)  # Adjust the y-axis limits based on function parameters

    # Show the plot
    plt.show()

def get_user_input():
    """
    Prompts the user to input numerator (zeros) and denominator (poles) coefficients in polynomial form.
    
    Returns:
    numerator (list): List of numerator coefficients.
    denominator (list): List of denominator coefficients.
    """
    try:
        # Get user input for the numerator
        numerator_input = input("Enter the numerator (e.g., s+2): ")
        numerator_poly = Poly(sympify(numerator_input)).all_coeffs()
        numerator = [float(coef) for coef in numerator_poly]

        # Get user input for the denominator
        denominator_input = input("Enter the denominator (e.g., s**2 - 4*s + 13): ")
        denominator_poly = Poly(sympify(denominator_input)).all_coeffs()
        denominator = [float(coef) for coef in denominator_poly]

        return numerator, denominator
    except Exception as e:
        print(f"Invalid input: {e}. Please enter valid polynomial expressions.")
        return None, None

# Main program to get user input and plot the root locus
numerator, denominator = get_user_input()

if numerator and denominator:
    plot_root_locus(numerator, denominator, xlim=(-10, 2), ylim=(-10, 10))
