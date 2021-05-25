#pragma once
#ifndef _STRUCT_RENDER_H_
#define _STRUCT_RENDER_H_
#include "Renderer.h"
#include "StructData.h"
#include <QColor>
enum StructTexture
{
	//理想导体
	PerfectConductor = 3,
	//电导新材料
	ConductorNew = 8,
	//介质
	Diolectric = 4,
	//电介质和电导
	dielectirAndconductance = 16,
	//磁导率
	Permeability = 32,
	//自由空间
	Freespace = 64,
	//电阻
	FOIL = 128,
	
	//线段
	//波导端口
	waveGuideport = 1024,
	//传动
	DRIVER=2048,
	//感应器
	Inductor = 16384
};
class StructRender :public Renderer
{
public:
	StructRender(std::shared_ptr<StructData> data);
	~StructRender();
	void SetColor(int Material_index, QColor color)
	{
		color_tab[Material_index] = color;
	}
	void discolor(int Material_index)
	{
		auto iter = color_tab.find(Material_index);
		if (iter != color_tab.end())
		{
			color_tab.erase(iter);
		}
	}
	virtual void loadconfig()override;
	virtual bool drawImage() override;
	virtual bool addListRang(std::list<Data::Rang> listRang) override;
	virtual bool drawPointImage() override;
	virtual bool setDefaultRang() override;
	virtual void dataInit() override;
	virtual bool setDefaultRang(QSize&) override;
private:
	bool drawImageRectspace();
	bool drawImageRandspace();
	float transitionX(const float& x, const float& xScale, const Data::Rang& xr);
	float transitionY(const float& y, const float& yScale, const Data::Rang& yr);
	void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, const Data::Rang& yr);
	void transitionRectF(QRectF& _rectf, const float& sScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr);
	bool getTransitionScale(float& xScale, float& yScale);
	bool drawImagePolar();
	bool drawImagePolarRz();
	bool drawImagePolarRtheta();
	bool drawImageCylindrical();
	bool drawImageCylindricalRz();
	bool drawImageCylindricalRtheta();
	bool drawImageCartesian();
	bool drawImageCartesianXy();
	bool drawImageCartesianYz();
	bool drawImageCartesianXz();
	QVector<QPainterPath> StructRender::GetPath(std::vector<StructData::CutCir>& _vector, const Data::Rang& xr, const Data::Rang& yr, const float& xScale, const float& yScale);
	bool drawPointImagePolar();
	bool drawPointImageCylindrical();
	bool drawPointImageCartesian();
	bool drawPointImagePolarRz();
	bool drawPointImagePolarRtheta();
	bool drawPointImageCylindricalRz();
	bool drawPointImageCylindricalRtheta();
	bool drawPointImageCartesianXyz();
	StructData::structpoint findApointZr(QPointF _curpostion);
	float GetDistance(QPointF p1, QPointF p2);

	//目前先暂时保留，改方法没有使用
	void drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d);
	bool drawPointRect();
	bool drawPointCir();
	StructData::structpoint findApointCylindrical(QPointF _curpoint);
private:
	QMap<int, QColor> color_tab;
	QMap<int, QColor> color_pen;
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
	bool isAA;
};

#endif
