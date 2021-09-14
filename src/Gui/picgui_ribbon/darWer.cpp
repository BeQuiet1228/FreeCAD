#include"PreCompiled.h"
#include"darWer.h"
#include<QBoxLayout>
darWer::darWer(QWidget* parent):QWidget(parent)
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
}
void darWer::addButton(QToolButton* button)
{
	button->setParent(this);
	button->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
	button->setMinimumSize(24, 24);
	button->setAutoRaise(true);
	button->setIconSize(QSize(20, 20));
	button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
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