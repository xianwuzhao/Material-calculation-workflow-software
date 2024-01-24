import wx
import os
import time
from .work_panel import WorkPanel
from .work_connect import SSHConnection
from.display import Display

class WorkService:
    def __init__(self, app):
        self.app = app
        self.frame = app.frame
        self.log = app.log

        self.frame.get_menu_bar().Insert(5, self.add_work_menu(self.frame), '计算')
        self.work_dir = os.path.join(self.app.dir, r'Share\work_dir.ini')
        self.job_dir = os.path.join(self.app.dir,r'Share\job_id')
        self.log.Info('插件 work service 加载成功！')

        self.frame.update()

        # if os.path.exists(os.path.join(self.app.project.get_dir(), 'POSCAR')):
        #     with open(os.path.join(self.app.project.get_dir(), 'POSCAR'), 'r') as f:
        #         name = f.readline().strip('\n').split(' ')
        #         self.file_name = name[0]
        # else:
        #     self.file_name = 'VASP'
        self.file_name = os.path.basename(self.app.project.get_dir())
        print("self.filename is:",self.file_name)

    def add_work_menu(self, parent):
        """ 计算 """
        work_menu = wx.Menu()
        submenu = wx.Menu()
        remote_sub = wx.Menu()
        cal_sub = wx.Menu()
        work_config = submenu.Append(-1, '服务器配置')
        work_connect = submenu.Append(-1, '服务器连接')
        work_close = submenu.Append(-1, '服务器关闭')
        remote_sub.AppendSubMenu(submenu, '服务器')
        upload_file = remote_sub.Append(-1, '上传文件')
        download_file = remote_sub.Append(-1, '下载文件')
        dynamic_display = remote_sub.Append(-1, '实时显示')
        relax_cal = cal_sub.Append(-1, '优化')
        scf_cal = cal_sub.Append(-1, '自洽')
        band_cal = cal_sub.Append(-1, '能带')
        dos_cal = cal_sub.Append(-1, '态密度')
        ''''''
        op_cal = cal_sub.Append(-1, '光学计算')
        ''''''
        remote_sub.AppendSubMenu(cal_sub, '计算')
        work_menu.AppendSubMenu(remote_sub, '集群计算')
        local_cal = work_menu.Append(-1, '本地计算')

        self.frame.Bind(wx.EVT_MENU, self.OnWorkConfig, work_config)
        self.frame.Bind(wx.EVT_MENU, self.OnWorkConnect, work_connect)
        self.frame.Bind(wx.EVT_MENU, self.OnWorkClose, work_close)
        self.frame.Bind(wx.EVT_MENU, self.OnUploadFile, upload_file)
        self.frame.Bind(wx.EVT_MENU, self.OnDownloadFile, download_file)
        self.frame.Bind(wx.EVT_MENU, self.OnDynamicDisplay, dynamic_display)
        self.frame.Bind(wx.EVT_MENU, self.OnRelaxCal, relax_cal)
        self.frame.Bind(wx.EVT_MENU, self.OnScfCal, scf_cal)
        self.frame.Bind(wx.EVT_MENU, self.OnBandCal, band_cal)
        self.frame.Bind(wx.EVT_MENU, self.OnDosCal, dos_cal)
        ''''''
        self.frame.Bind(wx.EVT_MENU, self.OnOpCal, op_cal)
        ''''''
        self.frame.Bind(wx.EVT_MENU, self.OnLocalCal, local_cal)

        return work_menu

    def OnWorkConfig(self, event):
        """ 服务器配置 """
        self.log.Info('服务器配置中...')
        workconfig = WorkPanel(self.frame, self.app)
        if workconfig.ShowModal() == wx.ID_OK:
            workconfig.CenterOnScreen()
        else:
            pass

    def OnWorkConnect(self, event):
        """ 服务器连接 """
        self.log.Info('服务器连接中...')
        if os.path.exists(self.work_dir):
            with open(self.work_dir, 'r') as f:
                self.config = eval(f.read())
                self.ssh = SSHConnection(self.config, self.app)
        else:
            pass
        self.ssh.connect()
        self.log.set_terminal_text()

    def OnWorkClose(self, event):
        """ 服务器关闭 """
        self.ssh.close()
        self.log.Info('服务器连接已断开！')

    def OnUploadFile(self, event):
        """ 上传文件 """
        self.log.Info('文件上传中...')
        pro_path = self.app.project.get_dir()
        try:
            # 集群创建计算文件夹
            folders = self.ssh.listdir('/home/iei/lds')
            if self.file_name not in folders:
                folder_path = '/home/iei/lds/{0}'.format(self.file_name)
                self.ssh.mkdir(folder_path)

                def makefolder(path):
                    for i in os.listdir(path):
                        path1 = os.path.join(path, i)
                        if os.path.isfile(path1):
                            file_name = os.path.basename(path1)
                            name, ext = os.path.splitext(file_name)
                            if ext == '.cif' :
                                mat_folder_name = os.path.basename(os.path.dirname(path1))
                                mat_folder_path = '/home/iei/lds/{0}/{1}'.format(self.file_name, mat_folder_name)
                                self.ssh.mkdir(mat_folder_path)
                                ''''''
                                for i in ['band', 'dos', 'relax', 'scf','op']:
                                    ''''''
                                    folder_target_path = '/home/iei/lds/{0}/{1}/{2}'.format(self.file_name, mat_folder_name, i)
                                    self.ssh.mkdir(folder_target_path)
                        else:
                            makefolder(path1)

                makefolder(path=pro_path)


                # for i in ['band', 'dos', 'relax', 'scf']:
                #     folder_target_path = '/home/iei/lds/{0}/{1}'.format(self.file_name, i)
                #     self.ssh.mkdir(folder_target_path)

                # 传送文件
                def upload(path):
                    for i in os.listdir(path):
                        path1 = os.path.join(path, i)
                        if os.path.isfile(path1):
                            if i == 'INCAR' or i=='POSCAR':
                                folder = os.path.dirname(path1)
                                for j in os.listdir(folder):
                                    folder1 = os.path.basename(folder)
                                    folder2 = os.path.basename(os.path.dirname(folder))
                                    local_path = os.path.join(folder, j)
                                    target_path = '/home/iei/lds/{0}/{1}/{2}/{3}'.format(self.file_name, folder2, folder1,j)
                                    self.ssh.upload(local_path, target_path)
                                    self.log.Info('{0}已上传'.format(local_path))
                        else:
                            upload(path1)

                upload(pro_path)

                # for i in os.listdir(pro_path):
                #     file_path = os.path.join(pro_path, i)
                #     if os.path.isdir(file_path) and os.path.exists(file_path):
                #         for j in os.listdir(file_path):
                #             local_path = os.path.join(file_path, j)
                #             target_path = '/home/iei/lds/{0}/{1}/{2}'.format(self.file_name, i, j)
                #             self.ssh.upload(local_path, target_path)
                #     else:
                #         if i.split('.')[-1] != 'cif' or 'xsf':
                #             proj_path = ['relax', 'scf', 'band', 'dos']
                #             for k in proj_path:
                #                 if k == 'relax' and os.path.exists(os.path.join(pro_path, k)):
                #                     local_path = file_path
                #                     target_path = '/home/iei/lds/{0}/{1}/{2}'.format(self.file_name,k,i)
                #                     self.ssh.upload(local_path, target_path)
                #                 else:
                #                     if i != 'POSCAR' and os.path.exists(os.path.join(pro_path, k)):
                #                         local_path = file_path
                #                         target_path = '/home/iei/lds/{0}/{1}/{2}'.format(self.file_name,k, i)
                #                         self.ssh.upload(local_path, target_path)
                #                     else:
                #                         pass
                #
                #         else:
                #             pass

                self.log.Info('文件上传完成！')

            else:
                self.log.Info('{0}文件已存在！'.format(self.file_name))

        except EnvironmentError as e:
             self.log.Error(e)

    def OnDownloadFile(self, event):
        """ 下载文件 """
        self.log.Info('文件下载中...')
        p_path = self.app.project.get_dir()

        try:
            def download(path):
                for i in os.listdir(path):
                    path1 = os.path.join(path, i)
                    if os.path.isfile(path1):
                        file = ['vasprun.xml', 'OUTCAR']
                        file1 = ['CONTCAR', 'OUTCAR']
                        file3 = ['EXTINCTION.dat','REFRACTIVE.dat','ABSORPTION.dat','REFLECTIVITY.dat','ENERGY_LOSSSPECTRUM.dat']
                        folder = os.path.dirname(path1)
                        folder_name = os.path.basename(folder)
                        folder1_name = os.path.basename(os.path.dirname(folder))
                        if i in file1 and folder_name in ['relax', 'scf']:
                            target_path = '/home/iei/lds/{0}/{1}/{2}/{3}'.format(self.file_name, folder1_name, folder_name, i)
                            local_path = os.path.join(p_path, folder1_name)
                            local_path = os.path.join(local_path, folder_name)
                            local_path = os.path.join(local_path, i)
                            self.ssh.download(target_path, local_path)
                        elif i in file and folder_name in ['band', 'dos']:
                            target_path = '/home/iei/lds/{0}/{1}/{2}/{3}'.format(self.file_name, folder1_name, folder_name, i)
                            local_path = os.path.join(p_path, folder1_name)
                            local_path = os.path.join(local_path, folder_name)
                            local_path = os.path.join(local_path, i)
                            self.ssh.download(target_path, local_path)
                        elif i in file3 and folder_name in ['op']:
                            target_path = '/home/iei/lds/{0}/{1}/{2}/{3}'.format(self.file_name, folder1_name, folder_name, i)
                            local_path = os.path.join(p_path, folder1_name)
                            local_path = os.path.join(local_path, folder_name)
                            local_path = os.path.join(local_path, i)
                            self.ssh.download(target_path, local_path)
                        else:
                            pass
                    else:
                        download(path1)

            download(p_path)
            self.log.Info('文件下载完成！')
            self.app.project.update_tree()
        except EnvironmentError as e:
             self.log.Error(e)


                    # root_path = '/home/iei/lds/{0}'.format(self.file_name)
                    # proj_path = ['band', 'dos', 'relax', 'scf']
                    # file = ['vasprun.xml', 'OUTCAR']
                    # file1 = ['CONTCAR', 'OUTCAR']
                    # try:
                    #     for i in proj_path:
                    #         target_path0 = root_path
                    #         local_path0 = self.app.project.get_dir()
                    #
                    #         target_path1 = target_path0 + '/' + i
                    #         local_path1 = os.path.join(local_path0, i)
                    #         if os.path.exists(local_path1):
                    #             if i in ['band', 'dos']:
                    #                 for j in file:
                    #                     target_path = target_path1
                    #                     local_path = local_path1
                    #
                    #                     target_path = target_path + '/' + j
                    #                     local_path = os.path.join(local_path, j)
                    #                     self.ssh.download(target_path, local_path)
                    #             else:
                    #                 for j in file1:
                    #                     target_path = target_path1
                    #                     local_path = local_path1
                    #
                    #                     target_path = target_path + '/' + j
                    #                     local_path = os.path.join(local_path, j)
                    #                     self.ssh.download(target_path, local_path)
                    #         else:
                    #             self.log.Error('该文件不存在！')
                    #
                    #     self.log.Info('文件下载完成！')
                    #
                    #     self.app.project.update_tree()
                    # except EnvironmentError as e:
                    #     self.log.Error(e)


    def display(self):
        """ 离子步能量实时显示 """
        command = 'cd lds/{0}/relax/;'.format(self.file_name) + "grep F= OSZICAR |awk '{print $1,$5}'"
        res = self.ssh.run_cmd(command)
        try:
            if res:
                res = res.strip().split('\r\n')
                x, y = [], []
                for i in  res:
                    data = i.strip().split(' ')
                    x.append(float(data[0]))
                    y.append(float(data[1]))

                display = Display(self.app, x, y)
                display.datamonitor()
            else:
                pass

            command = 'cd lds/{0}/relax/;qstat'.format(self.file_name)
            res = self.ssh.run_cmd(command)
            res = res.strip().split('\r\n')
            for i in range(2, len(res)):
                job = res[i].strip().split(' ')[0]
                state = res[i].strip().split(' ')[-2]

                if job == self.relax_job and state == 'C':
                    self.sched.shutdown(wait=False)
                    self.log.Info('实时显示结束！')
                else:
                    pass
        except EnvironmentError as e:
            self.log.Error(e)

    def OnDynamicDisplay(self, event):
        """ 实时显示 """
        self.log.Info('实时显示运行中...')
        from apscheduler.schedulers.background import BackgroundScheduler
        try:
            self.sched = BackgroundScheduler()
            self.sched.add_job(self.display,'interval', seconds=30)
            self.sched.start()
        except EnvironmentError as e:
            self.log.Error(e)

    def OnRelaxCal(self, event):
        """ 优化计算 """
        def relax(path):
            cmds = []
            folders = self.ssh.listdir(path)
            if 'relax' in folders:
                cmd = path + '/' + 'relax' + '/'
                cmds.append(cmd)
            else:
                for i in folders:
                    path1 = path + '/' + i
                    relax(path1)

            return cmds

        path = '/home/iei/lds/{0}'.format(self.file_name)
        cmds = relax(path)

        for i in cmds:

            command = 'cd {0};qsub job.sh'.format(i)
            res = self.ssh.run_cmd(command)
            self.relax_job = res.strip().split('\r\n')[0]
            relax_job_id = self.relax_job.strip().split('.')[0]
            start_time = time.strftime('%H:%M:%S')
            keys = ['任务编号', '开始时间']
            values = [relax_job_id, start_time]
            data = dict(zip(keys, values))
            with open(os.path.join(self.job_dir, 'relax.txt'), 'a+') as f:
                f.write(str(data)+'\n')

            self.log.state_display()

    def OnScfCal(self, event):
        """ 自洽计算 """
        command = 'cd lds/{0}/scf/;qsub job.sh'.format(self.file_name)
        res = self.ssh.run_cmd(command)
        scf_job = res.strip().split('\r\n')[0]
        scf_job_id = scf_job.strip().split('.')[0]
        start_time = time.strftime('%H:%M:%S')
        keys = ['任务编号', '开始时间']
        values = [scf_job_id, start_time]
        data = dict(zip(keys, values))
        with open(os.path.join(self.job_dir, 'scf.txt'), 'a+') as f:
            f.write(str(data) + '\n')


    def OnBandCal(self, event):
        """ 能带计算 """
        command = 'cd lds/{0}/band/;qsub job.sh'.format(self.file_name)
        res = self.ssh.run_cmd(command)
        band_job = res.strip().split('\r\n')[0]
        band_job_id = band_job.strip().split('.')[0]
        start_time = time.strftime('%H:%M:%S')
        keys = ['任务编号', '开始时间']
        values = [band_job_id, start_time]
        data = dict(zip(keys, values))
        with open(os.path.join(self.job_dir, 'band.txt'), 'a+') as f:
            f.write(str(data) + '\n')


    def OnDosCal(self, event):
        """ 态密度计算 """
        command = 'cd lds/{0}/dos/;qsub job.sh'.format(self.file_name)
        res = self.ssh.run_cmd(command)
        dos_job = res.strip().split('\r\n')[0]
        dos_job_id = dos_job.strip().split('.')[0]
        start_time = time.strftime('%H:%M:%S')
        keys = ['任务编号', '开始时间']
        values = [dos_job_id, start_time]
        data = dict(zip(keys, values))
        with open(os.path.join(self.job_dir, 'dos.txt'), 'a+') as f:
            f.write(str(data) + '\n')


    def OnLocalCal(self, event):
        """ 本地计算 """
        try:
            item = self.app.project.tree.GetSelection()
            path = self.app.project.tree.GetItemData(item)
            if os.path.isdir(path):
                jobfoldname = path
            else:
                jobfoldname = os.path.dirname(path)
            job_file = os.path.join(path, jobfoldname)
            job_file = os.path.join(job_file, 'job.bat')
            if os.path.exists(job_file):
                self.log.Info('本地计算运行中...')
                wx.Execute('bash.exe ' + job_file, wx.EXEC_SHOW_CONSOLE)
                out_path = os.path.join(os.path.join(path, jobfoldname), 'temp')
                self.log.Info('计算输出路径：{0}'.format(out_path))
            else:
                self.log.Warning('本地计算脚本文件未生成！')

            self.app.project.update_tree()

        except:
            raise IOError


    def OnOpCal(self, event):
        """ 光学性质计算 """
        command = 'cd lds/{0}/op/;qsub job.sh'.format(self.file_name)
        res = self.ssh.run_cmd(command)
        op_job = res.strip().split('\r\n')[0]
        op_job_id = op_job.strip().split('.')[0]
        start_time = time.strftime('%H:%M:%S')
        keys = ['任务编号', '开始时间']
        values = [op_job_id, start_time]
        data = dict(zip(keys, values))
        with open(os.path.join(self.job_dir, 'op.txt'), 'a+') as f:
            f.write(str(data) + '\n')

def start():
    app = wx.GetApp()
    work = WorkService(app)
    return work
