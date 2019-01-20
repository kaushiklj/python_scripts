import sys

ifn1 = "last.ramp"

tstep_falg = 0
noa_flag = 0
atoms_flag = 0
box_flag = 0
remap_flags = [0,0,0] #for x,y and z directions, non-zero value means remap 

pos_list = ['id','type','x','y','z']
pos_index = []
at_names = ['C','N','H']

count = 0
fr_count = 0

of1 = open('output.xyz','w')
of2 = open('type_output','w')

nlines = 0
with open(ifn1,'r') as if1:
    for line in if1:
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
                            pos_index.append(i2-2)
                            break

        if(tstep_flag == 1 and header_flag == 0):
            tstep_flag = 0
            tstep = int(line1[0])
        if(box_flag == 1 and header_flag == 0):
            lxyz.append(float(line1[0]))
            lxyz.append(float(line1[1]))
            box_count = box_count + 1
            if (box_count == 3):
                lx = lxyz[1] - lxyz[0]
                ly = lxyz[3] - lxyz[2]
                lz = lxyz[5] - lxyz[4]
                print (str(lx))
                box_flag = 0

        if (noa_flag == 1 and header_flag == 0):
            noa_flag = 0
            natoms = int(line1[0])
            x_cor = [None]*natoms
            y_cor = [None]*natoms
            z_cor = [None]*natoms
            names = [None]*natoms
            types = [None]*natoms
        if (atoms_flag == 1 and header_flag == 0):
            at_id = int(line1[pos_index[0]])-1
            n1 = int(line1[pos_index[1]])
            names[at_id] = at_names[n1-1]
            types[at_id] = int(line1[pos_index[1]])
            x_cor[at_id] = float(line1[pos_index[2]])
            y_cor[at_id] = float(line1[pos_index[3]])
            z_cor[at_id] = float(line1[pos_index[4]])
            #if (x_cor[at_id] < lxyz[0]):
            #    print ('x cord of %d is smaller than xlo ' %(at_id))
            if (remap_flags[0] == 1 and (x_cor[at_id] < lxyz[0]+lx/2.0)):
                x_cor[at_id] = x_cor[at_id] + lx
            if (remap_flags[1] == 1 and (y_cor[at_id] < lxyz[2]+ly/2.0)):
                y_cor[at_id] = y_cor[at_id] + ly
            if (remap_flags[2] == 1 and (z_cor[at_id] < lxyz[4]+lz/2.0)):
                z_cor[at_id] = z_cor[at_id] + lz

            count = count + 1

            if (count == natoms):
                atoms_flag = 0
                count = 0
                fr_count = fr_count + 1
                of1.write('%d\n'%natoms)
                of1.write('%f %f %f %f %f %f 90 90 90\n'%(lxyz[0],lxyz[1],lxyz[2],lxyz[3],lxyz[4],lxyz[5]))

                of2.write('%d\n'%natoms)
                of2.write('%f %f %f\n'%(lxyz[1]-lxyz[0],lxyz[3]-lxyz[2],lxyz[5]-lxyz[4]))
                
                for i1 in range(0,natoms):
                    of1.write('%s %f %f %f\n'%(names[i1],x_cor[i1],y_cor[i1],z_cor[i1]))
                    of2.write('%d %f %f %f\n'%(types[i1],x_cor[i1],y_cor[i1],z_cor[i1]))
                x_cor = []
                y_cor = []
                z_cor = []
                names = []
                types = []
                print ('Finished frame %d\n'%fr_count)

of1.close()
of2.close()
                    
            
            
        

        
