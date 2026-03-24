# -*- coding: utf-8 -*-
"""
家具模组服务端入口

此模块作为服务端功能的入口点，导入所有子模块。
子模块在导入时自动注册事件监听，无需手动初始化。

包含的模块：
- server.interact_block: 方块交互（斧子切换家具样式）
- server.interact_seat: 座椅交互（椅子/沙发坐下站起）
- server.interact_bed: 床交互（睡觉功能，含双人床同步）
- server.interact_water: 水桶交互（空桶装水、水桶倒水）

使用方法:
    在服务端脚本中导入此模块即可启用所有功能：
    from apple_furniture_scripts import Server

注意:
    模块导入时会自动执行事件注册，无需额外调用。
"""
from .server import interact_block
from .server import interact_seat
from .server import interact_bed
from .server import interact_water
