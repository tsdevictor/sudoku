import sys; args = sys.argv[1:]
import time
import cProfile


def brute_force(pzl, invalid_dct, enhance_dct):
    if '.' not in pzl: return pzl

    best_pos, invalid = optimal_pos(invalid_dct)
    choices = SYMBOL_SET - invalid

    best_sym, positions = optimal_sym(enhance_dct)

    if len(positions) < len(choices):
        for i, pos in enumerate(positions):
            sub_pzl, copy_invalid, copy_enhance = updated(pzl, best_sym, pos, invalid_dct, enhance_dct, i != len(positions) - 1)
            b_f = brute_force(sub_pzl, copy_invalid, copy_enhance)
            if b_f: return b_f
        return ''

    for i, choice in enumerate(choices):
        sub_pzl, copy_invalid, copy_enhance = updated(pzl, choice, best_pos, invalid_dct, enhance_dct, i != len(choices)-1)
        b_f = brute_force(sub_pzl, copy_invalid, copy_enhance)
        if b_f: return b_f
    return ''


def optimal_pos(invalid_dct):  # finds position with (most invalid symbols <==> least valid symbols)
    best_pos, invalid_at_best_pos = 0, set()  # invalid_at_best_pos: set of invalid symbols at best_pos
    for pos in invalid_dct:
        if len(invalid_dct[pos]) == PW:  # or len(invalid_dct[pos]) == PW - 1:  # pzl invalid or exactly one valid choice
            return pos, invalid_dct[pos]
        if len(invalid_dct[pos]) > len(invalid_at_best_pos):  # found new best position
            best_pos, invalid_at_best_pos = pos, invalid_dct[pos]
    return best_pos, invalid_at_best_pos


def optimal_sym(enhance_dct):
    best_sym, min_possible_positions = SYMBOL_LST[0], SYMBOL_LST
    for cs in enhance_dct:
        for sym in enhance_dct[cs]:
            if len(enhance_dct[cs][sym]) == 0:
                return sym, enhance_dct[cs][sym]
            if len(enhance_dct[cs][sym]) < len(min_possible_positions):
                best_sym, min_possible_positions = sym, enhance_dct[cs][sym]
    return best_sym, min_possible_positions


def updated(pzl, choice, pos, invalid_dct, enhance_dct, need_copy: bool):
    sub_pzl = pzl[:pos] + choice + pzl[pos + 1:]
    if need_copy:
        copy_invalid = {i: {*invalid_dct[i]} for i in invalid_dct}
        copy_enhance = {i: {k: {*enhance_dct[i][k]} for k in enhance_dct[i]} for i in enhance_dct}
    else:
        copy_invalid = invalid_dct
        copy_enhance = enhance_dct
    copy_invalid.pop(pos)
    for n in NEIGHBORS[pos]:
        if sub_pzl[n] == '.':
            copy_invalid[n].add(sub_pzl[pos])
    to_remove = []
    for cs in copy_enhance:
        if pos in cs and sub_pzl[pos] in copy_enhance[cs]:
            copy_enhance[cs].pop(sub_pzl[pos])
        if '.' not in cs:
            to_remove.append(cs)
    for r in to_remove:
        copy_enhance.pop(r)

    return sub_pzl, copy_invalid, copy_enhance


def create_invalid_dct(pzl):
    return {i: {pzl[c] for c in NEIGHBORS[i] if pzl[c] != '.'} for i in range(PW * PW) if pzl[i] == '.'}


def create_enhance_dct(pzl):
    enhance_dct = {}
    for cs in CONSTRAINTS:
        if cs in enhance_dct: continue
        enhance_dct[cs] = {}
        for sym in SYMBOL_SET - {pzl[i] for i in cs}:
            for c in cs:
                if pzl[c] != '.':
                    continue
                valid = True
                for n in NEIGHBORS[c]:
                    if pzl[n] == sym:
                        valid = False
                        break
                if valid:
                    if sym not in enhance_dct[cs]:
                        enhance_dct[cs][sym] = []
                    enhance_dct[cs][sym].append(c)
    return enhance_dct


def neighbors(i):  # returns all the neighbor positions of i
    return {*[i // (PW * BW) * (PW * BW) + i % PW - i % BW + k + j for k in
              range(BW) for j in range(0, BW * PW, PW)],
            *[i % PW + r * PW for r in range(PW)],
            *[c + i // PW * PW for c in range(PW)]} - {i}


def constraints():  # returns a list of all constraint tuples
    boxes = []
    for i in range(PW*PW):
        box = [i // (PW * BW) * (PW * BW) + i % PW - i % BW + k + j for k in range(BW) for j in range(0, BW * PW, PW)]
        boxes.append(box)
    cols = [[i % PW + r * PW for r in range(PW)] for i in range(PW*PW)]
    rows = [[c + i // PW * PW for c in range(PW)] for i in range(PW*PW)]

    return [tuple(boxes[i] + cols[i] + rows[i]) for i in range(PW*PW)]


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
            solution = brute_force(pzl, create_invalid_dct(pzl), create_enhance_dct(pzl))
            grader_print(i, pzl, solution)

    print(time.process_time() - start)


if __name__ == '__main__': cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024
