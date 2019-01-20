import sys
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

#natoms = 168200
ifn1 = "dump.airebo_stretch"
natoms = 0
nframes = 0
count = 0
target_frame_count = -1
natoms = 0
target_frames = [1]
print_xyz_flag = 0


stress_flag = 1
pe_flag = 0
per_atom_vol_flag = 0
target_atom_type = 1  #atom type 1 means Carbon
target_pe = -7.4500
en_tolerance = 30
nbins = 100
diff_nbins = 20
per_atom_stress_flag = 1

spatial_bin_flag = 1
spatial_bin_dirn = 1 #1 means X, 2 means Y and 3 means Z
spatial_nbins = 10
spatial_bin_dr = 0.0
#periodic_map_flag = 1
stress_dirn = 1 # 1 for x, 2 for y, 3 for z
pos_list = ['id','type','x','y','z','c_atomstress[1]','c_atomstress[2]','c_atomstress[3]','c_peatom','c_vol[1]']
at_type_names = ['C','H','H1','N']

#-------------------------------------------------------------------------------------------------
def find_natoms(ifn1):
    if1 = open(ifn1,'r')
    flag = 0
    count = 0
    global natoms
    for line in if1:
        count = count + 1
        if (flag == 0):
            if (line == "ITEM: NUMBER OF ATOMS\n"):
                flag = 1
        else:
            line1 = line.split()
            natoms = int(line1[0])
            flag = 0
            break
#-------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------
def sparse_frame():
    tstep_falg = 0
    noa_flag = 0
    atoms_flag = 0
    box_flag = 0
    pos_index = [0]*len(pos_list)
    for line in input_lines:
        #print('%s\n'%line)
        line1 = line.split()
        header_flag = 0
        if (len(line1) > 1):
            if (line1[0] == "ITEM:" and line1[1] == "TIMESTEP"):
                tstep_flag = 1
                header_flag = 1
            if (line1[0] == "ITEM:" and line1[1] == "NUMBER"):
                noa_flag = 1
                header_flag = 1
            if (line1[0] == "ITEM:" and line1[1] == "BOX"):
                box_flag = 1
                box_count = 0
                lxyz = []
                header_flag = 1
            if (line1[0] == "ITEM:" and line1[1] == "ATOMS"):
                atoms_flag = 1
                header_flag = 1
                for i1 in range(0,len(pos_list)):
                    for i2 in range(0,len(line1)):
                        if (line1[i2] == pos_list[i1]):
                            pos_index[i1] = i2-2;
                            #pos_index.append(i2-2)
                            break
                print (*pos_index,sep = ",")

        if (tstep_flag == 1 and header_flag == 0):
            tstep_flag = 0
            tstep = int(line1[0])
        if (box_flag == 1 and box_count < 4 and header_flag == 0):
            lxyz.append(float(line1[0]))
            lxyz.append(float(line1[1]))
            box_count = box_count + 1
            if (box_count == 3):
                box_flag = 0
                abc[0] = abc[0] + lxyz[0]
                abc[1] = abc[1] + lxyz[1]
                abc[2] = abc[2] + lxyz[2]
                abc[3] = abc[3] + lxyz[3]
                abc[4] = abc[4] + lxyz[4]
                abc[5] = abc[5] + lxyz[5]
                

        if (noa_flag == 1 and header_flag == 0):
            noa_flag = 0
            natoms = int(line1[0])
        
        if (atoms_flag == 1 and header_flag == 0):
            at_id = int(line1[pos_index[0]])-1
            n1 = int(line1[pos_index[1]])
            #names[at_id] = at_names[n1-1]
            at_type[at_id] = int(line1[pos_index[1]])
            x_cor[at_id] = x_cor[at_id] + float(line1[pos_index[2]])
            y_cor[at_id] = y_cor[at_id] + float(line1[pos_index[3]])
            z_cor[at_id] = z_cor[at_id] + float(line1[pos_index[4]])
            if (stress_flag == 1):
                x_stress[at_id] = x_stress[at_id] + float(line1[pos_index[5]])
                y_stress[at_id] = y_stress[at_id] + float(line1[pos_index[6]])
                z_stress[at_id] = z_stress[at_id] + float(line1[pos_index[7]])
            if (pe_flag == 1):
                pe[at_id]       = pe[at_id] + float(line1[pos_index[8]])
            if (per_atom_vol_flag == 1):
                at_vol[at_id]   = at_vol[at_id]+ float(line1[pos_index[9]])
    if (print_xyz_flag == 1):
        of1 = open(str(target_frames[target_frame_count]) + '.xyz','w')
        of1.write(str(natoms)+'\n')
        of1.write('\n')
        for i1 in range(0,natoms):
            of1.write('%d %f %f %f %f %f %f %f\n'%(at_type[i1],x_cor[i1],y_cor[i1],z_cor[i1],x_stress[i1],y_stress[i1],x_stress[i1],pe[i1]))
        of1.close()
#*****************************************************************************************

#-------------------------------------------------------------------------------------------------
def calculate_averages():
    if (avg_size == 0):
        print('Averaging size cannot be zero')
        quit()

    for i1 in range(0,6):
        abc[i1] = abc[i1]/avg_size
    
    for i1 in range(0,len(x_cor)):
        x_cor[i1] = x_cor[i1]/avg_size
        y_cor[i1] = y_cor[i1]/avg_size
        z_cor[i1] = z_cor[i1]/avg_size

        if (stress_flag == 1):
            x_stress[i1] = x_stress[i1]/avg_size
            y_stress[i1] = y_stress[i1]/avg_size
            z_stress[i1] = z_stress[i1]/avg_size

        if (pe_flag == 1):
            pe = pe[i1]/avg_size

        if (per_atom_vol_flag == 1):
            at_vol[i1] = at_vol[i1]/avg_size
