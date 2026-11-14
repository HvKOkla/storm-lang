from ast_nodes import *

class CodeGen:
    def __init__(self):
        self.indent_level = 0

    def get_indent(self):
        return "    " * self.indent_level

    def generate(self, program):
        output = []
        for func in program.functions:
            output.append(self.gen_function(func))
            output.append("") 
        return "\n".join(output)

    def gen_function(self, node):
        effects_str = ""
        if node.effects:
            verse_effects = []
            for e in node.effects:
                if e == "pure": verse_effects.append("<computes>")
                elif e == "transact": verse_effects.append("<transacts>")
                elif e == "decides": verse_effects.append("<decides>")
            effects_str = "".join(verse_effects)
        else:
            effects_str = "<computes>"

        params_str = ", ".join([f"{p.name}:{p.param_type}" for p in node.params])
        signature = f"{node.name}<public>({params_str}){effects_str}:{node.return_type} =\n"
        
        self.indent_level += 1
        body_str = self.gen_block(node.body)
        self.indent_level -= 1
        
        return signature + body_str

    def gen_block(self, node):
        output = []
        for stmt in node.statements:
            output.append(self.gen_statement(stmt))
        return "\n".join(output)

    def gen_statement(self, node):
        ind = self.get_indent()
        
        if isinstance(node, VariableDeclNode):
            if node.is_mutable:
                var_type = f":{node.var_type}" if node.var_type else ""
                return f"{ind}var {node.name}{var_type} = {self.gen_expr(node.value)}"
            else:
                return f"{ind}{node.name} := {self.gen_expr(node.value)}"

        if isinstance(node, AssignmentNode):
            return f"{ind}set {node.target.name} {node.operator} {self.gen_expr(node.value)}"

        if isinstance(node, ReturnNode):
            val = self.gen_expr(node.value) if node.value else ""
            # ATTENTION : On ne met PAS de .strip() ici !
            if val:
                return f"{ind}return {val}"
            else:
                return f"{ind}return"

        if isinstance(node, IfNode):
            cond = self.gen_expr(node.condition)
            out = f"{ind}if ({cond}):\n"
            
            self.indent_level += 1
            out += self.gen_block(node.then_branch)
            self.indent_level -= 1
            
            if node.else_branch:
                out += f"\n{ind}else:\n"
                self.indent_level += 1
                out += self.gen_block(node.else_branch)
                self.indent_level -= 1
            return out

        if isinstance(node, ForNode):
            start = self.gen_expr(node.start_expr)
            end = self.gen_expr(node.end_expr)
            out = f"{ind}for({node.var_name}:={start}..{end}) do:\n"
            
            self.indent_level += 1
            out += self.gen_block(node.body)
            self.indent_level -= 1
            return out

        return f"{ind}// TODO: Unhandled statement"

    def gen_expr(self, node):
        if isinstance(node, NumberNode):
            return str(node.value)
        if isinstance(node, StringNode):
            return f'"{node.value}"'
        if isinstance(node, IdentifierNode):
            return node.name
        if isinstance(node, BinaryOpNode):
            left = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            op = node.operator
            if op == "==": op = "="
            elif op == "!=": op = "<>"
            return f"{left} {op} {right}"
        if isinstance(node, CallNode):
            callee = self.gen_expr(node.callee)
            args = ", ".join([self.gen_expr(a) for a in node.arguments])
            return f"{callee}({args})"
        return "/* unknown_expr */"