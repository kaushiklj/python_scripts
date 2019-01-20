import numpy as np
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import math


#if1_name = "first.xyz"
#if2_name = "cycles.dat"
periodic_flag = 1
min_points = 5
max_points = 7
ring_color_flag = 1
##filenames = ['1.64_start','1.64_end',
##             '1.82_start','1.82_end',
##             '1.72_start','1.72_end',
##             '1.80_start','1.80_end',
##             '1.93_start','1.93_end'] #code will assume actual filename will have xya extension

filenames = ['1g_end']
#filenames = ['ng_end','config2_1g_end','2g_end','3g_end','4g_end','5g_end']

#------------------------------------------------------------
def read_xyz_file(filename,natoms,at_names,xcor,ycor,zcor,lxyz):
    count = 0
    with open(filename,'r') as if1:
        for line in if1:
            if (count == 0):
                natoms.append(int(line))
                count = count + 1
            elif (count == 1):
                line1 = line.split()
                if (len(line1) != 0):
                    for i1 in range(0,len(line1)):
                        lxyz.append(line1[i1])
                    if (len(lxyz) == 9):
                        for i1 in range(0,len(lxyz)):
                            lxyz[i1] = float(lxyz[i1])
                count = count + 1
            else:
                line1 = line.split()
                at_names.append(line1[0])
                xcor.append(float(line1[1]))
                ycor.append(float(line1[2]))
                zcor.append(float(line1[3]))
    lxyz[0] = min(xcor)
    lxyz[1] = max(xcor)
    lxyz[2] = min(ycor)
    lxyz[3] = max(ycor)
    lxyz[4] = min(zcor)
    lxyz[5] = max(zcor)
#____________________________________________________________

#------------------------------------------------------------
def read_points_data(if2_name,nplanes,points):
    count = 0
    with open(if2_name,'r') as if2:
        for line in if2:
            line1 = line.split()
            if (len(line1) != 0):
                points.append([])
                for i1 in range(1,len(line1)):
                    points[count].append(int(line1[i1]))
                count = count + 1
    nplanes.append(len(points))
#____________________________________________________________

#------------------------------------------------------------
def read_ring_xyz(filename,ring_xc,ring_yc,ring_zc,ring_nm):
    count = 0
    with open(filename,'r') as if1:
        for line in if1:
            count = count + 1
            if (count > 2):
                line1 = line.split()
                ring_xc.append(float(line1[1]))
                ring_yc.append(float(line1[2]))
                ring_zc.append(float(line1[3]))
                ring_nm.append('Z')
#____________________________________________________________

#------------------------------------------------------------
def check_periodic(list1,cell_param,cell_low):
    min_val = min(list1)
    max_val = max(list1)

    if (max_val - min_val > cell_param/2.0):
        for i1 in range(0,len(list1)):
            if (list1[i1] > cell_param/2.0+cell_low):
                list1[i1] = list1[i1] - cell_param
    
#____________________________________________________________

#------------------------------------------------------------
def fit_plane(plane_fits,temp_x,temp_y,temp_z,lxyz,periodic_flag):
    #equation being solved is ax + by + c = z. 
    #so normal vector set is (a,b,-1)
    if (periodic_flag == 1):
        check_periodic(temp_x,lxyz[1]-lxyz[0],lxyz[0])
        check_periodic(temp_y,lxyz[3]-lxyz[2],lxyz[2])
        check_periodic(temp_z,lxyz[5]-lxyz[4],lxyz[4])

    temp_A = []
    temp_B = []
    for i1 in range(0,len(temp_x)):
        temp_A.append([temp_x[i1],temp_y[i1],1])
        temp_B.append(temp_z[i1])
    B = np.matrix(temp_B).T
    A = np.matrix(temp_A)
    #print (A)
    #print (B)
    fit = []
    fit = (A.T * A).I * A.T * B
    error = B-A*fit
    #print (error)
    #print(fit)
    #fit.append(error)
    plane_fits.append(fit)
#____________________________________________________________