#*************************************************************************************************

#-------------------------------------------------------------------------------------------------
def reset_lists():
    for i1 in range(0,6):
        abc[i1] = 0
    for i1 in range(0,natoms):
        x_cor[i1] = 0
        y_cor[i1] = 0
        z_cor[i1] = 0
        #at_type = [0]*natoms
        if (stress_flag == 1):
            x_stress[i1] = 0
            y_stress[i1] = 0
            z_stress[i1] = 0
            stress[i1]   = 0
        if (pe_flag == 1):
            pe[i1] = 0
        if (per_atom_vol_flag == 1):
            at_vol[i1] = 0
#*************************************************************************************************


#-------------------------------------------------------------------------------------------------
def bin_atoms(cord,bin_pop,stress_bin_dr,offset):
    for i1 in range(0,len(cord)):
        bin_no = int((cord[i1]-offset)/stress_bin_dr)
        if (bin_no >= len(bin_pop)):
            bin_no = len(bin_pop)-1

        bin_pop[bin_no].append(i1)
#*************************************************************************************************

#-------------------------------------------------------------------------------------------------
def calculate_bin_property(values):
    for i1 in range(0,len(bin_pop)):
        temp = 0.0
        for i2 in range(0,len(bin_pop[i1])):
            at_id = bin_pop[i1][i2]
            temp = temp + values[at_id]
        if (vol_flag == 1):
            temp = temp/bin_vol
        else:
            temp = temp/len(bin_pop[i1])
        
        bin_property_value[i1] = temp
    
#*************************************************************************************************

        
#find number of atoms
find_natoms(ifn1)
input_lines = [None]*(natoms+9)
avg_size = 1
skip = 1
lower_lim = 250
upper_lim = 300
fr_count = 0
curr_avg_count = 0
time_betn_frames = 5000*0.25/1000 #this is in picoseconds
with open(ifn1,'r') as if1:
    for line in if1:
        input_lines[count] = line
        count = count + 1
        if (count == natoms + 9):
            count = 0
            print ('Done reading frame %d ' %fr_count)
            if (fr_count == 0):
                abc    = [0]*6
                x_cor   = [0]*natoms
                y_cor   = [0]*natoms
                z_cor   = [0]*natoms
                at_type = [0]*natoms
                if (stress_flag == 1):
                    x_stress = [0]*natoms
                    y_stress = [0]*natoms
                    z_stress = [0]*natoms
                    stress   = [0]*natoms
                if (pe_flag == 1):
                    pe = [0]*natoms
                if (per_atom_vol_flag == 1):
                    at_vol = [0]*natoms

            if ((fr_count%skip)==0 and lower_lim < fr_count < upper_lim):                    
                sparse_frame()
                curr_avg_count = curr_avg_count + 1
                if (curr_avg_count == avg_size):
                    calculate_averages()

                    if (per_atom_stress_flag == 1):
                        new_stress = [0]*natoms
                        vol_per_atom = (abc[1]-abc[0])*(abc[3]-abc[2])*(abc[5]-abc[4])/natoms
                        for i1 in range(0,natoms):
                            new_stress[i1] = x_stress[i1]/vol_per_atom

                        name = str(fr_count+1)+'_per_atom.dat'
                        of1=open(name,'w')
                        for i1 in range(0,natoms):
                            of1.write('%f %f\n'%(x_cor[i1],new_stress[i1]))
                        of1.close()

                        name = str(fr_count+1)+'_per_atom.xyz'
                        of1=open(name,'w')
                        of1.write('%d\n'%natoms)
                        of1.write('%f %f %f %f %f %f 90 90 90\n'%(abc[0],abc[1],abc[2],abc[3],abc[4],abc[5]))
                        for i1 in range(0,natoms):
                            if (abs(new_stress[i1]) < 500000):
                                at_name = 'N'
                            elif (500000<abs(new_stress[i1])<750000):
                                at_name = 'C'
                            elif (750000<abs(new_stress[i1])<1000000):
                                at_name = 'O'
                            else:
                                at_name = 'S'
                        
                            of1.write('%s %f %f %f\n'%(at_name,x_cor[i1],y_cor[i1],z_cor[i1]))
                        of1.close()
                        

                    if (spatial_bin_flag == 1):
                        hi = (spatial_bin_dirn-1)*2+1
                        lo = (spatial_bin_dirn-1)*2
                        spatial_bin_dr = (abc[hi]-abc[lo])/spatial_nbins
                        bin_vol = (abc[1]-abc[0])*(abc[3]-abc[2])*(abc[5]-abc[4])/spatial_nbins
                        bin_pop = []
                        bin_property_value = [0]*spatial_nbins
                        bin_center = [0]*spatial_nbins
                        
                        for i1 in range(0,spatial_nbins):
                            bin_pop.append([])
                            bin_center[i1] = (i1+0.5)*spatial_bin_dr
                        
                        if (spatial_bin_dirn == 1):
                            bin_atoms(x_cor,bin_pop,spatial_bin_dr,abc[0])
                        elif (spatial_bin_dirn == 2):
                            bin_atoms(y_cor,bin_pop,spatial_bin_dr,abc[2])
                        else:
                            bin_atoms(z_cor,bin_pop,spatial_bin_dr,abc[4])
                        
                        vol_flag = 1                        
                        calculate_bin_property(x_stress)
                        name = str(fr_count+1)+'.dat'
                        of1=open(name,'w')
                        for i1 in range(0,len(bin_center)):
                            of1.write('%f %f\n'%(bin_center[i1],bin_property_value[i1]))
                        of1.close()
                        
                                        
                    curr_avg_count = 0
                    reset_lists()
                                    
            fr_count = fr_count + 1
                
