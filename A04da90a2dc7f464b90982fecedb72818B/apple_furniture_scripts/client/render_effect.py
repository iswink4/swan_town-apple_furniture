# -*- coding: utf-8 -*-
"""
模块名称: render_effect.py
功能描述: 处理睡觉效果的渲染，包括黑屏和视角锁定

服务端调用:
- StartSleep: 开始睡觉（黑屏 + 锁定视角朝天）
- StopSleep: 停止睡觉（恢复视野 + 解除锁定）

外部依赖:
- QuModLibs.Client: 客户端基础API（clientApi, CallBackKey等）
- render_anim: 复用坐下动画系统

全局状态:
- _is_sleeping: bool - 是否正在睡觉

实现逻辑:
1. StartSleep 被服务端调用时：
   - 设置 _is_sleeping = True
   - 注册并播放坐下动画（复用 render_anim）
   - 设置雾效实现黑屏（近处灰雾遮挡视野）
   - 锁定相机朝向天空（pitch=-90, yaw=0）

2. StopSleep 被服务端调用时：
   - 设置 _is_sleeping = False
   - 停止坐下动画
   - 重置雾效恢复正常视野
   - 解除相机锁定

视觉效果说明:
- 黑屏效果：使用雾效在玩家面前创建一堵"墙"
  - 雾颜色：深灰色 (0.05, 0.05, 0.05, 1.0)
  - 雾范围：0.0 ~ 0.5（很近的距离）
- 视角锁定：强制相机朝向天空（pitch=-90表示垂直向上）

注意事项:
- 睡觉效果复用坐下动画（节省资源）
- 视角锁定使用 LockCamera，全面锁定相机位置和角度
- 起床时必须同时恢复雾效和解除锁定
"""
from ..QuModLibs.Client import *
from .render_anim import RegisterSitResources


# ============================================================
# 全局状态
# ============================================================

# 是否正在睡觉
_is_sleeping = False


# ============================================================
# 视觉效果控制
# ============================================================

def set_sleep_blur():
    """
    设置睡觉模糊效果（黑屏）
    
    使用雾效创建一个近处的"墙"来实现黑屏效果。
    设置雾的起始距离为0，结束距离为0.5，这样所有物体都会被雾遮挡。
    
    Args:
        无
    
    Returns:
        None
    
    Side Effects:
        - 修改雾颜色为深灰色
        - 修改雾范围为 0.0 ~ 0.5
    
    Note:
        使用深灰色而非纯黑，避免完全失明的感觉
    """
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    
    # 使用雾效创建一个近处的"墙"来实现黑屏效果
    # 设置雾的起始距离为0，结束距离为0.5，这样所有物体都会被雾遮挡
    fog_comp = comp.CreateFog(playerId)
    fog_comp.SetFogColor((0.05, 0.05, 0.05, 1.0))  # 深灰色，不是纯黑
    fog_comp.SetFogLength(0.0, 0.5)  # 很近的雾


def restore_normal_view():
    """
    恢复正常视野
    
    重置雾效到默认状态，恢复玩家的正常视野。
    
    Args:
        无
    
    Returns:
        None
    
    Side Effects:
        - 重置雾颜色为默认值
        - 重置雾范围为默认值
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
    
    获取当前相机位置，然后锁定相机朝向天空。
    在MC中，pitch=-90 表示垂直向上看（朝向天空）。
    
    Args:
        无
    
    Returns:
        None
    
    Side Effects:
        - 设置相机旋转角度为 (-90.0, 0.0)
        - 锁定相机位置和角度
    
    Note:
        使用 LockCamera 全面锁定相机，玩家无法移动视角
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
    
    解除相机的锁定状态，玩家可以自由移动视角。
    
    Args:
        无
    
    Returns:
        None
    
    Side Effects:
        - 调用 UnLockCamera 解除锁定
    """
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    camera_comp = comp.CreateCamera(playerId)
    
    # 解除相机锁定
    camera_comp.UnLockCamera()


# ============================================================
# 服务端调用的API
# ============================================================

@CallBackKey("StartSleep")
def StartSleep():
    """
    开始睡觉
    
    由服务端通过 Call(playerId, "StartSleep") 调用。
    触发睡觉效果：播放坐下动画、黑屏、锁定视角朝天。
    
    Args:
        无（服务端调用，无参数）
    
    Returns:
        None
    
    Side Effects:
        - 设置 _is_sleeping = True
        - 注册并播放坐下动画（复用 render_anim）
        - 设置雾效实现黑屏
        - 锁定相机朝向天空
    
    Note:
        睡觉动画复用坐下动画（query.mod.sitting = 1.0）
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
    
    由服务端通过 Call(playerId, "StopSleep") 调用。
    结束睡觉效果：停止动画、恢复视野、解除视角锁定。
    
    Args:
        无（服务端调用，无参数）
    
    Returns:
        None
    
    Side Effects:
        - 设置 _is_sleeping = False
        - 停止坐下动画
        - 重置雾效恢复正常视野
        - 解除相机锁定
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
