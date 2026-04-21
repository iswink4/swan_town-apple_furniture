# -*- coding: utf-8 -*-
"""
家具模组服务端入口

此模块作为服务端功能的入口点，导入所有子模块。
子模块在导入时自动注册事件监听，无需手动初始化。

包含的模块：
- server.interact_axe: 斧子交互（斧子切换家具样式）
- server.interact_hand: 空手交互（空手切换方块样式）
- server.interact_seat: 座椅交互（椅子/沙发坐下站起）
- server.interact_bed: 床交互（睡觉功能，含双人床同步）
- server.interact_water: 水桶交互（空桶装水、水桶倒水）
- server.interact_drainage: 放水交互
- server.interact_ice: 冰箱制冰（水桶点击冰箱生成冰块）
- server.placeholder: 占位方块系统（大型家具多格碰撞箱）

使用方法:
    在服务端脚本中导入此模块即可启用所有功能：
    from apple_furniture_scripts import Server

事件优先级与模块导入顺序:
========================================

【重要】模块导入顺序影响事件触发顺序，请勿随意调整！

ServerItemUseOnEvent 处理顺序（必须严格按此顺序导入）:
  1. interact_ice（冰箱制冰）
     - 最高优先级，需要先取消放水行为
     - 如果顺序错误，点击冰箱占位方块时会先触发放水
  2. interact_water（水桶放水）
     - 检查 args['ret'] 是否已被设置，避免重复处理

ServerBlockUseEvent 处理顺序:
  1. placeholder（占位方块交互转发）
     - 处理占位方块的交互转发逻辑
  2. interact_hand（空手循环切换）
     - 空手点击方块的样式切换
  3. interact_water（空桶装水）
     - 空桶点击水槽装水
  4. interact_drainage（排水功能）
     - 空手点击浴缸/水槽排水

ItemUseOnAfterServerEvent 处理顺序:
  1. interact_axe（斧子样式切换）
  2. placeholder（斧子交互转发）

注意事项:
- 模块导入时会自动执行事件注册，无需额外调用
- config 模块已拆分为 config/ 文件夹，向后兼容
- utils 模块提供公共工具函数（cooldown_check, cycle_block 等）
"""

# ============================================================
# 模块导入（顺序敏感，请勿随意调整）
# ============================================================

# ServerItemUseOnEvent：interact_ice 必须在 interact_water 之前
from .server import interact_ice
from .server import interact_water

# ServerBlockUseEvent：placeholder 优先处理占位方块
from .server import placeholder
from .server import interact_hand
from .server import interact_drainage

# 其他模块（顺序不敏感）
from .server import interact_axe
from .server import interact_seat
from .server import interact_bed
