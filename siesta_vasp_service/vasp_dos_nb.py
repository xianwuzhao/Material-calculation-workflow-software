import wx
import os
import shutil


class DOS(wx.Panel):
    """ DOS设置 """
    def __init__(self, parent, id, path):
        wx.Panel.__init__(self, parent, id)

        self.system = 'dos'

        # if os.path.exists(os.path.join(path, 'POSCAR')):
        #     with open(os.path.join(path, 'POSCAR'), 'r') as f:
        #         name = f.readline().strip('\n').split(' ')
        #         self.system = name[0]
        # else:
        #     self.system = 'VASP'

        self.dos = False
        self.istart = '1'
        self.icharg = '11'
        self.lorbit = '10'
        self.kpoints = '9   9   9'

        dos_box = wx.BoxSizer(wx.HORIZONTAL)

        box_l = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.CheckBox(self, label='DOS计算选择')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnDos)

        sz = wx.StaticBoxSizer(wx.VERTICAL, self, '初始化')
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='计算任务名: ')
        self.text1 = wx.TextCtrl(self, -1, value=self.system)
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='生成波函数: ')
        types = ['随机', '读取']
        self.cb1 = wx.ComboBox(self, -1, value='随机', choices=types, style=wx.CB_READONLY)
        self.cb1.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box2.Add(self.cb1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='生成电荷密度: ')
        types1 = ['读取', '叠加', '读取且不变']
        self.cb2 = wx.ComboBox(self, -1, value='读取且不变', choices=types1, style=wx.CB_READONLY)
        self.cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect1)
        box3.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box3.Add(self.cb2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz.Add(box1, flag=wx.ALL, border=5)
        sz.Add(box2, flag=wx.ALL, border=5)
        sz.Add(box3, flag=wx.ALL, border=5)

        box_l.Add(self.cb, flag=wx.ALL, border=5)
        box_l.Add(sz, flag=wx.ALL, border=5)

        box_m = wx.BoxSizer(wx.VERTICAL)

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '态密度参数')
        box4 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='总态密度的原子轨道投影: ')
        types2 = ['s,p', 's,px,py,pz']
        self.cb3 = wx.ComboBox(self, -1, value='s,px,py,pz', choices=types2, style=wx.CB_READONLY)
        self.cb3.Bind(wx.EVT_COMBOBOX, self.OnSelect2)
        box4.Add(st4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box4.Add(self.cb3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box5 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(self, label='态密度计算中的取点个数: ')
        self.text2 = wx.TextCtrl(self, -1, value='500')
        box5.Add(st5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box5.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz1.Add(box4, flag=wx.ALL, border=5)
        sz1.Add(box5, flag=wx.ALL, border=5)

        sz2 = wx.StaticBoxSizer(wx.VERTICAL, self, 'K点设置')
        box6 = wx.BoxSizer(wx.HORIZONTAL)
        st6 = wx.StaticText(self, label='K点网格: ')
        types3 = ['5*5*5', '7*7*7', '9*9*9', '11*11*11']
        self.cb4 = wx.ComboBox(self, -1, value='9*9*9', choices=types3, style=wx.CB_READONLY)
        self.cb4.Bind(wx.EVT_COMBOBOX, self.OnSelect3)
        box6.Add(st6, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box6.Add(self.cb4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz2.Add(box6, flag=wx.ALL, border=5)

        box_m.Add(sz1, flag=wx.ALL, border=5)
        box_m.Add(sz2, flag=wx.ALL, border=5)

        dos_box.Add(box_l, flag=wx.ALL, border=5)
        dos_box.Add(box_m, flag=wx.ALL, border=5)


        self.SetSizer(dos_box)
        parent.AddPage(self, 'dos')

    def OnSelect(self, event):
        if self.cb1.GetStringSelection() == '随机':
            self.istart = '0'
        else:
            self.istart = '1'

    def OnSelect1(self, event):
        if self.cb2.GetStringSelection() == '读取':
            self.icharg = '1'
        elif self.cb2.GetStringSelection() == '叠加':
            self.icharg = '2'
        else:
            self.icharg = '11'

    def OnSelect2(self, event):
        if self.cb3.GetStringSelection() == 's,p':
            self.lorbit = '10'
        else:
            self.lorbit = '11'

    def OnSelect3(self, event):
        if self.cb4.GetStringSelection() == '5*5*5':
            self.kpoints = '5   5   5'
        elif self.cb4.GetStringSelection() == '7*7*7':
            self.kpoints = '7   7   7'
        elif self.cb4.GetStringSelection() == '9*9*9':
            self.kpoints = '9   9   9'
        else:
            self.kpoints = '11  11  11'

    def OnDos(self, event):
         self.dos = self.cb.GetValue()

    def WriteDos(self, path):
        if self.dos:
            def dos_folder(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        file_name = os.path.basename(path1)
                        name, ext = os.path.splitext(file_name)
                        if ext == '.cif':
                            dos_path = os.path.join(os.path.dirname(path1), 'dos')

                            if not os.path.exists(dos_path):
                                os.mkdir(dos_path)

                            with open(os.path.join(dos_path, 'INCAR'), 'a+') as f:
                                f.write('SYSTEM = ' + self.text1.GetLineText(0) + '\n')
                                f.write('ISTART = ' + self.istart + '\n')
                                f.write('ICHARG = ' + self.icharg + '\n')
                                f.write('LORBIT = ' + self.lorbit + '\n')
                                f.write('NEDOS = ' + self.text2.GetLineText(0) + '\n')
                                f.write('ALGO = V\n'
                                        'EDIEF = 0.0001\n'
                                        'EDIEFG = -0.01\n'
                                        'ENCUT = 250\n'
                                        'IBRION = -1\n'
                                        'ISIF = 2\n'
                                        'ISMEAR = -5\n'
                                        'LCHARG = False\n'
                                        'LWAVE = False\n'
                                        'NELW = 80\n'
                                        'NSW = 0\n'
                                        'PREC = N\n'
                                        'SIGMA = 0.1')

                            with open(os.path.join(dos_path, 'KPOINTS'), 'a+') as f:
                                f.write('Automatic generation\n'
                                        '0\n'
                                        'Mohkorst-Pack\n')
                                f.write(self.kpoints + '\n')
                                f.write('0   0   0')
                            shutil.copyfile(os.path.join(os.path.dirname(path1), 'POTCAR'),
                                            os.path.join(dos_path, 'POTCAR'))
                    else:
                        dos_folder(path1)

            dos_folder(path)

