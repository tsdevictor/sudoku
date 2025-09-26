import sys; args = sys.argv[1:]
import time
import cProfile


def brute_force(pzl, invalid_dct):
    if '.' not in pzl: return pzl

    best_pos, invalid = optimal_pos(invalid_dct)  # optimal position based on number of possible symbols
    symbols = SYMBOL_SET - invalid
    best_sym, positions = optimal_sym(pzl, len(symbols))  # optimal symbol based on number of possible positions

    if len(positions) < len(symbols):  # traverse whichever has (less possibilities <=> less chance of error)
        for i, pos in enumerate(positions):
            sub_pzl, copy = updated(pzl, best_sym, pos, invalid_dct, i != len(positions) - 1)  # update variables
            b_f = brute_force(sub_pzl, copy)  # recursive call
            if b_f: return b_f                # solution found
        return ''                             # no choice was valid => this recursive branch was invalid

    for i, choice in enumerate(symbols):  # same process as just above
        sub_pzl, copy = updated(pzl, choice, best_pos, invalid_dct, i != len(symbols) - 1)
        b_f = brute_force(sub_pzl, copy)
        if b_f: return b_f
    return ''


def optimal_pos(invalid_dct):  # finds position with (most invalid symbols <==> least valid symbols)
    best_pos, most_invalid, max_len = 0, set(), 0  # most_invalid: set of invalid symbols at best_pos
    for pos in invalid_dct:
        curr_len = len(invalid_dct[pos])           # avoid recomputing len (profiler said this was costly)
        if curr_len < 2:                           # 0 or 1 valid choice
            return pos, invalid_dct[pos]
        if curr_len > max_len:                     # found new best position
            best_pos, most_invalid, max_len = pos, invalid_dct[pos], curr_len
    return best_pos, most_invalid


def optimal_sym(pzl, len_choices):  # finds symbol with the least possible positions within its constraint set
    best_sym, min_positions, min_len = pzl[0], SYMBOL_LST, len_choices  # min_positions: list of possible positions
    for cs in CONSTRAINTS:                             # go through each constraint set
        for sym in SYMBOL_SET - {pzl[i] for i in cs}:  # go through each unfilled symbol in the constraint set
            possible_positions = []
            for c in cs:
                if pzl[c] != '.': continue
                for n in NEIGHBORS[c]:
                    if pzl[n] == sym: break
                else: possible_positions.append(c)            # symbol can be put in that position
                if len(possible_positions) >= min_len: break  # no need to go further: this will not be a min anyway
            curr_len = len(possible_positions)                # avoid recomputing len (profiler said this was costly)
            if curr_len < 2:                # pzl invalid or exactly one valid choice
                return sym, possible_positions
            if curr_len < min_len:                            # found new min
                best_sym, min_positions, min_len = sym, possible_positions, curr_len
    return best_sym, min_positions


def updated(pzl, sym, pos, invalid_dct, need_copy: bool):  # need_copy False if checking last of available choices
    sub_pzl = pzl[:pos] + sym + pzl[pos + 1:]              # put the symbol into the puzzle
    if need_copy: copy = {i: invalid_dct[i] for i in invalid_dct}
    else: copy = invalid_dct
    copy.pop(pos)                                          # nothing can now go in the position that was last filled
    for n in NEIGHBORS[pos]:                               # add last put symbol to invalid symbol set of each neighbor
        if sub_pzl[n] == '.':
            copy[n] = copy[n] | {sub_pzl[pos]}
    return sub_pzl, copy


def reset_invalid_dct(pzl):  # create invalid symbol set at beginning of solving each pzl
    return {i: {pzl[c] for c in NEIGHBORS[i] if pzl[c] != '.'} for i in range(PW * PW) if pzl[i] == '.'}


def reset_position_dct(pzl):
    return {s: {c for c in range(PW*PW) if pzl[c] == '.'} for s in SYMBOL_LST}


