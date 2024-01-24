import wx
import wx.aui as aui
import os
import csv
from .text_editor import TextEditor
from MainFrame.util_file import is_structure_file, is_cfg_file, is_picture_file


class EditorService:
    """ 编辑区 """

    def __init__(self, parent):

        self.frame = parent
        self.nb = aui.AuiNotebook(self.frame, style=wx.aui.AUI_NB_TOP| wx.aui.AUI_NB_TAB_SPLIT
                                                    | wx.aui.AUI_NB_TAB_MOVE| wx.aui.AUI_NB_SCROLL_BUTTONS)

        self.pages = {}
        self.editor_cls = {}

        self.pdata = wx.PrintData()
        self.pdata.SetPaperId(wx.PAPER_LETTER)
        self.pdata.SetOrientation(wx.PORTRAIT)

    def set_app(self, app):
        self.app = app
        self.log = app.log
        self.project = app.project

        self.nb.Bind(aui.EVT_AUINOTEBOOK_TAB_RIGHT_DOWN, self.add_pop_up_menu)

        self.frame.get_menu_bar().Insert(0, self.add_file_menu(self.frame), '文件')
        self.frame.get_menu_bar().Insert(1, self.add_editor_menu(self.frame), '编辑')
        self.add_tool(self.frame)
        self.frame.get_mgr().AddPane(self.frame.get_tool_bar(), aui.AuiPaneInfo().ToolbarPane().Top())
        self.frame.get_mgr().AddPane(self.nb, aui.AuiPaneInfo().Name('editor').Caption('编辑区').
                                     CaptionVisible(False).Center().Layer(0).Position(0))
        self.frame.update()

    def get_page_id(self, path):
        """ 获取页码 """
        self.log.Debug('get_page_id: ' + str(self.nb.GetPageIndex(self.pages[path])))
        return self.nb.GetPageIndex(self.pages[path])

    def set_page_path(self, id, path):
        """ 设置页面路径 """
        self.nb.SetPageToolTip(id, path)
        return

    def get_page_path(self, id):
        """ 获取页面路径 """
        return self.nb.GetPageToolTip(id)

    def set_page_image(self, path):
        """ 设置页面图标 """
        image_list = wx.ImageList(16, 16, True, 3)
        file = image_list.Add(wx.Icon('./icon/files.ico'))
        file_structure = image_list.Add(wx.Icon('./icon/file_structure.ico'))
        file_config = image_list.Add(wx.Icon('./icon/file_config.ico'))
        picture = image_list.Add(wx.Icon('./icon/pictures.ico'))
        self.nb.AssignImageList(image_list)
        if is_structure_file(path):
            self.nb.SetPageImage(self.get_page_id(path), file_structure)
        elif is_cfg_file(path):
            self.nb.SetPageImage(self.get_page_id(path), file_config)
        elif is_picture_file(path):
            self.nb.SetPageImage(self.get_page_id(path), picture)
        else:
            self.nb.SetPageImage(self.get_page_id(path), file)

    def save_file(self, id):
        """ 保存文件 """
        path = self.get_page_path(id)
        if os.path.exists(path):
            editor = self.pages[path]
            if editor.IsModified():
                source = self.pages[path].GetText()
                with open(path, 'w') as f:
                    f.write(source)
                self.log.Info('文件 {} 保存好了'.format(path))
            else:
                self.log.Info('文件未修改')
        else:
            source = self.pages[self.project].GetText()
            with open(self.project, 'w') as f:
                f.write(source)
            self.log.Info('文件 {} 保存好了'.format(self.project))

    def open_file(self, path):
        """ 打开文件 """
        if not path:
            return

        if path in self.pages.keys():
            page_id = self.get_page_id(path)
            self.nb.SetSelection(page_id)

            return

        else:
            if not os.path.isfile(path):
                return
            if os.path.basename(path).split('.')[-1] == 'png':
                image = wx.Image(path, wx.BITMAP_TYPE_ANY).Rescale(width=600, height=400)
                temp = image.ConvertToBitmap()
                self.editor = wx.StaticBitmap(self.nb, -1, bitmap=temp)
            elif os.path.basename(path).split('.')[-1] == 'csv':
                self.editor = wx.TextCtrl(self.nb, -1, value='', style=wx.TE_MULTILINE)
                with open(path, 'r') as f:
                    data = ''
                    reader = csv.reader(f)
                    for row in reader:
                        data += str(row) + '\n'
                self.editor.AppendText(data)

            else:
                self.editor = TextEditor(self.nb)
                self.editor.LoadFile(path)

        self.log.Debug('path: ' + path)
        title = os.path.basename(path)
        self.pages[path] = self.editor
        self.nb.AddPage(self.editor, title, select=True)
        self.set_page_path(self.nb.GetSelection(), path)
        self.set_page_image(path)


    def add_tool(self, parent):
        """ 工具栏 """
        tool_bar = self.frame.get_tool_bar()

        file_new = tool_bar.AddTool(-1, 'new', wx.Bitmap('./icon/files.ico'), shortHelp='new')
        file_open = tool_bar.AddTool(-1, 'open', wx.Bitmap('./icon/folders.ico'),shortHelp='open')
        tool_bar.AddSeparator()
        file_save = tool_bar.AddTool(wx.ID_SAVE, 'save', wx.Bitmap('./icon/save.ico'), shortHelp='save')
        file_save_as = tool_bar.AddTool(wx.ID_SAVEAS, 'save as', wx.Bitmap('./icon/save_as.ico'), shortHelp='save as')
        file_save_all = tool_bar.AddTool(wx.ID_STATIC, 'save all', wx.Bitmap('./icon/all.ico'), shortHelp='save all')
        tool_bar.AddSeparator()
        file_printer = tool_bar.AddTool(wx.ID_PRINT, 'printer', wx.Bitmap('./icon/printers.ico'), shortHelp='printer')
        file_preview = tool_bar.AddTool(wx.ID_PREVIEW, 'preview', wx.Bitmap('./icon/preview.ico'), shortHelp='preview')
        tool_bar.AddSeparator()
        cut = tool_bar.AddTool(wx.ID_CUT, 'cut', wx.Bitmap('./icon/cut.ico'), shortHelp='cut')
        copy = tool_bar.AddTool(wx.ID_COPY, 'copy', wx.Bitmap('./icon/copy.ico'), shortHelp='copy')
        paste = tool_bar.AddTool(wx.ID_PASTE, 'paste', wx.Bitmap('./icon/paste.ico'), shortHelp='paste')
        undo = tool_bar.AddTool(wx.ID_UNDO, 'undo', wx.Bitmap('./icon/undo.ico'), shortHelp='undo')
        redo = tool_bar.AddTool(wx.ID_REDO, 'redo', wx.Bitmap('./icon/redo.ico'), shortHelp='redo')
        tool_bar.AddSeparator()
        frame_reset = tool_bar.AddTool(-1, 'frame reset', wx.Bitmap('./icon/reset.ico'), shortHelp='frame reset')
        exit = tool_bar.AddTool(-1, 'exit', wx.Bitmap('./icon/exit.ico'), shortHelp='exit')
        tool_bar.Realize()

        # 设置初始工具栏元素状态
        # tool_bar.EnableTool(wx.ID_SAVE, False)
        # tool_bar.EnableTool(wx.ID_SAVEAS, False)
        # tool_bar.EnableTool(wx.ID_STATIC, False)
        # tool_bar.EnableTool(wx.ID_PRINT, False)
        # tool_bar.EnableTool(wx.ID_PREVIEW, False)
        # tool_bar.EnableTool(wx.ID_CUT, False)
        # tool_bar.EnableTool(wx.ID_COPY, False)
        # tool_bar.EnableTool(wx.ID_PASTE, False)
        # tool_bar.EnableTool(wx.ID_UNDO, False)
        # tool_bar.EnableTool(wx.ID_REDO, False)

        parent.Bind(wx.EVT_TOOL, self.OnNew, file_new)
        parent.Bind(wx.EVT_TOOL, self.OnOpen, file_open)
        parent.Bind(wx.EVT_TOOL, self.OnSave, file_save)
        parent.Bind(wx.EVT_TOOL, self.OnSaveAs, file_save_as)
        parent.Bind(wx.EVT_TOOL, self.OnSaveAll, file_save_all)
        parent.Bind(wx.EVT_TOOL, self.OnPrinter, file_printer)
        parent.Bind(wx.EVT_TOOL, self.OnPreview, file_preview)
        parent.Bind(wx.EVT_TOOL, self.OnFrameReset, frame_reset)
        parent.Bind(wx.EVT_TOOL, self.OnExit, exit)
        parent.Bind(wx.EVT_TOOL, self.OnUndo, undo)
        parent.Bind(wx.EVT_TOOL, self.OnRedo, redo)
        parent.Bind(wx.EVT_TOOL, self.OnCut, cut)
        parent.Bind(wx.EVT_TOOL, self.OnCopy, copy)
        parent.Bind(wx.EVT_TOOL, self.OnPaste, paste)

        return tool_bar

    def add_file_menu(self, parent):
        """ 文件菜单 """
        file_menu = wx.Menu()

        nmi = wx.MenuItem(file_menu, -1, '新建\tCtrl+N')
        nmi.SetBitmap(wx.Bitmap('./icon/files.ico'))
        file_new = file_menu.Append(nmi)

        omi = wx.MenuItem(file_menu, -1, '打开\tCtrl+O')
        omi.SetBitmap(wx.Bitmap('./icon/folders.ico'))
        file_open = file_menu.Append(omi)

        cmi = wx.MenuItem(file_menu, wx.ID_CLOSE, '关闭')
        cmi.SetBitmap(wx.Bitmap('./icon/close.ico'))
        file_close = file_menu.Append(cmi)

        cami = wx.MenuItem(file_menu, wx.ID_CLOSE_ALL, '关闭所有')
        cami.SetBitmap(wx.Bitmap('./icon/close_all.ico'))
        file_close_all = file_menu.Append(cami)
        file_menu.AppendSeparator()

        smi = wx.MenuItem(file_menu, wx.ID_SAVE, '保存\tCtrl+S')
        smi.SetBitmap(wx.Bitmap('./icon/save.ico'))
        file_save = file_menu.Append(smi)

        sami = wx.MenuItem(file_menu, wx.ID_SAVEAS, '另存为')
        sami.SetBitmap(wx.Bitmap('./icon/save_as.ico'))
        file_save_as = file_menu.Append(sami)

        salmi = wx.MenuItem(file_menu, wx.ID_STATIC, '保存所有\tCtrl+Shift+A')
        salmi.SetBitmap(wx.Bitmap('./icon/all.ico'))
        file_save_all = file_menu.Append(salmi)
        file_menu.AppendSeparator()

        pmi = wx.MenuItem(file_menu, wx.ID_PRINT, '打印\tCtrl+P')
        pmi.SetBitmap(wx.Bitmap('./icon/printers.ico'))
        file_printer = file_menu.Append(pmi)

        pwmi = wx.MenuItem(file_menu, wx.ID_PREVIEW, '打印预览')
        pwmi.SetBitmap(wx.Bitmap('./icon/preview.ico'))
        file_preview = file_menu.Append(pwmi)

        rmi = wx.MenuItem(file_menu, -1, '重置页面')
        rmi.SetBitmap(wx.Bitmap('./icon/reset.ico'))
        frame_reset = file_menu.Append(rmi)
        file_menu.AppendSeparator()

        emi = wx.MenuItem(file_menu, -1, '退出')
        emi.SetBitmap(wx.Bitmap('./icon/exit.ico'))
        exit = file_menu.Append(emi)

        # 设置初始文件菜单元素状态
        # file_menu.Enable(wx.ID_CLOSE, False)
        # file_menu.Enable(wx.ID_CLOSE_ALL, False)
        # file_menu.Enable(wx.ID_SAVE, False)
        # file_menu.Enable(wx.ID_SAVEAS, False)
        # file_menu.Enable(wx.ID_STATIC, False)
        # file_menu.Enable(wx.ID_PRINT, False)
        # file_menu.Enable(wx.ID_PREVIEW, False)

        parent.Bind(wx.EVT_MENU, self.OnNew, file_new)
        parent.Bind(wx.EVT_MENU, self.OnOpen, file_open)
        parent.Bind(wx.EVT_MENU, self.OnClose, file_close)
        parent.Bind(wx.EVT_MENU, self.OnCloseAll, file_close_all)
        parent.Bind(wx.EVT_MENU, self.OnSave, file_save)
        parent.Bind(wx.EVT_MENU, self.OnSaveAs, file_save_as)
        parent.Bind(wx.EVT_MENU, self.OnSaveAll, file_save_all)
        parent.Bind(wx.EVT_MENU, self.OnPrinter, file_printer)
        parent.Bind(wx.EVT_MENU, self.OnPreview, file_preview)
        parent.Bind(wx.EVT_MENU, self.OnFrameReset, frame_reset)
        parent.Bind(wx.EVT_MENU, self.OnExit, exit)

        return file_menu

    def add_pop_up_menu(self, event):
        """ 编辑区的右键菜单 """
        menu = wx.Menu()
        file_close = menu.Append(-1, '关闭')
        file_close_all = menu.Append(-1, '关闭所有')
        menu.AppendSeparator()
        file_save = menu.Append(-1, '保存')
        file_save_as = menu.Append(-1, '另存为')

        self.frame.Bind(wx.EVT_MENU, self.OnClose, file_close)
        self.frame.Bind(wx.EVT_MENU, self.OnCloseAll, file_close_all)
        self.frame.Bind(wx.EVT_MENU, self.OnSave, file_save)
        self.frame.Bind(wx.EVT_MENU, self.OnSaveAs, file_save_as)
        self.nb.PopupMenu(menu)
        menu.Destroy()

    def add_editor_menu(self, parent):
        """ 编辑菜单 """
        editor_menu = wx.Menu()

        umi = wx.MenuItem(editor_menu, wx.ID_UNDO, 'Undo\tCtrl+Z')
        umi.SetBitmap(wx.Bitmap('./icon/undo.ico'))
        undo = editor_menu.Append(umi)

        rmi = wx.MenuItem(editor_menu, wx.ID_REDO, 'Redo\tCtrl+Y')
        rmi.SetBitmap(wx.Bitmap('./icon/redo.ico'))
        redo = editor_menu.Append(rmi)
        editor_menu.AppendSeparator()

        cmi = wx.MenuItem(editor_menu, wx.ID_CUT, '剪切\tCtrl+X')
        cmi.SetBitmap(wx.Bitmap('./icon/cut.ico'))
        cut = editor_menu.Append(cmi)

        cpmi = wx.MenuItem(editor_menu, wx.ID_COPY, '复制\tCtrl+C')
        cpmi.SetBitmap(wx.Bitmap('./icon/copy.ico'))
        copy = editor_menu.Append(cpmi)

        pmi = wx.MenuItem(editor_menu, wx.ID_PASTE, '粘贴\tCtrl+V')
        pmi.SetBitmap(wx.Bitmap('./icon/paste.ico'))
        paste = editor_menu.Append(pmi)

        dmi = wx.MenuItem(editor_menu, wx.ID_DELETE, '删除')
        dmi.SetBitmap(wx.Bitmap('./icon/delete.ico'))
        delete = editor_menu.Append(dmi)
        editor_menu.AppendSeparator()

        smi = wx.MenuItem(editor_menu, wx.ID_SELECTALL, '选择所有\tCtrl+A')
        smi.SetBitmap(wx.Bitmap('./icon/selection.ico'))
        select_all = editor_menu.Append(smi)

        dfmi = wx.MenuItem(editor_menu, wx.ID_DEFAULT, '删除文件')
        dfmi.SetBitmap(wx.Bitmap('./icon/file_delete.ico'))
        delete_file = editor_menu.Append(dfmi)

        # 设置初始编辑菜单元素状态
        # editor_menu.Enable(wx.ID_UNDO, False)
        # editor_menu.Enable(wx.ID_REDO, False)
        # editor_menu.Enable(wx.ID_CUT, False)
        # editor_menu.Enable(wx.ID_COPY, False)
        # editor_menu.Enable(wx.ID_PASTE, False)
        # editor_menu.Enable(wx.ID_DELETE, False)
        # editor_menu.Enable(wx.ID_SELECTALL, False)
        # editor_menu.Enable(wx.ID_DEFAULT, False)

        parent.Bind(wx.EVT_MENU, self.OnUndo, undo)
        parent.Bind(wx.EVT_MENU, self.OnRedo, redo)
        parent.Bind(wx.EVT_MENU, self.OnCut, cut)
        parent.Bind(wx.EVT_MENU, self.OnCopy, copy)
        parent.Bind(wx.EVT_MENU, self.OnPaste, paste)
        parent.Bind(wx.EVT_MENU, self.OnDelete, delete)
        parent.Bind(wx.EVT_MENU, self.OnSelectAll, select_all)
        parent.Bind(wx.EVT_MENU, self.OnDeleteFile, delete_file)

        return editor_menu


    def OnNew(self, event):
        """ 新建 """
        self.name = 1
        path = self.app.dir
        title = 'Unititled{0}'.format(self.name)
        path += title

        editor = TextEditor(self.nb)
        editor.SetValue('')
        self.pages[path] = editor
        self.nb.AddPage(editor, title, select=True)
        self.set_page_path(self.nb.GetSelection(), path)
        self.set_page_image(path)

        self.name += 1

    def OnOpen(self, event):
        """ 打开 """
        dlg = wx.FileDialog(None, message='打开文件', defaultDir=self.project.project_dir,
                            defaultFile='',style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.open_file(path)

    def OnClose(self, event):
        """ 关闭 """
        id = self.nb.GetSelection()
        path = self.get_page_path(id)
        self.log.Debug('关闭当前文件：' + str(id))
        self.pages.pop(path)
        self.nb.DeletePage(id)

    def OnCloseAll(self, event):
        """ 关闭所有 """
        self.log.Debug('关闭所有文件')
        self.pages.clear()
        self.nb.DeleteAllPages()

    def OnSave(self, event):
        """ 保存 """
        id = self.nb.GetSelection()
        self.save_file(id)

    def OnSaveAs(self, event):
        """ 另存为 """
        with wx.FileDialog(None, '保存文件', wildcard='',
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path_name = fileDialog.GetPath()
            try:
                path = self.get_page_path(self.nb.GetSelection())
                editor = self.pages[path]
                editor.SaveFile(path_name)
                self.log.Info('已保存文件 ' + path_name)
            except IOError:
                self.log.Error("不能将当前数据保存到 '%s' 文件中" % path_name)

    def OnSaveAll(self, event):
        """ 保存所有 """
        for i in range(self.nb.GetPageCount()):
            self.save_file(i)

    def OnPrinter(self, event):
        """ 打印 """
        text = ''
        data = wx.PrintDialogData(self.pdata)
        printer = wx.Printer(data)
        page = self.pages[self.get_page_path(self.nb.GetSelection())]
        for i in range(page.GetLineCount()):
            text += page.GetLine(i)
        printout = TextPrintout(text=text, margins=(self.frame.GetPosition(), self.frame.GetPosition()))
        if not printer.Print(None, printout, True) and printer.GetLastError() == wx.PRINTER_ERROR:
            wx.MessageBox('打印错误!', wx.OK)
        else:
            data = printer.GetPrintDialogData()
            printer.Print(None, printout, True)
            self.pdata = wx.PrintData(data.GetPrintData())
        printout.Destroy()

    def OnPreview(self, event):
        """ 打印预览 """
        text = ''
        data = wx.PrintDialogData(self.pdata)
        page = self.pages[self.get_page_path(self.nb.GetSelection())]
        for i in range(page.GetLineCount()):
            text += page.GetLine(i)
        printout1 = TextPrintout(text=text, margins=(self.frame.GetPosition(), self.frame.GetPosition()))
        printout2 = None
        preview = wx.PrintPreview(printout1, printout2, data)
        if not preview.IsOk():
            wx.MessageBox('不能创建打印预览！', '错误')
        else:
            frame = wx.PreviewFrame(preview, None, '打印预览', pos=self.frame.GetPosition(), size=self.frame.GetSize())
            frame.Initialize()
            frame.Show()

    def OnFrameReset(self, event):
        """ 重置页面 """
        self.frame.get_mgr().GetPane('log').Show()
        self.frame.get_mgr().GetPane('project').Show()
        self.frame.get_mgr().GetPane('editor').Show()
        self.frame.update()

    def OnExit(self, event):
        """ 退出 """
        self.frame.Close()
        return True

    def OnUndo(self, event):
        """ 撤销 """
        editor = self.pages[self.get_page_path(self.nb.GetSelection())]
        editor.Undo()

    def OnRedo(self, event):
        """ 重做 """
        editor = self.pages[self.get_page_path(self.nb.GetSelection())]
        editor.Redo()

    def OnCut(self, event):
        """ 剪切 """
        editor = self.pages[self.get_page_path(self.nb.GetSelection())]
        editor.Cut()

    def OnCopy(self, event):
        """ 复制 """
        editor = self.pages[self.get_page_path(self.nb.GetSelection())]
        editor.Copy()

    def OnPaste(self, event):
        """ 粘贴 """
        editor = self.pages[self.get_page_path(self.nb.GetSelection())]
        editor.Paste()

    def OnDelete(self, event):
        """ 删除 """
        editor = self.pages[self.get_page_path(self.nb.GetSelection())]
        editor.DeleteBack()

    def OnSelectAll(self, event):
        """ 选择所有 """
        editor = self.pages[self.get_page_path(self.nb.GetSelection())]
        editor.SelectAll()

    def OnDeleteFile(self, event):
        """ 删除文件 """
        yes_no_msg = wx.MessageDialog(None, message='将从工程及系统文件夹中删除对应文件，\n\n删除后将不能恢复，请确认吗？\n',
                                      caption='删除文件', style=wx.YES_NO | wx.ICON_QUESTION)
        status = yes_no_msg.ShowModal()
        yes_no_msg.Destroy()
        if status == wx.ID_NO:
            return
        item = self.project.tree.GetSelection()
        path = self.project.tree.GetItemData(item)
        self.log.Debug('删除：' + path + '文件')
        os.remove(path)
        self.project.tree.Delete(item)


class TextPrintout(wx.Printout):
    """ 打印类 """
    def __init__(self, text, margins):
        wx.Printout.__init__(self)
        self.lines = text.split('\n')
        self.margins = margins

    def HasPage(self, page):
        return page  <= self.numPages

    def GetPageInfo(self):
        return (1, self.numPages, 1, self.numPages)

    def CalculateScale(self, dc):
        # Scale the DC such that the printout is roughly the same as
        # the screen scaling.
        ppiPrinterX, ppiPrinterY = self.GetPPIPrinter()
        ppiScreenX, ppiScreenY = self.GetPPIScreen()
        logScale = float(ppiPrinterX) / float(ppiScreenX)

        # Now adjust if the real page size is reduced (such as when
        # drawing on a scaled wx.MemoryDC in the Print Preview.)  If
        # page width == DC width then nothing changes, otherwise we
        # scale down for the DC.
        pw, ph = self.GetPageSizePixels()
        dw, dh = dc.GetSize()
        scale = logScale * float(dw) / float(pw)

        # Set the DC's scale.
        dc.SetUserScale(scale, scale)

        # Find the logical units per millimeter (for calculating the
        # margins)
        self.logUnitsMM = float(ppiPrinterX) / (logScale * 25.4)

    def CalculateLayout(self, dc):
        # Determine the position of the margins and the
        # page/line height
        topLeft, bottomRight = self.margins
        dw, dh = dc.GetSize()
        self.x1 = topLeft.x * self.logUnitsMM
        self.y1 = topLeft.y * self.logUnitsMM

        self.x2 = dc.DeviceToLogicalXRel(dw) - bottomRight.x * self.logUnitsMM
        self.y2 = dc.DeviceToLogicalYRel(dh) - bottomRight.y * self.logUnitsMM

        # use a 1mm buffer around the inside of the box, and a few
        # pixels between each line
        self.pageHeight = self.y2 - self.y1 - 2 * self.logUnitsMM
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)

        self.lineHeight = dc.GetCharHeight()
        self.linesPerPage = int(self.pageHeight / self.lineHeight)

    def OnPreparePrinting(self):
        # calculate the number of pages
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)
        self.numPages = len(self.lines) / self.linesPerPage
        if len(self.lines) % self.linesPerPage != 0:
            self.numPages += 1

    def OnBeginDocument(self, startPage, endPage):
        return super(TextPrintout, self).OnBeginDocument(startPage, endPage)

    def OnEndDocument(self):
        super(TextPrintout, self).OnEndDocument()

    def OnBeginPrinting(self):
        super(TextPrintout, self).OnBeginPrinting()

    def OnEndPrinting(self):
        super(TextPrintout, self).OnEndPrinting()


    def OnPrintPage(self, pageNum):
        dc = self.GetDC()
        self.CalculateScale(dc)
        self.CalculateLayout(dc)

        # draw a page outline at the margin points
        dc.SetPen(wx.Pen("black", 0))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        r = wx.Rect((self.x1, self.y1),
                      (self.x2, self.y2))
        dc.DrawRectangle(r)
        dc.SetClippingRegion(r)

        # Draw the text lines for this page
        line = (pageNum - 1) * self.linesPerPage
        x = self.x1 + self.logUnitsMM
        y = self.y1 + self.logUnitsMM
        for i in range(len(self.lines)):
            dc.DrawText(self.lines[i], x, y)
            y += self.lineHeight
        return True


