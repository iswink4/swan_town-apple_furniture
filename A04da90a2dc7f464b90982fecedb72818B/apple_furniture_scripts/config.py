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
    'swan_town:toilet',
    'swan_town_apple:chair_11',
    'swan_town_apple:chair_12',
    'swan_town_apple:chair_13',
    'swan_town_apple:chair_14',
    'swan_town_apple:sofa_11',
    'swan_town_apple:sofa_12',
    'swan_town_apple:sofa_13',
    'swan_town_apple:sofa_14',
    'swan_town_apple:sofa_21',
    'swan_town_apple:stool_11',
    'swan_town_apple:stool_12',
    'swan_town_apple:stool_13',
    'swan_town_apple:stool_14',
    # 青苹果系列
    'swan_town_apple:chair_11_green',
    'swan_town_apple:chair_12_green',
    'swan_town_apple:chair_13_green',
    'swan_town_apple:chair_14_green',
    'swan_town_apple:sofa_11_green',
    'swan_town_apple:sofa_12_green',
    'swan_town_apple:sofa_13_green',
    'swan_town_apple:sofa_14_green',
    'swan_town_apple:sofa_21_green',
    'swan_town_apple:stool_11_green',
    'swan_town_apple:stool_12_green',
    'swan_town_apple:stool_13_green',
    'swan_town_apple:stool_14_green',
]

# 坐下动画名称
SIT_ANIMATION_NAME = "animation.sit_chair"

# 座位高度偏移
SEAT_HEIGHT = 0.5

# ============================================================
# 床功能配置
# ============================================================

# 床方块列表
BED_BLOCKS = ['swan_town:bed', 'swan_town:bed_single', 'swan_town_apple:bed_11', 'swan_town_apple:bed_12', 'swan_town_apple:bed_11_green', 'swan_town_apple:bed_12_green']

# 双人床列表（2格宽）
DOUBLE_BEDS = ['swan_town:bed', 'swan_town_apple:bed_11', 'swan_town_apple:bed_11_green']

# 单人床列表
SINGLE_BEDS = ['swan_town:bed_single', 'swan_town_apple:bed_12', 'swan_town_apple:bed_12_green']

# 向后兼容
DOUBLE_BED = 'swan_town:bed'
SINGLE_BED = 'swan_town:bed_single'

# 维度ID
DIMENSION_OVERWORLD = 0
DIMENSION_NETHER = 1
DIMENSION_END = 2

# 敌对生物类型列表（用于检测）
HOSTILE_MOBS = [
    'minecraft:zombie',
    'minecraft:skeleton',
    'minecraft:creeper',
    'minecraft:spider',
    'minecraft:enderman',
    'minecraft:witch',
    'minecraft:husk',
    'minecraft:stray',
    'minecraft:drowned',
    'minecraft:phantom',
    'minecraft:slime',
    'minecraft:ghast',
    'minecraft:magma_cube',
    'minecraft:blaze',
    'minecraft:piglin',
    'minecraft:piglin_brute',
    'minecraft:hoglin',
    'minecraft:zoglin',
    'minecraft:zombified_piglin',
    'minecraft:wither_skeleton',
]

# 夜晚开始时间（12500 = 18:45）
NIGHT_START_TIME = 12500

# 睡觉传送高度偏移
SLEEP_HEIGHT_OFFSET = 0.8

# 怪物检测范围（格）
MONSTER_CHECK_RADIUS = 8

# 床上方需要空旷的格数
BED_CLEARANCE_HEIGHT = 2

# ============================================================
# 水桶交互配置
# ============================================================

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

    # 请在此处添加更多配置...
    # 示例：
    # 'swan_town_apple:bathtub_11_empty': {
    #     'enable_fill': True,
    #     'enable_empty': True,
    #     'fill_replace': 'swan_town_apple:bathtub_11',
    #     'empty_replace': 'swan_town_apple:bathtub_11_empty',
    # },
}

# 桶交互冷却时间（秒）
BUCKET_INTERACT_COOLDOWN = 0.3

# ============================================================
# 空手交互配置
# ============================================================

