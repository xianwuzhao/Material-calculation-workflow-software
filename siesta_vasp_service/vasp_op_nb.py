import wx
import os
import shutil

class OP(wx.Panel):
    """ OP设置 """
    def __init__(self, parent, id, path):
        wx.Panel.__init__(self, parent, id)
        self.system = 'op'
        op_box = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.BoxSizer(wx.VERTICAL)
        self.cb = wx.CheckBox(self, label='OP计算选择')
        self.cb.SetValue(False)
        self.cb.Bind(wx.EVT_CHECKBOX, self.OnOp)
        sz = wx.StaticBoxSizer(wx.VERTICAL, self, '初始化')
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='计算任务名: ')
        self.text1 = wx.TextCtrl(self, -1, value=self.system)
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        sz.Add(box1, flag=wx.ALL, border=5)
        box.Add(self.cb, flag=wx.ALL, border=5)
        box.Add(sz, flag=wx.ALL, border=5)
        op_box.Add(box, flag=wx.ALL, border=5)      
        self.SetSizer(op_box)
        parent.AddPage(self, 'op')
    def OnOp(self, event):
        self.op = self.cb.GetValue()
    def WriteOp(self, path):
        if self.op:
            def op_folder(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    op_path = os.path.join(os.path.dirname(path1), 'op')
                    if not os.path.exists(op_path):
                        os.mkdir(op_path)
                        shutil.copyfile(os.path.join(os.path.dirname(path1), 'POSCAR'),
                                            os.path.join(op_path, 'POSCAR'))
                    else:
                        print(1)
                        try:
                            op_folder(path1)
                        except:
                            pass                       
            op_folder(path)