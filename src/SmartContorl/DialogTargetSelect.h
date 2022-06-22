#pragma once
#include <QDialog>

namespace Ui {
	class DialogTargetSelect;
}

class DialogTargetSelect :public QDialog {
	Q_OBJECT
public:
	DialogTargetSelect(QWidget* parent = 0);
	~DialogTargetSelect();
	
	//新建类型
	int index;
private:
	Ui::DialogTargetSelect* ui;
public slots:
	void on_pushButtonOk_clicked();
};