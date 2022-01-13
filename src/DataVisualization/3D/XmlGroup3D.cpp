#include "XmlGroup3D.h"
#include "../C_encoding.h"
#include "sstream"
using namespace DV::XmlData;

DV3D::XmlData::ColorF DV3D::XmlData::getColors(std::string colorStr)
{
	ColorF colorf;
	int len = colorStr.length();
	unsigned int colorR = 0, colorG = 0, colorB = 0, colorA = 0;
	if (len >= 8)
	{
		colorA = stoi(colorStr.substr(0, 2), 0, 16);
		colorR = stoi(colorStr.substr(2, 2), 0, 16);
		colorG = stoi(colorStr.substr(4, 2), 0, 16);
		colorB = stoi(colorStr.substr(6, 2), 0, 16);
		colorf.a = colorA / 255.0;
		colorf.r = colorR / 255.0;
		colorf.g = colorG / 255.0;
		colorf.b = colorB / 255.0;
	}
	return colorf;
}

std::vector<DV3D::XmlData::ColorF> DV3D::XmlData::getColors(std::vector<float>& values, std::vector<QColor>& colors, int black /*= 255*/)
{
	std::vector<ColorF> newColors;
	newColors.reserve(black);
	newColors.push_back(getColors(colors[0]));
	auto index = 0;
	for (auto i = 1; i < black; ++i)
	{
		/*
			获取值的范围
		*/
		//auto index = 0;
		while (i > values[index++] * black);
		index--;
		auto nextcolor = getColors(colors[index]);
		auto lastcolor = getColors(colors[index - 1]);
		auto nextvalue = values[index] * black;
		auto lastvalue = values[index - 1] * black;
		/*
			开始计算颜色值
		*/
		//获取比例
		auto step = (i - lastvalue) / (nextvalue - lastvalue);
		ColorF temp;
		temp.r = (nextcolor.r - lastcolor.r) * step + lastcolor.r;
		temp.g = (nextcolor.g - lastcolor.g) * step + lastcolor.g;
		temp.b = (nextcolor.b - lastcolor.b) * step + lastcolor.b;
		temp.a = (nextcolor.a - lastcolor.a) * step + lastcolor.a;
		newColors.push_back(temp);
	}
	return newColors;
}

DV3D::XmlData::ColorF DV3D::XmlData::getColors(QColor color)
{
	ColorF colorF;
	colorF.r = color.redF();
	colorF.g = color.greenF();
	colorF.b = color.blueF();
	colorF.a = color.alphaF();
	return colorF;
}
void DV3D::XmlData::loadXmlInfo(Struct3dXml& val)
{
	val.color = DV::StringToQColor(getGroup({ "struct3d","color" }).getValue("value"));
	loadXmlInfo(val.controlerXml, "struct3d");
}

void DV3D::XmlData::saveXmlInfo(Vector3dXml& val)
{
	getGroup({ "vector3d","XorRGridInc" }).setSetting("valMax", std::to_string(val.XorRGridInc));
	getGroup({ "vector3d","YorThetaGridInc" }).setSetting("valMax", std::to_string(val.YorThetaGridInc));
	getGroup({ "vector3d","ZGridInc" }).setSetting("valMax", std::to_string(val.ZGridInc));
	std::stringstream os;
	for (auto index = 0; index < val.colorBar.values.size(); ++index)
	{
		os.str("");
		os << "level_" << index;
		getGroup({ "vector3d","valueNumber",os.str() }).setSetting("value", std::to_string(val.colorBar.values[index]));
		getGroup({ "vector3d","valueNumber",os.str() }).setSetting("color", DV::QColorToQstring(val.colorBar.colors[index]).toStdString());
	}
	DV::Config::GetInstance()->saveFile();
}

void DV3D::XmlData::saveXmlInfo(Particle3dXml& val)
{
	getGroup({ "particle3d", "particleColor" }).setSetting("value", std::to_string(val.particleSize));
	getGroup({ "particle3d", "particleColor" }).setSetting("value", DV::QColorToQstring(val.particleColor).toStdString());
	DV::Config::GetInstance()->saveFile();
}

void DV3D::XmlData::loadXmlInfo(Vector3dXml& val)
{
	val.XorRGridInc = atoi(getGroup({ "vector3d","XorRGridInc" }).getValue("valMax").c_str());
	val.YorThetaGridInc = atoi(getGroup({ "vector3d","YorThetaGridInc" }).getValue("valMax").c_str());
	val.ZGridInc = atoi(getGroup({ "vector3d","ZGridInc" }).getValue("valMax").c_str());
	int size = atoi(getGroup({ "vector3d","valueNumber" }).getValue("value").c_str());
	std::stringstream is;
	for (auto index = 0; index < size; ++index)
	{
		is.str("");
		is << "level_" << index;
		val.colorBar.values.push_back(atof(getGroup({ "vector3d","valueNumber",is.str() }).getValue("value").c_str()));;
		val.colorBar.colors.push_back(DV::StringToQColor(getGroup({ "vector3d","valueNumber",is.str() }).getValue("color")));
	}
	loadXmlInfo(val.controlerXml, "vector3d");
}

