#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# Idea / Written by Sebastian Vivian Gresser - All Rights Reserved
#
# Copyright (C) by geeBee UG (haftungsbeschränkt) - All Rights Reserved
# Copyright (C) by Sebastian Vivian Gresser - All Rights Reserved
#
########################################################################

# number of parallel update processes
max_count=10

import os, sys, re, subprocess, time, inspect

regx=re.compile("git pull")

def procs_count():
    global regx
    cmd=["ps", "ax"]
    procs=str(subprocess.check_output(cmd))
    return int(len(regx.findall(procs)))

try:
    src_dirs=sys.argv[1]
except:
    src_dirs=os.getcwd()
    print("no source dir specified | usage 4git.py directory count \nFalling back to cwd..."+src_dirs)
try:
    src_dirs=int(sys.argv[2])
except:
    print("no max_count specified | usage 4git.py directory count \nFalling back to max_count:"+str(max_count))

procs=[]

for sdir in os.walk(src_dirs):    
    if(os.path.isdir(sdir[0]+"/.git")):
        sdir = sdir[0]
        cmd=["git", "pull"]
        print(cmd)
        procs.append(subprocess.Popen(cmd, cwd=sdir))
        i=procs_count()
        while i > max_count:
            i=procs_count()
            print("waiting for empty workspace...max_count:"+str(max_count))
            time.sleep(1)







