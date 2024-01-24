import wx
import os

class WorkPanel(wx.Dialog):
    """ 服务器配置界面 """

    def __init__(self, parent, app):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE)

        self.app = app
        self.log = app.log
        self.work_dir  = os.path.join(self.app.dir, r'Share\work_dir.ini')

        self.InitUI()
        sizer = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='  IP地址: ')
        self.text1 = wx.TextCtrl(self, -1, value='10.17.17.238', size=(120,20))
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='     端口: ')
        self.text2 = wx.TextCtrl(self, -1, value='131', size=(120, 20))
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box2.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='  用户名: ')
        self.text3 = wx.TextCtrl(self, -1, value='iei', size=(120, 20))
        box3.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box3.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box4 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='     密码: ')
        self.text4 = wx.TextCtrl(self, -1, value='ccmsiei', size=(120, 20), style=wx.TE_PASSWORD)
        box4.Add(st4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box4.Add(self.text4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sizer.Add(box1, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(box2, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(box3, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(box4, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnok = wx.Button(self, wx.ID_OK, '确定')
        btncancel = wx.Button(self, wx.ID_CANCEL, '取消')
        btnsizer.Add(btnok, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        btnsizer.Add(btncancel, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
        btnok.Bind(wx.EVT_BUTTON, self.OnOk)
        self.SetSizer(sizer)
        self.Layout()


    def InitUI(self):
        """ 初始化主界面 """
        icon = os.getcwd() + '\\icon\\MIDIS.ico'
        icon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        icon.SetHeight(18)
        icon.SetWidth(18)
        self.SetIcon(icon)
        self.SetTitle(title='服务器配置')
        self.SetSize(wx.Size(240, 210))
        self.Centre()

    def OnOk(self, event):
        keys = ['IP地址', '端口', '用户名', '密码']
        values = [self.text1.GetLineText(0), self.text2.GetLineText(0), self.text3.GetLineText(0),self.text4.GetLineText(0)]
        data = dict(zip(keys, values))
        with open(self.work_dir, 'w') as f:
            f.write(str(data))
        self.log.Info('服务器配置完成！')
        self.Close()