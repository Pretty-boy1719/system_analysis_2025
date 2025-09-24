def main():
    import sys

    path = sys.argv[1]
  
    with open(path, "r", encoding="utf-8-sig") as f:
        lines = [line.strip() for line in f if line.strip()]

    edges = []
    nodes = []
    idx = {}

    for line in lines:
        u, v = map(str.strip, line.split(",", 1))
        edges.append((u, v))

        for node in (u, v):
            if node not in idx:
                idx[node] = len(nodes)
                nodes.append(node)

    n = len(nodes)
    M = [[0] * n for _ in range(n)]

    for u, v in edges:
        i, j = idx[u], idx[v]
        M[i][j] = 1

    print(M)


if __name__ == "__main__":
    main()
