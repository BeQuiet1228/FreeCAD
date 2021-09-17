#include "PreCompiled.h"

#include "DlgDeleteParamImp.h"
#include "AboutParameter.h"

DeleteParamDialog::DeleteParamDialog(std::vector<std::pair<std::string, std::string>> param_list, QWidget* parent)
    : QDialog(parent)
    , ui(new Ui::DeleteDialog)
{
    ui->setupUi(this);
    this->_param_list = param_list;
    this->ui->sb_row->setValue(1);//序列号文本框初始为1
    this->ui->le_name->setText(QString::fromStdString(this->_param_list[0].first));
    this->isValid = false;
    this->isNeedToDelete = false;
    this->paramName = std::string("");
    this->ui->pb_ok->setEnabled(false);
    QObject::connect(this->ui->pb_analyze, SIGNAL(clicked(bool)), this, SLOT(slotAnalyze()));
    QObject::connect(this->ui->pb_ok, SIGNAL(clicked(bool)), this, SLOT(slotOK()));
    QObject::connect(this->ui->pb_cancel, SIGNAL(clicked(bool)), this, SLOT(slotCancel()));
    QObject::connect(this->ui->le_name, SIGNAL(textChanged(const QString&)), this, SLOT(slotTextChanged()));
    QObject::connect(this->ui->sb_row, SIGNAL(valueChanged(int)), this, SLOT(slotSpinBox(int)));//为sb_row提供connect函数
}

DeleteParamDialog::~DeleteParamDialog() {

}

std::string DeleteParamDialog::getParamName() {
    return this->paramName;
}

bool DeleteParamDialog::isDeleted() {
    return this->isValid;
}

void DeleteParamDialog::slotAnalyze() {
    this->paramName = this->ui->le_name->text().toStdString();
    if (this->_allParamName.empty() || this->paramName.empty()) {
        this->isValid = false;
        this->ui->te_message->setText(QString::fromUtf8("The variable does not exist. Please reenter it."));
        return;
    }
    for (const auto& i : this->_allParamName) {
        if (i == this->paramName) {
            this->isValid = true;
            this->ui->pb_ok->setEnabled(true);
            std::vector<std::string> affected_param = findLinkWithParam(paramName, this->ordered_param, std::string());
            std::vector<std::string> affected_obj = findLinkWithObject(affected_param, std::string());
            std::string warning = "The variable is effective, But the following variables will be affected:\n";
            for (const auto& i : affected_param) {
                warning += i + "\n";
            }
            warning += "The following models may fail:\n";
            for (const auto& i : affected_obj) {
                warning += i + "\n";
            }
            this->ui->te_message->setText(QString::fromStdString(warning));
            return;
        }
    }
    this->isValid = false;
}

void DeleteParamDialog::slotOK() {
    this->isNeedToDelete = true;
    this->close();
}

void DeleteParamDialog::inputAllParamName(const std::vector<std::string>& allParamName) {
    this->_allParamName = allParamName;
}

void DeleteParamDialog::slotCancel() {
    this->close();
}

void DeleteParamDialog::slotTextChanged() {
    this->ui->pb_ok->setEnabled(false);
    this->ui->te_message->clear();
}

void DeleteParamDialog::inputAllOrderedParam(std::vector<std::pair<std::string, std::string>>& _ordered_param) {
    this->ordered_param = _ordered_param;
}

void DeleteParamDialog::slotSpinBox(int i) {
    if (i > 0) {
        this->sb_row_lastNum = i;
    }
    else {
        i = this->sb_row_lastNum;
        this->ui->sb_row->setValue(i);
    }
    this->ui->le_name->setText(QString::fromStdString(this->_param_list[i - 1].first));
}

void DeleteParamDialog::deleteSb_row(int i) {
    this->ui->sb_row->setValue(i);
    this->ui->le_name->setText(QString::fromStdString(this->_param_list[i - 1].first));
}