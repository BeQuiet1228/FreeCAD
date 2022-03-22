#pragma once
#include"controler.h"
#include "Contour3dActorPipeline.h"
namespace DV3D
{
	class Contour3dControler :public Controler
	{
	public :
		Contour3dControler();
		~Contour3dControler();
	public:
		//设置等值面等级
		void setContourLeves(const int& n);
		void getContourValues(std::vector<ContourValue>& data);
		void setContourValues(std::vector<ContourValue>& data);
		double* getScalarRange();
	};
};
