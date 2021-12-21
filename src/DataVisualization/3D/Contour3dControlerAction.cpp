#include "Contour3dControlerAction.h"
#include "Contour3dControler.h"
#include "DataVisualization/realTimewidget.h"


void DV3D::ControlerContourSurface::active(std::shared_ptr<Controler> controler)
{
	std::shared_ptr<Contour3dControler> contour3dControler =
		std::dynamic_pointer_cast<Contour3dControler>(controler);
	assert(contour3dControler && "contour3dControler is nullptr");
	showWidget(controler);
}


void DV3D::ControlerContourSurface::showWidget(std::shared_ptr<Controler> controler)
{
	std::shared_ptr<Contour3dControler> contour3dControler =
		std::dynamic_pointer_cast<Contour3dControler>(controler);
	std::vector<ContourValue> values;
	contour3dControler->getContourValues(values);
	Contour3dControlerWidget* contour3dControlerWidget = new Contour3dControlerWidget();
	contour3dControlerWidget->setControler(controler);
	contour3dControlerWidget->setModal(true);
	contour3dControlerWidget->init(values);
	contour3dControlerWidget->resize(500, 300);
	contour3dControlerWidget->show();
}



DV3D::Contour3dControlerWidget::Contour3dControlerWidget(QWidget* parent/*=nullptr*/) :DV::realTimewidget(parent){}

DV3D::Contour3dControlerWidget::~Contour3dControlerWidget(){}
void DV3D::Contour3dControlerWidget::init(std::vector<ContourValue>& values)
{
	//数据转换
	std::list<double> valueFs;
	for (auto& i : values)
		valueFs.push_back(i);
	DV::realTimewidget::init(valueFs);
}

void DV3D::Contour3dControlerWidget::setControler(std::shared_ptr<Controler> controler)
{
	controlerptr = controler;
}

void DV3D::Contour3dControlerWidget::getContourValues(std::list<double>& values)
{
	std::shared_ptr<Contour3dControler> contour3dControler =
		std::dynamic_pointer_cast<Contour3dControler>(controlerptr);
	assert(contour3dControler && "contour3dControler is nullptr");
	//做数值转换
	std::vector<ContourValue> valueFs;
	valueFs.reserve(values.size());
	for (auto iter = values.begin(); iter != values.end(); iter++)
		valueFs.push_back(*iter);
	//转换完成
	contour3dControler->setContourValues(valueFs);
}

//#include "moc_Contour3dControlerAction.cpp"