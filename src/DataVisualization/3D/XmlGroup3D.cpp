#include "XmlGroup3D.h"
#include "../C_encoding.h"
#include "sstream"
//DV3D::XmlData::ColorF DV3D::XmlData::getColors(std::string colorStr)
//{
//	ColorF colorf;
//	int len = colorStr.length();
//	unsigned int colorR = 0, colorG = 0, colorB = 0, colorA = 0;
//	if (len >= 8)
//	{
//		colorA = stoi(colorStr.substr(0, 2), 0, 16);
//		colorR = stoi(colorStr.substr(2, 2), 0, 16);
//		colorG = stoi(colorStr.substr(4, 2), 0, 16);
//		colorB = stoi(colorStr.substr(6, 2), 0, 16);
//		colorf.a = colorA / 255.0;
//		colorf.r = colorR / 255.0;
//		colorf.g = colorG / 255.0;
//		colorf.b = colorB / 255.0;
//	}
//	return colorf;
//}

//std::vector<DV3D::XmlData::ColorF> DV3D::XmlData::getColors(std::vector<float>& values, std::vector<QColor>& colors, int black /*= 255*/)
//{
//	std::vector<ColorF> newColors;
//	newColors.reserve(black);
//	newColors.push_back(getColors(colors[0]));
//	auto index = 0;
//	for (auto i = 1; i < black; ++i)
//	{
//		/*
//			获取值的范围
//		*/
//		//auto index = 0;
//		while (i > values[index++] * black);
//		index--;
//		auto nextcolor = getColors(colors[index]);
//		auto lastcolor = getColors(colors[index - 1]);
//		auto nextvalue = values[index] * black;
//		auto lastvalue = values[index - 1] * black;
//		/*
//			开始计算颜色值
//		*/
//		//获取比例
//		auto step = (i - lastvalue) / (nextvalue - lastvalue);
//		ColorF temp;
//		temp.r = (nextcolor.r - lastcolor.r) * step + lastcolor.r;
//		temp.g = (nextcolor.g - lastcolor.g) * step + lastcolor.g;
//		temp.b = (nextcolor.b - lastcolor.b) * step + lastcolor.b;
//		temp.a = (nextcolor.a - lastcolor.a) * step + lastcolor.a;
//		newColors.push_back(temp);
//	}
//	return newColors;
//}
//
//DV3D::XmlData::ColorF DV3D::XmlData::getColors(QColor color)
//{
//	ColorF colorF;
//	colorF.r = color.redF();
//	colorF.g = color.greenF();
//	colorF.b = color.blueF();
//	colorF.a = color.alphaF();
//	return colorF;
//}
/*
	重新封装
*/
DV3D::XmlData::XmlPointf3d::XmlPointf3d(std::vector<std::string> group)
	:
	xf(group,"x_value"),
	yf(group,"y_value"),
	zf(group,"z_value")
{
	push_back(&xf);
	push_back(&yf);
	push_back(&zf);
}

DV3D::XmlData::XmlPointf3d::~XmlPointf3d()
{

}

double DV3D::XmlData::XmlPointf3d::x()
{
	return xf.value;
}

double DV3D::XmlData::XmlPointf3d::y()
{
	return yf.value;
}

double DV3D::XmlData::XmlPointf3d::z()
{
	return zf.value;
}

void DV3D::XmlData::XmlPointf3d::setX(double x)
{
	xf = x;
}

void DV3D::XmlData::XmlPointf3d::setY(double y)
{
	yf = y;
}

void DV3D::XmlData::XmlPointf3d::setZ(double z)
{
	zf = z;
}

void DV3D::XmlData::XmlPointf3d::addGroup(std::string val)
{
	xf.addGroup(val);
	yf.addGroup(val);
	zf.addGroup(val);
}

DV3D::XmlData::ControlerXml::ControlerXml(std::vector<std::string> group)
	:
alpha(group,"value"),
clipEnable(group,"value"),
gridEnable(group,"value"),
centerPoint(group),
normalPoint(group)
{
	alpha.addGroup("alpha");
	clipEnable.addGroup("clipEnable");
	gridEnable.addGroup("gridEnable");
	centerPoint.addGroup("centerPoint");
	normalPoint.addGroup("normalPoint");

	push_back(&alpha);
	push_back(&clipEnable);
	push_back(&gridEnable);
	push_back(&centerPoint);
	push_back(&normalPoint);
}


DV3D::XmlData::Struct3dXml::Struct3dXml()
	:
	Rotation({"struct3d","rotation"},"value"),
	color({"struct3d","color"},"value"),
	controlerXml({"struct","controler"})
{
	push_back(&Rotation);
	push_back(&color);
	push_back(&controlerXml);
}

DV3D::XmlData::Contour3dXml::Contour3dXml()
	: 
	Rotation({"contour3d","rotation"},"value"),
	colorbar({"contour3d","valueNumber"}, "value"),
	controlerXml({"contour3d","controler"})
{
	push_back(&Rotation);
	push_back(&colorbar);
	push_back(&controlerXml);
}

DV3D::XmlData::Particle3dXml::Particle3dXml()
	:
	particleSize({ "particle3d","particleSize"},"value"),
	particleColor({"particle3d","particleColor"},"value"),
	controlerXml({"particle3d","controler"})
{
	push_back(&particleSize);
	push_back(&particleColor);
	push_back(&controlerXml);
}

DV3D::XmlData::Vector3dXml::Vector3dXml()
	:
	XorRGridInc({ "vector3d" ,"XorRGridInc" }, "value"),
	YorThetaGridInc({ "vector3d","YorThetaGridInc" }, "value"),
	ZGridInc({ "vector3d","ZGridInc" }, "value"),
	colorBar({ "vector3d","valueNumber" }, "value"),
	controlerXml({ "vector3d" ,"controler"})
{
	push_back(&XorRGridInc);
	push_back(&YorThetaGridInc);
	push_back(&ZGridInc);
	push_back(&colorBar);
	push_back(&controlerXml);
}
