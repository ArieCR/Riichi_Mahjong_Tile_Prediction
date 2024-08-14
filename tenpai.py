orphans = [0, 8, 9, 17, 18, 26, 27, 28, 29, 30, 31, 32, 33]


def is_thirteen_orphans(hand):
    return sorted(set(hand)) == orphans


def is_seven_pairs(hand):
    unique_tiles = sorted(list(set(hand)))
    if len(unique_tiles) != 7:
        return False
    duplicated_list = [item for item in unique_tiles for _ in range(2)]
    return duplicated_list == hand


def is_four_trips(hand):
    if len(hand) == 2 and hand[0] == hand[1]:
        return True
    hand_cpy = hand.copy()
    for tile in range(34):
        if hand_cpy.count(tile) >= 3:
            for _ in range(3):
                hand_cpy.remove(tile)
            if is_four_trips(hand_cpy):
                return True
            hand_cpy = hand.copy()
    for color in range(3):
        for num in range(7):
            start_tile = color*9+num
            if all(start_tile + i in hand_cpy for i in range(3)):
                for i in range(3):
                    hand_cpy.remove(start_tile+i)
                if is_four_trips(hand_cpy):
                    return True
                hand_cpy = hand.copy()
    return False


def is_tenpai(hand):
    hand = sorted(hand)
    norm_hand = [tile // 4 for tile in hand]
    tenpai = False
    waits = []
    for tile in range(34):
        test_hand = norm_hand + [tile]
        if is_thirteen_orphans(test_hand):
            waits.append(tile)
            tenpai = True
            continue
        if is_seven_pairs(test_hand):
            waits.append(tile)
            tenpai = True
            continue
        if is_four_trips(test_hand):
            waits.append(tile)
            tenpai = True
    #print("hand is: ", norm_hand)
    #print("waits are: ", waits)

    return tenpai, waits


