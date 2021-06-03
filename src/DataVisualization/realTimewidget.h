#pragma once
#ifndef REALTIME_WIDGET_H_
#define REALTIME_WIDGET_H_
#include <QWidget>
class QTableWidgetItem;
namespace Ui
{
	class realTimewidget;
}
class realTimewidget :public QWidget
{
	Q_OBJECT
public:
	explicit realTimewidget(QWidget* parent = nullptr);
	~realTimewidget();
	void init(float min, float max);
Q_SIGNALS:
	void setcoloseEvent(bool);
	void GetListDouble(std::vector<double>&);
	public Q_SLOTS:
	void addClicked();
	void deleteClicked();
	void tableWidgetClicked(QTableWidgetItem*);
public :
	void closeEvent(QCloseEvent *event);
protected:
	int GetdecimalBit(float& value);
	void insertformatTableItem();
private:
	Ui::realTimewidget *ui;
	float min;
	float max;
	int curRow;
	int lastRow;
};
#endif