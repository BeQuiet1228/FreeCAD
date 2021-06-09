#include "PreCompiled.h"
#include "DlgChangeParamNameImp.h"


ChangeParamNameDialog::ChangeParamNameDialog(std::vector<std::pair<std::string, std::string>> param_list,
    QWidget* parent)
    : QDialog(parent)
    , ui(new Ui::ChangeParamName)
{
    ui->setupUi(this);
    if (param_list.empty()) {
        this->close();
        return;
    }
    this->_param_list = param_list;
    // 初始化对话框
    this->ui->sb_row->setValue(0);
    this->ui->le_before_name->setEnabled(false);
    this->ui->le_before_name->setText(QString::fromStdString(param_list[0].first));
    this->ui->sb_row->setMaximum(param_list.size()-1);
    // 链接信号与槽
    QObject::connect(this->ui->pb_ok, SIGNAL(clicked(bool)), this, SLOT(slotOK()));
    QObject::connect(this->ui->pb_cancel, SIGNAL(clicked(bool)), this, SLOT(slotCancel()));
    QObject::connect(this->ui->sb_row, SIGNAL(valueChanged(int)), this, SLOT(slotSpinBox(int)));
}

ChangeParamNameDialog::~ChangeParamNameDialog() {

}

void ChangeParamNameDialog::slotOK() {
    this->new_name = this->ui->le_later_name->text().toStdString();
    this->change_row = this->ui->sb_row->value();
    this->close();
}

void ChangeParamNameDialog::slotCancel() {
    this->close();
}

void ChangeParamNameDialog::slotSpinBox(int i) {
    this->ui->le_before_name->setText(QString::fromStdString(this->_param_list[i].first));
}