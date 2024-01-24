import wx
import os

class ModelProcessService:

    def __init__(self,app):
        self.frame = app.frame
        self.app = app
        self.project = app.project
        self.log = app.log

        self.frame.get_menu_bar().Insert(3, self.add_module_menu(self.frame), '模型处理')
        self.log.Info('插件 model process service 加载成功！')

        self.frame.update()

    def add_module_menu(self, parent):
        """ 模型处理 """
        module_menu = wx.Menu()

        model_pro = module_menu.Append(-1, '模型处理')

        parent.Bind(wx.EVT_MENU, self.OnModel, model_pro)

        return module_menu

    def OnModel(self, event):
        """ 模型处理配置 """
        configdlg = ModelPanel(self.frame, self.app)
        if configdlg.ShowModal() == wx.ID_OK:
            configdlg.CenterOnScreen()
        else:
            pass

class ModelPanel(wx.Dialog):
    """ 模型构建界面 """

    def __init__(self, parent, app):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)

        self.app = app
        self.log = app.log
        self.path = self.app.project.get_dir()

        self.InitUI()
        nb = wx.Notebook(self, -1)
        self.sup = SuperCell(nb, -1, self.path)
        self.ads = Adsorb(nb, -1, self.path)
        self.rep = Replace(nb, -1, self.path)
        self.de = Defect(nb, -1, self.path)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnok = wx.Button(self, wx.ID_OK, '确定')
        btncancel = wx.Button(self, wx.ID_CANCEL, '取消')
        btnsizer.Add(btnok, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        btnsizer.Add(btncancel, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
        btnok.Bind(wx.EVT_BUTTON, self.OnOk)
        self.SetSizer(sizer)
        self.Layout()
        self.Fit()


    def InitUI(self):
        """ 初始化主界面 """
        icon = os.getcwd() + '\\icon\\MIDIS.ico'
        icon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        icon.SetHeight(18)
        icon.SetWidth(18)
        self.SetIcon(icon)
        self.SetTitle(title='模型构建')
        self.Centre()

    def OnOk(self, event):
        item = self.app.project.tree.GetSelection()
        path = self.app.project.tree.GetItemData(item)

        self.sup.writesupercell(path)
        self.ads.writeadsorb(path)
        self.rep.writereplace(path)
        self.de.writedefect(path)
        self.app.project.update_tree()

        self.Destroy()


class SuperCell(wx.Panel):
    """ 扩胞设置 """

    def __init__(self, parent, id, path):
        wx.Panel.__init__(self, parent, id)

        self.supercell = False

        supercell_box = wx.BoxSizer(wx.VERTICAL)
        self.cb1 = wx.CheckBox(self, label='是否进行扩胞')
        self.cb1.SetValue(False)
        self.cb1.Bind(wx.EVT_CHECKBOX, self.OnSuperCell)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='x方向  ')
        self.text1 = wx.TextCtrl(self, -1, value='')
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='y方向  ')
        self.text2 = wx.TextCtrl(self, -1, value='')
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box2.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='z方向  ')
        self.text3 = wx.TextCtrl(self, -1, value='')
        box3.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box3.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        supercell_box.Add(self.cb1, flag=wx.ALL, border=5)
        supercell_box.Add(box1, flag=wx.ALL, border=5)
        supercell_box.Add(box2, flag=wx.ALL, border=5)
        supercell_box.Add(box3, flag=wx.ALL, border=5)

        self.SetSizer(supercell_box)
        parent.AddPage(self, '扩胞')

    def OnSuperCell(self, event):
        self.supercell = self.cb1.GetValue()

    def writesupercell(self, path):

        if self.supercell:

            def cell(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        folder_path = os.path.dirname(path1)
                        folder_name = os.path.basename(folder_path)
                        if i == 'POSCAR' and folder_name not in ['relax', 'scf', 'band', 'dos']:
                            x = int(self.text1.GetValue())
                            y = int(self.text2.GetValue())
                            z = int(self.text3.GetValue())
                            new_folder_path = os.path.join(os.path.dirname(folder_path), '{0}-{1}{2}{3}'.format(folder_name, x, y, z))
                            if not os.path.exists(new_folder_path):
                                os.mkdir(new_folder_path)
                            out_path = os.path.join(new_folder_path, 'POSCAR')

                            with open(path1, 'r+') as in_file:
                                lines = in_file.readlines()
                                numline = len(lines)

                                with open(out_path, 'w') as out_file:
                                    out_file.write(lines[0].strip())
                                    out_file.write('\n')
                                    out_file.write(str(round(float(lines[1].strip()), 1)))
                                    out_file.write('\n')

                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[2].strip().split()[0]) * x, '.9f')))
                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[2].strip().split()[1]) * x, '.9f')))
                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[2].strip().split()[2]) * x, '.9f')))
                                    out_file.write('\n')
                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[3].strip().split()[0]) * y, '.9f')))
                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[3].strip().split()[1]) * y, '.9f')))
                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[3].strip().split()[2]) * y, '.9f')))
                                    out_file.write('\n')
                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[4].strip().split()[0]) * z, '.9f')))
                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[4].strip().split()[1]) * z, '.9f')))
                                    out_file.write('      ')
                                    out_file.write(str(format(float(lines[4].strip().split()[2]) * z, '.9f')))
                                    out_file.write('\n')

                                    out_file.write('   ')
                                    out_file.write(lines[5].strip())
                                    out_file.write('\n')
                                    out_file.write('   ')
                                    numle = len(lines[6].strip().split())
                                    for i in range(numle):
                                        out_file.write(str(int(lines[6].strip().split()[i]) * x * y * z))
                                        out_file.write('   ')
                                    out_file.write('\n')

                                    out_file.write(lines[7].strip())
                                    out_file.write('\n')

                                    for j in range(8, numline):
                                        L = lines[j].strip().split()
                                        L[0] = float(L[0])
                                        L[1] = float(L[1])
                                        L[2] = float(L[2])
                                        for m in range(x):
                                            for n in range(y):
                                                for k in range(z):
                                                    out_file.write('     ')
                                                    out_file.write(str(format((L[0] + m) / x, '.9f')))
                                                    out_file.write('     ')
                                                    out_file.write(str(format((L[1] + n) / y, '.9f')))
                                                    out_file.write('     ')
                                                    out_file.write(str(format((L[2] + k) / z, '.9f')))
                                                    out_file.write('\n')

                    else:
                        cell(path1)

            cell(path)


