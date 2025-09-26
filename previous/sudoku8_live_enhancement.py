import sys; args = sys.argv[1:]
import time


def optimal_pos(invalid_dct):  # finds position with (most invalid symbols <==> least valid symbols)
    best_pos, invalid_at_best_pos = 0, set()  # invalid_at_best_pos: set of invalid symbols at best_pos
    for pos in invalid_dct:
        if len(invalid_dct[pos]) == PW:  # or len(invalid_dct[pos]) == PW - 1:  # pzl invalid or exactly one valid choice
            return pos, invalid_dct[pos]
        if len(invalid_dct[pos]) > len(invalid_at_best_pos):  # found new best position
            best_pos, invalid_at_best_pos = pos, invalid_dct[pos]
    return best_pos, invalid_at_best_pos


def brute_force(pzl, invalid_dct):
    if '.' not in pzl: return pzl

    best_pos, invalid = optimal_pos(invalid_dct)
    choices = SYMBOL_SET - invalid

    best_sym, positions = human_enhancement(pzl)
    if len(positions) < len(choices):
        for i, pos in enumerate(positions):
            sub_pzl, removed, added_invalid = update(pzl, best_sym, pos, invalid_dct)
            b_f = brute_force(sub_pzl, invalid_dct)
            if b_f: return b_f
            cleanup_invalid_dct(best_sym, pos, added_invalid, removed, invalid_dct)
        return ''

    for choice in choices:
        sub_pzl, removed, added_invalid = update(pzl, choice, best_pos, invalid_dct)
        b_f = brute_force(sub_pzl, invalid_dct)
        if b_f: return b_f
        cleanup_invalid_dct(choice, best_pos, added_invalid, removed, invalid_dct)
    return ''


def human_enhancement(pzl):
    best_symbol, min_possible_positions = pzl[0], SYMBOL_LST
    for constraint_set in CONSTRAINTS:
        for symbol in SYMBOL_SET - {pzl[i] for i in constraint_set}:
            possible_positions = []
            for c in constraint_set:
                if pzl[c] != '.':
                    continue
                valid = True
                for n in NEIGHBORS[c]:
                    if pzl[n] == symbol:
                        valid = False
                        break
                if valid:
                    possible_positions.append(c)
            if len(possible_positions) == 0 or len(possible_positions) == 1:
                return symbol, possible_positions
            if len(possible_positions) < len(min_possible_positions):
                min_possible_positions = possible_positions
                best_symbol = symbol
    return best_symbol, min_possible_positions


def update(pzl, choice, best_pos, invalid_dct):
    sub_pzl = pzl[:best_pos] + choice + pzl[best_pos + 1:]
    removed = invalid_dct[best_pos]
    added_invalid = []
    invalid_dct.pop(best_pos)
    for n in NEIGHBORS[best_pos]:
        if sub_pzl[n] == '.' and sub_pzl[best_pos] not in invalid_dct[n]:
            invalid_dct[n].add(sub_pzl[best_pos])
            added_invalid.append(n)
    return sub_pzl, removed, added_invalid


def cleanup_invalid_dct(choice, best_pos, added_invalid, removed, invalid_dct):
    invalid_dct[best_pos] = removed
    for i in added_invalid:
        invalid_dct[i].remove(choice)


def reset_invalid_dct(pzl):
    return {i: {pzl[c] for c in NEIGHBORS[i] if pzl[c] != '.'} for i in range(PW * PW) if pzl[i] == '.'}


def neighbors(i):  # returns all the neighbor positions of i
    return {*[i // (PW * BW) * (PW * BW) + i % PW - i % BW + k + j for k in
              range(BW) for j in range(0, BW * PW, PW)],
            *[i % PW + r * PW for r in range(PW)],
            *[c + i // PW * PW for c in range(PW)]} - {i}


def constraints():  # returns a list of all constraint sets
    boxes = []
    for i in range(PW*PW):
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

    print(f'\n{time.process_time() - start} seconds\n\n')


if __name__ == '__main__': main()
# cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024
