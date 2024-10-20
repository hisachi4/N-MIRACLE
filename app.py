from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to process the input
def solve_problem(input_data):
    # Example: Simple operation like evaluating the input as a mathematical expression
    try:
        result = eval(input_data)
    except Exception as e:
        result = f"Error: {str(e)}"
    return result

@app.route('/')
def index():
    return render_template('app.html')

@app.route('/solve', methods=['POST'])
def solve():
    input_data = request.form['inputData']
    result = solve_problem(input_data)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)
