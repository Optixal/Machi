#!/usr/bin/env python3

import sys


class Combination:

    def __init__(self):
        self.pongs = []
        self.chows = []
        self.eye = None
        self.winning_tile = None

    def count_sets(self):
        return len(self.pongs) + len(self.chows)

    def set_eye(self, eye_index):
        self.eye = eye_index

    def set_winning_tile(self, tile_index):
        self.winning_tile = tile_index

    def is_all_pong(self):
        pass

    def __str__(self):
        buffer = ''
        if not self.winning_tile == None:
            buffer += f'[{self.winning_tile + 1}] '
        buffer += '['
        all_sets = self.chows + self.pongs
        all_sets.sort(key=lambda x: x[0])
        for chow in all_sets:
            for tile in chow:
                buffer += str(tile + 1)
            buffer += ' '
        buffer = buffer.strip()
        if not self.eye == None:
            buffer += ' ' + str(self.eye + 1) * 2
        buffer += ']'
        return buffer


def hand_str_to_freq(hand):
    """'2234' -> (0, 2, 1, 1, 0, 0, 0, 0, 0)"""
    frequency_hand = [0] * 9
    for tile in hand:
        frequency_hand[int(tile) - 1] += 1
    return tuple(frequency_hand)


def hand_freq_to_str(hand):
    """(0, 2, 1, 1, 0, 0, 0, 0, 0) -> '2234'"""
    buffer = ''
    for i in range(len(hand)):
        buffer += hand[i] * str(i + 1)
    return buffer


def find_pong(hand, i):
    if hand[i] >= 3:
        hand[i] -= 3
        return (i,) * 3
    return


def find_chows(hand, i):
    chows = []
    # If the next 2 consecutive tiles are beyond the size of the hand, skip
    if i + 2 >= len(hand):
        return chows
    sets = min(hand[i], hand[i + 1], hand[i + 2])
    for j in range(3):
        hand[i + j] -= sets
    for _ in range(sets):
        chows.append((i, i + 1, i + 2))
    return chows


def find_sets(hand):
    combination = Combination()
    hand = list(hand)
    for i in range(len(hand)):
        # Pongs
        pong = find_pong(hand, i)
        if pong:
            combination.pongs.append(pong)
        # Chows
        combination.chows.extend(find_chows(hand, i))
    return combination


def find_sets_chows_first(hand):
    combination = Combination()
    hand = list(hand)
    for i in range(len(hand)):
        # Chows
        combination.chows.extend(find_chows(hand, i))
        # Pongs
        pong = find_pong(hand, i)
        if pong:
            combination.pongs.append(pong)
    return combination


def find_hu(hand):
    win_combis = []
    size = sum(hand)
    if (size > 14 or size < 2) or (size - 1) % 3 == 0:
        print('Incomplete hand.')
        return win_combis

    # Detect if the eyes are already formed outside of this hand
    eyes_outside = size % 3 == 0

    # Calculate number of sets
    sets = size // 3

    if eyes_outside:
        combination = find_sets(hand)
        if combination.count_sets() == sets:
            win_combis.append(combination)
            if len(combination.pongs) >= 3:
                combination = find_sets_chows_first(hand)
                if not len(combination.pongs) >= 3:
                    win_combis.append(combination)
    else:
        # If the eyes are inside, find and remove it
        for i in range(len(hand)):
            if hand[i] < 2:
                continue
            hand_eyeless = list(hand)
            hand_eyeless[i] -= 2
            hand_eyeless = tuple(hand_eyeless)
            combination = find_sets(hand_eyeless)
            if combination.count_sets() == sets:
                combination.set_eye(i) # add back the eyes
                win_combis.append(combination)
                if len(combination.pongs) >= 3:
                    combination = find_sets_chows_first(hand_eyeless)
                    if not len(combination.pongs) >= 3:
                        combination.set_eye(i) # add back the eyes
                        win_combis.append(combination)

    return win_combis


def find_waits(hand_str):
    waits = []
    hand_str = hand_str.strip()
    size = len(hand_str)
    if (size > 13 or size < 1) or size % 3 == 0:
        print('Hand is not waiting.')
        return waits

    try:
        hand = hand_str_to_freq(hand_str)
    except ValueError:
        print('Hand is invalid, contains characters.')
        return waits

    # Check if adding any tile (1-9) will make this hand win/hu
    for tile in range(9):

        # If there's more than 4 of the same tile, hand is invalid 
        if hand[tile] > 4:
            print(f'Hand is invalid, more than four of tile {tile + 1}.')
            return waits

        # If there's already 4 of the same tiles, skip
        if hand[tile] == 4:
            continue

        # Make a copy and add 1 tile to test out
        test_hand = list(hand)
        test_hand[tile] += 1
        test_hand = tuple(test_hand)
        win_combis = find_hu(test_hand)
        for combi in win_combis:
            combi.set_winning_tile(tile)
        waits.extend(win_combis)

    return waits


def generate_output(waits):
    buffer = ''
    tiles = []
    for c in waits:
        buffer += str(c) + '\n'
        if c.winning_tile + 1 not in tiles:
            tiles.append(c.winning_tile + 1)
    buffer += f'\nYou\'re waiting for: {tiles}'
    return buffer


def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} 3334567')
        exit(1)
    hand = sys.argv[1]

    waits = find_waits(hand)
    print(generate_output(waits))


if __name__ == '__main__':
    main()
