#pragma once
#include "string"
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
	};
};