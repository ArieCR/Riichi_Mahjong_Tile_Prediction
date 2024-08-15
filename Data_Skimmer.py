import random
import numpy as np

# if return is none then we don't have to predict waits, nothing to predict.
# else it returns a vector of 361 elements that would hopefully be used to predict waits.
def waits_data_proccessing(data):
    opponent_is_tnepai = 0
    tenpais = []
    for wind in range(4):
        if data.is_tenpai[wind] and data.player_wind != wind:
            opponent_is_tnepai = 1
            tenpais.append(wind)
    if opponent_is_tnepai == 0:
        return None
    target_player = random.choice(tenpais)
    vector = np.zeros(368, dtype=np.int16)
    vector[0] = target_player
    vector[1] = data.player_wind
    vector[2] = data.round_wind
    for wind in range(4):
        vector[wind + 3] = data.players_points[wind]
    vector[7] = data.num_remaining_tiles
    vector[8] = data.num_riichi
    vector[9] = data.num_honba
    for wind in range(4):
        vector[wind + 10] = data.is_riichi[wind]

    for i in range(5):
        vector[i + 14] = - 1
    for i in range(len(data.dora_indicators)):
        vector[i + 14] = data.dora_indicators[i]

    for i in range(14):
        vector[i + 19] = -1
    for i in range(len(data.hand_tiles)):
        vector[i + 19] = data.hand_tiles[i]

    for wind in range(4):
        for meld in range(4):
            for tile in range(4):
                vector[wind * 2 * 4 * 4 + meld * 2 * 4 + tile + 33] = data.melds_tiles[wind][meld][tile]
            for tile in range(4):
                vector[wind * 2 * 4 * 4 + meld * 2 * 4 + 4 + tile + 33] = data.melds_tiles_from_who[wind][meld][tile]
    for wind in range(4):
        for i in range(25):
            vector[wind * 25 * 2 + i * 2 + 160] = data.discard_tiles[wind][i]
            vector[wind * 25 * 2 + i * 2 + 1 + 160] = data.tsumo_giri[wind][i]
    assert (len(vector) == 368)
    return vector, data.waits[target_player]
def tenpai_data_proccecising(data):
    players = []
    for wind in range(4):
        if data.player_wind != wind:
            players.append(wind)
    target_player = random.choice(players)
    vector = np.zeros(368, dtype=np.int16)
    vector[0] = target_player
    vector[1] = data.player_wind
    vector[2] = data.round_wind
    for wind in range(4):
        vector[wind + 3] = data.players_points[wind]
    vector[7] = data.num_remaining_tiles
    vector[8] = data.num_riichi
    vector[9] = data.num_honba
    for wind in range(4):
        vector[wind + 10] = data.is_riichi[wind]

    for i in range(5):
        vector[i + 14] = - 1
    for i in range(len(data.dora_indicators)):
        vector[i + 14] = data.dora_indicators[i]

    for i in range(14):
        vector[i + 19] = -1
    for i in range(len(data.hand_tiles)):
        vector[i + 19] = data.hand_tiles[i]

    for wind in range(4):
        for meld in range(4):
            for tile in range(4):
                vector[wind * 2 * 4 * 4 + meld * 2 * 4 + tile + 33] = data.melds_tiles[wind][meld][tile]
            for tile in range(4):
                vector[wind * 2 * 4 * 4 + meld * 2 * 4 + 4 + tile + 33] = data.melds_tiles_from_who[wind][meld][tile]
    for wind in range(4):
        for i in range(25):
            vector[wind * 25 * 2 + i * 2 + 160] = data.discard_tiles[wind][i]
            vector[wind * 25 * 2 + i * 2 + 1 + 160] = data.tsumo_giri[wind][i]
    assert (len(vector) == 368)
    return vector, target_player
