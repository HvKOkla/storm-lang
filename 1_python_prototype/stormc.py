import sys
import os
from lexer import Lexer
from parser import Parser
from codegen import CodeGen

def compile_file(input_path, output_path):
    try:
        # 1. Lire le fichier source .storm
        with open(input_path, "r", encoding="utf-8") as f:
            source = f.read()
            
        print(f"[*] Compiling {input_path}...")

        # 2. Lexer
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # 3. Parser
        parser = Parser(tokens)
        program = parser.parse()

        # 4. CodeGen
        codegen = CodeGen()
        verse_code = codegen.generate(program)

        # 5. Écrire le fichier .verse
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(verse_code)

        print(f"[+] Success! Generated {output_path}")
        
    except Exception as e:
        print(f"[-] Error compiling {input_path}:")
        print(e)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python stormc.py <input.storm> [output.verse]")
        print("Example: python stormc.py test.storm")
        sys.exit(1)

    input_file = sys.argv[1]
    
    # Si l'utilisateur ne donne pas de nom de sortie, on remplace juste l'extension
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + ".verse"

    compile_file(input_file, output_file)

if __name__ == "__main__":
    main()