def neighbors(i):  # return all the neighbor positions of given position i
    boxes = [{0, 1, 2, 3, 12, 13, 14, 15, 24, 25, 26, 27},
             {4, 5, 6, 7, 16, 17, 18, 19, 28, 29, 30, 31},
             {8, 9, 10, 11, 20, 21, 22, 23, 32, 33, 34, 35},
             {36, 37, 38, 39, 48, 49, 50, 51, 60, 61, 62, 63},
             {40, 41, 42, 43, 52, 53, 54, 55, 64, 65, 66, 67},
             {44, 45, 46, 47, 56, 57, 58, 59, 68, 69, 70, 71},
             {72, 73, 74, 75, 84, 85, 86, 87, 96, 97, 98, 99},
             {76, 77, 78, 79, 88, 89, 90, 91, 100, 101, 102, 103},
             {80, 81, 82, 83, 92, 93, 94, 95, 104, 105, 106, 107},
             {108, 109, 110, 111, 120, 121, 122, 123, 132, 133, 134, 135},
             {112, 113, 114, 115, 124, 125, 126, 127, 136, 137, 138, 139},
             {116, 117, 118, 119, 128, 129, 130, 131, 140, 141, 142, 143}]

    correct_box = {}
    for box in boxes:
        if i in box:
            correct_box = box
            break

    return {*correct_box,
            *[i % PW + r * PW for r in range(PW)],
            *[c + i // PW * PW for c in range(PW)]} - {i}


def constraints():  # return list of all constraint sets
    boxes = [{0, 1, 2, 3, 12, 13, 14, 15, 24, 25, 26, 27},
             {4, 5, 6, 7, 16, 17, 18, 19, 28, 29, 30, 31},
             {8, 9, 10, 11, 20, 21, 22, 23, 32, 33, 34, 35},
             {36, 37, 38, 39, 48, 49, 50, 51, 60, 61, 62, 63},
             {40, 41, 42, 43, 52, 53, 54, 55, 64, 65, 66, 67},
             {44, 45, 46, 47, 56, 57, 58, 59, 68, 69, 70, 71},
             {72, 73, 74, 75, 84, 85, 86, 87, 96, 97, 98, 99},
             {76, 77, 78, 79, 88, 89, 90, 91, 100, 101, 102, 103},
             {80, 81, 82, 83, 92, 93, 94, 95, 104, 105, 106, 107},
             {108, 109, 110, 111, 120, 121, 122, 123, 132, 133, 134, 135},
             {112, 113, 114, 115, 124, 125, 126, 127, 136, 137, 138, 139},
             {116, 117, 118, 119, 128, 129, 130, 131, 140, 141, 142, 143}]

    # boxes = []
    # for i in range(PW * PW):
    #     box = {i // (PW * BH) * (PW * BH) + i % PW - i % BW + k + j for k in range(BW) for j in range(0, BH * PW, PW)}
    #     if box not in boxes: boxes.append(box)

    cols = [{c + r * PW for r in range(PW)} for c in range(PW)]
    rows = [{c + r * PW for c in range(PW)} for r in range(PW)]

    return boxes + cols + rows


def set_globals(pzl):  # define all the global variables
    # noinspection PyGlobalUndefined
    global PW, BW, BH, SYMBOL_SET, SYMBOL_LST, CONSTRAINTS, NEIGHBORS, STATS

    PW = int(len(pzl) ** 0.5)
    BW = max(w for w in range(1, 2 + int(PW ** 0.5 + 0.5)) if PW % w == 0)  # sub-block width
    BH = PW // BW
    SYMBOL_SET = {sym for sym in pzl if sym != '.'}
    for char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g']:
        if len(SYMBOL_SET) == PW: break
        SYMBOL_SET.add(char)
    # print(SYMBOL_SET)
    SYMBOL_LST = [*SYMBOL_SET]
    CONSTRAINTS = constraints()
    NEIGHBORS = [neighbors(i) for i in range(len(pzl))]  # neighbors for every position

    # print(sorted([*NEIGHBORS[16]]))

    STATS = {}


def update_stats(phrase):
    if phrase not in STATS:
        STATS[phrase] = 0
    STATS[phrase] += 1


def grader_print(i, pzl, solution):  # format is [pzl_number: original pzl \n solution checksum]
    min_ascii = ord('1')
    print(f'{i + 1}: ' + (' ' if i < 9 else '') + (' ' if i < 99 else '') + pzl)
    print(f'     {solution} {sum(ord(char) - min_ascii for char in solution)}')


def main():
    start = time.process_time()

    args = ['12x12.txt']
    with open(args[0]) as f:
        for i, line in enumerate(f):
            pzl = line.strip()
            if i == 0:
                set_globals(pzl)
                reset_position_dct(pzl)
            solution = brute_force(pzl, reset_invalid_dct(pzl))
            grader_print(i, pzl, solution)

    print(time.process_time() - start)
    print(len('..275..B...14.3...79..2...5..2..7..8.6...5.1.7B..3.....41........C....698B....9........98.....A..1C.A.2...9.C..1..A..4...A..49...5.37...B..5A1..'))


if __name__ == '__main__': main()  # cProfile.run('main()', sort='tottime')

# Tristan Devictor, pd. 6, 2024
