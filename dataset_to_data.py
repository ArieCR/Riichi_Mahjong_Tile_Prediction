from collections import deque
import gzip
import json
from tenpai import is_tenpai
import sqlite3
from typing import Union
from torch.utils.data import Dataset
import numpy as np
from numpy import ndarray
TILE_CLASS_DICT = {i: i // 4 for i in range(136)}

MAX_DISCARD_TILES = 25
MAX_VALID_ACTIONS = 32

class MahjongData():
    """
    majong data:
    self.player_wind:               int    
    self.position:                  int
    self.is_riichi:                 ndarray
    self.players_points:            ndarray
    self.num_honba:                 int    
    self.num_riichi:                int    
    self.num_remaining_tiles:       int
    self.round_wind:                int    
    self.melds_types:               ndarray
    self.melds_tiles:               ndarray
    self.melds_tiles_from_who:      ndarray
    self.discard_tiles:             ndarray
    self.tsumo_giri:                ndarray
    self.hand_tiles:                ndarray
    self.dora_indicators:           ndarray
    self.tenpai:                    ndarray
    self.waits:                     ndarray
    """

    
    def __init__(self, board_states: dict):

        self.player_wind: int = board_states["player_wind"]
        self.postiion: int = board_states["position"]
        
        melds_types = np.zeros((4, 4), dtype=np.int32) - 1
        melds_tiles = np.zeros((4, 4, 4), dtype=np.int32) - 1
        melds_tiles_from_who = np.zeros((4, 4, 4), dtype=np.int32) - 1
        
        discard_tiles = np.zeros((4, MAX_DISCARD_TILES), dtype=np.int32) - 1
        tsumo_giri = np.zeros((4, MAX_DISCARD_TILES), dtype=np.int32) - 1
        
        hand_tiles = np.zeros(14, dtype=np.int32) - 1
        dora_indicators = np.zeros(5, dtype=np.int32) - 1
        
        hand_tile: ndarray = np.array(list(map(lambda x: TILE_CLASS_DICT[x], sorted(board_states["hand_tiles"]))))
        hand_tiles[:len(hand_tile)] = hand_tile
        
        dora_indicator: ndarray = np.array(list(map(lambda x: TILE_CLASS_DICT[x], board_states["dora_indicators"])))
        dora_indicators[:len(dora_indicator)] = dora_indicator

        _is_tenpai = np.zeros(4, dtype=np.int32)
        waits = np.zeros((4, 34), dtype=np.int32)

        for wind in range(4):
            dis_tiles = board_states[str(wind)]["discards"]
            if dis_tiles:
                discard_tile = list(map(lambda x: TILE_CLASS_DICT[x], dis_tiles))
                is_tsumo_giri = board_states[str(wind)]["tsumo_giri"]
                discard_tile = np.array(discard_tile, dtype=np.int32)
                discard_tiles[wind, :discard_tile.shape[0]] = discard_tile
                tsumo_giri[wind, :discard_tile.shape[0]] = is_tsumo_giri

            melds = board_states[str(wind)]["melds"]
            if not melds: continue

            # Handle melds_type
            melds_type = np.array([meld["type"] for meld in melds], dtype=np.int32) - 2
            max_melds = melds_types.shape[1]  # Assuming the second dimension of melds_types is the max size
            if melds_type.shape[0] > max_melds:
                melds_type = melds_type[:max_melds]  # Truncate if too long
            melds_types[wind, :melds_type.shape[0]] = melds_type

            # Handle melds_tile_from_who
            meld_tile_from_who = [meld["who"] for meld in melds]
            if len(meld_tile_from_who) > max_melds:
                meld_tile_from_who = meld_tile_from_who[:max_melds]  # Truncate if too long
            melds_tiles_from_who[wind, :len(meld_tile_from_who)] = meld_tile_from_who
            melds_tile = [meld["tiles"] for meld in melds]
            # Handle melds_tile
            for i, tiles in enumerate(melds_tile[:max_melds]):  # Truncate if too long
                tile_array = list(map(lambda x: TILE_CLASS_DICT[x], filter(lambda x: x != -1, tiles)))
                melds_tiles[wind, i, :len(tile_array)] = tile_array

            _is_tenpai[wind], wait = is_tenpai(board_states[str(wind)]["hand_tiles"], board_states[str(wind)]["melds"])
            for tile in wait:
                waits[wind][tile] = 1
            
        
        self.is_riichi: ndarray = np.array([board_states[str(wind)]["riichi"] for wind in range(4)])
        self.players_points: ndarray = np.array([board_states[str(wind)]["points"] // 100 for wind in range(4)])
        
        self.num_honba: int = board_states["num_honba"]
        self.num_riichi: int = board_states["num_riichi"]
        self.round_wind: int = board_states["round_wind"]
        self.num_remaining_tiles: int = board_states["remain_tiles"]
        self.melds_types: ndarray = melds_types
        self.melds_tiles: ndarray = melds_tiles
        self.melds_tiles_from_who: ndarray = melds_tiles_from_who
        self.discard_tiles: ndarray = discard_tiles
        self.tsumo_giri: ndarray = tsumo_giri
        self.hand_tiles: ndarray = hand_tiles
        self.dora_indicators: ndarray = dora_indicators
        self.all_hand_tiles = board_states
        self.is_tenpai: ndarray = _is_tenpai
        self.waits: ndarray = waits

class MahjongDataset(Dataset):
    def __init__(self, data_path: str):
        conn = sqlite3.connect(data_path)
        cursor = conn.cursor()
        self.cur = cursor
        
#     def __len__(self):
#         return 

    def __getitem__(self, idx) -> MahjongData:
        try:
            self.cur.execute(f"SELECT data FROM Discard WHERE id = {idx + 1}")
#             self.cur.execute(f"SELECT data FROM Riichi WHERE id = {id + 1}")
#             self.cur.execute(f"SELECT data FROM Chi WHERE id = {id + 1}")
#             self.cur.execute(f"SELECT data FROM Pon WHERE id = {id + 1}")
#             self.cur.execute(f"SELECT data FROM DaiMinKan WHERE id = {id + 1}")
#             self.cur.execute(f"SELECT data FROM ShouMinKan WHERE id = {id + 1}")
#             self.cur.execute(f"SELECT data FROM AnKan WHERE id = {id + 1}")
#             self.cur.execute(f"SELECT data FROM Skip WHERE id = {id + 1}")
        
        except: raise(IndexError(f"{idx} out of range"))
        data = self.cur.fetchall()
        data = data[0][0]
        data = gzip.decompress(data)
        data = json.loads(data)
        mdata = MahjongData(data)
        return mdata
    
    
import time
import torch
from torch import Tensor
from typing import Optional, Union


class Batch:
    def __init__(self, 
                 player_wind:                   Tensor,
                 position:                      Tensor,
                 is_riichi:                     Tensor,
                 players_points:                Tensor,
                 num_honba:                     Tensor,
                 num_riichi:                    Tensor,
                 round_wind:                    Tensor,
                 num_remaining_tiles:           Tensor,
                 melds_types:                   Tensor,
                 melds_tiles:                   Tensor,
                 melds_tiles_from_who:          Tensor,
                 discard_tiles:                 Tensor,
                 tsumo_giri:                    Tensor,
                 hand_tiles:                    Tensor,
                 dora_indicators:               Tensor,
                 ):
        self.player_wind = player_wind
        self.position = position
        self.is_riichi = is_riichi
        self.players_points = players_points
        self.num_honba = num_honba
        self.num_riichi = num_riichi
        self.round_wind = round_wind
        self.num_remaining_tiles = num_remaining_tiles
        self.melds_types = melds_types
        self.melds_tiles = melds_tiles
        self.melds_tiles_from_who = melds_tiles_from_who
        self.discard_tiles = discard_tiles
        self.tsumo_giri = tsumo_giri
        self.hand_tiles = hand_tiles
        self.dora_indicators = dora_indicators

    def cuda(self, dev: Optional[Union[str, int]]=None):
        self.player_wind = self.player_wind.cuda(dev)
        self.position = self.position.cuda(dev)
        self.is_riichi = self.is_riichi.cuda(dev)
        self.players_points = self.players_points.cuda(dev)
        self.num_honba = self.num_honba.cuda(dev)
        self.num_riichi = self.num_riichi.cuda(dev)
        self.round_wind = self.round_wind.cuda(dev)
        self.num_remaining_tiles = self.num_remaining_tiles.cuda(dev)
        self.melds_types = self.melds_types.cuda(dev)
        self.melds_tiles = self.melds_tiles.cuda(dev)
        self.melds_tiles_from_who = self.melds_tiles_from_who.cuda(dev)
        self.discard_tiles = self.discard_tiles.cuda(dev)
        self.tsumo_giri = self.tsumo_giri.cuda(dev)
        self.hand_tiles = self.hand_tiles.cuda(dev)
        self.dora_indicators = self.dora_indicators.cuda(dev)
        return self

    def to(self, dev: Optional[Union[str, int]]=None):
        self.player_wind = self.player_wind.to(dev)
        self.position = self.position.to(dev)
        self.is_riichi = self.is_riichi.to(dev)
        self.players_points = self.players_points.to(dev)
        self.num_honba = self.num_honba.to(dev)
        self.num_riichi = self.num_riichi.to(dev)
        self.round_wind = self.round_wind.to(dev)
        self.num_remaining_tiles = self.num_remaining_tiles.to(dev)
        self.melds_types = self.melds_types.to(dev)
        self.melds_tiles = self.melds_tiles.to(dev)
        self.melds_tiles_from_who = self.melds_tiles_from_who.to(dev)
        self.discard_tiles = self.discard_tiles.to(dev)
        self.tsumo_giri = self.tsumo_giri.to(dev)
        self.hand_tiles = self.hand_tiles.to(dev)
        self.dora_indicators = self.dora_indicators.to(dev)
        return self

    def __len__(self) -> int:
        return self.player_wind.shape[0]


def collator(data_list: list[MahjongData]) -> Batch:
    batch_size = len(data_list)
    data_list = [(data.player_wind,
                  data.postiion,
                  data.is_riichi,
                  data.players_points,
                  data.num_honba,
                  data.num_riichi,
                  data.round_wind,
                  data.num_remaining_tiles,
                  data.melds_types,
                  data.melds_tiles,
                  data.melds_tiles_from_who,
                  data.discard_tiles,
                  data.tsumo_giri,
                  data.hand_tiles,
                  data.dora_indicators,
                  ) for data in data_list]
    (
        player_wind,
        position,
        is_riichi,
        players_points,
        num_honba,
        num_riichi,
        round_wind,
        num_remaining_tiles,
        melds_types,
        melds_tiles,
        melds_tiles_from_who,
        discard_tiles,
        tsumo_giri,
        hand_tiles,
        dora_indicators,
    ) = zip(*data_list)

    player_wind = torch.tensor(player_wind, dtype=torch.long)
    position = torch.tensor(position, dtype=torch.long)
    num_honba = torch.tensor(num_honba, dtype=torch.long)
    num_riichi = torch.tensor(num_riichi, dtype=torch.long)
    round_wind = torch.tensor(round_wind, dtype=torch.long)
    num_remaining_tiles = torch.tensor(num_remaining_tiles, dtype=torch.long)
    is_riichi = torch.stack([torch.from_numpy(x) for x in is_riichi]).long()
    players_points = torch.stack([torch.from_numpy(x) for x in players_points])
    melds_types = torch.stack([torch.from_numpy(x) for x in melds_types]).long()
    melds_tiles = torch.stack([torch.from_numpy(x) for x in melds_tiles]).long()
    melds_tiles_from_who = torch.stack([torch.from_numpy(x) for x in melds_tiles_from_who]).long()
    discard_tiles = torch.stack([torch.from_numpy(x) for x in discard_tiles]).long()
    tsumo_giri = torch.stack([torch.from_numpy(x) for x in tsumo_giri]).long()
    hand_tiles = torch.stack([torch.from_numpy(x) for x in hand_tiles]).long()
    dora_indicators = torch.stack([torch.from_numpy(x) for x in dora_indicators]).long()

    return Batch(player_wind=player_wind,
                 position=position,
                 is_riichi=is_riichi,
                 players_points=players_points,
                 num_honba=num_honba,
                 num_riichi=num_riichi,
                 round_wind=round_wind,
                 num_remaining_tiles=num_remaining_tiles,
                 melds_types=melds_types,
                 melds_tiles=melds_tiles,
                 melds_tiles_from_who=melds_tiles_from_who,
                 discard_tiles=discard_tiles,
                 tsumo_giri=tsumo_giri,
                 hand_tiles=hand_tiles,
                 dora_indicators=dora_indicators,)
