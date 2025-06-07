def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def compare_trees(tree1_lines, tree2_lines):
    total = max(len(tree1_lines), len(tree2_lines))
    common = sum(1 for a, b in zip(tree1_lines, tree2_lines) if a == b)
    similarity = (common / total) * 100 if total > 0 else 0
    return similarity, common, total

def main():
    tree1 = read_lines("parse_tree.txt")
    tree2 = read_lines("parse_tree_group.txt")

    similarity, common, total = compare_trees(tree1, tree2)

    print("🔍 تعداد خطوط مشابه:", common)
    print("📄 تعداد کل خطوط:", total)
    print(f"📊 درصد شباهت: {similarity:.2f}%")

if __name__ == "__main__":
    main()
