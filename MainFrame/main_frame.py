# -*- coding: utf-8 -*-

import time
import os
import wx
import wx.adv as adv
import wx.aui as aui


class MainFrame(wx.Frame):
    """ 创建程序主框架 """

    def __init__(self, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        # 设置界面
        self.InitUI()

    def InitUI(self):
        """ 初始化主界面 """

        # 设置软件打开画面
        midis = os.getcwd() + '\\icon\\MIDIS.jpg'
        bmp = wx.Image(midis).ConvertToBitmap()
        adv.SplashScreen(bitmap=bmp, splashStyle=adv.SPLASH_CENTER_ON_SCREEN | adv.SPLASH_TIMEOUT,
                         milliseconds=1000, parent=None, id=-1)
        wx.Yield()

        time.sleep(1)
        # 设置主界面左上角图标
        icon = os.getcwd() + '\\icon\\MIDIS.ico'
        icon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        icon.SetHeight(18)
        icon.SetWidth(18)
        self.SetIcon(icon)
        # 设置主界面标题
        self.SetTitle(title='')
        # 设置主界面风格
        self.SetWindowStyle(style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER | wx.CLIP_CHILDREN)
        # 设置主界面大小
        c_x, c_y, c_w, c_h = wx.ClientDisplayRect()
        self.SetSize(wx.Size(c_w,c_h))
        # 设置主界面居中
        self.Centre()

        # 创建窗口的管理器
        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self)

        # 创建菜单栏
        self.mb = wx.MenuBar()
        self.SetMenuBar(self.mb)

        # 创建工具栏
        self.tb = wx.ToolBar(self, style=wx.TB_HORIZONTAL | wx.TB_NODIVIDER | wx.TB_FLAT)

        # 创建状态栏
        self.stausbar = self.CreateStatusBar(1, wx.STB_DEFAULT_STYLE)
        self.stausbar.SetStatusText("准备")

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def update(self):
        """ 刷新界面 """
        self.mgr.Update()

    def get_mgr(self):
        """ 获得管理器 """
        return self.mgr

    def get_menu_bar(self):
        """ 获得菜单栏 """
        return self.mb

    def get_tool_bar(self):
        """ 获得工具栏 """
        return self.tb

    def get_staus_bar(self):
        """ 获得状态栏 """
        return self.stausbar

    def OnClose(self, event):
        """ 管理器与托管窗口分离，销毁管理器，关闭主界面 """
        self.mgr.UnInit()
        del self.mgr
        self.Destroy()


def main():
    app = wx.App()
    frame = MainFrame(parent=None)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()