#------------------------------------------------------------
def plot_desired_plane(frame_no,plane_fits,temp_x,temp_y,temp_z):
    mesh_points = 8
    plt.figure()
    ax =plt.subplot(111,projection='3d')
    ax.scatter(temp_x,temp_y,temp_z,color='b',linewidth = 10)
    print (temp_x)
    print (temp_y)
    print (temp_z)
    print(ax.get_xlim())
    print(ax.get_ylim())
    print(ax.get_zlim())

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    dx = (xlim[1]-xlim[0])/mesh_points
    dy = (ylim[1]-ylim[0])/mesh_points
    X,Y = np.meshgrid(np.arange(xlim[0],xlim[1],0.25),
                      np.arange(ylim[0],ylim[1],0.05))
    print (xlim)
    print (ylim)
    Z = np.zeros(X.shape)
    for i1 in range(X.shape[0]):
        for i2 in range(X.shape[1]):
            Z[i1,i2] = plane_fits[frame_no][0]*X[i1,i2] + plane_fits[frame_no][1]*Y[i1,i2] + plane_fits[frame_no][2]
    ax.plot_wireframe(X,Y,Z,color='k')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
#____________________________________________________________

#-----------------------------------------------------------------
def calculate_hof(cosine_values):
    temp_sum = 0
    for i1 in range(0,len(cosine_values)):
        #temp_sum = ((math.cos(plane_fits[i1][0]))**2) + temp_sum
        temp_sum = (cosine_values[i1]**2) + temp_sum
    if (len(plane_fits) != 0):
        temp_sum = temp_sum/(len(plane_fits))
    return (3*temp_sum-1)/2.0
#_________________________________________________________________

#-----------------------------------------------------------------
def get_histograms(list1,low,high,nbins,filename):
    bin_range = np.linspace(low,high,nbins)
    freq,bin_edges = np.histogram(list1,bin_range)
    of1 = open(filename,'w')
    for i1 in range(0,len(freq)):
        of1.write('%f %f\n'%(bin_edges[i1],freq[i1]*100/(len(list1))))
    of1.close()
#_________________________________________________________________

#-----------------------------------------------------------------
def get_2d_histogram(data,nbins,hist_range):
    x = []
    y = []
    for i1 in range(0,len(data)):
        x.append(data[i1][0])
        y.append(data[i1][1])


    values, xedges, yedges = np.histogram2d(x,y,bins = nbins, range = hist_range)
    ntot = 0
    for i1 in range(0,len(values)):
        for i2 in range(0,len(values[0])):
            ntot = ntot + values[i1][i2]
    print (ntot)
    

    for i1 in range(0,len(values)):
        for i2 in range(0,len(values[0])):
            values[i1][i2] = values[i1][i2]*100/ntot
    print (values)
    print (xedges)
    print (yedges)
    values = values.T
    extent_list = [xedges[0],xedges[-1],yedges[0],yedges[-1]]
    #bounds = [0.0,1.0,2.0,4.0,8.0,16.0,32.0]
    #cmap = mpl.colors.ListedColormap(['ghostwhite','royalblue','cornflowerblue','green','yellow','orange'])
    #cmap.set_over('red')
    #cmap.set_under('blue')
    #norm = mpl.colors.BoundaryNorm(bounds,cmap.N)
    cmap = mpl.cm.rainbow
    #norm = mpl.colors.Normalize(vmin=0,vmax = 40)
    plt.clf()
    plt.imshow(values,aspect = 'auto', origin = 'lower',extent = extent_list,interpolation = 'nearest',cmap = cmap, norm = LogNorm())
    #plt.hist2d(x,y,bins = nbins, range = hist_range, norm = LogNorm())
    #plt.hist2d(x,y,bins = nbins, range = hist_range)
    #plt.plot(values)
    plt.colorbar()
    plt.show()

