import json
import sys
import os


def _flatten_once(seq):
    """Разворачивает список на один уровень."""
    out = []
    for elem in seq:
        if isinstance(elem, list):
            out.extend(elem)
        else:
            out.append(elem)
    return out


def _collect_unique(a, b):
    """Собирает уникальные элементы из двух ранжировок."""
    seen = []
    for item in _flatten_once(a) + _flatten_once(b):
        if item not in seen:
            seen.append(item)
    return seen


def _as_blocks(rank):
    """Каждый элемент превращает в блок; списки оставляет блоками."""
    blocks = []
    for entry in rank:
        if isinstance(entry, list):
            blocks.append(entry)
        else:
            blocks.append([entry])
    return blocks


def _make_matrix(blocks, universe):
    size = len(universe)
    pos = {obj: idx for idx, obj in enumerate(universe)}
    mat = [[0] * size for _ in range(size)]

    for i, group in enumerate(blocks):
        # внутри блока — взаимная достижимость
        for x in group:
            for y in group:
                mat[pos[x]][pos[y]] = 1

        # блоки после текущего — "правее"
        for follow in blocks[i + 1:]:
            for x in group:
                for y in follow:
                    mat[pos[x]][pos[y]] = 1

    return mat


def _locate_conflicts(m1, m2, all_objs):
    n = len(all_objs)
    bad = []

    for i in range(n):
        for j in range(i + 1, n):
            a_ij = m1[i][j] == 1 and m1[j][i] == 0
            a_ji = m1[j][i] == 1 and m1[i][j] == 0
            b_ij = m2[i][j] == 1 and m2[j][i] == 0
            b_ji = m2[j][i] == 1 and m2[i][j] == 0

            # Противоречие в относительном порядке
            if (a_ij and b_ji) or (a_ji and b_ij):
                bad.append([all_objs[i], all_objs[j]])

    return bad


def _merge_conflicted(conflicts, objs):
    consumed = set()
    result = []

    for obj in objs:
        if obj in consumed:
            continue

        pack = [obj]
        for pair in conflicts:
            if obj in pair:
                for other in pair:
                    if other != obj:
                        pack.append(other)
                        consumed.add(other)

        consumed.add(obj)

        if len(pack) > 1:
            result.append(sorted(pack))
        else:
            result.append(obj)

    return result


def _read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _store_output(data):
    dst = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.json")
    with open(dst, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def main(path_a, path_b):
    rank_a = _read_json(path_a)
    rank_b = _read_json(path_b)

    universe = _collect_unique(rank_a, rank_b)

    blocks_a = _as_blocks(rank_a)
    blocks_b = _as_blocks(rank_b)

    matrix_a = _make_matrix(blocks_a, universe)
    matrix_b = _make_matrix(blocks_b, universe)

    conflicts = _locate_conflicts(matrix_a, matrix_b, universe)
    final_rank = _merge_conflicted(conflicts, universe)

    _store_output({"conflicts": conflicts, "ranking": final_rank})

    return json.dumps(final_rank, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(main(sys.argv[1], sys.argv[2]))
