#pragma once
#include "Renderer.h"
#include "Data.h"
#include "qwt/qwt_plot_spectrogram.h"
#include "ContourData.h"
#include "qwt/qwt_color_map.h"
typedef struct ContourParam
{
	//抗锯齿属性
	bool isAA;
	ContourParam();
}CONTOURPARAM;

class ContourRender:public Renderer,public QwtPlotSpectrogram{
public:
	ContourRender(std::shared_ptr<ContourData> data);
	~ContourRender();

public:
	bool drawImage() override;
	bool addListRang(std::list<Data::Rang> listRang) override;
	bool drawPointImage() override;
	bool setDefaultRang() override;
	void dataInit() override;
	virtual void loadconfig() override;
	//获取value范围
	Data::Rang getValueRange();
	//获取对应的结构体面
	std::vector<float> getStructFace();
private:
	//绘制提示框
	void drawDisplayPoint(QPainter& painter, const QPointF& position, const ContourData::Grid& grid);
	ContourParam contourParam;
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