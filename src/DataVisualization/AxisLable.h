#pragma once
#ifndef AXISLABLE_H_
#define AXISLABLE_H_
#include <QDialog>
class QLineEdit;
class QGridLayout;
class QBoxLayout;
class AxisLable :public QDialog
{
	Q_OBJECT
public:
	AxisLable(QWidget* parent = nullptr);
	~AxisLable();
	//
	void setMinval(QString);
	void setMaxval(QString);
	void setAxisUnitval(QString);
	//
	double getMinval();
	double getMaxval();
	QString getAxisUnitval();
	void closeEvent(QCloseEvent * e);
Q_SIGNALS:
	void signalCloseEvent();
private:
	void initUI();
private:
	QLineEdit* minLineedit;
	QLineEdit* maxLineedit;
	QLineEdit* AxisUnitedit;
	QGridLayout* mQGridLayout;
	//QBoxLayout* boxLayout;
};
#endif // !AXISLABLE_H_
