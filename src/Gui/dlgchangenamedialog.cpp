#include "dlgchangenamedialog.h"
#include "ui_dlgchangenamedialog.h"
#include <QDebug>

DlgChangeNameDialog::DlgChangeNameDialog(QWidget* parent)
    : QDialog(parent)
    , ui(new Ui::DlgChangeNameDialog)
{
    ui->setupUi(this);
    //ui->pre_name->setEnabled(false);
    /*ui->pre_name->setText(QString::fromStdString(cur_name));
    ui->after_name->setText(QString::fromStdString(cur_name));*/
    QObject::connect(this->ui->pb_ok, SIGNAL(clicked(bool)), this, SLOT(slotok()));
    QObject::connect(this->ui->pb_cancel, SIGNAL(clicked(bool)), this, SLOT(slotCancel()));
}

DlgChangeNameDialog::~DlgChangeNameDialog()
{
    delete ui;
}

void DlgChangeNameDialog::slotok()
{
    this->l_name = ui->pre_name->text();
    this->n_name = ui->after_name->text();
    this->isChanged = 1;
    this->close();
}

void DlgChangeNameDialog::slotCancel()
{
    this->isChanged = 0;
    this->close();
}

QString DlgChangeNameDialog::getLastName()
{
    return this->l_name;
}

QString DlgChangeNameDialog::getAfterName()
{
    return this->n_name;
}

