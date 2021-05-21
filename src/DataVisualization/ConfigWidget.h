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
class ArrowCtrl;
namespace Mas{
	enum DATA_VISUALIZATION_EXPORT structTexture
	{
		//理想导体
		PerfectConductor = 3,
		//电导新材料
		ConductorNew = 8,
		//介质
		Diolectric = 4,
		//电介质和电导
		dielectirAndconductance = 16,
		//磁导率
		Permeability = 32,
		//
		Freespace = 64,
		//
		FOIL = 128,

		//线段
		//波导端口
		waveGuideport = 1024,
		DRIVER = 2048,
		//感应器
		Inductor = 16384

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
public:
	explicit ConfigWidget(QWidget* panter = nullptr);
	~ConfigWidget();
protected:
	void initUI();
public Q_SLOTS:
	//保存
	void saveclicked();
	void canclelicked();
	//刻度标
	void axisColorclicked();
	void axisValColorclicked();
	//结构图
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
	//2维结构图
	void PerfectConductorClicked2();
	void ConductorNewClicked2();
	void DiolectricClicked2();
	void PermeabilityClicked2();
	void dielectirAndconductanceClicked2();
	//时间图
	void linecolorClicked();
	//矢量图
	void veccolorClicked();
	//相空间图
	void partcleColorclicked();
	//等位图
	void changeUser_defined(int);
private:
	void loadxmlConfig();
	void SetAllreRender(QPushButton*);
	void fileeButtom(QPushButton*, std::string);
	QColor setbuttomColor(QPushButton*);
private:
	void structInfoClicked(int _property,QPushButton*);
	void structinfolineClicked(int _property, QPushButton*);
	void struct_2D_clicked(int _property,QPushButton*);
	//结构图
	std::map<QString, QString> structColor;
	std::map<QString, QString>structlineColor;
	std::map<int, QString> struct2dinfo;
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
	ArrowCtrl* arrowCtrl;
private:
	Ui::ConfigWidget *ui;
};
#endif