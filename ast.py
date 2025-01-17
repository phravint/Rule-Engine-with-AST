import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Reference to left child
        self.right = right  # Reference to right child
        self.value = value  # Value for operand nodes

def create_rule(rule_string):
    # Remove spaces for easier parsing
    rule_string = rule_string.replace(" ", "")

    # Define regex patterns for operands and operators
    operand_pattern = r"(\w+)([<>]=?|=)(\d+|'[\w\s]+')"
    operator_pattern = r"AND|OR"

    # Tokenize the input string
    tokens = []
    index = 0

    while index < len(rule_string):
        if re.match(operand_pattern, rule_string[index:]):
            match = re.match(operand_pattern, rule_string[index:]).group(0)
            tokens.append(('operand', match))
            index += len(match)
        elif rule_string[index:index + 3] in ["AND", "OR"]:
            tokens.append(('operator', rule_string[index:index + 3]))
            index += 3
        elif rule_string[index] in ['(', ')']:
            tokens.append(('parenthesis', rule_string[index]))
            index += 1
        else:
            index += 1  # Skip unrecognized characters

    # Now we need to build the AST from tokens
    def parse(tokens):
        def parse_expression(index):
            current_node = None
            last_operator = None

            while index < len(tokens):
                token_type, token_value = tokens[index]

                if token_type == 'parenthesis':
                    if token_value == '(':
                        # Start a new subexpression
                        index += 1
                        sub_node, index = parse_expression(index)
                        if current_node is None:
                            current_node = sub_node
                        else:
                            if last_operator:
                                new_node = Node("operator", left=current_node, right=sub_node, value=last_operator)
                                current_node = new_node
                                last_operator = None
                    else:
                        index += 1  # Close parenthesis
                elif token_type == 'operand':
                    node = Node("operand", value=token_value)
                    if current_node is None:
                        current_node = node
                    else:
                        if last_operator:
                            new_node = Node("operator", left=current_node, right=node, value=last_operator)
                            current_node = new_node
                            last_operator = None
                elif token_type == 'operator':
                    last_operator = token_value
                    index += 1  # Move past the operator
                    continue

                index += 1

            return current_node, index

        root, _ = parse_expression(0)
        return root

    root = parse(tokens)
    return root

def evaluate_rule(node, data):
    if node.type == "operand":
        # Parse operand condition (e.g., age > 30)
        left, operator, right = re.match(r"(\w+)([<>]=?|=)(\d+|'[\w\s]+')", node.value).groups()
        left_value = data.get(left)  # Use get to avoid KeyError if the key is missing
        if right.startswith("'"):
            right_value = right.strip("'")  # Remove quotes for string comparison
        else:
            right_value = int(right)  # Convert right_value to int for numerical comparison

        if left_value is None:
            return False  # If left_value is not present in data, return False

        # Ensure left_value is treated as int if it should be
        if isinstance(left_value, str) and left_value.isdigit():
            left_value = int(left_value)

        if operator == '=':
            return left_value == right_value
        elif operator == '>':
            return left_value > right_value
        elif operator == '<':
            return left_value < right_value
        elif operator == '>=':
            return left_value >= right_value
        elif operator == '<=':
            return left_value <= right_value
    elif node.type == "operator":
        if node.value == "AND":
            return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
        elif node.value == "OR":
            return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)
    return False

def combine_rules(rules):
    combined_nodes = [create_rule(rule) for rule in rules]

    if not combined_nodes:
        return None

    # Create a combined AST using OR as the operator
    root = Node("operator", left=combined_nodes[0], right=combined_nodes[1], value="OR")
    return root
