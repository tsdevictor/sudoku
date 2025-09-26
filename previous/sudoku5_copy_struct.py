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
    choices = SYMBOLS - invalid
    for i, choice in enumerate(choices):
        sub_pzl, copy = updated(pzl, choice, best_pos, invalid_dct, i != len(choices)-1)
        b_f = brute_force(sub_pzl, copy)
        if b_f: return b_f
    return ''


def updated(pzl, choice, best_pos, invalid_dct, need_copy: bool):
    sub_pzl = pzl[:best_pos] + choice + pzl[best_pos + 1:]
    if need_copy:
        copy = {i: {*invalid_dct[i]} for i in invalid_dct}
    else: copy = invalid_dct
    copy.pop(best_pos)
    for n in NEIGHBORS[best_pos]:
        if sub_pzl[n] == '.':
            copy[n].add(sub_pzl[best_pos])
    return sub_pzl, copy


def reset_invalid(pzl):
    return {i: {pzl[c] for c in NEIGHBORS[i] if pzl[c] != '.'} for i in range(PW * PW) if pzl[i] == '.'}


def neighbors(i):  # returns all the neighbor positions of i
    return {*[i // (PW * BW) * (PW * BW) + i % PW - i % BW + k + j for k in
              range(BW) for j in range(0, BW * PW, PW)],
            *[i % PW + r * PW for r in range(PW)],
            *[c + i // PW * PW for c in range(PW)]} - {i}


def set_globals(pzl):
    # noinspection PyGlobalUndefined
    global PW, BW, SYMBOLS, NEIGHBORS

    PW = int(len(pzl) ** 0.5)  # puzzle width
    BW = int(PW ** 0.5)  # sub-block width
    SYMBOLS = {str(i + 1) for i in range(PW)}  # set of all symbols
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
            solution = brute_force(pzl, reset_invalid(pzl))
            grader_print(i, pzl, solution)

    print(time.process_time() - start)


if __name__ == '__main__': main()
# cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024
