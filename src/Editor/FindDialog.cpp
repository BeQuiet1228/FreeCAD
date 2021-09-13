#include "FindDialog.h"
#include "ui_FindDialog.h"
#include <iostream>
#include <QMessageBox>
#include <QPalette>
FindDialog::FindDialog(QWidget* parent /*= 0*/)
	:QDialog(parent), ui(new Ui::FindDialog()), textEdit(nullptr)
{
	ui->setupUi(this);
	connect(ui->pushButtonAll_replace,SIGNAL(clicked()),this,SLOT(on_pushButton_replace()));
	connect(ui->pushButtonNext_replace,SIGNAL(clicked()),this,SLOT(on_pushButton_replace()));
}
/**
* @brief FindDialog::on_pushButton_replace 实现替换（全部替换,替换下一个）
* @return void
* @Time 2021/7/16
*/
void FindDialog::on_pushButton_replace()
{
	QTextDocument::FindFlags flag = 0;
	flag = ui->checkBox_1->isChecked() ? flag | QTextDocument::FindFlag::FindCaseSensitively : flag;
	flag = ui->checkBox_2->isChecked() ? flag | QTextDocument::FindFlag::FindWholeWords : flag;
	QString findtext = ui->lineEdit->text();//获得对话框的内容
	QString replacetext = ui->lineEdit_2->text();//获取替换的对话框内容
	//替换全部
	if (sender()==ui->pushButtonAll_replace)
	{
		//获取当前的光标位置
		auto curtextcursor=textEdit->textCursor();
		QTextCursor fistCursor;
		fistCursor.setPosition(0);
		textEdit->setTextCursor(fistCursor);
		int replaceCount = 0;
		while (textEdit->find(findtext,flag))
		{
			textEdit->cut();
			textEdit->insertPlainText(replacetext);
			replaceCount++;
		}
		textEdit->setTextCursor(curtextcursor);
		if (replaceCount>0)
			QMessageBox::information(this, QString::fromLocal8Bit("output"), QString::fromLocal8Bit("replace text count:%1").arg(replaceCount), QMessageBox::Ok);
		else
			QMessageBox::information(this, QString::fromLocal8Bit("waring"), QString::fromLocal8Bit("not find text!"), QMessageBox::Ok);
	}
	//替换下一个
	else if(sender()==ui->pushButtonNext_replace)
	{
		if (textEdit->find(findtext,flag))
		{
			textEdit->cut();
			textEdit->insertPlainText(replacetext);
			textEdit->find(replacetext, QTextDocument::FindFlag::FindBackward);
			QPalette palette = textEdit->palette();
			palette.setColor(QPalette::Highlight, palette.color(QPalette::Active, QPalette::Highlight));
			textEdit->setPalette(palette);
		}
		else
			QMessageBox::information(this, QString::fromLocal8Bit("waring"), QString::fromLocal8Bit("not find text!"), QMessageBox::Ok);
	}
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