class Adsorb(wx.Panel):
    """ 吸附设置 """

    def __init__(self, parent, id, path):
        wx.Panel.__init__(self, parent, id)

        self.adsorb = False

        adsorb_box = wx.BoxSizer(wx.VERTICAL)
        self.cb1 = wx.CheckBox(self, label='是否进行吸附')
        self.cb1.SetValue(False)
        self.cb1.Bind(wx.EVT_CHECKBOX, self.OnAdsorb)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='吸附原子   ')
        self.text1 = wx.TextCtrl(self, -1, value='')
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='吸附位置   ')
        self.text2 = wx.TextCtrl(self, -1, value='')
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box2.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='被吸附原子  ')
        self.text3 = wx.TextCtrl(self, -1, value='H')
        box3.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box3.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        adsorb_box.Add(self.cb1, flag=wx.ALL, border=5)
        adsorb_box.Add(box1, flag=wx.ALL, border=5)
        adsorb_box.Add(box2, flag=wx.ALL, border=5)
        adsorb_box.Add(box3, flag=wx.ALL, border=5)

        self.SetSizer(adsorb_box)
        parent.AddPage(self, '吸附')


    def OnAdsorb(self, event):
        self.adsorb = self.cb1.GetValue()

    def writeadsorb(self, path):
        if self.adsorb:
            def ads(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        folder_path = os.path.dirname(path1)
                        folder_name = os.path.basename(folder_path)
                        if i == 'POSCAR' and folder_name not in ['relax', 'scf', 'band', 'dos']:
                            atom = self.text1.GetValue()
                            num = int(self.text2.GetValue())
                            element = self.text3.GetValue()
                            new_folder_path = os.path.join(os.path.dirname(folder_path),
                                                           '{0}-{1}'.format(folder_name, element))
                            if not os.path.exists(new_folder_path):
                                os.mkdir(new_folder_path)
                            out_path = os.path.join(new_folder_path, 'POSCAR')

                            with open(path1, 'r+') as in_file:
                                lines = in_file.readlines()
                                numline = len(lines)

                                with open(out_path, 'w') as out_file:
                                    for i in range(5):
                                        out_file.write(lines[i].strip('\n'))
                                        out_file.write('\n')

                                    for i in lines[5].strip().split():
                                        if atom == i:
                                            post = lines[5].strip().split().index(i)

                                    out_file.write(lines[5].strip('\n'))
                                    out_file.write('   ' + element)
                                    out_file.write('\n')
                                    numle = lines[6].strip().split()
                                    n = 0
                                    for i in range(post):
                                        n += int(numle[i])
                                    n += int(int(numle[post]) / 2) - 5

                                    out_file.write(lines[6].strip('\n'))
                                    out_file.write('   ' + str(1))
                                    out_file.write('\n')

                                    out_file.write(lines[7].strip('\n'))
                                    out_file.write('\n')

                                    for i in range(8, numline):
                                        out_file.write(lines[i].strip('\n'))
                                        out_file.write('\n')

                                    L = lines[n + 8].strip().split()
                                    L[2] = format(float(L[2]) + 1 / 25, '.9f')
                                    out_file.write('     ')
                                    for i in L:
                                        out_file.write(str(i))
                                        out_file.write('     ')

                                    out_file.write('\n')

                    else:
                        ads(path1)
            ads(path)


class Replace(wx.Panel):
    """ 替换设置 """

    def __init__(self, parent, id, path):
        wx.Panel.__init__(self, parent, id)

        self.replace = False

        replace_box = wx.BoxSizer(wx.VERTICAL)
        self.cb1 = wx.CheckBox(self, label='是否进行掺杂')
        self.cb1.SetValue(False)
        self.cb1.Bind(wx.EVT_CHECKBOX, self.OnReplace)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='被掺杂原子  ')
        self.text1 = wx.TextCtrl(self, -1, value='')
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='掺杂位置   ')
        self.text2 = wx.TextCtrl(self, -1, value='')
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box2.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='掺杂原子   ')
        self.text3 = wx.TextCtrl(self, -1, value='H')
        box3.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box3.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        replace_box.Add(self.cb1, flag=wx.ALL, border=5)
        replace_box.Add(box1, flag=wx.ALL, border=5)
        replace_box.Add(box2, flag=wx.ALL, border=5)
        replace_box.Add(box3, flag=wx.ALL, border=5)

        self.SetSizer(replace_box)
        parent.AddPage(self, '掺杂')


    def OnReplace(self, event):
        self.replace = self.cb1.GetValue()

    def writereplace(self, path):
        if self.replace:
            def rep(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        folder_path = os.path.dirname(path1)
                        folder_name = os.path.basename(folder_path)
                        if i == 'POSCAR' and folder_name not in ['relax', 'scf', 'band', 'dos']:
                            atom = self.text1.GetValue()
                            port = int(self.text2.GetValue())
                            element = self.text3.GetValue()
                            new_folder_path = os.path.join(os.path.dirname(folder_path),
                                                           '{0}-{1}-{2}'.format(folder_name, atom, element))
                            if not os.path.exists(new_folder_path):
                                os.mkdir(new_folder_path)
                            out_path = os.path.join(new_folder_path, 'POSCAR')
                            post = 0

                            with open(path1, 'r+') as in_file:
                                lines = in_file.readlines()
                                numline = len(lines)

                                with open(out_path, 'w') as out_file:
                                    for i in range(5):
                                        out_file.write(lines[i].strip('\n'))
                                        out_file.write('\n')

                                    for i in lines[5].strip().split():
                                        if atom == i:
                                            post = lines[5].strip().split().index(i)

                                    out_file.write(lines[5].strip('\n'))
                                    out_file.write('   ' + element)
                                    out_file.write('\n')
                                    numle = lines[6].strip().split()
                                    n = 0
                                    for i in range(post):
                                        n += int(numle[i])
                                    n += port

                                    out_file.write('   ')
                                    for i in range(len(numle)):
                                        if i == post:
                                            a = str(int(numle[i]) - 1)
                                            out_file.write(a)
                                            out_file.write('   ')
                                        else:
                                            out_file.write(numle[i])
                                            out_file.write('   ')

                                    out_file.write(str(1))
                                    out_file.write('\n')

                                    out_file.write(lines[7].strip('\n'))
                                    out_file.write('\n')

                                    for i in range(8, 8 + n):
                                        out_file.write(lines[i].strip('\n'))
                                        out_file.write('\n')

                                    for i in range(8 + n + 1, numline):
                                        out_file.write(lines[i].strip('\n'))
                                        out_file.write('\n')

                                    out_file.write(lines[8 + n].strip('\n'))
                                    out_file.write('\n')

                    else:
                        rep(path1)

            rep(path)


class Defect(wx.Panel):
    """ 缺陷设置 """

    def __init__(self, parent, id, path):
        wx.Panel.__init__(self, parent, id)

        self.defect = False

        defect_box = wx.BoxSizer(wx.VERTICAL)
        self.cb1 = wx.CheckBox(self, label='是否进行缺陷')
        self.cb1.SetValue(False)
        self.cb1.Bind(wx.EVT_CHECKBOX, self.OnDefect)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='缺陷原子  ')
        self.text1 = wx.TextCtrl(self, -1, value='')
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='缺陷位置  ')
        self.text2 = wx.TextCtrl(self, -1, value='')
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box2.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        defect_box.Add(self.cb1, flag=wx.ALL, border=5)
        defect_box.Add(box1, flag=wx.ALL, border=5)
        defect_box.Add(box2, flag=wx.ALL, border=5)

        self.SetSizer(defect_box)
        parent.AddPage(self, '缺陷')

    def OnDefect(self, event):
        self.defect = self.cb1.GetValue()

    def writedefect(self, path):
        if self.defect:
            def det(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        folder_path = os.path.dirname(path1)
                        folder_name = os.path.basename(folder_path)
                        if i == 'POSCAR' and folder_name not in ['relax', 'scf', 'band', 'dos']:
                            atom = self.text1.GetValue()
                            port = int(self.text2.GetValue())
                            new_folder_path = os.path.join(os.path.dirname(folder_path),
                                                           '{0}-{1}-{2}'.format(folder_name, atom, port))
                            if not os.path.exists(new_folder_path):
                                os.mkdir(new_folder_path)
                            out_path = os.path.join(new_folder_path, 'POSCAR')
                            post = 0

                            with open(path1, 'r+') as in_file:
                                lines = in_file.readlines()
                                numline = len(lines)

                                with open(out_path, 'w') as out_file:
                                    for i in range(5):
                                        out_file.write(lines[i].strip('\n'))
                                        out_file.write('\n')

                                    for i in lines[5].strip().split():
                                        if atom == i:
                                            post = lines[5].strip().split().index(i)

                                    out_file.write(lines[5].strip('\n'))
                                    out_file.write('\n')
                                    numle = lines[6].strip().split()
                                    n = 0
                                    for i in range(post):
                                        n += int(numle[i])
                                    n += port

                                    out_file.write('   ')
                                    for i in range(len(numle)):
                                        if i == post:
                                            a = str(int(numle[i]) - 1)
                                            out_file.write(a)
                                            out_file.write('   ')
                                        else:
                                            out_file.write(numle[i])
                                            out_file.write('   ')

                                    out_file.write('\n')

                                    out_file.write(lines[7].strip('\n'))
                                    out_file.write('\n')

                                    for i in range(8, 8 + n):
                                        out_file.write(lines[i].strip('\n'))
                                        out_file.write('\n')

                                    for i in range(8 + n + 1, numline):
                                        out_file.write(lines[i].strip('\n'))
                                        out_file.write('\n')
                    else:
                        det(path1)

            det(path)


def start():
    app = wx.GetApp()
    model = ModelProcessService(app)
    return model