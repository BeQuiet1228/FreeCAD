#pragma once
#ifndef TLABEL_H_
#define TLABEL_H_
#include <QWidget>
#include <QLabel>
#include <QLineEdit>
class TlineEdit :public QLineEdit
{
	Q_OBJECT
public:
	TlineEdit(QWidget* parent = nullptr);
	~TlineEdit();
	void closeEvent(QCloseEvent *e);
Q_SIGNALS:
	void signalCloseEvent();
};

class TLabel:public QLabel
{
	Q_OBJECT
public:
	explicit TLabel(QWidget* parent=nullptr);
	~TLabel();
	virtual void mouseDoubleClickEvent(QMouseEvent *e) override;
	public Q_SLOTS:
	void slotCloseEvent();
protected:
	TlineEdit* mTlineEdit;
};
#endif // !TLABEL_H_
