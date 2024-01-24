import wx
import os
import shutil
from .vasp_relax_nb import RELAX
from .vasp_scf_nb import SCF
from .vasp_band_nb import BAND
from .vasp_dos_nb import DOS
from .vasp_op_nb import OP
from .vasp_job_nb import JOB
from .siesta_relax_nb import relax
from .siesta_band_nb import band
from .siesta_dos_nb import dos
from .siesta_job_nb import job
from .siesta_scf_nb import scf
from .siesta_denchar_nb import denchar
from math import sqrt
from ase.io import xsf
import configparser

_e = 1.60217733e-19          # elementary charge
_amu = 1.6605402e-27         # atomic mass unit, kg
second = 1e10 * sqrt(_e / _amu)
fs = 1e-15 * second

class VaspSiestaService:

    def __init__(self,app):
        self.frame = app.frame
        self.app = app
        self.project = app.project
        self.log = app.log

        self.frame.get_menu_bar().Insert(3, self.add_module_menu(self.frame), '模块')
        self.log.Info('插件 vasp siesta service 加载成功！')

        self.frame.update()

    def add_module_menu(self, parent):
        """ 模块 """
        module_menu = wx.Menu()

        vasp_cal = module_menu.Append(-1, 'Vasp计算配置')
        siesta_cal = module_menu.Append(-1, 'Siesta计算配置')

        parent.Bind(wx.EVT_MENU, self.OnSiesta, siesta_cal)

        parent.Bind(wx.EVT_MENU, self.OnVasp, vasp_cal)

        return module_menu

    def OnVasp(self, event):
        """ VASP计算配置 """
        configdlg = VaspConfig(self.frame, self.app)
        if configdlg.ShowModal() == wx.ID_OK:
            configdlg.CenterOnScreen()
        else:
            pass

    def OnSiesta(self, event):
        """ Siesta计算配置 """
        configdlg = SiestaConfig(self.frame, self.app)
        if configdlg.ShowModal() == wx.ID_OK:
            configdlg.CenterOnScreen()
        else:
            pass


