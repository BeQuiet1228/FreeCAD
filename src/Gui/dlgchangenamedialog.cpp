#include "dlgchangenamedialog.h"
#include "ui_dlgchangenamedialog.h"
#include <QDebug>

DlgChangeNameDialog::DlgChangeNameDialog(std::string& cur_name, QWidget* parent)
    : QDialog(parent)
    , ui(new Ui::DlgChangeNameDialog)
{
    ui->setupUi(this);
    ui->pre_name->setEnabled(false);
    ui->pre_name->setText(QString::fromStdString(cur_name));
    QObject::connect(this->ui->pb_ok, SIGNAL(clicked(bool)), this, SLOT(slotok()));
    QObject::connect(this->ui->pb_cancel, SIGNAL(clicked(bool)), this, SLOT(slotCancel()));
}

DlgChangeNameDialog::~DlgChangeNameDialog()
{
    delete ui;
}

void DlgChangeNameDialog::slotok()
{
    this->n_name = ui->after_name->text();
    this->close();
}

void DlgChangeNameDialog::slotCancel()
{
    this->close();
}

QString DlgChangeNameDialog::getName()
{
    return this->n_name;
}

