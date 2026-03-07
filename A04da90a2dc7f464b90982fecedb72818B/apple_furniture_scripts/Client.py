# -*- coding: utf-8 -*-
"""
家具模组客户端逻辑
功能：
1. 注册坐下动画资源
2. 响应服务端调用播放/停止动画
"""
from .QuModLibs.Client import *
from .config import SIT_ANIMATION_NAME

# ============================================================
# 全局状态
# ============================================================

# 动画资源是否已注册
_res_registered = False

# ============================================================
# 动画资源注册
# ============================================================

@Listen(Events.OnLocalPlayerStopLoading)
def OnLocalPlayerLoad(args):
    """
    本地玩家加载完成时预注册动画资源
    避免首次坐下时动画不播放的问题
    """
    RegisterSitResources()

def RegisterSitResources():
    """
    注册坐下动画资源到玩家实体
    包括：动画、动画控制器、Query变量、ScriptAnimate节点
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
    由服务端通过 Call(playerId, "PlaySitAnim") 调用
    """
    RegisterSitResources()
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
    comp.Set("query.mod.sitting", 1.0)

@CallBackKey("StopSitAnim")
def StopSitAnim():
    """
    停止坐下动画
    由服务端通过 Call(playerId, "StopSitAnim") 调用
    """
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
    comp.Set("query.mod.sitting", 0.0)