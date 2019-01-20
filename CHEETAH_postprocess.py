import sys
from decimal import Decimal

#The script assumes that user is provifing following two files
fn1 = "P_T.txt" #This file is currently not used
#fn2 = "thermo.txt"
print ("Enter the CHEETAH output file name")
fn2 = input()
f_flag = 0
#try:
#    if1 = open(fn1,'r')
#    if1.close()
#except IOError as e:
#    print('%s file does not exist'%fn1)
#    f_flag = 1

try:
    if2 = open(fn2,'r')
    if2.close()
except IOError as e:
    print('%s file does not exist'%fn2)
    f_flag = 2

if (f_flag !=0):
    sys.exit()

npoints = 0
nlines = 0
print ('Reading the input files\n')
data_lines = []
start_line = []

if2 = open(fn2,'r')
for i1 in if2:
    data_lines.append(i1)
    line1 = i1.split()
    nlines = nlines + 1
    if (len(line1) > 0 and line1[0] == 'Input>point,'):
        npoints = npoints + 1
        start_line.append(nlines)
if2.close()

if (len(start_line) == 0):
    print('Something wrong with the input file')
    sys.exit()

thermo_list = []
transport_list = []
product_list = []

header_flag = 0
for i1 in range(0,npoints):
#for i1 in range(0,1):
    start = start_line[i1]
    if (i1 < npoints-1):
        end = start_line[i1+1]
    else:
        end = nlines-1

    if (header_flag == 0):
        header_flag = 1
        flag = 0
        for i2 in range(start,end):
            line1 = data_lines[i2].split()
            if (len(line1) > 0 and line1[0] == "THERMODYNAMICS"):
                flag = 1
            if (len(line1) > 1 and flag == 1):
                line2 = line1[:-1]
                thermo_list.append(" ".join(line2))
            if (len(line1) > 0 and line1[0] == "TRANSPORT"):
                flag = 2
            if (len(line1) > 1 and flag == 2):
                line2 = line1[:-1]
                transport_list.append(" ".join(line2))
            if (len(line1) > 0 and line1[0] == "PRODUCTS"):
                flag = 3
            if (len(line1) > 1 and flag == 3):
                product_list.append(line1[0])
            if (len(line1) == 0):
                flag = 0

        #Check for the main keywords before moving forward
        if (len(thermo_list) == 0):
            print ('File does not contain THERMODYNAMICS keyword. So Stopping')
            sys.exit()
        if (len(transport_list) == 0):
            print ('File does not contain TRANSPORT keyword. So Stopping')
            sys.exit()
        if (len(product_list) == 0):
            print ('File does not contain PRODUCTS keyword. So Stopping')
            sys.exit()

        #Open output files
        of1 = open("thermo.dat",'w')
        of2 = open("transport.dat",'w')
        of3 = open("products.dat",'w')
        #write header lines for thermodynamics section
        for i2 in range(0,len(thermo_list)):
            of1.write('%26s'%thermo_list[i2])
        of1.write('\n')
        #of1.close()
        
        #write header lines for transport section
        for i2 in range(0,3,2):
            of2.write('%16s'%thermo_list[i2])
        for i2 in range(0,len(transport_list)):
            of2.write('%46s'%transport_list[i2])
        of2.write('\n')
        #of2.close()
        
        #write header lines for product section
        for i2 in range(0,3,2):
            of3.write('%16s'%thermo_list[i2])
        for i2 in range(1,len(product_list)):
            of3.write('%12s'%product_list[i2])
        of3.write('\n')
        #of3.close()

    flag = 0
    prod_lines = 0
    entries_thermal = []
    entries_transport = []
    entries_product = []
    product_map = []
    #Store all the relevant values in corresponding lists
    for i2 in range(start,end):
        line1 = data_lines[i2].split()
        if (len(line1) > 0 and line1[0] == "THERMODYNAMICS"):
            flag = 1
        if (len(line1) > 1 and flag == 1):
            entries_thermal.append(float(line1[len(line1)-1]))
        if (len(line1) > 0 and line1[0] == "TRANSPORT"):
            flag = 2
        if (len(line1) > 1 and flag == 2):
            entries_transport.append(float(line1[len(line1)-1]))
        if (len(line1) > 0 and line1[0] == "PRODUCTS"):
            flag = 3
        if (len(line1) > 1 and flag == 3):
            if(prod_lines > 0):
                entries_product.append(line1[len(line1)-1])
                prod_lines = prod_lines + 1
                #Find the map between current order of names and first order
                curr_name = line1[0]
                for i3 in range(0,len(product_list)):
                    if (product_list[i3] == curr_name):
                        product_map.append(i3)
                        break
            else:
                prod_lines = prod_lines + 1
        if (len(line1) == 0):
                flag = 0
    #Write all output to the corresponding files
    #Existing implementation assumes pressure is 0th index
    #and temperature is 2nd index. It can be changed in the future.
    #Before writing check if length of header list and entries list
    #match with each other.
    if (len(thermo_list) != len(entries_thermal)):
        print ('Length of thermal lists do not match')
        sys.exit()
    if( len(transport_list) != len(entries_transport)):
        print ('Length of transport lists do not match')
        sys.exit()
    if( len(product_list)-1 != len(entries_product) or len(product_list)-1 != len(product_map) ):
        print ('Length of product lists do not match')
        sys.exit()
        
    #write data of thermodynamics section
    for i2 in range(0,len(entries_thermal)):
        of1.write('%26f'%entries_thermal[i2])
    of1.write('\n')

    #write data of transport section
    for i2 in range(0,3,2):
        of2.write('%16f'%entries_thermal[i2])
    for i2 in range(0,len(entries_transport)):
        of2.write('%46f'%entries_transport[i2])
    of2.write('\n')

    #write data of product section. Using "product_map" to identify the
    #position 
    for i2 in range(0,3,2):
        of3.write('%16f'%entries_thermal[i2])
    for i2 in range(0,len(product_list)):
        for i3 in range(0,len(product_map)):
            if (product_map[i3] == i2):
                of3.write('%12s'%entries_product[i3])
    of3.write('\n')
    print ('%d point completed'%i1)

of1.close()
of2.close()
of3.close()
