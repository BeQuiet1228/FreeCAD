#include "TLabel.h"
#include <QDebug>
#include<QMouseEvent>
#include<QLineEdit>
#include <QPushButton>
#include <QPlainTextEdit>
#include<QGridLayout>
#include "C_encoding.h"
#include "CustomConfig.h"
#include<QPainter>
/**
* @brief TLabel::TLabel
* @param QWidget * parent
* @return 
* @Time 2021/6/29
*/
TLabel::TLabel(QWidget* parent) :QLabel(parent){
	//mTlineEdit = new TlineEdit;
	mTDialog = new TDialog();
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
			mTDialog->SetMsgtext(mtitle);
			/*QWidget* parent = dynamic_cast<QWidget*>(this->parent());
			QPoint pos = parent->mapToGlobal(QPoint(0,0));
			mTDialog->move(pos);*/
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
	mPlainTextEdit = new QPlainTextEdit(this);
	gridLayout->addWidget(mPlainTextEdit,0,0,1,3);
	appbutton = new QPushButton(this);
	appbutton->setText(GetEncodingstr("确定",ENCODING_GB2312));
	unappbtn=new QPushButton(this);
	unappbtn->setText(GetEncodingstr("取消",ENCODING_GB2312));
	gridLayout->addWidget(appbutton,1,1,1,1);
	gridLayout->addWidget(unappbtn, 1, 2, 1, 1);
	this->setLayout(gridLayout);
	connect(appbutton, SIGNAL(clicked()), this, SLOT(buttonClicked()));
	connect(unappbtn, SIGNAL(clicked()), this, SLOT(buttonClicked()));
}
void TDialog::buttonClicked()
{
	if (sender()==appbutton)
	{
		emit signalCloseEvent(false);
	}
	else if (sender()==unappbtn)
	{
		hide();
	}
	
}
TDialog::~TDialog(){

}
void TDialog::closeEvent(QCloseEvent *e)
{
	//忽略关闭信号
	e->ignore();
	//emit signalCloseEvent(true);
	hide();
}
void TLabel::slotCloseEvent(bool isclose)
{
	this->setTextstr(mTDialog->GetMsgText());
	if (isclose)
	{
		mTDialog->hide();
	}
}
/**
* @brief TLabel::loadconfig 加载配置
* @return void
* @Time 2021/7/14
*/
void TLabel::loadconfig()
{
	//获取字体
	if (Config::GetInstance()->loadConfig())
	{
		auto Group = Config::GetInstance()->getRootGroup();
		auto axisGroup = Group.getGroup("axis");
		QString unitfontstr = QString::fromStdString( axisGroup.getGroup("font").getValue("value"));
		QFont mfont = font();
		mfont.setFamily(unitfontstr);
		//mfont.setPixelSize(atoi(axisGroup.getGroup("axisSize").getValue("value").c_str()));
		setFont(mfont);
	}
}
/**
* @brief TLabel::setStyle 设置方向
* @param Axisstyle axisstyle
* @return void
* @Time 2021/7/29
*/
void TLabel::setStyle(Axisstyle axisstyle)
{
	mAxisstyle = axisstyle;
}
void TLabel::paintEvent(QPaintEvent* event)
{
	QPainter* painter=new QPainter(this);
	switch (mAxisstyle)
	{
	case Axisleft:
	case AxisRight:
		drawTitle(painter);
		break;
	case AxisTop:
	case AxisBottom:
	default:
		QLabel::paintEvent(event);
		break;
	}
	delete painter;
}
/**
* @brief TLabel::drawTitle 绘制label
* @param QPainter * painter
* @return void
* @Time 2021/7/29
*/
void TLabel::drawTitle(QPainter* painter)
{
	painter->save();
	QRectF r = QRectF(QPointF(0.0,0.0),QPointF(this->width(),this->height()));
	r.setRect(r.left(),r.bottom(),r.height(),r.width());
	painter->setFont(this->font());
	painter->setPen(this->palette().color(QPalette::Text));
	painter->translate(r.x(),r.y());
	QwtText title;
	title.setFont(this->font());
	title.setText(mtitle);
	int flag = title.renderFlags() & ~(Qt::AlignTop|Qt::AlignBottom|Qt::AlignVCenter);
	flag |= Qt::AlignVCenter;
	title.setRenderFlags(flag);
	QColor color = this->palette().windowText().color();
	QPen pen = painter->pen();
	pen.setColor(color);
	painter->setPen(pen);
	painter->setRenderHint(QPainter::Antialiasing, true);
	switch (mAxisstyle)
	{
	case Axisleft:
		painter->rotate(-90);
		break;
	case AxisRight:
		painter->rotate(90);
		break;
	}
	title.draw(painter,QRectF(0.0,0.0,r.width(),r.height()));
	painter->restore();
}
/**
* @brief TLabel::setColor 设置颜色
* @param QColor color
* @return void
* @Time 2021/7/29
*/
void TLabel::setColor(QColor color)
{
	QPalette palette=this->palette();
	palette.setColor(QPalette::WindowText,color);
	this->setPalette(palette);
}
/**
* @brief TLabel::setTextstr 传入label信息
* @param QString str
* @return void
* @Time 2021/7/29
*/
void TLabel::setTextstr(QString str)
{
	mtitle = str;
	switch (mAxisstyle)
	{
	case Axisleft:
	case AxisRight:
	{
		QwtText mtext;
		mtext.setFont(this->font());
		mtext.setText(str);
		QSizeF size = mtext.textSize();
		this->setMinimumWidth(size.height()+10);
		update();
	}
	break;
	case AxisTop:
	case AxisBottom:
	default:
		setText(str);
		break;
	}
}
#include "moc_TLabel.cpp"