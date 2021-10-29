#pragma once
#ifndef SMARTCALC_H_
#define SMARTCALC_H_
#include <QWidget>
#include<QDialog>
#include<vector>
#include<memory>
#include "SmartContorlConfig.hpp"
struct VariateData;
class SmartContorl;
class QListWidgetItem;
namespace Ui {
	class smartCalc;
}
class SMARTCONTORL_EXPORT smartCalc
	:public QDialog
{
	Q_OBJECT
public:
	explicit smartCalc(QWidget* parent = nullptr);
public:
	void initUI();
	void initData();
	void afferscriptpath(std::string path);
	void afferm3dpath(std::string path);
	bool getRunning();
public Q_SLOTS:
	void BtnClicked(bool);
	void addListWidgetItem(QListWidgetItem* item, QWidget* widget);
	void pringLuaLog(std::string str);
protected:
	void addButton(bool);
	void deleteButton(bool);
	void run(bool);
	void qPrint(std::string str);
	void qPrint(QString str);
	QString replaceVariate();
	void loadParameterXml();
	void saveParameterXml();
private:
	//变量列表
	std::vector<std::shared_ptr<VariateData>> variateDatas;
	SmartContorl* smartContorl;
private:
	Ui::smartCalc* ui;
	//传入的脚本路径
	std::string scriptPath;
	//生成的m3d路径
	std::string m3dPath;
public :
	////批处理整个模块的运行状态
	//bool isRun;
};
#endif