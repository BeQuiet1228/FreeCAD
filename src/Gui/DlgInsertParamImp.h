#ifndef MY_DIALOG_H
#define MY_DIALOG_H

#include <QDialog>
#include "ui_DlgInsertParam.h"

//QT_BEGIN_NAMESPACE
namespace Ui { class Dialog; }
//QT_END_NAMESPACE

class InsertParamDialog : public QDialog
{
    Q_OBJECT

public:
    InsertParamDialog(QWidget *parent = nullptr);
    ~InsertParamDialog();
    QString getName();
    int getRow();
    void slotSpinBox(int);//避免spinbox大于或者小于1
    int row_sb_lastNum = 1;

private:
    QString name;
    int row;

public Q_SLOTS:
    void insertParam();

private:
    Ui::Dialog *ui;
};
#endif // MY_DIALOG_H
