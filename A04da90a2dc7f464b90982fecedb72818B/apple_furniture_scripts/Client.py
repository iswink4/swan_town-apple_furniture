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

# ============================================================
# 睡觉功能客户端
# ============================================================

# 睡觉状态
_is_sleeping = False
_original_camera_locked = False

def set_sleep_blur():
    """
    设置睡觉模糊效果（使用原版睡觉效果）
    通过设置玩家的视野距离来模拟黑屏
    """
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    
    # 使用雾效创建一个近处的"墙"来实现黑屏效果
    # 设置雾的起始距离为0，结束距离为0.1，这样所有物体都会被雾遮挡
    fog_comp = comp.CreateFog(playerId)
    fog_comp.SetFogColor((0.05, 0.05, 0.05, 1.0))  # 深灰色，不是纯黑
    fog_comp.SetFogLength(0.0, 0.5)  # 很近的雾

def restore_normal_view():
    """
    恢复正常视野
    """
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    
    # 重置雾效
    fog_comp = comp.CreateFog(playerId)
    fog_comp.ResetFogColor()
    fog_comp.ResetFogLength()

def lock_view_to_sky():
    """
    锁定视角朝向天空
    """
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    camera_comp = comp.CreateCamera(playerId)
    
    # 获取当前相机位置
    current_pos = camera_comp.GetPosition()
    
    # 设置相机朝向天空 (pitch=-90 朝天, yaw=0)
    # 注意：在MC中，-90是垂直向上看
    camera_comp.SetCameraRot((-90.0, 0.0))
    
    # 使用 LockCamera 全面锁定相机
    # LockCamera(pos, rot) - pos是位置（不移动），rot是角度
    camera_comp.LockCamera(current_pos, (-90.0, 0.0))

def unlock_view():
    """
    解除视角锁定
    """
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    camera_comp = comp.CreateCamera(playerId)
    
    # 解除相机锁定
    camera_comp.UnLockCamera()

@CallBackKey("StartSleep")
def StartSleep():
    """
    开始睡觉
    由服务端通过 Call(playerId, "StartSleep") 调用
    """
    global _is_sleeping
    _is_sleeping = True
    
    # 注册资源（复用坐下动画）
    RegisterSitResources()
    
    # 播放睡觉动画（复用坐下动画）
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    query_comp = comp.CreateQueryVariable(playerId)
    query_comp.Set("query.mod.sitting", 1.0)
    
    # 黑屏效果
    set_sleep_blur()
    
    # 锁定视角朝向天空
    lock_view_to_sky()

@CallBackKey("StopSleep")
def StopSleep():
    """
    停止睡觉
    由服务端通过 Call(playerId, "StopSleep") 调用
    """
    global _is_sleeping
    _is_sleeping = False
    
    # 停止动画
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    query_comp = comp.CreateQueryVariable(playerId)
    query_comp.Set("query.mod.sitting", 0.0)
    
    # 恢复视野
    restore_normal_view()
    
    # 解除视角锁定
    unlock_view()