#-------------------------------------------------------------------
def get_3d_histogram(data,bins,hist_range,filename):
    zlim = 5
    zpoints = 6
    x = []
    y = []
    for i1 in range(0,len(data)):
        x.append(data[i1][0])
        y.append(data[i1][1])
    #plt.clf()
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    values, xedges, yedges = np.histogram2d(x,y,bins = nbins, range = hist_range)
    #print (xedges)

    ntot = 0
    for i1 in range(0,len(values)):
        for i2 in range(0,len(values[0])):
            ntot = ntot + values[i1][i2]
    print (ntot)
    

    for i1 in range(0,len(values)):
        for i2 in range(0,len(values[0])):
            values[i1][i2] = values[i1][i2]*100/ntot

    xpos,ypos = np.meshgrid(xedges[:-1],yedges[:-1])
    #print (xpos)
    xpos = xpos.flatten('F')
    #print (xpos)
    ypos = ypos.flatten('F')
    zpos = values.flatten()

    dx = (xedges[-1]-xedges[0])/len(xedges)
    dy = (yedges[-1]-yedges[0])/len(yedges)
    dz = zpos

    ax.bar3d(xpos,ypos,np.zeros(len(zpos)),dx,dy,dz,color = 'red')
    #ax.set_axes(fontsize = 15)
    ax.set_xlabel(r'cos$\theta$',fontsize = 20,labelpad = 10)
    ax.set_ylabel(r'$\phi$',fontsize = 20,labelpad = 10)
    ax.set_zlabel('% rings',fontsize = 20,labelpad = 8)
    #ax.set_xticks(np.linspace(-3.14,3.14,5))
    ax.set_xticks(np.linspace(hist_range[0][0],hist_range[0][1],5))
    ax.tick_params(labelsize = 'large')
    ax.set_yticks(np.linspace(hist_range[1][0],hist_range[1][1],3))
    ax.set_zlim(0,zlim)
    ax.set_zticks(np.linspace(0,zlim,zpoints))

    fig.savefig(filename +'.png')
    
    #plt.show()

#----------------------------------------------------------------------
def screen_planes(screening_range,dim,plane_orien,points,xcor,ycor,zcor):
    at_count = 0
    plane_list = []
    natoms = len(xcor)
    at_flags = [0]*natoms
    
    for i1 in range(0,len(plane_orien)):
        val = plane_orien[i1][dim]
        for i2 in range(0,len(screening_range)):
            if (screening_range[i2][0] < val < screening_range[i2][1]):
                plane_list.append(plane_orien[i1][2]-1)
                
    for i1 in range(0,len(plane_list)):
        plane_no = plane_list[i1]
        for i2 in range(0,points[plane_no][0]):
            at_id = points[plane_no][i2+1]-1
            if (at_flags[at_id] == 0):
                at_flags[at_id] = 1
                at_count = at_count + 1
    of1 = open('screened_planes.xyz','w')
    of1.write('%d\n'%(at_count))
    of1.write('\n')
    for i1 in range(0,natoms):
        if (at_flags[i1] == 1):
            of1.write('C %f %f %f\n'%(xcor[i1],ycor[i1],zcor[i1]))
        
    of1.close()
#_______________________________________________________________________

#----------------------------------------------------------------------
def get_1d_histogram(data,nbins,hist_range,filename):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    x = []
    for i1 in range(0,len(data)):
        x.append(data[i1])
    values,bin_edges = np.histogram(x,nbins,range=hist_range)
    ntot = sum(values)
    #print (values[10])
    print(ntot)
    for i1 in range(0,len(values)):
        values[i1] = values[i1]*100/ntot
    
    ax.bar(bin_edges[1:],values,color = 'r',width = 0.09)
    if (max(values)< 20.0 ):
        ax.set_yticks(np.linspace(0,20,5))
    else:
        ax.set_yticks(np.linspace(0,60,7))
    ax.set_xticks(np.linspace(-1,1,9))
    ax.tick_params(labelsize = 'medium')
    ax.set_xlabel(r'cos$\alpha_y$',fontsize = 15,labelpad = 5)
    ax.set_ylabel('% rings',fontsize = 20,labelpad = 10)
    fig.savefig(filename +'_x.png')
    of1 = open(filename+'_x.dat','w')
    for i1 in range(0,len(values)):
        of1.write('%f %f\n'%(bin_edges[i1+1]-0.05,values[i1]))
    of1.close()
               
    #plt.show()
#----------------------------------------------------------------------

#-----------------------------------------------------------------------
def write_ring_center_colors(ring_color_data,filename):
    of1 = open(filename+'_ring_colors.xyz','w')
    of1.write('%d\n'%(len(ring_color_data)))
    of1.write('\n')
    for i1 in range(0,len(ring_color_data)):
        of1.write('%s %f %f %f\n'%(ring_color_data[i1][0],ring_color_data[i1][1],ring_color_data[i1][2],ring_color_data[i1][3]))
              
    of1.close()
#_______________________________________________________________________


