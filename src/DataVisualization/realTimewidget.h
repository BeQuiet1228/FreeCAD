#pragma once
#ifndef REALTIME_WIDGET_H_
#define REALTIME_WIDGET_H_
#include <QWidget>
#include <QDialog>
class QTableWidgetItem;
namespace Ui
{
	class realTimewidget;
}
class realTimewidget :public QDialog
{
	Q_OBJECT
public:
	explicit realTimewidget(QWidget* parent = nullptr);
	~realTimewidget();
	void init(float min, float max);
	void init(std::list<double>&);
Q_SIGNALS:
	void setcoloseEvent(bool);
	void GetListDouble(std::list<double>&);
	public Q_SLOTS:
	void addClicked();
	void deleteClicked();
	void tableWidgetClicked(QTableWidgetItem*);
	void BtnClicked();
public :
	void closeEvent(QCloseEvent *event);
protected:
	int GetdecimalBit(float& value);
	int GetdecimalBit(double& value);
	void insertformatTableItem();
	void addTableItem(double);
private:
	Ui::realTimewidget *ui;
	double min;
	double max;
	//int curRow;
	//int lastRow;
};
#endif