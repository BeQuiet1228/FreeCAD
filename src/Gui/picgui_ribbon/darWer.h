#pragma once
#ifndef DARWER_H_
#define DARWER_H_
#include<QWidget>
#include <QDialog>
//#include<QBoxLayout>
class darWer:public QWidget
{
	Q_OBJECT
public:
	darWer(QWidget* parent = nullptr);
	~darWer();
	void initUI();
	void insertbutton(std::list<QAction*>&);
private:
	QString Titile;
	QBoxLayout* layout;
};
#endif // !DARWER_H_
