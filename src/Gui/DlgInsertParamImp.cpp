#include "PreCompiled.h"

#include "DlgInsertParamImp.h"


InsertParamDialog::InsertParamDialog(QWidget *parent)
    : QDialog(parent)
    , ui(new Ui::Dialog)
{
    ui->setupUi(this);
    this->name = QString();
    this->row = -999;
    QObject::connect(this->ui->ok_btn, SIGNAL(clicked(bool)), this, SLOT(insertParam()));
    QObject::connect(this->ui->ok_btn, SIGNAL(clicked(bool)), this, SLOT(close()));
}

InsertParamDialog::~InsertParamDialog()
{
    delete ui;
}

void InsertParamDialog::insertParam() {
    this->name = this->ui->param_le->text().simplified();
    this->row = this->ui->row_sb->value();
    this->close();
}

QString InsertParamDialog::getName() {
    return this->name;
}
int InsertParamDialog::getRow() {
    return this->row;
}

