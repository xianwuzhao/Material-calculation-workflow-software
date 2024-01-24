import wx
import configparser

class denchar(wx.Panel):
    """ DENCHAR设置 """
    def __init__(self, parent, id, atom=None):
        wx.Panel.__init__(self, parent, id)

        self.atoms = atom
        self._paras = {}
        self._default = {}
        self._addition = {}

        self.denchar = False
        self.saverho = 'TRUE'
        self.savedeltarho = 'TRUE'
        self.writedenchar = 'TRUE'
        self.savetotalcharge = 'TRUE'


        denchar_box = wx.BoxSizer(wx.HORIZONTAL)

        box = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.CheckBox(self, label='电荷密度计算选择')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnDenchar)

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '常规设置')
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        SaveRho_x = wx.StaticText(self, label='SaveRho:             ')
        types1 = ['TRUE', 'FALSE']
        self.SaveRho = wx.ComboBox(self, -1, value='TRUE', choices=types1, style=wx.CB_READONLY, size=(100, 24))
        self.SaveRho.Bind(wx.EVT_COMBOBOX, self.OnSelect1)
        box1.Add(SaveRho_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.SaveRho, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        SaveDeltaRho_x = wx.StaticText(self, label='SaveDeltaRho:      ')
        types2 = ['TRUE', 'FALSE']
        self.SaveDeltaRho = wx.ComboBox(self, -1, value='TRUE', choices=types2, style=wx.CB_READONLY, size=(100, 24))
        self.SaveDeltaRho.Bind(wx.EVT_COMBOBOX, self.OnSelect2)
        box2.Add(SaveDeltaRho_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(self.SaveDeltaRho, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        WriteDenchar_x = wx.StaticText(self, label='WriteDenchar:      ')
        types3 = ['TRUE', 'FALSE']
        self.WriteDenchar = wx.ComboBox(self, -1, value='TRUE', choices=types3, style=wx.CB_READONLY, size=(100, 24))
        self.WriteDenchar.Bind(wx.EVT_COMBOBOX, self.OnSelect3)
        box3.Add(WriteDenchar_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box3.Add(self.WriteDenchar, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box4 = wx.BoxSizer(wx.HORIZONTAL)
        SaveTotalCharge_x = wx.StaticText(self, label='SaveTotalCharge: ')
        types4 = ['TRUE', 'FALSE']
        self.SaveTotalCharge = wx.ComboBox(self, -1, value='TRUE', choices=types4, style=wx.CB_READONLY, size=(100, 24))
        self.SaveTotalCharge.Bind(wx.EVT_COMBOBOX, self.OnSelect4)
        box4.Add(SaveTotalCharge_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box4.Add(self.SaveTotalCharge, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box5 = wx.BoxSizer(wx.HORIZONTAL)
        DencharTypeOfRun_x = wx.StaticText(self, label='Denchar.TypeOfRun:  ')
        self.DencharTypeOfRun = wx.TextCtrl(self, -1, value='3D', size=(70, 24))

        box6 = wx.BoxSizer(wx.HORIZONTAL)
        DencharPlotCharge_x = wx.StaticText(self, label='Denchar.PlotCharge:  ')
        self.DencharPlotCharge = wx.TextCtrl(self, -1, value='T', size=(70, 24))

        box7 = wx.BoxSizer(wx.HORIZONTAL)
        DencharCoorUnits_x = wx.StaticText(self, label='Denchar.CoorUnits:    ')
        self.DencharCoorUnits = wx.TextCtrl(self, -1, value='Ang', size=(70, 24))

        box8 = wx.BoxSizer(wx.HORIZONTAL)
        DencharDensityUnits_x = wx.StaticText(self, label='Denchar.DensityUnits: ')
        self.DencharDensityUnits = wx.TextCtrl(self, -1, value='Ele/Ang**3', size=(70, 24))

        box5.Add(DencharTypeOfRun_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box5.Add(self.DencharTypeOfRun, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box6.Add(DencharPlotCharge_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box6.Add(self.DencharPlotCharge, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box7.Add(DencharCoorUnits_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box7.Add(self.DencharCoorUnits, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box8.Add(DencharDensityUnits_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box8.Add(self.DencharDensityUnits, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz1.Add(box1, flag=wx.ALL, border=2)
        sz1.Add(box2, flag=wx.ALL, border=2)
        sz1.Add(box3, flag=wx.ALL, border=2)
        sz1.Add(box4, flag=wx.ALL, border=2)
        sz1.Add(box5, flag=wx.ALL, border=2)
        sz1.Add(box6, flag=wx.ALL, border=2)
        sz1.Add(box7, flag=wx.ALL, border=2)
        sz1.Add(box8, flag=wx.ALL, border=2)

        sz2 = wx.StaticBoxSizer(wx.VERTICAL, self, '参数设置')
        box9 = wx.BoxSizer(wx.HORIZONTAL)
        DencharNumberPointsX_x = wx.StaticText(self, label='Denchar.NumberPointsX: ')
        self.DencharNumberPointsX = wx.TextCtrl(self, -1, value='80', size=(70, 24))

        box10 = wx.BoxSizer(wx.HORIZONTAL)
        DencharNumberPointsY_x = wx.StaticText(self, label='Denchar.NumberPointsY: ')
        self.DencharNumberPointsY = wx.TextCtrl(self, -1, value='80', size=(70, 24))

        box11 = wx.BoxSizer(wx.HORIZONTAL)
        DencharNumberPointsZ_x = wx.StaticText(self, label='Denchar.NumberPointsZ: ')
        self.DencharNumberPointsZ = wx.TextCtrl(self, -1, value='40', size=(70, 24))

        box12 = wx.BoxSizer(wx.HORIZONTAL)
        DencharMinX_x = wx.StaticText(self, label='Denchar.MinX: ')
        self.DencharMinX = wx.TextCtrl(self, -1, value='-3', size=(70, 24))

        box13 = wx.BoxSizer(wx.HORIZONTAL)
        DencharMaxX_x = wx.StaticText(self, label='Denchar.MaxX: ')
        self.DencharMaxX = wx.TextCtrl(self, -1, value='8', size=(70, 24))

        box14 = wx.BoxSizer(wx.HORIZONTAL)
        DencharMinY_x = wx.StaticText(self, label='Denchar.MinY: ')
        self.DencharMinY = wx.TextCtrl(self, -1, value='-2', size=(70, 24))

        box15 = wx.BoxSizer(wx.HORIZONTAL)
        DencharMaxY_x = wx.StaticText(self, label='Denchar.MaxY: ')
        self.DencharMaxY = wx.TextCtrl(self, -1, value='11', size=(70, 24))

        box16 = wx.BoxSizer(wx.HORIZONTAL)
        DencharMinZ_x = wx.StaticText(self, label='Denchar.MinZ: ')
        self.DencharMinZ = wx.TextCtrl(self, -1, value='1', size=(70, 24))

        box17 = wx.BoxSizer(wx.HORIZONTAL)
        DencharMaxZ_x = wx.StaticText(self, label='Denchar.MaxZ: ')
        self.DencharMaxZ = wx.TextCtrl(self, -1, value='13', size=(70, 24))

        box9.Add(DencharNumberPointsX_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box9.Add(self.DencharNumberPointsX, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box10.Add(DencharNumberPointsY_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box10.Add(self.DencharNumberPointsY, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box11.Add(DencharNumberPointsZ_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box11.Add(self.DencharNumberPointsZ, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box12.Add(DencharMinX_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box12.Add(self.DencharMinX, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box13.Add(DencharMaxX_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box13.Add(self.DencharMaxX, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box14.Add(DencharMinY_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box14.Add(self.DencharMinY, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box15.Add(DencharMaxY_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box15.Add(self.DencharMaxY, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box16.Add(DencharMinZ_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box16.Add(self.DencharMinZ, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box17.Add(DencharMaxZ_x, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box17.Add(self.DencharMaxZ, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz2.Add(box9, flag=wx.ALL, border=2)
        sz2.Add(box10, flag=wx.ALL, border=2)
        sz2.Add(box11, flag=wx.ALL, border=2)
        sz2.Add(box12, flag=wx.ALL, border=2)
        sz2.Add(box13, flag=wx.ALL, border=2)
        sz2.Add(box14, flag=wx.ALL, border=2)
        sz2.Add(box15, flag=wx.ALL, border=2)
        sz2.Add(box16, flag=wx.ALL, border=2)
        sz2.Add(box17, flag=wx.ALL, border=2)

        sz3 = wx.StaticBoxSizer(wx.VERTICAL, self, '超胞设置')
        box18 = wx.BoxSizer(wx.HORIZONTAL)
        X_a = wx.StaticText(self, label='X轴方向: ')
        self.X_a = wx.TextCtrl(self, -1, value='3', size=(70, 24))
        box19 = wx.BoxSizer(wx.HORIZONTAL)
        Y_b = wx.StaticText(self, label='Y轴方向: ')
        self.Y_b = wx.TextCtrl(self, -1, value='3', size=(70, 24))
        box20 = wx.BoxSizer(wx.HORIZONTAL)
        Z_c = wx.StaticText(self, label='Z轴方向: ')
        self.Z_c = wx.TextCtrl(self, -1, value='1', size=(70, 24))

        box18.Add(X_a, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box18.Add(self.X_a, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box19.Add(Y_b, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box19.Add(self.Y_b, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box20.Add(Z_c, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box20.Add(self.Z_c, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz3.Add(box18, flag=wx.ALL, border=2)
        sz3.Add(box19, flag=wx.ALL, border=2)
        sz3.Add(box20, flag=wx.ALL, border=2)

        box.Add(self.cb, flag=wx.ALL, border=2)
        box.Add(sz1, flag=wx.ALL, border=2)

        denchar_box.Add(box, flag=wx.ALL, border=2)
        denchar_box.Add(sz2, flag=wx.ALL, border=2)
        denchar_box.Add(sz3, flag=wx.ALL, border=2)


        self.SetSizer(denchar_box)
        parent.AddPage(self, 'denchar')

    def doReConfig(self, filepath):
        conf = configparser.RawConfigParser()
        conf.read(filepath)
        ###
        if conf.get('Denchar', 'select') == 'True':
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)
        ###
        self.SaveRho.SetStringSelection(conf.get('Denchar', 'SaveRho'))
        self.SaveDeltaRho.SetStringSelection(conf.get('Denchar', 'SaveDeltaRho'))
        self.WriteDenchar.SetStringSelection(conf.get('Denchar', 'WriteDenchar'))
        self.SaveTotalCharge.SetStringSelection(conf.get('Denchar', 'SaveTotalCharge'))

        self.DencharTypeOfRun.SetValue(conf.get('Denchar', 'DencharTypeOfRun'))
        self.DencharPlotCharge.SetValue(conf.get('Denchar', 'DencharPlotCharge'))
        self.DencharCoorUnits.SetValue(conf.get('Denchar', 'DencharCoorUnits'))
        self.DencharDensityUnits.SetValue(conf.get('Denchar', 'DencharDensityUnits'))
        ###
        self.DencharNumberPointsX.SetValue(conf.get('Denchar', 'DencharNumberPointsX'))
        self.DencharNumberPointsY.SetValue(conf.get('Denchar', 'DencharNumberPointsY'))
        self.DencharNumberPointsZ.SetValue(conf.get('Denchar', 'DencharNumberPointsZ'))
        self.DencharMinX.SetValue(conf.get('Denchar', 'DencharMinX'))
        self.DencharMaxX.SetValue(conf.get('Denchar', 'DencharMaxX'))
        self.DencharMinY.SetValue(conf.get('Denchar', 'DencharMinY'))
        self.DencharMaxY.SetValue(conf.get('Denchar', 'DencharMaxY'))
        self.DencharMinZ.SetValue(conf.get('Denchar', 'DencharMinZ'))
        self.DencharMaxZ.SetValue(conf.get('Denchar', 'DencharMaxZ'))

    def SaveConfig(self, conf):
        conf.add_section('Denchar')
        ###
        conf.set('Denchar', 'select', self.cb.GetValue())
        ###
        conf.set('Denchar', 'SaveRho', self.SaveRho.GetStringSelection())
        conf.set('Denchar', 'SaveDeltaRho', self.SaveDeltaRho.GetStringSelection())
        conf.set('Denchar', 'WriteDenchar', self.WriteDenchar.GetStringSelection())
        conf.set('Denchar', 'SaveTotalCharge', self.SaveTotalCharge.GetStringSelection())
        conf.set('Denchar', 'DencharTypeOfRun', self.DencharTypeOfRun.GetValue())
        conf.set('Denchar', 'DencharPlotCharge', self.DencharPlotCharge.GetValue())
        conf.set('Denchar', 'DencharCoorUnits', self.DencharCoorUnits.GetValue())
        conf.set('Denchar', 'DencharDensityUnits', self.DencharDensityUnits.GetValue())
        ###
        conf.set('Denchar', 'DencharNumberPointsX', self.DencharNumberPointsX.GetValue())
        conf.set('Denchar', 'DencharNumberPointsY', self.DencharNumberPointsY.GetValue())
        conf.set('Denchar', 'DencharNumberPointsZ', self.DencharNumberPointsZ.GetValue())
        conf.set('Denchar', 'DencharMinX', self.DencharMinX.GetValue())
        conf.set('Denchar', 'DencharMaxX', self.DencharMaxX.GetValue())
        conf.set('Denchar', 'DencharMinY', self.DencharMinY.GetValue())
        conf.set('Denchar', 'DencharMaxY', self.DencharMaxY.GetValue())
        conf.set('Denchar', 'DencharMinZ', self.DencharMinZ.GetValue())
        conf.set('Denchar', 'DencharMaxZ', self.DencharMaxZ.GetValue())


    def GetParas(self):
        fdf = {
            'SaveRho': self.SaveRho.GetStringSelection(),
            'SaveDeltaRho': self.SaveDeltaRho.GetStringSelection(),
            'WriteDenchar': self.WriteDenchar.GetStringSelection(),
            'SaveTotalCharge': self.SaveTotalCharge.GetStringSelection(),
            'Denchar.TypeOfRun': self.DencharTypeOfRun.GetValue(),
            'Denchar.PlotCharge': self.DencharPlotCharge.GetValue(),
            'Denchar.CoorUnits': self.DencharCoorUnits.GetValue(),
            'Denchar.DensityUnits': self.DencharDensityUnits.GetValue(),
            ###
            'Denchar.NumberPointsX': self.DencharNumberPointsX.GetValue(),
            'Denchar.NumberPointsY': self.DencharNumberPointsY.GetValue(),
            'Denchar.NumberPointsZ': self.DencharNumberPointsZ.GetValue(),
            'Denchar.MinX': self.DencharMinX.GetValue(),
            'Denchar.MaxX': self.DencharMaxX.GetValue(),
            'Denchar.MinY': self.DencharMinY.GetValue(),
            'Denchar.MaxY': self.DencharMaxY.GetValue(),
            'Denchar.MinZ': self.DencharMinX.GetValue(),
            'Denchar.MaxZ': self.DencharMaxZ.GetValue()
        }
        self._paras.update(fdf)
        self._paras.update(self._default)
        self._paras.update(self._addition)
        return self._paras

    def OnDenchar(self, event):
        self.denchar = self.cb.GetValue()

    def OnSelect1(self, event):
        self.saverho = self.SaveRho.GetStringSelection()

    def OnSelect2(self, event):
        self.savedeltarho = self.SaveDeltaRho.GetStringSelection()

    def OnSelect3(self, event):
        self.writedenchar = self.WriteDenchar.GetStringSelection()

    def OnSelect4(self, event):
        self.savetotalcharge = self.SaveTotalCharge.GetStringSelection()

    def rho2xsf(self, path, model_path):

        with open(model_path, 'r') as f1:
            lines = f1.readlines()
            x = lines[2].strip('\n').strip(' ').split(' ')
            y = lines[3].strip('\n').strip(' ').split(' ')
            z = lines[4].strip('\n').strip(' ').split(' ')
            with open(path, 'w') as f:
                f.write('Siesta\nA\n0 0 0\n')
                f.write('{0} {1} {2}\n'.format(int(self.X_a.GetValue()) * float(x[0]),
                                               int(self.Y_b.GetValue()) * float(x[1]),
                                               int(self.Z_c.GetValue()) * float(x[2])))
                f.write('{0} {1} {2}\n'.format(int(self.X_a.GetValue()) * float(y[0]),
                                               int(self.Y_b.GetValue()) * float(y[1]),
                                               int(self.Z_c.GetValue()) * float(y[2])))
                f.write('{0} {1} {2}\n'.format(int(self.X_a.GetValue()) * float(z[0]),
                                               int(self.Y_b.GetValue()) * float(z[1]),
                                               int(self.Z_c.GetValue()) * float(z[2])))
                f.write(
                    '{0} {1} {2}\n'.format(self.DencharNumberPointsX.GetValue(), self.DencharNumberPointsY.GetValue(),
                                           self.DencharNumberPointsZ.GetValue()))
                f.write('RHO\nq')



