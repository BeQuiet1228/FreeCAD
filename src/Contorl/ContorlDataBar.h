#pragma once

#include <QtGui/QWidget>
#include "Chipic.h"
#include <memory>
#include "ContorlConfig.hpp"

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
private:
	Ui::Form *ui;
};