void DV3D::XmlData::saveXmlInfo(Contour3dXml& val)
{
	getGroup({ "contour3d","valueNumber" }).setSetting("value", std::to_string(val.values.size()));
	std::stringstream os;
	for (auto index = 0; index < val.values.size(); ++index)
	{
		os.str("");
		os << "level_" << index;
		getGroup({ "contour3d","valueNumber",os.str() }).setSetting("value", std::to_string(val.values[index]));
		getGroup({ "contour3d","valueNumber",os.str() }).setSetting("color", DV::QColorToQstring(val.colors[index]).toStdString());
	}
	DV::Config::GetInstance()->saveFile();
}

void DV3D::XmlData::loadXmlInfo(Particle3dXml& val)
{
	val.particleColor = DV::StringToQColor(getGroup({ "particle3d", "particleColor" }).getValue("value"));
	val.particleSize = atof(getGroup({ "particle3d", "particleSize" }).getValue("value").c_str());
	loadXmlInfo(val.controlerXml, "particle3d");
}

void DV3D::XmlData::saveXmlInfo(Struct3dXml& val)
{
	getGroup({ "struct3d","color" }).setSetting("value", DV::QColorToQstring(val.color).toStdString());
	DV::Config::GetInstance()->saveFile();
}

void DV3D::XmlData::loadXmlInfo(Contour3dXml& val)
{
	int size = atoi(getGroup({ "contour3d" ,"valueNumber" }).getValue("value").c_str());
	val.colors.reserve(size);
	val.values.reserve(size);
	std::stringstream is;
	for (auto index = 0; index < size; ++index)
	{
		is.str("");
		is << "level_" << index;
		val.values.push_back(atof(getGroup({ "contour3d","valueNumber",is.str() }).getValue("value").c_str()));
		val.colors.push_back(DV::StringToQColor(getGroup({ "contour3d","valueNumber",is.str() }).getValue("color")));
	}
	loadXmlInfo(val.controlerXml, "contour3d");
}
void DV3D::XmlData::loadXmlInfo(ControlerXml& val, std::string parentGroup)
{
	//struct ControlerXml
	//	{
	//		float alpha;//0~1
	//		bool clipEnable;//
	//		QVector3D centerPoint
	//		QVector3D normalPoint;
	//	}
	val.alpha = atof(getGroup({ parentGroup,"controler","alpha" }).getValue("value").c_str());
	val.clipEnable = atoi(getGroup({ parentGroup,"controler","clipEnable" }).getValue("value").c_str());
	val.gridEnable= atoi(getGroup({ parentGroup,"controler","gridEnable" }).getValue("value").c_str());
	val.centerPoint.setX(atof(getGroup({ parentGroup,"controler","centerPoint" }).getValue("x_value").c_str()));
	val.centerPoint.setY(atof(getGroup({ parentGroup,"controler","centerPoint" }).getValue("y_value").c_str()));
	val.centerPoint.setZ(atof(getGroup({ parentGroup,"controler","centerPoint" }).getValue("z_value").c_str()));
	val.normalPoint.setX(atof(getGroup({ parentGroup,"controler","normalPoint" }).getValue("x_value").c_str()));
	val.normalPoint.setY(atof(getGroup({ parentGroup,"controler","normalPoint" }).getValue("y_value").c_str()));
	val.normalPoint.setZ(atof(getGroup({ parentGroup,"controler","normalPoint" }).getValue("z_value").c_str()));
}
void DV3D::XmlData::saveXmlInfo(ControlerXml& val, std::string parentGroup)
{
	getGroup({ parentGroup,"controler","alpha" }).setSetting("value", std::to_string(val.alpha));
	getGroup({ parentGroup,"controler","clipEnable" }).setSetting("value", std::to_string(val.clipEnable));
	getGroup({ parentGroup,"controler","gridEnable" }).setSetting("value", std::to_string(val.gridEnable));
	getGroup({ parentGroup,"controler","centerPoint" }).setSetting("x_value", std::to_string(val.centerPoint.x()));
	getGroup({ parentGroup,"controler","centerPoint" }).setSetting("y_value", std::to_string(val.centerPoint.y()));
	getGroup({ parentGroup,"controler","centerPoint" }).setSetting("z_value", std::to_string(val.centerPoint.z()));
	getGroup({ parentGroup,"controler","normalPoint" }).setSetting("x_value", std::to_string(val.normalPoint.x()));
	getGroup({ parentGroup,"controler","normalPoint" }).setSetting("y_value", std::to_string(val.normalPoint.y()));
	getGroup({ parentGroup,"controler","normalPoint" }).setSetting("z_value", std::to_string(val.normalPoint.z()));
	DV::Config::GetInstance()->saveFile();
}