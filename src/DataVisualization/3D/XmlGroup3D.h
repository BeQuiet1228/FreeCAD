#pragma once
#include "QColor"
#include "string"
#include "vector"
namespace DV3D
{
	namespace XmlData
	{
		struct ColorF {
			double r;
			double g;
			double b;
			double a;
		};
		ColorF getColors(std::string colorStr);
		ColorF getColors(QColor color);
		struct  Struct3dXml
		{
			QColor color;
		};
		struct  Contour3dXml
		{
			std::vector<float> values;
			std::vector<QColor> colors;
		};
		struct Particle3dXml
		{
			double particleSize;
			QColor particleColor;
		};
		struct Vector3dXml {
			int XorRGridInc;
			int YorThetaGridInc;
			int ZGridInc;
			Contour3dXml colorBar;
		};
		/*
			创建255个颜色过度表
		*/
		std::vector<ColorF> getColors(std::vector<float>&, std::vector<QColor>&, int black = 255);
		//std::vector<ColorF> getColors(std::vector<float>&, std::vector<ColorF>&, int black = 255);
		void loadXmlInfo(Struct3dXml&);
		void saveXmlInfo(Struct3dXml&);
		void loadXmlInfo(Contour3dXml&);
		void saveXmlInfo(Contour3dXml&);
		void loadXmlInfo(Particle3dXml&);
		void saveXmlInfo(Particle3dXml&);
		void loadXmlInfo(Vector3dXml&);
		void saveXmlInfo(Vector3dXml&);

	}
};