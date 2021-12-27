#pragma once
#ifndef REALTIME_WIDGET_H_
#define REALTIME_WIDGET_H_
#include <QWidget>
#include <QDialog>
#include "exportConfig.hpp"
#include <list>
class QTableWidgetItem;
namespace Ui
{
	class realTimewidget;
}
namespace DV
{
	
	class DATA_VISUALIZATION_EXPORT realTimewidget :public QDialog
	{
		Q_OBJECT
	public:
		explicit realTimewidget(QWidget* parent = nullptr);
		~realTimewidget();
		void loadConfigLevels(std::list<double>&);
		std::list<double> getConfigLevels();
	public:
		struct ScalarItemData
		{
			QString valStr;
			double value;
			bool  operator <(const ScalarItemData& that) const;
		};
		std::list<ScalarItemData> getScalarDatas(std::list<double>& value);
	protected:
		void addTableItem(double val);
		void setRangTitle();
		void clearTableItem();
		void boolCellChangedConnect(bool);
		void addTableItem(QString, double);
	Q_SIGNALS:
		void sendConfigLevels(std::list<double>&);
	public Q_SLOTS:
		void btnClicked();
		void slotCellChange(int,int);
	protected:
		virtual void addClicked();
		virtual void deleteClicked();
		virtual void saveClicked();
	protected:
		Ui::realTimewidget* ui;
		double min, max;
	};
}
#endif