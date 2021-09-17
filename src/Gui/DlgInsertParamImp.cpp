#include "PreCompiled.h"

#include "DlgInsertParamImp.h"


InsertParamDialog::InsertParamDialog(QWidget *parent)
    : QDialog(parent)
    , ui(new Ui::Dialog)
{
    ui->setupUi(this);
    this->ui->row_sb->setValue(1);
    this->name = QString();
    this->row = -999;
    QObject::connect(this->ui->ok_btn, SIGNAL(clicked(bool)), this, SLOT(insertParam()));
    QObject::connect(this->ui->cancel_btn, SIGNAL(clicked(bool)), this, SLOT(close()));
    QObject::connect(this->ui->row_sb, SIGNAL(clicked(bool)), this, SLOT(slotSpinBox(int)));
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

void InsertParamDialog::slotSpinBox(int i) {
    if (i > 0) {
        this->row_sb_lastNum = i;
        this->ui->row_sb->setValue(i);
    }
    else {
        i = this->row_sb_lastNum;
        this->ui->row_sb->setValue(i);
    }
}

