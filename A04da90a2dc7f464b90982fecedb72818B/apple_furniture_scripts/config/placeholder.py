# -*- coding: utf-8 -*-
"""
占位方块配置
定义大型家具的多格碰撞箱配置
"""

# ============================================================
# 占位方块类型定义
# ============================================================

# 占位方块类型定义
# 格式: {类型名: 方块标识符}
PLACEHOLDER_TYPES = {
    'default': 'swan_town:placeholder',
    'half': 'swan_town:placeholder_half',
    '75': 'swan_town:placeholder_75',
}

# 默认占位方块类型
PLACEHOLDER_DEFAULT_TYPE = 'default'

# 所有占位方块标识符集合（自动生成）
ALL_PLACEHOLDER_BLOCKS = set(PLACEHOLDER_TYPES.values())

# ============================================================
# 家具占位配置
# ============================================================

# 家具占位配置
# 格式: {家具方块名: {'type': 类型名, 'offsets': [(相对x, 相对y, 相对z), ...]}}
# 相对位置基于家具方块的 aux 值（朝向）自动转换
# aux: 0=北(-Z), 1=东(+X), 2=南(+Z), 3=西(-X)
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
        'offsets': [(-1,0,0),(-2,0,0),(-1,0,-1),(-2,0,-1),(0,0,-1)]
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