#pragma once
#ifndef TLABEL_H_
#define TLABEL_H_
#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QDialog>
#include"Axis.h"
class QPushButton;
class QPlainTextEdit;
class QGridLayout;
class QPainter;
class TDialog :public QDialog
{
	Q_OBJECT
public:
	TDialog(QWidget* parent = nullptr);
	~TDialog();
	void closeEvent(QCloseEvent *e);
	void SetMsgtext(QString&);
	QString GetMsgText();
Q_SIGNALS:
	void signalCloseEvent(bool);
private Q_SLOTS:
void buttonClicked();
private:
	QPushButton* appbutton;
	QPushButton* unappbtn;
	QPlainTextEdit* mPlainTextEdit;
	QGridLayout* gridLayout;
	
};

class TLabel:public QLabel
{
	Q_OBJECT
public:
	explicit TLabel(QWidget* parent=nullptr);
	~TLabel();
	virtual void mouseDoubleClickEvent(QMouseEvent *e) override;
	void loadconfig();
	void setStyle(Axisstyle);
	public Q_SLOTS:
	void slotCloseEvent(bool);
	QSizeF TextSize();
	void Autosize();
	void setColor(QColor);
protected:
	void paintEvent(QPaintEvent* event);
	void drawTitle(QPainter*);
protected:
	//TlineEdit* mTlineEdit;
	TDialog* mTDialog;
	std::vector<QRect> screens;
	Axisstyle mAxisstyle;
};
#endif // !TLABEL_H_
