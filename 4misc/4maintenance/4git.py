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


import os, sys, re, subprocess

try:
    src_dirs=sys.argv[1]
except:
    src_dirs=os.getcwd()
    print("no source dir specified | usage 4git.py directory \nFalling back to cwd..."+src_dirs)


for sdir in os.walk(src_dirs):    
    if(os.path.isdir(sdir[0]+"/.git")):
        sdir = sdir[0]
        cmd=["screen", "-dmt", "git_repo_worker", "git", "-C", sdir, "pull"]
        print(cmd)
        subprocess.Popen(cmd)





