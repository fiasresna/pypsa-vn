#!/usr/bin/python3

import os
import time as t

files=os.listdir('./')
files.sort()
files.remove('execute_optimisations.py')
files.remove('slurm_batches.py')

#counter = 0

for f in files:

    job_name = '--job-name='+f
    partition = '--partition=' # your machine cluster
    nodes = '--nodes=1'
    ntasks = '--ntasks=1'
    cpus = '--cpus-per-task=32'
    memory = '--mem=62000'
    output = '--output='+f[:-3]+'.out'
    time = '--time=10-00:00:00'

    print('Call "' +
          'sbatch' + ' ' + job_name + ' ' + partition + ' ' + nodes + ' ' +
                           ntasks + ' ' + cpus + ' ' + memory + ' ' + output + ' ' + time + ' ' +
          'slurm_batches.py' + ' ' + f + '"')

    os.system('sbatch' + ' ' + job_name + ' ' + partition + ' ' + nodes + ' ' +
                               ntasks + ' ' + cpus + ' ' + memory + ' ' + output + ' ' + time + ' ' +
              'slurm_batches.py' + ' ' + f)

