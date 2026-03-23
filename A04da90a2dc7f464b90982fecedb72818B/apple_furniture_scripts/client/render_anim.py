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
- _res_registered: bool - 动画资源是否已注册（防止重复注册）

实现逻辑:
1. 本地玩家加载完成时自动调用 RegisterSitResources 预注册资源
2. RegisterSitResources 注册 Query 变量、动画、动画控制器
3. PlaySitAnim 被服务端调用时，设置 query.mod.sitting = 1.0 播放动画
4. StopSitAnim 被服务端调用时，设置 query.mod.sitting = 0.0 停止动画

动画系统说明:
- Query 变量 query.mod.sitting 控制动画状态（0.0=站立，1.0=坐下）
- 动画控制器 controller.animation.player.sit_chair 根据 Query 变量切换动画
- 动画资源在首次坐下前预注册，避免首次播放时的延迟

注意事项:
- 资源只需注册一次，使用 _res_registered 标志防止重复
- RebuildPlayerRender 必须调用才能使资源生效
- 该动画系统也用于睡觉功能（复用坐下动画）
"""
from ..QuModLibs.Client import *
from ..config import SIT_ANIMATION_NAME


# ============================================================
# 全局状态
# ============================================================

# 动画资源是否已注册（防止重复注册）
_res_registered = False


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
    RegisterSitResources()


def RegisterSitResources():
    """
    注册坐下动画资源到玩家实体
    
    注册内容包括：
    1. Query 变量 query.mod.sitting - 控制动画状态
    2. 坐下动画 animation.sit_chair
    3. 动画控制器 controller.animation.player.sit_chair
    4. ScriptAnimate 绑定 - 将控制器绑定到 Query 变量
    
    Args:
        无
    
    Returns:
        None
    
    Side Effects:
        - 设置 _res_registered = True
        - 调用 RebuildPlayerRender 重建玩家渲染器
    
    Note:
        如果 _res_registered 已为 True，直接返回不重复注册
    """
    global _res_registered
    if _res_registered:
        return
    
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    
    # 获取渲染组件和Query变量组件
    render_comp = comp.CreateActorRender(playerId)
    query_comp = comp.CreateQueryVariable(playerId)
    
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
    
    _res_registered = True


# ============================================================
# 服务端调用的API
# ============================================================

@CallBackKey("PlaySitAnim")
def PlaySitAnim():
    """
    播放坐下动画
    
    由服务端通过 Call(playerId, "PlaySitAnim") 调用。
    设置 Query 变量 query.mod.sitting = 1.0，触发坐下动画播放。
    
    Args:
        无（服务端调用，无参数）
    
    Returns:
        None
    
    Side Effects:
        - 调用 RegisterSitResources 确保资源已注册
        - 设置 Query 变量触发动画
    
    Note:
        该函数也用于睡觉功能（复用坐下动画）
    """
    RegisterSitResources()
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
    comp.Set("query.mod.sitting", 1.0)


@CallBackKey("StopSitAnim")
def StopSitAnim():
    """
    停止坐下动画
    
    由服务端通过 Call(playerId, "StopSitAnim") 调用。
    设置 Query 变量 query.mod.sitting = 0.0，停止坐下动画。
    
    Args:
        无（服务端调用，无参数）
    
    Returns:
        None
    
    Side Effects:
        - 设置 Query 变量停止动画
    
    Note:
        该函数也用于睡觉功能（复用坐下动画）
    """
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
    comp.Set("query.mod.sitting", 0.0)
