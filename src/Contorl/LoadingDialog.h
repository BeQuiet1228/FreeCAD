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
	void  setText(const std::string& text);
	void show();
	void close();

public:
	bool isShow = false;
private:
	Ui::LoadingDialog *ui;
protected:
	void closeEvent(QCloseEvent *event) override;

Q_SIGNALS:
	void dialogClose();
};
