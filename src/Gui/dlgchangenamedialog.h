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
    DlgChangeNameDialog(std::string& cur_name, QWidget* parent = nullptr);
    ~DlgChangeNameDialog();

    QString getName();

private Q_SLOTS:
    void slotok();
    void slotCancel();

private:
    QString n_name;

private:
    Ui::DlgChangeNameDialog* ui;
};
#endif // DLGCHANGENAMEDIALOG_H
