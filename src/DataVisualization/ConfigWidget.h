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
		Perfect_Conductor = 3,
		//电导新材料
		Conductor_New = 8,
		//介质
		Diolectric = 4,
		//磁导率
		Permeability = 16,
		//真空
		Vacuo = 1024,
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
	void perfectconductorClicked();
	void conductornewClicked();
	void diolectricClicked();
	void permeabilityClicked();
	void vacuoClicked();
	void perfectconductorlineClicked();
	void conductornewlineClicked();
	void diolectriclineClicked();
	void permeabilitylineClicked();
	void vacuolineClicked();
	//2维结构图
	void perfectconductorClicked_2();
	void conductornewClicked_2();
	void diolectricClicked_2();
	void permeabilityClicked_2();
	void vacuoClicked_2();
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