#!/usr/bin/env python
# encoding: utf-8

import ConfigParser
import commands
import log as deployLog
import socket
import fcntl
import struct
import telnetlib
import os
import platform
from distutils.dir_util import copy_tree

log = deployLog.getLogger()
platformStr = platform.platform()

def getIpAddress(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def getLocalIp():
    return getIpAddress("eth0")
    
def net_if_used(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        result=s.connect_ex((ip, int(port)))
        if result==0:
            print "  error! port {} has been used. please check.".format(port)
            return True
        else:
            return False
    finally:
        s.close()

def isUbuntu():
    return platformStr.lower().find("ubuntu") > -1

def isCentos():
    return platformStr.lower().find("centos") > -1

def isSuse():
    return platformStr.lower().find("suse") > -1

def getBaseDir():
    cwd = os.getcwd()
    log.info("  os.getcwd() is {}".format(cwd))
    path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    return path

def getCurrentBaseDir():
    cwd = os.getcwd()
    log.info("  os.getcwd() is {}".format(cwd))
    path = os.path.abspath(os.path.join(os.getcwd(), "."))
    return path

def copytree(src, dst):
    copy_tree(src,dst)
    return

def doCmd(cmd):
    log.info(" execute cmd  start ,cmd : {}".format(cmd))
    result = dict()
    (status, output) = commands.getstatusoutput(cmd)
    result["status"] = status
    result["output"] = output
    log.info(" execute cmd  end ,cmd : {},status :{} , output: {}".format(cmd,status,output))
    if (0 != status):
        raise Exception("execute cmd  error ,cmd : {}, status is {} ,output is {}".format(cmd,status, output))
    return result

def doCmdIgnoreException(cmd):
    log.info(" execute cmd  start ,cmd : {}".format(cmd))
    result = dict()
    (status, output) = commands.getstatusoutput(cmd)
    result["status"] = status
    result["output"] = output
    log.info(" execute cmd  end ,cmd : {},status :{} , output: {}".format(cmd, status, output))
    return result

def getCommProperties(paramsKey):
    current_dir = getCurrentBaseDir()
    cf = ConfigParser.ConfigParser()
    propertiesDir =current_dir+"/common.properties"
    cf.read(propertiesDir)
    log.info(" commProperties is {} ".format(propertiesDir))
    cf.sections()
    value = cf.get('browser', paramsKey)
    return value

def replaceConf(fileName,oldStr,newStr):
    if not os.path.isfile(fileName):
        print "{} is not a file ".format(fileName)
        return
    oldData =""
    with open(fileName, "r") as f:
        for line in f:
            if oldStr in line:
                line = line.replace(oldStr, newStr)
            oldData += line
    with open(fileName, "w") as f:
        f.write(oldData)
    return

def replaceConfDir(filePath,oldStr,newStr):
    if not os.path.isdir(filePath):
        print "{} is not a dir ".format(filePath)
        return
    for root, dirs, files in os.walk(filePath):
        for file in files:
            replaceConf(os.path.join(root,file),oldStr,newStr)
    return
    
def do_telnet(host,port):
    try:
        tn = telnetlib.Telnet(host, port, timeout=5)
        tn.close()
    except:
        return False
    return True

if __name__ == '__main__':
    print(getIpAddress("eth0"))
    pass