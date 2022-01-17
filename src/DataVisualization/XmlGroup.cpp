#include"XmlGroup.h"
#include "C_encoding.h"
#include "sstream"
#include "cassert"
#include "CustomConfig.h"
namespace DV
{
	namespace XmlData
	{
		ConfigGroup getGroup(std::vector<std::string> value);
		/*结构体相关的参数*/

		std::vector<std::string> strlist{
		"CONDUCTORNEW",
		"DIELECTIRANDCONDUCTANCE",
		"DIOLECTRIC",
		"DRIVER",
		"FOIL",
		"FREESPACE",
		"INDUCTOR",
		"PERFECTCONDUCTOR",
		"PERMEABILITY",
		"PORT",
		"VACUO"
		"CONDUCTORNEWLINE",
		"DIELECTIRANDCONDUCTANCELINE",
		"DIOLECTRICLINE",
		"FOILLINE",
		"FREESPACELINE",
		"PERFECTCONDUCTORLINE",
		"PERMEABILITYLINE",
		"VACUOLINE" };
	}
}
DV::ConfigGroup DV::XmlData::getGroup(std::vector<std::string> value)
{
	DV::Config::GetInstance()->loadConfig();
	auto group = DV::Config::GetInstance()->getRootGroup();
	for (auto iter = value.begin(); iter != value.end(); iter++)
	{
		group = group.getGroup(*iter);
	}
	return group;
}
/*
	重新封装
*/
DV::XmlData::XmlObject::XmlObject(std::vector<std::string> group, std::string valueKey)
{
	groupStr = group;
	valKey = valueKey;
}

DV::XmlData::XmlObject::~XmlObject()
{

}
void DV::XmlData::XmlObject::loadXml()
{
	valStr = getGroup(groupStr).getValue(valKey);
}
void DV::XmlData::XmlObject::saveXml()
{
	getGroup(groupStr).setSetting(valKey, valStr);
	Config::GetInstance()->saveFile();
}

std::vector<std::string> DV::XmlData::XmlObject::getGroupStr()
{
	return groupStr;
}

void DV::XmlData::XmlObject::setValstr(std::string val)
{
	valStr = val;
}

void DV::XmlData::XmlObject::setValKey(std::string key)
{
	valKey = key;
}

std::string DV::XmlData::XmlObject::getValStr()
{
	return valStr;
}

std::string DV::XmlData::XmlObject::getValKey()
{
	return valKey;
}

void DV::XmlData::XmlObject::setGroup(std::vector<std::string> group)
{
	groupStr = group;
}

void DV::XmlData::XmlObject::addGroup(std::string val)
{
	groupStr.push_back(val);
}

DV::XmlData::XmlObject& DV::XmlData::XmlObject::operator=(const XmlObject& that)
{
	this->groupStr = that.groupStr;
	this->valKey = that.valKey;
	this->valStr = that.valStr;
	return  *this;
}

DV::XmlData::XmlInt& DV::XmlData::XmlInt::operator=(const XmlInt& that)
{
	this->value = that.value;
	return *this;
}
void DV::XmlData::XmlInt::operator=(const int n)
{
	this->value = n;
	setValstr(std::to_string(value));
}

void DV::XmlData::XmlInt::loadXml()
{
	XmlObject::loadXml();
	this->value = atoi(getValStr().c_str());
}
void DV::XmlData::XmlColor::operator=(const QColor& color)
{
	this->value = color;
	r = value.redF();
	g = value.greenF();
	b = value.blueF();
	a = value.alphaF();
	setValstr(QColorToQstring(value).toStdString());
}

DV::XmlData::XmlColor& DV::XmlData::XmlColor::operator=(XmlColor& that)
{
	this->value = that.value;
	r = that.r;
	g = that.g;
	b = that.b;
	a = that.a;
	setValstr(that.getValStr());
	setGroup(that.getGroupStr());
	setValKey(that.getValKey());
	return *this;
}

void DV::XmlData::XmlColor::loadXml()
{
	XmlObject::loadXml();
	value = StringToQColor(getValStr());
}

void DV::XmlData::XmlFloat::operator=(const float& f)
{
	this->value = f;
	setValstr(std::to_string(f));
}

void DV::XmlData::XmlFloat::loadXml()
{
	XmlObject::loadXml();
	value = atof(getValStr().c_str());

}

