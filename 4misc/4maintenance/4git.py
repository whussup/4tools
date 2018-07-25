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

import os, sys, re, subprocess, time, inspect, requests

repositories=re.compile("<div\sclass=\"d-inline-block.*?\">.*?<h3>.*?<a\shref=\"(.*?)\"\sitemprop=\"name.*?\">(.*?)</a>.*?</h3>.*?</div>", re.S)
repo_name=re.compile("https://github.com/(.*?)/")
pages=re.compile("<div\sclass=\"pagination\">(.*?)</div>")
pages_ints=re.compile("<a\srel=\"next\"\shref=\".*?\">(.*?)</a>")
regx_update=re.compile("git pull")
regx_clone=re.compile("git clone")

def procs_count(regx):
    cmd=["ps", "ax"]
    procs=str(subprocess.check_output(cmd))
    return int(len(regx.findall(procs)))

def dump_repos(url, dr, response=False):
    if response == True:
        r=url
    else:
        r=requests.get(url)
    rps=repositories.findall(r.text)
    if rps != []:
        link=rps[0]
        name=rps[1]
        sdir = src_dirs
        for rp in rps:
            cmd=["git", "clone", "https://github.com"+rp[0], ]
            print(cmd)
            procs.append(subprocess.Popen(cmd, cwd=dr))
            i=procs_count(regx_clone)
            print(i)
            while i > max_count:
                i=procs_count(regx_clone)
                print("waiting for empty workspace...max_count:"+str(max_count))
                time.sleep(1)
try:
    cmd = sys.argv[1]
    if cmd == "update":
        try:
            src_dirs=sys.argv[2]
        except:
            print("no source dir specified | usage 4git.py update directory count \nFalling back to cwd..."+src_dirs)
        try:
            src_dirs=int(sys.argv[3])
        except:
            print("no max_count specified | usage 4git.py update directory count \nFalling back to max_count:"+str(max_count))
    elif cmd == "clone":
        try:
            url=sys.argv[2]
            rname=repo_name.findall(url)
            if rname == []:
                ""+1
            r=requests.get(url)
        except:
            print("no valid url specified | usage 4git.py clone git_repo_parent_url directory count \n")
        try:
            src_dirs=sys.argv[3]
        except:
            print("no source destination specified | usage 4git.py clone git_repo_parent_url directory count \nFalling back to cwd..."+src_dirs)
        try:
            src_dirs=int(sys.argv[3])
        except:
            print("no max_count specified | usage 4git.py clone git_repo_parent_url directory count \nFalling back to max_count:"+str(max_count))
except:
    print("no valid cmd specified | valid cmds clone, update")
    print("usage 4git.py clone git_repo_parent_url directory count ")
    print("usage 4git.py update directory count ")
    exit()

procs=[]

if cmd == "update":
    for sdir in os.walk(src_dirs):
        if(os.path.isdir(sdir[0]+"/.git")):
            sdir = sdir[0]
            cmd=["git", "pull"]
            procs.append(subprocess.Popen(cmd, cwd=sdir))
            i=procs_count(regx_update)
            while i > max_count:
                i=procs_count(regx_update)
                print("waiting for empty workspace...max_count:"+str(max_count))
                time.sleep(1)

elif cmd == "clone":
    pgs=[]
    rname=repo_name.findall(url)
    rname=rname[0]
    cmd=["mkdir",rname]
    try:
        procs.append(subprocess.Popen(cmd, cwd=src_dirs))
    except:
        print("repo_parent name already exists continue with cloning...")
    pgs=pages.findall(r.text)
    pgs_ints=pages_ints.findall(pgs[0])
    dump_repos(r, src_dirs+"/"+rname, True)
    for pg in pgs_ints:
        try:
            url_=url+"?page="+str(int(pg))
        except:
            continue
        dump_repos(url_, src_dirs+"/"+rname)
