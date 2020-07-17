#pragma once

#include <QtGui/QWidget>
#include <memory>
#include "ContorlConfig.hpp"
class Chipic;
namespace Ui{
	class Form;
}
class CONTROL_EXPORT ContorlDataBar: public QWidget
{
	Q_OBJECT

public:
	ContorlDataBar(QWidget *parent = 0);
	~ContorlDataBar();

public: 
	//设置显示数据
	void setChipicData(std::shared_ptr<Chipic> chipic);
	//chipic关闭
	void chipicClose();
private:
	Ui::Form *ui;
};