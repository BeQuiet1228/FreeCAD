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
namespace Ui {
	class ConfigWidget;
}
namespace DV {
	class Plot;
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
		void addTabWidget(std::vector<QWidget*>&);
	public:
		static QwtLinearColorMap* getQwtLinearColorMap();
		void loadxmlConfig();
	Q_SIGNALS:
		void plotLoadconfig();
	public Q_SLOTS:
		void btnClicked();
	private:
		
		//±£´æ
		void saveclicked();
		void canclelicked();
	private:
		QwtScaleWidget* scaleWIdget;
		QwtScaleEngine* scaleEngine;
	private:
		Ui::ConfigWidget* ui;
	};
};

#endif