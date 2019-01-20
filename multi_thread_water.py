import os
import subprocess
import shutil
import sys
import threading

parc1 = 0.55  #This is the control file parameter
parc2 = 0.001
accerr = 1.0
quantum_diff_num = 0.23
weight_diff_point = 0.0003
stem= [None]*3
sdy = [None]*3
curr_dir = os.getcwd()
fchange  = "yes"
print  curr_dir
old_diff_num = 0.0
thread_visit = 1

#Following is the class of each thread
class myThread (threading.Thread):
    def __init__(self,threadID, name, counter):
        self.threadID = threadID
        self.name     = name
        self.counter  = counter
        threading.Thread.__init__(self)

    def run(self):
        global thread_visit
        global curr_dir
        print "Starting " + self.name
        print "Counter of thread " + self.name + " is " + str(self.counter)
        temp_name = '/val_' + str(self.threadID-1)
        dir_path = curr_dir + temp_name
        os.chdir(dir_path)
        temp_dir = os.getcwd()
        #print "current working director for node " + str(self.threadID) + temp_dir
        run_cycle(self.threadID-1,0,1)
        print "Exiting " + self.name



#Function changes the force field parameter value
def change_ff(ichange,change,current_param,high,low):
   global curr_dir
   if (current_param >= 0):
      if (ichange == 0):
         new_param1 = current_param - change
      elif (ichange == 1):
         new_param1 = current_param + change
      else:
         new_param1 = current_param
   else:
      if (ichange == 0):
         new_param1 = current_param + change
      elif (ichange == 1):
         new_param1 = current_param - change
      else:
         new_param1 = current_param
   if(new_param1 > high):
      new_param1 = high
   if(new_param1 < low):
      new_param1 = low

   return new_param1

#Function for parabolic extrapolatin
def kmin(curr_parm_val,vpmax,vpmin,):
   global sdy
   global stem

   a=0.0
   b=0.0
   c=0.0
   ac=0.0
   expec =0.0
   iagain = 0
    
   file5 = open('fort.79',"a")
   file5.write('three parameter values are: ')
   file5.write('\n')
   s22= '%8.4f' %stem[0]+'    '+'%8.4f' %stem[1]+'    '+'%8.4f'%stem[2]
   file5.write(s22)
   file5.write('\n')
   file5.write('three  error values are: ')
   file5.write('\n')
   s22= '%8.4f' %sdy[0]+'    '+'%8.4f' %sdy[1]+'    '+'%8.4f'%sdy[2]
   file5.write(s22)
   file5.write('\n')
   
   if (abs(sdy[0]-sdy[1]) < 0.00001 and abs(sdy[0]-sdy[2])< 0.00001):
      temax = stem[2]
   elif (abs(sdy[1]-sdy[2])<0.00001):
      temax = stem[2]
   else:
      ste32 = stem[2]*stem[2]
      ste22 = stem[1]*stem[1]
      ste12 = stem[0]*stem[0]
      if((ste22 - ste12) < 0.00001):
         ste22 = ste22 + 0.001
      if(abs(ste32-ste12)<0.00001):
         ste32 = ste32 + 0.001

      b1 = (sdy[2]-sdy[0])*(ste22-ste12) - (sdy[1]- sdy[0])*(ste32 - ste12)
      b2 = (stem[2] - stem[0])*(ste22-ste12) - (stem[1] - stem[0])*(ste32-ste12)
      b  = b1/b2
      a  = (sdy[1]-sdy[0]-b*(stem[1]-stem[0]))/(ste22 - ste12)
      print 'value of a is : ', a
      ac = sdy[0] - a*ste12-b*stem[0]
      temax = -b/(2.0*a)
      expec = 0.01*a*temax*temax+ 0.01*b*temax+0.01*ac
   file5.write('a,b anc c are: ')
   file5.write('\n')
   s22= '%8.4f' %a+'    '+'%8.4f' %b+'    '+'%8.4f'%c
   file5.write(s22)
   file5.write('\n')
   file5.write('calculated optimum value from a,b,c is: ')
   file5.write('\n')
   s22 = '%8.4f'%temax
   file5.write(s22)
   file5.write('\n')
   file5.write('predicted error with optimum parameter value is: ')
   file5.write('\n')
   s22 ='%8.4f'%(100*expec)
   file5.write(s22)
   file5.write('\n')


   hu1 = 1.00 - parc2
   hu2 = 1.00 + parc2

   if(curr_parm_val > 0):
      if(temax < hu1*stem[0]):
               temax = hu1*stem[0]
      if(temax > hu2*stem[1]):
               temax = hu2*stem[1]
   if(curr_parm_val <0):
      if(temax > hu1*stem[0]):
               temax = hu1*stem[0]
      if (temax < hu2*stem[1]):
               temax = hu2*stem[1]

   if(a < 0):
      iagain = iagain + 1
      if(sdy[0]<sdy[1]):
               temax = stem[0]
      else:
               temax = stem[1]
   else:
      iagain = 0

   if(temax > vpmax):
               temax = vpmax
   if(temax < vpmin):
               temax = vpmin

   expec = 0.01*a*temax*temax + 0.01*b*temax+0.01*ac
   file5.write(str(temax))
   file5.write('\n')
   file5.write(str(100*expec))
   file5.write('\n')
   file5.close()
   return temax
