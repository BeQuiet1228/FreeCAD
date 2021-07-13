#pragma once
#ifndef VARIATEITEMWIDGET2_H_
#define VARIATEITEMWIDGET2_H_
#include<QDialog>
class QTableWidget;
class QPushButton;
class QGridLayout;
class QLineEdit;
class QTableWidgetItem;
class VariateitemWidget2:public QDialog
{
	Q_OBJECT
public:
	VariateitemWidget2(QWidget* parent=nullptr);
	~VariateitemWidget2();
	QString getName()
	{
		return name;
	}
	std::vector<double> getdatas()
	{
		return datas;
	}
	int getCount()
	{
		return Count;
	}
protected:
	void initUI();
	void addtablewidget();
	void deletetablewidget();
	void OKClicked();
protected Q_SLOTS:
	void BtnClicked(bool);
	void tableWidgetClicked(QTableWidgetItem*);
private:
	QTableWidget* mtablewidget;
	QPushButton* addBtn;
	QPushButton* deleteBtn;
	QPushButton* okBtn;
	QGridLayout* layout;
	QLineEdit* mLineEdit;
	int currow;
	//
	int Count;
	std::vector<double> datas;
	QString name;
public:
	bool okClicked=false;
};
#endif