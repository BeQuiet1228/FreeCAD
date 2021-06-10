#pragma once
#include "Renderer.h"
#include "Data.h"
#include "qwt/qwt_plot_spectrogram.h"
#include "ContourData.h"
#include "qwt/qwt_color_map.h"
class ContourRender:public Renderer,public QwtPlotSpectrogram,public RendererValueRangeInterface{
public:
	ContourRender(std::shared_ptr<ContourData> data);
	~ContourRender();

	enum ContourLevelsMod{
		EQUAL_DIFFERENCE = 0,//等差模式
		PROPORTIONAL		//等比
	};
	//配置信息
	typedef struct CfgInfo
	{
		typedef struct valColor{
			double value;
			QColor color;
		}VALCOLOR;
		//等级模式
		ContourLevelsMod contourLevelsMod;
		//绘制模式
		bool isAA;
		//等值线取值模式
		QwtLinearColorMap::Mode mode;
		std::vector<valColor> colorlist;
	}CFGINFO;
public:
	bool drawImage() override;
	bool addListRang(std::list<Data::Rang> listRang) override;
	bool drawPointImage() override;
	bool setDefaultRang() override;
	void dataInit() override;
	virtual void loadconfig() override;
	//获取value范围
	Data::Rang getValueRange() override;
	//获取对应的结构体面
	std::vector<float> getStructFace();
protected:
	CFGINFO cfgInfo;
private:
	//绘制提示框
	void drawDisplayPoint(QPainter& painter, const QPointF& position, const ContourData::Grid& grid);
	//初始化等值线等级
	void initContourLevels();
private:
	ContourLevelsMod contourLevelsMod;
	//等值线等级
	unsigned int contourLevel;

};

//测试用
class ColorMap : public QwtLinearColorMap
{
public:
	ColorMap() :
		QwtLinearColorMap(Qt::darkBlue, Qt::darkRed)
	{
		addColorStop(0.2, Qt::blue);
		addColorStop(0.4, Qt::cyan);
		addColorStop(0.6, Qt::yellow);
		addColorStop(0.8, Qt::red);
	}
};