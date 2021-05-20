
#ifndef CODEEDITOR_H
#define CODEEDITOR_H

#include <QPlainTextEdit>
#include <QObject>
#include <QListWidget>
#include <QThread>
#include <QMutex>
#include <QKeyEvent>
#include <SmartContorl/SmartContorlConfig.hpp>
class CaseWordListWidget;

QT_BEGIN_NAMESPACE
class QPaintEvent;
class QResizeEvent;
class QSize;
class QWidget;
QT_END_NAMESPACE

class LineNumberArea1;
class MatchWordsThread;
class FindDialog;

class SMARTCONTORL_EXPORT CodeEditor : public QPlainTextEdit
{
    Q_OBJECT

public:
    CodeEditor(QWidget *parent = 0);
    ~CodeEditor();

    void lineNumberAreaPaintEvent(QPaintEvent *event);
    int lineNumberAreaWidth();
    CaseWordListWidget *listWidget;

	void showFindDialog();
	void hideFindDialog();
	//调整查找框的位置
	void autoFindDialogPoint();
protected:
    void resizeEvent(QResizeEvent *event);
    void keyPressEvent(QKeyEvent *event);

private slots:
    void updateLineNumberAreaWidth(int newBlockCount);
    void highlightCurrentLine();
    void updateLineNumberArea(const QRect &, int);
    void inserChanged(int position, int charsRemoved, int charsAdded);
    void matchFinished(QList<QString> vipCaseWords,QList<QString> lowCaseWords,int caseWordSize);
    void hideLisetWidget();

private:
    int caseWordCurrentSize;
    MatchWordsThread *matchWordThrad;
    QWidget *lineNumberArea;

	FindDialog *findDialog;
};

class SMARTCONTORL_EXPORT LineNumberArea1 : public QWidget
{
public:
    LineNumberArea1(CodeEditor *editor) : QWidget(editor) {
        codeEditor = editor;
    }

    QSize sizeHint(){
        return QSize(codeEditor->lineNumberAreaWidth(), 0);
    }
protected:
    void paintEvent(QPaintEvent *event) {
        codeEditor->lineNumberAreaPaintEvent(event);
    }

private:
    CodeEditor *codeEditor;
};

#endif
