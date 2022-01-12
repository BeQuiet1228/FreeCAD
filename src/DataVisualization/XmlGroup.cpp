#include"XmlGroup.h"
#include "C_encoding.h"
#include "sstream"
DV::ConfigGroup DV::XmlGroup::getGroup(std::vector<std::string> value)
{
	DV::Config::GetInstance()->loadConfig();
	auto group = DV::Config::GetInstance()->getRootGroup();
	for (auto iter = value.begin(); iter != value.end(); iter++)
	{
		group = group.getGroup(*iter);
	}
	return group;
}

void DV::AxisXmlGroup::saveXmlInfo(AxisXml& value)
{
	std::string axisSizeStr = std::to_string(value.axisSize);
	getGroup({ "axis", "axisSize" }).setSetting("value", axisSizeStr);

	std::string axisColor = QColorToQstring(value.axisColor).toStdString();
	getGroup({ "axis", "axisColor" }).setSetting("value", axisColor);

	std::string axisvalColor = QColorToQstring(value.axisvalColor).toStdString();
	getGroup({ "axis", "axisvalColor" }).setSetting("value", axisvalColor);

	std::string axisvalSize = std::to_string(value.axisvalSize);
	getGroup({ "axis", "axisvalSize" }).setSetting("value", axisvalSize);

	std::string infoShow = std::to_string(value.infoShow);
	getGroup({ "axis", "infoShow" }).setSetting("value", infoShow);

	std::string font = value.font.toStdString();
	getGroup({ "axis", "font" }).setSetting("value", font);
	Config::GetInstance()->saveFile();
}

DV::AxisXmlGroup::AxisXml DV::AxisXmlGroup::loadXmlInfo()
{
	AxisXml value;
	value.axisColor = StringToQColor(getGroup({ "axis", "axisColor" }).getValue("value"));
	value.axisSize = atoi(getGroup({ "axis", "axisSize" }).getValue("value").c_str());
	value.axisvalColor = StringToQColor(getGroup({ "axis", "axisvalColor" }).getValue("value"));
	value.axisvalSize = atoi(getGroup({ "axis", "axisvalSize" }).getValue("value").c_str());
	value.font = QString::fromStdString(getGroup({ "axis", "font" }).getValue("value"));
	value.infoShow = atoi(getGroup({ "axis", "infoShow" }).getValue("value").c_str());
	return value;

}

void DV::VectorXmlGroup::saveXmlInfo(VectorXml& val)
{
	getGroup({ "vector","vectorsize" }).setSetting("value", std::to_string(val.vectorsize));
	getGroup({ "vector","vectorColor" }).setSetting("value", QColorToQstring(val.vectorColor).toStdString());
	getGroup({ "vector","AlisAttitude" }).setSetting("isAlis", std::to_string(val.AlisAttitude));
	getGroup({ "vector","disMode" }).setSetting("value", std::to_string(val.disMode));
	Config::GetInstance()->saveFile();
}

DV::VectorXmlGroup::VectorXml DV::VectorXmlGroup::loadXmlInfo()
{
	VectorXml vectorXml;
	vectorXml.vectorsize = atoi(getGroup({ "vector","vectorsize" }).getValue("value").c_str());
	vectorXml.vectorColor = StringToQColor(getGroup({ "vector","vectorColor" }).getValue("value"));
	vectorXml.AlisAttitude = atoi(getGroup({ "vector","AlisAttitude" }).getValue("isAlis").c_str());
	vectorXml.disMode = atoi(getGroup({ "vector","disMode" }).getValue("value").c_str());
	return vectorXml;
}

void DV::ContourXmlGroup::saveXmlInfo(ContourXml& val)
{

	getGroup({ "contour","lineMapColors" }).setSetting("value", val.lineMapColors);
	getGroup({ "contour","AlisAttitude" }).setSetting("isAlis", std::to_string(val.AlisAttitude));
	getGroup({ "contour","valueStyle" }).setSetting("value", val.valueStyle);
	getGroup({ "contour","lineMapColorval" }).setSetting("valueNumber", std::to_string(val.values.size()));

	for (int index = 0; index < val.values.size(); index++)
	{
		std::stringstream os;
		os << "level_" << index;
		getGroup({ "contour","lineMapColorval" ,os.str() })
			.setSetting("value", std::to_string(val.values[index]));
		getGroup({ "contour","lineMapColorval" ,os.str() })
			.setSetting("color", QColorToQstring(val.colors[index]).toStdString());
	}
	Config::GetInstance()->saveFile();
}

