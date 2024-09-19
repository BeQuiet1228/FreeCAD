#pragma once
#include <QDialog>
#include <memory>
namespace Ui {
	class VariateInputDialog_UI;
} // namespace Ui
struct VariateData;
class VariateInputDialog:public QDialog{
	Q_OBJECT
public:
	VariateInputDialog(QWidget *parent = 0);
	~VariateInputDialog();
	//获取variate数据
	std::shared_ptr<VariateData> getData();
	void setData(std::shared_ptr<VariateData>);
	//ok按钮是否被点击
	bool okClicked = false;
protected:
	Ui::VariateInputDialog_UI *ui;
	//数据对象
	std::shared_ptr<VariateData> data;

public Q_SLOTS:
void on_pushButtonOk_clicked();
};