#pragma once
#include <QtGui/QDialog>
#include "LoadingDialog.h"
namespace Ui{
	class LoadingDialog;
}
class  LoadingDialog : public QDialog
{

	Q_OBJECT
public:
	LoadingDialog(QWidget *parent = 0);
	~LoadingDialog();
private:
	Ui::LoadingDialog *ui;
};
