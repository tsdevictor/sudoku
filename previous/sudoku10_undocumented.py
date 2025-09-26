import sys; args = sys.argv[1:]
import time
import cProfile


def brute_force(pzl, invalid_dct):
    if '.' not in pzl: return pzl

    best_pos, invalid = optimal_pos(invalid_dct)
    choices = SYMBOL_SET - invalid
    best_sym, positions = optimal_sym(pzl, len(choices))

    if len(positions) < len(choices):
        for i, pos in enumerate(positions):
            sub_pzl, copy = updated(pzl, best_sym, pos, invalid_dct, i != len(positions) - 1)
            b_f = brute_force(sub_pzl, copy)
            if b_f: return b_f
        return ''

    for i, choice in enumerate(choices):
        sub_pzl, copy = updated(pzl, choice, best_pos, invalid_dct, i != len(choices) - 1)
        b_f = brute_force(sub_pzl, copy)
        if b_f: return b_f
    return ''


def optimal_pos(invalid_dct):  # finds position with (most invalid symbols <==> least valid symbols)
    best_pos, most_invalid, max_len = 0, set(), 0  # most_invalid: set of invalid symbols at best_pos
    for pos in invalid_dct:
        curr_len = len(invalid_dct[pos])
        if curr_len == PW or curr_len == PW - 1:  # pzl invalid or exactly one valid choice
            return pos, invalid_dct[pos]
        if curr_len > max_len:  # found new best position
            best_pos, most_invalid, max_len = pos, invalid_dct[pos], curr_len
    return best_pos, most_invalid


def optimal_sym(pzl, len_choices):
    best_sym, min_positions, min_len = pzl[0], SYMBOL_LST, len_choices
    for cs in CONSTRAINTS:
        for sym in SYMBOL_SET - {pzl[i] for i in cs}:
            possible_positions = []
            for c in cs:
                if pzl[c] != '.': continue
                for n in NEIGHBORS[c]:
                    if pzl[n] == sym: break
                else: possible_positions.append(c)  # for-loop above did not terminate normally (break)
                if len(possible_positions) >= min_len: break
            curr_len = len(possible_positions)
            if curr_len == 0 or curr_len == 1:
                return sym, possible_positions
            if curr_len < min_len:
                best_sym, min_positions, min_len = sym, possible_positions, curr_len
    return best_sym, min_positions


def updated(pzl, sym, pos, invalid_dct, need_copy: bool):
    sub_pzl = pzl[:pos] + sym + pzl[pos + 1:]
    if need_copy:
        copy = {i: {*invalid_dct[i]} for i in invalid_dct}
    else:
        copy = invalid_dct
    copy.pop(pos)
    for n in NEIGHBORS[pos]:
        if sub_pzl[n] == '.':
            copy[n].add(sub_pzl[pos])
    return sub_pzl, copy


def reset_invalid_dct(pzl):
    return {i: {pzl[c] for c in NEIGHBORS[i] if pzl[c] != '.'} for i in range(PW * PW) if pzl[i] == '.'}


def neighbors(i):  # returns all the neighbor positions of i
    return {*[i // (PW * BW) * (PW * BW) + i % PW - i % BW + k + j for k in
              range(BW) for j in range(0, BW * PW, PW)],
            *[i % PW + r * PW for r in range(PW)],
            *[c + i // PW * PW for c in range(PW)]} - {i}


def constraints():  # returns a list of all constraint lists
    boxes = []
    for i in range(PW * PW):
        box = {i // (PW * BW) * (PW * BW) + i % PW - i % BW + k + j for k in range(BW) for j in range(0, BW * PW, PW)}
        if box not in boxes: boxes.append(box)
    cols = [{c + r * PW for r in range(PW)} for c in range(PW)]
    rows = [{c + r * PW for c in range(PW)} for r in range(PW)]

    return boxes + cols + rows


def set_globals(pzl):
    # noinspection PyGlobalUndefined
    global PW, BW, SYMBOL_SET, SYMBOL_LST, CONSTRAINTS, NEIGHBORS

    PW = int(len(pzl) ** 0.5)  # puzzle width
    BW = int(PW ** 0.5)  # sub-block width
    SYMBOL_SET = {str(i + 1) for i in range(PW)}  # set of all symbols
    SYMBOL_LST = [*SYMBOL_SET]
    CONSTRAINTS = constraints()
    NEIGHBORS = [neighbors(i) for i in range(PW * PW)]  # neighbors for every position


def grader_print(i, pzl, solution):
    min_ascii = ord('1')
    print(f'{i + 1}: ' + (' ' if i < 9 else '') + (' ' if i < 99 else '') + pzl)
    print(f'     {solution} {sum(ord(char) - min_ascii for char in solution)}')


def main():
    start = time.process_time()

    with open(args[0]) as f:
        for i, line in enumerate(f):
            pzl = line.strip()
            if i == 0:
                set_globals(pzl)
            solution = brute_force(pzl, reset_invalid_dct(pzl))
            grader_print(i, pzl, solution)

    print(time.process_time() - start)


if __name__ == '__main__': main()  # cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024
