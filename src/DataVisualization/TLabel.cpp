#include "TLabel.h"
#include <QDebug>
#include<QMouseEvent>
#include<QLineEdit>
#include <QPushButton>
#include <QPlainTextEdit>
#include<QGridLayout>
#include "C_encoding.h"
#include<QApplication>
#include <QDesktopWidget>
/**
* @brief TLabel::TLabel
* @param QWidget * parent
* @return 
* @Time 2021/6/29
*/
TLabel::TLabel(QWidget* parent) :QLabel(parent){
	//mTlineEdit = new TlineEdit;
	mTDialog = new TDialog(this);
	mTDialog->setModal(true);
	connect(mTDialog, SIGNAL(signalCloseEvent(bool)), this, SLOT(slotCloseEvent(bool)));
}
/**
* @brief TLabel::~TLabel
* @return 
* @Time 2021/6/29
*/
TLabel::~TLabel(){
	//delete mTlineEdit;
	delete mTDialog;
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
		if (mTDialog->isVisible())
		{
			slotCloseEvent(true);
		}
		else
		{
			mTDialog->SetMsgtext(this->text());
			QWidget* parent = dynamic_cast<QWidget*>(this->parent());
			QPoint pos = parent->mapToGlobal(QPoint(0,0));
			mTDialog->move(pos);
			mTDialog->show();
		}
	}
}
/**
* @brief TDialog::SetMsgtext 设置消息
* @param QString & str
* @return void
* @Time 2021/6/30
*/
void TDialog::SetMsgtext(QString& str)
{
	mPlainTextEdit->setPlainText(str);
}
/**
* @brief TDialog::GetMsgText 获取消息
* @return QT_NAMESPACE::QString
* @Time 2021/6/30
*/
QString TDialog::GetMsgText()
{
	QString res = mPlainTextEdit->toPlainText();
	return res;
}
TDialog::TDialog(QWidget* parent) :QDialog(parent){

	gridLayout = new QGridLayout;;
	mPlainTextEdit = new QPlainTextEdit();
	gridLayout->addWidget(mPlainTextEdit,0,0,1,2);
	appbutton = new QPushButton();
	appbutton->setText(QString("save"));
	gridLayout->addWidget(appbutton,1,1,1,1);
	gridLayout->setRowStretch(0,9);
	gridLayout->setRowStretch(1, 1);
	gridLayout->setColumnStretch(0,9);
	gridLayout->setColumnStretch(1, 1);
	this->setLayout(gridLayout);
	connect(appbutton, SIGNAL(clicked()), this, SLOT(buttonClicked()));

	
}
void TDialog::buttonClicked()
{
	emit signalCloseEvent(false);
}
TDialog::~TDialog(){

}
void TDialog::closeEvent(QCloseEvent *e)
{
	//忽略关闭信号
	e->ignore();
	emit signalCloseEvent(true);
}
void TLabel::slotCloseEvent(bool isclose)
{
	this->setText(mTDialog->GetMsgText());
	if (isclose)
	{
		mTDialog->hide();
	}
}
#include "moc_TLabel.cpp"