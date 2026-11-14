from lexer import Lexer
from parser import Parser
from codegen import CodeGen

# Le code source en Storm
source = (
    "// Test the Storm compiler\n"
    "pure fn add(a: int, b: int) -> int {\n"
    "    let x = 10\n"
    "    var y: int = 20\n"
    "    y += 1\n"
    "    if x == 10 {\n"
    "        return a + b\n"
    "    }\n"
    "    return 0\n"
    "}\n"
)

print("=== 1. Lexing ===")
lexer = Lexer(source)
tokens = lexer.tokenize()
print(f"Generated {len(tokens)} tokens.")

print("\n=== 2. Parsing ===")
parser = Parser(tokens)
program = parser.parse()
print(f"Parsed {len(program.functions)} function(s).")

print("\n=== 3. AST Structure ===")
def print_ast(node, indent=0):
    prefix = "  " * indent
    print(f"{prefix}{type(node).__name__}")
    if hasattr(node, 'statements'):
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    if hasattr(node, 'body'):
        print_ast(node.body, indent + 1)
    if hasattr(node, 'then_branch'):
        print_ast(node.then_branch, indent + 1)
    if hasattr(node, 'else_branch') and node.else_branch:
        print_ast(node.else_branch, indent + 1)

for func in program.functions:
    print_ast(func)

print("\n=== 4. Generating Verse Code ===")
codegen = CodeGen()
verse_code = codegen.generate(program)

print("\n--- OUTPUT (RAW) ---")
for line in verse_code.split('\n'):
    print(f"[{line}]")
print("--------------------")