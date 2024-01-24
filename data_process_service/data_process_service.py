import wx
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')

from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter, BSPlotterProjected, DosPlotter

from .plot_panel import PlotConfig
import pandas as pd

class DataProcessService:

    def __init__(self,app):
        self.frame = app.frame
        self.app = app
        self.project = app.project
        self.log = app.log

        self.frame.get_menu_bar().Insert(3, self.add_data_process_menu(self.frame), '数据处理')
        self.draw_config = os.path.join(self.app.dir, r'Share\datadraw_set.ini')
        self.log.Info('插件 data process service 加载成功！')

        self.frame.update()

        self.band_element = False
        self.band_orbit = False
        self.elements = []
        self.orbits = []

        self.dos_element = False
        self.dos_orbit = False

    def add_data_process_menu(self, parent):
        data_process_menu = wx.Menu()
        vasp_data_menu = wx.Menu()
        siesta_data_menu = wx.Menu()
        vasp_band_plot = vasp_data_menu.Append(-1, '能带图')
        vasp_dos_plot = vasp_data_menu.Append(-1, '态密度图')
        vasp_plot_config = vasp_data_menu.Append(-1, '绘图配置')
        ''''''
        vasp_op_plot = vasp_data_menu.Append(-1, '光学性质')
        ''''''
        data_process_menu.AppendSubMenu(vasp_data_menu, 'Vasp数据处理')
        siesta_band_plot = siesta_data_menu.Append(-1, '能带图')
        siesta_dos_plot = siesta_data_menu.Append(-1, '态密度图')
        siesta_plot_config = siesta_data_menu.Append(-1, '绘图配置')
        data_process_menu.AppendSubMenu(siesta_data_menu, 'Siesta数据处理')

        self.frame.Bind(wx.EVT_MENU, self.OnVaspBandPlot, vasp_band_plot)
        self.frame.Bind(wx.EVT_MENU, self.OnVaspDosPlot, vasp_dos_plot)
        self.frame.Bind(wx.EVT_MENU, self.OnVaspPlotConfig, vasp_plot_config)
        ''''''
        self.frame.Bind(wx.EVT_MENU, self.OnVaspOpPlot, vasp_op_plot)
        ''''''
        self.frame.Bind(wx.EVT_MENU, self.OnSiestaBandPlot, siesta_band_plot)
        self.frame.Bind(wx.EVT_MENU, self.OnSiestaDosPlot, siesta_dos_plot)
        self.frame.Bind(wx.EVT_MENU, self.OnSiestaPlotConfig, siesta_plot_config)

        return data_process_menu

    def OnVaspOpPlot(self, evnet):
        """ 光学性质 """
        for i in ['EXTINCTION.dat','REFRACTIVE.dat','ABSORPTION.dat','REFLECTIVITY.dat','ENERGY_LOSSSPECTRUM.dat']:
            dir_path = os.path.join(self.app.project.get_dir(), 'op')
            file = os.path.join(dir_path,i)
            name, ext = os.path.splitext(i)
            if os.path.exists(os.path.join(dir_path,name)):
                pass
            else:
                dir_path1=os.path.join(dir_path,name)
                os.mkdir(dir_path1)
            dir_path1=os.path.join(dir_path,name)
            if os.path.exists(file):
                dat=pd.read_table(file,sep="  ",skiprows=0,engine='python')
                dat.fillna('0', inplace = True)
                dat1 = dat.iloc[:,0:7]
                cnt = 1
                for j in ['xx','yy','zz','xy','yz','zx']:
                    if os.path.exists(os.path.join(dir_path1,j)):
                        pass
                    else:
                        os.mkdir(os.path.join(dir_path1,j))
                    dir_save_path=os.path.join(dir_path1,j)
                    fig1=plt.plot(dat1.iloc[0:1000,0],dat1.iloc[0:1000,cnt])
                    plt.savefig(os.path.join(dir_save_path, '{0}.png'.format(name)), format='png')
                    plt.cla()
                    plt.clf()
                    cnt = cnt+1
                self.log.Info('{0}绘制成功！'.format(i))
            else:
                self.log.Warning('{0}不存在， 无法绘制！'.format(i))
        self.project.update_tree()
        '''plot = self.app.plot.MPL
        plot.cla()
        plot.grid(False)
        plot.title('态密度图')
        plot.xlabel('Energy(eV)')
        plot.ylabel('DOS')
        plot.axvline(x=0, c="blue", ls="-", lw=1)

        with open(self.draw_config, 'r') as f:
            self.config_values = eval(f.read())
            self.xmin = self.config_values['xmin']
            self.xmax = self.config_values['xmax']

        xdata = []
        ydata = []
        with open(dos_data, 'r') as f:
            for eachline in f.readlines():
                xypair = eachline.strip().split()
                ydata.append(eval(xypair[2]))
                xdata.append(eval(xypair[1]) - eval(xypair[0]))

        plot.ylim(min(ydata) - 0.01, max(ydata) + 0.01)
        plot.xlim(float(self.xmin), float(self.xmax))

        plot.plot(xdata, ydata, color='r', linewidth=1)
'''
        '''
        try:
            if os.path.exists(file):
                op_vasprun = Vasprun(file, parse_projected_eigen=True)
                op_data = op_vasprun.dielectric(op_vasprun)
                if self.band_element and self.band_orbit:
                    bs_plot_element = BSPlotterProjected(bs=bs_data)
                    bs_plot_element.get_elt_projected_plots_color()
                    plt.savefig(os.path.join(self.app.project.get_dir(), 'op\\band_element.png'), format='png')

                    dots = dict(zip(self.elements, self.orbits))
                    bs_plot_orbit = BSPlotterProjected(bs=bs_data)
                    bs_plot_orbit.get_projected_plots_dots(dots)
                    plt.savefig(os.path.join(self.app.project.get_dir(), 'op\\band_orbit.png'), format='png')

                    bs_plot = BSPlotter(bs=bs_data)
                    bs_plot.get_plot()
                    bs_plot.save_plot(os.path.join(self.app.project.get_dir(), 'op\\band.png'), img_format='png')
                elif self.band_element and not self.band_orbit:
                    bs_plot_element = BSPlotterProjected(bs=bs_data)
                    bs_plot_element.get_elt_projected_plots_color()
                    plt.savefig(os.path.join(self.app.project.get_dir(), 'op\\band_element.png'), format='png')

                    bs_plot = BSPlotter(bs=bs_data)
                    bs_plot.get_plot()
                    bs_plot.save_plot(os.path.join(self.app.project.get_dir(), 'op\\band.png'), img_format='png')
                elif not self.band_element and self.band_orbit:
                    dots = dict(zip(self.elements, self.orbits))
                    bs_plot_orbit = BSPlotterProjected(bs=bs_data)
                    bs_plot_orbit.get_projected_plots_dots(dots)
                    plt.savefig(os.path.join(self.app.project.get_dir(), 'op\\band_orbit.png'), format='png')

                    bs_plot = BSPlotter(bs=bs_data)
                    bs_plot.get_plot()
                    bs_plot.save_plot(os.path.join(self.app.project.get_dir(), 'op\\band.png'), img_format='png')
                else:
                    bs_plot = BSPlotter(bs=bs_data)
                    bs_plot.get_plot()
                    bs_plot.save_plot(os.path.join(self.app.project.get_dir(), 'op\\band.png'), img_format='png')

                self.project.update_tree()
                self.log.Info('能带图成功保存！')
            else:
                self.log.Warning('该文件不存在， 无法绘制能带图！')

        except EnvironmentError as e:
            self.log.Error(e)
            '''




    def OnVaspBandPlot(self, evnet):
        """ 能带图 """
        file = os.path.join(self.app.project.get_dir(), 'band/vasprun.xml')
        try:
            if os.path.exists(file):
                bs_vasprun = Vasprun(file, parse_projected_eigen=True)
                bs_data = bs_vasprun.get_band_structure(line_mode=1)
                if self.band_element and self.band_orbit:
                    bs_plot_element = BSPlotterProjected(bs=bs_data)
                    bs_plot_element.get_elt_projected_plots_color()
                    plt.savefig(os.path.join(self.app.project.get_dir(), 'band/band_element.png'), format='png')

                    dots = dict(zip(self.elements, self.orbits))
                    bs_plot_orbit = BSPlotterProjected(bs=bs_data)
                    bs_plot_orbit.get_projected_plots_dots(dots)
                    plt.savefig(os.path.join(self.app.project.get_dir(), 'band/band_orbit.png'), format='png')

                    bs_plot = BSPlotter(bs=bs_data)
                    bs_plot.get_plot()
                    bs_plot.save_plot(os.path.join(self.app.project.get_dir(), 'band/band.png'), img_format='png')
                elif self.band_element and not self.band_orbit:
                    bs_plot_element = BSPlotterProjected(bs=bs_data)
                    bs_plot_element.get_elt_projected_plots_color()
                    plt.savefig(os.path.join(self.app.project.get_dir(), 'band/band_element.png'), format='png')

                    bs_plot = BSPlotter(bs=bs_data)
                    bs_plot.get_plot()
                    bs_plot.save_plot(os.path.join(self.app.project.get_dir(), 'band/band.png'), img_format='png')
                elif not self.band_element and self.band_orbit:
                    dots = dict(zip(self.elements, self.orbits))
                    bs_plot_orbit = BSPlotterProjected(bs=bs_data)
                    bs_plot_orbit.get_projected_plots_dots(dots)
                    plt.savefig(os.path.join(self.app.project.get_dir(), 'band/band_orbit.png'), format='png')

                    bs_plot = BSPlotter(bs=bs_data)
                    bs_plot.get_plot()
                    bs_plot.save_plot(os.path.join(self.app.project.get_dir(), 'band/band.png'), img_format='png')
                else:
                    bs_plot = BSPlotter(bs=bs_data)
                    bs_plot.get_plot()
                    bs_plot.save_plot(os.path.join(self.app.project.get_dir(), 'band/band.png'), img_format='png')

                self.project.update_tree()
                self.log.Info('能带图成功保存！')
            else:
                self.log.Warning('该文件不存在， 无法绘制能带图图！')

        except EnvironmentError as e:
            self.log.Error(e)


    def OnVaspDosPlot(self, event):
        """ 态密度图 """
        file = os.path.join(self.app.project.get_dir(), 'dos/vasprun.xml')
        try:
            if os.path.exists(file):
                dos_vasprun = Vasprun(file)
                dos_data = dos_vasprun.complete_dos
                dos_plot = DosPlotter(stack=False, sigma=0.5)
                dos_plot.add_dos('total dos', dos=dos_data)
                if self.dos_element and self.dos_orbit:
                    dos_plot_element = DosPlotter(stack=False, sigma=0.5)
                    dos_plot_element.add_dos('total dos', dos=dos_data)
                    dos_plot_element.add_dos_dict(dos_data.get_element_dos())
                    dos_plot_element.save_plot(os.path.join(self.app.project.get_dir(), 'dos/dos_element.png'), img_format='png')

                    dos_plot_orbit = DosPlotter(stack=False, sigma=0.5)
                    dos_plot_orbit.add_dos('total dos', dos=dos_data)
                    dos_plot_orbit.add_dos_dict(dos_data.get_spd_dos())
                    dos_plot_orbit.save_plot(os.path.join(self.app.project.get_dir(), 'dos/dos_orbit.png'), img_format='png')

                    dos_plot = DosPlotter(stack=False, sigma=0.5)
                    dos_plot.add_dos('total dos', dos=dos_data)
                    dos_plot.save_plot(os.path.join(self.app.project.get_dir(), 'dos/dos.png'), img_format='png')
                elif self.dos_element and not self.dos_orbit:
                    dos_plot_element = DosPlotter(stack=False, sigma=0.5)
                    dos_plot_element.add_dos('total dos', dos=dos_data)
                    dos_plot_element.add_dos_dict(dos_data.get_element_dos())
                    dos_plot_element.save_plot(os.path.join(self.app.project.get_dir(), 'dos/dos_element.png'),img_format='png')

                    dos_plot = DosPlotter(stack=False, sigma=0.5)
                    dos_plot.add_dos('total dos', dos=dos_data)
                    dos_plot.save_plot(os.path.join(self.app.project.get_dir(), 'dos/dos.png'), img_format='png')
                elif not self.dos_element and self.dos_orbit:
                    dos_plot_orbit = DosPlotter(stack=False, sigma=0.5)
                    dos_plot_orbit.add_dos('total dos', dos=dos_data)
                    dos_plot_orbit.add_dos_dict(dos_data.get_spd_dos())
                    dos_plot_orbit.save_plot(os.path.join(self.app.project.get_dir(), 'dos/dos_orbit.png'),img_format='png')

                    dos_plot = DosPlotter(stack=False, sigma=0.5)
                    dos_plot.add_dos('total dos', dos=dos_data)
                    dos_plot.save_plot(os.path.join(self.app.project.get_dir(), 'dos/dos.png'), img_format='png')
                else:
                    dos_plot = DosPlotter(stack=False, sigma=0.5)
                    dos_plot.add_dos('total dos', dos=dos_data)
                    dos_plot.save_plot(os.path.join(self.app.project.get_dir(), 'dos/dos.png'), img_format='png')
                self.project.update_tree()
                self.log.Info('态密度图成功保存！')
            else:
                self.log.Warning('该文件不存在， 无法绘制态密度图！')

        except EnvironmentError as e:
            self.log.Error(e)


    def OnVaspPlotConfig(self, event):
        """ 绘图配置 """
        plotconfig = PlotConfig(self.frame, self.app)
        if plotconfig.ShowModal() == wx.OK:
            plotconfig.CenterOnScreen()
        else:
            self.dos_element = plotconfig.dos_element
            self.dos_orbit = plotconfig.dos_orbit

            self.band_element = plotconfig.band_element
            self.band_orbit = plotconfig.band_orbit

            for i in [plotconfig.element1, plotconfig.element2,
                      plotconfig.element3, plotconfig.element4, plotconfig.element5]:
                if i != '':
                    self.elements.append(i)
                else:
                    pass

            for j in [plotconfig.orbit1, plotconfig.orbit2,
                      plotconfig.orbit3, plotconfig.orbit4, plotconfig.orbit5]:
                if j != '':
                    self.orbits.append(list(j))
                else:
                    pass

    def OnSiestaBandPlot(self, event):
        item = self.app.project.tree.GetSelection()
        path = self.app.project.tree.GetItemData(item)
        if os.path.isdir(path):
            proj_dir = path
        else:
            proj_dir = os.path.dirname(path)
        band_data = os.path.join(proj_dir, 'band.dat')
        K_Pointsfile = os.path.join(proj_dir, 'band.confg')

        plot = self.app.plot.MPL
        plot.cla()
        plot.grid(False)
        plot.title('能带图')
        plot.xlabel('Kpoints')
        plot.ylabel('Energy(eV)')

        k_data = []
        k_label = []

        with open(K_Pointsfile, 'r') as f:
            for eachline in f.readlines():
                kdata = eachline.split()
                k_data.append(eval(kdata[0]))
                k_label.append(kdata[1])

        for i in range(len(k_data)):
            plot.axvline(x=k_data[i], c="blue", ls="-", lw=1)
        plot.axhline(y=0, c="r", ls="--", lw=1)
        plot.xticks(k_data)
        plot.xticklabels(k_label)

        with open(self.draw_config, 'r') as f:
            self.config_values = eval(f.read())
            self.ymin = self.config_values['ymin']
            self.ymax = self.config_values['ymax']

        n = 0
        with open(band_data, 'r') as f:
            n = len(f.readline().strip().split())

        for i in range(n - 2):
            xdata = []
            ydata = []
            with open(band_data, 'r') as f:
                for eachline in f.readlines():
                    xypair = eachline.strip().split()
                    ydata.append(eval(xypair[i + 2]) - eval(xypair[0]))
                    xdata.append(eval(xypair[1]))

                plot.ylim(float(self.ymin), float(self.ymax))
                plot.xlim(k_data[0], k_data[-1])
                plot.plot(xdata, ydata, color='black', linewidth=1)

    def OnSiestaDosPlot(self, event):
        item = self.app.project.tree.GetSelection()
        path = self.app.project.tree.GetItemData(item)
        if os.path.isdir(path):
            proj_dir = path
        else:
            proj_dir = os.path.dirname(path)
        dos_data = os.path.join(proj_dir, 'dos.dat')
        plot = self.app.plot.MPL
        plot.cla()
        plot.grid(False)
        plot.title('态密度图')
        plot.xlabel('Energy(eV)')
        plot.ylabel('DOS')
        plot.axvline(x=0, c="blue", ls="-", lw=1)

        with open(self.draw_config, 'r') as f:
            self.config_values = eval(f.read())
            self.xmin = self.config_values['xmin']
            self.xmax = self.config_values['xmax']

        xdata = []
        ydata = []
        with open(dos_data, 'r') as f:
            for eachline in f.readlines():
                xypair = eachline.strip().split()
                ydata.append(eval(xypair[2]))
                xdata.append(eval(xypair[1]) - eval(xypair[0]))

        plot.ylim(min(ydata) - 0.01, max(ydata) + 0.01)
        plot.xlim(float(self.xmin), float(self.xmax))

        plot.plot(xdata, ydata, color='r', linewidth=1)

    def OnSiestaPlotConfig(self, evnet):
        self.app.editor.open_file(self.draw_config)



def start():
    app = wx.GetApp()
    data_process = DataProcessService(app)
    return data_process