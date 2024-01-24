from .panel_base import MPL_Panel_base
import wx.aui as aui


class PlotService:

    def __init__(self, parent):

        self.frame = parent

        self.MPL = MPL_Panel_base(self.frame)

        self.frame.get_mgr().AddPane(self.MPL, aui.AuiPaneInfo().Name('plot').Caption('显示区').BestSize((400, -1)).
                                     CaptionVisible(False).Right().Layer(0).Position(0))
        self.frame.update()