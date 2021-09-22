#pragma once
#ifndef DARWER_H_
#define DARWER_H_
#include<QWidget>
#include <QDialog>
//#include<QBoxLayout>
class QBoxLayout;
class darWer:public /*QWidget*/QFrame
{
	Q_OBJECT
public:
	darWer(QWidget* parent = nullptr);
	~darWer();
	void initUI();
	void addButton(QToolButton* button);
	void setTitle(const QString& title);
	void setSize(QSize& size);
	QSize getSize() { return mSize; }
	QList<QAction*> get_action_all();
protected Q_SLOTS:
	void btnClicked();
private:
	QBoxLayout* mQBoxLayout;
	QString Title;
	QSize mSize;
};
#endif // !DARWER_H_
