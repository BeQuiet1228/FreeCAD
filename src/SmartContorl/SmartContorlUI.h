#pragma once
#include <QWidget>
#include "FileMaker.h"
#include <deque>
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
public Q_SLOTS:
	void on_pushButton_clicked();
	void chipicStartFinished(unsigned long threadID);
};