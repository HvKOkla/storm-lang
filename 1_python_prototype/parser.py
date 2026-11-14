from lexer import TokenType
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def match(self, token_type):
        if self.current_token().type == token_type:
            self.pos += 1
            return True
        return False

    def consume(self, token_type, message):
        if self.match(token_type):
            return self.tokens[self.pos - 1]
        raise Exception(f"[Line {self.current_token().line}] {message}, got {self.current_token().type.name}")

    def parse(self):
        functions = []
        while self.current_token().type != TokenType.EOF:
            functions.append(self.parse_function())
        return ProgramNode(functions)

    def parse_function(self):
        effects = []
        while self.current_token().type in (TokenType.KW_PURE, TokenType.KW_TRANSACT, TokenType.KW_DECIDES):
            effects.append(self.current_token().lexeme)
            self.pos += 1

        self.consume(TokenType.KW_FN, "Expected 'fn'")
        name = self.consume(TokenType.IDENT, "Expected function name").lexeme
        
        self.consume(TokenType.LPAREN, "Expected '('")
        params = []
        while self.current_token().type != TokenType.RPAREN:
            param_name = self.consume(TokenType.IDENT, "Expected parameter name").lexeme
            self.consume(TokenType.COLON, "Expected ':' after parameter name")
            param_type = self.current_token().lexeme
            self.pos += 1
            params.append(ParamNode(param_name, param_type))
            
            if not self.match(TokenType.COMMA):
                break
        self.consume(TokenType.RPAREN, "Expected ')'")

        return_type = "void"
        if self.match(TokenType.ARROW):
            return_type = self.current_token().lexeme
            self.pos += 1

        body = self.parse_block()
        
        return FunctionNode(name, params, return_type, body, effects)

    def parse_block(self):
        self.consume(TokenType.LBRACE, "Expected '{'")
        statements = []
        while self.current_token().type != TokenType.RBRACE and self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        self.consume(TokenType.RBRACE, "Expected '}'")
        return BlockNode(statements)

    def parse_statement(self):
        if self.current_token().type in (TokenType.KW_LET, TokenType.KW_VAR):
            is_mutable = self.current_token().type == TokenType.KW_VAR
            self.pos += 1
            name = self.consume(TokenType.IDENT, "Expected variable name").lexeme
            
            var_type = None
            if self.match(TokenType.COLON):
                var_type = self.current_token().lexeme
                self.pos += 1
            
            self.consume(TokenType.ASSIGN, "Expected '='")
            value = self.parse_expression()
            
            return VariableDeclNode(name, var_type, value, is_mutable)

        if self.current_token().type == TokenType.KW_RETURN:
            self.pos += 1
            if self.current_token().type == TokenType.RBRACE:
                return ReturnNode()
            return ReturnNode(self.parse_expression())

        if self.current_token().type == TokenType.KW_IF:
            self.pos += 1
            condition = self.parse_expression()
            then_branch = self.parse_block()
            else_branch = None
            if self.match(TokenType.KW_ELSE):
                else_branch = self.parse_block()
            return IfNode(condition, then_branch, else_branch)

        if self.current_token().type == TokenType.KW_FOR:
            self.pos += 1
            var_name = self.consume(TokenType.IDENT, "Expected loop variable").lexeme
            self.consume(TokenType.KW_IN, "Expected 'in'")
            start_expr = self.parse_expression()
            self.consume(TokenType.RANGE, "Expected '..'")
            end_expr = self.parse_expression()
            body = self.parse_block()
            return ForNode(var_name, start_expr, end_expr, body)

        # Assignment (e.g., y = 10 or y += 1)
        if self.current_token().type == TokenType.IDENT:
            next_type = self.tokens[self.pos + 1].type
            if next_type in (TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN):
                name = self.current_token().lexeme
                self.pos += 1
                op = self.current_token().lexeme
                self.pos += 1
                value = self.parse_expression()
                return AssignmentNode(IdentifierNode(name), op, value)

        expr = self.parse_expression()
        if self.match(TokenType.SEMICOLON):
            pass
        return expr

    def parse_expression(self, min_precedence=0):
        left = self.parse_primary()
        
        # Precedence for operators
        precedence = {
            TokenType.EQUAL: 1, TokenType.NOT_EQUAL: 1,
            TokenType.LESS: 2, TokenType.LESS_EQUAL: 2,
            TokenType.GREATER: 2, TokenType.GREATER_EQUAL: 2,
            TokenType.PLUS: 3, TokenType.MINUS: 3,
            TokenType.STAR: 4, TokenType.SLASH: 4
        }
        
        while True:
            op_token = self.current_token()
            if op_token.type not in precedence:
                break
                
            op_precedence = precedence[op_token.type]
            if op_precedence < min_precedence:
                break
                
            self.pos += 1
            right = self.parse_expression(op_precedence + 1)
            left = BinaryOpNode(left, op_token.lexeme, right)
            
        return left

    def parse_primary(self):
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.pos += 1
            return NumberNode(int(token.lexeme))
            
        if token.type == TokenType.STRING:
            self.pos += 1
            return StringNode(token.lexeme)
            
        if token.type == TokenType.IDENT:
            self.pos += 1
            if self.match(TokenType.LPAREN):
                args = []
                while self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    if not self.match(TokenType.COMMA):
                        break
                self.consume(TokenType.RPAREN, "Expected ')'")
                return CallNode(IdentifierNode(token.lexeme), args)
            return IdentifierNode(token.lexeme)

        if token.type == TokenType.LPAREN:
            self.pos += 1
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')'")
            return expr

        raise Exception(f"[Line {token.line}] Unexpected token in expression: {token.type.name}")