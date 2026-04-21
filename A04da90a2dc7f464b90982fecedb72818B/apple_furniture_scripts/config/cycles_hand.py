# -*- coding: utf-8 -*-
"""
空手方块循环配置
定义空手点击方块时的样式循环映射
"""

# 空手点击方块循环映射配置（按类型分类）
HAND_BLOCK_CYCLES = {
    # 灯光循环
    'light': {
        'swan_town:light1': 'swan_town:light1_off',
        'swan_town:light1_off': 'swan_town:light1',
        'swan_town:light2': 'swan_town:light2_off',
        'swan_town:light2_off': 'swan_town:light2',
        'swan_town:light3': 'swan_town:light3_off',
        'swan_town:light3_off': 'swan_town:light3',
    },
    # 重置版窗帘
    'curtain1':{
        'swan_town_apple:curtain_31':'swan_town_apple:curtain_32',
        'swan_town_apple:curtain_32':'swan_town_apple:curtain_33',
        'swan_town_apple:curtain_33':'swan_town_apple:curtain_31',
    },
    'curtain2':{
        'swan_town_apple:curtain_21':'swan_town_apple:curtain_22',
        'swan_town_apple:curtain_22':'swan_town_apple:curtain_23',
        'swan_town_apple:curtain_23':'swan_town_apple:curtain_21',
    },
    'curtain3':{
        'swan_town_apple:curtain_11':'swan_town_apple:curtain_12',
        'swan_town_apple:curtain_12':'swan_town_apple:curtain_13',
        'swan_town_apple:curtain_13':'swan_town_apple:curtain_14',
        'swan_town_apple:curtain_14':'swan_town_apple:curtain_11',
    },
    # 电脑循环
    'computer1':{
        'swan_town_apple:computer_22':'swan_town_apple:computer_21',
        'swan_town_apple:computer_21':'swan_town_apple:computer_22',
    },
    'computer2':{
        'swan_town_apple:computer_12':'swan_town_apple:computer_11',
        'swan_town_apple:computer_11':'swan_town_apple:computer_12',
    },
    # 电视循环
    'tv1':{
        'swan_town_apple:tv_11':'swan_town_apple:tv_12',
        'swan_town_apple:tv_12':'swan_town_apple:tv_11',
    },
    'tv2':{
        'swan_town_apple:tv_21':'swan_town_apple:tv_22',
        'swan_town_apple:tv_22':'swan_town_apple:tv_21',
    },
    # 水槽填充
    'sink1':{
        'swan_town_apple:sink_12_1':'swan_town_apple:sink_12'
    },
    'sink2':{
        'swan_town_apple:sink_13':'swan_town_apple:sink_11'
    },
    # 浴缸填充
    'bathtub1':{
        'swan_town_apple:bathtub_13':'swan_town_apple:bathtub_11'
    },
    'bathtub2':{
        'swan_town_apple:bathtub_23':'swan_town_apple:bathtub_21'
    },
    # 淋浴填充
    'shower':{
        'swan_town_apple:shower_133':'swan_town_apple:shower_13'
    },
    # 灯循环
    'lamp1':{
        'swan_town_apple:lamp_11':'swan_town_apple:lamp_11_off',
        'swan_town_apple:lamp_11_off':'swan_town_apple:lamp_11'
    },
    'lamp2':{
        'swan_town_apple:lamp_12':'swan_town_apple:lamp_12_off',
        'swan_town_apple:lamp_12_off':'swan_town_apple:lamp_12'
    },
    'lamp3':{
        'swan_town_apple:lamp_13':'swan_town_apple:lamp_13_off',
        'swan_town_apple:lamp_13_off':'swan_town_apple:lamp_13'
    },
    'lamp4':{
        'swan_town_apple:lamp_14':'swan_town_apple:lamp_14_off',
        'swan_town_apple:lamp_14_off':'swan_town_apple:lamp_14'
    },
    'lamp5':{
        'swan_town_apple:lamp_15':'swan_town_apple:lamp_15_off',
        'swan_town_apple:lamp_15_off':'swan_town_apple:lamp_15'
    },
    'lamp6':{
        'swan_town_apple:lamp_16':'swan_town_apple:lamp_16_off',
        'swan_town_apple:lamp_16_off':'swan_town_apple:lamp_16'
    },
    'lamp7':{
        'swan_town_apple:lamp_17':'swan_town_apple:lamp_17_off',
        'swan_town_apple:lamp_17_off':'swan_town_apple:lamp_17'
    },
    # 青苹果系列
    'computer1_green':{
        'swan_town_apple:computer_22_green':'swan_town_apple:computer_21_green',
        'swan_town_apple:computer_21_green':'swan_town_apple:computer_22_green',
    },
    'computer2_green':{
        'swan_town_apple:computer_12_green':'swan_town_apple:computer_11_green',
        'swan_town_apple:computer_11_green':'swan_town_apple:computer_12_green',
    },
    'tv1_green':{
        'swan_town_apple:tv_11_green':'swan_town_apple:tv_12_green',
        'swan_town_apple:tv_12_green':'swan_town_apple:tv_11_green',
    },
    'tv2_green':{
        'swan_town_apple:tv_21_green':'swan_town_apple:tv_22_green',
        'swan_town_apple:tv_22_green':'swan_town_apple:tv_21_green',
    },
    'sink1_green':{
        'swan_town_apple:sink_12_1_green':'swan_town_apple:sink_12_green'
    },
    'sink2_green':{
        'swan_town_apple:sink_13_green':'swan_town_apple:sink_11_green'
    },
    'shower_green':{
        'swan_town_apple:shower_133_green':'swan_town_apple:shower_13_green'
    },
    'lamp1_green':{
        'swan_town_apple:lamp_11_green':'swan_town_apple:lamp_11_off_green',
        'swan_town_apple:lamp_11_off_green':'swan_town_apple:lamp_11_green'
    },
    'lamp2_green':{
        'swan_town_apple:lamp_12_green':'swan_town_apple:lamp_12_off_green',
        'swan_town_apple:lamp_12_off_green':'swan_town_apple:lamp_12_green'
    },
    'lamp3_green':{
        'swan_town_apple:lamp_13_green':'swan_town_apple:lamp_13_off_green',
        'swan_town_apple:lamp_13_off_green':'swan_town_apple:lamp_13_green'
    },
    'lamp4_green':{
        'swan_town_apple:lamp_14_green':'swan_town_apple:lamp_14_off_green',
        'swan_town_apple:lamp_14_off_green':'swan_town_apple:lamp_14_green'
    },
    'lamp5_green':{
        'swan_town_apple:lamp_15_green':'swan_town_apple:lamp_15_off_green',
        'swan_town_apple:lamp_15_off_green':'swan_town_apple:lamp_15_green'
    },
    'lamp6_green':{
        'swan_town_apple:lamp_16_green':'swan_town_apple:lamp_16_off_green',
        'swan_town_apple:lamp_16_off_green':'swan_town_apple:lamp_16_green'
    },
    'lamp7_green':{
        'swan_town_apple:lamp_17_green':'swan_town_apple:lamp_17_off_green',
        'swan_town_apple:lamp_17_off_green':'swan_town_apple:lamp_17_green'
    },
    'curtain1_green':{
        'swan_town_apple:curtain_11_green':'swan_town_apple:curtain_12_green',
        'swan_town_apple:curtain_12_green':'swan_town_apple:curtain_13_green',
        'swan_town_apple:curtain_13_green':'swan_town_apple:curtain_14_green',
        'swan_town_apple:curtain_14_green':'swan_town_apple:curtain_11_green',
    },
    'curtain2_green':{
        'swan_town_apple:curtain_21_green':'swan_town_apple:curtain_22_green',
        'swan_town_apple:curtain_22_green':'swan_town_apple:curtain_23_green',
        'swan_town_apple:curtain_23_green':'swan_town_apple:curtain_21_green',
    },
    'curtain3_green':{
        'swan_town_apple:curtain_31_green':'swan_town_apple:curtain_32_green',
        'swan_town_apple:curtain_32_green':'swan_town_apple:curtain_33_green',
        'swan_town_apple:curtain_33_green':'swan_town_apple:curtain_31_green',
    },
    'bathtub1_green':{
        'swan_town_apple:bathtub_13_green':'swan_town_apple:bathtub_11_green'
    },
    'bathtub2_green':{
        'swan_town_apple:bathtub_23_green':'swan_town_apple:bathtub_21_green'
    },
}

# 合并所有空手方块循环映射，便于快速查询
ALL_HAND_BLOCK_CYCLES = {}
for cycle_dict in HAND_BLOCK_CYCLES.values():
    ALL_HAND_BLOCK_CYCLES.update(cycle_dict)