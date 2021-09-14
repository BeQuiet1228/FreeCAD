#ifndef MY_CHANGED_PARAM_NAME_DIALOG_H
#define MY_CHANGED_PARAM_NAME_DIALOG_H

#include <QDialog>
#include "ui_DlgChangeParamName.h"

QT_BEGIN_NAMESPACE
namespace Ui { class ChangeParamName; }
QT_END_NAMESPACE

class ChangeParamNameDialog : public QDialog
{
    Q_OBJECT

public:
    ChangeParamNameDialog(std::vector<std::pair<std::string, std::string>> param_list,
        QWidget* parent = nullptr);
    ~ChangeParamNameDialog();


private Q_SLOTS:
    void slotOK();
    void slotCancel();
    void slotSpinBox(int i);

public:
    int change_row; //修改变量名的行数
    std::vector<std::pair<std::string, std::string>> _param_list;
    std::string new_name;
    int sb_row_lastNum = 1;//记录sb_row的上一个值，当用户出入0 时 将slotSpinBox函数的参数改为sb_row_lastNum
    void changeSb_row(int);

private:
    Ui::ChangeParamName* ui;
};
#endif
