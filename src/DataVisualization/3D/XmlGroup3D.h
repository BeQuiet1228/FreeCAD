#pragma once
#include "QColor"
#include "string"
#include "vector"
#include <QVector3D>
#include "../XmlGroup.h"
namespace DV3D
{
	namespace XmlData
	{
		//ColorF getColors(std::string colorStr);
		//ColorF getColors(QColor color);
		class XmlPointf3d:public DV::XmlData::XmlStructObj
		{
		public:
			XmlPointf3d(std::vector<std::string> group);
			~XmlPointf3d();
			double x();
			double y();
			double z();
			void setX(double x);
			void setY(double y);
			void setZ(double z);
			void addGroup(std::string val);
		private:
			DV::XmlData::XmlFloat xf;
			DV::XmlData::XmlFloat yf;
			DV::XmlData::XmlFloat zf;
		};
		class ControlerXml :public DV::XmlData::XmlStructObj
		{
		public:
			ControlerXml(std::vector<std::string> group);
			DV::XmlData::XmlFloat alpha;//0~1
			DV::XmlData::XmlInt clipEnable;//
			DV::XmlData::XmlInt gridEnable;
			XmlPointf3d centerPoint;
			XmlPointf3d normalPoint;
		};
		/*
			3维图保存数据
		*/
		class Struct3dXml:public DV::XmlData::XmlStructObj
		{
		public:
			Struct3dXml();
			DV::XmlData::XmlInt Rotation;//插值的平滑度
			DV::XmlData::XmlColor color;
			ControlerXml controlerXml;
		};
		class  Contour3dXml:public DV::XmlData::XmlStructObj
		{
		public:
			Contour3dXml();
			DV::XmlData::XmlInt Rotation;//插值的平滑度
			DV::XmlData::XmlColorBar colorbar;
			ControlerXml controlerXml;
		};
		class Particle3dXml:public DV::XmlData::XmlStructObj
		{
		public:
			Particle3dXml();
			DV::XmlData::XmlFloat particleSize;
			DV::XmlData::XmlColor particleColor;
			ControlerXml controlerXml;
		};
		class Vector3dXml :public DV::XmlData::XmlStructObj
		{
		public:
			Vector3dXml();
			DV::XmlData::XmlInt XorRGridInc;
			DV::XmlData::XmlInt YorThetaGridInc;
			DV::XmlData::XmlInt ZGridInc;
			DV::XmlData::XmlColorBar colorBar;
			ControlerXml controlerXml;
		};

		/*
			创建255个颜色过度表
		*/
		std::vector<DV::XmlData::XmlColor> getColors(std::vector<float>&, std::vector<DV::XmlData::XmlColor>&, int black = 255);
		std::vector<QColor> getColors(std::vector<float>&, std::vector<QColor>&, int black = 255);
	}
};