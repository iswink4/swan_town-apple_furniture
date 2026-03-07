# -*- coding: utf-8 -*-
import time
from .QuModLibs.Server import *
from .QuModLibs.Util import QThrottle
from .config import AXE_NAMES, ALL_BLOCK_CYCLES, CHAIR_LIST, SIT_ANIMATION_NAME, SEAT_HEIGHT

sitting_players = {}
last_click_time = {}

@Listen(Events.ServerBlockUseEvent)
def use(args):
    block_name = args['blockName']
    player_id = args['playerId']
    x, y, z = args['x'], args['y'], args['z']
    
    if block_name not in CHAIR_LIST:
        return
    
    now = time.time()
    last_time = last_click_time.get(player_id, 0)
    if now - last_time < 0.3:
        return
    last_click_time[player_id] = now
    
    comp = serverApi.GetEngineCompFactory()
    item_comp = comp.CreateItem(player_id)
    hand_item = item_comp.GetPlayerItem(0, 0, False)
    
    if hand_item and hand_item.get('newItemName') in AXE_NAMES:
        return
    
    if player_id in sitting_players:
        stand_up(player_id)
    else:
        sit_down(player_id, x, y, z)

def sit_down(player_id, x, y, z):
    comp = serverApi.GetEngineCompFactory()
    seat_pos = (x + 0.5, y + SEAT_HEIGHT, z + 0.5)
    
    pos_comp = comp.CreatePos(player_id)
    pos_comp.SetFootPos(seat_pos)
    
    sitting_players[player_id] = {"pos": (x, y, z), "seat_pos": seat_pos}
    Call(player_id, "PlaySitAnim")

def stand_up(player_id):
    if player_id not in sitting_players:
        return
    del sitting_players[player_id]
    Call(player_id, "StopSitAnim")

@Listen(Events.OnScriptTickServer)
def on_tick():
    comp = serverApi.GetEngineCompFactory()
    for player_id, data in list(sitting_players.items()):
        pos_comp = comp.CreatePos(player_id)
        current_pos = pos_comp.GetFootPos()
        if current_pos:
            dx = current_pos[0] - data["seat_pos"][0]
            dy = current_pos[1] - data["seat_pos"][1]
            dz = current_pos[2] - data["seat_pos"][2]
            if dx*dx + dy*dy + dz*dz > 0.3:
                stand_up(player_id)

@Listen(Events.DestroyBlockEvent)
def on_block_destroy(args):
    pos = (args['x'], args['y'], args['z'])
    for pid, data in list(sitting_players.items()):
        if data["pos"] == pos:
            stand_up(pid)
