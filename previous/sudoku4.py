import sys; args = sys.argv[1:]
import time


def is_invalid(pzl, pos):
    if pos == -1:
        return False
    for i in NEIGHBORS[pos]:
        if pzl[i] == pzl[pos]:
            return True
    return False


def optimal_pos(invalid_dct):  # finds position with (most invalid symbols <==> least valid symbols)
    best_pos, invalid_at_best_pos = 0, set()  # invalid_at_best_pos: set of invalid symbols at best_pos
    for pos in invalid_dct:
        if len(invalid_dct[pos]) == PW or len(invalid_dct[pos]) == PW - 1:  # pzl invalid or exactly one valid choice
            return pos, invalid_dct[pos]
        if len(invalid_dct[pos]) > len(invalid_at_best_pos):  # found new best position
            best_pos, invalid_at_best_pos = pos, invalid_dct[pos]
    return best_pos, invalid_at_best_pos


def brute_force(pzl, pos, invalid_dct):
    # if is_invalid(pzl, pos): return ''  # unnecessary: this will never happen because such choices are not even processed
    if '.' not in pzl: return pzl

    invalid_dct = updated_invalid(pzl, pos, invalid_dct)  # invalid symbols {position: invalid_symbol_set}
    best_pos, invalid = optimal_pos(invalid_dct)
    for choice in SYMBOLS - invalid:
        sub_pzl = pzl[:best_pos] + choice + pzl[best_pos + 1:]
        b_f = brute_force(sub_pzl, best_pos, invalid_dct)
        if b_f: return b_f
    return ''


def updated_invalid(pzl, pos, invalid_dct):
    copy = {i: {*invalid_dct[i]} for i in invalid_dct}
    if pos == -1:  # first call of brute_force
        return copy
    copy.pop(pos)
    for i in NEIGHBORS[pos]:
        if i in copy:
            copy[i].add(pzl[pos])
    return copy


def reset_invalid(pzl):
    return {i: {pzl[c] for c in NEIGHBORS[i] if pzl[c] != '.'} for i in range(PW * PW) if pzl[i] == '.'}


def neighbors(i):  # returns all the neighbor positions of i
    return {*[i // (PW * BW) * (PW * BW) + i % PW - i % BW + k + j for k in
              range(BW) for j in range(0, BW * PW, PW)],
            *[i % PW + r * PW for r in range(PW)],
            *[c + i // PW * PW for c in range(PW)]} - {i}


def set_globals(pzl):
    # noinspection PyGlobalUndefined
    global PW, BW, SYMBOLS, NEIGHBORS, STATS_COUNT

    PW = int(len(pzl) ** 0.5)  # puzzle width
    BW = int(PW ** 0.5)  # sub-block width
    SYMBOLS = {str(i + 1) for i in range(PW)}  # set of all symbols
    NEIGHBORS = [neighbors(i) for i in range(PW * PW)]  # neighbors for every position
    STATS_COUNT = {}  # debugging tool


def update_stats(phrase):
    if phrase not in STATS_COUNT:
        STATS_COUNT[phrase] = 0
    STATS_COUNT[phrase] += 1


def grader_print(i, pzl, solution):
    min_ascii = ord('1')
    print(f'{i + 1}: ' + (' ' if i < 9 else '') + pzl)
    print(f'    {solution} {sum(ord(char) - min_ascii for char in solution)}')


def square_print(pzl):
    for r in range(PW):
        for c in range(PW):
            print(pzl[r * PW + c], end=" ")
            if c + 1 != PW and (c + 1) % BW == 0:
                print("|", end=" ")
        if r + 1 != PW and (r + 1) % BW == 0:
            print()
            print("- " * PW, end=" ")
        print()


def main():
    start = time.process_time()

    with open(args[0]) as f:
        for i, line in enumerate(f):
            pzl = line.strip()
            if i == 0:
                set_globals(pzl)
            solution = brute_force(pzl, -1, reset_invalid(pzl))
            grader_print(i, pzl, solution)

    print(time.process_time() - start)


if __name__ == '__main__': main()
# cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024
