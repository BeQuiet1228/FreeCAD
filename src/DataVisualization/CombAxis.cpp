#include"CombAxis.h"
#include<QGridLayout>
CombAxis::CombAxis(Axisstyle astyle,QWidget* parent) :QWidget(parent)
{
	initUI(astyle);
}
CombAxis::~CombAxis()
{

}
void CombAxis::initUI(Axisstyle astyle)
{
	layout = new QGridLayout;
	this->setLayout(layout);
	layout->setSpacing(0);
	//
	mAxis = new Axis(this);
	mtlabel =new TLabel(this);
	switch (astyle)
	{
	case Axisleft:
		setLeft();
	break;
	case AxisRight:
		setRight();
	break;
	case AxisBottom:
		setBottom();
	break;
	case AxisTop:
		setTop();
	break;
	}
}

void CombAxis::setLeft(){
	layout->addWidget(mtlabel,0,0,1,1);
	layout->addWidget(mAxis,0,1,1,1);

}
void CombAxis::setRight(){
	layout->addWidget(mAxis,0,0,1,1);
	layout->addWidget(mtlabel,0,1,1,1);
}
void CombAxis::setTop(){
	layout->addWidget(mtlabel,0,0,1,1);
	layout->addWidget(mAxis,1,0,1,1);
}
void CombAxis::setBottom(){
	layout->addWidget(mAxis,0,0,1,1);
	layout->addWidget(mtlabel,1,0,1,1);
}
#include"moc_CombAxis.cpp"