# 空手点击方块循环映射配置（与斧子分开）
HAND_BLOCK_CYCLES = {
    'light': {
        'swan_town:light1': 'swan_town:light1_off',
        'swan_town:light1_off': 'swan_town:light1',
        'swan_town:light2': 'swan_town:light2_off',
        'swan_town:light2_off': 'swan_town:light2',
        'swan_town:light3': 'swan_town:light3_off',
        'swan_town:light3_off': 'swan_town:light3',
    },
    # 重置版配置
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
    'computer1':{
        'swan_town_apple:computer_22':'swan_town_apple:computer_21',
        'swan_town_apple:computer_21':'swan_town_apple:computer_22',
    },
    'computer2':{
        'swan_town_apple:computer_12':'swan_town_apple:computer_11',
        'swan_town_apple:computer_11':'swan_town_apple:computer_12',
    },
    'tv1':{
        'swan_town_apple:tv_11':'swan_town_apple:tv_12',
        'swan_town_apple:tv_12':'swan_town_apple:tv_11',
    },
    'tv2':{
        'swan_town_apple:tv_21':'swan_town_apple:tv_22',
        'swan_town_apple:tv_22':'swan_town_apple:tv_21',
    },
    'sink1':{
        'swan_town_apple:sink_12_1':'swan_town_apple:sink_12'
    },
    'sink2':{
        'swan_town_apple:sink_13':'swan_town_apple:sink_11'
    },
    'bathtub1':{
        'swan_town_apple:bathtub_13':'swan_town_apple:bathtub_11'
    },
    'bathtub2':{
        'swan_town_apple:bathtub_23':'swan_town_apple:bathtub_21'
    },
    'shower':{
        'swan_town_apple:shower_133':'swan_town_apple:shower_13'
    },
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

# 合并所有空手方块循环映射
ALL_HAND_BLOCK_CYCLES = {}
for cycle_dict in HAND_BLOCK_CYCLES.values():
    ALL_HAND_BLOCK_CYCLES.update(cycle_dict)

# 空手交互冷却时间（秒）
HAND_INTERACT_COOLDOWN = 0.2

# ============================================================
# 占位方块配置
# ============================================================

# 占位方块类型定义
# 格式: {类型名: 方块标识符}
PLACEHOLDER_TYPES = {
    'default': 'swan_town:placeholder',
    'half': 'swan_town:placeholder_half',
    '75':'swan_town:placeholder_75',
    # 添加更多类型:
    # 'large': 'swan_town:placeholder_large',
}

# 默认占位方块类型
PLACEHOLDER_DEFAULT_TYPE = 'default'

# 家具占位配置
# 格式: {家具方块名: {'type': 类型名, 'offsets': [(相对x, 相对y, 相对z), ...]}}
# 相对位置基于家具方块的 aux 值（朝向）自动转换
# aux: 0=北(-Z), 1=东(+X), 2=南(+Z), 3=西(-X)
# 示例:
#   'swan_town:wardrobe': {
#       'type': 'default',
#       'offsets': [(0, 0, 1), (0, 0, 2)]
#   }
PLACEHOLDER_CONFIG = {
    # 在此添加需要占位的家具配置
    'swan_town:bed': {
        'type': 'half',
        'offsets': [(-1,0,0),(-1,0,-1),(-1,0,-2),(0,0,-1),(0,0,-2)]
    },
    'swan_town:bed_single':{
        'type': 'half',
        'offsets': [(0,0,-1)]
    },
    'swan_town:dressing_table1':{
        'type': 'default',
        'offsets': [(-1,0,0),(-2,0,0)]
    },
    'swan_town:dressing_table2':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town:wardrobe':{
        'type': 'default',
        'offsets': [(-1,0,0),(-1,1,0,),(-1,2,0),(0,1,0),(0,2,0)]
    },
    'swan_town:desk1':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town:desk2':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town:desk3':{
        'type': 'default',
        'offsets': [(-1,0,0),(-2,0,0)]
    },
    'swan_town:closet2':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town:bathtub1':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town:bathtub2':{
        'type': 'default',
        'offsets': [(-1,0,0),(-1,0,-1),(-2,0,0),(-2,0,-1),(0,0,-1)]
    },
    'swan_town:shelf1':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town:shelf2':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    # 重置版家具
    'swan_town_apple:cabinet_11':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:cabinet_12':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:cabinet_13':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:cabinet_14':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },

    'swan_town_apple:desk_11':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:desk_12':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:desk_13':{
        'type':'default',
        'offsets':[(-1,0,0),(-2,0,0)]
    },
    'swan_town_apple:desk_14':{
        'type':'default',
        'offsets':[(-1,0,0),(-2,0,0)]
    },

    'swan_town_apple:bathtub_11':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:bathtub_12':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:bathtub_13':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:bathtub_21':{
        'type': 'default',
        'offsets': [(-1,0,0),(-1,0,-1),(-2,0,0),(-2,0,-1),(0,0,-1)]
    },
    'swan_town_apple:bathtub_22':{
        'type': 'default',
        'offsets': [(-1,0,0),(-1,0,-1),(-2,0,0),(-2,0,-1),(0,0,-1)]
    },
    'swan_town_apple:bathtub_23':{
        'type': 'default',
        'offsets': [(-1,0,0),(-1,0,-1),(-2,0,0),(-2,0,-1),(0,0,-1)]
    },

    'swan_town_apple:refrigerator_11':{
        'type': 'default',
        'offsets': [(0,1,0),(0,2,0),(-1,0,0),(-1,1,0),(-1,2,0)]
    },
    'swan_town_apple:refrigerator_12':{
        'type': 'default',
        'offsets': [(0,1,0),(0,2,0)]
    },

    'swan_town_apple:wardrobe_11':{
        'type': 'default',
        'offsets': [(0,1,0),(0,2,0),(-1,0,0),(-1,1,0),(-1,2,0)]
    },
    'swan_town_apple:wardrobe_12':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:wardrobe_13':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },

    'swan_town_apple:table_51':{
        'type': 'default',
        'offsets': [(-2,0,0)]
    },

    'swan_town_apple:bed_12':{
        'type': '75',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:bed_11':{
        'type': '75',
        'offsets': [(-1,0,0),(-2,0,0),(-1,0,-1),(-2,0,-1),]
    },
    # 青苹果系列
    'swan_town_apple:bed_11_green':{
        'type': '75',
        'offsets': [(-1,0,0),(-2,0,0),(-1,0,-1),(-2,0,-1),]
    },
    'swan_town_apple:bed_12_green':{
        'type': '75',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:cabinet_11_green':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:cabinet_12_green':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:cabinet_13_green':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:cabinet_14_green':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:desk_11_green':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:desk_12_green':{
        'type':'default',
        'offsets':[(-1,0,0)]
    },
    'swan_town_apple:desk_13_green':{
        'type':'default',
        'offsets':[(-1,0,0),(-2,0,0)]
    },
    'swan_town_apple:desk_14_green':{
        'type':'default',
        'offsets':[(-1,0,0),(-2,0,0)]
    },
    'swan_town_apple:refrigerator_11_green':{
        'type': 'default',
        'offsets': [(0,1,0),(0,2,0),(-1,0,0),(-1,1,0),(-1,2,0)]
    },
    'swan_town_apple:refrigerator_12_green':{
        'type': 'default',
        'offsets': [(0,1,0),(0,2,0)]
    },
    'swan_town_apple:wardrobe_11_green':{
        'type': 'default',
        'offsets': [(0,1,0),(0,2,0),(-1,0,0),(-1,1,0),(-1,2,0)]
    },
    'swan_town_apple:wardrobe_12_green':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:wardrobe_13_green':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:table_51_green':{
        'type': 'default',
        'offsets': [(-2,0,0)]
    },
    'swan_town_apple:bathtub_11_green':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:bathtub_12_green':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:bathtub_13_green':{
        'type': 'default',
        'offsets': [(-1,0,0)]
    },
    'swan_town_apple:bathtub_21_green':{
        'type': 'default',
        'offsets': [(-1,0,0),(-1,0,-1),(-2,0,0),(-2,0,-1),(0,0,-1)]
    },
    'swan_town_apple:bathtub_22_green':{
        'type': 'default',
        'offsets': [(-1,0,0),(-1,0,-1),(-2,0,0),(-2,0,-1),(0,0,-1)]
    },
    'swan_town_apple:bathtub_23_green':{
        'type': 'default',
        'offsets': [(-1,0,0),(-1,0,-1),(-2,0,0),(-2,0,-1),(0,0,-1)]
    },
}

# 所有需要占位的家具集合（自动生成）
PLACEHOLDER_FURNITURES = set(PLACEHOLDER_CONFIG.keys())

# 所有占位方块标识符集合（自动生成）
ALL_PLACEHOLDER_BLOCKS = set(PLACEHOLDER_TYPES.values())

# ============================================================
# 排水功能配置
# ============================================================

# 排水方块映射配置
# 格式: {原方块: (放水中方块, 放水完成方块)}
# 示例: 'swan_town_apple:bathtub_11': ('swan_town_apple:bathtub_11_draining', 'swan_town_apple:bathtub_11_empty')
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

# 排水动画持续时间（秒）
DRAINAGE_DURATION = 0.5

# 排水功能冷却时间（秒）
DRAINAGE_COOLDOWN = 1.0
