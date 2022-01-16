#pragma once
#include "QColor"
#include"string"
#include "vector"
#include "map"
#include "exportConfig.hpp"
namespace DV
{
	namespace XmlData
	{
		class DATA_VISUALIZATION_EXPORT XmlObject
		{
		public:
			XmlObject(std::vector<std::string> group, std::string valueKey);
			virtual  ~XmlObject();
			virtual void loadXml();
			virtual void saveXml();
			XmlObject& operator =(const XmlObject& that);
			std::vector<std::string> getGroupStr();
			void setGroup(std::vector<std::string> group);
			void addGroup(std::string);
			void setValstr(std::string val);
			void setValKey(std::string key);
			std::string getValStr();
			std::string getValKey();
		private:
			std::vector<std::string> groupStr;
			std::string valKey;
			std::string valStr;
		};
#define  XMLDATABIND(a,b)\
a##(std::vector<std::string> va1,std::string va2):b(va1,va2){}
		class DATA_VISUALIZATION_EXPORT XmlInt :public XmlObject
		{
		public:
			XMLDATABIND(XmlInt, XmlObject);
			XmlInt& operator=(const XmlInt& that);
			void operator =(const int);
			void loadXml();
		public:
			int value;
		};
		class DATA_VISUALIZATION_EXPORT XmlColor :public XmlObject
		{
		public:
			XMLDATABIND(XmlColor, XmlObject);
			XmlColor();
			XmlColor& operator =(XmlColor& that);
			void operator =(const QColor&);
		public:
			void loadXml();
		public:
			QColor value;
			double r;
			double g;
			double b;
			double a;
		};
		class DATA_VISUALIZATION_EXPORT XmlFloat :public XmlObject
		{
		public:
			XMLDATABIND(XmlFloat, XmlObject);
			void operator =(const float& f);
		public:
			void loadXml();
		public:
			float value;
		};
		class DATA_VISUALIZATION_EXPORT XmlString :public XmlObject
		{
		public:
			XMLDATABIND(XmlString, XmlObject);
			void operator =(const QString& s);
			void operator =(const std::string& s);
		public:
			void loadXml();
		public:
			QString value;
		};

		class DATA_VISUALIZATION_EXPORT XmlVectorFloat :public XmlObject
		{
		public:
			XMLDATABIND(XmlVectorFloat, XmlObject);
			~XmlVectorFloat();
			void loadXml(int count);
			void saveXml();
			XmlFloat& operator [] (int index);
			void operator=(std::vector<float> val);
			void push_back(float f);
			void push_back(XmlFloat f);
			int Size();
			std::vector<float> toVector();
		private:
			std::vector<XmlFloat> values;
		};
		class DATA_VISUALIZATION_EXPORT XmlVectorColor :public XmlObject
		{
		public:
			XMLDATABIND(XmlVectorColor, XmlObject);
			~XmlVectorColor();
			void loadXml(int count);
			void saveXml();
			XmlColor& operator[](int index);
			void push_back(QColor);
			void push_back(XmlColor);
			int Size();
			std::vector<QColor> toVector();
			void operator =(std::vector<QColor>);
		private:
			std::vector<XmlColor> values;
		};
		class DATA_VISUALIZATION_EXPORT XmlColorBar :public XmlObject
		{
		public:
			XmlColorBar(std::vector<std::string> group, std::string valKey);
			void loadXml();
			void saveXml();
		public:
			XmlVectorColor colors;
			XmlVectorFloat values;
		};
#undef XMLDATABIND(a,b)
		class DATA_VISUALIZATION_EXPORT XmlStructObj
		{
		public:
			XmlStructObj();
			virtual ~XmlStructObj();
			void saveXml();
			void loadXml();
			void push_back(XmlObject*);
			void push_back(XmlStructObj*);
		private:
			std::vector<XmlObject*> memberList;
			std::vector<XmlStructObj*> memberLists;
		};
#ifdef DATA_VISUALIZATIONG_DLL

		class AxisXml :public XmlStructObj
		{
		public:
			AxisXml();
			~AxisXml();
		public:
			XmlInt		axisSize;
			XmlColor	axisColor;
			XmlColor	axisvalColor;
			XmlInt		axisvalSize;
			XmlInt		infoShow;
			XmlString	font;
		};
		class  VectorXml :public XmlStructObj
		{
		public:
			VectorXml();
			~VectorXml();
		public:
			XmlInt		vectorsize;
			XmlColor	vectorColor;
			XmlInt		AlisAttitude;
			XmlInt		disMode;
		};
		class ContourXml :public XmlStructObj
		{
		public:
			ContourXml();
			~ContourXml();
		public:
			XmlString lineMapColors;
			XmlInt AlisAttitude;
			XmlString valueStyle;
			XmlColorBar colorBar;
		};
		class ParticleXml :public XmlStructObj
		{
		public:
			ParticleXml();
			~ParticleXml();
		public:
			XmlInt size;
			XmlColor color;
			XmlInt AlisAttitude;
		};
		class  StructXml:public XmlStructObj
		{
		public:
			StructXml();
			~StructXml();
			void loadXml();
			void saveXml();
		public:
			XmlInt AlisAttitude;
			std::map<std::string, QColor> proPerty;
		};
#endif
	};
}