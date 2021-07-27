#include"CombAxis.h"
#include<QGridLayout>
CombAxis::CombAxis(QWidget* parent):QWidget(parent)
{
	mAxis = new Axis(this);
	mtlabel = new TLabel(this);
	mtlabel->setAlignment(Qt::AlignHCenter|Qt::AlignVCenter);
	layout = new QGridLayout;
	this->setLayout(layout);
	layout->setSpacing(0);
	layout->setMargin(0);
}
CombAxis::~CombAxis()
{

}
void CombAxis::setLeft(){
	layout->addWidget(mtlabel,0,0,1,1);
	layout->addWidget(mAxis,0,1,1,1);
	mtlabel->setText("123");
}
void CombAxis::setRight(){
	layout->addWidget(mAxis,0,0,1,1);
	layout->addWidget(mtlabel,0,1,1,1);
	mtlabel->setText("123");
}
void CombAxis::setTop(){
	layout->addWidget(mtlabel,0,0,1,1);
	layout->addWidget(mAxis,1,0,1,1);
	mtlabel->setText("123");
}
void CombAxis::setBottom(){
	layout->addWidget(mAxis,0,0,1,1);
	layout->addWidget(mtlabel,1,0,1,1);
	mtlabel->setText("123");
}
void CombAxis::setAxisRange(float min, float max)
{
	mAxis->setAxisRange(min,max);
}
void CombAxis::_update()
{
	mAxis->_update();
}
void CombAxis::setAxisText(QString str)
{
	mtlabel->setText(str);
}
void CombAxis::setAxixStyle(Axisstyle mAxisstyle)
{
	mAxis->setAxixStyle(mAxisstyle);
	mtlabel->setStyle(mAxisstyle);
	setView(mAxisstyle);
}
void CombAxis::SetAxisNumber(unsigned int level)
{
	mAxis->SetAxisNumber(level);
}
void CombAxis::setColorBarEnabled(bool istrue)
{
	mAxis->setColorBarEnabled(istrue);
}
void CombAxis::setMargin(float margin)
{
	mAxis->setMargin(margin);
}
void CombAxis::setSpacing(float spacing)
{
	mAxis->setSpacing(spacing);
}
void CombAxis::setBorderDist(float start, float end)
{
	mAxis->setBorderDist(start,end);
}
void CombAxis::loadconfig()
{
	mAxis->loadconfig();
	mtlabel->loadconfig();
}
//用于组合控件的拼接
void CombAxis::setView(Axisstyle mAxisstyle)
{
	switch (mAxisstyle)
	{
	case Axisleft:
		setLeft();break;
	case AxisRight:
		setRight();break;
	case AxisTop:
		setTop(); break;
	case AxisBottom:
		setBottom(); break;
	}
}
#include"moc_CombAxis.cpp"