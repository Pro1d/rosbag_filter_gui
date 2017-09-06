#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt4.QtGui  import *
import sys

_SimplePyQTGUIKit_validated = False

class SimplePyQtGUIKit:
    def QuitApp(self):
        QApplication.quit()

    @classmethod
    def GetFilePath(self,caption="Open File",filefilter="",isApp=False):
        u"""
            "Images (*.png *.xpm *.jpg);;Text files (*.txt);;XML files (*.xml)"
        """

        if not isApp:
          app = QApplication(sys.argv)
        files=QFileDialog.getOpenFileNames(caption=caption,filter=filefilter)

        strlist=[]
        for file in files:
            strlist.append(str(file))

        return strlist

    @classmethod
    def saveCacheTopicFilter(self, checked):
        try:
            f = open("filter_cache.txt", "w")
            f.write("\n".join([topic for topic in checked if checked[topic]]))
            f.close()
        except:
            pass

    @classmethod
    def loadCacheTopicFilter(self, selectList):
        checked = set()
        try:
            f = open("filter_cache.txt", "r")
            checked = set([t.replace("\n","") for t in f.readlines()])
            f.close()
        except:
            pass
        return checked

    @classmethod
    def GetCheckButtonSelect(self, selectList, time, title="Filter rosbag", fname="",app=None):
        """
        Get selected check button options

        title: Window name
        mag: Label of the check button
        return selected dictionary
            {'sample b': False, 'sample c': False, 'sample a': False}
        """
 
        if app is None:
          app = QApplication(sys.argv)
        win = QWidget()
        layout=QGridLayout()
        layoutRow=0

        # Topic title
        label = QLabel("Filter by topic name:")
        layout.addWidget(label,layoutRow,0)
        layoutRow=layoutRow+1

        # Topic uncheck/check all
        def setAllTopicState(checkboxs, state):
            for c in checkboxs:
                c.setChecked(state)
        btn=QPushButton("Select all")
        btn.clicked.connect(lambda: setAllTopicState(checkboxs, True))
        layout.addWidget(btn,layoutRow, 0)
        btn=QPushButton("Unselect all")
        btn.clicked.connect(lambda: setAllTopicState(checkboxs, False))
        layout.addWidget(btn,layoutRow, 1)
        layoutRow=layoutRow+1
        

        # Topic checkbox
        checked = SimplePyQtGUIKit.loadCacheTopicFilter(selectList)
        checkboxs=[]
        i=0
        for select in selectList:
            checkbox=QCheckBox(select)
            checkbox.setChecked(select in checked)
            layout.addWidget(checkbox,layoutRow,0, 1, 2)
            layoutRow=layoutRow+1
            checkboxs.append(checkbox)
            i+=1

        # Text time start
        title_start = QLabel("Start time:")
        layout.addWidget(title_start, layoutRow, 0)

        textedit_start = QLineEdit(str(time[0]))
        layout.addWidget(textedit_start, layoutRow, 1)
        layoutRow+=1

        # Text time end
        title_end = QLabel("End time:")
        layout.addWidget(title_end, layoutRow, 0)

        textedit_end = QLineEdit(str(time[1]))
        layout.addWidget(textedit_end, layoutRow, 1)
        layoutRow+=1
        
        # Button OK
        global _SimplePyQTGUIKit_validated
        _SimplePyQTGUIKit_validated = False
        def validate():
            global _SimplePyQTGUIKit_validated
            _SimplePyQTGUIKit_validated = True
            app.quit()
        btn=QPushButton("OK")
        btn.clicked.connect(validate)
        layout.addWidget(btn,layoutRow,0, 1, 2)
        layoutRow=layoutRow+1

        win.setLayout(layout)
        win.setWindowTitle(title+" "+fname)
        win.show()
        app.exec_()

        if _SimplePyQTGUIKit_validated:
            result={}
            for (checkbox, select) in zip(checkboxs, selectList):
                result[select]=checkbox.isChecked()
            SimplePyQtGUIKit.saveCacheTopicFilter(result)
            tStart = eval(str(textedit_start.text()))
            tEnd = eval(str(textedit_end.text()))

            return (result, (tStart, tEnd))
        else:
            return tuple()

if __name__ == '__main__':
    #  print "GetCheckButtonSelect"
    #  optList=SimplePyQtGUIKit.GetCheckButtonSelect(["sample a","sample b","sample c"], title="Select sample", msg="Please select sample")
    #  print optList
    filePath=SimplePyQtGUIKit.GetFilePath(caption=u"Select files",filefilter="*py")
    print filePath


