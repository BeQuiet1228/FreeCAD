#pragma once
#include <QWidget>
#include "FileMaker.h"
#include <deque>
#include <QListWidgetItem>
#include <map>
#include <QModelIndex>
#include "SmartContorl.h"
#include <QListWidgetItem>
#include <vector>
#include <memory>
#include <qdialog.h>
#include <QCloseEvent>
#include "SmartContorlConfig.hpp"
#include "SmartContorlUI.h"
class VariateChart;
class VariateItemWidget;
namespace Ui {
	class MultipleTargetGeneticAlgorithmUI;
}
class OptimizeCurseLua;
class SMARTCONTORL_EXPORT MultipleTargetGeneticAlgorithmUI :public QDialog {
	Q_OBJECT
public:
	MultipleTargetGeneticAlgorithmUI(QWidget* parent = 0);
	~MultipleTargetGeneticAlgorithmUI();

public:
	void setTextPath(const std::string& path);
	//载入优化配置
	void loadParameterXml();
	bool getRunning();

	void setGMod(const bool& b);
private:
	Ui::MultipleTargetGeneticAlgorithmUI* ui;
	//组合之后的文件信息
	std::deque<FileMaker::M3dData> m3dDatas;
	//信息栏
	std::map<unsigned long, QListWidgetItem*> itemMap;
	//文件生成器
	FileMaker fileMaker;
	//threadID对应的m3d路径
	std::map<unsigned long, QString> pathMap;

	SmartContorl* smartContorl;
	//变量列表
	std::vector<std::shared_ptr<VariateData>> variateDatas;

	//是否是G占优模式
	bool GMod = false;

public Q_SLOTS:
	void on_pushButton_clicked();
	void on_pushButton_2_clicked();
	void on_pushButtonF_clicked();
	void on_pushButtonAddVariate_clicked();
	void on_pushButtonDeleteVariate_clicked();
	void on_pushButtonAddTarget_clicked();
	void on_pushButtonDeleteTarget_clicked();
	void on_pushButtonTargetChart_clicked();
	void chipicStartFinished(unsigned long threadID);
	void chipicWorkFinished(unsigned long threadID);
	void addListWidgetItem(QListWidgetItem* item, QWidget* widget);
	//打印lua中输出得log
	void pringLuaLog(std::string str);
	//查看变量趋势图
	void on_pushButtonVariateMax_clicked();

private:
	//替换变量
	QString replaceVariate();
	//保存xml文件
	void saveParameterXml();
protected:
	void closeEvent(QCloseEvent* event);
};