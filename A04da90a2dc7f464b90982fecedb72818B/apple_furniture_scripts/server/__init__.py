# -*- coding: utf-8 -*-
"""
服务端功能模块包

包含所有服务端游戏逻辑模块：
- interact_axe: 斧子交互（切换家具样式）
- interact_seat: 座椅交互（椅子/沙发坐下站起）
- interact_bed: 床交互（睡觉功能，含双人床同步）
- interact_hand: 空手交互（循环切换方块样式）
- interact_water: 水桶交互（水池交互）
- interact_drainage: 排水交互（水槽/浴缸排水）
- placeholder: 占位方块管理（多格家具碰撞）

模块在导入时自动注册事件监听，无需手动初始化。
"""
