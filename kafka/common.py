#!/usr/bin/env python
# encoding: utf-8
import time
def log(str):
    t = time.strftime(r"%Y-%m-%d_%H-%M-%S",time.localtime())
    print("[%s]%s"%(t,str))