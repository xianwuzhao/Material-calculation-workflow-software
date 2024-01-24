import matplotlib.pyplot as pltimport matplotlib as mpl
mpl.use( 'Agg)
from pymatgen.io.vasp.outputs import vasprun
from pymatgen.electronic_structure.plotter import BSDOSPlotter,lBSPlotter,BSPlotterProjected,DosPlotter
#read vasprun.xml.get band and dos information
bs_vasprun = vasprun("vasprun.xm1" , parse_projected_eigen=True)
bs_data= bs_vasprun.get_band_structure(line_mode=True)

dos_vasprun=vasprun(""vasprun.xml")
dos_data=dos_vasprun.complete_dos

#set figure parameters, draw figure
banddos_fig = BSDOsPlotter(bs_projection='elements ', dos _projection='elements ',vb_energy_range=2,cb_energy_range=2)
banddos_fig.get_plot(bs=bs_ data, dos=dos_data)
plt.savefig(' banddos_fig.png'）
