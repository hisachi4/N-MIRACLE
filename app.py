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
            # Detect the type of expression
            if expr.is_Add:
                method = "Sum/Difference Rule"
                steps.append(f"<strong>Step 1:</strong> You have a sum of terms: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> According to the <em>Sum/Difference Rule</em>, you differentiate each term individually.")
                for term in expr.args:
                    derivative = diff(term, x)
                    steps.append(f"  - The derivative of {latex(term)} is {latex(derivative)}.")
            elif expr.is_Mul:
                method = "Product Rule"
                steps.append(f"<strong>Step 1:</strong> You have a product of terms: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> We will use the <em>Product Rule</em>, which states: (fg)' = f'g + fg'.")
                derivative = diff(expr, x)
                steps.append(f"  - Applying the product rule, we get: {latex(derivative)}.")
            elif expr.is_Pow:
                method = "Power Rule"
                # Extracting the base and exponent
                base = expr.base
                exponent = expr.exp
                steps.append(f"<strong>Step 1:</strong> This is a power function: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> The <em>Power Rule</em> states: if f(x) = {latex(base)}^{latex(exponent)}, then f'(x) = {latex(exponent)} \\cdot {latex(base)}^{latex(exponent - 1)}.")
                derivative = diff(expr, x)
                steps.append(f"  - The derivative of {latex(expr)} is {latex(derivative)}.")
            else:
                method = "Chain Rule (for composite functions)"
                steps.append(f"<strong>Step 1:</strong> This is a composite function: {latex(expr)}.")
                steps.append(f"<strong>Step 2:</strong> Using the <em>Chain Rule</em>, we differentiate the outer function and multiply by the derivative of the inner function.")
                derivative = diff(expr, x)
                steps.append(f"  - Applying the chain rule, we get: {latex(derivative)}.")
            
            explanation = f"<strong>Method:</strong> {method}<br><br>" + "<br>".join(steps) + f"<br><br><strong>Final Answer:</strong> {latex(derivative)}"
            return explanation
        
        elif operation == 'integrate':
            steps.append(f"<strong>Step 1:</strong> You are integrating the function {latex(expr)}.")
            result = integrate(expr, x)
            steps.append(f"<strong>Step 2:</strong> Apply the rules of integration. The result is: {latex(result)}.")
            return "<br>".join(steps)
        
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
