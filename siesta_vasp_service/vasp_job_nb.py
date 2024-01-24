import wx
import os
import shutil


class JOB(wx.Panel):
    """ JOB设置 """
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)

        job_box = wx.BoxSizer(wx.VERTICAL)

        sz = wx.StaticBoxSizer(wx.VERTICAL, self, '计算相关配置')
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='任务名称: ')
        self.text1 = wx.TextCtrl(self, -1, value='VASP')
        box1.Add(st1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box1.Add(self.text1, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='   nodes: ')
        self.text2 = wx.TextCtrl(self, -1, value='1')
        st21 = wx.StaticText(self, label=' 节点数')
        box2.Add(st2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box2.Add(self.text2, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box2.Add(st21, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='      ppn: ')
        self.text3 = wx.TextCtrl(self, -1, value='8')
        st31 = wx.StaticText(self, label=' 单个节点CPU数')
        box3.Add(st3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box3.Add(self.text3, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box3.Add(st31, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        box4 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='walltime: ')
        self.text4 = wx.TextCtrl(self, -1, value='7200:00:00')
        st41 = wx.StaticText(self, label=' 最长计算时间')
        box4.Add(st4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box4.Add(self.text4, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box4.Add(st41, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz.Add(box1, flag=wx.ALL, border=5)
        sz.Add(box2, flag=wx.ALL, border=5)
        sz.Add(box3, flag=wx.ALL, border=5)
        sz.Add(box4, flag=wx.ALL, border=5)

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '软件相关配置')
        box5 = wx.BoxSizer(wx.HORIZONTAL)
        st5 = wx.StaticText(self, label='VASP软件包位置: ')
        self.text5 = wx.TextCtrl(self, -1, value='/home/iei/software/vasp.5.4.4/bin/vasp_std', size=(260,20))
        box5.Add(st5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        box5.Add(self.text5, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)

        sz1.Add(box5, flag=wx.ALL, border=5)

        job_box.Add(sz, flag=wx.ALL, border=5)
        job_box.Add(sz1, flag=wx.ALL, border=5)

        self.SetSizer(job_box)
        parent.AddPage(self, 'job')

    def WriteJob(self, path):
        def job_folder(path):
            for i in os.listdir(path):
                path1 = os.path.join(path, i)
                if os.path.isfile(path1):
                    if os.path.basename(path1) == 'INCAR':
                        job_path = os.path.join(os.path.dirname(path1), 'job.sh')

                        if not os.path.exists(job_path):
                            with open(job_path, 'a+') as f:
                                f.write('#!/bin/bash\n'
                                        '#PBS -N {0}\n'
                                        '#PBS -o out.dat\n'
                                        '#PBS -e err.dat\n'
                                        '#PBS -q batch\n'
                                        '#PBS -l nodes={1}:ppn={2}\n'
                                        '#PBS -l walltime={3}\n'
                                        'cd $PBS_O_WORKDIR\n\n'
                                        'mpirun -n {2} {4} > vasp.out'.format(self.text1.GetLineText(0), self.text2.GetLineText(0), self.text3.GetLineText(0), self.text4.GetLineText(0), self.text5.GetLineText(0)))

                else:
                    job_folder(path1)

        job_folder(path)
