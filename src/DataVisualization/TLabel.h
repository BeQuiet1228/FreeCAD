#pragma once
#ifndef TLABEL_H_
#define TLABEL_H_
#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QDialog>
class QPushButton;
class QPlainTextEdit;
class QGridLayout;
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
	public Q_SLOTS:
	void slotCloseEvent(bool);
protected:
	//TlineEdit* mTlineEdit;
	TDialog* mTDialog;
	std::vector<QRect> screens;
};
#endif // !TLABEL_H_
