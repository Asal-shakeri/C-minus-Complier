import scanner
from antlr_runner import run_antlr_tokenizer
from comparator import Check

if __name__ == "__main__":
    print("🔍 Running manual scanner...")
    scanner.Scanner('input.txt').scan()

    print("🤖 Running ANTLR lexer...")
    run_antlr_tokenizer()

    print("📊 Comparing token files...")
    Check()

