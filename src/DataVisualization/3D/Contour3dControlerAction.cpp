#include "Contour3dControlerAction.h"
#include "Contour3dControler.h"
#include "Contour3dControlerWidget.h"


void DV3D::ControlerContourSurface::active(std::shared_ptr<Controler> controler)
{
	std::shared_ptr<Contour3dControler> contour3dControler =
		std::dynamic_pointer_cast<Contour3dControler>(controler);
	assert(contour3dControler && "contour3dControler is nullptr");
	//弹窗,弹出窗口
	showWidget(controler);

}


/**
* @brief DV3D::ControlerContourSurface::showWidget 显示窗口
* @param std::shared_ptr<Controler> controler
* @return void
* @time	2021/12/21
*/
bool  DV3D::ControlerContourSurface::showWidget(std::shared_ptr<Controler> controler)
{
	std::shared_ptr<Contour3dControler> contour3dControler =
		std::dynamic_pointer_cast<Contour3dControler>(controler);
	std::vector<ContourValue> values;
	if (nullptr == contour3dControler)
		return false;
	contour3dControler->getContourValues(values);
	Contour3dControlerWidget* contour3dControlerWidget = new Contour3dControlerWidget();
	contour3dControlerWidget->setModal(true);
	contour3dControlerWidget->setControler(controler);
	contour3dControlerWidget->init(values);
	contour3dControlerWidget->resize(500, 300);
	contour3dControlerWidget->show();
	return true;
}
void DV3D::ControlerContourSurface::initState(std::shared_ptr<Controler> controler)
{
	on();
}