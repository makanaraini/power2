import numpy as np
import matplotlib.pyplot as plt
import control as ctrl
from sympy import sympify, Poly

def calculate_breakaway_points(numerator, denominator):
    """
    Calculate breakaway and break-in points on the root locus.
    
    Parameters:
    numerator (list): The numerator coefficients of the transfer function.
    denominator (list): The denominator coefficients of the transfer function.
    
    Returns:
    breakaway_points (list): List of breakaway/break-in points.
    """
    s = ctrl.TransferFunction(numerator, denominator).num[0]
    P = np.poly1d(denominator)
    dP = np.polyder(P)

    # Finding the breakaway points
    breakaway_points = []
    for r in np.linspace(-10, 10, 1000):
        if dP(r) != 0:  # Avoid division by zero
            breakaway_points.append(r - P(r) / dP(r))
    
    return np.unique(np.array(breakaway_points))

def calculate_jw_axis_crossovers(numerator, denominator):
    """
    Calculate the jω-axis crossover points.
    
    Parameters:
    numerator (list): The numerator coefficients of the transfer function.
    denominator (list): The denominator coefficients of the transfer function.
    
    Returns:
    crossover_points (list): List of crossover points on the jω-axis.
    """
    sys = ctrl.TransferFunction(numerator, denominator)
    # Generate a range of imaginary frequencies
    imaginary_freqs = np.linspace(-10, 10, 1000) * 1j
    responses = ctrl.forced_response(sys, T=imaginary_freqs)

    crossover_points = []
    for i, val in enumerate(responses[1]):
        if np.isclose(val.imag, 0, atol=1e-5):
            crossover_points.append(responses[1][i].real)

    return crossover_points

def plot_root_locus(numerator: list, denominator: list, angle_at_point: float = None, xlim: tuple = (-10, 2), ylim: tuple = (-10, 10)) -> None:
    """
    Plots the root locus of a system.
    
    Parameters:
    - numerator: List of numerator coefficients.
    - denominator: List of denominator coefficients.
    - angle_at_point: Optional angle for the plot.
    - xlim: Limits for the x-axis.
    - ylim: Limits for the y-axis.
    """
    # Create the transfer function
    sys = ctrl.TransferFunction(numerator, denominator)
    
    # Get poles and zeros
    poles = ctrl.poles(sys)
    zeros = ctrl.zeros(sys)

    # Generate the root locus data
    rlist, klist = ctrl.root_locus(sys, plot=False)  # Get data without plotting
    
    plt.figure()
    plt.title('Root Locus with Characteristics')
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.axhline(0, color='black', lw=1)
    plt.axvline(0, color='black', lw=1)
    plt.grid(True)

    # Plot the root locus
    for r in rlist:
        plt.plot(r.real, r.imag, 'b')  # Plot the root locus curves

    # Plot poles and zeros
    plt.scatter(poles.real, poles.imag, marker='x', color='red', s=100, label='Poles')
    plt.scatter(zeros.real, zeros.imag, marker='o', color='blue', s=100, label='Zeros')

    # Calculate and plot breakaway points and jω-axis crossover points (same as before)
    breakaway_points = calculate_breakaway_points(numerator, denominator)
    plt.scatter(breakaway_points, np.zeros_like(breakaway_points), marker='*', color='orange', s=100, label='Breakaway Points')
    crossover_points = calculate_jw_axis_crossovers(numerator, denominator)
    plt.scatter(crossover_points, np.zeros_like(crossover_points), marker='D', color='purple', s=100, label='jω Crossover Points')

    # Plot asymptotes and centroid
    n_poles = len(poles)
    n_zeros = len(zeros)
    n_diff = n_poles - n_zeros

    if n_diff > 0:
        # Asymptotes centroid
        centroid = (sum(poles.real) - sum(zeros.real)) / n_diff
        angles = [(2*i + 1) * np.pi / n_diff for i in range(n_diff)]  # Asymptote angles

        for angle in angles:
            x = np.linspace(xlim[0], xlim[1], 100)  # Generate points for the asymptote lines
            plt.plot(x, np.tan(angle) * (x - centroid), 'k--', lw=1, label="Asymptotes")

        plt.scatter([centroid], [0], color='green', marker='P', s=100, label='Centroid')

    # Display characteristics and finalize the plot
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.legend(loc='best')
    plt.show()

def get_user_input():
    """
    Prompts the user to input numerator (zeros) and denominator (poles) coefficients in polynomial form.
    
    Returns:
    tuple: A tuple containing the numerator (list) and denominator (list) coefficients.
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

        print(f"Numerator: {numerator}, Denominator: {denominator}")  # Debug print
        return numerator, denominator
    except Exception as e:
        print(f"Invalid input: {e}. Please enter valid polynomial expressions.")
        return [], []  # Return empty lists to prevent unpacking errors

# Main program to get user input and plot the root locus
numerator, denominator = get_user_input()

if numerator and denominator:  # Check if lists are not empty
    angle_input = input("Enter a point to calculate angle as a complex number (e.g., 2+1j) or press Enter to skip: ")
    angle_at_point = complex(angle_input) if angle_input else None  # Use None if no input is provided
    plot_root_locus(numerator, denominator, angle_at_point, xlim=(-10, 2), ylim=(-10, 10))
else:
    print("Failed to get valid numerator and denominator.")
