#!/usr/bin/env python

# Program created to search for delta scuti stars in Fernandez-Trincado et al. (2015a) data: http://cdsads.u-strasbg.fr/abs/2015A%26A...574A..15F  
# Author: J. G. Fernandez-Trincado
# Status: Article, ApJ, 2016. 
# Last update: 2015 November 13
# This program is a modified version of the original, supported by: https://github.com/keatonb/pyperiod04/blob/master/pyperiod04.py
# J. G. Fernandez-Trincado also thanks Patrick Lenz by the support of "period04-v1.2.0-co140-linux-64bit.csh" (Update: November 2015)

import os
import numpy as np
import scipy as sc

def period04(lc, copy_lc='temp.lc', output_ft='temp.ft', output_project='project.p04', batchfile='batch_temp.bat'):

        """
        [1] lc: array, col1 = time, col2 = mag, col3 = error_mag
        """

        # Constant values ...
        fmin, fmax = str(0), str(50)                                # range of frequencies: mim to max 
        np.savetxt(copy_lc,lc)                                      # Write out the light curve file

        # The new version of Period04 was supported by Patrick Lenz. 
        f = open(batchfile,'w')
        f.write('import to '+copy_lc+'\n')
        f.write('fourier '+fmin+' '+fmax+' o y\n')
        # f.write('addharmonics 3 \n')
        f.write('fit o 2 \n')
        f.write('saveproject '+output_project+'\n')
        f.write('savefourier '+fmin+' '+fmax+' o y '+output_ft+'\n')
        f.write('exit\n')
        f.close()

        os.system('period04 -batch='+batchfile)                     # Run the batch file
        ft = np.loadtxt(output_ft)                                  # Read in the FT
        if copy_lc   == 'temp.lc': os.remove(copy_lc)               # clean up light curve copy
        if batchfile == 'batch_temp.bat': os.remove(batchfile)      # clean up batch file
        return ft                                                   # Return the Period04


lc = sc.genfromtxt('lc.dat')
period04(lc, copy_lc='temp.lc', output_ft='fourier.ft', output_project='project.p04', batchfile='batch_temp.bat')
