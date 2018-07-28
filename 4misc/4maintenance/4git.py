#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# 4git - for collecting, updating and investigating repos @github
#
# VERSION 0.0.3
#
# Idea / Written by Sebastian Vivian Gresser - All Rights Reserved
#
# Copyright (C) by geeBee UG (haftungsbeschränkt) - All Rights Reserved
# Copyright (C) by Sebastian Vivian Gresser - All Rights Reserved
#
########################################################################

# number of parallel update processes
max_count=10
# change this settings for not using github
# should work for any webinterface based github clone
parent_url="https://github.com"
repos_url_add="?tab=repositories"

import os, sys, re, subprocess, time, requests
repositories=re.compile("<h3.*?>.*?<a.*?href=\"(.*?)\".*?>.*?</a>.*?</h3>", re.S)
repo_name=re.compile(parent_url+"/(.*?)$")
search_regx=re.compile(".*?search\?q\=(.*?)$")
regx_update=re.compile("git pull")
regx_clone=re.compile("git clone")
next_page_regx=re.compile("rel=\"next\".*?href=\"(.*?)\">(.*?)</a>")
def procs_count(regx):
    cmd=["ps", "ax"]
    procs=str(subprocess.check_output(cmd))
    return int(len(regx.findall(procs)))
def dump_repos(url, dr):
    r=requests.get(url)
    next_page = next_page_regx.findall(r.text)
    rps=repositories.findall(r.text)
    if rps != []:
        sdir = src_dirs
        for rp in rps:
            cmd=["git", "clone", parent_url+rp]
            procs.append(subprocess.Popen(cmd, cwd=dr))
            i=procs_count(regx_clone)
            while i > max_count:
                i=procs_count(regx_clone)
                print("waiting for empty workspace...max_count:"+str(max_count))
                time.sleep(7)
    if next_page != []:
        next_page = next_page.pop()[0]
        time.sleep(20)
        dump_repos(parent_url+next_page, dr)
try:
    cmd = sys.argv[1]
    if not cmd in ["update", "clone"]:
        ""+1
    if cmd == "update":
        try:
            src_dirs=sys.argv[2]
        except:
            print("no source dir specified | usage 4git.py update directory count \nFalling back to cwd..."+src_dirs)
        try:
            max_count=int(sys.argv[3])
        except:
            print("no max_count specified | usage 4git.py update directory count \nFalling back to max_count:"+str(max_count))
    elif cmd in ["clone"]:
        try:
            url=sys.argv[2]
            rname=repo_name.findall(url)
            if rname == []:
                ""+1
            r=requests.get(url)
        except:
            print("no valid url specified | usage 4git.while py clone git_repo_parent_url directory count \n")
        try:
            src_dirs=sys.argv[3]
        except:
            print("no source destination specified | usage 4git.py clone git_repo_parent_url directory count \nFalling back to cwd..."+src_dirs)
        try:
            max_count=int(sys.argv[4])
        except:
            print("no max_count specified | usage 4git.py chttps://github.com/CoolerVoid?page=2&tab=followinglone git_repo_parent_url directory count \nFalling back to max_count:"+str(max_count))
except:
    print("no valid cmd specified | valid cmds clone, clone_if, update")
    print("usage 4git.py clone git_repo_parent_url directory count (clones the whole repository of the holder)")
    print("usage 4git.py update directory count (updates all repositories which directories are childs of directory)")
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
                time.sleep(7)
elif cmd in ["clone"]:
    pgs=[]
    if url.find("?q=") == -1:
        rname=repo_name.findall(url)
        rname=rname[0]
        url=url+repos_url_add
    else:
        rname=search_regx.findall(url)
        rname=rname[0].replace("+", "_")
    cmd=["mkdir",rname]
    try:
        procs.append(subprocess.Popen(cmd, cwd=src_dirs))
    except:
        print("repo_parent name already exists continue with cloning...")
    dump_repos(url, src_dirs+"/"+rname)