class VaspConfig(wx.Dialog):
    """ VASP计算配置界面 """

    def __init__(self, parent, app):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE)

        self.app = app
        self.log = app.log
        self.path = self.app.project.get_dir()


        self.InitUI()
        nb = wx.Notebook(self, -1)
        self.relax = RELAX(nb, -1, self.path)
        self.scf = SCF(nb, -1, self.path)
        self.band = BAND(nb, -1, self.path)
        self.dos = DOS(nb, -1, self.path)
        self.op = OP(nb, -1, self.path)
        self.job = JOB(nb, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnok = wx.Button(self, wx.ID_OK, '确定')
        btncancel = wx.Button(self, wx.ID_CANCEL, '取消')
        btnsizer.Add(btnok, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        btnsizer.Add(btncancel, 0, flag=wx.ALIGN_LEFT| wx.EXPAND, border=0)
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
        self.SetTitle(title='VASP计算配置')
        self.Centre()

    def OnOk(self, event):
        self.relax.WriteRelax(self.path)
        self.scf.WriteScf(self.path)
        self.band.WriteBand(self.path)
        self.dos.WriteDos(self.path)
        self.op.WriteOp(self.path)
        self.job.WriteJob(self.path)
        self.app.project.update_tree()

        self.Destroy()


class SiestaConfig(wx.Dialog):
    """ Siesta计算配置界面 """

    def __init__(self, parent, app, reconfig=False):
        wx.Dialog.__init__(self, parent, -1, style = wx.DEFAULT_DIALOG_STYLE)

        self.app = app
        self.log = app.log
        self.path = self.app.project.get_dir()
        self.pro_num = 1
        self.reconfig = reconfig

        if self.reconfig:
            self.tre = self.app.project.tree
            self.jobfold = os.path.dirname(self.tre.GetItemData(self.tre.GetSelection()))
            self.profold = self.jobfold.split(os.sep)[-1]
            self.model = os.path.join(self.jobfold, 'model.xsf')
            with open(self.model, 'r') as f:
                self.atoms = xsf.read_xsf(f, read_data=False)
        else:
            for i in os.listdir(self.path):
                ext = i.split('_')[-1]
                path1 = os.path.join(self.path, i)
                if os.path.isdir(path1) and ext == 'org':
                    for i in os.listdir(path1):
                        if i.strip().split('.')[-1] == 'xsf':
                            self.model = os.path.join(path1, i)
                            with open(os.path.join(path1, i)) as f:
                                self.atoms = xsf.read_xsf(f, read_data=False)
                else:
                    if i.strip().split('.')[-1] == 'xsf':
                        self.model = os.path.join(path1, i)
                        with open(os.path.join(path1, i)) as f:
                            self.atoms = xsf.read_xsf(f, read_data=False)

        self.InitUI()
        nb = wx.Notebook(self, -1)
        self.relax = relax(nb, -1, self.atoms)
        self.scf = scf(nb, -1, self.atoms)
        self.denchar = denchar(nb, -1, self.atoms)
        self.band = band(nb, -1, self.atoms)
        self.dos = dos(nb, -1, self.atoms)
        self.job = job(nb, -1, self.atoms)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        btnok = wx.Button(self, wx.ID_OK, '确定')
        btncancel = wx.Button(self, wx.ID_CANCEL, '取消')
        btnsizer.Add(btnok, 0, flag=wx.ALIGN_LEFT | wx.EXPAND, border=0)
        btnsizer.Add(btncancel, 0, flag=wx.ALIGN_LEFT| wx.EXPAND, border=0)
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, 5)
        btnok.Bind(wx.EVT_BUTTON, self.OnOk)
        self.SetSizer(sizer)
        self.Layout()
        self.Fit()

        if self.reconfig:
            filepath = self.tre.GetItemData(self.tre.GetSelection())
            self.relax.doReConfig(filepath)
            self.scf.doReConfig(filepath)
            self.denchar.doReConfig(filepath)
            self.band.doReConfig(filepath)
            self.dos.doReConfig(filepath)
            self.job.doReConfig(filepath)

    def InitUI(self):
        """ 初始化主界面 """
        icon = os.getcwd() + '\\icon\\MIDIS.ico'
        icon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
        icon.SetHeight(18)
        icon.SetWidth(18)
        self.SetIcon(icon)
        self.SetTitle(title='Siesta计算配置')
        self.Centre()

    def CreatJobFold(self):
        if self.reconfig:
            return
        dirs = os.listdir(self.path)
        for i in dirs:
            path1 = os.path.join(self.path, i)
            if os.path.isdir(path1):
                fold = []
                for file in os.listdir(path1):
                    if os.path.isdir(os.path.join(path1, file)):
                        fold.append(file)
                if fold:
                    num = fold[-1].strip().split('-')[1]
                    self.pro_num = int(num) + 1

        modelname = os.listdir(self.path)[0].strip().split('.')[0]
        jobstyle = 'Siesta'
        jobfoldname = str(modelname) + '_' + jobstyle

        jobfoldname = '{0}-{1}'.format(jobfoldname, self.pro_num)

        if os.path.exists(os.path.join(self.path, jobfoldname)):
            self.app.log.Warning('任务文件夹已存在！')
        else:
            os.makedirs(os.path.join(self.path, jobfoldname))

        self.projfold = jobfoldname
        self.jobfold = os.path.join(self.path, jobfoldname)

    def CreatJobFiles(self):
        if self.reconfig:
            return

        model2xyz = os.path.join(self.jobfold, 'model.xyz')
        model2xsf = os.path.join(self.jobfold, 'model.xsf')

        shutil.copyfile(self.model, model2xsf)
        model_cif = self.model.replace('.xsf', '.cif')
        shutil.copyfile(model_cif, os.path.join(self.jobfold, 'model.cif'))
        numbers = self.atoms.get_atomic_numbers().copy()
        species = []
        for Z in numbers:
            if Z not in species:
                species.append(Z)
        with open(model2xyz, 'a+') as f:
            for s, (x, y, z) in zip(numbers, self.atoms.get_positions()):
                f.write('%22.15f %22.15f %22.15f %s\n' % (x, y, z, species.index(s) + 1))


    def OnOk(self, event):
        isrelax = self.relax.cb.GetValue()
        isscf = self.scf.cb.GetValue()
        isdenchar = self.denchar.cb.GetValue()
        isband = self.band.cb.GetValue()
        isdos = self.dos.cb.GetValue()

        if isdenchar and not isscf:
            mgl = wx.MessageDialog(self, 'Denchar计算需要使用scf参数，将默认选择scf，请注意检查scf配置！', '提示', wx.YES_NO | wx.ICON_QUESTION)
            mgl.CenterOnParent()
            state = mgl.ShowModal()
            if state == wx.ID_YES:
                self.scf.scf.SetValue(True)
                isscf = True
            else:
                return

        if isband and not isscf:
            mgl = wx.MessageDialog(self,
                                   'Band计算需要使用scf参数，将默认选择scf，请注意检查scf配置！', '提示',
                                   wx.YES_NO | wx.ICON_QUESTION)
            mgl.CenterOnParent()
            state = mgl.ShowModal()
            if state == wx.ID_YES:
                self.scf.cb.SetValue(True)
                isscf = True
            else:
                return

        if isdos and not isscf:
            mgl = wx.MessageDialog(self,
                                   'Dos计算需要使用scf参数，将默认选择scf，请注意检查scf配置！', '提示',
                                   wx.YES_NO | wx.ICON_QUESTION)
            mgl.CenterOnParent()
            state = mgl.ShowModal()
            if state == wx.ID_YES:
                self.scf.cb.SetValue(True)
                isscf = True
            else:
                return

        self.CreatJobFold()
        self.CreatJobFiles()
        if isrelax:
            relaxfile = os.path.join(self.jobfold, 'relax.fdf')
            relaxsiesta = Siesta(self.atoms, self.relax.GetParas(), self.relax.GetKpts())
            relaxsiesta.write_fdf(relaxfile)

            relaxoutfile = os.path.join(self.jobfold, 'relax.out')
            with open(relaxoutfile, 'w') as f:
                f.write('')

            relaxoutEFfile = os.path.join(self.jobfold, 'relax.outEF')
            with open(relaxoutEFfile, 'w') as f:
                f.write('')

            relaxstruct = os.path.join(self.jobfold, 'model_rlx.xsf')
            with open(relaxstruct, 'w') as f:
                f.write('')

        if isscf:
            scffile = os.path.join(self.jobfold, 'scf.fdf')
            scfpara = self.scf.GetParas()
            scfoutfile = os.path.join(self.jobfold, 'scf.out')
            with open(scfoutfile, 'w') as f:
                f.write('')

            scfoutEFfile = os.path.join(self.jobfold, 'scf.outEF')
            with open(scfoutEFfile, 'w') as f:
                f.write('')

            bandstr = ''
            dosstr = ''
            if isdenchar:
                scfpara.update(self.denchar.GetParas())
                self.denchar.rho2xsf(os.path.join(self.jobfold, 'rho.bat'), self.model)
                dencharoutfile = os.path.join(self.jobfold, 'denchar.out')
                with open(dencharoutfile, 'w') as f:
                    f.write('')


            if isband:
                bandstr = self.band.Getbandstr()
                bandfile = os.path.join(self.jobfold, 'band.dat')
                with open(bandfile, 'w') as f:
                    f.write('')
            if isdos:
                dosstr = self.dos.Getdosstr()
                dosfile = os.path.join(self.jobfold, 'dos.dat')
                with open(dosfile, 'w') as f:
                    f.write('')

            configfile = os.path.join(self.jobfold, 'Siesta.cfg')
            conf = configparser.RawConfigParser()
            conf.add_section('general')
            conf.set('general', 'servicename', 'SiestaService')

            self.relax.SaveConfig(conf)
            self.scf.SaveConfig(conf)
            self.denchar.SaveConfig(conf)
            self.band.SaveConfig(conf)
            self.dos.SaveConfig(conf)
            self.job.SaveConfig(conf)

            with open(configfile, 'w') as f:
                conf.write(f)

            scfsiesta = Siesta(self.atoms, scfpara, self.scf.GetKpts(), self.dos.GetKpts())
            scfsiesta.write_fdf(scffile, scf=True, band=isband, bandstr=bandstr, dos=isdos, dosstr=dosstr)

        work_file = os.path.join(self.jobfold, r'job.bat')
        filestr = self.job.GetJobWinBatstr(self.jobfold, isrelax=isrelax, isscf=isscf, isdenchar=isdenchar, isdos=isdos,
                                           isband=isband)
        with open(work_file, 'w') as f:
            f.write(str(filestr))

        self.log.Info('计算文件生成成功！')
        self.app.project.update_tree()
        self.Destroy()


class Siesta:

    def __init__(self, atom, fdf={}, kpts=None, pkpts=None, ghosts=[]):
        self.name = 'Siesta'
        self.atom = atom
        self.kpts = kpts
        self.pkpts = pkpts
        self.fdf = fdf
        self.ghosts = ghosts
        self.e_fermi = None
        self.setallparas()

    def set_fdf(self, key, value):
        self.fdf[key] = value

    def write_fdf(self, filepath, scf=False, band=False, bandstr='', dos=False, dosstr=''):
        fdf = self.parasdict
        atoms = self.atom
        self.positions = atoms.get_positions().copy()
        self.cell = atoms.get_cell().copy()
        self.pbc = atoms.get_pbc().copy()

        self.numbers = atoms.get_atomic_numbers().copy()
        self.species = []
        for a, Z in enumerate(self.numbers):
            if a in self.ghosts:
                Z = -Z
            if Z not in self.species:
                self.species.append(Z)

        with open(filepath, 'a+') as f:
            fdf['NumberOfAtoms'] = len(atoms)

            if self.fdf['XC.functional'] != 'LDA':
                fdf['XC.authors'] = 'PBE'
            else:
                fdf['XC.authors'] = 'CA'

            magmoms = atoms.get_initial_magnetic_moments()
            if magmoms.any():
                fdf['SpinPolarized'] = True
                f.write('%block InitSpin\n')
                for n, M in enumerate(magmoms):
                    if M != 0:
                        f.write('%d %.14f\n' % (n+1, M))
                f.write('%endblock InitSpin\n')

            fdf['NumberOfSpecies'] = len(self.species)
            fdf.update(self.fdf)

            for section in self.parasdict['general']:
                f.write('\n# %s\n'%section)
                for item in self.parasdict[section]:
                    key = item
                    value = fdf[key]
                    if value is None:
                        continue
                    if isinstance(value, list):
                        f.write('%%block %s\n' % key)
                        for line in value:
                            f.write(line + '\n')
                        f.write('%%endblock %s\n' % key)
                    else:
                        unit =keys_with_units.get(fdfify(key))
                        if unit is None:
                            f.write('%s %s\n' % (key, value))
                        else:
                            if 'fs**2' in unit:
                                value /= fs**2
                            elif 'fs' in unit:
                                value /= fs
                            f.write('%s %f %s\n' % (key, float(value), unit))
            f.write('\n%block LatticeVectors\n')
            for v in self.cell:
                f.write('%.14f %.14f %.14f\n' % tuple(v))
            f.write('%endblock LatticeVectors\n')

            f.write('\n%block Chemical_Species_label\n')
            for n, Z in enumerate(self.species):
                f.write('%d %s %s\n' % (n + 1, Z, chemical_symbols[abs(Z)]))
            f.write('%endblock Chemical_Species_label\n')

            if scf:
                f.write('\n%block AtomicCoordinatesAndAtomicSpecies < scf.xyz\n')
            else:
                f.write('\n%block AtomicCoordinatesAndAtomicSpecies < model.xyz\n')

            if self.kpts is not None:
                f.write('\n%block kgrid_Monkhorst_Pack\n')
                for i in range(3):
                    for j in range(3):
                        if i == j:
                            f.write('%d ' % self.kpts[i])
                        else:
                            f.write('0 ')
                    f.write('%.1f\n' % (((self.kpts[i] + 1) % 2) * 0.5))
                f.write('%endblock kgrid_Monkhorst_Pack\n')

            if band:
                f.write('\n%block BandLines\n')
                f.write(bandstr)
                f.write('%endblock BandLines\n')

            if dos:
                f.write('\n%block ProjectedDensityOfStates\n')
                f.write(dosstr)
                f.write('%endblock ProjectedDensityOfStates\n')

            if self.pkpts is not None and dos:
                f.write('\n%block PDOS.kgrid_Monkhorst_Pack\n')
                for i in range(3):
                    for j in range(3):
                        if i == j:
                            f.write('%d ' % self.pkpts[i])
                        else:
                            f.write('0 ')
                    f.write('%.1f\n' % (((self.pkpts[i] + 1) % 2) * 0.5))
                f.write('%endblock PDOS.kgrid_Monkhorst_Pack\n')

    def setallparas(self):
        parafile = os.path.join(os.path.join(os.getcwd(), 'Share'), 'siesta_paras.txt')
        self.conf_para = configparser.ConfigParser()
        self.conf_para.read(parafile)
        self.parasdict = {}
        self.paraslist = []
        self.parasdict['general'] = self.conf_para.get('general', 'sections').strip().split(', ')
        for section in self.parasdict['general']:
            self.parasdict[section] = self.conf_para.get(section, 'paras').strip().split(', ')
            for item in self.parasdict[section]:
                self.parasdict[item] = None
            self.paraslist += self.parasdict[section]



def fdfify(key):
    return key.lower().replace('_', '').replace('.', '').replace('-', '')

keys_with_units = {
    'paoenergyshift': 'eV',
    'zmunitslength': 'Bohr',
    'zmunitsangle': 'rad',
    'zmforcetollength': 'eV/Ang',
    'zmforcetolangle': 'eV/rad',
    'zmmaxdispllength': 'Ang',
    'zmmaxdisplangle': 'rad',
    'meshcutoff': 'Ry',
    'dmenergytolerance': 'eV',
    'electronictemperature': 'meV',
    'oneta': 'eV',
    'onetaalpha': 'eV',
    'onetabeta': 'eV',
    'onrclwf': 'Ang',
    'onchemicalpotentialrc': 'Ang',
    'onchemicalpotentialtemperature': 'eV',
    'mdmaxcgdispl': 'Ang',
    'mdmaxforcetol': 'eV/Ang',
    'mdmaxstresstol': 'GPa',
    'mdlengthtimestep': 'fs',
    'mdinitialtemperature': 'eV',
    'mdtargettemperature': 'eV',
    'mdtargetpressure': 'GPa',
    'mdnosemass': 'eV*fs**2',
    'mdparrinellorahmanmass': 'eV*fs**2',
    'mdtaurelax': 'fs',

	###WANGQI
    'mdbulkmodulus': 'eV/Ang**3',
	###WANGQI DONE

    'mdfcdispl': 'Ang',
    'warningminimumatomicdistance': 'Ang',
    'rcspatial': 'Ang',
    'kgridcutoff': 'Ang',
    'latticeconstant': 'Ang',
    'dencharminx':'Ang',
    'dencharmaxx':'Ang',
    'dencharminy':'Ang',
    'dencharmaxy':'Ang',
    'dencharminz':'Ang',
    'dencharmaxz':'Ang'
    }

chemical_symbols = ['X',  'H',  'He', 'Li', 'Be',
                    'B',  'C',  'N',  'O',  'F',
                    'Ne', 'Na', 'Mg', 'Al', 'Si',
                    'P',  'S',  'Cl', 'Ar', 'K',
                    'Ca', 'Sc', 'Ti', 'V',  'Cr',
                    'Mn', 'Fe', 'Co', 'Ni', 'Cu',
                    'Zn', 'Ga', 'Ge', 'As', 'Se',
                    'Br', 'Kr', 'Rb', 'Sr', 'Y',
                    'Zr', 'Nb', 'Mo', 'Tc', 'Ru',
                    'Rh', 'Pd', 'Ag', 'Cd', 'In',
                    'Sn', 'Sb', 'Te', 'I',  'Xe',
                    'Cs', 'Ba', 'La', 'Ce', 'Pr',
                    'Nd', 'Pm', 'Sm', 'Eu', 'Gd',
                    'Tb', 'Dy', 'Ho', 'Er', 'Tm',
                    'Yb', 'Lu', 'Hf', 'Ta', 'W',
                    'Re', 'Os', 'Ir', 'Pt', 'Au',
                    'Hg', 'Tl', 'Pb', 'Bi', 'Po',
                    'At', 'Rn', 'Fr', 'Ra', 'Ac',
                    'Th', 'Pa', 'U',  'Np', 'Pu',
                    'Am', 'Cm', 'Bk', 'Cf', 'Es',
                    'Fm', 'Md', 'No', 'Lr']



def start():
    app = wx.GetApp()
    vasp = VaspSiestaService(app)
    return vasp

