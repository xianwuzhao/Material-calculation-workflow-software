import wx
import numpy as np
import configparser


class dos(wx.Panel):
    """ DOS设置 """
    def __init__(self, parent, id, atoms=None):
        wx.Panel.__init__(self, parent, id)

        self.atoms = atoms

        self.dos = False
        self.kpt1 = '0'
        self.kpt2 = '0'
        self.kpt3 = '0'

        dos_box = wx.BoxSizer(wx.VERTICAL)

        self.cb = wx.CheckBox(self, label='dos计算选择')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnDos)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='K点设置精度: ')
        types = ['corase', 'medium', 'fine', 'ultra-fine']
        self.cb1 = wx.ComboBox(self, -1, value='', choices=types, style=wx.CB_READONLY, size=(80,24))
        self.cb1.Bind(wx.EVT_COMBOBOX, self.OnSelect1)

        self.text1 = wx.TextCtrl(self, -1, value='', size=(40,24))
        self.text2 = wx.TextCtrl(self, -1, value='', size=(40,24))
        self.text3 = wx.TextCtrl(self, -1, value='', size=(40,24))

        types1 = ['0', '0.5']
        self.cb2 = wx.ComboBox(self, -1, value='', choices=types1, style=wx.CB_READONLY, size=(40,24))
        self.cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect2)
        self.cb3 = wx.ComboBox(self, -1, value='', choices=types1, style=wx.CB_READONLY, size=(40, 24))
        self.cb3.Bind(wx.EVT_COMBOBOX, self.OnSelect3)
        self.cb4 = wx.ComboBox(self, -1, value='', choices=types1, style=wx.CB_READONLY, size=(40, 24))
        self.cb4.Bind(wx.EVT_COMBOBOX, self.OnSelect4)

        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.cb1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.cb2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.cb3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.cb4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz = wx.StaticBoxSizer(wx.VERTICAL, self, '费米能级上下区间参数设置')
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='下限(eV): ')
        self.text4 = wx.TextCtrl(self, -1, value='-20.0', size=(70,24))
        st3 = wx.StaticText(self, label='上限(eV): ')
        self.text5 = wx.TextCtrl(self, -1, value='10.0', size=(70, 24))

        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(self.text4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(self.text5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='间隔(eV): ')
        self.text6 = wx.TextCtrl(self, -1, value='0.2', size=(70, 24))
        st5 = wx.StaticText(self, label='取点数:    ')
        self.text7 = wx.TextCtrl(self, -1, value='800', size=(70, 24))

        box3.Add(st4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box3.Add(self.text6, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box3.Add(st5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box3.Add(self.text7, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz.Add(box2, flag=wx.ALL, border=2)
        sz.Add(box3, flag=wx.ALL, border=2)

        dos_box.Add(self.cb, flag=wx.ALL, border=2)
        dos_box.Add(box1, flag=wx.ALL, border=2)
        dos_box.Add(sz, flag=wx.ALL, border=2)

        self.initial()
        self.SetSizer(dos_box)
        parent.AddPage(self, 'dos')

    def doSetAccuracy(self):
        valueindex = self.cb1.GetSelection()
        multi = [1,1.5,2,4]
        self.text1.SetValue(str(int(self.kdosvalue1 * multi[valueindex])))
        self.text2.SetValue(str(int(self.kdosvalue2 * multi[valueindex])))
        self.text3.SetValue(str(int(self.kdosvalue3 * multi[valueindex])))

    def initial(self):
        self.cb1.SetSelection(1)
        self.cb2.SetSelection(0)
        self.cb3.SetSelection(0)
        self.cb4.SetSelection(0)

        self.a = np.linalg.norm(self.atoms.cell[0])
        a = self.a
        kvalue = 3 * 4 * 4 / a
        if kvalue < 1:
            kvalue = 1
        elif kvalue > int(kvalue) + 0.5:
            kvalue = int(kvalue) + 1
        else:
            kvalue = int(kvalue)
        self.kdosvalue1 = kvalue

        self.a = np.linalg.norm(self.atoms.cell[1])
        a = self.a
        kvalue = 3*4*4/a
        if kvalue < 1:
            kvalue = 1
        elif kvalue > int(kvalue) + 0.5:
            kvalue = int(kvalue) + 1
        else:
            kvalue = int(kvalue)
        self.kdosvalue2 = kvalue

        self.a = np.linalg.norm(self.atoms.cell[2])
        a = self.a
        kvalue = 3 * 4 * 4 / a
        if kvalue < 1:
            kvalue = 1
        elif kvalue > int(kvalue) + 0.5:
            kvalue = int(kvalue) + 1
        else:
            kvalue = int(kvalue)
        self.kdosvalue3 = kvalue
        self.cb1.SetSelection(1)
        self.doSetAccuracy()

    def OnDos(self, event):
        self.dos = self.cb.GetValue()

    def OnSelect1(self, event):
        self.doSetAccuracy()

    def OnSelect2(self, event):
        self.kpt1 = self.cb2.GetStringSelection()

    def OnSelect3(self, event):
        self.kpt2 = self.cb3.GetStringSelection()

    def OnSelect4(self, event):
        self.kpt3 = self.cb4.GetStringSelection()

    def GetKpts(self):
        return (int(self.text1.GetValue()), int(self.text2.GetValue()), int(self.text3.GetValue()))

    def Getdosstr(self):
        dosstr = ''
        energysection_sdata = float(self.text4.GetValue())
        dosstr += str(energysection_sdata)
        dosstr += ' '

        energysection_edata = float(self.text5.GetValue())
        dosstr += str(energysection_edata)
        dosstr += '    '
        dosstr += self.text6.GetValue()
        dosstr += '   '
        dosstr += self.text7.GetValue()
        dosstr += '    '
        dosstr += 'eV\n'
        return dosstr

    def doReConfig(self, filepath):
        conf = configparser.RawConfigParser()
        conf.read(filepath)
        ###
        if conf.get('DOS', 'select') == 'True':
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)
            ###
        self.text4.SetValue(conf.get('DOS', 'energysection_s'))
        self.text5.SetValue(conf.get('DOS', 'energysection_e'))
        self.text6.SetValue(conf.get('DOS', 'energyinterval'))
        self.text7.SetValue(conf.get('DOS', 'energynum'))
        ###
        self.text1.SetValue(conf.get('DOS', 'kpts1'))
        self.text2.SetValue(conf.get('DOS', 'kpts2'))
        self.text3.SetValue(conf.get('DOS', 'kpts3'))
        self.cb2.SetStringSelection(conf.get('DOS', 'kpts4'))
        self.cb3.SetStringSelection(conf.get('DOS', 'kpts5'))
        self.cb4.SetStringSelection(conf.get('DOS', 'kpts6'))
        ###
        self.cb1.SetStringSelection(conf.get('DOS', 'Accuracy'))

    def SaveConfig(self, conf):
        conf.add_section('DOS')
        ###
        conf.set('DOS', 'select', str(self.cb.GetValue()))
        ###
        conf.set('DOS', 'energysection_s', self.text4.GetValue())
        conf.set('DOS', 'energysection_e', self.text5.GetValue())
        conf.set('DOS', 'energyinterval', self.text6.GetValue())
        conf.set('DOS', 'energynum', self.text7.GetValue())
        ###
        conf.set('DOS', 'Accuracy', self.cb1.GetStringSelection())
        ###
        conf.set('DOS', 'kpts1', self.text1.GetValue())
        conf.set('DOS', 'kpts2', self.text2.GetValue())
        conf.set('DOS', 'kpts3', self.text3.GetValue())
        conf.set('DOS', 'kpts4', self.cb2.GetStringSelection())
        conf.set('DOS', 'kpts5', self.cb3.GetStringSelection())
        conf.set('DOS', 'kpts6', self.cb4.GetStringSelection())