#End of kmin function
#___________________________________________________________________________


#This part of the code calls reaxff executable
def reaxff_call(inum,switch):
   global curr_dir
   #os.chdir('/home/kaushik/python_script/trial1')
   #print os.getcwd()
   #process = subprocess.Popen(["C:/Python25/python_scripts/temp/reax.exe"], stdout=subprocess.PIPE)
   #print process.communicate()

   curr_dir2 = os.getcwd()
   print 'working directory for thread ' + str(inum) + '\n'
   print curr_dir2
   if(switch == 1):
      subprocess.call([curr_dir2 +'/reac_intel'])
      #read the data from fort.13
      file4 = open(curr_dir2 + '/fort.13',"r")
      temp_string =file4.readline()
      sdy[inum] = float(temp_string)
      file4.close()
      print 'error from fort.13 file is : ', sdy[inum]

      #sourceFile = curr_dir + '/fort.90'
      #destinFile = curr_dir + '/rest_geo'
      #shutil.copy(sourceFile,destinFile)
      os.remove(curr_dir2 + "/fort.90")
      os.remove(curr_dir2 + "/fort.71")
      os.remove(curr_dir2 + "/fort.73")
      print 'program reac_intel executed succefully', inum
   else:
      #subprocess.call([curr_dir2 +'/reac_intel'])
      subprocess.call([curr_dir2 +'/reaxff_2'])
      sourceFile = curr_dir2 + '/diff_traj.xyz'
      destinFile = curr_dir2 + '/input.xyz'
      shutil.copy(sourceFile,destinFile)
      os.remove(curr_dir2 + "/diff_traj.xyz")
      #os.remove(curr_dir2 + "/fort.90")
      #os.remove(curr_dir2 + "/fort.71")
      #os.remove(curr_dir2 + "/fort.73")
      #os.remove(curr_dir2 + "/moldyn.vel")
      print 'program reaxff_2 executed succefully', inum

   os.remove(curr_dir2 + "/fort.7")
   os.remove(curr_dir2 + "/fort.8")
   os.remove(curr_dir2 + "/fort.11")
   os.remove(curr_dir2 + "/fort.13")
   os.remove(curr_dir2 + "/fort.55")
   os.remove(curr_dir2 + "/fort.56")
   os.remove(curr_dir2 + "/fort.72")
   os.remove(curr_dir2 + "/fort.98")
   #os.remove(curr_dir2 + "/fort.99")
   os.remove(curr_dir2 + "/molfra.out")
   os.remove(curr_dir2 + "/output.pdb")
   os.remove(curr_dir2 + "/summary.txt")
   #os.remove(curr_dir2 + "/translate.out")
   #os.remove(curr_dir2 + "/Water_800.bgf")
   #os.remove(curr_dir2 + "/Water_800.geo")
   os.remove(curr_dir2 + "/xmolout")
