#include "FindDialog.h"
#include "ui_FindDialog.h"
#include <iostream>
#include <QMessageBox>
#include <QPalette>
FindDialog::FindDialog(QWidget* parent /*= 0*/)
	:QDialog(parent), ui(new Ui::FindDialog()), textEdit(nullptr)
{
	ui->setupUi(this);
}

FindDialog::~FindDialog()
{
	delete ui;
}

void FindDialog::on_pushButtonNext_clicked()
{
	QTextDocument::FindFlags flag = 0;

	flag = ui->checkBox_1->isChecked() ? flag | QTextDocument::FindFlag::FindCaseSensitively : flag;
	flag = ui->checkBox_2->isChecked() ? flag | QTextDocument::FindFlag::FindWholeWords : flag;

	QString findtext = ui->lineEdit->text();//获得对话框的内容
	if (textEdit->find(findtext,flag))//查找后一个
	{
		// 查找到后高亮显示
		QPalette palette = textEdit->palette();
		palette.setColor(QPalette::Highlight, palette.color(QPalette::Active, QPalette::Highlight));
		textEdit->setPalette(palette);
	}else{
		QMessageBox::information(this, QString::fromLocal8Bit("waring"), QString::fromLocal8Bit("not find text!"), QMessageBox::Ok);
	}

}

void FindDialog::on_pushButtonLast_clicked()
{
	QTextDocument::FindFlags flag = QTextDocument::FindFlag::FindBackward;

	flag = ui->checkBox_1->isChecked() ? flag | QTextDocument::FindFlag::FindCaseSensitively : flag;
	flag = ui->checkBox_2->isChecked() ? flag | QTextDocument::FindFlag::FindWholeWords : flag;

	QString findtext = ui->lineEdit->text();//获得对话框的内容
	if (textEdit->find(findtext, flag))//查找后一个
	{
		// 查找到后高亮显示
		QPalette palette = textEdit->palette();
		palette.setColor(QPalette::Highlight, palette.color(QPalette::Active, QPalette::Highlight));
		textEdit->setPalette(palette);
	}else{
		QMessageBox::information(this, QString::fromLocal8Bit("waring"), QString::fromLocal8Bit("not find text!"), QMessageBox::Ok);
	}
}

#include "codeEdit/moc_FindDialog.cpp"