# -*- coding: utf-8 -*-
"""
统一冷却机制模块
提供冷却检查函数，避免各模块重复实现冷却逻辑
"""

import time


_last_cooldown_times = {}


def cooldown_check(key, cooldown_time):
    """
    冷却检查函数
    
    Args:
        key: 冷却标识（通常是玩家ID，也可以是方块位置等）
        cooldown_time: 冷却时间（秒）
    
    Returns:
        bool: True=冷却已过可执行，False=冷却中跳过
    
    Example:
        if not cooldown_check(player_id, 0.3):
            return  # 冷却中，跳过
        # 执行逻辑...
    """
    now = time.time()
    last_time = _last_cooldown_times.get(key, 0)
    if now - last_time < cooldown_time:
        return False
    _last_cooldown_times[key] = now
    return True


def cooldown_remaining(key, cooldown_time):
    """
    获取剩余冷却时间
    
    Args:
        key: 冷却标识
        cooldown_time: 冷却时间（秒）
    
    Returns:
        float: 剩余冷却时间（秒），0表示冷却已过
    """
    now = time.time()
    last_time = _last_cooldown_times.get(key, 0)
    remaining = cooldown_time - (now - last_time)
    return max(0, remaining)


def reset_cooldown(key):
    """
    重置冷却时间
    
    Args:
        key: 冷却标识
    """
    if key in _last_cooldown_times:
        del _last_cooldown_times[key]