# -*- coding: utf-8 -*-

import wx

import numpy as np

import matplotlib

# matplotlib采用WXAgg为后台,将matplotlib嵌入wxPython中
matplotlib.use("WXAgg")

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

myfont = fm.FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
matplotlib.rcParams['axes.unicode_minus'] = False


######################################################################################
class MPL_Panel_base(wx.Panel):
    ''' #MPL_Panel_base面板,可以继承或者创建实例'''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)

        self.Figure, self.axes = plt.subplots(figsize=(4, 3), dpi=80)
        self.FigureCanvas = FigureCanvas(self, -1, self.Figure)

        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.FigureCanvas, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.TopBoxSizer)

        ###方便调用
        self.np = np
        self.plt = plt

    def UpdatePlot(self):
        '''#修改图形的任何属性后都必须使用self.UpdatePlot()更新GUI界面 '''
        self.FigureCanvas.draw()

    def plot(self, *args, **kwargs):
        '''#最常用的绘图命令plot '''
        self.axes.plot(*args, **kwargs)
        self.UpdatePlot()

    def show(self):
        self.plt.show()

    def ion(self):
        """ 打开交互模式 """
        self.plt.ion()

    def ioff(self):
        """ 关闭交互模式 """
        self.plt.ioff()

    def pause(self,time):
        """ 暂停 """
        self.plt.pause(time)

    def semilogx(self, *args, **kwargs):
        ''' #对数坐标绘图命令 '''
        self.axes.semilogx(*args, **kwargs)
        self.UpdatePlot()

    def semilogy(self, *args, **kwargs):
        ''' #对数坐标绘图命令 '''
        self.axes.semilogy(*args, **kwargs)
        self.UpdatePlot()

    def loglog(self, *args, **kwargs):
        ''' #对数坐标绘图命令 '''
        self.axes.loglog(*args, **kwargs)
        self.UpdatePlot()

    def grid(self, flag=True):
        ''' ##显示网格  '''
        if flag:
            self.axes.grid()
        else:
            self.axes.grid(False)

    def title(self, TitleString="wxMatPlotLib Example In wxPython"):
        ''' # 给图像添加一个标题   '''
        self.axes.set_title(TitleString, fontproperties=myfont)

    def xlabel(self, XabelString="X"):
        ''' # Add xlabel to the plotting    '''
        self.axes.set_xlabel(XabelString, fontproperties=myfont)

    def ylabel(self, YabelString="Y"):
        ''' # Add ylabel to the plotting '''
        self.axes.set_ylabel(YabelString, fontproperties=myfont)

    def xticker(self,major_ticker=1.0,minor_ticker=0.1):
        ''' # 设置X轴的刻度大小 '''
        self.axes.xaxis.set_major_locator( MultipleLocator(major_ticker) )
        self.axes.xaxis.set_minor_locator( MultipleLocator(minor_ticker) )


    def yticker(self,major_ticker=1.0,minor_ticker=0.1):
        ''' # 设置Y轴的刻度大小 '''
        self.axes.yaxis.set_major_locator( MultipleLocator(major_ticker) )
        self.axes.yaxis.set_minor_locator( MultipleLocator(minor_ticker) )


    def legend(self, *args, **kwargs):
        ''' #图例legend for the plotting  '''
        self.axes.legend(prop=myfont, *args, **kwargs)

    def xlim(self, x_min, x_max):
        ''' # 设置x轴的显示范围  '''
        self.axes.set_xlim(x_min, x_max)

    def ylim(self, y_min, y_max):
        ''' # 设置y轴的显示范围   '''
        self.axes.set_ylim(y_min, y_max)

    def savefig(self, *args, **kwargs):
        ''' #保存图形到文件 '''
        self.Figure.savefig(*args, **kwargs)

    def cla(self):
        ''' # 再次画图前,必须调用该命令清空原来的图形  '''
        self.axes.clear()
        self.Figure.set_canvas(self.FigureCanvas)
        self.UpdatePlot()

    def axvline(self, *args, **kwargs):
        self.axes.axvline(*args, **kwargs)

    def axhline(self, *args, **kwargs):
        self.axes.axhline(*args, **kwargs)

    def xticks(self, *args, **kwargs):
        self.axes.set_xticks(*args, **kwargs)

    def xticklabels(self, *args, **kwargs):
        self.axes.set_xticklabels(*args, **kwargs)

