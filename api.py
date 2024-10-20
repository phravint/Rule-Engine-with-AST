from flask import Flask, request, jsonify
from ast import create_rule, evaluate_rule, combine_rules

app = Flask(__name__)

@app.route('/create_rule', methods=['POST'])
def api_create_rule():
    data = request.json
    rule_string = data.get('rule_string')
    root_node = create_rule(rule_string)
    return jsonify({"ast": str(root_node)})

@app.route('/evaluate_rule', methods=['POST'])
def api_evaluate_rule():
    data = request.json
    ast = data.get('ast')  # Send the AST representation as a string
    user_data = data.get('user_data')
    
    # You need to parse the string back to Node for evaluation
    # Here, we assume `ast` is a representation you can convert back to Node object
    # You may need to implement a method to convert string representation back to Node if required

    result = evaluate_rule(ast, user_data)
    return jsonify({"result": result})

@app.route('/combine_rules', methods=['POST'])
def api_combine_rules():
    data = request.json
    rules = data.get('rules')
    combined_ast = combine_rules(rules)
    return jsonify({"combined_ast": str(combined_ast)})

if __name__ == '__main__':
    app.run(debug=True)
