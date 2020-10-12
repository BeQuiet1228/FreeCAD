
#include <QWidget>
#include <qdebug.h>
#include <qglobal.h>
#include "codeeditor.h"
#include "casewordlistwidget.h"
#include <qpainter.h>
#include <QTextBlock>
#include "myhightlighter.h"

//![constructor]

CodeEditor::CodeEditor(QWidget *parent) : QPlainTextEdit(parent)
{
    lineNumberArea = new LineNumberArea1(this);
    matchWordThrad = new MatchWordsThread;

    connect(this, SIGNAL(blockCountChanged(int)), this, SLOT(updateLineNumberAreaWidth(int)));
    connect(this, SIGNAL(updateRequest(QRect,int)), this, SLOT(updateLineNumberArea(QRect,int)));
    connect(this, SIGNAL(cursorPositionChanged()), this, SLOT(highlightCurrentLine()));
    connect(this->document(),SIGNAL(contentsChange(int,int,int)),SLOT(inserChanged(int,int,int)));
    connect(matchWordThrad,SIGNAL(matchCaseWordFinished(QList<QString>,QList<QString>,int)),this,SLOT(matchFinished(QList<QString>,QList<QString>,int)));
    connect(matchWordThrad,SIGNAL(hideListWidget()),this,SLOT(hideLisetWidget()));

    updateLineNumberAreaWidth(0);
    highlightCurrentLine();

    listWidget = new CaseWordListWidget(this);      //关键字提示窗口
    listWidget->hide();

    myHightLighter *highLighter = new myHightLighter(this->document());         //设置高亮器
}

CodeEditor::~CodeEditor()
{
    matchWordThrad->terminate(); //终止线程
    matchWordThrad->wait();     //等待线程终止
    delete matchWordThrad;

}
//![constructor]

//![extraAreaWidth]

int CodeEditor::lineNumberAreaWidth()
{
    int digits = 1;
    int max = qMax(1, blockCount());
    while (max >= 10) {
        max /= 10;
        ++digits;
    }

    int space = 20 + fontMetrics().width(QLatin1Char('9')) * digits;

    return space;
}

//![extraAreaWidth]

//![slotUpdateExtraAreaWidth]

void CodeEditor::updateLineNumberAreaWidth(int /* newBlockCount */)
{
    setViewportMargins(lineNumberAreaWidth(), 0, 0, 0);
}

//![slotUpdateExtraAreaWidth]

//![slotUpdateRequest]

void CodeEditor::updateLineNumberArea(const QRect &rect, int dy)
{
    if (dy)
        lineNumberArea->scroll(0, dy);
    else
        lineNumberArea->update(0, rect.y(), lineNumberArea->width(), rect.height());

    if (rect.contains(viewport()->rect()))
        updateLineNumberAreaWidth(0);
}

//![slotUpdateRequest]

//![resizeEvent]

void CodeEditor::resizeEvent(QResizeEvent *e)
{
    QPlainTextEdit::resizeEvent(e);

    QRect cr = contentsRect();
    lineNumberArea->setGeometry(QRect(cr.left(), cr.top(), lineNumberAreaWidth(), cr.height()));
}

//![resizeEvent]

//![cursorPositionChanged]

void CodeEditor::highlightCurrentLine()
{
    QList<QTextEdit::ExtraSelection> extraSelections;

    if (!isReadOnly()) {
        QTextEdit::ExtraSelection selection;

        QColor lineColor = QColor(Qt::yellow).lighter(160);

        selection.format.setBackground(lineColor);
        selection.format.setProperty(QTextFormat::FullWidthSelection, true);
        selection.cursor = textCursor();
        selection.cursor.clearSelection();
        extraSelections.append(selection);
    }

    setExtraSelections(extraSelections);
}

//![cursorPositionChanged]

//![extraAreaPaintEvent_0]

