import wx
import wx.grid as grid
import os
import configparser
from ase.io import xsf
import numpy as np

class scf(wx.Panel):
    """ SCF设置 """
    def __init__(self, parent, id, atom=None):
        wx.Panel.__init__(self, parent, id)

        self.atoms = atom


        self.default = {
            'keys': ['SystemName', 'AtomicCoordinatesFormat', 'LatticeConstant', 'DM.NumberPulay', 'DM.MixingWeight',
                     'BandLinesScale', 'OccupationFunction', 'ElectronicTemperature', 'LongOutput', 'PAO.split_norm'],
            'SystemName': 'Siesta',
            'AtomicCoordinatesFormat': 'Ang',
            'LatticeConstant': 1.0,
            'DM.NumberPulay': 3,
            'DM.MixingWeight': 0.25,
            'BandLinesScale': 'ReciprocalLatticeVectors',
            'OccupationFunction': 'FD',
            'ElectronicTemperature': 250,
            'LongOutput': 'T',
            'PAO.split_norm': '0.16'
        }


        self.basissize = []
        self.addpara = []

        self.setallparas()

        rulefile = os.path.join(os.path.join(os.getcwd(), 'Share'), 'siesta_rules.txt')
        self.conf_rule = configparser.ConfigParser()
        self.conf_rule.read(rulefile)

        self.scf = False
        self.function = 'LDA'
        self.meshcutoff = '150'
        self.kpt1 = '0'
        self.kpt2 = '0'
        self.kpt3 = '0'
        self.electrons_accuracy = '1.d-4'
        self.method = 'diagon'
        self.metal = False
        self.spin = False
        self.restart = False

        scf_box = wx.BoxSizer(wx.HORIZONTAL)

        box = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.CheckBox(self, label='scf计算选择')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnScf)

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '系统控制')
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='SystemName:     ')
        self.text = wx.TextCtrl(self, -1, value='Siesta', size=(100, 24))
        st1_1 = wx.StaticText(self, label='系统标签')
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.text, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(st1_1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='Functional:         ')
        types1 = ['LDA', 'GGA']
        self.cb1 = wx.ComboBox(self, -1, value='', choices=types1, style=wx.CB_READONLY, size=(100, 24))
        self.cb1.Bind(wx.EVT_COMBOBOX, self.OnSelect1)
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(self.cb1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='Meshcutoff(.Ry): ')
        types2 = ['corase', 'medium', 'fine', 'ultra-fine']
        self.cb2 = wx.ComboBox(self, -1, value='', choices=types2, style=wx.CB_READONLY, size=(100, 24))
        self.cb2.Bind(wx.EVT_COMBOBOX, self.OnSelect2)
        st3_1 = wx.StaticText(self, label='截断能')
        box3.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box3.Add(self.cb2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box3.Add(st3_1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz2 = wx.StaticBoxSizer(wx.VERTICAL, self, 'K点设置')
        box4 = wx.BoxSizer(wx.HORIZONTAL)
        self.text1 = wx.TextCtrl(self, -1, value='', size=(40, 24))
        self.text2 = wx.TextCtrl(self, -1, value='', size=(40, 24))
        self.text3 = wx.TextCtrl(self, -1, value='', size=(40, 24))
        types3 = ['0', '0.5']
        self.cb3 = wx.ComboBox(self, -1, value='', choices=types3, style=wx.CB_READONLY, size=(40, 24))
        self.cb3.Bind(wx.EVT_COMBOBOX, self.OnSelect3)
        self.cb4 = wx.ComboBox(self, -1, value='', choices=types3, style=wx.CB_READONLY, size=(40, 24))
        self.cb4.Bind(wx.EVT_COMBOBOX, self.OnSelect4)
        self.cb5 = wx.ComboBox(self, -1, value='', choices=types3, style=wx.CB_READONLY, size=(40, 24))
        self.cb5.Bind(wx.EVT_COMBOBOX, self.OnSelect5)

        box4.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box4.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box4.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box4.Add(self.cb3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box4.Add(self.cb4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box4.Add(self.cb5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        sz2.Add(box4, flag=wx.ALL, border=2)

        sz1.Add(box1, flag=wx.ALL, border=2)
        sz1.Add(box2, flag=wx.ALL, border=2)
        sz1.Add(box3, flag=wx.ALL, border=2)
        sz1.Add(sz2, flag=wx.ALL, border=2)

        sz3 = wx.StaticBoxSizer(wx.VERTICAL, self, '电子自洽')
        box5 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='电子自洽精度:       ')
        types4 = ['corase', 'medium', 'fine', 'ultra-fine']
        self.cb6 = wx.ComboBox(self, -1, value='', choices=types4, style=wx.CB_READONLY, size=(100, 24))
        self.cb6.Bind(wx.EVT_COMBOBOX, self.OnSelect6)
        box5.Add(st4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box5.Add(self.cb6, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box6 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(self, label='Solution Method: ')
        types5 = ['diagon', 'OrderN']
        self.cb7 = wx.ComboBox(self, -1, value='', choices=types5, style=wx.CB_READONLY, size=(100, 24))
        self.cb7.Bind(wx.EVT_COMBOBOX, self.OnSelect7)
        box6.Add(st5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box6.Add(self.cb7, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box7 = wx.BoxSizer(wx.HORIZONTAL)
        st6 = wx.StaticText(self, label='Max steps:          ')
        self.text4 = wx.TextCtrl(self, -1, value='100', size=(100, 24))
        st6_1 = wx.StaticText(self, label='最大循环次数')
        box7.Add(st6, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box7.Add(self.text4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box7.Add(st6_1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz3.Add(box5, flag=wx.ALL, border=2)
        sz3.Add(box6, flag=wx.ALL, border=2)
        sz3.Add(box7, flag=wx.ALL, border=2)


        sz4 = wx.StaticBoxSizer(wx.VERTICAL, self, '')
        box8 = wx.BoxSizer(wx.HORIZONTAL)
        self.cbx1 = wx.CheckBox(self, label='金属')
        self.cbx1.SetValue(False)
        self.cbx1.Bind(wx.EVT_CHECKBOX, self.OnCbx1)

        self.cbx2 = wx.CheckBox(self, label='自旋')
        self.cbx2.SetValue(False)
        self.cbx2.Bind(wx.EVT_CHECKBOX, self.OnCbx2)

        self.cbx3 = wx.CheckBox(self, label='ReStart')
        self.cbx3.SetValue(False)
        self.cbx3.Bind(wx.EVT_CHECKBOX, self.OnCbx3)

        box8.Add(self.cbx1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box8.Add(self.cbx2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box8.Add(self.cbx3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        sz4.Add(box8, flag=wx.ALL, border=2)

        sz5 = wx.StaticBoxSizer(wx.VERTICAL, self, '基组设置')
        self.basislabels = ['元素', '基组']
        self.basisindex = -1
        self.basisgridrow = 3
        self.basisgrid = grid.Grid(self, -1, size=(260, 130))
        self.basisgrid.CreateGrid(self.basisgridrow, 2)
        self.basisgrid.DisableDragRowSize()
        self.basisgrid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.basisgrid.SetDefaultRowSize(26)
        self.basisgrid.SetColLabelValue(0, self.basislabels[0])
        self.basisgrid.SetColLabelValue(1, self.basislabels[1])
        self.basisgrid.SetColSize(0, 100)
        self.basisgrid.SetColSize(1, 100)
        self.basisgrid.SetRowLabelSize(40)
        self.basischoice = ['SZ', 'DZ', 'SZP', 'DZP']
        self.basisgrid.Bind(grid.EVT_GRID_CELL_CHANGED, self.OnBasisGridCellChanged)

        sz5.Add(self.basisgrid, flag=wx.ALL, border=2)

        box.Add(self.cb, flag=wx.ALL, border=2)
        box.Add(sz1, flag=wx.ALL, border=2)
        box.Add(sz3, flag=wx.ALL, border=2)
        box.Add(sz4, flag=wx.ALL, border=2)
        box.Add(sz5, flag=wx.ALL, border=2)

        sz6 = wx.StaticBoxSizer(wx.VERTICAL, self, '详细参数设置')
        box9 = wx.BoxSizer(wx.HORIZONTAL)
        add = wx.Button(self, -1, '添加')
        delete = wx.Button(self, -1, '删除')
        reset = wx.Button(self, -1, '重置')

        box9.Add(add, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box9.Add(delete, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box9.Add(reset, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        add.Bind(wx.EVT_BUTTON, self.OnAdd)
        delete.Bind(wx.EVT_BUTTON, self.OnDelete)
        reset.Bind(wx.EVT_BUTTON, self.OnReset)

        self.labels = ['参数', '值', '备注']
        self.index = -1
        self.gridrow = 3
        self.grid = grid.Grid(self, -1, size=(450, 460))
        self.grid.CreateGrid(self.gridrow, 3)
        self.grid.DisableDragRowSize()
        self.grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_RIGHT)
        self.grid.SetDefaultRowSize(26)
        self.grid.SetColLabelValue(0, self.labels[0])
        self.grid.SetColLabelValue(1, self.labels[1])
        self.grid.SetColLabelValue(2, self.labels[2])
        self.grid.SetColSize(0, 150)
        self.grid.SetColSize(1, 50)
        self.grid.SetColSize(2, 180)
        self.grid.SetRowLabelSize(40)
        self.grid.Bind(grid.EVT_GRID_CELL_CHANGED, self.OnGridCellChanged)

        sz6.Add(box9, flag=wx.ALL, border=2)
        sz6.Add(self.grid, flag=wx.ALL, border=2)

        scf_box.Add(box, flag=wx.ALL, border=2)
        scf_box.Add(sz6, flag=wx.ALL, border=2)

        self.initial()

        self.SetSizer(scf_box)
        parent.AddPage(self, 'scf')

    def setallparas(self):
        parafile = os.path.join(os.getcwd(), r'Share\siesta_paras.txt')
        self.conf_para = configparser.ConfigParser()
        self.conf_para.read(parafile)
        self.parasdict = {}
        self.paraslist = []
        self.parasdict['general'] = self.conf_para.get('general', 'sections').strip().split(', ')
        for section in self.parasdict['general']:
            self.parasdict[section] = self.conf_para.get(section, 'paras').strip().split(', ')
            for item in self.parasdict[section]:
                self.parasdict[item] = self.conf_para.get(section, item)
            self.paraslist += self.parasdict[section]

    def setbasisatom(self):
        self.symbols = list(set(self.atoms.get_chemical_symbols()))
        for i,data in enumerate(self.symbols):
            if i > 2:
                self.basisgrid.AppendRows()
            valueChoice = grid.GridCellChoiceEditor(self.basischoice)
            self.basisgrid.SetCellValue(i, 0, data)
            self.basisgrid.SetCellEditor(i, 1, valueChoice)
            self.basisgrid.SetCellValue(i, 1, self.basischoice[3])
            basisvalue = [data,self.basischoice[3]]
            self.basissize.append(basisvalue)

    def initial(self):
        self.setbasisatom()
        valueChoice = grid.GridCellChoiceEditor(self.paraslist)
        self.grid.SetCellEditor(0, 0, valueChoice)
        self.grid.SetCellEditor(1, 0, valueChoice)
        self.grid.SetCellEditor(2, 0, valueChoice)

        self.cb1.SetSelection(0)
        self.cb2.SetSelection(2)
        self.cb3.SetSelection(0)
        self.cb4.SetSelection(0)
        self.cb5.SetSelection(0)
        self.cb6.SetSelection(2)
        self.cb7.SetSelection(0)

        self.a = np.linalg.norm(self.atoms.cell[0])
        a = self.a
        kvalue = 4 * 4 / a
        if kvalue < 1:
            kvalue = 1
        elif kvalue > int(kvalue) + 0.5:
            kvalue = int(kvalue) + 1
        else:
            kvalue = int(kvalue)
        self.text1.SetValue(str(kvalue))

        self.a = np.linalg.norm(self.atoms.cell[1])
        a = self.a
        kvalue = 4 * 4 / a
        if kvalue < 1:
            kvalue = 1
        elif kvalue > int(kvalue) + 0.5:
            kvalue = int(kvalue) + 1
        else:
            kvalue = int(kvalue)
        self.text2.SetValue(str(kvalue))

        self.a = np.linalg.norm(self.atoms.cell[2])
        a = self.a
        kvalue = 4 * 4 / a
        if kvalue < 1:
            kvalue = 1
        elif kvalue > int(kvalue) + 0.5:
            kvalue = int(kvalue) + 1
        else:
            kvalue = int(kvalue)
        self.text3.SetValue(str(kvalue))

        sections = ['MeshCutoff', 'Electrons-Accuracy']
        for section in sections:
            paras = self.conf_rule.get(section, 'paras').strip().split(', ')
            for para in paras:
                value = self.conf_rule.get(section, para).strip().split(', ')[1]
                if para in self.addpara:
                    self.grid.SetCellValue(self.addpara.index(para), 1, value)
                else:
                    self.addpara.append(para)
                    self.index += 1
                    if self.index > 2:
                        self.grid.AppendRows()
                        valueChoice = grid.GridCellChoiceEditor(self.paraslist)
                        self.grid.SetCellEditor(self.index, 0, valueChoice)
                    self.grid.SetCellValue(self.index, 0, para)
                    self.grid.SetReadOnly(self.index, 0)
                    self.grid.SetCellValue(self.index, 1, value)

        for item in self.default['keys']:
            self.index += 1
            if self.index > 2:
                self.grid.AppendRows()
            self.grid.SetCellValue(self.index, 0, item)
            self.grid.SetCellValue(self.index, 1, str(self.default[item]))

    def dopararules(self, event, section):
        index = event.GetSelection()
        paras = self.conf_rule.get(section, 'paras').strip().split(', ')
        for para in paras:
            value = self.conf_rule.get(section, para).strip().split(', ')[index]
            self.grid.SetCellValue(self.addpara.index(para), 1, value)
            self.grid.SetCellTextColour(self.addpara.index(para), 1, wx.RED)

    def OnScf(self, event):
        self.scf = self.cb.GetValue()

    def OnSelect1(self, event):
        self.function = self.cb1.GetStringSelection()

    def OnSelect2(self, event):
        self.dopararules(event, 'MeshCutoff')

    def OnSelect3(self, event):
        self.kpt1 = self.cb3.GetStringSelection()

    def OnSelect4(self, event):
        self.kpt2 = self.cb4.GetStringSelection()

    def OnSelect5(self, event):
        self.kpt3 = self.cb5.GetStringSelection()

    def OnSelect6(self, event):
        self.dopararules(event,  'Electrons-Accuracy')

    def OnSelect7(self, event):
        self.method = self.cb7.GetStringSelection()

    def OnCbx1(self, event):
        self.metal = self.cbx1.GetValue()

    def OnCbx2(self, event):
        self.spin = self.cbx2.GetValue()

    def OnCbx3(self, event):
        self.restart = self.cbx3.GetValue()

    def metalkset(self):
        kvalue = 1
        a = self.a
        if self.metal:
            kvalue = 4*6/a
        else:
            kvalue = 4*4/a

        if kvalue < 1:
            kvalue = 1
        elif kvalue > int(kvalue) + 0.5:
            kvalue = int(kvalue) + 1
        else:
            kvalue = int(kvalue)

        self.text1.SetValue(str(kvalue))
        self.text2.SetValue(str(kvalue))
        self.text3.SetValue(str(kvalue))

    def OnBasisGridCellChanged(self, event):
        row = event.GetRow()
        col = event.GetCol()
        if col == 0:
            return
        self.basissize[row][1] = self.basisgrid.GetCellValue(row, 1)

    def OnGridCellChanged(self, event):
        row = event.GetRow()
        col = event.GetCol()
        if row < len(self.addpara):
            return
        if col == 0:
            value = self.grid.GetCellValue(row, 0)
            self.grid.SetCellValue(row, 1, self.parasdict[value])

    def OnAdd(self, event, key=None, value=None):
        """ 添加 """
        self.index += 1
        if self.index > 2:
            self.grid.AppendRows()
            valueChoice = grid.GridCellChoiceEditor(self.paraslist)
            self.grid.SetCellEditor(self.index, 0, valueChoice)
        if not key:
            gridkey = self.paraslist[0]
            gridvalue = self.parasdict[gridkey]
        else:
            gridkey = key
            gridvalue = value

        self.grid.SetCellValue(self.index, 0, gridkey)
        self.grid.SetCellValue(self.index, 1, gridvalue)

    def OnDelete(self, event):
        """ 删除 """
        if self.index < len(self.addpara):
            return False
        self.grid.DeleteRows(self.index)
        self.index -= 1
        return True

    def OnReset(self, event):
        state = self.OnDelete(event)
        while state:
            state = self.OnDelete(event)
        for item in self.default['keys']:
            self.index += 1
            if self.index > 2:
                self.grid.AppendRows()
                valueChoice = grid.GridCellChoiceEditor(self.paraslist)
                self.grid.SetCellEditor(self.index, 0, valueChoice)
            self.grid.SetCellValue(self.index, 0, item)
            self.grid.SetCellValue(self.index, 1, str(self.default[item]))

    def GetParas(self):
        fdf = {}
        for i in range(self.index + 1):
            item = str(self.grid.GetCellValue(i, 0))
            value = str(self.grid.GetCellValue(i, 1))
            fdf[item] = value

        fdf['SystemLabel'] = str(self.text.GetValue())
        fdf['XC.functional'] = str(self.cb1.GetStringSelection())
        if self.spin:
            fdf['SpinPolarized'] = True
        fdf['SolutionMethod'] = str(self.cb7.GetStringSelection())
        fdf['MaxSCFIterations'] = str(self.text4.GetValue())
        fdf.update(self.getbasissizes())
        return fdf

    def GetKpts(self):
        return (int(self.text1.GetValue()), int(self.text2.GetValue()), int(self.text3.GetValue()))

    def getbasissizes(self):
        basissizes = {}
        basislist = []
        for item in self.basissize:
            basisstr = ''
            basisstr += item[0] + ' ' + item[1]
            basislist.append(basisstr)
        basissizes['PAO.BasisSizes'] = basislist
        return basissizes

    def doReConfig(self,filepath):
        conf = configparser.RawConfigParser()
        conf.read(filepath)
        ###
        if conf.get('SCF','select') == 'True':
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)
        ###
        if conf.get('SCF','ismetal') == 'True':
            self.cbx1.SetValue(True)
        else:
            self.cbx1.SetValue(False)
        ###
        if conf.get('SCF','isspin') == 'True':
            self.cbx2.SetValue(True)
        else:
            self.cbx2.SetValue(False)
        ###
        if conf.get('SCF','restart') == 'True':
            self.cbx3.SetValue(True)
        else:
            self.cbx3.SetValue(False)
        ###
        self.text.SetValue(conf.get('SCF','systemlabel'))
        self.cb1.SetStringSelection(conf.get('SCF','xcfunctional'))
        self.cb2.SetStringSelection(conf.get('SCF','meshcutoff'))
        ###
        self.text1.SetValue(conf.get('SCF','kpts1'))
        self.text2.SetValue(conf.get('SCF','kpts2'))
        self.text3.SetValue(conf.get('SCF','kpts3'))
        self.cb3.SetStringSelection(conf.get('SCF','kpts4'))
        self.cb4.SetStringSelection(conf.get('SCF','kpts5'))
        self.cb5.SetStringSelection(conf.get('SCF','kpts6'))
        ###

        self.cb6.SetStringSelection(conf.get('SCF','dmtolerance'))
        self.text4.SetValue(conf.get('SCF','MaxSCFIterations'))
        self.cb7.SetStringSelection(conf.get('SCF','solutionmethod'))
        if conf.has_option('SCF','basisstr'):
            basisvalue = conf.get('SCF','basisstr').split(', ')
            for i,item in enumerate(basisvalue):
                self.basisgrid.SetCellValue(i, 1, item)
        ###grid
        gridvalue = conf.get('SCF','gridstr').split(', ')
        state = self.delChoice()
        while state:
            state = self.delChoice()
        for i,item in enumerate(gridvalue):
            item = item.split('*')
            if i >= len(self.addpara):
                self.index += 1
                self.grid.AppendRows()
                valueChoice = grid.GridCellChoiceEditor(self.paraslist)
                self.grid.SetCellEditor(self.index, 0, valueChoice)
                self.grid.SetCellValue(self.index,0,item[0])
                self.grid.SetCellValue(self.index,1,item[1])
            else:
                self.grid.SetCellValue(i,1,item[1])

    def delChoice(self):
        if self.index < len(self.addpara):
            return False
        self.grid.DeleteRows(self.index)
        self.index -= 1
        return True

    def SaveConfig(self,conf):
        conf.add_section('SCF')
        ###
        conf.set('SCF','select',str(self.cb.GetValue()))
        ###
        conf.set('SCF','systemlabel',self.text.GetValue())
        conf.set('SCF','xcfunctional',self.cb1.GetStringSelection())
        conf.set('SCF','meshcutoff',self.cb2.GetStringSelection())
        ###
        conf.set('SCF','kpts1',self.text1.GetValue())
        conf.set('SCF','kpts2',self.text2.GetValue())
        conf.set('SCF','kpts3',self.text3.GetValue())
        conf.set('SCF','kpts4',self.cb3.GetStringSelection())
        conf.set('SCF','kpts5',self.cb4.GetStringSelection())
        conf.set('SCF','kpts6',self.cb5.GetStringSelection())
        ###
        conf.set('SCF','ismetal',str(self.cbx1.GetValue()))
        conf.set('SCF','isspin',str(self.cbx2.GetValue()))
        conf.set('SCF','restart',str(self.cbx3.GetValue()))

        ###
        conf.set('SCF','dmtolerance',self.cb6.GetStringSelection())
        conf.set('SCF','MaxSCFIterations',self.text4.GetValue())
        conf.set('SCF','solutionmethod',self.cb7.GetStringSelection())

        basisstr = ''
        for i in range(len(self.symbols)):
            basisstr += str(self.basisgrid.GetCellValue(i,1)) + ', '
        basisstr = basisstr.strip(', ')
        conf.set('SCF','basisstr',basisstr)
        ###grid
        gridstr = ''
        for i in range(self.index+1):
            gridstr += self.grid.GetCellValue(i,0)
            gridstr += '*'
            gridstr += self.grid.GetCellValue(i,1)
            gridstr += ', '
        gridstr = gridstr.strip(', ')
        conf.set('SCF','gridstr',gridstr)





