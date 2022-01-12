#pragma once
#include "QColor"
#include "CustomConfig.h"
#include"string"
#include "vector"
namespace DV
{
	class XmlGroup
	{
	public:
		XmlGroup() = default;
		~XmlGroup() = default;
	protected:
		//ConfigGroup getGroup(char*,...);
		ConfigGroup getGroup(std::vector<std::string>);
	};
	class AxisXmlGroup :public XmlGroup
	{
	public:
		struct AxisXml
		{
			int axisSize;
			QColor axisColor;
			QColor axisvalColor;
			int axisvalSize;
			int infoShow;
			QString font;
		};
		AxisXmlGroup() = default;
		~AxisXmlGroup() = default;
		void saveXmlInfo(AxisXml&);
		AxisXml loadXmlInfo();
	};
	class VectorXmlGroup :public XmlGroup
	{
	public:
		struct VectorXml
		{
			int vectorsize;
			QColor vectorColor;
			int AlisAttitude;
			int disMode;
		};
		void saveXmlInfo(VectorXml&);
		VectorXml loadXmlInfo();
	};
	class ContourXmlGroup :public XmlGroup
	{
	public:
		struct ContourXml
		{
			std::string lineMapColors;
			int AlisAttitude;
			std::string valueStyle;
			std::vector<float> values;
			std::vector<QColor> colors;
		};
		void saveXmlInfo(ContourXml&);
		ContourXml getXmlInfo();
	};
	class ParticleXmlGroup :public XmlGroup
	{
	public:
		struct ParticleXml
		{
			int size;
			QColor color;
			int AlisAttitude;
		};
		void saveXmlInfo(ParticleXml&);
		ParticleXml getXmlInfo();
	};
	class StructXmlGroup :public XmlGroup
	{
	public:
		struct StructXml
		{
			std::vector<std::string> proPertyStr;
			std::vector<QColor> proPertyCol;
			int AlisAttitude;
		}; 
		void saveXmlInfo(StructXml&);
		StructXml getXmlInfo();
	};

}