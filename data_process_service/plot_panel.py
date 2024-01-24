import wx
import os


class PlotConfig(wx.Dialog):
    """ 绘图配置界面 """

    def __init__(self, parent, app):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE)

        self.app = app
        types = ['s', 'p', 'd', 'f']

        self.band_element = False
        self.band_orbit = False

        self.dos_element = False
        self.dos_orbit = False

        self.element1 = ''
        self.element2 = ''
        self.element3 = ''
        self.element4 = ''
        self.element5 = ''

        self.orbit1 = ''
        self.orbit2 = ''
        self.orbit3 = ''
        self.orbit4 = ''
        self.orbit5 = ''

        self.InitUI()

        sz1 = wx.StaticBoxSizer(wx.HORIZONTAL, self, '能带绘图设置')
        Box = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.CheckBox(self, label='投影到元素上')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnCb1)

        self.cb1 = wx.CheckBox(self, label='投影到轨道上')
        self.cb1.SetValue(False)
        self.cb1.Bind(wx.EVT_CHECKBOX, self.OnCb2)

        Box.Add(self.cb, flag=wx.ALL, border=5)
        Box.Add(self.cb1, flag=wx.ALL, border=5)

        sz = wx.StaticBoxSizer(wx.VERTICAL, self, '轨道设置')
        box = wx.BoxSizer(wx.HORIZONTAL)

        st1 = wx.StaticText(self, label='元素      ')
        st2 = wx.StaticText(self, label='轨道')

        box.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND| wx.ALL, border=3)
        box.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND| wx.ALL, border=3)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        self.text1 = wx.TextCtrl(self, -1, value=self.element1, size=(50,20))
        self.cb1_1 = wx.ComboBox(self, choices=types, style=wx.CB_READONLY)
        self.cb1_1.Bind(wx.EVT_COMBOBOX, self.OnSelect1)

        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.cb1_1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.text2 = wx.TextCtrl(self, -1, value=self.element2, size=(50,20))
        self.cb2_1 = wx.ComboBox(self, choices=types, style=wx.CB_READONLY)
        self.cb2_1.Bind(wx.EVT_COMBOBOX, self.OnSelect2)

        box2.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(self.cb2_1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        self.text3 = wx.TextCtrl(self, -1, value=self.element3, size=(50,20))
        self.cb3_1 = wx.ComboBox(self, choices=types, style=wx.CB_READONLY)
        self.cb3_1.Bind(wx.EVT_COMBOBOX, self.OnSelect3)

        box3.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box3.Add(self.cb3_1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box4 = wx.BoxSizer(wx.HORIZONTAL)
        self.text4 = wx.TextCtrl(self, -1, value=self.element4, size=(50,20))
        self.cb4_1 = wx.ComboBox(self, choices=types, style=wx.CB_READONLY)
        self.cb4_1.Bind(wx.EVT_COMBOBOX, self.OnSelect4)

        box4.Add(self.text4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box4.Add(self.cb4_1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box5 = wx.BoxSizer(wx.HORIZONTAL)
        self.text5 = wx.TextCtrl(self, -1, value=self.element5, size=(50,20))
        self.cb5_1 = wx.ComboBox(self, choices=types, style=wx.CB_READONLY)
        self.cb5_1.Bind(wx.EVT_COMBOBOX, self.OnSelect5)

        box5.Add(self.text5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box5.Add(self.cb5_1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz.Add(box, flag=wx.ALL, border=5)
        sz.Add(box1, flag=wx.ALL, border=5)
        sz.Add(box2, flag=wx.ALL, border=5)
        sz.Add(box3, flag=wx.ALL, border=5)
        sz.Add(box4, flag=wx.ALL, border=5)
        sz.Add(box5, flag=wx.ALL, border=5)

        sz1.Add(Box, flag=wx.ALL, border=5)
        sz1.Add(sz, flag=wx.ALL, border=5)

        sz2 = wx.StaticBoxSizer(wx.VERTICAL, self, '态密度绘图设置')
        self.cb2 = wx.CheckBox(self, label='投影到元素上')
        self.cb2.SetValue(False)
        self.cb2.Bind(wx.EVT_CHECKBOX, self.OnCb3)

        self.cb3 = wx.CheckBox(self, label='投影到轨道上')
        self.cb3.SetValue(False)
        self.cb3.Bind(wx.EVT_CHECKBOX, self.OnCb4)

        sz2.Add(self.cb2, flag=wx.ALL, border=5)
        sz2.Add(self.cb3, flag=wx.ALL, border=5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sz1, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sizer.Add(sz2, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnok = wx.Button(self, wx.ID_OK, '确定')
        btncancel = wx.Button(self, wx.ID_CANCEL, '取消')
        btnsizer.Add(btnok, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        btnsizer.Add(btncancel, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
        btnok.Bind(wx.EVT_BUTTON, self.OnOk)
        self.SetSizer(sizer)
        self.Layout()


    def OnCb1(self, event):
        self.band_element = self.cb.GetValue()

    def OnCb2(self, event):
        self.band_orbit = self.cb1.GetValue()

    def OnCb3(self, event):
        self.dos_element = self.cb2.GetValue()

    def OnCb4(self, event):
        self.dos_orbit = self.cb3.GetValue()

    def OnSelect1(self, event):
        self.orbit1 = self.cb1_1.GetStringSelection()

    def OnSelect2(self, event):
        self.orbit2 = self.cb2_1.GetStringSelection()

    def OnSelect3(self, event):
        self.orbit3 = self.cb3_1.GetStringSelection()

    def OnSelect4(self, event):
        self.orbit4 = self.cb4_1.GetStringSelection()

    def OnSelect5(self, event):
        self.orbit5 = self.cb5_1.GetStringSelection()


    def InitUI(self):
        """ 初始化主界面 """
        icon = os.getcwd() + '\\icon\\MIDIS.ico'
        icon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        icon.SetHeight(18)
        icon.SetWidth(18)
        self.SetIcon(icon)
        self.SetTitle(title='绘图配置')
        self.Centre()

    def OnOk(self, event):
        self.element1 = self.text1.GetLineText(0)
        self.element2 = self.text2.GetLineText(0)
        self.element3 = self.text3.GetLineText(0)
        self.element4 = self.text4.GetLineText(0)
        self.element5 = self.text5.GetLineText(0)

        self.Destroy()
