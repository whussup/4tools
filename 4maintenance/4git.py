#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################
#
# 4git - for collecting, updating and investigating repos @github
#
# VERSION 0.0.7
#
# Idea / Written by Sebastian Vivian Gresser - All Rights Reserved
#
# Copyright (C) by Sebastian Vivian Gresser - All Rights Reserved
#
########################################################################
#
# Should work for any webinterface based github clone.
# You maybe need to make minor changes to the regx and url_adds for github clones.
# As far as I know it is working for the parrot linux github clone.

# number of parallel processes
# change this settings for not using github

max_count=2

repos_url_add="?tab=repositories"
follow_url_add={"following":"?tab=following", "followers":"?tab=followers"}

import re
repositories=re.compile("<h3.*?>.*?<a.*?href=\"(.*?)\".*?>.*?</a>.*?</h3>", re.S)
parent_url_regx=re.compile("(.*?)://(.*?)/")
repo_name=re.compile("^.*?//.*?/(.*?)$")
search_regx=re.compile(".*?search\?q\=(.*?)$")
regx_update=re.compile("git pull")
regx_clone=re.compile("git clone")
ppl_regx=re.compile("<a.*?data-hovercard-type=\"user\".*?href=\"(.*?)\">")

#github does not really want to be scraped so following next pages is disabled
#next_page_regx=regx=re.compile("</button><a.*?href=\"(.*?)\">Next</a>")
next_page_regx=False

del re

def urllib_get(url):
    if version == "2":
        import urllib
        r=urllib.urlopen(url).read()
        del urllib
        return r
    elif version == "3":
        import urllib3
        http=urllib3.PoolManager()
        req=http.request("get", url)
        del urllib3
        return str(req)

def procs_count(regx):
    cmd=["ps", "ax"]
    import subprocess
    procs=str(subprocess.check_output(cmd))
    del subprocess
    return int(len(regx.findall(procs)))

def dump_repos(url, dr):
    r=urllib_get(url)
    if next_page_regx:
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
    if next_page_regx and next_page != []:
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
    print("usage 4git.py clone_ppl git_repo_parent_url directory count (clones all repositories of the holder's social connections)")
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

script_origin=sys.argv[0]
version=sys.version[0]
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
    rname=repo_name.findall(url)
    rname=rname[0].replace("+", "_")
    cmd = ["mkdir", rname]
    import subprocess
    subprocess.Popen(cmd, cwd=src_dirs)
    del subprocess
    for fua in follow_url_add:
        cmd = ["mkdir", rname+"/"+fua]
        import subprocess
        subprocess.Popen(cmd, cwd=src_dirs)
        del subprocess
        r=urllib_get(url+follow_url_add[fua])
        if next_page_regx:
            next_page=next_page_regx.findall(r)
        follow=ppl_regx.findall(r)
        if follow != []:
            ppl_done=[]
            for f in xrange(len(follow)):
                if f % 2 == 0:
                    continue
                else:
                    cmd=["python", script_origin, "clone", "https://github.com"+follow[f], src_dirs+"/"+rname+"/"+fua, str(max_count)]
                    print(cmd)
                    import subprocess
                    subprocess.Popen(cmd)
                    del subprocess
        if next_page_regx and next_page != [] and next_page != next_page:
            next_page=next_page[0].replace("&amp;","&")
            clone_all(next_page, dr)
