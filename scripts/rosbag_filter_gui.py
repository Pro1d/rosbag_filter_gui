#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import ntpath
from SimplePyQtGUIKit import SimplePyQtGUIKit
from PyQt4 import QtGui
import rosbag
import subprocess

def GetTopicList(path):
    bag = rosbag.Bag(path)
    topics = bag.get_type_and_topic_info()[1].keys()
    tStart = bag.get_start_time()
    tEnd = bag.get_end_time()
    types=[]
    for i in range(0,len(bag.get_type_and_topic_info()[1].values())):
        types.append(bag.get_type_and_topic_info()[1].values()[i][0])

    results=[]    
    for to,ty in zip(topics,types):
        results.append(to)

    #  print "GetTopicList result:"
    #  print results
    return (results, (tStart, tEnd))

def main():
    app = QtGui.QApplication(sys.argv)

    #GetFilePath
    files=SimplePyQtGUIKit.GetFilePath(isApp=True,caption="Select bag file",filefilter="*bag")
    #  print files
    if len(files)<1:
        print("Please select a bag file")
        sys.exit()

    topics, time=GetTopicList(files[0])
    res = SimplePyQtGUIKit.GetCheckButtonSelect(topics, time, app=app,fname=ntpath.basename(files[0]))
    if len(res) != 2:
        print "Canceled!"
        exit(0)
    selected, time = res

    # Construct commandline
    cmd = "rosbag filter "+files[0]+" "+files[0][:-4]+'_filtered.bag '
    cmd += '"'
    cmd += "topic in [" + ", ".join(["'"+k+"'" for k,v in selected.items() if v]) + "]"
    cmd += " and "
    cmd += str(time[0])+"<=(t.secs+t.nsecs/1e9)<="+str(time[1])
    cmd += '"'
    
    print "Run command:"
    print cmd

    print("Converting....")
    p = subprocess.Popen(cmd, shell=True)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()

    QtGui.QMessageBox.information(QtGui.QWidget(), "Message", "Finish Convert!!")

if __name__ == '__main__':
    print "rosbag_filter_gui start!!"
    main()
