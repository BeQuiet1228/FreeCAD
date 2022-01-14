#pragma once
#include "QColor"
#include"string"
#include "vector"
#include "map"
namespace DV
{
	namespace XmlData
	{
		struct AxisXml
		{
			int axisSize;
			QColor axisColor;
			QColor axisvalColor;
			int axisvalSize;
			int infoShow;
			QString font;
		};
		struct VectorXml
		{
			int vectorsize;
			QColor vectorColor;
			int AlisAttitude;
			int disMode;
		};
		struct ContourXml
		{
			std::string lineMapColors;
			int AlisAttitude;
			std::string valueStyle;
			std::vector<float> values;
			std::vector<QColor> colors;
		};
		struct ParticleXml
		{
			int size;
			QColor color;
			int AlisAttitude;
		};
		struct StructXml
		{
			std::map<std::string, QColor> proPerty;
			int AlisAttitude;
		};
		void saveXmlInfo(AxisXml&);
		void loadXmlInfo(AxisXml&);
		void saveXmlInfo(VectorXml&);
		void loadXmlInfo(VectorXml&);
		void saveXmlInfo(ContourXml&);
		void getXmlInfo(ContourXml&);
		void saveXmlInfo(ParticleXml&);
		void getXmlInfo(ParticleXml&);
		void saveXmlInfo(StructXml&);
		void getXmlInfo(StructXml&);
	};
}