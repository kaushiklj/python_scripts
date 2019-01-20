import sys
from operator import itemgetter
name_list = ['C12H18','C12H19O1','C16H25O1','C20H31O1','C24H37O1','C28H43O1','C32H50O2','C4H6','C8H12','C8H13O1']
r_name = 'C12H18'
#r_name = 'H2O1'


def find_reactant_product(line1,rlist,plist):
    #initialize all the lists
    #rlist = []
    #plist = []
    #find number of reactants
    flag = 0
    i2 = 1
    while(flag == 0):
        #print (line[i2])
        if (line1[i2] != '------->'):
            if (line1[i2] != '+'):
                rlist.append(line1[i2])
                #print (rlist)
                i2 = i2 + 1
            else:
                i2 = i2 + 1
        else:
            i2 = i2 + 1
            flag = 1
    #find number of products
    flag = 0
    while(flag  == 0):
        if (i2 < len(line1)):
            if (line1[i2] != '+'):
                plist.append(line1[i2])
                i2 = i2 + 1
            else:
                i2 = i2 + 1
        else:
            i2 = i2 + 1
            flag = 1
#-----------End of function defination--------------------

#*************Start of function defination****************
def compare_reactions(r1,p1,r2,p2):
    #negative value means reactions dont match
    #positive value means reactions match
    nr1 = len(r1)
    np1 = len(p1)

    nr2 = len(r2)
    np2 = len(p2)

    rflag = [None]* nr1
    pflag = [None]* np1

    for i1 in range(0,nr1):
        rflag[i1] = 0
    for i1 in range(0,np1):
        pflag[i1] = 0

    if (nr1 != nr2 or np1 != np2):
        return -10
    
    #Start comparing reactants
    count1 = 0
    for i1 in range(0,nr1):
        for i2 in range(0,nr2):
            if (r1[i1] == r2[i2] and rflag[i2] == 0):
                count1 = count1 + 1
                rflag[i2] = 1
                break
    
    #Start comparing products
    count2 = 0
    for i1 in range(0,np1):
        for i2 in range(0,np2):
            if (p1[i1] == p2[i2] and pflag[i2] == 0):
                count2 = count2 + 1
                pflag[i2] = 1
                break
    
    #Check if the reactions match
    if (count1 == nr1 and count2 == np1):
        return 10
    else:
        return -10
            
#------------End of the function definition---------------

#*************Start of function defination****************
def compare_backward_reactions(r1,p1,r2,p2):
    #negative value means reactions dont match
    #positive value means reactions match
    nr1 = len(r1)
    np1 = len(p1)

    nr2 = len(p2)
    np2 = len(r2)

    rflag = [None]* nr1
    pflag = [None]* np1

    for i1 in range(0,nr1):
        rflag[i1] = 0
    for i1 in range(0,np1):
        pflag[i1] = 0

    if (nr1 != nr2 or np1 != np2):
        return -10
    
    #Start comparing reactants
    count1 = 0
    for i1 in range(0,nr1):
        for i2 in range(0,nr2):
            if (r1[i1] == p2[i2] and rflag[i2] == 0):
                count1 = count1 + 1
                rflag[i2] = 1
                break
    
    #Start comparing products
    count2 = 0
    for i1 in range(0,np1):
        for i2 in range(0,np2):
            if (p1[i1] == r2[i2] and pflag[i2] == 0):
                count2 = count2 + 1
                pflag[i2] = 1
                break
    
    #Check if the reactions match
    if (count1 == nr1 and count2 == np1):
        return 10
    else:
        return -10
            
#------------End of the function definition---------------


