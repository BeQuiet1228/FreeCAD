#pragma once
#include <qobject.h>
#include "SmartContorlConfig.hpp";
class QWidget;
class SMARTCONTORL_EXPORT SmartContorlInterface :public QObject{
	Q_OBJECT
public:
	SmartContorlInterface()= default;
	~SmartContorlInterface() = default;
	void  init();
	static void showSmartControlUI(const std::string& path);
	static QWidget* creatSmartControlUI(const std::string& path);
public slots:
	void buttonClicked(int type);
};