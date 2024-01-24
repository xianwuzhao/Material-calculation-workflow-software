import wx
import os
import wx.grid as grid
import numpy as np
import configparser
import ase.dft.kpoints as dftkpoints

class band(wx.Panel):
    """ BAND设置 """

    def __init__(self, parent, id, atoms):
        wx.Panel.__init__(self, parent, id)

        self.images = os.path.join(os.getcwd(), r'Share\kbands_jpg')

        self.atoms = atoms

        band_box = wx.BoxSizer(wx.HORIZONTAL)
        self.band = False

        box = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.CheckBox(self, label='band计算选择')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnBand)

        sz = wx.StaticBoxSizer(wx.VERTICAL, self, '参数设置')

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='晶格类型: ')
        self.types = ['1D-line', 'fcc', 'cubic', 'tetragonal', '2D-hexagonal', 'bcc', 'orthorhombic', 'hexagonal', '2D-square']
        self.cb1 = wx.ComboBox(self, -1, value='', choices=self.types, style=wx.CB_READONLY)
        self.cb1.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box1.Add(self.cb1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        add = wx.Button(self, -1, '添加', size=(50,26))
        delete = wx.Button(self, -1, '删除', size=(50,26))
        cal = wx.Button(self, -1, '计算', size=(50,26))
        self.text = wx.TextCtrl(self, -1, value='50', size=(50, 26))
        st2 = wx.StaticText(self, label='K点数')

        box2.Add(add, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(delete, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(cal, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(self.text, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND | wx.ALL, border=3)

        add.Bind(wx.EVT_BUTTON, self.OnAdd)
        delete.Bind(wx.EVT_BUTTON, self.OnDelete)
        cal.Bind(wx.EVT_BUTTON, self.OnCal)

        self.labels = ['取点数', '高对称点']
        self.index = -1
        self.gridrow = 6
        self.grid = grid.Grid(self, -1, size=(270, 350))
        self.grid.CreateGrid(self.gridrow, 2)
        self.grid.DisableDragRowSize()
        self.grid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_LEFT)
        self.grid.SetDefaultRowSize(self.grid.GetDefaultRowSize()*1.2)
        self.grid.SetColLabelValue(0, self.labels[0])
        self.grid.SetColLabelValue(1, self.labels[1])
        self.grid.SetColSize(0, 50)
        self.grid.SetColSize(1, 150)
        self.grid.SetRowLabelSize(50)
        self.grid.Bind(grid.EVT_GRID_CELL_CHANGED, self.OnGridCellChanged)


        sz.Add(box1, flag=wx.ALL, border=2)
        sz.Add(box2, flag=wx.ALL, border=2)
        sz.Add(self.grid, flag=wx.ALL, border=2)

        box.Add(self.cb,flag=wx.ALL, border=2)
        box.Add(sz, flag=wx.ALL, border=2)

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '向量显示')
        image_path = os.path.join(self.images, r'default.jpg')
        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY).Rescale(width=400, height=400)
        temp = image.ConvertToBitmap()
        self.sbp = wx.StaticBitmap(self, -1, bitmap=temp, size=(400, 400))

        sz1.Add(self.sbp, flag=wx.ALL, border=2)

        band_box.Add(box, flag=wx.ALL, border=2)
        band_box.Add(sz1, flag=wx.ALL, border=2)

        self.SetSizer(band_box)
        parent.AddPage(self, 'band')

    def OnBand(self, event):
        self.band = self.cb.GetValue()

    def OnSelect(self, event):
        # 清空grid
        while self.gridrow > 1:
            self.grid.DeleteRows(self.gridrow-1)
            self.gridrow -= 1
        self.line = []

        # 取得选择晶格类型及其数据
        k_name =  self.cb1.GetStringSelection()
        image_path = os.path.join(self.images, ''.join([k_name,'.jpg']))
        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY).Rescale(width=400, height=400)
        temp = image.ConvertToBitmap()
        self.sbp.SetBitmap(temp)
        data = ibz_points.get(k_name)

        # 取得可选线段
        self.choices = []
        linekeys = data['keys']

        for lines in linekeys:
            pointstr = ''
            for item in data[lines]:
                pointstr += str(item) + ' '
            self.choices.append(pointstr + lines)

        # 取得初始化，线段排列
        keys = data.get('linemode')
        linenum = len(keys)

        # 初始化grid
        while self.gridrow < linenum:
            self.grid.AppendRows()
            self.gridrow += 1

        self.index = linenum - 1
        for index, item in enumerate(keys):
            valueChoice = grid.GridCellChoiceEditor(self.choices)
            self.grid.SetCellEditor(index, 1, valueChoice)
            for valuestr in self.choices:
                if valuestr.endswith(item):
                    self.grid.SetCellValue(index, 1, valuestr)
            self.line.append('line'+str(index))
        self.OnCal(event)

    def GetBandpoints(self):
        key = self.cb1.GetStringSelection()
        data = ibz_points.get(key)
        bandpoint = []
        for index in range(self.index+1):
            item = self.grid.GetCellValue(index,1)
            item = item.strip().split(' ')[-1]
            bandpoint.append(data[item])

        return bandpoint


    def OnAdd(self, event):
        """ 添加 """
        if self.index + 1 >= self.gridrow:
            self.grid.AppendRows()
            self.gridrow += 1
        self.index += 1
        valueChoice = grid.GridCellChoiceEditor(self.choices)
        self.grid.SetCellEditor(self.index, 1, valueChoice)
        self.grid.SetCellValue(self.index, 0, '')
        self.grid.SetCellValue(self.index, 1, self.choices[0])

        self.line.append('line'+str(self.index))

    def OnDelete(self, event):
        """ 删除 """
        if self.index < 0:
            return
        self.line.pop()
        if self.index > 5:
            self.grid.DeleteRows(self.index)
            self.gridrow -= 1
            self.index -= 1
        else:
            self.grid.SetCellValue(self.index, 0, '')
            nullchoice = []
            valueChoice = grid.GridCellChoiceEditor(nullchoice)
            self.grid.SetCellEditor(self.index, 1, valueChoice)
            self.grid.SetCellValue(self.index, 1, '')
            self.index -= 1

    def OnCal(self, event):
        """ 计算 """
        cell = self.atoms.cell
        points = self.GetBandpoints()
        points = np.asarray(points)
        dists = points[1:] - points[:-1]
        lengths = [np.linalg.norm(d) for d in dftkpoints.kpoint_convert(cell, skpts_kc=dists)]
        length = sum(lengths)
        numtotal = int(self.text.GetValue())
        numsub = 0
        self.grid.SetCellValue(0, 0, '1')
        for index, p in enumerate(lengths):
            if index + 1 == self.index:
                self.grid.SetCellValue(index + 1, 0, str(numtotal - numsub))
                break
            number = int(p / length * numtotal)
            numsub += number
            self.grid.SetCellValue(index + 1, 0, str(number))

    def OnGridCellChanged(self, event):
        pass

    def Getbandstr(self):
        bandstr = ''
        for i in range(self.index+1):
            bandstr += self.grid.GetCellValue(i, 0)
            bandstr += ' '
            bandstr += self.grid.GetCellValue(i, 1)
            bandstr += '\n'

        return bandstr

    def doReConfig(self, filepath):
        self.line = []
        conf = configparser.RawConfigParser()
        conf.read(filepath)
        ###
        if conf.get('BAND', 'select') == 'True':
            self.cb.SetValue(True)
        else:
            self.cb.SetValue(False)
        ###
        self.text.SetValue(conf.get('BAND', 'kbandnum'))
        ###
        typeindex = int(conf.get('BAND', 'type'))
        self.cb1.SetSelection(typeindex)
        key = self.cb1.GetStringSelection()
        image_path = os.path.join(self.images, ''.join([key, '.jpg']))
        image = wx.Image(image_path, wx.BITMAP_TYPE_ANY).Rescale(width=400, height=400)
        temp = image.ConvertToBitmap()
        self.sbp.SetBitmap(temp)
        ###
        if not typeindex == -1:
            self.choices = self.GetCellChoices(filepath)
        if conf.has_option('BAND', 'linetotal'):
            additionpara = conf.get('BAND', 'linetotal').split('%')
            for item in additionpara:
                item = conf.get('BAND', item)
                pointnum = item.split('%')[0]
                pointname = item.split('%')[1]
                self.addChoice(pointnum, pointname)

    def GetCellChoices(self, filepath):
        typekeys = self.types
        conf = configparser.ConfigParser()
        conf.read(filepath)
        typekey = typekeys[int(conf.get('BAND', 'type'))]
        data = ibz_points.get(typekey)

        ##取得可选线段
        cellchoices = []
        linekeys = data['keys']

        for lines in linekeys:
            pointstr = ''
            for item in data[lines]:
                pointstr += str(item) + ' '
            cellchoices.append(pointstr + lines)
        return cellchoices

    def addChoice(self, num, name):
        if self.index + 1 >= self.gridrow:
            self.grid.AppendRows()
            self.gridrow += 1
        self.index += 1
        valueChoice = wx.grid.GridCellChoiceEditor(self.choices)
        self.grid.SetCellEditor(self.index, 1, valueChoice)
        self.grid.SetCellValue(self.index, 0, num)
        self.grid.SetCellValue(self.index, 1, name)

        self.line.append('line' + str(self.index))

    def SaveConfig(self,conf):
        conf.add_section('BAND')
        ###
        conf.set('BAND','select',str(self.cb.GetValue()))
        conf.set('BAND','type',str(self.cb1.GetSelection()))
        conf.set('BAND','kbandnum',self.text.GetValue())
        ###
        for i,item in enumerate(self.line):
            itemstr = ''
            itemstr += self.grid.GetCellValue(i,0)
            itemstr += '%'
            itemstr += self.grid.GetCellValue(i,1)
            conf.set('BAND',item,itemstr)

        if self.line:
            linetotal = ''
            for item in self.line:
                linetotal += item
                linetotal += ' '
            linetotal = linetotal.strip().replace(' ','%')
            conf.set('BAND','linetotal',linetotal)



