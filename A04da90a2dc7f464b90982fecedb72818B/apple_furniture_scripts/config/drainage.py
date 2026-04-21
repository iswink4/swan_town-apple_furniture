# -*- coding: utf-8 -*-
"""
排水功能配置
定义浴缸/水槽的排水动画配置
"""

# 排水方块映射配置
# 格式: {原方块: (放水中方块, 放水完成方块)}
DRAINAGE_BLOCKS = {
    'swan_town_apple:sink_12':('swan_town_apple:sink_12_2','swan_town_apple:sink_12_1'),
    'swan_town_apple:sink_11':('swan_town_apple:sink_13_1','swan_town_apple:sink_13'),
    'swan_town_apple:bathtub_11':('swan_town_apple:bathtub_12','swan_town_apple:bathtub_13'),
    'swan_town_apple:bathtub_21':('swan_town_apple:bathtub_22','swan_town_apple:bathtub_23'),
    'swan_town_apple:shower_13':('swan_town_apple:shower_132','swan_town_apple:shower_133'),
    'swan_town_apple:sink_12_green':('swan_town_apple:sink_12_2_green','swan_town_apple:sink_12_1_green'),
    'swan_town_apple:sink_11_green':('swan_town_apple:sink_13_1_green','swan_town_apple:sink_13_green'),
    'swan_town_apple:shower_13_green':('swan_town_apple:shower_132_green','swan_town_apple:shower_133_green'),
    'swan_town_apple:bathtub_11_green':('swan_town_apple:bathtub_12_green','swan_town_apple:bathtub_13_green'),
    'swan_town_apple:bathtub_21_green':('swan_town_apple:bathtub_22_green','swan_town_apple:bathtub_23_green'),
}