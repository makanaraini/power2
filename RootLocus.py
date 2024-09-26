import numpy as np

def evaluate_function_direct(s, numerator_func, denominator_func):
    # Direct substitution into F(s)
    numerator = numerator_func(s)
    denominator = denominator_func(s)
    return numerator / denominator

def evaluate_function_vector(s, numerator_func, denominator_func):
    # Using vectors to evaluate F(s)
    s_vector = np.array([s.real, s.imag])
    numerator = numerator_func(s_vector)
    denominator = denominator_func(s_vector)
    
    # Calculate the complex result
    result = numerator / denominator
    return result[0] + 1j * result[1]

# User input for numerator and denominator
numerator_input = input("Enter the numerator as a function of s (e.g., '2 * s + 4'): ")
denominator_input = input("Enter the denominator as a function of s (e.g., 's**2 + 3 * s + 6'): ")

# Define the point s
s = 7 + 9j

# Create functions from user input
numerator_func = eval(f"lambda s: {numerator_input}")
denominator_func = eval(f"lambda s: {denominator_input}")

# Evaluate using both methods
result_direct = evaluate_function_direct(s, numerator_func, denominator_func)
result_vector = evaluate_function_vector(s, numerator_func, denominator_func)

print("Result using direct substitution:", result_direct)
print("Result using vector calculation:", result_vector)
