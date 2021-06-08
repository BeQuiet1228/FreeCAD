#ifndef CASEWORDLISTWIDGET_H
#define CASEWORDLISTWIDGET_H
#include <QListWidget>
#include "codeEdit/codeeditor.h"

class CaseWordListWidget:public QListWidget
{
    friend class CodeEditor;
public:
    CaseWordListWidget(QWidget *parent = 0);
protected:
   void keyPressEvent(QKeyEvent *event);
};

#endif // CASEWORDLISTWIDGET_H