#End of reaxff function
#__________________________________________________________________

def run_cycle(num,num1,num2):
   global quantum_diff_num
   global weight_diff_point
   global curr_dir
   global fchange
   global old_diff_num
   if(num2 == 1):
      curr_dir1 = curr_dir + '/val_' +str(num)
   else:
      curr_dir1 = curr_dir
   os.chdir(curr_dir1) 
   print 'working directory for thread ' + str(num) + '\n'
   print curr_dir1
   #Perform MD diffusion run
   diffusion_error = 0.0
   file3 = open(curr_dir1 + '/diff_error', "w")
   st1='%8.4f' %diffusion_error
   file3.write(st1)
   file3.close()
 
   sourceFile = curr_dir1 + '/diff_geo'
   destinFile = curr_dir1 + '/fort.3'

   shutil.copy(sourceFile,destinFile)

   sourceFile = curr_dir1 + '/diff_control'
   destinFile = curr_dir1 + '/control'

   shutil.copy(sourceFile,destinFile)

   sourceFile = curr_dir1 + '/diff_vels'
   destinFile = curr_dir1 + '/moldyn.vel'

   shutil.copy(sourceFile,destinFile)
   if (num == 2 and num1 == 0):
      if(fchange == "yes"):

         reaxff_call(num,0)
         #Caculation of diffusion coefficient goes in here
         os.chdir(curr_dir1)
         subprocess.call([curr_dir1 + '/diffusion_coefficient'])
         print 'diffusion routine ran successfully'+ str(num)
         file10=open(curr_dir1 +'/diff_coeff',"r")
         st10 = file10.readline()
         diff_num = float(st10)
         file10.close()
         old_diff_num = diff_num
         print 'old diffusion number is',old_diff_num
      else:
         diff_num = old_diff_num
   else:
      reaxff_call(num,0)
      #Caculation of diffusion coefficient goes in here
      os.chdir(curr_dir1)
      subprocess.call([curr_dir1 + '/diffusion_coefficient'])
      print 'diffusion routine ran successfully '+ str(num)
      file10=open(curr_dir1 +'/diff_coeff',"r")
      st10 = file10.readline()
      diff_num = float(st10)
      file10.close()

   diff_error1 = (diff_num - quantum_diff_num)/(weight_diff_point)
   diffusion_error  = diff_error1*diff_error1

   threadLock.acquire(1)
   print str(num) + "have acquired the lock"
   try:
       file11=open(curr_dir + '/diff_coeff_history',"a")
       st11 =str(num) + '  ' + str(diff_num)
       file11.write(st11)
       file11.write('\n')
       file11.close()

       file33 = open(curr_dir + '/diff_error_history', "a")
       st33 = str(num) + '  ' + str(diffusion_error)
       file33.write(st33)
       file33.write('\n')
       file33.close()
   finally:
       threadLock.release()

   #Force field traning for rest of the geo file
   file3 = open(curr_dir1 +'/diff_error', "w")
   st1='%8.4f' %diffusion_error
   file3.write(st1)
   file3.close()

   
   sourceFile = curr_dir1 + '/rest_geo'
   destinFile = curr_dir1 + '/fort.3'

   shutil.copy(sourceFile,destinFile)

   sourceFile = curr_dir1 + '/rest_control'
   destinFile = curr_dir1 + '/control'

   shutil.copy(sourceFile,destinFile)

   reaxff_call(num,1)
#end of run cycle
#_____________________________________________________________________

fsock = open('error.log','w')
sys.stderr = fsock

file = open('params')
pnlines = 0
for a1 in file:
   pnlines = pnlines +1

#print "Number of lines in params are ", pnlines
file.close()

file = open(curr_dir + '/params')
params_lines = [None]*pnlines
pnos = range(pnlines)

