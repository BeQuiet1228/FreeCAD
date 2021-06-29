#include "TLabel.h"
#include <QDebug>
#include<QMouseEvent>
#include<QLineEdit>
/**
* @brief TLabel::TLabel
* @param QWidget * parent
* @return 
* @Time 2021/6/29
*/
TLabel::TLabel(QWidget* parent) :QLabel(parent){
	mTlineEdit = new TlineEdit;
	connect(mTlineEdit, SIGNAL(signalCloseEvent()), this, SLOT(slotCloseEvent()));
}
/**
* @brief TLabel::~TLabel
* @return 
* @Time 2021/6/29
*/
TLabel::~TLabel(){
	delete mTlineEdit;
}
/**
* @brief TLabel::mouseDoubleClickEvent 鼠标双击事件
* @param QMouseEvent * e
* @return void
* @Time 2021/6/29
*/
void TLabel::mouseDoubleClickEvent(QMouseEvent *e){
	if (e->button()==Qt::LeftButton)
	{
		if (mTlineEdit->isVisible())
		{
			slotCloseEvent();
		}
		else
		{
			mTlineEdit->setText(this->text());
			QSize size = mTlineEdit->size();
			size.setWidth(this->text().length()*10);
			size.setHeight(40);
			mTlineEdit->resize(size);
			mTlineEdit->show();
		}
	}
}
/**
* @brief TlineEdit::TlineEdit
* @param QWidget * parent
* @return 
* @Time 2021/6/29
*/
TlineEdit::TlineEdit(QWidget* parent) :QLineEdit(parent)
{

}
/**
* @brief TlineEdit::~TlineEdit
* @return 
* @Time 2021/6/29
*/
TlineEdit::~TlineEdit()
{

}
void TlineEdit::closeEvent(QCloseEvent *e)
{
	//忽略关闭信号
	e->ignore();
	emit signalCloseEvent();
}
void TLabel::slotCloseEvent()
{
	QString text = mTlineEdit->text();
	this->setText(text);
	mTlineEdit->hide();
}
#include "moc_TLabel.cpp"