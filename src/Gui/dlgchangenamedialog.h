#ifndef DLGCHANGENAMEDIALOG_H
#define DLGCHANGENAMEDIALOG_H

#include <QDialog>

QT_BEGIN_NAMESPACE
namespace Ui { class DlgChangeNameDialog; }
QT_END_NAMESPACE

class DlgChangeNameDialog : public QDialog
{
    Q_OBJECT

public:
    DlgChangeNameDialog(QWidget* parent = nullptr);
    ~DlgChangeNameDialog();

    QString getAfterName();
    QString getLastName();
    QPushButton* returnAllreplaceBtn();
    QPushButton* returnReplaceBtn();
    QPushButton* returnLastBtn();
    QPushButton* returnNextBtn();
    QPushButton* returnCloseBtn();

private Q_SLOTS:
    void slotCancel();
    //为widget添加4种功能
    void slotAllreplace();
    void slotReplace();
    void slotLast();
    void slotNext();
    

private:
    QString l_name;
    QString n_name;

private:
    Ui::DlgChangeNameDialog* ui;
};
#endif // DLGCHANGENAMEDIALOG_H
