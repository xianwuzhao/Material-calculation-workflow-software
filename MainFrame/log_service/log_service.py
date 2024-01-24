# !/usr/bin/env python

import wx
import wx.aui as aui
import wx.grid as grid
import time
import os
import paramiko


class LogService:
    """ 信息区 """

    def __init__(self, parent=None, type='info'):
        self.frame = parent
        self.type = type
        self.type_dict = {'debug': 0, 'info': 1, 'warning': 2, 'error': 3}

        self.work_dir = os.path.join(os.getcwd(), r'Share\work_dir.ini')
        self.job_dir = os.path.join(os.getcwd(), r'Share\job_id')
        # if os.path.exists(self.work_dir):
        #     with open(self.work_dir, 'r') as f:
        #         self.config = eval(f.read())
        #         self.ssh = SSH(self.config)
        # else:
        #     pass
        #
        # self.ssh.connect()
        self.cmd = ''

        # 设置笔记本框
        self.nb = aui.AuiNotebook(self.frame, style=aui.AUI_NB_BOTTOM)
        self.nb.SetTabCtrlHeight(35)

        # 信息
        self.log_panel = wx.Panel(self.nb, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN, size=(1200, 800))
        log_box = wx.BoxSizer(wx.VERTICAL)
        self.log_text = wx.TextCtrl(self.log_panel, -1, '', wx.Point(0, 0),
                                style=wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        log_box.Add(self.log_text, 1, wx.EXPAND | wx.ALL, 0)
        self.log_panel.SetSizer(log_box)

        # 终端
        self.terminal_panel = wx.Panel(self.nb, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN, size=(1200, 800))
        terminal_box = wx.BoxSizer(wx.VERTICAL)
        self.terminal_text = wx.TextCtrl(self.terminal_panel, -1, '', wx.Point(0, 0),
                                style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE | wx.NO_BORDER)
        terminal_box.Add(self.terminal_text, 1, wx.EXPAND | wx.ALL, 0)
        self.terminal_panel.SetSizer(terminal_box)
        # self.set_terminal_text()

        # 任务管理器
        self.job_panel = wx.Panel(self.nb, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN, size=(1200, 800))
        job_box = wx.BoxSizer(wx.VERTICAL)
        labels = ['任务编号', '计算类型', 'IP地址', '计算状态', '开始时间']
        self.rows = 6
        self.index = -1
        self.grid = grid.Grid(self.job_panel, -1)
        self.grid.AutoSizeColumns()
        self.grid.AutoSizeRows()
        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.grid.CreateGrid(self.rows, 5)
        self.grid.SetColLabelValue(0, labels[0])
        self.grid.SetColLabelValue(1, labels[1])
        self.grid.SetColLabelValue(2, labels[2])
        self.grid.SetColLabelValue(3, labels[3])
        self.grid.SetColLabelValue(4, labels[4])

        self.grid.SetColSize(0, 100)
        self.grid.SetColSize(1, 100)
        self.grid.SetColSize(2, 100)
        self.grid.SetColSize(3, 100)
        self.grid.SetColSize(4, 100)

        job_box.Add(self.grid, 1, wx.EXPAND | wx.ALL, 0)
        self.job_panel.SetSizer(job_box)

        self.nb.AddPage(self.log_panel, '信息')
        self.nb.AddPage(self.terminal_panel, '终端')
        self.nb.AddPage(self.job_panel, '任务管理器')
        self.nb.SetPageBitmap(0, wx.Bitmap('./icon/information.ico'))
        self.nb.SetPageBitmap(1, wx.Bitmap('./icon/terminal.ico'))
        self.nb.SetPageBitmap(2, wx.Bitmap('./icon/taskmanager.ico'))

        parent.get_mgr().AddPane(self.nb, aui.AuiPaneInfo().
                                     Name('log').Caption('信息区').CaptionVisible(False).BestSize((-1, 180)).
                                     Bottom().Layer(0).Position(0).CloseButton(False))
        parent.update()


    def reset_panel(self):
        """ 重置信息框 """
        self.frame.get_mgr().GetPane("log").Show()
        self.frame.update()

    def Debug(self, info):
        """ 调试 """
        if self.type_dict[self.type] < 1:
            self.log_text.SetDefaultStyle(wx.TextAttr(wx.Colour(88, 164, 176)))
            self.log_text.AppendText(time.strftime('%H:%M:%S') + '[ DEBUG: ] ' + str(info) + '\n')

    def Info(self, info):
        """ 信息 """
        if self.type_dict[self.type] < 2:
            self.log_text.SetDefaultStyle(wx.TextAttr(wx.BLUE))
            self.log_text.AppendText(time.strftime('%H:%M:%S') + '[ INFO: ] ' + str(info) + '\n')

    def Warning(self, info):
        """ 警告 """
        if self.type_dict[self.type] < 3:
            self.log_text.SetDefaultStyle(wx.TextAttr(wx.RED))
            self.log_text.AppendText(time.strftime('%H:%M:%S') + '[ WARNING: ] ' + str(info) + '\n')

    def Error(self, info):
        """ 错误 """
        if self.type_dict[self.type] < 4:
            self.log_text.SetDefaultStyle(wx.TextAttr(wx.Colour(255, 12, 25)))
            self.log_text.AppendText(time.strftime('%H:%M:%S') + '[ ERROR: ] ' + str(info) + '\n')

    def set_log_type(self, type):
        """ 设置信息类型 """
        self.type = type

    def read_data(self):
        if os.path.exists(self.work_dir):
            with open(self.work_dir, 'r') as f:
                self.ip = eval(f.read())['IP地址']

        self.relax_job_id = []
        self.relax_job_time = []
        if os.path.exists(os.path.join(self.job_dir, 'relax.txt')):
            with open(os.path.join(self.job_dir, 'relax.txt'), 'r') as f:
                for i in f.readlines():
                    if eval(i):
                        self.relax_job_id.append(eval(i)['任务编号'])
                        self.relax_job_time.append(eval(i)['开始时间'])
                    else:
                        pass

        self.scf_job_id = []
        self.scf_job_time = []
        if os.path.exists(os.path.join(self.job_dir, 'scf.txt')):
            with open(os.path.join(self.job_dir, 'scf.txt'), 'r') as f:
                for i in f.readlines():
                    if eval(i):
                        self.scf_job_id.append(eval(i)['任务编号'])
                        self.scf_job_time.append(eval(i)['开始时间'])
                    else:
                        pass

        self.band_job_id = []
        self.band_job_time = []
        if os.path.exists(os.path.join(self.job_dir, 'band.txt')):
            with open(os.path.join(self.job_dir, 'band.txt'), 'r') as f:
                for i in f.readlines():
                    if eval(i):
                        self.band_job_id.append(eval(i)['任务编号'])
                        self.band_job_time.append(eval(i)['开始时间'])
                    else:
                        pass

        self.dos_job_id = []
        self.dos_job_time = []
        if os.path.exists(os.path.join(self.job_dir, 'dos.txt')):
            with open(os.path.join(self.job_dir, 'dos.txt'), 'r') as f:
                for i in f.readlines():
                    if eval(i):
                        self.dos_job_id.append(eval(i)['任务编号'])
                        self.dos_job_time.append(eval(i)['开始时间'])
                    else:
                        pass

    def set_job_text(self):
        self.read_data()
        res = self.ssh.cmd('qstat')
        if res:
            res = res.strip().split('\r\n')
            for i in range(2, len(res)):
                print(res[i])
                job = res[i].strip().split(' ')[0]
                job_id = job.strip().split('.')[0]
                state = res[i].strip().split(' ')[-2]
                if self.index + 1 >= self.rows:
                    self.grid.AppendRows()
                    self.rows += 1
                self.index += 1
                if  job_id in self.relax_job_id and state != 'C':
                    self.grid.SetCellValue(self.index, 0, job_id)
                    self.grid.SetCellValue(self.index, 1, 'relax')
                    self.grid.SetCellValue(self.index, 2, self.ip)
                    self.grid.SetCellValue(self.index, 3, state)
                    self.grid.SetCellValue(self.index, 4,
                                           self.relax_job_time[self.relax_job_id.index(job_id)])

                elif job_id in self.scf_job_id and state != 'C':
                    self.grid.SetCellValue(self.index, 0, job_id)
                    self.grid.SetCellValue(self.index, 1, 'scf')
                    self.grid.SetCellValue(self.index, 2, self.ip)
                    self.grid.SetCellValue(self.index, 3, state)
                    self.grid.SetCellValue(self.index, 4,
                                           self.scf_job_time[self.scf_job_id.index(job_id)])

                elif job_id in self.band_job_id and state != 'C':
                    self.grid.SetCellValue(self.index, 0, job_id)
                    self.grid.SetCellValue(self.index, 1, 'band')
                    self.grid.SetCellValue(self.index, 2, self.ip)
                    self.grid.SetCellValue(self.index, 3, state)
                    self.grid.SetCellValue(self.index, 4,
                                           self.band_job_time[self.band_job_id.index(job_id)])

                elif job_id in self.dos_job_id and state != 'C':
                    self.grid.SetCellValue(self.index, 0, job_id)
                    self.grid.SetCellValue(self.index, 1, 'dos')
                    self.grid.SetCellValue(self.index, 2, self.ip)
                    self.grid.SetCellValue(self.index, 3, state)
                    self.grid.SetCellValue(self.index, 4,
                                           self.dos_job_time[self.dos_job_id.index(job_id)])

                elif state != 'C':
                    self.grid.SetCellValue(self.index, 0, job_id)
                    self.grid.SetCellValue(self.index, 1, 'vasp')
                    self.grid.SetCellValue(self.index, 2, self.ip)
                    self.grid.SetCellValue(self.index, 3, state)
                    self.grid.SetCellValue(self.index, 4, '未知')

                else:
                    self.sched.shutdown(wait=False)

        else:
            pass


    def state_display(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        try:
            self.sched = BackgroundScheduler()
            self.sched.add_job(self.set_job_text, 'interval', seconds=10)
            self.sched.start()
        except EnvironmentError as e:
            print(e)

    def set_terminal_text(self):
        """ 设置终端属性 """
        if os.path.exists(self.work_dir):
            with open(self.work_dir, 'r') as f:
                self.config = eval(f.read())
                self.ssh = SSH(self.config)
        else:
            pass
        self.prompt = '[iei@iei031 ~]$ '
        self.default_txt = self.terminal_text.GetDefaultStyle()
        self.terminal_text.AppendText(self.prompt)
        self.__bind_events()

    def __bind_events(self):
        self.terminal_panel.Bind(wx.EVT_TEXT_ENTER, self.__enter)

    def __enter(self, event):
        self.eval_last_line()

    def eval_last_line(self):
        self.ssh.connect()
        self.cmd = ''

        try:
            nl = self.terminal_text.GetNumberOfLines()
            ln = self.terminal_text.GetLineText(nl-1)
            ln = ln[len(self.prompt):]
            args = ln.split('//')
            cmd = args[0]
            if cmd == 'cd .':
                if self.cmd and len(self.cmd.split(';'))>=1:
                    cmds = self.cmd.strip().split(';')
                    cmds.pop(-1)
                    self.cmd = ';'.join(cmds)
                else:
                    pass
            elif cmd == 'cd ..':
                if self.cmd and len(self.cmd.split(';'))>=2:
                    cmds = self.cmd.strip().split(';')
                    cmds.pop(-1)
                    cmds.pop(-1)
                    self.cmd = ';'.join(cmds)
                else:
                    pass
            else:
                pass

            self.cmd = self.cmd + cmd + ';'
            res = self.ssh.cmd(self.cmd)
            self.terminal_text.AppendText('\n' + res)

            cmd_temp = ''
            for i in self.cmd.split(';'):
                if 'cd' in i and i not in ['cd .', 'cd ..']:
                    cmd_temp = cmd_temp + i + ';'
                else:
                    pass
            self.cmd = cmd_temp

            self.terminal_text.SetDefaultStyle(self.default_txt)
            self.terminal_text.AppendText(self.prompt)

        except EnvironmentError as e:
            print(e)

class SSH(object):

    def __init__(self, host_dict):
        """ 初始化 """
        self.host = host_dict['IP地址']
        self.port = host_dict['端口']
        self.username = host_dict['用户名']
        self.pwd = host_dict['密码']

    def connect(self):
        try:
            transport = paramiko.Transport((self.host, int(self.port),))
            transport.connect(username=self.username, password=self.pwd)
            self.__transport = transport
        except EnvironmentError as e:
            print(e)

    def cmd(self,command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
        # 获取命令结果
        res = to_str(stdout.read())
        # 获取错误信息
        error = to_str(stderr.read())
        # 如果有错误信息，返回error， 否则返回res
        if error.strip():
            return error
        else:
            return  res



def to_str(bytes_or_str):
    """
    把byte类型转换为str
    :return:
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str

    return value



