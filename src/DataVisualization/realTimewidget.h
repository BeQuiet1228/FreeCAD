#pragma once
#ifndef REALTIME_WIDGET_H_
#define REALTIME_WIDGET_H_
#include <QWidget>
#include <QDialog>
#include "exportConfig.hpp"
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
	protected:
		void addTableItem(double val);
		void setRangTitle();
		void clearTableItem();
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