#!/bin/python
from __future__ import print_function
import sys
import os
import argparse
import subprocess

class SlurmJob(object):
    def __init__(self,args):
        # Check input actually exists
        if not os.path.isfile(args.infile):
            sys.exit('The input file does not exist!')
        
        # Make sure we have the correct extension
        infile = args.infile.split('.')
        self.software = None
        try:
            extension = infile[1]
        except IndexError:
            sys.exit('Gaussian input file must have .com or .gjf extension')
        if (extension == 'com') or (extension == 'gjf'):
            self.software = 'g16'
        else:
            sys.exit('Gaussian input file must have .com or .gjf extension \n \
                      ...please make the appropriate changes and resubmit.')
     
        self.name        = infile[0]
        self.infile      = args.infile 
        self.threads     = args.nthreads
        self.partition   = args.partition
        self.reservation = args.reservation
        self.time        = args.time
        self.script      = self.name+'.sh'

    def submit_slurm_script(self):
        with open(self.script,'w') as f:
           f.write("#!/bin/bash\n")
           f.write("#SBATCH --job-name="+self.name+"\n")
           f.write("#SBATCH --nodes=1\n")
           f.write("#SBATCH --cpus-per-task="+str(self.threads)+"\n")
           f.write("#SBATCH --partition="+self.partition+"\n")
           f.write("#SBATCH --reservation "+self.reservation+"\n")
           f.write("#SBATCH -t 00:"+str(self.time).zfill(2)+":00\n")
           f.write("\n")
           if self.software == 'g16':
               f.write("module load Gaussian/16-C.01_AVX\n")
               f.write("\n")
               f.write(self.software+" < "+self.infile+" > "+self.name+".log\n")
               f.write("\n")
               f.write("formchk " + self.infile[:-4] + ".chk " + self.infile[:-4] + ".fchk\n")
               f.write("rm slurm-${SLURM_JOB_ID}.out\n")
               f.write("rm core.*\n")
               f.write("rm fort.7\n")
               f.write("rm " + self.script)

        #print(self.software+' submission script written to '+self.script) 
        #print('To submit, do "sbatch '+self.script+'"') 
        subprocess.call(['sbatch',self.script])
        print(self.infile+' was successfully submitted.\n'
              +'\tQueue: '+self.partition+'.\n'
              +'\tReservation: '+self.reservation+'.\n'
              +'\tTime: '+str(self.time)+' minutes.\n'
              +'\tCPUs: '+str(self.threads)+' CPUs.\n'+
               'You can check the status of your job(s) by typing "squeue -u <your_NetID>".')

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Submit Gaussian 16 job on Grace.')
    parser.add_argument("infile", help="Gaussian 16 input file")
    parser.add_argument("-nt", "--nthreads",metavar='N', help="CPUs-per-node",type=int,default=1)
    parser.add_argument("-p","--partition",metavar='P',help="queue",type=int,default='day')
    parser.add_argument("-r","--reservation",metavar='R',help="reservation",type=int,default='chem496')
    parser.add_argument("-t","--time",metavar='T',help="time (min)",type=int,default=15)
    args = parser.parse_args()

    slurmjob = SlurmJob(args)
    slurmjob.submit_slurm_script()

