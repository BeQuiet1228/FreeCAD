#-*- coding:utf-8 -*-
from  PySide.QtGui  import *
from  PySide.QtCore  import *
import math
import sys
import re
import os
import json,time
import shutil
import FreeCAD
reload(sys)
sys.setdefaultencoding("utf-8")

class AutoCompleteEdit(QLineEdit):
    def __init__(self,dialog1,model=[], separator=['+', '-', '*', '/'], addSpaceAfterCompleting=True):
        super(AutoCompleteEdit, self).__init__()
        self._separator = separator
        self._addSpaceAfterCompleting = addSpaceAfterCompleting
        self._completer = QCompleter(model,dialog1)
        self._completer.setWidget(self)
        # FreeCAD.Console.PrintMessage(self._completer.widget())
        self.connect(
            self._completer,
            SIGNAL('activated(QString)'),
            self._insertCompletion)
        self._keysToIgnore = [Qt.Key_Enter,
                              Qt.Key_Return,
                              Qt.Key_Escape,
                              Qt.Key_Tab]
        # FreeCAD.Console.PrintMessage(model)
        
    def setcompleterlist(self,list1):
        var_list=QStringListModel()
        var_list.setStringList(list1)
        self._completer.setModel(var_list)

    def _insertCompletion(self, completion):

        extra = len(completion) - len(self._completer.completionPrefix())
        if extra == 0:
            extra_text
        else:
            extra_text = completion[-extra:]
        # FreeCAD.Console.PrintMessage(str(extra_text)+'  '+str(extra)+'\n')
        if self._addSpaceAfterCompleting:
            extra_text += ''
        text_after = ''
        text_temp = self.text()
        i = self.cursorPosition()
        # FreeCAD.Console.PrintMessage(str(i)+'\n')
        x = self.cursorPosition() - 1
        text_after = text_temp[0:i] + extra_text + text_temp[i:]
        # FreeCAD.Console.PrintMessage(str(text_after)+'test!!!\n')
        self.setText(text_after)
        self.setCursorPosition(i+len(extra_text))

    def textUnderCursor(self):
        text = self.text()
        textUnderCursor = ''
        i = self.cursorPosition() - 1
        while i >= 0 and not text[i] in self._separator:
            textUnderCursor = text[i] + textUnderCursor
            i -= 1
        return textUnderCursor
    
    def keyPressEvent(self, event):
        # if self._completer.popup().isVisible():
        if True:
            if event.key() in self._keysToIgnore:
                event.ignore()
                return
        super(AutoCompleteEdit, self).keyPressEvent(event)
        completionPrefix = self.textUnderCursor()

        if completionPrefix != self._completer.completionPrefix():
            self._updateCompleterPopupItems(completionPrefix)
        if len(event.text()) > 0 and len(completionPrefix) > 0:
            self._completer.complete()
            #该行的作用为弹出提示框
        if len(completionPrefix) == 0:
            self._completer.popup().hide()

    def _updateCompleterPopupItems(self, completionPrefix):

        self._completer.setCompletionPrefix(completionPrefix)
        # 设置索引项
        self._completer.popup().setCurrentIndex(
            self._completer.completionModel().index(0, 0))