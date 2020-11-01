#pragma once
#include <qobject.h>
#include "SmartContorlConfig.hpp"
class SMARTCONTORL_EXPORT SmartContorlInterface :public QObject{
	Q_OBJECT
public:
	SmartContorlInterface(){};
	~SmartContorlInterface(){}
	void  init();
public slots:
	void buttonClicked(int type);
};