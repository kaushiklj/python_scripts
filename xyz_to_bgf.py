import os
import glob

max_strcutures = 500

def write_biograf_file(data_lines,name1):
    natoms = int(data_lines[0])
    line1= data_lines[1].split()
    lx = float(line1[2])-float(line1[1])
    ly = float(line1[4])-float(line1[3])
    lz = float(line1[6])-float(line1[5])
    ang1 = 90.0
    ang2 = 90.0
    ang3 = 90.0
    
    if os.path.isfile('./combined_geo'):
       of1 = open('combined_geo','a')
    else:
       of1 = open('combined_geo','w')

    of1.write('BIOGRF 200\n')
    of1.write('DESCRP %s\n'%(name1))
    of1.write('REMARK\n')
    of1.write('CRYSTX  %10.5f %10.5f %10.5f %10.5f %10.5f %10.5f\n'%(lx,ly,lz,ang1,ang2,ang3))
    of1.write('FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,3f10.5,1x,a5,i3,i2,1x,f8.5)\n')
    for i1 in range(0,natoms):
        line1 = data_lines[i1+2].split()
        at_name = line1[0]
        xcor    = float(line1[1])
        ycor    = float(line1[2])
        zcor    = float(line1[3])
        of1.write('HETATM %5d %-5s            %10.5f %9.5f %9.5f %5s  0 0  0.00000\n'%(i1+1,at_name,xcor,ycor,zcor,at_name))
    of1.write('END\n')
    of1.write('\n')
    of1.close()
    

dir_name = os.getcwd()

#name_list = []
#name_list.append('input.xyz')

of1 = open('combined_geo','w')
of1.close()
struct_count = 0
multiple_file_flag = 0 # 0 means all frame in one single file
#for i1 in range(0,len(name_list)):
if (multiple_file_flag == 1):
    for name in sorted(glob.glob('*.xyz')):
        print ('%s\n'%(name))
        data_lines = []
        count = 0
        with open(name,'r') as ifile:
            for line in ifile:
                data_lines.append(line)
        write_biograf_file(data_lines,name)
        struct_count = struct_count + 1
else:
    with open('first.xyz','r') as ifile:
        data_lines = []
        count = 0
        frame_flag = 0
        for line in ifile:
            if (frame_flag == 0):
                data_lines.append(line)
                natoms = int(line)
                frame_flag = 1
                count = count + 1
            else:
                data_lines.append(line)
                count = count + 1
                if (count == natoms+2):
                    struct_count = struct_count + 1
                    write_biograf_file(data_lines,str(struct_count)+'_struct')
                    frame_flag = 0
                    count = 0
                    data_lines = []
                
print('Done converting %d structures'%(struct_count))
    
