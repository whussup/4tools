#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# 4git - for collecting, updating and investigating repos @github
#
# VERSION 0.0.4
#
# Idea / Written by Sebastian Vivian Gresser - All Rights Reserved
#
# Copyright (C) by geeBee UG (haftungsbeschränkt) - All Rights Reserved
# Copyright (C) by Sebastian Vivian Gresser - All Rights Reserved
#
########################################################################

# number of parallel processes
max_count=4
# change this settings for not using github
# should work for any webinterface based github clone
repos_url_add="?tab=repositories"

import re
repositories=re.compile("<h3.*?>.*?<a.*?href=\"(.*?)\".*?>.*?</a>.*?</h3>", re.S)
parent_url_regx=re.compile("(.*?)://(.*?)/")
repo_name=re.compile("^.*?//.*?/(.*?)$")
search_regx=re.compile(".*?search\?q\=(.*?)$")
regx_update=re.compile("git pull")
regx_clone=re.compile("git clone")
next_page_regx=re.compile("rel=\"next\".*?href=\"(.*?)\">(.*?)</a>")

#next_page_ppl_regx=re.compile("<div\sclass=\"pagination\">.*?<a.*?href=\"(.*?)\">Next</a>", re.S)
ppl_regx=re.compile("<div.*?<a.*data-hovercard-type=\"user\".*href=\"(.*?)\">.*?</a>.*?</div>", re.S)

del re


def urllib_get(url):
    import urllib
    r=urllib.urlopen(url).read()
    del urllib
    return r

def procs_count(regx):
    cmd=["ps", "ax"]
    import subprocess
    procs=str(subprocess.check_output(cmd))
    del subprocess
    return int(len(regx.findall(procs)))

def dump_repos(url, dr):
    urllib_get(url)
    next_page = next_page_regx.findall(r)
    rps=repositories.findall(r)
    if rps != []:
        sdir = src_dirs
        for rp in rps:
            cmd=["git", "clone", parent_url+rp]
            import subprocess
            procs.append(subprocess.Popen(cmd, cwd=dr))
            del subprocess
            i=procs_count(regx_clone)
            while i > max_count:
                i=procs_count(regx_clone)
                print("waiting for empty workspace...max_count:"+str(max_count))
                import time
                time.sleep(7)
                del time
    if next_page != []:
        next_page = next_page.pop()[0]
        import time
        time.sleep(20)
        del time
        dump_repos(parent_url+next_page, dr)
try:
    import sys
    cmd = sys.argv[1]
    if not cmd in ["update", "clone", "clone_ppl"]:
        ""+1
except:
    print("no valid cmd specified | valid cmds clone, clone_ppl, update")
    print("usage 4git.py clone git_repo_parent_url directory count (clones the whole repository of the holder)")
    print("usage 4git.py update directory count (updates all repositories which directories are childs of directory)")
    exit()

if cmd == "update":
    try:
        src_dirs=sys.argv[2]
    except:
        import os
        src_dirs=os.getcwd()
        del os
        print("no source dir specified | usage 4git.py update directory count \nFalling back to cwd..."+src_dirs)
    try:
        max_count=int(sys.argv[3])
    except:
        print("no max_count specified | usage 4git.py update directory count \nFalling back to max_count:"+str(max_count))
elif cmd in ["clone", "clone_ppl"]:
    try:
        url=sys.argv[2]
        rname=repo_name.findall(url)
        if rname == []:
            ""+1
        urllib_get(url)
    except:
        print("no valid url specified | usage 4git.while py clone git_repo_parent_url directory count")
    try:
        src_dirs=sys.argv[3]
    except:
        import os
        src_dirs=os.getcwd()
        del os
        print("no source destination specified | usage 4git.py clone git_repo_parent_url directory count \nFalling back to cwd..."+src_dirs)
    try:
        max_count=int(sys.argv[4])
    except:
        print("no max_count specified | usage 4git.py clone git_repo_parent_url directory count \nFalling back to max_count:"+str(max_count))
del sys

procs=[]
if cmd == "update":
    import os
    for sdir in os.walk(src_dirs):
        if(os.path.isdir(sdir[0]+"/.git")):
            sdir = sdir[0]
            cmd=["git", "pull"]
            import subprocess
            procs.append(subprocess.Popen(cmd, cwd=sdir))
            del subprocess
            i=procs_count(regx_update)
            while i > max_count:
                i=procs_count(regx_update)
                print("waiting for empty workspace...max_count:"+str(max_count))
                time.sleep(7)
    del os
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
        import subprocess
        procs.append(subprocess.Popen(cmd, cwd=src_dirs))
        del subprocess
    except:
        print("repo_parent name already exists continue with cloning...")
    parent_url=parent_url_regx.findall(url)
    if parent_url != []:
        parent_url=parent_url[0][0]+"://"+parent_url[0][1]
    else:
        print("something is wrong with your url..."+url)
        exit()
    dump_repos(url, src_dirs+"/"+rname)

elif cmd in ["clone_ppl"]:
    r=urllib_get(url)
    next_page=next_page_regx.findall(r)
    #print(next_page)
    followed=ppl_regx.findall(r)
    if followed != []:
        for f in followed:
            cmd=["python2.7", "4git.py", "clone", "https://github.com"+f, src_dirs, "4" ]
            print(cmd)
            #import subprocess
            #subprocess.Popen(cmd)
            #del subprocess
    if next_page != [] and next_page != next_page:
        next_page=next_page[0].replace("&amp;","&")
        clone_all(next_page, dr)

def clone_ppl(url, dr):
    global result
    print(result)
    print(url, dr)
    r=requests.get(sys.argv[1])
    next_page=next_page_regx.findall(r.text)
    #print(next_page)
    followed=ppl_regx.findall(r.text)
    if followed != []:
        for f in followed:
            cmd=["python2.7", "4git.py", "clone", "https://github.com"+f, dr, "4" ]
            print(cmd)
            subprocess.Popen(cmd)
    if next_page != [] and next_page != next_page:
        next_page=next_page[0].replace("&amp;","&")
        clone_all(next_page, dr)
