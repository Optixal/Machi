#!/usr/bin/env python3
import sys

def hand_str_to_freq(hand):
    """'2234' -> [0, 2, 1, 1, 0, 0, 0, 0, 0]"""
    frequency_hand = [0] * 9
    for tile in hand:
        frequency_hand[int(tile) - 1] += 1
    return frequency_hand

def hand_freq_to_str(hand):
    """[0, 2, 1, 1, 0, 0, 0, 0, 0] -> '2234'"""
    buffer = ''
    for i in range(len(hand)):
        buffer += hand[i] * str(i + 1)
    return buffer

def checkChow(hand, i):
    sets = min(hand[i], hand[i+1], hand[i+2])
    if sets  > 0:
        hand[i:i+3] = [x - sets for x in hand[i:i+3]]
    return sets

def checkSets(hand, n):
    found = 0
    for i in range(len(hand)):
        # Pong
        if hand[i] >= 3:
            hand[i] -= 3
            found += 1
        # Chow
        if i + 2 < len(hand):
            found += checkChow(hand, i)
    return found == n

"""
14: 4 sets, eyes inside
13: invalid
12: 4 sets, eyes outside
11: 3 sets, eyes inside
10: invalid
 9: 3 sets, eyes outside
 8: 2 sets, eyes inside
 7: invalid
 6: 2 sets, eyes outside
 5: 1 set,  eyes inside
 4: invalid
 3: 1 set,  eyes outside
 2: 0 set,  eyes inside
 1: invalid
"""
def checkHu(hand):
    size = sum(hand)

    # Detect an incomplete hand
    if (size > 14 or size < 2) or (size - 1) % 3 == 0:
        print('Incomplete hand.')
        return False

    # Detect if the eyes are already formed outside of this hand
    eyes_outside = size % 3 == 0

    # Calculate number of sets
    sets = size // 3

    if eyes_outside:
        if checkSets(list(hand), sets):
            print(f'Hand: {hand_freq_to_str(hand)}')
            return True
    else:
        for i in range(len(hand)):
            # If the eyes are inside, find and remove it
            if hand[i] < 2:
                continue
            hand_no_eyes = list(hand)
            hand_no_eyes[i] -= 2
            if checkSets(hand_no_eyes, sets):
                print(f'Hand: {hand_freq_to_str(hand)}, Eye Index: {i + 1}')
                return True

"""
13: 4 sets, eyes inside
12: invalid
11: 4 sets, eyes outside
10: 3 sets, eyes inside
 9: invalid
 8: 3 sets, eyes outside
 7: 2 sets, eyes inside
 6: invalid
 5: 2 sets, eyes outside
 4: 1 set,  eyes inside
 3: invalid
 2: 1 set,  eyes outside
 1: 0 set,  eyes inside
 0: invalid
"""
def checkWaits(hand):
    size = sum(hand)
    waits = []

    # Detect a non-waiting hand
    if (size > 13 or size < 1) or size % 3 == 0:
        print('Hand is not waiting.')
        return waits

    for tile in range(9):
        # If there's already 4 of the same tiles, skip
        if hand[tile] == 4:
            continue
        test_hand = list(hand) # make a copy
        test_hand[tile] += 1
        if checkHu(test_hand):
            print(f'Wait tile found: {tile + 1}')
            waits.append(tile + 1)
    return waits

def main():
    # hand = [0, 2, 2, 2, 3, 3, 1, 0, 0]
    # hand = [0, 0, 3, 1, 1, 1, 1, 0, 0]
    # hand = [0, 1, 1, 1, 3, 2, 2, 0, 0]
    # hand = [0, 0, 3, 1, 1, 1, 1, 1, 0]
    # hand = [0, 1, 1, 4, 1, 4, 1, 1, 0]
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} 3334567')
        exit(1)
    hand = sys.argv[1]
    hand = hand_str_to_freq(hand)
    print(checkWaits(hand))

if __name__ == '__main__':
    main()

