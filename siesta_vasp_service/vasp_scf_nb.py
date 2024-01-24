import wx
import os
import shutil


class SCF(wx.Panel):
    """ SCF设置 """
    def __init__(self, parent, id, path):
        wx.Panel.__init__(self, parent, id)


        self.system = 'scf'

        # if os.path.exists(os.path.join(path, 'POSCAR')):
        #     with open(os.path.join(path, 'POSCAR'), 'r') as f:
        #         name = f.readline().strip('\n').split(' ')
        #         self.system = name[0]
        # else:
        #     self.system = 'VASP'

        scf_box = wx.BoxSizer(wx.HORIZONTAL)
        self.scf = False
        self.ip = True
        self.cv = False
        self.cs = False
        self.istart = '0'
        self.icharg = '2'
        self.ismear = '-5'
        self.ibrion = '-1'
        self.isif = '2'
        self.prec = 'N'
        self.ispin = '1'
        self.algo = 'V'
        self.lwave = 'False'
        self.lcharg = 'False'
        self.kpoints = '9   9   9'
        self.encut = '250'

        # 左边
        box_l = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.CheckBox(self, label='SCF计算选择')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnScf)

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
        self.cb2 = wx.ComboBox(self, -1, value='叠加', choices=types1, style=wx.CB_READONLY)
        self.cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect1)
        box3.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box3.Add(self.cb2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz.Add(box1, flag=wx.ALL, border=5)
        sz.Add(box2, flag=wx.ALL, border=5)
        sz.Add(box3, flag=wx.ALL, border=5)

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '电子自洽收敛')
        box4 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='电子迭代的最大步数: ')
        self.text2 = wx.TextCtrl(self, -1, value='80')
        box4.Add(st4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box4.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box5 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(self, label='电子迭代收敛标准: ')
        self.text3 = wx.TextCtrl(self, -1, value='0.0001')
        st51 = wx.StaticText(self, label=' eV/Ang')
        box5.Add(st5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box5.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box5.Add(st51, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz1.Add(box4, flag=wx.ALL, border=5)
        sz1.Add(box5, flag=wx.ALL, border=5)

        sz2 = wx.StaticBoxSizer(wx.VERTICAL, self, 'smearing方法')
        box6 = wx.BoxSizer(wx.HORIZONTAL)
        st6 = wx.StaticText(self, label='轨道占据数的拖尾效应: ')
        types2 = ['四面体方法', '高斯', 'MP方法']
        self.cb3 = wx.ComboBox(self, -1, value='四面体方法', choices=types2, style=wx.CB_READONLY)
        self.cb3.Bind(wx.EVT_COMBOBOX, self.OnSelect2)
        box6.Add(st6, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box6.Add(self.cb3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box7 = wx.BoxSizer(wx.HORIZONTAL)
        st7 = wx.StaticText(self, label='拖尾效应展宽: ')
        self.text4 = wx.TextCtrl(self, -1, value='0.1')
        st71 = wx.StaticText(self, label=' eV')
        box7.Add(st7, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box7.Add(self.text4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box7.Add(st71, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz2.Add(box6, flag=wx.ALL, border=5)
        sz2.Add(box7, flag=wx.ALL, border=5)

        box_l.Add(self.cb, flag=wx.ALL, border=5)
        box_l.Add(sz, flag=wx.ALL, border=5)
        box_l.Add(sz1, flag=wx.ALL, border=5)
        box_l.Add(sz2, flag=wx.ALL, border=5)

        # 中间
        box_m = wx.BoxSizer(wx.VERTICAL)
        sz3 = wx.StaticBoxSizer(wx.VERTICAL, self, '离子优化')

        box8 = wx.BoxSizer(wx.HORIZONTAL)
        st8 = wx.StaticText(self, label='离子优化收敛标准: ')
        self.text5 = wx.TextCtrl(self, -1, value='-0.05')
        st81 = wx.StaticText(self, label=' eV/Ang')
        box8.Add(st8, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box8.Add(self.text5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box8.Add(st81, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box9 = wx.BoxSizer(wx.HORIZONTAL)
        st9 = wx.StaticText(self, label='离子优化最大步长: ')
        self.text6 = wx.TextCtrl(self, -1, value='0')
        box9.Add(st9, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box9.Add(self.text6, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box10 = wx.BoxSizer(wx.HORIZONTAL)
        st10 = wx.StaticText(self, label='离子优化方法: ')
        types3 = ['准牛顿法', '共轭梯度(CG)法', '动力学计算', '弹性常数计算', 'DFT分子动力学计算', '其他']
        self.cb4 = wx.ComboBox(self, -1, value='其他', choices=types3, style=wx.CB_READONLY)
        self.cb4.Bind(wx.EVT_COMBOBOX, self.OnSelect3)
        box10.Add(st10, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box10.Add(self.cb4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz3.Add(box8, flag=wx.ALL, border=5)
        sz3.Add(box9, flag=wx.ALL, border=5)
        sz3.Add(box10, flag=wx.ALL, border=5)

        sz4 = wx.StaticBoxSizer(wx.VERTICAL, self, '结构优化参数')

        self.cbx1 = wx.CheckBox(self, label='离子位置弛豫')
        self.cbx1.SetValue(True)
        self.cbx1.Bind(wx.EVT_CHECKBOX, self.OnIonPosition)

        self.cbx2 = wx.CheckBox(self, label='改变原胞体积')
        self.cbx2.SetValue(False)
        self.cbx2.Bind(wx.EVT_CHECKBOX, self.OnCellVolume)

        self.cbx3 = wx.CheckBox(self, label='改变原胞形状')
        self.cbx3.SetValue(False)
        self.cbx3.Bind(wx.EVT_CHECKBOX, self.OnCellShape)

        sz4.Add(self.cbx1, flag=wx.ALL, border=5)
        sz4.Add(self.cbx2, flag=wx.ALL, border=5)
        sz4.Add(self.cbx3, flag=wx.ALL, border=5)

        sz5 = wx.StaticBoxSizer(wx.VERTICAL, self, 'K点设置')

        box11 = wx.BoxSizer(wx.HORIZONTAL)
        st11 = wx.StaticText(self, label='K点网格: ')
        types4 = ['5*5*5', '7*7*7', '9*9*9', '11*11*11']
        self.cb5 = wx.ComboBox(self, -1, value='9*9*9', choices=types4, style=wx.CB_READONLY)
        self.cb5.Bind(wx.EVT_COMBOBOX, self.OnSelect4)
        box11.Add(st11, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box11.Add(self.cb5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz5.Add(box11, flag=wx.ALL, border=5)

        box_m.Add(sz3, flag=wx.ALL, border=5)
        box_m.Add(sz4, flag=wx.ALL, border=5)
        box_m.Add(sz5, flag=wx.ALL, border=5)

        # 右边
        box_r = wx.BoxSizer(wx.VERTICAL)

        sz6 = wx.StaticBoxSizer(wx.VERTICAL, self, '计算精度')

        box12 = wx.BoxSizer(wx.HORIZONTAL)
        st12 = wx.StaticText(self, label='平面波切断动能: ')
        types5 = ['250', '300', '350', '400']
        self.cb6 = wx.ComboBox(self, -1, value='250', choices=types5, style=wx.CB_READONLY)
        self.cb6.Bind(wx.EVT_COMBOBOX, self.OnSelect5)
        st121 = wx.StaticText(self, label=' eV')
        box12.Add(st12, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box12.Add(self.cb6, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box12.Add(st121, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box13 = wx.BoxSizer(wx.HORIZONTAL)
        st13 = wx.StaticText(self, label='计算精度: ')
        types6 = ['低', '常规', '高']
        self.cb7 = wx.ComboBox(self, -1, value='常规', choices=types6, style=wx.CB_READONLY)
        self.cb7.Bind(wx.EVT_COMBOBOX, self.OnSelect6)
        box13.Add(st13, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box13.Add(self.cb7, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz6.Add(box12, flag=wx.ALL, border=5)
        sz6.Add(box13, flag=wx.ALL, border=5)

        sz7 = wx.StaticBoxSizer(wx.VERTICAL, self, '自旋极化和电子优化算法')
        self.cbx4 = wx.CheckBox(self, label='自旋极化')
        self.cbx4.SetValue(False)
        self.cbx4.Bind(wx.EVT_CHECKBOX, self.OnSpin)

        box13 = wx.BoxSizer(wx.HORIZONTAL)
        st13 = wx.StaticText(self, label='电子波函数优化算法: ')
        types7 = ['DVA算法', 'RMM算法', 'N与V结合']
        self.cb8 = wx.ComboBox(self, -1, value='RMM算法', choices=types7, style=wx.CB_READONLY)
        self.cb8.Bind(wx.EVT_COMBOBOX, self.OnSelect7)
        box13.Add(st13, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box13.Add(self.cb8, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz7.Add(self.cbx4, flag=wx.ALL, border=5)
        sz7.Add(box13, flag=wx.ALL, border=5)

        sz8 = wx.StaticBoxSizer(wx.VERTICAL, self, '文件输出控制')
        box14 = wx.BoxSizer(wx.HORIZONTAL)
        st14 = wx.StaticText(self, label='输出波函数: ')
        types8 = ['FALSE', 'TRUE']
        self.cb9 = wx.ComboBox(self, -1, value='FALSE', choices=types8, style=wx.CB_READONLY)
        self.cb9.Bind(wx.EVT_COMBOBOX, self.OnSelect8)
        box14.Add(st14, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box14.Add(self.cb9, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box15 = wx.BoxSizer(wx.HORIZONTAL)
        st21 = wx.StaticText(self, label='输出电荷密度: ')
        types9 = ['FALSE', 'TRUE']
        self.cb10 = wx.ComboBox(self, -1, value='FALSE', choices=types9, style=wx.CB_READONLY)
        self.cb10.Bind(wx.EVT_COMBOBOX, self.OnSelect9)
        box15.Add(st21, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box15.Add(self.cb10, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz8.Add(box14, flag=wx.ALL, border=5)
        sz8.Add(box15, flag=wx.ALL, border=5)

        box_r.Add(sz6, flag=wx.ALL, border=5)
        box_r.Add(sz7, flag=wx.ALL, border=5)
        box_r.Add(sz8, flag=wx.ALL, border=5)

        scf_box.Add(box_l, flag=wx.ALL, border=5)
        scf_box.Add(box_m, flag=wx.ALL, border=5)
        scf_box.Add(box_r, flag=wx.ALL, border=5)

        self.SetSizer(scf_box)
        parent.AddPage(self, 'scf')

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
        if self.cb3.GetStringSelection() == '四面体方法':
            self.ismear = '-5'
        elif self.cb3.GetStringSelection() == '高斯':
            self.ismear = '0'
        else:
            self.ismear = '1'

    def OnSelect3(self, event):
        if self.cb4.GetStringSelection() == '准牛顿法':
            self.ibrion = '1'
        elif self.cb4.GetStringSelection() == '共轭梯度(CG)法':
            self.ibrion = '2'
        elif self.cb4.GetStringSelection() == '动力学计算':
            self.ibrion = '5'
        elif self.cb4.GetStringSelection() == '弹性常数计算':
            self.ibrion = '6'
        elif self.cb4.GetStringSelection() == 'DFT分子动力学计算':
            self.ibrion = '0'
        else:
            self.ibrion = '-1'

    def OnSelect4(self, event):
        if self.cb5.GetStringSelection() == '5*5*5':
            self.kpoints = '5   5   5'
        elif self.cb5.GetStringSelection() == '7*7*7':
            self.kpoints = '7   7   7'
        elif self.cb5.GetStringSelection() == '9*9*9':
            self.kpoints = '9   9   9'
        else:
            self.kpoints = '11  11  11'

    def OnSelect5(self, event):
        self.encut = self.cb6.GetStringSelection()

    def OnSelect6(self, event):
        if self.cb7.GetStringSelection() == '低':
            self.prec = 'L'
        elif self.cb7.GetStringSelection() == '常规':
            self.prec = 'N'
        else:
            self.prec = 'H'

    def OnSelect7(self, event):
        if self.cb8.GetStringSelection() == 'DAV算法':
            self.algo = 'N'
        elif self.cb8.GetStringSelection() == 'RMM算法':
            self.algo = 'V'
        else:
            self.algo = 'F'

    def OnSelect8(self, event):
        self.lwave = self.cb9.GetStringSelection()

    def OnSelect9(self, event):
        self.lcharg = self.cb10.GetStringSelection()

    def OnIonPosition(self, event):
        if self.cbx1.GetValue():
            self.ip = True
        else:
            self.ip = False

    def OnCellVolume(self, event):
        if self.cbx2.GetValue():
            self.cv = True
        else:
            self.cv = False

    def OnCellShape(self, event):
        if self.cbx3.GetValue():
            self.cs = True
        else:
            self.cs = False

    def OnSpin(self, event):
        if self.cbx4.GetValue():
            self.ispin = '2'
        else:
            pass

    def OnScf(self, event):
        self.scf = self.cb.GetValue()

    def Isif(self):
        if self.ip and not self.cs and not self.cv:
            self.isif = '2'
        elif self.ip and self.cv and self.cs:
            self.isif = '3'
        elif self.ip and not self.cv and self.cs:
            self.isif = '4'
        elif not self.ip and self.cv and self.cs:
            self.isif = '6'
        else:
            pass

    def WriteScf(self, path):
        if self.scf:

            def scf_folder(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        file_name = os.path.basename(path1)
                        name, ext = os.path.splitext(file_name)
                        if ext == '.cif':
                            scf_path = os.path.join(os.path.dirname(path1), 'scf')

                            if not os.path.exists(scf_path):
                                os.mkdir(scf_path)

                            with open(os.path.join(scf_path, 'INCAR'), 'a+') as f:
                                f.write('SYSTEM = ' + self.text1.GetLineText(0) + '\n')
                                f.write('ISTART = ' + self.istart + '\n')
                                f.write('ICHARG = ' + self.icharg + '\n')
                                f.write('PREC = ' + self.prec + '\n')
                                f.write('ALGO = ' + self.algo + '\n')
                                f.write('NELM = ' + self.text2.GetLineText(0) + '\n')
                                f.write('EDIFF = ' + self.text3.GetLineText(0) + '\n')
                                f.write('ENCUT = ' + self.encut + '\n')
                                f.write('IBRION = ' + self.ibrion + '\n')
                                f.write('NSW = ' + self.text6.GetLineText(0) + '\n')
                                f.write('ISIF = ' + self.isif + '\n')
                                f.write('EDIFFG = ' + self.text5.GetLineText(0) + '\n')
                                f.write('SIGMA = ' + self.text4.GetLineText(0) + '\n')
                                f.write('ISMEAR = ' + self.ismear + '\n')
                                f.write('ISPIN = ' + self.ispin + '\n')
                                f.write('LWAVE = ' + self.lwave + '\n')
                                f.write('LCHARG = ' + self.lcharg)

                            with open(os.path.join(scf_path, 'KPOINTS'), 'a+') as f:
                                f.write('Automatic generation\n'
                                        '0\n'
                                        'Mohkorst-Pack\n')
                                f.write(self.kpoints + '\n')
                                f.write('0   0   0')

                            shutil.copyfile(os.path.join(os.path.dirname(path1), 'POTCAR'),
                                            os.path.join(scf_path, 'POTCAR'))
                    else:
                        scf_folder(path1)

            scf_folder(path)