# -*- coding: utf-8 -*-
"""
水桶交互配置
定义空桶装水、水桶放水的方块交互配置
"""

# 水桶交互方块配置
# 格式: {
#     '方块名': {
#         'enable_fill': bool,      # 是否启用空桶装水功能
#         'enable_empty': bool,     # 是否启用水桶放水功能
#         'fill_replace': str,      # 空桶装水时替换的目标方块（None表示不替换）
#         'empty_replace': str,     # 水桶放水时替换的目标方块（None表示不替换）
#     }
# }
WATER_TANK_BLOCKS = {
    # 传统水槽（只装水放水，不替换方块）
    'swan_town:cabinet3': {
        'enable_fill': True,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': None,
    },
    # 重置版水槽
    'swan_town_apple:sink_12_1':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:sink_12',
        'empty_replace': None,
    },
    'swan_town_apple:sink_12':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:sink_12_1',
    },
    'swan_town_apple:sink_11':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:sink_13',
    },
    'swan_town_apple:sink_13':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:sink_11',
        'empty_replace': None,
    },
    'swan_town_apple:bathtub_21':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:bathtub_23',
    },
    'swan_town_apple:bathtub_23':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:bathtub_21',
        'empty_replace': None,
    },
    'swan_town_apple:bathtub_11':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:bathtub_13',
    },
    'swan_town_apple:bathtub_13':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:bathtub_11',
        'empty_replace': None,
    },
    'swan_town_apple:shower_13':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:shower_133',
    },
    'swan_town_apple:shower_133':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:shower_13',
        'empty_replace': None,
    },
    # 青苹果系列
    'swan_town_apple:sink_12_1_green':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:sink_12_green',
        'empty_replace': None,
    },
    'swan_town_apple:sink_12_green':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:sink_12_1_green',
    },
    'swan_town_apple:sink_11_green':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:sink_13_green',
    },
    'swan_town_apple:sink_13_green':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:sink_11_green',
        'empty_replace': None,
    },
    'swan_town_apple:shower_13_green':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:shower_133_green',
    },
    'swan_town_apple:shower_133_green':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:shower_13_green',
        'empty_replace': None,
    },
    'swan_town_apple:bathtub_11_green':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:bathtub_13_green',
    },
    'swan_town_apple:bathtub_13_green':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:bathtub_11_green',
        'empty_replace': None,
    },
    'swan_town_apple:bathtub_21_green':{
        'enable_fill': False,
        'enable_empty': True,
        'fill_replace': None,
        'empty_replace': 'swan_town_apple:bathtub_23_green',
    },
    'swan_town_apple:bathtub_23_green':{
        'enable_fill': True,
        'enable_empty': False,
        'fill_replace': 'swan_town_apple:bathtub_21_green',
        'empty_replace': None,
    },
}