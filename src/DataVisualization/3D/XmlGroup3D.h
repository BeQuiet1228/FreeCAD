#pragma once
#include "QColor"
#include "string"
#include "vector"
#include <QVector3D>
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
		struct ControlerXml
		{
			float alpha;//0~1
			int clipEnable;//
			int gridEnable;
			QVector3D centerPoint;
			QVector3D normalPoint;
		};
		/*
			3维图保存数据
		*/
		struct  Struct3dXml
		{
			QColor color;
			ControlerXml controlerXml;
		};
		struct  Contour3dXml
		{
			std::vector<float> values;
			std::vector<QColor> colors;
			ControlerXml controlerXml;
		};
		struct Particle3dXml
		{
			double particleSize;
			QColor particleColor;
			ControlerXml controlerXml;
		};
		struct Vector3dXml {
			int XorRGridInc;
			int YorThetaGridInc;
			int ZGridInc;
			Contour3dXml colorBar;
			ControlerXml controlerXml;
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
		/*
			控制窗口的读取
		*/
		void loadXmlInfo(ControlerXml&, std::string parentGroup = "");
		void saveXmlInfo(ControlerXml&, std::string parentGroup = "");
	}
};