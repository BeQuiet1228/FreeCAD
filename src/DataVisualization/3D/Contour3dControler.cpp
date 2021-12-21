#include"Contour3dControler.h"
#include"Contour3dActorPipeline.h"
DV3D::Contour3dControler::Contour3dControler():Controler()
{

}
DV3D::Contour3dControler::~Contour3dControler()
{

}
/**
* @time	2021/12/17
* @brief DV3D::Contour3dControler::setContourLeves 计算等值面时，设置等值面的等级
* @param const int & n
* @return void
*/
void DV3D::Contour3dControler::setContourLeves(const int& n)
{
	auto pipeline = getActorPipeline();
	std::shared_ptr<Contour3dActorPipline> contour3DPipline = std::dynamic_pointer_cast<Contour3dActorPipline>(pipeline);
	contour3DPipline->setContourSurfarCount(n);
}