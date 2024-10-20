# backend.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rules.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    department = db.Column(db.String(50))
    income = db.Column(db.Integer)
    spend = db.Column(db.Integer)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String, nullable=False)

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

def create_rule(rule_string):
    # Tokenization and parsing logic as shown previously
    # This function creates the AST based on the rule_string
    pass  # Implement as needed

def evaluate_rule(node, data):
    # Evaluation logic as shown previously
    pass  # Implement as needed

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "user_id": user.id}), 201

@app.route('/rules', methods=['POST'])
def create_rule_endpoint():
    data = request.json
    rule = Rule(expression=data['expression'])
    db.session.add(rule)
    db.session.commit()
    return jsonify({"message": "Rule created", "rule_id": rule.id}), 201

@app.route('/evaluate/<int:user_id>/<int:rule_id>', methods=['GET'])
def evaluate(user_id, rule_id):
    user = User.query.get(user_id)
    rule = Rule.query.get(rule_id)

    if user is None or rule is None:
        return jsonify({"message": "User or rule not found"}), 404

    # Create AST from rule expression
    ast = create_rule(rule.expression)

    # Prepare user data for evaluation
    user_data = {
        "age": user.age,
        "department": user.department,
        "income": user.income,
        "spend": user.spend
    }

    # Evaluate rule
    result = evaluate_rule(ast, user_data)
    return jsonify({"eligible": result})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
