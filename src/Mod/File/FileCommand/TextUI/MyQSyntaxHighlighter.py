#-*- coding: utf-8 -*-

from PySide import QtCore, QtGui
# 定义涉及到的关键字
keywordInCommand = ["FUNCTION",
                    "START", "STOP",
                    "SYSTEM", "POINT", "LINE", "AREA", "VOLUME",
                    "DURATION", "TIMER", "MARK", "AUTOGRID",
                    "SYMMETRY", "PORT", "FREESPACE",
                    "CONDUCTANCE", "DIELECTRIC", "CONDUCTOR", "VOID", "MATERIAL", "FOIL", "INDUCTOR", "DRIVER",
                    "EMISSION", "EMIT",
                    "MAXWELL", "MODE", "TIME_STEP",
                    "CONTINUITY",
                    "PRESET",
                    "GRAPHICS", "DUMP", "HEADER",
                    "OBSERVE",
                    "DISPLAY", "CONTOUR", "VECTOR", "PHASESPACE", "RANGE",
                    "KINEMATICS"]


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        # 1.设置关键字

        # 设置字体样式
        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(QtCore.Qt.darkBlue)

        # 获得关键字
        keywordPatterns = []
        for key in keywordInCommand:
            key = "\\b" + key + "\\b"
            keywordPatterns.append(key)

        # 添加到规则中
        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)for pattern in keywordPatterns]

        # 2.设置注释

        # 设置字体样式
        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.darkGreen)

        # 添加到规则中
        self.highlightingRules.append((QtCore.QRegExp("![^\n]*"), singleLineCommentFormat))

        # FreeCAD.Console.PrintMessage(self.highlightingRules)


    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
