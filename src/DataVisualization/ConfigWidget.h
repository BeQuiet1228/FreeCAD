#pragma once
#ifndef CONFIG_WIDGET_H_
#define CONFIG_WIDGET_H_
#include <QWidget>
#include <map>
#include "exportConfig.hpp"
class QPushButton;
//class QGridLayout;
class QBoxLayout;
class QwtScaleWidget;
class QwtScaleEngine;
class QwtLinearColorMap;
class ColorTab;
class ArrowCtrl;
class Plot;
namespace Mas{
	enum DATA_VISUALIZATION_EXPORT structTexture
	{
		//理想导体
		PERFECTCONDUCTOR = 3,
		//电导新材料
		CONDUCTORNEW = 8,
		//介质
		DIOLECTRIC = 4,
		//电介质和电导
		DIELECTIRANDCONDUCTANCE = 16,
		//磁导率
		PERMEABILITY = 32,
		//
		FREESPACE = 64,
		//
		FOIL = 128,

		//线段
		PORT,
		DRIVER,
		INDUCTOR

	};
	struct DATA_VISUALIZATION_EXPORT Setconfig
	{
		QString _1st;
		QString _2nd;
		QString _3th;
		QString _4th;
		Setconfig();
	};
}
namespace Ui{
	class ConfigWidget;
}
class DATA_VISUALIZATION_EXPORT ConfigWidget :public QWidget
{
	Q_OBJECT
public:
	explicit ConfigWidget(QWidget* panter = nullptr);
	~ConfigWidget();
protected:
	void initUI();
public:
	void bindplot(Plot* lp);
public:
	static QwtLinearColorMap* getQwtLinearColorMap();
	//static std::map<double, QColor> getColortab();
Q_SIGNALS:
	void plotLoadconfig();
public Q_SLOTS:
	//保存
	void saveclicked();
	void canclelicked();
	void axisColorclicked();
	void axisValColorclicked();
	void PerfectConductorClicked();
	void ConductorNewClicked();
	void DiolectricClicked();
	void PermeabilityClicked();
	void dielectirAndconductanceClicked();
	void PerfectConductorlineClicked();
	void ConductorNewlineClicked();
	void DiolectriclineClicked();
	void PermeabilitylineClicked();
	void dielectirAndconductancelineClicked();
	void FreespaceClicked();
	void Freespacelineclicked();
	void FOILclicked();
	void FOILlineclicked();
	void PortClicked();
	void InductorClicked();
	void DriverClicked();
	void linecolorClicked();
	void veccolorClicked();
	void partcleColorclicked();
	void radioButton1(bool);
	void radioButton2(bool);
	void setfirstColor();
	void setendColor();
private:
	void loadxmlConfig();
	void SetAllreRender(QPushButton*);
	void fileeButtom(QPushButton*, std::string);
	QColor setbuttomColor(QPushButton*);
private:
	void structInfoClicked(int _property,QPushButton*);
	void structinfolineClicked(int _property, QPushButton*);
	//结构图
	std::map<QString, QString> structColor;
	std::map<QString, QString> structlineColor;
	//向量
	Mas::Setconfig vecconfig;
	//时间图
	Mas::Setconfig timeConfig;
	//相空间图
	Mas::Setconfig partcleConfig;
	//刻度相关的参数
	Mas::Setconfig axisinfo;
	//等位图相关
	//QGridLayout* gridLayout;
	QBoxLayout* boxLayout;
	QwtScaleWidget *scaleWIdget;
	QwtScaleEngine *scaleEngine;
	ColorTab* mColorTab;
	ArrowCtrl* arrowCtrl;
private:
	Ui::ConfigWidget *ui;
};
#endif