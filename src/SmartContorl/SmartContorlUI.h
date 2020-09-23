#pragma once
#include <QWidget>
#include "FileMaker.h"
#include <deque>
#include <QListWidgetItem>
#include <map>
#include <QModelIndex>
#include "SmartContorl.h"
namespace Ui{
	class SmartContorlUI;
}
class SmartContorlUI:public QWidget{
	Q_OBJECT
public:
	SmartContorlUI(QWidget * parent = 0);
	~SmartContorlUI();
private:
	Ui::SmartContorlUI *ui;
	//组合之后的文件信息
	std::deque<FileMaker::M3dData> m3dDatas;
	//信息栏
	std::map<unsigned long, QListWidgetItem*> itemMap;
	//文件生成器
	FileMaker fileMaker;
	//threadID对应的m3d路径
	std::map<unsigned long, QString> pathMap;

	SmartContorl smartContorl;
public Q_SLOTS:
	void on_pushButton_clicked();
	void on_pushButton_3_clicked();
	void on_pushButton_4_clicked();
	void on_pushButton_5_clicked();
	void on_pushButton_6_clicked();
	void on_pushButton_7_clicked();
	void chipicStartFinished(unsigned long threadID);
	void chipicWorkFinished(unsigned long threadID);
};