for list_counter in range(0,len(name_list)):
    nreacs = 0
    count = 0
    rlist = []
    r_name = name_list[list_counter]
    with open('reactions.out','r') as file:
        for line in file:
            #print (line)
            line1 = line.split()
            flag = 0
            i1=0;
            while(flag == 0):
                if (line1[i1] == r_name):
                
                    if (nreacs == 0):
                        r1 = []
                        p1 = [] 
                        find_reactant_product(line1,r1,p1)

                        rlist.append([])
                        rlist[nreacs].append(int(1))
                        rlist[nreacs].append(int(0))
                        rlist[nreacs].append(line)
                        rlist[nreacs].append(line1)
                        rlist[nreacs].append(len(r1))
                        rlist[nreacs].append(len(p1))
                        nreacs = nreacs + 1
                    else:
                        #find reactant and products of current reaction
                        r1 = []
                        p1 = []
                        find_reactant_product(line1,r1,p1)

                        #search through the rlist to see if there is any match
                        i2 = 0
                        flag1 = 0
                        while (i2 < nreacs):                    
                            r2 = []
                            p2 = []

                            find_reactant_product(rlist[i2][3],r2,p2)

                            #compare forward reaction
                            comp_result = 0
                            comp_result = compare_reactions(r1,p1,r2,p2)
                            if (comp_result > 0):
                                rlist[i2][0] = rlist[i2][0] + 1
                                flag1 = 1
                                break

                            #compare backward reaction
                            comp_result1 = 0
                            comp_result1 = compare_backward_reactions(r1,p1,r2,p2)
                            if (comp_result1 > 0):
                                rlist[i2][1] = rlist[i2][1] + 1
                                flag1 = 1
                                break

                            i2 = i2 + 1
                    
                        #Found new reaction if flag = 0
                        if (flag1 == 0):
                            rlist.append([])
                            rlist[nreacs].append(int(1))
                            rlist[nreacs].append(int(0))
                            rlist[nreacs].append(line)
                            rlist[nreacs].append(line1)
                            rlist[nreacs].append(len(r1))
                            rlist[nreacs].append(len(p1))
                            nreacs = nreacs + 1
                        
                    
                    #ofile.write(line)
                    flag = 1
                    count = count + 1
                #elif(line1[i1] == '------->'):
                elif (i1+1 == len(line1)):
                    flag = 1
                else:
                    i1 = i1 +1
    for i1 in range(0,nreacs):
        n1 = abs(rlist[i1][0] - rlist[i1][1])
        rlist[i1].append(n1)
    rsorted = []
    #rsorted = sorted(rlist,key=itemgetter(4,0-1))
    rsorted = sorted(rlist,key=itemgetter(6),reverse = True)
    s1 = r_name + '.reactions'
    s2 = r_name + '_reactant.reactions'
    s3 = r_name + '_product.reactions'

    ofile = open(s1,'w')
    ofile1 = open(s2,'w')
    ofile2 = open(s3,'w')

    for i1 in range(0,nreacs):
        #ofile.write(str(rlist[i1][0]) + '    ' )+ rlist[i1][1] + '\n')
        ofile.write(str(rsorted[i1][0]) + '    ' + str(rsorted[i1][1]) + '    ')
        l11 = rsorted[i1][3]
        for i2 in range(1,len(l11)):
            ofile.write(l11[i2] + ' ')
        ofile.write('\n')
        ofile.write('\n')

        #Search if the molecule is in reactant side or product side
        r1 = []
        p1 = []
        find_reactant_product(l11,r1,p1)
        flag = 0
        for i2 in range(0,len(r1)):
            if (r1[i2] == r_name):
                flag = 1
                break;

        if (flag == 1):
            ofile1.write(str(rsorted[i1][0]) + '    ' + str(rsorted[i1][1]) + '    ')
            for i2 in range(1,len(l11)):
                ofile1.write(l11[i2] + ' ')
            ofile1.write('\n')
            ofile1.write('\n')
        else:
            ofile2.write(str(rsorted[i1][0]) + '    ' + str(rsorted[i1][1]) + '    ')
            for i2 in range(1,len(l11)):
                ofile2.write(l11[i2] + ' ')
            ofile2.write('\n')
            ofile2.write('\n')
                        
    ofile.close()
    ofile1.close()
    ofile2.close()
