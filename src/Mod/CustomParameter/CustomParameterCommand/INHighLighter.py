
#-*- coding: utf-8 -*-
from PySide import QtCore, QtGui
import FreeCAD
from File.FileCommand.M3DFile.CHIPICCommand import keywordInCommand
class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        # 1.设置关键字

        # 设置字体样式
        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkBlue)

        # 获得关键字
        keywordPatterns = []
        # keywordInCommand=[]
        for key in keywordInCommand:
            key = "\\b" + key + "\\b"
            keywordPatterns.append(key)

        # 添加到规则中
        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)for pattern in keywordPatterns]

        # 2.设置注释

        # 设置字体样式
        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.darkGreen)
        # self.highlightingRules.append((QtCore.QRegExp("i[^;]*;"), singleLineCommentFormat))
        # FreeCAD.Console.PrintMessage(self.highlightingRules)
        # 添加到规则中
        self.highlightingRules.append((QtCore.QRegExp("![^\n]*"), singleLineCommentFormat))

        keywordFormatInt = QtGui.QTextCharFormat()
        keywordFormatInt.setForeground(QtCore.Qt.darkRed)  
        keywordFormatInt.setFontItalic(True) 
        self.highlightingRules.append((QtCore.QRegExp("\\b[i-n|I-N][^;]*[=][^;]*;"), keywordFormatInt))
        # (i|j|l|m|n|I|J|K|L|M|N)
        # keywordFormatOther = QtGui.QTextCharFormat()
        # keywordFormatOther.setForeground(QtCore.Qt.darkRed)
        # self.highlightingRules.append((QtCore.QRegExp("(.+?);"), keywordFormatOther))


    def highlightBlock(self, text):
        # FreeCAD.Console.PrintError("INBLOCK\n")
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            # FreeCAD.Console.PrintMessage(expression)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

# class Highlighter(QtGui.QSyntaxHighlighter):
#     def __init__(self, parent=None):
#         super(Highlighter, self).__init__(parent)
#         self.highlightingRules=[]
#         # 1.设置关键字

#         # 设置字体样式
#         keywordFormatInt = QtGui.QTextCharFormat()
#         keywordFormatInt.setForeground(QtCore.Qt.darkBlue)

#         #
#         keywordFormatOther = QtGui.QTextCharFormat()
#         keywordFormatOther.setForeground(QtCore.Qt.darkRed)
#         # 获得关键字
#         keywordPatterns = []
#         # keywordInCommand=[]
#         for key in keywordInCommand:
#             key = "\\b" + key + "\\b"
#             keywordPatterns.append(key)

#         # 添加到规则中
#         self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormatInt)for pattern in keywordPatterns]

#         # 2.设置注释

#         # 设置字体样式
#         singleLineCommentFormat = QtGui.QTextCharFormat()
#         singleLineCommentFormat.setForeground(QtCore.Qt.darkGreen)

#         # 添加到规则中
#         self.highlightingRules.append((QtCore.QRegExp("![^\n]*"), singleLineCommentFormat))

#         # self.highlightingRules.append((QtCore.QRegExp("(i|j|l|m|n|I|J|K|L|M|N)(.+?);"), keywordFormatInt))

#         # self.highlightingRules.append((QtCore.QRegExp("(.+?);"), keywordFormatOther))
