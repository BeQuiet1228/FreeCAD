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


/**
* @time	2021/12/21
* @brief DV3D::Contour3dControler::getContourValues 获取数据
* @param std::vector<ContourValue> & data
* @return void
*/
void DV3D::Contour3dControler::getContourValues(std::vector<ContourValue>& data)
{
	auto pipeline = getActorPipeline();
	std::shared_ptr<Contour3dActorPipline> contour3dActorPipline = 
		std::dynamic_pointer_cast<Contour3dActorPipline>(pipeline);
	assert(contour3dActorPipline && "contour3dActorPipline is nullptr");
	data = contour3dActorPipline->getContourValues();
	return;
}


/**
* @time	2021/12/21
* @brief DV3D::Contour3dControler::setContourValues 设置等值面
* @param std::vector<ContourValue> & data
* @return void
*/
void DV3D::Contour3dControler::setContourValues(std::vector<ContourValue>& data)
{
	auto pipeline = getActorPipeline();
	std::shared_ptr<Contour3dActorPipline> contour3dActorPipline =
		std::dynamic_pointer_cast<Contour3dActorPipline>(pipeline);
	assert(contour3dActorPipline && "contour3dActorPipline is nullptr");
	contour3dActorPipline->setContourValues(data);
	return;
}

double* DV3D::Contour3dControler::getScalarRange()
{
	auto pipeline = getActorPipeline();
	std::shared_ptr<Contour3dActorPipline> contour3dActorPipline =
		std::dynamic_pointer_cast<Contour3dActorPipline>(pipeline);
	assert(contour3dActorPipline && "contour3dActorPipline is nullptr");
	return contour3dActorPipline->getScalarRang();
}
