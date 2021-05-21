#ifndef MY_DELETE_DIALOG_H
#define MY_DELETE_DIALOG_H

#include <QDialog>
#include "ui_DlgDeleteParam.h"

QT_BEGIN_NAMESPACE
namespace Ui { class DeleteDialog; }
QT_END_NAMESPACE

class DeleteParamDialog : public QDialog
{
    Q_OBJECT

public:
    DeleteParamDialog(QWidget* parent = nullptr);
    ~DeleteParamDialog();
    // 在获取变量名之前必须先调用isDeleted,查看所删除的变量是否有效
    std::string getParamName();
    bool isDeleted();
    void inputAllParamName(const std::vector<std::string> &allParamName);

private Q_SLOTS:
    void slotAnalyze();
    void slotOK();
    void slotCancel();
    void slotTextChanged();

public:
    std::string paramName;
    bool isValid;
    std::vector<std::string>& _allParamName = std::vector<std::string>();

private:
    Ui::DeleteDialog* ui;
};
#endif