DV::ContourXmlGroup::ContourXml DV::ContourXmlGroup::getXmlInfo()
{
	ContourXml contourXml;
	//<contour>
			//	<lineMapColorval valueNumber = "5">
			//	<level_0 value = "0" color = "FF5500FF" / >
			//	<level_1 value = "0.174504" color = "FF5555FF" / >
			//	<level_2 value = "0.478579" color = "FF55FFFF" / >
			//	<level_3 value = "0.785789" color = "FF55AA00" / >
			//	<level_4 value = "1" color = "FFFFFF00" / >
			//	< / lineMapColorval>
			//	< / contour>
	contourXml.lineMapColors = getGroup({ "contour","lineMapColors" }).getValue("value");
	contourXml.AlisAttitude = atoi(getGroup({ "contour","AlisAttitude" }).getValue("isAlis").c_str());
	contourXml.valueStyle = getGroup({ "contour","valueStyle" }).getValue("value");
	int size = atoi(getGroup({ "contour","lineMapColorval" }).getValue("valueNumber").c_str());
	contourXml.values.reserve(size);
	contourXml.colors.reserve(size);

	for (auto index = 0; index < size; ++index)
	{
		std::stringstream is;
		is << "level_" << index;
		contourXml
			.values
			.push_back(
				atof(getGroup({ "contour","lineMapColorval" ,is.str() })
					.getValue("value").c_str()));
		contourXml
			.colors
			.push_back(
				StringToQColor(getGroup({ "contour","lineMapColorval" ,is.str() })
					.getValue("color")));
	}
	return contourXml;
}

void DV::ParticleXmlGroup::saveXmlInfo(ParticleXml& val)
{
	getGroup({ "particle" ,"size" }).setSetting("value", std::to_string(val.size));
	getGroup({ "particle","color" }).setSetting("value", QColorToQstring(val.color).toStdString());
	getGroup({ "particle","AlisAttitude" }).setSetting("isAlis", std::to_string(val.AlisAttitude));
	Config::GetInstance()->saveFile();
}

DV::ParticleXmlGroup::ParticleXml DV::ParticleXmlGroup::getXmlInfo()
{
	/*<particle>
		<size value = "1" / >
		<color value = "FFFFAAFF" / >
		<AlisAttitude isAlis = "0" / >
		< / particle>*/
	ParticleXml particleXml;
	particleXml.size = atoi(getGroup({ "particle" ,"size" }).getValue("value").c_str());
	particleXml.color = StringToQColor(getGroup({ "particle","color" }).getValue("value"));
	particleXml.AlisAttitude = atoi(getGroup({ "particle","AlisAttitude" }).getValue("isAlis").c_str());
	return particleXml;
}

void DV::StructXmlGroup::saveXmlInfo(StructXml& value)
{

	for (auto index = 0; index < value.proPertyStr.size(); ++index)
		getGroup({ "struct", value.proPertyStr[index] })
		.setSetting("value", QColorToQstring(value.proPertyCol[index])
			.toStdString());
	getGroup({ "struct", "AlisAttitude" }).setSetting("isAlis", std::to_string(value.AlisAttitude));
}

DV::StructXmlGroup::StructXml DV::StructXmlGroup::getXmlInfo()
{
	/*<struct>
				<CONDUCTORNEW value = "FFAAFFFF" / >
				<DIELECTIRANDCONDUCTANCE value = "FFFF0000" / >
				<DIOLECTRIC value = "FFAAAAFF" / >
				<DRIVER value = "FFFF00FF" / >
				<FOIL value = "FFAAAA00" / >
				<FREESPACE value = "FF00AA00" / >
				<INDUCTOR value = "FF55AAFF" / >
				<PERFECTCONDUCTOR value = "FFFF0000" / >
				<PERMEABILITY value = "FF0000FF" / >
				<PORT value = "FFAA55FF" / >
				<VACUO value = "7DFF007F" / >
				<CONDUCTORNEWLINE value = "FFFFAA00" / >
				<DIELECTIRANDCONDUCTANCELINE value = "FF2C1621" / >
				<DIOLECTRICLINE value = "FF550000" / >
				<FOILLINE value = "FF003E3E" / >
				<FREESPACELINE value = "FF0A1E1E" / >
				<PERFECTCONDUCTORLINE value = "FF55FFFF" / >
				<PERMEABILITYLINE value = "FF002400" / >
				<VACUOLINE value = "00FFFFFF" / >
				<AlisAttitude isAlis = "1" / >
				< / struct>*/
	StructXml xmlinfo;
	std::stringstream is;
	is << "CONDUCTORNEW"
		<< "DIELECTIRANDCONDUCTANCE"
		<< "DIOLECTRIC"
		<< "DRIVER"
		<< "FOIL"
		<< "FREESPACE"
		<< "INDUCTOR"
		<< "PERFECTCONDUCTOR"
		<< "PERMEABILITY"
		<< "PORT"
		<< "VACUO"
		<< "CONDUCTORNEWLINE"
		<< "DIELECTIRANDCONDUCTANCELINE"
		<< "DIOLECTRICLINE"
		<< "FOILLINE"
		<< "FREESPACELINE"
		<< "PERFECTCONDUCTORLINE"
		<< "PERMEABILITYLINE"
		<< "VACUOLINE";
	int count= is.get();
	std::string ss = "";
	while (is>>ss)
	{
		xmlinfo.proPertyCol.push_back(StringToQColor(getGroup({ "struct",ss }).getValue("value")));
		xmlinfo.proPertyStr.push_back(ss);
	}
	xmlinfo.AlisAttitude = atoi(getGroup({ "struct", "AlisAttitude" }).getValue("isAlis").c_str());
	return xmlinfo;
}
