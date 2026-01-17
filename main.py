import sys
from pathlib import Path
from sctokenizer import (
    CTokenizer,
    CppTokenizer,
    JavaTokenizer,
    PythonTokenizer,
    PhpTokenizer,
    TokenType
)
import random
import string


def obfuscate(file_content: list[str], filename: str) -> str:
    obf_map = {} # original_token -> obfuscated_token
    output_tokens = []

    for line in file_content:
        tokens, language = tokenize(line, filename)

        if language == "NONE":
            output_tokens.append(line)
            output_tokens.append("\n")
            continue
        
        for tok_info in tokens:
            tok = tok_info.token_value

            if tok_info.token_type == TokenType.IDENTIFIER:
                if tok not in obf_map.keys():
                    obf_map[tok] = obfuscate_token(tok, obf_map.values())
                output_tokens.append(obf_map[tok])
            else:
                output_tokens.append(tok)
        
        output_tokens.append("\n")

    return " ".join(output_tokens)


def obfuscate_token(token: str, existing: list[str], min_len: int = 1) -> str:
    if not token:
        max_len = 2
    else:
        max_len = max(1, 2 * len(token))

    alphabet = string.ascii_letters + string.digits

    while True:
        length = random.randint(min_len, max_len)
        candidate = "".join(random.choices(alphabet, k=length))

        if candidate not in existing:
            return f"__{candidate}"


def tokenize(content: str, filename: str):
    ext = filename.lower().split(".")[-1]

    tokenizer_map = {
        "c": (CTokenizer, "C"),
        "h": (CTokenizer, "C"),
        "cpp": (CppTokenizer, "C++"),
        "cc": (CppTokenizer, "C++"),
        "cxx": (CppTokenizer, "C++"),
        "hpp": (CppTokenizer, "C++"),
        "java": (JavaTokenizer, "Java"),
        "py": (PythonTokenizer, "Python"),
        "php": (PhpTokenizer, "PHP"),
    }

    if ext not in tokenizer_map:
        return ([], "NONE")

    tokenizer, language = tokenizer_map[ext][0](), tokenizer_map[ext][1]
    tokens = tokenizer.tokenize(content)
    return (tokens, language)


def process_file(input_path: Path, output_dir: Path):
    try:
        with input_path.open("r", encoding="utf-8") as infile:
            content = infile.readlines()
    except:
        print(f"Unable to process file: {input_path.name}. Skipping it.")
        return

    new_content = obfuscate(content, input_path.name)

    output_path = output_dir / input_path.name
    with output_path.open("w", encoding="utf-8") as outfile:
        outfile.write(new_content)


def main():
    if len(sys.argv) != 2:
        print("Usage: program.py <path_to_directory_or_file>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: {input_path} does not exist")
        sys.exit(1)

    # Create output directory in current working directory
    output_dir = Path.cwd() / "obfus_output"
    output_dir.mkdir(exist_ok=True)

    if input_path.is_file():
        process_file(input_path, output_dir)

    elif input_path.is_dir():
        for item in input_path.iterdir():
            if item.is_file():
                process_file(item, output_dir)

    else:
        print("Error: Path is neither a file nor a directory")
        sys.exit(1)


if __name__ == "__main__":
    main()