for i in pnos:
    params_lines[i] = file.readline()
#print params_lines[pnlines-1]

file.close()


sourceFile = curr_dir + '/rest_geo'
destinFile = curr_dir + '/original_rest_geo'

shutil.copy(sourceFile,destinFile)


sourceFile = curr_dir + '/ffield'
destinFile = curr_dir + '/original_ffield'

shutil.copy(sourceFile,destinFile)

#Identifying the position of first line of every section
no_sections = 7
section_lines = [None]*no_sections
section_start_line = [None]*no_sections
nlines_each_section = [None]*no_sections
offset_colomns_section = [None]*no_sections

nlines_each_section[0] = 1
nlines_each_section[1] = 4
nlines_each_section[2] = 2
nlines_each_section[3] = 1
nlines_each_section[4] = 1
nlines_each_section[5] = 1
nlines_each_section[6] = 1

offset_colomns_section[0] = 0

offset_colomns_section[1] = 1
offset_colomns_section[2] = 2
offset_colomns_section[3] = 2
offset_colomns_section[4] = 3
offset_colomns_section[5] = 4
offset_colomns_section[6] = 3

for jj in range(0,pnlines):
   #This is where looping will begin for new parameter line
   file = open(curr_dir + '/ffield')
   nlines = 0
   for a in file:
      nlines= nlines +1
   # print file.read()
   #print nlines
   file.close()

   file = open(curr_dir + '/ffield')
   ffield_lines = [None]*nlines
   nos = range(nlines)
   
   for i in nos:
       ffield_lines[i] = file.readline()
   file.close()
   
   
   fl1 = ffield_lines[1]
   
   section_lines[0] = int (fl1[1:3])
   section_start_line[0]  = 0 
   #print section_lines[0]
   
   n33 = section_lines[0] * nlines_each_section[0] + 1 
   fl1 = ffield_lines[section_lines[0] * nlines_each_section[0] + 1 + 1]
   section_lines[1] = int (fl1[1:3])
   section_start_line[1] = n33
   #print 'n33 is: ', n33
   #print fl1
   print section_start_line[1], 1
   
   
   for i in range(2,no_sections):
      fl2= 0
      j  = 0
      for j in range(0,i):
         fl2 = fl2 + (section_lines[j]+1)* nlines_each_section[j]
         #print 'fl2 is ', i, j, fl2
      fl1= ffield_lines[fl2+1]
      section_lines[i] = int (fl1[1:3])
      section_start_line[i] = fl2
      #print section_start_line[i], i
   
   fl3 = params_lines[jj]
   print 'selected parameter line is: ', fl3 
   section = int (fl3[1:3])-1
   ptype   = int (fl3[4:6])
   param   = int (fl3[7:9])
   dparam    = float(fl3[10:17])
   temp1 = fl3[18:25]
   if(temp1 == ""):
      param_max = 300.00
   else:
      param_max = float(fl3[18:25])
   temp22 = fl3[26:33]
   if(temp22 == ""):
      param_min = -100
   else:
      param_min = float(fl3[26:33])
   #print 'Selected parameter is: ',section, ptype, param
   #print 'Selected parameter line is: ', fl3
   #print 'param value is: ', param
   
   #**Just check max and min values of parameter are written in correct order
   if (param_max < param_min):
      vph       = param_max
      param_max = param_min
      param_min = vph
   
   #**Identify the paramete value
   lineNo = section_start_line[section] +(ptype) * nlines_each_section[section] 
   #print 'linNo is : ', lineNo
   if (section == 1 or section == 2):
      temp33 =abs(param/8)
      temp44 =int(temp33/8) 
      #print 'temp33 is: ', temp33
      lineNo = lineNo + temp33 
      offset = param - (int ((param-1)/8))*8
   else:
      offset = param
   #print 'offset is: ', offset
   num1 = offset_colomns_section[section] * 3 + (offset -1)*9
   #if (num1 < (len(ffield_lines[lineNo]))):
   lineNo = lineNo + 1
   fl4 = ffield_lines[lineNo]
   print 'parameter line is: ',fl4 
   param_val = float(fl4[num1+1:num1+9])
   
   print 'Parameter value is: ', param_val
   icc = 0
   while(icc < 1):
      dparam = parc1*dparam
      for il1 in range(0,3):
   
         new_param_val =change_ff(il1,dparam,param_val,param_max,param_min)
         print 'new_param_val is: ', new_param_val
         stem[il1] = new_param_val
         #print 'paramater value is: ',param_val
         #print 'new parameter value is: ', new_param_val, dparam
         len_fl4 = len(fl4)
         s1= fl4[0:num1+1]
         s2= '%8.4f' %new_param_val
         s3= fl4[num1+9:len_fl4+1]
         lst = [s1,s2,s3]
         #s3= "%9.4fnew_val_param" + s2
         fl5 = "".join(lst)
         ffield_lines[lineNo] = fl5
   
         #print  'parameter line is: ', ffield_lines[lineNo]
         #print ffield_lines[lineNo]
   
         file= open(curr_dir + '/fort.4',"w")
         for i in range(0,nlines):
            fl6= ffield_lines[i]
            file.write(fl6)
         file.close()
   
         file= open(curr_dir + '/ffield_set',"a")
         for i in range(0,nlines):
            fl6= ffield_lines[i]
            file.write(fl6)
         file.close()
         ##where are we?
         #cwd = os.getcwd()
         ##print cwd
         temp_dir = 'val_' + str(il1)
         os.mkdir(temp_dir)  
 
         sourceFile = curr_dir + '/fort.4'
         destinFile = curr_dir + '/'+temp_dir+'/fort.4'
         shutil.copy(sourceFile,destinFile)
         
         sourceFile = curr_dir + '/diff_vels'
         destinFile = curr_dir + '/'+temp_dir+'/diff_vels'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/diff_control'
         destinFile = curr_dir + '/'+temp_dir+'/diff_control'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/diff_geo'
         destinFile = curr_dir + '/'+temp_dir+'/diff_geo'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/reaxff_2'
         destinFile = curr_dir + '/'+temp_dir+'/reaxff_2'
         shutil.copy(sourceFile,destinFile)

         sourceFile = curr_dir + '/rest_geo'
         destinFile = curr_dir + '/'+temp_dir+'/rest_geo'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/rest_control'
         destinFile = curr_dir + '/'+temp_dir+'/rest_control'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/trainset.in'
         destinFile = curr_dir + '/'+temp_dir+'/trainset.in'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/H2O.out'
         destinFile = curr_dir + '/'+temp_dir+'/H2O.out'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/reac_intel'
         destinFile = curr_dir + '/'+temp_dir+'/reac_intel'
         shutil.copy(sourceFile,destinFile)

         sourceFile = curr_dir + '/fort.20'
         destinFile = curr_dir + '/'+temp_dir+'/fort.20'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/fort.35'
         destinFile = curr_dir + '/'+temp_dir+'/fort.35'
         shutil.copy(sourceFile,destinFile)
 
         sourceFile = curr_dir + '/diffusion_coefficient'
         destinFile = curr_dir + '/'+temp_dir+'/diffusion_coefficient'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/compute-msd.list'
         destinFile = curr_dir + '/'+temp_dir+'/compute-msd.list'
         shutil.copy(sourceFile,destinFile)
         sourceFile = curr_dir + '/ip_param'
         destinFile = curr_dir + '/'+temp_dir+'/ip_param'
         shutil.copy(sourceFile,destinFile)
         #run_cycle(il1,0)

      threadLock = threading.Lock()
      threads =[]

      thread1 = myThread(1,"Thread-1", 10)
      thread2 = myThread(2,"Thread-2", 20)
      thread3 = myThread(3,"Thread-3", 30)

      threads.append(thread1)
      threads.append(thread2)
      threads.append(thread3)

      thread1.start()
      thread2.start()
      thread3.start()

      for t in threads:
      	  t.join()
      
      os.chdir(curr_dir)
      errsav = sdy[2]
      #Perform the parabolic extrapolation
      opt_param1 =kmin(param_val,param_max,param_min)
      opt_param_val =change_ff(3,0,opt_param1,param_max,param_min)
      #Write the force field containing oprimized parameter
      len_fl4 = len(fl4)
      s1= fl4[0:num1+1]
      s2= '%8.4f' %opt_param_val
      s3= fl4[num1+9:len_fl4+1]
      lst = [s1,s2,s3]
      #s3= "%9.4fnew_val_param" + s2
      fl5 = "".join(lst)
      ffield_lines[lineNo] = fl5
   
      file= open('fort.4',"w")
      for i in range(0,nlines):
         fl6= ffield_lines[i]
         file.write(fl6)
      file.close()
   
      file= open(curr_dir + '/ffield_set',"a")
      for i in range(0,nlines):
         fl6= ffield_lines[i]
         file.write(fl6)
      file.close()
      run_cycle(2,1,0)

      file5 = open('fort.79',"a")
      file5.write('actual error with optmized parameter value is: ')
      file5.write('\n')
      file5.write(str(sdy[2]))
      file5.write('\n')
      if(sdy[2]>= errsav):
         if(sdy[0]<errsav):
            icc = 10
            fchange = "yes"
            file5.write('optimization failed. still found better value')
         elif(sdy[1]<errsav):
            icc = 10
            fchange = "yes"
            file5.write('optimization failed. still found better value')
         else:
            icc = icc + 1
            fchange = "no"
            file5.write('the optimization failed. trying different dparam')
      else:
         icc = 10
         fchange = "yes"
         file5.write('the optimization is successfull')
      file5.write('\n')
      file5.close()
      shutil.rmtree(curr_dir+'/val_0')
      shutil.rmtree(curr_dir+'/val_1')
      shutil.rmtree(curr_dir+'/val_2')
        
   conv_value = 0.0 
   if(sdy[2] > errsav):
      if(sdy[0] < errsav):
   	 opt_param_val = stem[0]
         conv_value = sdy[0]
      elif(sdy[1] < errsav):
         opt_param_val = stem[1]
         conv_value = sdy[1]
      else:
         opt_param_val = stem[2]
         conv_value = errsav
   else:
      conv_value = sdy[2]

   
   file5 = open('fort.79',"a")
   file5.write('final selected value of parameter is:')
   file5.write('\n')
   file5.write(str(opt_param_val))
   file5.write('\n')
   file5.write('this step is done')
   file5.write('\n')
   file5.close()
   #Write the force field containing oprimized parameter
   #len_fl4 = len(fl4)
   s1= fl4[0:num1+1]
   s2= '%8.4f' %opt_param_val
   s3= fl4[num1+9:len_fl4+1]
   lst = [s1,s2,s3]
   #s3= "%9.4fnew_val_param" + s2
   fl5 = "".join(lst)
   ffield_lines[lineNo] = fl5
  
   file= open('fort.4',"w")
   for i in range(0,nlines):
      fl6= ffield_lines[i]
      file.write(fl6)
   file.close()
  
   sourceFile = curr_dir + '/fort.4'
   destinFile = curr_dir + '/ffield'
   shutil.copy(sourceFile,destinFile)
  
   #write the convergence data
   file12=open(curr_dir + '/conv',"a")
   s22= '%8.4f' %jj+'    '+'%8.4f' %conv_value
   file12.write(s22)
   file12.write('\n')
   file12.close()
   print 'parameter line completed is: ', jj

   file55= open(curr_dir + '/param_track',"a")
   temp77 = str(jj)
   file55.write(temp77)
   file55.write('\n')
   file55.close()


file= open(curr_dir + '/ffield_set',"a")
for i in range(0,nlines):
    fl6= ffield_lines[i]
    file.write(fl6)
file.close()
print 'optimization run has ended successfully'
