import wx


class ViewService:

    def __init__(self, app):
        self.frame = app.frame
        self.app = app
        self.project = app.project
        self.log = app.log
        self.plot = app.plot

        self.frame.get_menu_bar().Insert(1, self.add_view_menu(self.frame), '视图')
        self.log.Info('插件 view service 加载成功！')

        self.frame.update()

    def add_view_menu(self, parent):
        """ 视图 """
        view_menu = wx.Menu()

        self.view_toolbar = view_menu.Append(-1, '工具栏', kind=wx.ITEM_CHECK)
        self.view_stausbar = view_menu.Append(-1, '状态栏', kind=wx.ITEM_CHECK)
        self.view_project = view_menu.Append(-1, '工程', kind=wx.ITEM_CHECK)
        self.view_log = view_menu.Append(-1, '信息', kind=wx.ITEM_CHECK)
        self.view_plot = view_menu.Append(-1, '显示区', kind=wx.ITEM_CHECK)

        view_menu.Check(self.view_toolbar.GetId(), True)
        view_menu.Check(self.view_stausbar.GetId(), True)
        view_menu.Check(self.view_project.GetId(), True)
        view_menu.Check(self.view_log.GetId(), True)
        view_menu.Check(self.view_plot.GetId(), True)

        parent.Bind(wx.EVT_MENU, self.OnViewToolbar, self.view_toolbar)
        parent.Bind(wx.EVT_MENU, self.OnViewStausbar, self.view_stausbar)
        parent.Bind(wx.EVT_MENU, self.OnViewProject, self.view_project)
        parent.Bind(wx.EVT_MENU, self.OnViewLog, self.view_log)
        parent.Bind(wx.EVT_MENU, self.OnViewPlot, self.view_plot)

        return view_menu

    def OnViewToolbar(self, event):
        """ 工具栏显示与隐藏 """
        if self.view_toolbar.IsChecked():
            self.frame.get_tool_bar().Show()
        else:
            self.frame.get_tool_bar().Hide()

    def OnViewStausbar(self, event):
        """ 状态栏的显示与隐藏 """
        if self.view_stausbar.IsChecked():
            self.frame.get_staus_bar().Show()
        else:
            self.frame.get_staus_bar().Hide()

    def OnViewProject(self, event):
        """ 工程区的显示与隐藏 """
        if self.view_project.IsChecked():
            self.project.left_panel.Show()
        else:
            self.project.left_panel.Hide()

    def OnViewLog(self, event):
        """ 信息区的显示与隐藏 """
        if self.view_log.IsChecked():
            self.log.nb.Show()
        else:
            self.log.nb.Hide()

    def OnViewPlot(self, event):
        """ 显示区的显示与隐藏 """
        if self.view_plot.IsChecked():
            self.plot.MPL.Show()
        else:
            self.plot.MPL.Hide()


def start():
    app = wx.GetApp()
    view = ViewService(app)
    return view
