import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

def plot_root_locus(numerator, denominator, xlim=(-10, 2), ylim=(-10, 10)):
    """
    This function plots the root locus of a system, along with poles, zeros, 
    asymptotes, and centroid.

    Parameters:
    numerator (list): The numerator coefficients of the transfer function.
    denominator (list): The denominator coefficients of the transfer function.
    xlim (tuple): Limits for the x-axis of the plot.
    ylim (tuple): Limits for the y-axis of the plot.
    """
    
    # Create the transfer function
    sys = ctrl.TransferFunction(numerator, denominator)

    # Plot the root locus directly
    plt.figure()
    ctrl.root_locus(sys)

    # Get poles and zeros without plotting
    poles = ctrl.poles(sys)  # Use ctrl.poles() to get poles
    zeros = ctrl.zeros(sys)  # Use ctrl.zeros() to get zeros

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


# Example usage:
numerator = [1]  # Numerator (K, which will vary)
denominator = [1, 5, 6]  # Denominator (s^2 + 5s + 6)
plot_root_locus(numerator, denominator, xlim=(-10, 2), ylim=(-10, 10))
