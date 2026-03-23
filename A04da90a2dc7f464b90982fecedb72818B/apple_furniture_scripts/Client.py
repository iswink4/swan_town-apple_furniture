# -*- coding: utf-8 -*-
"""
家具模组客户端入口

此模块作为客户端功能的入口点，导入所有子模块。
子模块在导入时自动注册事件监听和API回调，无需手动初始化。

包含的模块：
- client.render_anim: 动画渲染（坐下动画注册与控制）
- client.render_effect: 效果渲染（睡觉黑屏和视角锁定）

使用方法:
    在客户端脚本中导入此模块即可启用所有功能：
    from apple_furniture_scripts import Client

注意:
    模块导入时会自动执行事件注册和API回调注册，无需额外调用。
"""
from .client import render_anim
from .client import render_effect