DV::XmlData::AxisXml::AxisXml()
	:
	axisSize({ "axis","axisSize" }, "value"),
	axisColor({ "axis","axisColor" }, "value"),
	axisvalColor({ "axis","axisvalColor" }, "value"),
	axisvalSize({ "axis","axisvalSize" }, "value"),
	infoShow({ "axis","infoShow" }, "value"),
	font({ "axis","font" }, "value")
{
	push_back(&axisSize);
	push_back(&axisColor);
	push_back(&axisvalColor);
	push_back(&axisvalSize);
	push_back(&infoShow);
	push_back(&font);
}

DV::XmlData::AxisXml::~AxisXml()
{

}

void DV::XmlData::XmlString::operator=(const QString& s)
{
	value = s;
	setValstr(s.toStdString());
}

void DV::XmlData::XmlString::operator=(const std::string& s)
{
	value = QString::fromStdString(s);
	setValstr(s);
}

void DV::XmlData::XmlString::loadXml()
{
	XmlObject::loadXml();
	value = QString::fromStdString(getValStr());
}

DV::XmlData::XmlStructObj::XmlStructObj()
{

}

DV::XmlData::XmlStructObj::~XmlStructObj()
{
	memberList.clear();
}

void DV::XmlData::XmlStructObj::saveXml()
{
	for (auto iter = memberList.begin(); iter != memberList.end(); iter++)
		(*iter)->saveXml();
	for (auto iter = memberLists.begin(); iter != memberLists.end(); iter++)
		(*iter)->saveXml();
}

void DV::XmlData::XmlStructObj::loadXml()
{
	for (auto iter = memberList.begin(); iter != memberList.end(); iter++)
		(*iter)->loadXml();
	for (auto iter = memberLists.begin(); iter != memberLists.end(); iter++)
		(*iter)->loadXml();
}

void DV::XmlData::XmlStructObj::push_back(XmlObject* val)
{
	memberList.push_back(val);
}

void DV::XmlData::XmlStructObj::push_back(XmlStructObj* obj)
{
	memberLists.push_back(obj);
}

DV::XmlData::VectorXml::VectorXml()
	:
	vectorsize({ "vector","vectorsize" }, "value"),
	vectorColor({ "vector","vectorColor" }, "value"),
	AlisAttitude({ "vector","AlisAttitude" }, "isAlis"),
	disMode({ "vector","disMode" }, "value")
{
	push_back(&vectorsize);
	push_back(&vectorColor);
	push_back(&AlisAttitude);
	push_back(&disMode);
}

DV::XmlData::VectorXml::~VectorXml()
{

}
DV::XmlData::ContourXml::ContourXml()
	:lineMapColors({ "contour","lineMapColors" }, "value"),
	AlisAttitude({ "contour","AlisAttitude" }, "isAlis"),
	valueStyle({ "contour","valueStyle" }, "value"),
	colorBar({ "contour","lineMapColorval" }, "valueNumber")
{
	push_back(&lineMapColors);
	push_back(&AlisAttitude);
	push_back(&colorBar);
}

DV::XmlData::ContourXml::~ContourXml()
{

}
DV::XmlData::XmlVectorFloat::~XmlVectorFloat()
{

}

void DV::XmlData::XmlVectorFloat::loadXml(int count)
{
	std::stringstream is;
	for (auto index = 0; index < count; ++index)
	{
		is << "level_" << index;
		auto grop = getGroupStr();
		grop.push_back(is.str());
		XmlFloat tempFloat(grop, getValKey());
		tempFloat.loadXml();
		values.push_back(tempFloat);
		is.str("");
	}
}


void DV::XmlData::XmlVectorFloat::saveXml()
{
	std::stringstream os;
	for (auto index = 0; index < values.size(); ++index)
	{
		os << "level_" << index;
		auto group = getGroupStr();
		group.push_back(os.str());
		values[index].setGroup(group);
		values[index].setValKey(getValKey());
		values[index].saveXml();
		os.str("");
	}
}

DV::XmlData::XmlFloat& DV::XmlData::XmlVectorFloat::operator[](int index)
{
	return values[index];
}

void DV::XmlData::XmlVectorFloat::operator=(std::vector<float> val)
{
	for (auto iter = val.begin(); iter != val.end(); iter++)
		push_back(*iter);
}

