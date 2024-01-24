import wx
import os
import wx.grid as grid
import configparser

class job(wx.Panel):
    """ JOB设置 """
    def __init__(self, parent, id, atoms):
        wx.Panel.__init__(self, parent, id)

        self.atoms = atoms

        job_box = wx.BoxSizer(wx.HORIZONTAL)

        sz1 = wx.StaticBoxSizer(wx.VERTICAL, self, '赝势选择')
        self.labels = ['元素', '类型选择']
        self.gridrow = 1
        self.grid = grid.Grid(self, -1, size=(260, 130))
        self.grid.CreateGrid(self.gridrow, 2)
        self.grid.DisableDragRowSize()
        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.grid.SetDefaultRowSize(self.grid.GetDefaultRowSize()*1.2)
        self.grid.SetColLabelValue(0, self.labels[0])
        self.grid.SetColLabelValue(1, self.labels[1])
        self.grid.SetColSize(0, 80)
        self.grid.SetColSize(1, 100)
        self.grid.Bind(grid.EVT_GRID_CELL_CHANGED, self.OnGridCellChanged)

        sz1.Add(self.grid, flag=wx.ALL, border=2)
        job_box.Add(sz1, flag=wx.ALL, border=2)

        self.getatom()
        self.setatom()
        self.SetSizer(job_box)
        parent.AddPage(self, 'job')



    def OnGridCellChanged(self, event):
        row = event.GetRow()
        col = event.GetCol()

        atom = self.grid.GetCellValue(row, 0)
        key = self.grid.GetCellValue(row, col)

        self.atomset[atom] = str(key)

    def getatom(self):
        self.symbols = list(set(self.atoms.get_chemical_symbols()))

    def setatom(self):
        linenum = len(self.symbols)

        while self.gridrow > 1:
            self.grid.DeleteRows(self.gridrow-1)
            self.gridrow -= 1

        ##初始化grid
        while self.gridrow < linenum:
            self.grid.AppendRows()
            self.gridrow += 1
        self.atomset = {}

        for index,atom in enumerate(self.symbols):
            choices = ['LDA-CA','GGA-PB']
            valueChoice = wx.grid.GridCellChoiceEditor(choices)
            self.grid.SetCellValue(index, 0, atom)
            self.grid.SetCellEditor(index,1,valueChoice)
            self.grid.SetCellValue(index, 1, choices[0])
            self.atomset[atom] = choices[0]

    def getatomset(self):
        return self.atomset

    def doReConfig(self, filepath):
        conf = configparser.RawConfigParser()
        conf.read(filepath)
        ###
        atomstype = conf.get('JOB', 'atomstype')
        cellvalue = atomstype.split('%')
        for i, item in enumerate(cellvalue):
            self.grid.SetCellValue(i, 1, item)

    def SaveConfig(self,conf):
        conf.add_section('JOB')
        ###
        atomstype = ''
        linenum = len(self.symbols)
        for i in range(linenum):
            atomstype += self.grid.GetCellValue(i,1) + ' '
        atomstype = atomstype.strip().replace(' ','%')
        conf.set('JOB','atomstype',atomstype)

    def GetJobWinBatstr(self, filepath, isrelax=False, isscf=False, isdenchar=False, isdos=False, isband=False):
        pse_path = os.path.join(os.path.join(os.getcwd(), 'Share'), 'Pseudos')
        filestr = ''
        filestr += 'cd ' + filepath.replace('\\', '\\\\') + '\n'
        if not os.path.exists(os.path.join(filepath, 'temp')):
            filestr += 'mkdir temp\n'
        filestr += 'cd temp\n'
        filestr += 'cp ..\\\\model.xyz .\n'
        if not isrelax:
            if os.path.exists(os.path.join(filepath, 'scf.xyz')):
                filestr += 'cp ..\\\\scf.xyz .\n'
            else:
                filestr += 'cp ..\\\\model.xyz scf.xyz\n'
        for atom in self.atomset.keys():
            atomfile = atom + '.psf'
            filestr += 'cp ' + pse_path.replace('\\', '\\\\') + '\\\\' + self.atomset[
                atom] + '\\\\' + atomfile + ' .\n'
        if isrelax:
            filestr += '\nsiesta.exe < ..\\\\relax.fdf | tee ..\\\\relax.out | awk \'/iscf/, /constrained/\'\n'
            filestr += 'awk \'/iscf/, /constrained/\' ..\\\\relax.out > ..\\\\relax.outEF\n'
            filestr += 'sed -n \'/Relaxed/,/siesta/p\' ..\\\\relax.out | sed \'1d\' | sed \'N;$!P;$!D;$d\' | awk \'{print $1, $2, $3, $4}\' > scf.xyz\n'
            filestr += 'cp scf.xyz ..\\\\.\n'
            # ####
            filestr += 'bash ..\\\\crt_rlx_struct.bat\n'
            ####
            crt_rlx_structstr = ''
            ####
            crt_rlx_structstr += '\nsed -n \'1,24p\' ..\\\\model.cif > tmptop\n'
            crt_rlx_structstr += 'sed -n \'25,$p\' ..\\\\model.cif > tmpdown\n'
            crt_rlx_structstr += 'awk \'{print $1,$2}\' tmpdown | tr \" \" \"\\t\" >tmpdownleft\n'
            crt_rlx_structstr += 'awk \'{print $6,$7,$8}\' tmpdown > tmpdownright\n'
            crt_rlx_structstr += 'sed -n \'5,$p\' Siesta.STRUCT_OUT | awk \'{print $3,$4,$5}\' >tmprlx\n'
            crt_rlx_structstr += 'paste tmpdownleft tmprlx tmpdownright | tr \"\\t\" \"    \"> newtmpdown\n'
            crt_rlx_structstr += 'cat tmptop newtmpdown > ..\\\\model_rlx.cif\n'
            crt_rlx_structstr += 'sed -n \'1,8p\' ..\\\\model.xsf > tmptop\n'
            crt_rlx_structstr += 'sed -n \'9,$p\' ..\\\\model.xsf > tmpdown\n'
            crt_rlx_structstr += 'awk \'{print $1}\' tmpdown | tr \" \" \"\\t\" >tmpdownleft\n'
            crt_rlx_structstr += 'awk \'{print $1,$2,$3}\' scf.xyz | tr \" \" \"\t\" >tmprlx\n'
            crt_rlx_structstr += 'paste tmpdownleft tmprlx > newtmpdown\n'
            crt_rlx_structstr += 'cat tmptop newtmpdown > ..\\\\model_rlx.xsf\n'
            rlx_structfile = os.path.join(filepath, 'crt_rlx_struct.bat')
            with open(rlx_structfile, 'w') as fp:
                fp.write(crt_rlx_structstr)

        if isscf:
            filestr += '\nsiesta.exe < ..\\\\scf.fdf | tee ..\\\\scf.out | awk \'/iscf/, /constrained/\'\n'
            filestr += 'awk \'/iscf|Fermi energy/, /constrained|Fermi energy/\' ..\\\\scf.out > ..\\\\scf.outEF\n'

        if isdenchar:
            filestr +='\ncp ..\\\\rho.bat .\n'
            filestr += 'denchar.exe < ..\\\\scf.fdf | tee ..\\\\denchar.out\n'
            filestr += 'rho2xsf.exe < rho.bat\n'
            filestr += 'cp Siesta.XSF ..\\\\.\n'

        if isband:
            filestr += '\nFermi=`head -1 Siesta.bands | awk \'{print $1}\' | tail -1`\n'
            filestr += 'cat Siesta.bands |sed -e \'1,4d\' |sed -e \"/\'/d\" | sed -e \'$d\'| wfr /r:\"\\n        \" /t:\"\" | awk  -v Fermi=$Fermi \'{print  Fermi,$0}\' | sed -e \'$d\' > ..\\\\band.dat\n'
            filestr += 'sed -n \"/\'/p\" Siesta.bands | tr -d \"\'\" > ..\\\\band.confg\n'
        if isdos:
            filestr += '\nFermi=`head -1 Siesta.bands | awk \'{print $1}\' | tail -1`\n'
            filestr += 'awk  -v Fermi=$Fermi \'{print  Fermi,$0}\' Siesta.DOS > ..\\\\dos.dat\n'

        return filestr
