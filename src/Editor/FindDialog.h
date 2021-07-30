#pragma once
#include <QDialog>
#include "QPlainTextEdit"
namespace Ui {
	class FindDialog;
}
class FindDialog:public QDialog
{
	Q_OBJECT
public:
	FindDialog(QWidget* parent = 0);
	~FindDialog();

	void setTextEidt(QPlainTextEdit* eidt){
		textEdit = eidt;
	};
private:
	Ui::FindDialog *ui;
	QPlainTextEdit *textEdit;

public slots:
	void on_pushButtonNext_clicked();
	void on_pushButtonLast_clicked();
	void on_pushButton_replace();
};