# -*- coding: utf-8 -*-
import os
# import platform
from ase.io import write
from Plugin.cif import read_cif
# from win32api import ShellExecute
import wx

def cif22xsf(modelfile, log=None):
    if log:
        print=log.Debug

    orig_dir = os.path.dirname(modelfile)
    filename = os.path.basename(modelfile)
    name, ext = os.path.splitext(filename)

    print('ASE.io.read ' + filename)
    try:
        atoms = read_cif(modelfile)
    except:
        print('ASE无法解析模型文件 ' + modelfile)
        return False

    if ext == '.xsf':
        filename = name + '.cif'
    else:
        filename = name + '.xsf'
    path_file = os.path.join(orig_dir, filename)

    print('ASE.io.write ' + path_file)
    try:
        write(path_file, atoms)
    except:
        print('ASE无法输出模型文件 ' + path_file)
        return False

    return path_file


def view_model(f_model, f_view_soft_path, ASEgui=True, log=None, path=''):
    file = os.path.basename(f_model)
    name, ext = os.path.splitext(file)
    if log:
        print=log.Debug

    try:
        if not ASEgui:
            raise AssertionError

        # 调用ASE\gui显示
        print('ASE\gui 显示模型 ' + file)
        try:
            if os.path.exists(f_model):
                cmd = os.path.join(os.getcwd(), 'Plugin','view_model.py')
                wx.Execute('python ' + cmd + ' -i ' + f_model, wx.EXEC_HIDE_CONSOLE)
            else:
                pass
        except:
            print('ASE\gui无法显示模型 ' + f_model)
            raise RuntimeError

    except:
        # 从view_set_dir.ini文件中读取第三方软件路径
        # 调用第三方软件显示结构模型
        view_model_exe = 'No_soft'
        if os.path.isfile(f_view_soft_path):
            with open(f_view_soft_path, 'r') as f:
                view_model_exe = f.read()
            if view_model_exe == '':
                view_model_exe = 'No_soft'

        # print('使用 ' + os.path.basename(view_model_exe) + ' 显示模型 ' + file)
        # sys = platform.system()
        # if sys == "Windows":
        #     viewexe = os.path.abspath(view_model_exe)
        #     ShellExecute(0, 'open', viewexe, f_model, '', 1)
        # else:
        #     print(view_model_exe + ' 无法显示模型 ' + f_model)
        #     return False
