import wx
import os
import shutil

class BAND(wx.Panel):
    """ BAND设置 """

    def __init__(self, parent, id, path):
        wx.Panel.__init__(self, parent, id)

        self.system = 'band'

        # if os.path.exists(os.path.join(path, 'POSCAR')):
        #     with open(os.path.join(path, 'POSCAR'), 'r') as f:
        #         name = f.readline().strip('\n').split(' ')
        #         self.system = name[0]
        # else:
        #     self.system = 'VASP'

        self.images = os.path.join(os.getcwd(), r'Share\kbands')
        self.kpoints = os.path.join(os.getcwd(), r'Share\kpoints')

        band_box = wx.BoxSizer(wx.HORIZONTAL)
        self.band = False
        self.istart = '1'
        self.icharg = '11'

        box = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.CheckBox(self, label='BAND计算选择')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnBand)

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

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '参数设置')
        box4 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='晶格类型: ')
        types2 = ['1D Nano Structure', '2D Nano Structure']
        self.cb3 = wx.ComboBox(self, choices=types2, style=wx.CB_READONLY)
        self.cb3.Bind(wx.EVT_COMBOBOX, self.OnSelect2)

        box4.Add(st4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box4.Add(self.cb3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box5 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(self, label='总能带数: ')
        self.text2 = wx.TextCtrl(self, -1, value='default')
        box5.Add(st5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box5.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        self.text = wx.TextCtrl(self, -1, value='', style=wx.TE_MULTILINE, size=(400, 200))

        sz1.Add(box4, flag=wx.ALL, border=5)
        sz1.Add(box5, flag=wx.ALL, border=5)
        sz1.Add(self.text, flag=wx.ALL, border=5)

        box.Add(self.cb, flag=wx.ALL, border=5)
        box.Add(sz, flag=wx.ALL, border=5)
        box.Add(sz1, flag=wx.ALL, border=5)

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '向量显示')
        image = os.path.join(self.images, r'default.jpg')
        temp = wx.Image(image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.sbp = wx.StaticBitmap(self, -1, bitmap=temp, size=(400, 400))

        sz1.Add(self.sbp, flag=wx.ALL, border=5)

        band_box.Add(box, flag=wx.ALL, border=5)
        band_box.Add(sz1, flag=wx.ALL, border=5)

        self.SetSizer(band_box)
        parent.AddPage(self, 'band')

    def OnBand(self, event):
        self.band = self.cb.GetValue()

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
        if self.cb3.GetStringSelection() == '1D Nano Structure':
            self.text.Clear()
            with open(os.path.join(self.kpoints, r'1D Nano Structure'), 'r') as f:
                file = f.readlines()
                for i in range(4, len(file)):
                    self.text.AppendText(file[i])

            image = os.path.join(self.images, r'1D Nano Structure.jpg')
            temp = wx.Image(image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            temp.SetHeight(400)
            temp.SetWidth(400)
            self.sbp.SetBitmap(temp)


        elif self.cb3.GetStringSelection() == '2D Nano Structure':
            self.text.Clear()
            with open(os.path.join(self.kpoints, r'2D Nano Structure'), 'r') as f:
                file = f.readlines()
                for i in range(4, len(file)):
                    self.text.AppendText(file[i])

            image = os.path.join(self.images, r'2D Nano Structure.jpg')
            temp = wx.Image(image, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            temp.SetHeight(400)
            temp.SetWidth(400)
            self.sbp.SetBitmap(temp)

        else:
            self.text.Clear()

    def WriteBand(self, path):
        if self.band:

            def band_folder(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        file_name = os.path.basename(path1)
                        name, ext = os.path.splitext(file_name)
                        if ext == '.cif':
                            band_path = os.path.join(os.path.dirname(path1), 'band')

                            if not os.path.exists(band_path):
                                os.mkdir(band_path)

                            with open(os.path.join(band_path, 'INCAR'), 'a+') as f:
                                f.write('SYSTEM = ' + self.text1.GetLineText(0) + '\n')
                                f.write('ISTART = ' + self.istart + '\n')
                                f.write('ICHARG = ' + self.icharg + '\n')
                                f.write('ALGO = N\n'
                                        'LORBIT = 11\n'
                                              'EDIEF = 0.0001\n'
                                              'ENCUT = 250\n'
                                              'IBRION = -1\n'
                                              'ISMEAR = 0\n'
                                              'LCHARG = False\n'
                                              'LWAVE = False\n'
                                              'NELW = 80\n'
                                              'NSW = 0\n'
                                              'PREC = N\n'
                                              'SIGMA = 0.05\n')
                                if self.text1.GetLineText(0) != 'default':
                                    f.write('NBANDS = ' + self.text2.GetLineText(0))

                            if self.cb3.GetStringSelection() == '1D Nano Structure':
                                shutil.copyfile(os.path.join(self.kpoints, r'1D Nano Structure'),
                                                os.path.join(band_path, 'KPOINTS'))
                            elif self.cb3.GetStringSelection() == '2D Nano Structure':
                                shutil.copyfile(os.path.join(self.kpoints, r'2D Nano Structure'),
                                                os.path.join(band_path, 'KPOINTS'))
                            else:
                                pass

                            shutil.copyfile(os.path.join(os.path.dirname(path1), 'POTCAR'),
                                            os.path.join(band_path, 'POTCAR'))


                    else:
                        band_folder(path1)

            band_folder(path)