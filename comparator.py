def Check(scanner_tokens_file='tokens.txt', antlr_tokens_file='ANTLR_p1.txt'):
    def read_tokens(path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        tokens = []
        for line in lines:
            parts = line.strip().split()[1:]  # skip lineno
            tokens.extend(parts)
        return tokens

    scanner_tokens = read_tokens(scanner_tokens_file)
    antlr_tokens = read_tokens(antlr_tokens_file)

    min_len = min(len(scanner_tokens), len(antlr_tokens))
    match_count = sum(1 for i in range(min_len) if scanner_tokens[i] == antlr_tokens[i])
    total = max(len(scanner_tokens), len(antlr_tokens))

    similarity = (match_count / total) * 100 if total > 0 else 100
    print(f"Similarity: {similarity:.2f}%")

