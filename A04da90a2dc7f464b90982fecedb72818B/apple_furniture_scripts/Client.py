# -*- coding: utf-8 -*-
from .QuModLibs.Client import *
from .config import SIT_ANIMATION_NAME

_res_registered = False

@Listen(Events.OnLocalPlayerStopLoading)
def OnLocalPlayerLoad(args):
    RegisterSitResources()

def RegisterSitResources():
    global _res_registered
    if _res_registered:
        return
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory()
    render_comp = comp.CreateActorRender(playerId)
    query_comp = comp.CreateQueryVariable(playerId)
    query_comp.Register("query.mod.sitting", 0.0)
    render_comp.AddPlayerAnimation("sit_chair", SIT_ANIMATION_NAME)
    render_comp.AddPlayerAnimationController("sit_chair_ctrl", "controller.animation.player.sit_chair")
    render_comp.AddPlayerScriptAnimate("sit_chair_ctrl", "query.mod.sitting")
    render_comp.RebuildPlayerRender()
    _res_registered = True

@CallBackKey("PlaySitAnim")
def PlaySitAnim():
    RegisterSitResources()
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
    comp.Set("query.mod.sitting", 1.0)

@CallBackKey("StopSitAnim")
def StopSitAnim():
    playerId = clientApi.GetLocalPlayerId()
    comp = clientApi.GetEngineCompFactory().CreateQueryVariable(playerId)
    comp.Set("query.mod.sitting", 0.0)

