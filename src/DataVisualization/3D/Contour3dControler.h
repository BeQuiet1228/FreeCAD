#pragma once
#include"controler.h"
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
	};
};
