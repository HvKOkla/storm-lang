class ASTNode:
    """Base class for all AST nodes."""
    pass

# --- Expressions ---
class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class CallNode(ASTNode):
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

# --- Statements ---
class VariableDeclNode(ASTNode):
    def __init__(self, name, var_type, value, is_mutable):
        self.name = name
        self.var_type = var_type
        self.value = value
        self.is_mutable = is_mutable

class AssignmentNode(ASTNode):
    def __init__(self, target, operator, value):
        self.target = target
        self.operator = operator
        self.value = value

class ReturnNode(ASTNode):
    def __init__(self, value=None):
        self.value = value

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class ForNode(ASTNode):
    def __init__(self, var_name, start_expr, end_expr, body):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

# --- Declarations ---
class ParamNode(ASTNode):
    def __init__(self, name, param_type):
        self.name = name
        self.param_type = param_type

class FunctionNode(ASTNode):
    def __init__(self, name, params, return_type, body, effects=None):
        self.name = name
        self.params = params
        self.return_type = return_type
        self.body = body
        self.effects = effects or [] # e.g., ["pure", "transacts"]

class ProgramNode(ASTNode):
    def __init__(self, functions):
        self.functions = functions