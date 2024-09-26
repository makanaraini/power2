import numpy as np
from sympy import sympify, symbols, re, im, Abs, arg, N, deg

def evaluate_function_direct(s_value, numerator_func, denominator_func):
    # Use the subs method instead of calling the function
    numerator = numerator_func.subs(s, s_value)
    denominator = denominator_func.subs(s, s_value)
    return numerator, denominator

def evaluate_function_vector(s_value, numerator_func, denominator_func):
    # Using vectors to evaluate F(s)
    numerator = numerator_func.subs(s, s_value)
    denominator = denominator_func.subs(s, s_value)
    
    # Calculate the complex result
    result = numerator / denominator
    return result

# Function to get complex input from the user
def get_complex_input(prompt):
    user_input = input(prompt)
    try:
        # Convert input to complex number
        return complex(user_input)
    except ValueError:
        print("Invalid input. Please enter a complex number in the form 'a + bj' or 'a + b*i'.")
        return get_complex_input(prompt)

# Get the value of s from the user
s_value = get_complex_input("Enter the value of s (e.g., '2 + 3j'): ")

# User input for numerator and denominator
numerator_input = input("Enter the numerator as a function of s (e.g., '2 * s + 4'): ")
denominator_input = input("Enter the denominator as a function of s (e.g., 's**2 + 3 * s + 6'): ")

# Define the variable
s = symbols('s')

# Create functions from user input with validation
try:
    numerator_func = sympify(numerator_input)
    denominator_func = sympify(denominator_input)
except Exception as e:
    print(f"Error in input: {e}")
    numerator_func = None  # Set to None if there's an error
    denominator_func = None  # Set to None if there's an error

# Check if functions are defined before evaluating
if numerator_func is not None and denominator_func is not None:
    result_direct = evaluate_function_direct(s_value, numerator_func, denominator_func)
    result_vector = evaluate_function_vector(s_value, numerator_func, denominator_func)

    # Convert results to rectangular form
    rect_result_direct = result_direct[0] / result_direct[1]
    rect_result_vector = result_vector

    # Convert to polar form
    polar_result_direct = (Abs(rect_result_direct), arg(rect_result_direct))
    polar_result_vector = (Abs(rect_result_vector), arg(rect_result_vector))

    # Simplify and format results
    rect_result_direct = N(rect_result_direct).evalf(4)
    polar_result_direct = (round(float(polar_result_direct[0]), 4), round(float(deg(polar_result_direct[1])), 1))
    
    rect_result_vector = N(rect_result_vector).evalf(4)
    polar_result_vector = (round(float(polar_result_vector[0]), 4), round(float(deg(polar_result_vector[1])), 1))

    print("Result using direct substitution (Rectangular):", rect_result_direct)
    print("Result using direct substitution (Polar):", polar_result_direct[0], "Magnitude, Angle:", polar_result_direct[1], "°")
    print("Result using vector calculation (Rectangular):", rect_result_vector)
    print("Result using vector calculation (Polar):", polar_result_vector[0], "Magnitude, Angle:", polar_result_vector[1], "°")
else:
    print("Numerator or denominator function is not defined.")
