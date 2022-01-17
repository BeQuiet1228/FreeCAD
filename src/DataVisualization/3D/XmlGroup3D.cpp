#include "XmlGroup3D.h"
#include "../C_encoding.h"
#include "sstream"
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
	controlerXml({"struct3d","controler"})
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

std::vector<QColor> DV3D::XmlData::getColors(std::vector<float>& values, std::vector<QColor>& colors, int black)
{
	std::vector<QColor> newColors;
	newColors.reserve(black);
	newColors.push_back(colors[0]);
	auto index = 0;
	for (auto i = 1; i < black; ++i)
	{
		/*
			获取值的范围
		*/
		//auto index = 0;
		while (i > values[index++] * black);
		index--;
		auto nextcolor = colors[index];
		auto lastcolor = colors[index - 1];
		auto nextvalue = values[index] * black;
		auto lastvalue = values[index - 1] * black;
		/*
			开始计算颜色值
		*/
		//获取比例
		auto step = (i - lastvalue) / (nextvalue - lastvalue);
		QColor temp;
		temp.setAlphaF((nextcolor.alphaF() - lastcolor.alphaF()) * step + lastcolor.alphaF());
		temp.setRedF((nextcolor.redF() - lastcolor.redF()) * step + lastcolor.redF());
		temp.setGreenF((nextcolor.greenF() - lastcolor.greenF()) * step + lastcolor.greenF());
		temp.setBlueF((nextcolor.blueF() - lastcolor.blueF()) * step + lastcolor.blueF());
		newColors.push_back(temp);
	}
	return newColors;
}