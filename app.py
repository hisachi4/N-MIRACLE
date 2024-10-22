from flask import Flask, render_template, request, jsonify
from sympy import symbols, diff, integrate, sympify, latex

app = Flask(__name__)

# Define the variable for calculus
x = symbols('x')

# Function to process differentiation and show step-by-step explanation
def solve_problem(input_data, operation):
    try:
        # Convert the input string into a symbolic expression
        expr = sympify(input_data)
        steps = []
        
        if operation == 'differentiate':
            if expr.is_Add:
                method = "Sum/Difference Rule"
                steps.append(f"<strong>Step 1:</strong> You have a sum of terms: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> According to the <em>Sum/Difference Rule</em>, you differentiate each term individually.")
                
                total_derivative = 0  # Initialize total derivative
                for term in expr.args:
                    derivative = diff(term, x)
                    total_derivative += derivative  # Sum derivatives
                    steps.append(f"  - The derivative of {latex(term)} is {latex(derivative)}.")
                    
                final_answer = latex(total_derivative)  # Combine derivatives for final output
            elif expr.is_Mul:
                method = "Product Rule"
                steps.append(f"<strong>Step 1:</strong> You have a product of terms: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> We will use the <em>Product Rule</em>, which states: (fg)' = f'g + fg'.")
                derivative = diff(expr, x)
                steps.append(f"  - Applying the product rule, we get: {latex(derivative)}.")
                final_answer = latex(derivative)
            elif expr.is_Pow:
                method = "Power Rule"
                base = expr.base
                exponent = expr.exp
                steps.append(f"<strong>Step 1:</strong> This is a power function: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> The <em>Power Rule</em> states: if f(x) = {latex(base)}^{latex(exponent)}, then f'(x) = {latex(exponent)} \\cdot {latex(base)}^{latex(exponent - 1)}.")
                derivative = diff(expr, x)
                steps.append(f"  - The derivative of {latex(expr)} is {latex(derivative)}.")
                final_answer = latex(derivative)
            else:
                method = "Chain Rule (for composite functions)"
                steps.append(f"<strong>Step 1:</strong> This is a composite function: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> Using the <em>Chain Rule</em>, we differentiate the outer function and multiply by the derivative of the inner function.")
                derivative = diff(expr, x)
                steps.append(f"  - Applying the chain rule, we get: {latex(derivative)}.")
                final_answer = latex(derivative)

            explanation = f"<strong>Method:</strong> {method}<br><br>" + "<br>".join(steps) + f"<br><br><strong>Final Answer:</strong> {final_answer}"
            return explanation
        
        elif operation == 'integrate':
            if expr.is_Add:
                method = "Sum Rule for Integration"
                steps.append(f"<strong>Step 1:</strong> You have a sum of terms: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> According to the <em>Sum Rule for Integration</em>, you integrate each term individually.")
                
                total_integral = 0  # Initialize total integral
                for term in expr.args:
                    integral = integrate(term, x)
                    total_integral += integral  # Sum integrals
                    steps.append(f"  - The integral of {latex(term)} is {latex(integral)}.")
                    
                final_answer = latex(total_integral)  # Combine integrals for final output
            elif expr.is_Mul:
                method = "Integration by Parts"
                steps.append(f"<strong>Step 1:</strong> You have a product of terms: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> We will use the <em>Integration by Parts</em> formula: ∫udv = uv - ∫vdu.")
                integral = integrate(expr, x)
                steps.append(f"  - The integral using parts is: {latex(integral)}.")
                final_answer = latex(integral)
            elif expr.is_Pow:
                method = "Power Rule for Integration"
                base = expr.base
                exponent = expr.exp
                steps.append(f"<strong>Step 1:</strong> This is a power function: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> The <em>Power Rule for Integration</em> states: ∫x^n dx = \\frac{{x^{{n+1}}}}{{n+1}} + C.")
                integral = integrate(expr, x)
                steps.append(f"  - The integral of {latex(expr)} is {latex(integral)}.")
                final_answer = latex(integral)
            elif expr.has('sin') or expr.has('cos'):
                method = "Trigonometric Integrals"
                steps.append(f"<strong>Step 1:</strong> This is a trigonometric function: {latex(expr)}.")
                integral = integrate(expr, x)
                steps.append(f"  - The integral of {latex(expr)} is {latex(integral)}.")
                final_answer = latex(integral)
            elif expr.has('exp') or expr.has('log'):
                method = "Exponential/Logarithmic Integrals"
                steps.append(f"<strong>Step 1:</strong> This is an exponential or logarithmic function: {latex(expr)}.")
                integral = integrate(expr, x)
                steps.append(f"  - The integral of {latex(expr)} is {latex(integral)}.")
                final_answer = latex(integral)
            else:
                method = "General Integration"
                steps.append(f"<strong>Step 1:</strong> This is a general function: {latex(expr)}.")
                integral = integrate(expr, x)
                steps.append(f"  - The integral of {latex(expr)} is {latex(integral)}.")
                final_answer = latex(integral)

            explanation = f"<strong>Method:</strong> {method}<br><br>" + "<br>".join(steps) + f"<br><br><strong>Final Answer:</strong> {final_answer}"
            return explanation
        
        else:
            return "Invalid operation"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    input_data = request.form['inputData']
    operation = request.form['operation']
    result = solve_problem(input_data, operation)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)
