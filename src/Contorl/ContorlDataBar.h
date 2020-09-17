#pragma once

#include <QtGui/QWidget>
#include <memory>
#include "ContorlConfig.hpp"
#include "ContorlBar.h"
class Chipic;
namespace Ui{
	class Form;
}
class CONTROL_EXPORT ContorlDataBar: public ContorlBar
{
	Q_OBJECT

public:
	ContorlDataBar(QWidget *parent = 0);
	~ContorlDataBar();

public: 
	//chipic¹Ø±Õ
	void chipicClose();
	
	void updateUI() override;
private:
	Ui::Form *ui;
};