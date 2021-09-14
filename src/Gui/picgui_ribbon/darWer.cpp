#include"PreCompiled.h"
#include"darWer.h"
#include<QBoxLayout>
#include"qstring.h"
darWer::darWer(QWidget* parent):/*QWidget(parent)*/QFrame(parent)
{
	initUI();
}
darWer::~darWer()
{

}
void darWer::initUI()
{
	mQBoxLayout = new QBoxLayout(QBoxLayout::Direction::BottomToTop,this);
	this->setLayout(mQBoxLayout);
	mQBoxLayout->setSpacing(5);
	this->setObjectName(
		QString::fromUtf8("MyDarWetWidget")
		);
	this->setStyleSheet(
		QString::fromUtf8(
			"QWidget#MyDarWetWidget{"
			"background-color:rgb(189,193,196,255);"
			"border:1px solid rgba(125,125,125,255);"
			"}"
		)
	);
}
void darWer::addButton(QToolButton* button)
{
	button->setParent(this);
	button->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
	button->setMinimumSize(24, 24);
	button->setAutoRaise(true);
	button->setIconSize(QSize(20, 20));
	button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
	button->setStyleSheet(
		QString::fromUtf8(
			//按钮正常样式
			"QToolButton{"
			//"border:2px solid rgba(125,125,125);"
			"}"
			//按钮按下的样式
			"QToolButton:pressed{"
			"border:2px solid rgba(1,1,1,255);"
			"}"
			//按钮悬停的样式
			"QToolButton:hover{"
			"border:2px solid rgba(125,125,125,255);"
			"}"
		)
	);
	mQBoxLayout->addWidget(button);
}
void darWer::setTitle(const QString& title)
{
	Title = title;
}
void darWer::setSize(QSize& size)
{
	mSize = size;
}
QList<QAction*> darWer::get_action_all()
{
	QList<QToolButton*> list_b = this->findChildren<QToolButton*>();
	QList<QAction*> list;
	for (int i = 0; i < list_b.count(); i++)
	{
		list.append(list_b.at(i)->actions());
	}
	return list;
}
#include"picgui_ribbon/moc_darWer.cpp"