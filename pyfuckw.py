#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Auto connect to ssh tunnel
"""

import pexpect
import commands
import time

__DEBUG__ = False 
existSSh = "ssh -qTfnN"

# fill the exact ssh information below
info = (host, username, password)

def d(msg):
    """ print msg when __DEBUG__ is True"""
    if __DEBUG__ : print msg

def getPid(process):
    """ print the first pid associated with the given process
        a empty list will return if process no found
    """
    pids = commands.getoutput(r"pgrep -f '%s'" % (process))
    pids = pids.split()
    if len(pids) > 1:
        return pids[ : len(pids) - 1]
    else:
        return []

def connSSH():
    """ connect to ssh """
    cmd = r"ssh -qTfnN -D 7070 %s@%s" % (info[1], info[0])
    d(cmd)
    ssh = pexpect.spawn(cmd)
    ssh.expect(".*password")
    print "password sending"
    time.sleep(0.1)
    ssh.sendline(info[2])
    time.sleep(3)
    # ssh.interact()
    ssh.expect(pexpect.EOF)
    print "ssh connect done"

def main():
    existPid = getPid(existSSh);
    for pid in existPid:
        print ("will kill a exist ssh which pid is " + pid)
        commands.getoutput("kill %s" % (pid))

    print "try to connect ssh..."
    connSSH()
    print "check..."
    existPid = getPid(existSSh);
    if len(existPid) > 0:
        print "ssh opened"
    else:
        print "ssh never open"


if __name__ == "__main__":
    main();
    # existPid = getPid("python");
    # print existPid
