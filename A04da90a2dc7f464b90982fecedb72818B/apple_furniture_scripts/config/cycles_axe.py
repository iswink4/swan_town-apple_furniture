# -*- coding: utf-8 -*-
"""
斧子方块循环配置
定义斧子点击方块时的样式循环映射
"""

# 方块循环映射配置（按类型分类）
BLOCK_CYCLES = {
    # 桌子循环
    'table': {
        'swan_town:table1': 'swan_town:table2',
        'swan_town:table2': 'swan_town:table3',
        'swan_town:table3': 'swan_town:table4',
        'swan_town:table4': 'swan_town:table1'
    },
    # 沙发循环
    'sofa': {
        'swan_town:sofa1': 'swan_town:sofa2',
        'swan_town:sofa2': 'swan_town:sofa3',
        'swan_town:sofa3': 'swan_town:sofa4',
        'swan_town:sofa4': 'swan_town:sofa1'
    },
    # 长凳循环
    'stool': {
        'swan_town:stool': 'swan_town:stool1',
        'swan_town:stool1': 'swan_town:stool2',
        'swan_town:stool2': 'swan_town:stool3',
        'swan_town:stool3': 'swan_town:stool',
    },
    # 画循环
    'picture': {
        'swan_town:picture1': 'swan_town:picture2',
        'swan_town:picture2': 'swan_town:picture3',
        'swan_town:picture3': 'swan_town:picture1',
    },
    # 电视循环
    'tv': {
        'swan_town:tv1': 'swan_town:tv2',
        'swan_town:tv2': 'swan_town:tv1',
    },
    # 电脑循环
    'computer': {
        'swan_town:computer1': 'swan_town:computer2',
        'swan_town:computer2': 'swan_town:computer1',
    },
    # 窗帘循环1
    'curtain1': {
        'swan_town:curtain11': 'swan_town:curtain12',
        'swan_town:curtain12': 'swan_town:curtain13',
        'swan_town:curtain13': 'swan_town:curtain14',
        'swan_town:curtain14': 'swan_town:curtain15',
        'swan_town:curtain15': 'swan_town:curtain16',
        'swan_town:curtain16': 'swan_town:curtain17',
        'swan_town:curtain17': 'swan_town:curtain11',
    },
    # 窗帘循环2
    'curtain2': {
        'swan_town:curtain21': 'swan_town:curtain22',
        'swan_town:curtain22': 'swan_town:curtain23',
        'swan_town:curtain23': 'swan_town:curtain24',
        'swan_town:curtain24': 'swan_town:curtain21',
    },

    # 重制版
    # 沙发循环
    'sofa1':{
        'swan_town_apple:sofa_11':'swan_town_apple:sofa_12',
        'swan_town_apple:sofa_12':'swan_town_apple:sofa_13',
        'swan_town_apple:sofa_13':'swan_town_apple:sofa_14',
        'swan_town_apple:sofa_14':'swan_town_apple:sofa_11',
    },
    # 凳子循环
    'stool1':{
        "swan_town_apple:stool_11":'swan_town_apple:stool_12',
        "swan_town_apple:stool_12":'swan_town_apple:stool_13',
        "swan_town_apple:stool_13":'swan_town_apple:stool_14',
        "swan_town_apple:stool_14":'swan_town_apple:stool_11',
    },
    # 桌子循环
    'table1':{
        'swan_town_apple:table_11':'swan_town_apple:table_12',
        'swan_town_apple:table_12':'swan_town_apple:table_13',
        'swan_town_apple:table_13':'swan_town_apple:table_14',
        'swan_town_apple:table_14':'swan_town_apple:table_11',
    },
    'table2':{
        'swan_town_apple:table_21':'swan_town_apple:table_22',
        'swan_town_apple:table_22':'swan_town_apple:table_23',
        'swan_town_apple:table_23':'swan_town_apple:table_24',
        'swan_town_apple:table_24':'swan_town_apple:table_21',
    },
    'table3':{
        'swan_town_apple:table_31':'swan_town_apple:table_32',
        'swan_town_apple:table_32':'swan_town_apple:table_33',
        'swan_town_apple:table_33':'swan_town_apple:table_34',
        'swan_town_apple:table_34':'swan_town_apple:table_31',
    },
    # 青苹果系列
    'sofa1_green':{
        'swan_town_apple:sofa_11_green':'swan_town_apple:sofa_12_green',
        'swan_town_apple:sofa_12_green':'swan_town_apple:sofa_13_green',
        'swan_town_apple:sofa_13_green':'swan_town_apple:sofa_14_green',
        'swan_town_apple:sofa_14_green':'swan_town_apple:sofa_11_green',
    },
    'stool1_green':{
        'swan_town_apple:stool_11_green':'swan_town_apple:stool_12_green',
        'swan_town_apple:stool_12_green':'swan_town_apple:stool_13_green',
        'swan_town_apple:stool_13_green':'swan_town_apple:stool_14_green',
        'swan_town_apple:stool_14_green':'swan_town_apple:stool_11_green',
    },
    'table1_green':{
        'swan_town_apple:table_11_green':'swan_town_apple:table_12_green',
        'swan_town_apple:table_12_green':'swan_town_apple:table_13_green',
        'swan_town_apple:table_13_green':'swan_town_apple:table_14_green',
        'swan_town_apple:table_14_green':'swan_town_apple:table_11_green',
    },
    'table2_green':{
        'swan_town_apple:table_21_green':'swan_town_apple:table_22_green',
        'swan_town_apple:table_22_green':'swan_town_apple:table_23_green',
        'swan_town_apple:table_23_green':'swan_town_apple:table_24_green',
        'swan_town_apple:table_24_green':'swan_town_apple:table_21_green',
    },
    'table3_green':{
        'swan_town_apple:table_31_green':'swan_town_apple:table_32_green',
        'swan_town_apple:table_32_green':'swan_town_apple:table_33_green',
        'swan_town_apple:table_33_green':'swan_town_apple:table_34_green',
        'swan_town_apple:table_34_green':'swan_town_apple:table_31_green',
    },
}

# 合并所有方块循环映射，便于快速查询
ALL_BLOCK_CYCLES = {}
for cycle_dict in BLOCK_CYCLES.values():
    ALL_BLOCK_CYCLES.update(cycle_dict)