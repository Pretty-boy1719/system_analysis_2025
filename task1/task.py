import sys

def map_nodes(edge_list):
    index_map = {}
    nodes = []
    for a, b in edge_list:
        for node in (a, b):
            if node not in index_map:
                index_map[node] = len(nodes)
                nodes.append(node)
    return index_map, nodes


def build_relations(edge_list, index_map, nodes, root):
    n = len(nodes)
    r1 = [[False] * n for _ in range(n)]
    r2 = [[False] * n for _ in range(n)]
    r3 = [[False] * n for _ in range(n)]
    r4 = [[False] * n for _ in range(n)]
    r5 = [[False] * n for _ in range(n)]

    # граф в виде списка потомков
    tree = {node: [] for node in nodes}
    for a, b in edge_list:
        tree[a].append(b)

    # прямые и обратные связи
    for a, b in edge_list:
        i, j = index_map[a], index_map[b]
        r1[i][j] = True
        r2[j][i] = True

    # обход в глубину
    def explore(start, current, seen):
        for nxt in tree[current]:
            if nxt not in seen:
                seen.add(nxt)
                explore(start, nxt, seen)

    # достижимость (косвенные связи)
    for a in nodes:
        reached = set()
        explore(a, a, reached)
        reached.discard(a)
        for b in reached:
            i, j = index_map[a], index_map[b]
            if not r1[i][j]:
                r3[i][j] = True
            if not r2[j][i]:
                r4[j][i] = True

    # братья и сестры (общие родители)
    for parent, kids in tree.items():
        if len(kids) > 1:
            for i in range(len(kids)):
                for j in range(i + 1, len(kids)):
                    x, y = kids[i], kids[j]
                    ix, iy = index_map[x], index_map[y]
                    r5[ix][iy] = r5[iy][ix] = True

    return r1, r2, r3, r4, r5


def read_edges(filepath):
    with open(filepath, encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]
    pairs = []
    for line in lines:
        left, right = [p.strip() for p in line.split(",", 1)]
        pairs.append((left, right))
    return pairs


def display_matrix(title, matrix):
    print(f"\n{title}")
    for row in matrix:
        print(" ".join("1" if cell else "0" for cell in row))


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file> [root]")
        sys.exit(1)

    filename = sys.argv[1]
    edges = read_edges(filename)
    root = sys.argv[2] if len(sys.argv) > 2 else edges[0][0]

    index_map, nodes = map_nodes(edges)
    r1, r2, r3, r4, r5 = build_relations(edges, index_map, nodes, root)

    for name, matrix in zip(("r1", "r2", "r3", "r4", "r5"), (r1, r2, r3, r4, r5)):
        display_matrix(name, matrix)


if __name__ == "__main__":
    main()
