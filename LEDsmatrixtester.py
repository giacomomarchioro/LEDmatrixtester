# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 23:01:09 2014

@author: giacomo
This is a script to test brightness of a LEDs matrix. Create an instance of  testLEDsMatrix() class and then use its functions to report measured birghtness and resistance values.
"""
import pickle
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import numpy as np
import matplotlib

print "create an instance with testLEDsMatrix()" 

def saveobject(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output,-1)

def loadobject(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

###Paul H code for shifted color map http://stackoverflow.com/questions/7404116/defining-the-midpoint-of-a-colormap-in-matplotlib/20528097#20528097

def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and 1.0.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          0.0 and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap
        
class testLEDsMatrix:
    
    '''
        This is the main class used to perfom the test. Create an instance of this class (e.g. matrix1=testLEDsMatrix()) then use the following functions:
            
            matrix1.Measure Brightness : to insert  experimental brightness values for every LED.
            
            matrix1.Measure Resistence : to insert experimental or nominal resistence value for every resistance..
            
            matrix1.plotresult : to plot the resulting data
            matrix1.saveobject : to save the data in an external file
        Input
        -----
        projectname='test' type your project name (e.g. testLEDsMatrix('matrixBlueLEDs')) by default is set to 'test'.
        
    '''
    
    def __init__(self,projectname='test'):
        self.projectname=projectname
        self.num_col=0
        self.num_lines=0
        self.resistancecolumn=0
        self.trend=[]
        self.trend2=[]
        self.LEDs={}
        self.R={}
        
    def MeasureBrightness(self):
        '''
        Function used to input brightness values from the LEDs matrix
        
        Input
        -----
        
        Don't pass any arguments, function automatically ask you what it needs.
        '''
        print "Insert parameters for your matrix:"                   
        self.num_col=input('number of columns:')
        self.num_lines=input('number of lines:')
        num_mes=input('number of test for every LED:')
        for i in range(self.num_lines):#righe
            for k in range(self.num_col):#colonne
                 self.LEDs[(chr(65+i)+str(k))]=[]
        
        for z in range(num_mes):
            for gg in range(self.num_lines):#righe
                for h in range(self.num_col):#colonne
                    value=input('Value for the component %s:' %((chr(65+gg)+str(h))))
                    self.LEDs[(chr(65+gg)+str(h))].append(value)
                    self.trend.append(value)
    
    
    def MeasureResistance(self):
        '''
        Function used to input resistance values from the LEDs matrix
        Input
        -----
        Don't pass any arguments, function automatically ask you what it needs.
        '''
        num_mes=input('number of test for every LED:')
        for resi in range(self.num_lines):#righe
                 self.R[('R'+str(resi))]=[]
        
        for MM in range(num_mes):
            for RR in range(self.num_lines):#righe
                    value=input('Valore per il compoenent %s:' %(('R'+str(RR))))
                    self.R[('R'+str(RR))].append(value)
                    self.trend2.append(value)
        self.resistancecolumn=1
    
    
    
    
    def plotresult(self):    
        '''
        Plot data with matplotlib
        -----
        Don't pass any arguments.
        '''
        orig_cmap = matplotlib.cm.coolwarm
        shrunk_cmap = shiftedColorMap(orig_cmap, start=min(self.trend)/max(self.trend), midpoint=np.mean(self.trend)/max(self.trend), stop=1, name='shrunk')
        
        fig, ax = plt.subplots()
        for rf in range(self.num_lines):#righe
            ax.add_line(matplotlib.lines.Line2D([-1,0],[4*rf+1.5,4*rf+1.5]) )
            for s in range(self.num_col):#colonne
                ax.add_artist(mpatch.Rectangle((4*s,4*rf), 3, 3, facecolor=shrunk_cmap((np.mean(self.LEDs[(chr(65+rf)+str(s))]))/max(self.trend)))) 
                ax.annotate((chr(65+rf)+str(s)), (4*s+1.5, 4*rf+1.5), color='w', weight='bold', 
                            fontsize='large', ha='center', va='center')
                ax.annotate("%0.1f" %(np.mean(self.LEDs[(chr(65+rf)+str(s))])), (4*s+0.2, 4*rf+2.8), color='w', weight='bold', 
                            fontsize='medium', ha='left', va='top')
                ax.annotate("sd:%0.1f" %(np.std(self.LEDs[(chr(65+rf)+str(s))])), (4*s + 0.2, 4*rf+0.2), color='black', weight='bold', 
                            fontsize='small', ha='left', va='bottom')
                ax.add_line(matplotlib.lines.Line2D([4*s+3,4*s+4],[4*rf+1.5,4*rf+1.5]) )
        if self.resistancecolumn==1:
            print "right"
            for resll in range(self.num_lines):#colonne
                    ax.add_artist(mpatch.Rectangle((4*self.num_col,4*resll+1), 3, 1, facecolor=shrunk_cmap((np.mean(self.R['R'+str(resll)]))/max(self.trend2)))) 
                    ax.annotate(('R'+str(resll)), (4*self.num_col+1.5, 4*resll+1.5), color='w', weight='bold', 
                                fontsize='large', ha='center',va='center')
                    ax.annotate("sd:%0.1f $\Omega$" %(np.std(self.R['R'+str(resll)])), (4*self.num_col+1.5, 4*resll+0.9), color='black', weight='bold', 
                                fontsize='small', ha='center', va='top')
                    ax.annotate("%0.1f$\Omega$" %(np.mean(self.R['R'+str(resll)])), (4*self.num_col+1.5, 4*resll+2.1), color='black', weight='bold', 
                                fontsize='medium', ha='center', va='bottom')
                    ax.add_line(matplotlib.lines.Line2D([4*self.num_col+3,4*self.num_col+4],[4*resll+1.5,4*resll+1.5]) )
                       
        ax.add_line(matplotlib.lines.Line2D([-1,-1],[-1.5,4*(self.num_lines)-2.5]))  
        ax.add_line(matplotlib.lines.Line2D([4*(self.num_col+self.resistancecolumn),4*(self.num_col+self.resistancecolumn)],[-1.5,4*(self.num_lines)-2.5]))                                 
        ax.annotate("+", (-1, -2.8), color='red', weight='bold',fontsize='xx-large', ha='center', va='bottom')
        ax.annotate("-", (4*(self.num_col+self.resistancecolumn), -2.8), color='blue', weight='bold',fontsize='xx-large', ha='center', va='bottom')
        ax.set_xlim(-3,4*(self.num_col+self.resistancecolumn)+1)
        ax.set_ylim(-3,4*self.num_lines+1)
        ax.set_aspect('equal')
        plt.grid(color='red')
        plt.axis('off')
        plt.title("Brightness test: %s (mean:%0.1f,std:%0.1f,ratio:%0.1f%%)" %(self.projectname,np.mean(self.trend),np.std(self.trend),np.std(self.trend)/np.mean(self.trend)*100))
        #sm = plt.cm.ScalarMappable(cmap=shrunk_cmap)
        #plt.colorbar(sm)
        plt.show()
    
