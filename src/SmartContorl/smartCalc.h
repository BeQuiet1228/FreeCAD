#pragma once
#ifndef SMARTCALC_H_
#define SMARTCALC_H_
#include <QWidget>
#include<vector>
#include<memory>
struct VariateData;
namespace Ui {
	class smartCalc;
}
class smartCalc 
	:public QWidget
{
	Q_OBJECT
public:
	explicit smartCalc(QWidget* parent = nullptr);
public:
	void initUI();
public Q_SLOTS:
	void BtnClicked(bool);
protected:
	void addButton(bool);
	void deleteButton(bool);
	void run(bool);
	void qPrint(std::string str);
private:
	//变量列表
	std::vector<std::shared_ptr<VariateData>> variateDatas;
private:
	Ui::smartCalc* ui;
};
#endif