# -*- coding: utf-8 -*-
# 原版斧子名称集合
AXE_NAMES = {
    'minecraft:axe',
    'minecraft:wooden_axe',
    'minecraft:stone_axe',
    'minecraft:iron_axe',
    'minecraft:diamond_axe',
    'minecraft:netherite_axe',
    'minecraft:golden_axe',
}

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
}

# 合并所有方块循环映射，便于快速查询
ALL_BLOCK_CYCLES = {}
for cycle_dict in BLOCK_CYCLES.values():
    ALL_BLOCK_CYCLES.update(cycle_dict)

# 椅子列表（可坐下的方块）
CHAIR_LIST = [
    'swan_town:sofa1',
    'swan_town:sofa2',
    'swan_town:sofa3',
    'swan_town:sofa4',
    'swan_town:chair',
    'swan_town:stool',
    'swan_town:stool1',
    'swan_town:stool2',
    'swan_town:stool3',
]

# 坐下动画名称
SIT_ANIMATION_NAME = "animation.sit_chair"

# 座位高度偏移
SEAT_HEIGHT = 0.5