void CodeEditor::lineNumberAreaPaintEvent(QPaintEvent *event)
{
    QPainter painter(lineNumberArea);
    painter.fillRect(event->rect(), Qt::lightGray);

//![extraAreaPaintEvent_0]

//![extraAreaPaintEvent_1]
    QTextBlock block = firstVisibleBlock();
    int blockNumber = block.blockNumber();
    int top = (int) blockBoundingGeometry(block).translated(contentOffset()).top();
    int bottom = top + (int) blockBoundingRect(block).height();
//![extraAreaPaintEvent_1]

//![extraAreaPaintEvent_2]
    while (block.isValid() && top <= event->rect().bottom()) {
        if (block.isVisible() && bottom >= event->rect().top()) {
            QString number = QString::number(blockNumber + 1);
            QPen pen(Qt::black);
            pen.setWidth(2);
            painter.setPen(pen);
            painter.drawText(0, top, lineNumberArea->width(), fontMetrics().height(),
                             Qt::AlignCenter, number);
        }
        QTextCursor cursor = this->textCursor();

        block = block.next();
        top = bottom;
        bottom = top + (int) blockBoundingRect(block).height();
        ++blockNumber;
    }



}
/*
*文本改变事件
* @position 插入位置
* @charsRemoved 删除字符的个数
* @charsAdded 增加字符的个数
* 在这个事件里取词，根据光标的位置，取当前输入的单词
*/
void  CodeEditor::inserChanged(int position, int charsRemoved, int charsAdded)
{
    QTextCursor cursor = this->textCursor();        //获取当前文本光标
    QString blockText = cursor.block().text();      //获取光标所在文本块的文本
    blockText = blockText.left(cursor.positionInBlock());   //获取光标之前的文本

    matchWordThrad->setMatchWord(blockText);

}
/*
*关键字匹配完成槽
* 将关键字放入listwidget中
* 如果没有匹配的关键字，则隐藏listwidget
* @vipCaseWords 完全匹配的关键字
* @lowCaseWords 模糊匹配的关键字
* @caseWordSize 用户键入关键字的长度
*/
void CodeEditor::matchFinished(QList<QString> vipCaseWords, QList<QString> lowCaseWords,int caseWordSize)
{
    if(vipCaseWords.size() == 0 && lowCaseWords.size() == 0)
    {
        listWidget->hide();
        return;
    }
    this->caseWordCurrentSize = caseWordSize;
    listWidget->clear();
    listWidget->addItems(vipCaseWords);
    listWidget->addItems(lowCaseWords);
    listWidget->setCurrentRow(0);
    //设置listwidget的位置
    QTextBlock block = firstVisibleBlock();
    QTextCursor cursor = this->textCursor();
    QTextBlock cursorBlock = cursor.block();
    int y = 3;
    while(block != cursorBlock)     //获取文本块在当前显示区域是第几行
    {
        y = y + blockBoundingRect(block).height();
        block = block.next();
    }
    y = y + blockBoundingRect(cursorBlock).height();
  //  int x = 3 + cursor.positionInBlock() *fontMetrics().width('a');
    int x = 3 + lineNumberAreaWidth();
    QString text = QString(cursorBlock.text()).left(cursor.positionInBlock());
    for(int i = 0; i < text.size();i++)         //获取光标前所有字符相加的宽度，用于关键字提示框的位置
    {
        x = x + fontMetrics().width(text.at(i));
    }
    listWidget->move(x,y);
    listWidget->show();
}
/*
*键盘按下事件
*/
void CodeEditor::keyPressEvent(QKeyEvent *event)
{
    if(!listWidget->isHidden())
    {
        if(event->key() == Qt::Key_Up               //传入上下按键
                ||event->key() == Qt::Key_Down)
        {
            listWidget->keyPressEvent(event);
            return;
        }
        if(event->text() == "\r")               //如果是回车符，则键入关键字
        {
            QString caseWord = listWidget->currentItem()->text();           //获取当前关键字
            QTextCursor cursor = this->textCursor();            //获取光标信息

            cursor.movePosition(QTextCursor::Left,QTextCursor::KeepAnchor,caseWordCurrentSize);

            cursor.insertText(caseWord);    //插入关键字
            this->setTextCursor(cursor);    //设置光标信息
            return;
        }

    }
    //按下tab按键不键入tab符，而是键入连续的空格，可以解决无法获取tab符实际长度的问题
    if(event->key() == Qt::Key_Tab)
    {
        QTextCursor cursor = this->textCursor();
        cursor.insertText("     ");
        this->setTextCursor(cursor);
        return;
    }

    QPlainTextEdit::keyPressEvent(event);
}
//隐藏关键词提示的listwiget
void CodeEditor::hideLisetWidget()
{
    listWidget->hide();
}

#include "codeEdit/moc_codeeditor.cpp"