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
	layout = new QBoxLayout(QBoxLayout::Direction::BottomToTop,this);
	layout->setSpacing(2);
	this->setLayout(layout);
}
void darWer::insertbutton(std::list<QAction*>&)
{

}
#include"picgui_ribbon/moc_darWer.cpp"