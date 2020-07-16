#pragma once
#include <QtGui/QDialog>
namespace Ui{
	class ThreadCountDialog;
}
class  ThreadCountDialog : public QDialog
{

	Q_OBJECT
public:
	ThreadCountDialog(QWidget *parent = 0);
	~ThreadCountDialog();

	bool okBuutonClicked = false;
	int threadCount = 1;
private:
	Ui::ThreadCountDialog *ui;

public Q_SLOTS:
	void on_pushButtonOk_clicked();
};
