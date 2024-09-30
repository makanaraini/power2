import matplotlib.pyplot as plt
import numpy as np

# Simple root locus example
num = [1]  # Coefficients for the numerator
den = [1, 1, 1]  # Coefficients for the denominator

plt.figure()
r = np.linspace(-2, 2, 100)
p = np.linspace(-2, 2, 100)

# Plotting the real and imaginary parts of poles
plt.plot(r, np.zeros_like(r), label='Real Axis', color='grey', lw=1)
plt.scatter([0], [0], color='red', label='Pole at Origin')  # Example pole

plt.title('Root Locus Example')
plt.xlabel('Real Axis')
plt.ylabel('Imaginary Axis')
plt.axhline(0, color='black', lw=1)
plt.axvline(0, color='black', lw=1)
plt.grid(True)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.legend()
plt.show()
