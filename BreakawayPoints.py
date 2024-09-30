import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Define the transfer function
# Example: G(s) = K / (s^2 + 5s + 6), where K is the gain
numerator = [1]  # Numerator (K, which will vary)
denominator = [1, 5, 6]  # Denominator (s^2 + 5s + 6)

# Create the transfer function
sys = ctrl.TransferFunction(numerator, denominator)

# Plot the root locus
plt.figure()
rlist, klist = ctrl.root_locus(sys, Plot=True)

# Add labels for poles and zeros
poles, zeros = ctrl.pzmap(sys, Plot=False)  # Get poles and zeros without plotting

# Plot poles as 'x' and zeros as 'o'
plt.scatter(poles.real, poles.imag, marker='x', color='red', s=100, label='Poles')
plt.scatter(zeros.real, zeros.imag, marker='o', color='blue', s=100, label='Zeros')

# Annotate the gain values at some key points
for i in range(0, len(klist), len(klist)//10):  # Sample points to annotate
    plt.text(rlist[i, 0].real, rlist[i, 0].imag, f'K={klist[i]:.2f}', fontsize=9)
    
# Plot asymptotes and centroid
n_poles = len(poles)
n_zeros = len(zeros)
n_diff = n_poles - n_zeros

if n_diff > 0:
    # Asymptotes centroid (real part of poles minus zeros divided by the difference)
    centroid = (sum(poles.real) - sum(zeros.real)) / n_diff
    angles = [(2*i + 1) * np.pi / n_diff for i in range(n_diff)]  # Asymptote angles

    for angle in angles:
        x = np.linspace(-10, 10, 100)  # Generate points for the asymptote lines
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
plt.xlim([-10, 2])  # Adjust the x-axis limits for better visibility

# Show the plot
plt.show()
