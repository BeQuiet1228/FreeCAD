#include "Contour3dControlerWidget.h"
#include "Contour3dControler.h"

DV3D::Contour3dControlerWidget::Contour3dControlerWidget(QWidget* parent /*= nullptr*/):DV::realTimewidget(parent)
{
	connect(this,SIGNAL(sendConfigLevels(std::list<double>&)),
		this,SLOT(slotGetContourValues(std::list<double>&)));
}

DV3D::Contour3dControlerWidget::~Contour3dControlerWidget()
{

}

void DV3D::Contour3dControlerWidget::init(std::vector<ContourValue>& values)
{
	//数据转换
	std::list<double> valueFs;
	for (auto& i : values)
		valueFs.push_back(i);
	DV::realTimewidget::loadConfigLevels(valueFs);
}

void DV3D::Contour3dControlerWidget::setControler(std::shared_ptr<Controler> controler)
{
	controlerptr = controler;
}

void DV3D::Contour3dControlerWidget::slotGetContourValues(std::list<double>& values)
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
//#include "moc_Contour3dControlerWidget.cpp"
#include "../moc_realTimewidget.cpp"