for filecount in range(0,len(filenames)):
    print('starting file '+filenames[filecount])
    if1_name = filenames[filecount]+'.xyz'
    if2_name = filenames[filecount]+'_cycles.dat'
    if3_name = filenames[filecount]+'_rings.xyz'
    xcor = []
    ycor = []
    zcor = []
    at_names = []
    lxyz = []
    natoms = []
    points = []
    nplanes = []
    plane_fits = []
    plane_orien = []
    xangles = []
    yangles = []
    zangles = []
    if (ring_color_flag == 1):
        ring_xc = []
        ring_yc = []
        ring_zc = []
        ring_nm = []
    plot_plane_number = 25000 #13330
    screening_range = [[-3.15,-3.05],[3.05,3.15]]

    read_xyz_file(if1_name,natoms,at_names,xcor,ycor,zcor,lxyz)
    read_points_data(if2_name,nplanes,points)
    if (ring_color_flag == 1):
        read_ring_xyz(if3_name,ring_xc,ring_yc,ring_zc,ring_nm)

    plane_count = 0
    ring_color_data = []
    color_plane_count = 0

    for i1 in range(0,nplanes[0]):
        temp_x = []
        temp_y = []
        temp_z = []
        
        if (points[i1][0] >=min_points and points[i1][0] <= max_points):
            for i2 in range(0,points[i1][0]):
                at_id = points[i1][i2+1]-1
                temp_x.append(xcor[at_id])
                temp_y.append(ycor[at_id])
                temp_z.append(zcor[at_id])
            #Following part is required for a group of points who have same x or y
            # or z coordinates (so equation of plane will be y =c or x = c or z =c
            #The algorithm used for identifying equation of plane fails for such cases
            # because inverse matrix has very big values due to singularities
            if all(val == temp_x[0] for val in temp_x):
                #perpendicular exactly parallel to x-axis
                xvec = temp_x[0]/abs(temp_x[0])
                yvec = 0.0
                zvec = 0.0
            elif all(val == temp_y[0] for val in temp_y):
                #perpendicular exactly parallel to y-axis
                xvec = 0.0
                yvec = temp_y[0]/abs(temp_y[0])
                zvec = 0.0
            elif all(val == temp_z[0] for val in temp_z):
                xvec = 0.0
                yvec = 0.0
                zvec = temp_z[0]/abs(temp_z[0])
            else:
                fit_plane(plane_fits,temp_x,temp_y,temp_z,lxyz,periodic_flag)
                elem = len(plane_fits)
                xvec = plane_fits[elem-1][0]
                yvec = plane_fits[elem-1][1]
                cvec = plane_fits[elem-1][2]
                mag = math.sqrt(xvec*xvec+yvec*yvec+1)
                xvec = xvec/mag
                yvec = yvec/mag
                if (cvec > 0.0 ):
                    zvec = -1.0/mag
                else:
                    zvec = 1.0/mag

##                if (i1+1 == plot_plane_number):
##                    print (i1+1)
##                    print (plane_count+1)
##                    plot_desired_plane(plane_count,plane_fits,temp_x,temp_y,temp_z)
                    
           
            #plane_orien.append([theta,phi,i1+1])
            #plane_orien.append([math.cos(theta),phi,i1+1])
            xangles.append(xvec)
            yangles.append(yvec)
            zangles.append(zvec)
            #print(plane_orien[-1])
            if (ring_color_flag == 1):
                if (0.0 < abs(xvec) < 0.1):
                    ring_nm[i1] = 'O'
                elif (0.1 < abs(xvec) < 0.2):
                    ring_nm[i1] = 'C'
                elif (0.2 < abs(xvec) < 0.3):
                    ring_nm[i1] = 'N'
                else:
                    ring_nm[i1] = 'H'
                ring_color_data.append([ring_nm[i1],ring_xc[i1],ring_yc[i1],ring_zc[i1]])
                
                
            plane_count = plane_count + 1
                     
    nbins = [36,18]
    #hist_range = [[0,3.14],[0,3.14]]
    hist_range = [[-1,1],[0,3.14]]
    #get_2d_histogram(plane_orien,nbins,hist_range)
    #get_3d_histogram(plane_orien,nbins,hist_range,filenames[filecount])
    get_1d_histogram(xangles,20,[-1,1],filenames[filecount])
    hof = calculate_hof(xangles)
    print ('HOF is %f'%(hof))
    if (ring_color_flag == 1):
        write_ring_center_colors(ring_color_data,filenames[filecount])
##
##    if (screening_range != []):
##        screen_planes(screening_range,0,plane_orien,points,xcor,ycor,zcor)