void DV::XmlData::XmlVectorFloat::push_back(float f)
{
	XmlFloat xmlf(getGroupStr(), getValKey());
	xmlf = f;
	push_back(xmlf);
}

int DV::XmlData::XmlVectorFloat::Size()
{
	return values.size();
}

std::vector<float> DV::XmlData::XmlVectorFloat::toVector()
{
	std::vector<float> fs;
	for (auto iter = values.begin(); iter != values.end(); iter++)
		fs.push_back(iter->value);
	return fs;
}

void DV::XmlData::XmlVectorFloat::push_back(XmlFloat f)
{
	values.push_back(f);
}

DV::XmlData::XmlColorBar::XmlColorBar(std::vector<std::string> group, std::string valKey)
	:XmlObject(group, valKey),
	values(group, "value"),
	colors(group, "color")
{

}

void DV::XmlData::XmlColorBar::loadXml()
{
	XmlObject::loadXml();
	auto count = atoi(getValStr().c_str());
	values.loadXml(count);
	colors.loadXml(count);
}

void DV::XmlData::XmlColorBar::saveXml()
{
	//XmlObject::saveXml();
	values.saveXml();
	colors.saveXml();
	int count = values.Size();
	setValstr(std::to_string(count));
	XmlObject::saveXml();
}

DV::XmlData::XmlVectorColor::~XmlVectorColor()
{

}

void DV::XmlData::XmlVectorColor::loadXml(int count)
{
	std::stringstream is;
	for (auto index = 0; index < count; ++index)
	{
		is << "level_" << index;
		auto group = getGroupStr();
		group.push_back(is.str());
		XmlColor tempColor(group, getValKey());
		tempColor.loadXml();
		values.push_back(tempColor);
		is.str("");
	}
}

void DV::XmlData::XmlVectorColor::saveXml()
{
	std::stringstream os;
	for (auto index = 0; index < values.size(); ++index)
	{
		os << "level_" << index;
		auto group = getGroupStr();
		group.push_back(os.str());
		values[index].setGroup(group);
		values[index].setValKey(getValKey());
		values[index].saveXml();
		os.str("");
	}
}

DV::XmlData::XmlColor& DV::XmlData::XmlVectorColor::operator[](int index)
{
	return values[index];
}

void DV::XmlData::XmlVectorColor::push_back(QColor color)
{
	XmlColor xmlColor(getGroupStr(), getValKey());
	xmlColor = color;
	push_back(xmlColor);
}

int DV::XmlData::XmlVectorColor::Size()
{
	return values.size();
}

std::vector<QColor> DV::XmlData::XmlVectorColor::toVector()
{
	std::vector<QColor> cols;
	for (auto iter = values.begin(); iter != values.end(); iter++)
		cols.push_back(iter->value);
	return cols;
}

void DV::XmlData::XmlVectorColor::operator=(std::vector<QColor> val)
{
	for (auto iter = val.begin(); iter != val.end(); iter++)
		push_back(*iter);
}

void DV::XmlData::XmlVectorColor::push_back(XmlColor color)
{
	values.push_back(color);
}

DV::XmlData::ParticleXml::ParticleXml()
	:
	size({ "particle","size" }, "value"),
	color({ "particle","color" }, "value"),
	AlisAttitude({ "particle" ,"AlisAttitude" }, "isAlis")
{
	push_back(&size);
	push_back(&color);
	push_back(&AlisAttitude);
}

DV::XmlData::ParticleXml::~ParticleXml()
{

}

DV::XmlData::StructXml::StructXml()
	:AlisAttitude({ "struct","AlisAttitude" }, "value")
{

	push_back(&AlisAttitude);
}

DV::XmlData::StructXml::~StructXml()
{

}

void DV::XmlData::StructXml::loadXml()
{
	XmlStructObj::loadXml();
	/*
		结构图属性数据先暂时这样chuli
	*/
	proPerty.clear();
	for (auto iter= strlist.begin();iter!=strlist.end();iter++)
	{
		XmlColor color({"struct",*iter},"value");
		color.loadXml();
		proPerty.insert(std::pair<std::string, QColor>(*iter,color.value));
	}
}

void DV::XmlData::StructXml::saveXml()
{
	XmlStructObj::loadXml();
	for (auto iter=proPerty.begin();iter!=proPerty.end();iter++)
	{
		XmlColor color({"struct",iter->first}, "value");
		color = iter->second;
		color.saveXml();
	}
}