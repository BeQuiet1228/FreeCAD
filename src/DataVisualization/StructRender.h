#pragma once
#ifndef _STRUCT_RENDER_H_
#define _STRUCT_RENDER_H_
#include "Renderer.h"
#include "StructData.h"
#include <QColor>
enum StructTexture
{
	//理想导体
	Perfect_Conductor = 3,
	//电导新材料
	Conductor_New = 8,
	//介质
	Diolectric = 4,
	//磁导率
	Permeability = 16,
	//真空
	Vacuo = 1024,
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
	virtual bool drawImage() override;
	virtual bool addListRang(std::list<Data::Rang> listRang) override;
	virtual bool drawPointImage() override;
	virtual bool setDefaultRang() override;
	virtual void dataInit() override;

private:
	float transitionX(const float& x, const float& xScale, const Data::Rang& xr);
	float transitionY(const float& y, const float& yScale, const Data::Rang& yr);
	void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, const Data::Rang& yr);
	void transitionRectF(QRectF& _rectf, const float& sScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr);
	bool getTransitionScale(float& xScale, float& yScale);
	bool drawImage_polar();
	bool drawImage_polar_r_z();
	bool drawImage_polar_r_theta();
	bool drawImage_cylindrical();
	bool drawImage_cartesian();
private:
	QMap<int, QColor> color_tab;
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
};

#endif
