#ifndef FOURIERDIALOG_H
#define FOURIERDIALOG_H

#include <QDialog>

QT_BEGIN_NAMESPACE
namespace Ui { class FourierDialog; }
QT_END_NAMESPACE

class FourierDialog : public QDialog
{
    Q_OBJECT

public:
    FourierDialog(QWidget* parent = nullptr);
    ~FourierDialog();

private Q_SLOTS:
    void slotOk();

private:
    Ui::FourierDialog* ui;
};
#endif 
