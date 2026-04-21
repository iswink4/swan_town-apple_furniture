# -*- coding: utf-8 -*-
"""
家具功能配置
定义座椅、床、容器等家具的功能配置
"""

# ============================================================
# 座椅配置
# ============================================================

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

# ============================================================
# 床配置
# ============================================================

# 床方块列表
BED_BLOCKS = [
    'swan_town:bed', 
    'swan_town:bed_single', 
    'swan_town_apple:bed_11', 
    'swan_town_apple:bed_12', 
    'swan_town_apple:bed_11_green', 
    'swan_town_apple:bed_12_green'
]

# 双人床列表（2格宽）
DOUBLE_BEDS = [
    'swan_town:bed', 
    'swan_town_apple:bed_11', 
    'swan_town_apple:bed_11_green'
]

# 单人床列表
SINGLE_BEDS = [
    'swan_town:bed_single', 
    'swan_town_apple:bed_12', 
    'swan_town_apple:bed_12_green'
]

# 向后兼容（废弃，建议使用 DOUBLE_BEDS/SINGLE_BEDS）
DOUBLE_BED = 'swan_town:bed'
SINGLE_BED = 'swan_town:bed_single'

# ============================================================
# 容器配置
# ============================================================

# 冰箱容器列表（点击占位方块时打开容器）
REFRIGERATOR_CONTAINERS = {
    'swan_town_apple:refrigerator_11',
    'swan_town_apple:refrigerator_11_green',
    'swan_town_apple:refrigerator_12',
    'swan_town_apple:refrigerator_12_green',
}

# 衣柜容器列表（点击占位方块时打开容器）
WARDROBE_CONTAINERS = {
    'swan_town_apple:wardrobe_11',
    'swan_town_apple:wardrobe_11_green',
    'swan_town_apple:wardrobe_12',
    'swan_town_apple:wardrobe_12_green',
    'swan_town_apple:wardrobe_13',
    'swan_town_apple:wardrobe_13_green',
}