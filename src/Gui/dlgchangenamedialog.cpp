#include "dlgchangenamedialog.h"
#include "ui_dlgchangenamedialog.h"
#include <QDebug>

DlgChangeNameDialog::DlgChangeNameDialog(QWidget* parent)
    : QDialog(parent)
    , ui(new Ui::DlgChangeNameDialog)
{
    ui->setupUi(this);
    QObject::connect(this->ui->pb_allReplace, SIGNAL(clicked(bool)), this, SLOT(slotAllreplace()));
    QObject::connect(this->ui->pb_replace, SIGNAL(clicked(bool)), this, SLOT(slotReplace()));
    QObject::connect(this->ui->pb_last, SIGNAL(clicked(bool)), this, SLOT(slotLast()));
    QObject::connect(this->ui->pb_next, SIGNAL(clicked(bool)), this, SLOT(slotNext()));
    QObject::connect(this->ui->pb_cancel, SIGNAL(clicked(bool)), this, SLOT(slotCancel()));
}

DlgChangeNameDialog::~DlgChangeNameDialog()
{
    delete ui;
}

void DlgChangeNameDialog::slotAllreplace()
{
    this->l_name = ui->pre_name->text();
    this->n_name = ui->after_name->text();
}

void DlgChangeNameDialog::slotReplace()
{
    this->l_name = ui->pre_name->text();
    this->n_name = ui->after_name->text();
}

void DlgChangeNameDialog::slotLast()
{
    this->l_name = ui->pre_name->text();
    this->n_name = ui->after_name->text();
}

void DlgChangeNameDialog::slotNext()
{
    this->l_name = ui->pre_name->text();
    this->n_name = ui->after_name->text();
}

void DlgChangeNameDialog::slotCancel()
{
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

QPushButton* DlgChangeNameDialog::returnAllreplaceBtn() {
    return this->ui->pb_allReplace;
}

QPushButton* DlgChangeNameDialog::returnReplaceBtn() {
    return this->ui->pb_replace;
}

QPushButton* DlgChangeNameDialog::returnLastBtn() {
    return this->ui->pb_last;
}

QPushButton* DlgChangeNameDialog::returnNextBtn() {
    return this->ui->pb_next;
}

QPushButton* DlgChangeNameDialog::returnCloseBtn() {
    return this->ui->pb_cancel;
}

