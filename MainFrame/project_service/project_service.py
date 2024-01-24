import wx
import wx.aui as aui
import os
import pathlib
import shutil
import configparser

from MainFrame.util_file import is_structure_file, is_edit_file, is_picture_file, is_cfg_file
from Plugin.siesta_vasp_service.siesta_vasp_service import SiestaConfig
from Plugin.ase_MIDIS import cif22xsf, view_model
from Plugin.cif2pos import ciftoposcar



class ProjectService:
    """ 工程区 """

    def __init__(self, parent, project_dir=''):

        self.frame = parent
        self.project_dir = project_dir

        self.left_panel = wx.Panel(self.frame, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
        self.set_project_box()

    def set_app(self, app):
        self.app = app
        self.log = app.log
        self.editor = app.editor

        self.frame.get_menu_bar().Insert(2, self.add_project_menu(self.frame), '工程')
        self.frame.get_mgr().AddPane(self.left_panel, aui.AuiPaneInfo().
                                     Name('project').Caption('工程区').BestSize((240, -1)).
                                     CaptionVisible(False).Left().Layer(1).Position(0))

        self.frame.update()

        self.f_history_dirs = os.path.join(self.app.dir, r'Share\history_dirs.ini')
        self.history_dirs = self.set_history_dirs(self.f_history_dirs, self.combox)

        if self.history_dirs:
            self.project_dir = self.history_dirs[-1]
            self.update_tree()

    def set_project_box(self):
        """ 设置工程区框架 """

        # 历史工程框
        self.combox = wx.ComboBox(self.left_panel, -1, value='', style=wx.CB_DROPDOWN)
        self.combox.Bind(wx.EVT_COMBOBOX, self.OnHistoryPathSelect)

        # 压缩、展开按钮
        self.fold = wx.BitmapButton(self.left_panel, -1, bitmap=wx.Bitmap('./icon/fold.ico'))
        self.unfold = wx.BitmapButton(self.left_panel, -1, bitmap=wx.Bitmap('./icon/unfold.ico'))
        self.fold.Bind(wx.EVT_BUTTON, self.OnFold)
        self.unfold.Bind(wx.EVT_BUTTON, self.OnUnfold)

        # 工程树
        self.tree = wx.TreeCtrl(self.left_panel, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_TWIST_BUTTONS)
        self.update_tree()
        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.add_pop_up_menu)
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnTreeLeftDclick)

        # 工程树图标
        image_list = wx.ImageList(16, 16, True, 4)
        image_list.Add(wx.Icon('./icon/folders.ico'))
        image_list.Add(wx.Icon('./icon/files.ico'))
        image_list.Add(wx.Icon('./icon/file_structure.ico'))
        image_list.Add(wx.Icon('./icon/file_config.ico'))
        image_list.Add(wx.Icon('./icon/pictures.ico'))
        image_list.Add(wx.Icon('./icon/MIDIS.ico'))
        self.select = image_list.Add(wx.Icon('./icon/select.ico'))
        self.tree.AssignImageList(image_list)

        # 过滤搜索框
        self.filter = wx.SearchCtrl(self.left_panel, style=wx.TE_PROCESS_ENTER)
        self.filter.ShowCancelButton(True)
        self.filter.Bind(wx.EVT_SEARCH, self.OnFilterTextEnter)
        self.filter.Bind(wx.EVT_SEARCH_CANCEL, self.OnFilterCancel)

        # 工程区框架布局
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.combox, 1, wx.EXPAND, 5)
        box.Add(self.fold, 0, wx.EXPAND, 5)
        box.Add(self.unfold, 0, wx.EXPAND, 5)
        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.Add(box, 0, wx.EXPAND, 5)
        left_box.Add(self.tree, 1, wx.EXPAND)
        left_box.Add(self.filter, 0, wx.EXPAND, 5)
        self.left_panel.SetSizer(left_box)

    def update_tree(self):
        """ 更新工程树 """
        self.tree.DeleteAllItems()
        if self.project_dir:
            self.root = self.tree.AddRoot(os.path.basename(self.project_dir), 0)
            self.tree.SetItemData(self.root, self.project_dir)
            self.search = self.filter.GetValue()
            self._tree_open_dir(self.project_dir, filter=self.search)
            self.tree.Expand(self.root)
        else:
            self.root = self.tree.AddRoot('工程', 0)
            self.tree.SetItemImage(self.tree.GetRootItem(), 5)

    def _tree_open_dir(self, dir, root=None, filter=None, dept=2):
        """ 打开工程文件夹，添加文件夹树形节点"""
        items = os.listdir(dir)
        dirs = []
        files = []

        for item in items:
            if os.path.isdir(os.path.join(dir, item)):
                dirs.append(item)
            else:
                files.append(item)

        root = root if root else self.root
        for item in dirs:
            root_next = self.tree.AppendItem(root, item, 0)
            path_item = os.path.join(dir, item)
            self.tree.SetItemData(root_next, path_item)

            if dept > 0:
                self._tree_open_dir(path_item, root_next, filter, dept=dept-1)

        for item in files:
            it = self.tree.AppendItem(root, item, 1)
            path_item = os.path.join(dir, item)
            if is_structure_file(path_item):
                self.tree.SetItemImage(it, 2)
            elif is_cfg_file(path_item):
                self.tree.SetItemImage(it, 3)
            elif is_picture_file(path_item):
                self.tree.SetItemImage(it, 4)
            else:
                self.tree.SetItemImage(it, 1)
            self.tree.SetItemData(it, path_item)
            if filter and filter in item:
                self.tree.SetItemTextColour(it, 'blue')

    def get_dir(self):
        """ 获取工程路径 """
        return self.project_dir

    def get_selected_dir(self):
        """ 获取树控件当前选中文件夹及对应树节点 """
        item = self.tree.GetSelection()
        if not item:
            return self.project_dir, self.root
        path_item = self.tree.GetItemData(item)
        if item and os.path.isdir(path_item):
            return path_item, item
        elif item and os.path.isfile(path_item):
            return os.path.dirname(path_item), self.tree.GetItemParent(item)
        elif self.project_dir:
            return self.project_dir, self.root
        else:
            return self.project_dir, self.root

    def get_selected_file(self):
        """ 获取树控件当前选中文件夹及对应树节点 """
        item = self.tree.GetSelection()
        if not item:
            return
        path_item = self.tree.GetItemData(item)
        if os.path.isfile(path_item):
            return path_item

    def set_history_dirs(self, f_history_dirs, combox, num=10):
        """ 打开历史路径文件 """
        if not os.path.exists(f_history_dirs):
            pathlib.Path(f_history_dirs).touch()
            return

        file = open(f_history_dirs, 'r')
        history_dirs = file.read().strip(',').split('\n')[-num:]
        file.close()

        file = open(f_history_dirs, 'w')
        for tp_dir in history_dirs:
            if os.path.isdir(tp_dir):
                dir_short = tp_dir.split('\\')[-2] + '\\' + tp_dir.split('\\')[-1]
                combox.Append(dir_short, tp_dir)
                file.write(tp_dir + '\n')
            else:
                history_dirs.remove(tp_dir)
        file.close()

        return history_dirs

    def OnTreeLeftDown(self, event):
        """ 工程区鼠标左键按下选中 """
        if self.project_dir is None:
            return
        else:
            item, flags = self.tree.HitTest(event.GetPosition())
            self.tree.SetItemImage(item, self.select, wx.TreeItemIcon_Selected)

        event.Skip()

    def OnTreeLeftDclick(self, event):
        """ 工程区鼠标左键双击功能 """
        if self.project_dir is None:
            return
        else:
            item, flags = self.tree.HitTest(event.GetPosition())
            self.tree.SetItemImage(item, self.select, wx.TreeItemIcon_Selected)

        path_item = self.tree.GetItemData(item)
        if item and os.path.isdir(path_item) and not self.tree.ItemHasChildren(item):
            self._tree_open_dir(path_item, item, self.filter.GetValue())
        elif item and os.path.isfile(path_item):
            if is_structure_file(path_item):
                self.log.Info('ViewModel ' + path_item)
                self.OnModelView(event)
            elif is_edit_file(path_item):
                self.log.Info('Edit ' + path_item)
                self.editor.open_file(path_item)
            elif is_cfg_file(path_item):
                self.log.Info('Siesta计算文件配置中...')
                configdlg = SiestaConfig(self.frame, self.app, reconfig=True)
                if configdlg.ShowModal() == wx.ID_OK:
                    configdlg.CenterOnScreen()
                else:
                    configdlg.Destroy()
            else:
                pass
        else:
            pass

    def OnFilterTextEnter(self, event):
        """ 工程区过滤搜索框 """
        self.update_tree()
        self.tree.ExpandAllChildren(self.root)

    def OnFilterCancel(self, event):
        """ 工程区过滤取消 """
        self.filter.SetValue('')
        self.update_tree()

    def OnHistoryPathSelect(self, event):
        """ 历史工程框 """
        cb = event.GetEventObject()
        project_dir = cb.GetClientData(event.GetSelection())
        if os.path.exists(project_dir):
            self.log.Info('打开工程文件夹：' + project_dir)
            self.project_dir = project_dir
            self.update_tree()
        else:
            self.log.Warning('不存在该路径：'+ project_dir)

    def OnFold(self, event):
        """ 工程树折叠 """
        self.update_tree()
        self.tree.CollapseAllChildren(self.root)

    def OnUnfold(self,event):
        """ 工程树展开 """
        self.update_tree()
        self.tree.ExpandAllChildren(self.root)

    def add_project_menu(self, parent):
        project_menu = wx.Menu()

        project_new = project_menu.Append(-1, '新建工程')
        project_open = project_menu.Append(-1, '打开工程')
        project_update = project_menu.Append(-1, '&刷新工程\tF5')
        open_explor = project_menu.Append(-1, '在文件夹中打开')
        project_menu.AppendSeparator()

        model_input = project_menu.Append(-1, '载入模型文件')
        batch_processing = project_menu.Append(-1, '批量载入模型文件')
        model_view = project_menu.Append(-1, '显示模型文件')
        project_menu.AppendSeparator()

        parent.Bind(wx.EVT_MENU, self.OnProjectNew, project_new)
        parent.Bind(wx.EVT_MENU, self.OnProjectOpen, project_open)
        parent.Bind(wx.EVT_MENU, self.OnProjectUpdate, project_update)
        parent.Bind(wx.EVT_MENU, self.OnOpenExplor, open_explor)
        parent.Bind(wx.EVT_MENU, self.OnModelInput, model_input)
        parent.Bind(wx.EVT_MENU, self.OnBatchProcessing, batch_processing)
        parent.Bind(wx.EVT_MENU, self.OnModelView, model_view)

        return project_menu

    def add_pop_up_menu(self, event):
        """ 工程树控件的右键菜单 """
        if self.project_dir is None:
            return
        else:
            item, flags = self.tree.HitTest(event.GetPosition())
            self.tree.SetItemImage(item, self.select, wx.TreeItemIcon_Selected)

        project_menu = wx.Menu()

        project_edit = project_menu.Append(-1, '打开')
        project_new = project_menu.Append(-1, '新建工程')
        project_open = project_menu.Append(-1, '打开工程')
        project_update = project_menu.Append(-1, '&刷新工程\tF5')
        open_explor = project_menu.Append(-1, '在文件夹中打开')
        project_menu.AppendSeparator()

        model_input = project_menu.Append(-1, '载入模型文件')
        batch_processing = project_menu.Append(-1, '批量载入模型文件')
        model_view = project_menu.Append(-1, '显示模型文件')
        project_menu.AppendSeparator()

        upload_database = project_menu.Append(-1, '导入数据库')
        file_delete = project_menu.Append(-1, '删除文件')

        self.tree.Bind(wx.EVT_MENU, self.OnProjectEdit, project_edit)
        self.tree.Bind(wx.EVT_MENU, self.OnProjectNew, project_new)
        self.tree.Bind(wx.EVT_MENU, self.OnProjectOpen, project_open)
        self.tree.Bind(wx.EVT_MENU, self.OnProjectUpdate, project_update)
        self.tree.Bind(wx.EVT_MENU, self.OnOpenExplor, open_explor)
        self.tree.Bind(wx.EVT_MENU, self.OnModelInput, model_input)
        self.tree.Bind(wx.EVT_MENU, self.OnBatchProcessing, batch_processing)
        self.tree.Bind(wx.EVT_MENU, self.OnModelView, model_view)
        self.tree.Bind(wx.EVT_MENU, self.OnUploadDatabase, upload_database)
        self.tree.Bind(wx.EVT_MENU, self.OnFileDelete, file_delete)
        self.tree.PopupMenu(project_menu)
        project_menu.Destroy()

    def OnProjectEdit(self, event):
        """ 编辑文件 """
        item = self.tree.GetSelection()
        if not item:
            return
        path_item = self.tree.GetItemData(item)
        if item and os.path.isfile(path_item):
            self.log.Debug('编辑: ' + path_item)
            self.editor.open_file(path_item)
        else:
            pass

    def OnProjectNew(self, event):
        """ 新建工程 """
        dlg = CreateProjDialog(None)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()

        if val == wx.ID_OK:
            dir = CreateProjDialog.get_proj_dir(dlg)
            name = CreateProjDialog.get_proj_name(dlg)
            proj_dir = str(dir + '\\' + name)
            is_exists = os.path.exists(proj_dir)
            if not is_exists:
                os.makedirs(proj_dir)
                self.project_dir = proj_dir
                self.combox.AppendItems(self.project_dir)
                with open(self.f_history_dirs, 'a') as f:
                    f.write('\n' + self.project_dir)
                self.log.Debug('工程创建成功！')
                self.update_tree()
            else:
                self.log.Warning('该工程已存在！')
        dlg.Destroy()

    def OnProjectOpen(self, event):
        """ 打开工程 """
        dlg = wx.DirDialog(None, '选择工程文件夹：', style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            self.log.Info('打开工程文件夹：' + dlg.GetPath())
            self.project_dir = dlg.GetPath()
            self.update_tree()

            dir_short = self.project_dir.split('\\')[-2] + '\\' + self.project_dir.split('\\')[-1]
            self.combox.Append(dir_short, self.project_dir)
            with open(self.f_history_dirs, 'a') as f:
                f.write(self.project_dir + '\n')

        dlg.Destroy()

    def OnProjectUpdate(self, event):
        """ 更新工程树 """
        self.update_tree()

    def OnOpenExplor(self, event):
        """ 打开系统文件夹 """
        dir_item, _ = self.get_selected_dir()
        if dir_item:
            self.log.Debug('打开系统文件夹：' + dir_item)
            os.startfile(dir_item)
        else:
            self.log.Warning('该工程文件夹不存在！')

    def OnModelInput(self, event, defaultDir=''):
        """ 载入模型文件 """
        if self.project_dir is None:
            return
        fileDialog = wx.FileDialog(None, '选择文件：', defaultDir=defaultDir)
        if fileDialog.ShowModal() == wx.ID_OK:
            self.log.Debug('载入文件： %s\n' % fileDialog.GetPath())
            model_file = fileDialog.GetPath()
            file_name = os.path.basename(model_file)
            name, ext = os.path.splitext(file_name)

            # 目标文件
            dir_item, item = self.get_selected_dir()
            folder_path = os.path.join(dir_item, name + '_org')
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                it = self.tree.AppendItem(item, name, 0)
                self.tree.SetItemData(it, folder_path)
            path_file = os.path.join(folder_path, file_name)
            if not os.path.exists(path_file):
                file_name = name + ext
                path_file = os.path.join(folder_path, file_name)

                self.log.Debug('导入文件 ' + model_file + ' 到 ' + folder_path)
                shutil.copyfile(model_file, path_file)
                it = self.tree.AppendItem(item, file_name, 1)
                self.tree.SetItemData(it, path_file)

            # 对于模型文件，转换格式
            if is_structure_file(path_file):
                # from .cif2pos import ciftoposcar
                # from .ase_MIDIS import cif22xsf
                path_files = ciftoposcar(model_file, path_file)
                path_file = cif22xsf(path_file, log=self.log)
                path_files.append(path_file)
                for i in range(len(path_files)):
                    path_file = path_files[i]
                    if path_file:
                        file_name = os.path.basename(path_file)
                        it = self.tree.AppendItem(item, file_name, 1)
                        self.tree.SetItemData(it, path_file)

        self.log.Info('文件载入成功！')
        self.update_tree()

    def OnBatchProcessing(self, event):
        """ 批量载入模型文件 """
        dlg = wx.DirDialog(None, '选择模型文件夹：', style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            self.log.Info('打开模型文件夹：' + dlg.GetPath())
            model_dir = dlg.GetPath()

            dir_item, item = self.get_selected_dir()

            # from .cif2pos import ciftoposcar
            def filesconverting(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        name, ext = os.path.splitext(os.path.basename(path1))
                        folder_path = os.path.join(dir_item, name)
                        os.mkdir(folder_path)
                        it = self.tree.AppendItem(item, name, 0)
                        self.tree.SetItemData(it, folder_path)
                        shutil.copyfile(path1, os.path.join(folder_path, os.path.basename(path1)))
                        it = self.tree.AppendItem(item, os.path.basename(path1), 1)
                        self.tree.SetItemData(it, os.path.join(folder_path, os.path.basename(path1)))
                        folder_path1 = os.path.join(folder_path, 'POSCAR')
                        folder_path2 = os.path.join(folder_path, 'POTCAR')
                        with open(folder_path1, 'w') as f1:
                            f1.write('')
                        with open(folder_path2, 'w') as f2:
                            f2.write('')
                        path_files = ciftoposcar(path1, folder_path1)
                        for i in range(len(path_files)):
                            path_file = path_files[i]
                            if path_file:
                                file_name = os.path.basename(path_file)
                                it = self.tree.AppendItem(item, file_name, 1)
                                self.tree.SetItemData(it, path_file)
                    else:
                        filesconverting(path1)

            filesconverting(model_dir)
            self.update_tree()

        dlg.Destroy()

    def OnModelView(self, event, ASEgui=True):
        """ 调用 ASE 软件显示模型 """
        item = self.tree.GetSelection()
        if not item:
            return
        file_path = self.tree.GetItemData(item)
        if is_structure_file(file_path):
            # from .ase_MIDIS import view_model
            view_model(file_path, None, ASEgui=True, log=self.log, path=self.project_dir)
            self.update_tree()
        else:
            self.log.Warning('这不是模型文件：' + file_path)

    def OnFileDelete(self, event):
        """ 删除文件 """
        yes_no_msg = wx.MessageDialog(None, message='将从工程及系统文件夹中删除对应文件，\n\n删除后将不能恢复，请确认吗？\n',
                                      caption='删除文件', style=wx.YES_NO | wx.ICON_QUESTION)
        status = yes_no_msg.ShowModal()
        yes_no_msg.Destroy()
        if status == wx.ID_NO:
            return
        item = self.tree.GetSelection()
        path = self.tree.GetItemData(item)
        self.log.Debug('删除：' + path + '文件')
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        self.tree.Delete(item)

    def OnUploadDatabase(self, event):
        """ 导入数据库 """
        self.log.Info('开始导入数据...')
        database_path = os.path.join(os.getcwd(), r'Share\database')

        try:
            if os.path.exists(os.path.join(self.project_dir, 'POSCAR')):
                with open(os.path.join(self.project_dir, 'POSCAR'), 'r') as f:
                    name = f.readline().strip('\n').split(' ')
                    self.database_path = os.path.join(database_path, name[0])
                    os.mkdir(self.database_path)
            else:
                pass

            file = os.path.join(self.database_path, r'structure')
            os.mkdir(file)
            for i in os.listdir(self.project_dir):
                file_path = os.path.join(self.project_dir, i)
                if os.path.isdir(file_path) and os.path.exists(file_path):
                    files = os.path.join(self.database_path, i)
                    os.mkdir(files)
                    for j in os.listdir(file_path):
                        if i == 'RELAX' and j in ['INCAR', 'KPOINTS', 'CONTCAR']:
                            local_file = os.path.join(file_path, j)
                            database_file = os.path.join(files, j)
                            shutil.copyfile(local_file, database_file)
                        elif i == 'BAND' and j in ['INCAR', 'KPOINTS', 'band.png',
                                                   'band_element.png','band_orbit.png']:
                            local_file = os.path.join(file_path, j)
                            database_file = os.path.join(files, j)
                            shutil.copyfile(local_file, database_file)
                        elif i == 'DOS' and j in ['INCAR', 'KPOINTS', 'dos.png',
                                                   'dos_element.png', 'dos_orbit.png']:
                            local_file = os.path.join(file_path, j)
                            database_file = os.path.join(files, j)
                            shutil.copyfile(local_file, database_file)
                        elif i == 'SCF' and j in ['INCAR', 'KPOINTS']:
                            local_file = os.path.join(file_path, j)
                            database_file = os.path.join(files, j)
                            shutil.copyfile(local_file, database_file)
                        else:
                            pass
                else:
                    if i not in ['POTCAR', 'JOB']:
                        shutil.copyfile(file_path, os.path.join(file, i))
                    else:
                        pass
        except EnvironmentError as e:
            self.log.Error(e)

        self.log.Info('数据导入完成！')

class CreateProjDialog(wx.Dialog):
    """ 创建一个新建工程对话框 """

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, style = wx.DEFAULT_DIALOG_STYLE)

        self.InitUI()
        self.pro_dir = os.path.join(os.getcwd(), 'work')

        sizer = wx.BoxSizer(wx.VERTICAL)
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, '工程名称：')
        box.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.text_1 = wx.TextCtrl(self, -1, '', size=(300, -1))
        box.Add(self.text_1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer.Add(box, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, '工程路径：')
        box.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.text_2 = wx.TextCtrl(self, -1, '{}'.format(self.pro_dir), size=(300, -1))
        box.Add(self.text_2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        button = wx.Button(self, -1, '浏览', size=(40, -1))
        self.Bind(wx.EVT_BUTTON, self.OpenProjDir, button)
        box.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sizer.Add(box, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(480, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.ALIGN_LEFT | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def InitUI(self):
        """ 初始化主界面 """
        icon = os.getcwd() + '\\icon\\MIDIS.ico'
        icon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        icon.SetHeight(18)
        icon.SetWidth(18)
        self.SetIcon(icon)
        self.SetTitle(title='新建工程')
        self.SetSize(wx.Size(350, 200))
        self.Centre()

    def get_proj_name(self):
        """ 获取工程名称 """
        proj_name = self.text_1.GetValue()
        return proj_name

    def get_proj_dir(self):
        """ 获取工程路径名称 """
        proj_dir = self.text_2.GetValue()
        return proj_dir

    def OpenProjDir(self, event):
        """ 获取工程路径 """
        self.text_2.Clear()
        dlg = wx.DirDialog(None, '选择工程路径：', style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            dir = dlg.GetPath()
            dlg.Destroy()
            self.text_2.AppendText(str(dir))




