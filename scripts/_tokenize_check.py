import tokenize
import io
import os

base = os.path.dirname(os.path.abspath(__file__))

files_to_check = [
    'core/v8/bestseller_opening_templates_v16.py',
    'core/v8/opening_examples_library_v15.py',
]

for rel_path in files_to_check:
    fpath = os.path.join(base, rel_path)
    print(f'\n=== {rel_path} ===')

    with open(fpath, 'r', encoding='utf-8') as f:
        source = f.read()
        lines = source.split('\n')

    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
        print('  All tokens OK!')

        # Check for unclosed triple-quoted strings
        in_triple = None
        for tok in tokens:
            if tok.type == tokenize.STRING and tok.string.startswith('"""'):
                if in_triple is None:
                    in_triple = tok
                else:
                    # Closing
                    in_triple = None
        if in_triple:
            print(f'  UNCLOSED triple-quoted string starting at line {in_triple.start[0]}')

    except tokenize.TokenError as e:
        print(f'  TokenError: {e}')
    except SyntaxError as e:
        print(f'  SyntaxError at line {e.lineno}: {e.msg}')
    except IndentationError as e:
        print(f'  IndentationError at line {e.lineno}: {e.msg}')
