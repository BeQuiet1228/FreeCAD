#pragma once
#include "string"
#include "vector"
namespace DV3D
{
	/*
		统一的读取xml配置的类,继承必须重写loadConfig
	*/
	class UnifyXmlConfig3D
	{
	public :
		UnifyXmlConfig3D()=default;
		~UnifyXmlConfig3D() = default;
	protected:
		/*
			读取xml中的配置
		*/
		virtual void loadConfig() = 0;
		/*
			一些xml信息转换成数据的方法
		*/
		struct ColorF {
			double r;
			double g;
			double b;
			double a;
		};
		ColorF getColors(std::string colorStr);
		/*
			创建255个颜色过度表
		*/
		std::vector<ColorF> getColors(std::vector<float>&,std::vector<ColorF>&,int black=255);
	};
};