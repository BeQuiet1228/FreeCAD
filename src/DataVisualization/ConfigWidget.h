#pragma once
#ifndef CONFIG_WIDGET_H_
#define CONFIG_WIDGET_H_
#include <QWidget>
#include <map>
class QPushButton;
namespace Mas{
	enum structTexture
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
	struct Setconfig
	{
		QString _1st;
		QString _2nd;
		QString _3th;
		QString _4th;
		Setconfig() :_1st("1"), _2nd("1"), _3th("1"), _4th("1")
		{}
	};
}
namespace Ui{
	class ConfigWidget;
}
class ConfigWidget:public QWidget
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
	//时间图
	void linecolorClicked();
	//矢量图
	void veccolorClicked();
	//相空间图
	void partcleColorclicked();
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
	std::map<QString, QString>structlineColor;
	//向量
	Mas::Setconfig vecconfig;
	//时间图
	Mas::Setconfig timeConfig;
	//相空间图
	Mas::Setconfig partcleConfig;
	//刻度相关的参数
	Mas::Setconfig axisinfo;
private:
	Ui::ConfigWidget *ui;
};
#endif