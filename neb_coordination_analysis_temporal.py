import sys
import math

max_neighbors = 20
type_no = 1
cut_off= 2.9

neigh_flag = 0 #1 means user is providing neighbor list
jump_analysis = 1 #Find the coordinate state of selected move

if1_name = 'move.xyz'
if2_name = 'sp_data.in'
if3_name = 'move_energy.dat'

if1 = open(if1_name,'r')
natoms = int(if1.readline())
if1.close()

neigh_list = []

for i1 in range(0,natoms):
    neigh_list.append([])


if (neigh_flag == 1):
    if2 = open(if2_name,'r')
    flag_count = 0
    sp_lines = []
    for line in if2:
        sp_lines.append(line)
        if(line == 'Neighbors\n'):
            flag_count = 1
        if (flag_count > 0):
            flag_count = flag_count + 1
        if (flag_count > 3):
            line1 = line.split()
            n1 = int(line1[0]) - 1
            for i1 in range(1,len(line1)):
                neigh_list[n1].append(int(line1[i1]))
    if2.close()

data_lines = [None]*(natoms+2)
at_type = [None]*natoms
at_flag = [None]*natoms
neigh_pop = [None]*max_neighbors
x_cor = [None]*natoms
y_cor = [None]*natoms
z_cor = [None]*natoms
count = 0
frame_no = 0
of1 = open('coordination.dat','w')
of1.write('frame_no ')

for i1 in range(0,max_neighbors):
    of1.write('%d '%(i1))
of1.write('\n')

if(jump_analysis == 1):
    if3 = open(if3_name,'r')
    temporal_jump_coordination = []
    jump_coordination = [None]*max_neighbors
    for i1 in range(0,max_neighbors):
        jump_coordination[i1] = 0

with open(if1_name,'r') as if1:
    for line in if1:
        data_lines[count] = line
        count = count + 1

        if (count == natoms + 2):
            count = 0
            frame_no = frame_no + 1

            if (neigh_flag == 0 and frame_no == 1):
                for i1 in range(0,natoms):
                    line1 = data_lines[i1+2].split()
                    at_type[i1] = int(line1[0])
                    x_cor[i1] = float(line1[1])
                    y_cor[i1] = float(line1[2])
                    z_cor[i1] = float(line1[3])
                line1 = data_lines[1].split()
                lx = float(line1[1])
                ly = float(line1[2])
                lz = float(line1[3])

                for i1 in range(0,natoms):
                    x1 = x_cor[i1]
                    y1 = y_cor[i1]
                    z1 = z_cor[i1]

                    for i2 in range(0,natoms):
                        x2 = x_cor[i2]
                        y2 = y_cor[i2]
                        z2 = z_cor[i2]

                        dx = x1 - x2
                        dy = y1 - y2
                        dz = z1 - z2

                        #Check for periodic boundary conditions
                        if (dx > lx/2.0):
                            dx =dx - lx
                        if (dx <= (-1.0)*(lx/2.0)):
                            dx =dx + lx

                        if (dy > ly/2.0):
                            dy = dy - ly
                        if (dy <= (-1.0)*(ly/2.0)):
                            dy =dy + ly

                        if (dz > lz/2.0):
                            dz = dz - lz
                        if (dz <= (-1.0)*(lz/2.0)):
                            dz = dz + lz

                        dr = math.sqrt(dx*dx + dy*dy + dz*dz)

                        if(dr < cut_off and i1 != i2):
                            neigh_list[i1].append(i2+1)

            else:
                for i1 in range(0,natoms):
                    line1 = data_lines[i1+2].split()
                    at_type[i1] = int(line1[0])
            if ((frame_no -1)%2 == 0):
                if (jump_analysis == 1):
                    line1 = if3.readline().split()
                    swap1 = int(line1[0])
                    swap2 = int(line1[1])
                for i1 in range(0,max_neighbors):
                    neigh_pop[i1] = 0
                of2 = open('atom_coordination','w')
                for i1 in range(0,natoms):
                    if (at_type[i1] == type_no):
                        neigh_count = 0
                        of2.write('%d '%(i1+1)) 
                        for i2 in range(0,len(neigh_list[i1])):
                            n1 = neigh_list[i1][i2] - 1
                            if (at_type[n1] == type_no):
                                neigh_count = neigh_count + 1
                                of2.write('%d '%(n1+1))
                        if (neigh_count > max_neighbors):
                            print ('Exceeded maximum number of neighbrs\n')
                            exit()
                        of2.write('%d\n'%(neigh_count))
                        neigh_pop[neigh_count] = neigh_pop[neigh_count] + 1
                        if (jump_analysis == 1):
                            if (i1 == swap1 or i1 == swap2):
                                jump_coordination[neigh_count] = jump_coordination[neigh_count]+ 1
                                temporal_jump_coordination.append(neigh_count)
                of2.close()
                of1.write('%d '%(frame_no/2))
                for i1 in range(0,max_neighbors):
                    of1.write('%d '%(neigh_pop[i1]))
                of1.write('\n')
                print('%d frame is done\n'%(frame_no))
if3.close()
of1.close()

of1 = open('temporal_jump_coordination.dat','w')
for i1 in range(0,len(temporal_jump_coordination)):
    of1.write('%d %d\n'%(i1+1,temporal_jump_coordination[i1]))
of1.close()

of1 = open('jump_coordination.dat','w')
for i1 in range(0,len(jump_coordination)):
    of1.write('%d %d\n'%(i1+1,jump_coordination[i1]))
of1.close()
