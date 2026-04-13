# -*- coding: utf-8 -*-
"""
模块名称: render_anim.py
功能描述: 处理坐下动画的注册和播放控制

事件监听:
- OnLocalPlayerStopLoading: 本地玩家加载完成时触发，预注册动画资源

服务端调用:
- PlaySitAnim: 播放坐下动画
- StopSitAnim: 停止坐下动画

外部依赖:
- QuModLibs.Client: 客户端基础API（clientApi, Events, Listen, CallBackKey等）
- config: SIT_ANIMATION_NAME（坐下动画名称）

全局状态:
- _registered_players: set - 已注册动画资源的玩家ID集合（防止重复注册）

实现逻辑:
1. 本地玩家加载完成时自动调用 RegisterSitResources 预注册本地玩家资源
2. RegisterSitResources 注册 Query 变量、动画、动画控制器到指定玩家实体
3. PlaySitAnim 被服务端调用时，为指定玩家设置 query.mod.sitting = 1.0 播放动画
4. StopSitAnim 被服务端调用时，为指定玩家设置 query.mod.sitting = 0.0 停止动画

动画系统说明:
- Query 变量 query.mod.sitting 控制动画状态（0.0=站立，1.0=坐下）
- 动画控制器 controller.animation.player.sit_chair 根据 Query 变量切换动画
- 动画资源在首次坐下前预注册，避免首次播放时的延迟
- 服务端通过 Call("*", "PlaySitAnim", targetPlayerId) 广播给所有客户端

注意事项:
- 每个玩家需要独立注册动画资源，使用 _registered_players 集合防止重复
- RebuildPlayerRender 必须调用才能使资源生效
- 该动画系统也用于睡觉功能（复用坐下动画）
"""
from ..QuModLibs.Client import *
from ..config import SIT_ANIMATION_NAME


# ============================================================
# 全局状态
# ============================================================

# 已注册动画资源的玩家ID集合（防止重复注册）
_registered_players = set()


# ============================================================
# 动画资源注册
# ============================================================

@Listen(Events.OnLocalPlayerStopLoading)
def OnLocalPlayerLoad(args):
    """
    本地玩家加载完成时预注册动画资源
    
    在玩家进入世界时自动调用，提前注册坐下动画资源，
    避免首次坐下时动画不播放的问题。
    
    Args:
        args: 事件参数字典（OnLocalPlayerStopLoading标准参数）
    
    Returns:
        None
    
    Note:
        此事件在玩家加载完成、可以操作角色时触发
    """
    RegisterSitResources(clientApi.GetLocalPlayerId())


def RegisterSitResources(target_player_id):
    """
    注册坐下动画资源到指定玩家实体
    
    注册内容包括：
    1. Query 变量 query.mod.sitting - 控制动画状态
    2. 坐下动画 animation.sit_chair
    3. 动画控制器 controller.animation.player.sit_chair
    4. ScriptAnimate 绑定 - 将控制器绑定到 Query 变量
    
    Args:
        target_player_id: str - 目标玩家实体ID
    
    Returns:
        None
    
    Side Effects:
        - 将 target_player_id 加入 _registered_players 集合
        - 调用 RebuildPlayerRender 重建玩家渲染器
    
    Note:
        如果 target_player_id 已在 _registered_players 中，直接返回不重复注册
    """
    if target_player_id in _registered_players:
        return
    
    comp = clientApi.GetEngineCompFactory()
    
    # 获取渲染组件和Query变量组件
    render_comp = comp.CreateActorRender(target_player_id)
    query_comp = comp.CreateQueryVariable(target_player_id)
    
    # 注册 Query 变量，用于控制动画状态
    query_comp.Register("query.mod.sitting", 0.0)
    
    # 添加坐下动画
    render_comp.AddPlayerAnimation("sit_chair", SIT_ANIMATION_NAME)
    
    # 添加动画控制器
    render_comp.AddPlayerAnimationController("sit_chair_ctrl", "controller.animation.player.sit_chair")
    
    # 将动画控制器绑定到 Query 变量
    render_comp.AddPlayerScriptAnimate("sit_chair_ctrl", "query.mod.sitting")
    
    # 重建玩家渲染器使资源生效
    render_comp.RebuildPlayerRender()
    
    _registered_players.add(target_player_id)


# ============================================================
# 服务端调用的API
# ============================================================

@CallBackKey("PlaySitAnim")
def PlaySitAnim(target_player_id):
    """
    播放指定玩家的坐下动画
    
    由服务端通过 Call("*", "PlaySitAnim", targetPlayerId) 广播调用。
    设置指定玩家的 Query 变量 query.mod.sitting = 1.0，触发坐下动画播放。
    
    Args:
        target_player_id: str - 目标玩家实体ID（由服务端传入）
    
    Returns:
        None
    
    Side Effects:
        - 调用 RegisterSitResources 确保资源已注册
        - 设置 Query 变量触发动画
    
    Note:
        该函数也用于睡觉功能（复用坐下动画）
    """
    RegisterSitResources(target_player_id)
    comp = clientApi.GetEngineCompFactory()
    query_comp = comp.CreateQueryVariable(target_player_id)
    query_comp.Set("query.mod.sitting", 1.0)


@CallBackKey("StopSitAnim")
def StopSitAnim(target_player_id):
    """
    停止指定玩家的坐下动画
    
    由服务端通过 Call("*", "StopSitAnim", targetPlayerId) 广播调用。
    设置指定玩家的 Query 变量 query.mod.sitting = 0.0，停止坐下动画。
    
    Args:
        target_player_id: str - 目标玩家实体ID（由服务端传入）
    
    Returns:
        None
    
    Side Effects:
        - 设置 Query 变量停止动画
    
    Note:
        该函数也用于睡觉功能（复用坐下动画）
    """
    if target_player_id not in _registered_players:
        return
    comp = clientApi.GetEngineCompFactory()
    query_comp = comp.CreateQueryVariable(target_player_id)
    query_comp.Set("query.mod.sitting", 0.0)
