import matplotlib.pyplot as plt
import numpy as np 
x = []
y = []
dic = {}
with open("LOCPOT_Z", mode='r') as f:
    first_line = f.readline()
    name_x = first_line.split()[1]
    name_y = first_line.split()[2]
    for line in f:
        xy=line.rstrip().split()
        x.append(float(xy[0]))
        y.append(float(xy[1]))
        dic.update({xy[0]:xy[1]})
plt.plot(x,y) 
plt.xlabel(name_x) 
plt.ylabel(name_y) 
plt.savefig('workfunction' + '.pdf', dpi=400)
plt.show()
# Get the total line numbers of POSCAR 
num_lines = sum(1 for line in open('POSCAR'))

# Read POSCAR 
pos = open('POSCAR', mode = 'r')
line = pos.readlines()

# Get  the  slab length in z direction 
vaccum = float(line[4].split()[2])

# Get all atoms' coordination in z direction and store them in the list
z_list = []
for i in range(9, num_lines): 
    z_list.append(float(line[i].split()[2]))

#  max(z_list) is highest atoms' coordination in z direction
# Get the vaccum lenth: 
l_vaccum = vaccum - max(z_list)
print ('The Vaccum in this calculation is:\t\t %s'  %(l_vaccum))

# Choose the middle z value in the workfuntion.pdf 
num_middle = (max(z_list) + vaccum) / 2 
#print num_middle

middle_y = []
for i in dic.keys():
    i = float(i)
# Select the date area within 1 angstrom from the middle point:
    if i > num_middle -1 and i <  num_middle + 1:
        middle_y.append(float(dic.get(str(i))))
# Get the average value in the selected area
print ('The Vaccum Energy in this calculation is:\t %s'  %(np.mean(middle_y)))
pos.close()