from typing import List, Dict, Set, Tuple
import math
import sys


def task(source: str, root: str) -> Tuple[float, float]:
    """
    Основная функция: принимает список связей между вершинами (в виде CSV-строки)
    и имя корневой вершины, затем вычисляет два значения — H и h.
    """
    text = source.strip()
    if not text:
        return (0.0, 0.0)

    # Парсим строки в пары (u, v)
    edge_list: List[Tuple[str, str]] = []
    vertex_set: Set[str] = set()
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 2:
            continue
        u, v = parts
        edge_list.append((u, v))
        vertex_set.update([u, v])

    vertex_set.add(root)

    # Формируем список потомков для каждой вершины
    children_map: Dict[str, List[str]] = {v: [] for v in vertex_set}
    for a, b in edge_list:
        children_map[a].append(b)

    # Вычисляем глубину каждой вершины от корня
    depth_map: Dict[str, int] = {root: 0}
    queue = [root]
    while queue:
        current = queue.pop()
        for nxt in children_map.get(current, []):
            depth_map[nxt] = depth_map[current] + 1
            queue.append(nxt)

    # Рекурсивно собираем всех потомков для каждой вершины
    def gather_descendants(node: str, storage: Dict[str, Set[str]]) -> Set[str]:
        total: Set[str] = set()
        for child in children_map.get(node, []):
            total.add(child)
            total |= gather_descendants(child, storage)
        storage[node] = total
        return total

    desc_map: Dict[str, Set[str]] = {}
    gather_descendants(root, desc_map)

    # Разные виды отношений между вершинами
    rel_direct = set(edge_list)                        # прямые связи
    rel_inverse = {(b, a) for (a, b) in edge_list}     # обратные связи

    # связи через два и более уровня
    rel_skip = set()
    for a in vertex_set:
        for b in desc_map.get(a, set()):
            if depth_map.get(b, 0) - depth_map.get(a, 0) >= 2:
                rel_skip.add((a, b))
    rel_skip_inv = {(b, a) for (a, b) in rel_skip}

    # связи между "соседями" — вершинами с общим родителем
    rel_siblings = set()
    for p, childs in children_map.items():
        for i in range(len(childs)):
            for j in range(len(childs)):
                if i != j:
                    rel_siblings.add((childs[i], childs[j]))

    relations = [rel_direct, rel_inverse, rel_skip, rel_skip_inv, rel_siblings]
    total_nodes = len(vertex_set)

    if total_nodes <= 1:
        return (0.0, 0.0)

    # Подсчёт энтропии
    H_value = 0.0
    norm = total_nodes - 1
    for node in vertex_set:
        for rel in relations:
            deg = sum(1 for (src, _) in rel if src == node)
            p = deg / norm
            if p > 0:
                H_value -= p * math.log(p, 2)

    # Нормализация результата
    const_factor = 1 / (math.e * math.log(2))
    H_ref = const_factor * total_nodes * len(relations)
    norm_entropy = H_value / H_ref if H_ref > 0 else 0.0

    return round(H_value, 1), round(norm_entropy, 1)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python task.py <csv_file> <root>")
        sys.exit(1)

    file_path, root_node = sys.argv[1], sys.argv[2]
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    H, h = task(content, root_node)
    print(H, h)