############## 晶格类型 ###########
ibz_points = {'1D-line': {'keys': ['Gamma', 'X', 'Y', 'Z'],
                          'linemode': ['Gamma', 'Z'],
                          'Gamma': [0, 0, 0],
                          'X': [0.5, 0, 0],
                          'Y': [0, 0.5, 0],
                          'Z': [0, 0, 0.5]},

              '2D-hexagonal': {'keys': ['Gamma', 'K', 'M'],
                               'linemode': ['K', 'Gamma', 'M', 'K'],
                               'Gamma': [0, 0, 0],
                               'K': [-0.33333, 0.66667, 0],
                               'M': [0, 0.5, 0]},

              '2D-square': {'keys': ['Gamma', 'X', 'M'],
                            'linemode': ['M', 'Gamma', 'X', 'M'],
                            'Gamma': [0, 0, 0],
                            'X': [0.5, 0, 0],
                            'M': [0.5, 0.5, 0]},

              'cubic': {'keys': ['Gamma', 'X', 'R', 'M'],
                        'linemode': ['X', 'R', 'M', 'Gamma', 'R'],
                        'Gamma': [0, 0, 0],
                        'X': [0, 0, 0.5],
                        'R': [0.5, 0.5, 0.5],
                        'M': [0, 0.5, 0.5]},

              'fcc': {'keys': ['Gamma', 'X', 'W', 'K', 'U', 'L'],
                      'linemode': ['W', 'L', 'Gamma', 'X', 'W', 'K'],
                      'Gamma': [0, 0, 0],
                      'X': [0.5, 0, 0.5],
                      'W': [0.5, 0.25, 0.75],
                      'K': [0.375, 0.375, 0.75],
                      'U': [0.625, 0.25, 0.625],
                      'L': [0.5, 0.5, 0.5]},

              'bcc': {'keys': ['Gamma', 'H', 'N', 'P'],
                      'linemode': ['Gamma', 'H', 'N', 'P', 'Gamma', 'N'],
                      'Gamma': [0, 0, 0],
                      'H': [0.5, -0.5, 0.5],
                      'N': [0, 0, 0.5],
                      'P': [0.25, 0.25, 0.25]},
              'hexagonal':
                  {'keys': ['Gamma', 'M', 'K', 'A', 'L', 'H'],
                   'linemode': ['Gamma', 'A', 'H', 'K', 'Gamma', 'M', 'L', 'H'],
                   'Gamma': [0, 0, 0],
                   'M': [0, 0.5, 0],
                   'K': [-0.33333, 0.33333, 0],
                   'A': [0, 0, 0.5],
                   'L': [0, 0.5, 0.5],
                   'H': [-0.33333, 0.33333, 0.5]},
              'tetragonal':
                  {'keys': ['Gamma', 'X', 'M', 'Z', 'R', 'A'],
                   'linemode': ['Z', 'A', 'M', 'Gamma', 'Z', 'R', 'X', 'Gamma'],
                   'Gamma': [0, 0, 0],
                   'X': [0.5, 0, 0],
                   'M': [0.5, 0.5, 0],
                   'Z': [0, 0, 0.5],
                   'R': [0.5, 0, 0.5],
                   'A': [0.5, 0.5, 0.5]},
              'orthorhombic':
                  {'keys': ['Gamma', 'R', 'S', 'T', 'U', 'X', 'Y', 'Z'],
                   'linemode': ['Gamma', 'Z', 'T', 'Y', 'S', 'X', 'U', 'R'],
                   'Gamma': [0, 0, 0],
                   'R': [0.5, 0.5, 0.5],
                   'S': [0.5, 0.5, 0],
                   'T': [0, 0.5, 0.5],
                   'U': [0.5, 0, 0.5],
                   'X': [0.5, 0, 0],
                   'Y': [0, 0.5, 0],
                   'Z': [0, 0, 0.5]},
              }