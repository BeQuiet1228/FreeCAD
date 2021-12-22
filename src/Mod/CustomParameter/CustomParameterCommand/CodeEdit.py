#-*- coding: utf-8 -*-
import sys
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
from PySide.QtGui import *
from PySide.QtCore import *

import numpy as np
# 这个是从QT官网的例子翻译过来的，具体去QT官网查看
# 详情见： https://doc.qt.io/archives/qt-4.8/qt-widgets-codeeditor-example.html


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self.editor = editor


    def sizeHint(self):
        return Qsize(self.editor.lineNumberAreaWidth(), 0)


    def paintEvent(self, event):
        # print('LineNumberArea.paintEvent')
        self.editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(None)
        self.lineNumberArea = LineNumberArea(self)

        self.connect(self, SIGNAL('blockCountChanged(int)'), self.updateLineNumberAreaWidth)
        self.connect(self, SIGNAL('updateRequest(QRect,int)'), self.updateLineNumberArea)
        self.connect(self, SIGNAL('cursorPositionChanged()'), self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)


    def lineNumberAreaWidth(self):
        """ This method has been slightly modified (use of log and uses actual
        font rather than standart.) """
        n_lines = self.blockCount()
        digits = np.ceil(np.log10(n_lines)) + 1
        return digits * QFontMetrics(self.font()).width('9') + 3


    def updateLineNumberAreaWidth(self, _):
        # print('CodeEditor.updateLineNumberAreaWidth: margin = {}'.format(self.lineNumberAreaWidth()))
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)


    def updateLineNumberArea(self, rect, dy):
        # print('CodeEditor.updateLineNumberArea: rect = {}, dy = {}'.format(rect, dy))

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)


    def resizeEvent(self, event):
        super(CodeEditor, self).resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                        self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        # painter(self.lineNumberArea)
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = QFontMetrics(self.font()).height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height,
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.yellow).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
