#include "RendererFactory.h"
#include "TimeData.h"
#include "ParticleData.h"
#include "ContourData.h"
#include "ContourDataPolar.h"
#include "InterSpaceData.h"
#include "TimeRenderer.h"
#include "InterspaceRender.h"
#include "ParticleRenderer.h"
#include "ContourRender.h"
#include "ContourRenderPolar.h"
#include "StructData.h"
#include "StructRender.h"
#include "Struct2dData.h"
#include "Struct2dRenderer.h"
#include "phasorData.h"
#include "phasorRenderer.h"
#include "Renderer.h"
#include "ContourPlotAdapter.h"
#include "phasorPlotAdapter.h"
#include "TimePlotAdapter.h"
#include "TimeMultiplePlotAdapter.h"
#include <iostream>
namespace DV {
	RendererFactory::RendererFactory(Hdf5Data h5d)
		: structData(h5d), ishaveStruct(true)
	{

	}
	RendererFactory::RendererFactory() : ishaveStruct(false)
	{

	}
	Renderers RendererFactory::creatRenderers(Hdf5Data h5d, DirectionType type /*= X_Y*/)
	{
		RendererPtr renderer = creatRenderer(h5d, type);

		Renderers renderers;
		renderers.push_back(renderer);
		if (!ishaveStruct)
			return renderers;
		if (renderer->getNeedStrucuType() != Data::NEED_STRUCT)
			return renderers;
		//如果是等位图，那么必须使用观测面初始化结构图
		auto contourRender = std::dynamic_pointer_cast<ContourRender>(renderer);

		if (contourRender)
		{
			auto sRender = creatContourStructRender(contourRender);
			if (sRender)
			{
				renderers.push_back(sRender);
				return renderers;
			}
		}

		RendererPtr structRenderer = creatRenderer(structData, renderer->getDirection());
		renderers.push_back(structRenderer);

		return renderers;
	}


	RendererPtr RendererFactory::creatRenderer(Hdf5Data h5d, DirectionType type /*= X_Y*/)
	{
		if (h5d.name == "OBSERVE")
		{
			std::shared_ptr<TimeData> d(new TimeData(h5d));
			TimeRenderer* r = new TimeRenderer(d);
			return RendererPtr(r);

		}
		else if (h5d.name == "PHASESPACE") {
			std::shared_ptr<ParticleData> d(new ParticleData(h5d));
			ParticleRenderer* r = new ParticleRenderer(d);
			return RendererPtr(r);
		}
		else if (h5d.name == "CONTOUR") {
			return creatContuorRender(h5d);

		}
		else if (h5d.name == "RANGE") {
			std::shared_ptr<InterspaceData> d(new InterspaceData(h5d));
			InterspaceRender* r = new InterspaceRender(d);
			return RendererPtr(r);
		}
		else if (h5d.name == "struct"
				|| h5d.name=="struct2d")
		{
			return creatStructRender(h5d, type);
		}
		else if (h5d.name == "VECTOR")
		{
			return creatVectorRender(h5d);
		}

		return RendererPtr();
	}

	DataPtr RendererFactory::creatTimeData(Hdf5Data h5d)
	{
		TimeData* data = new TimeData(h5d);
		return DataPtr(data);
	}

	DataPtr RendererFactory::creatParticleData(Hdf5Data h5d)
	{
		ParticleData* data = new ParticleData(h5d);
		return DataPtr(data);
	}

	DataPtr RendererFactory::creatContuorData(Hdf5Data h5d)
	{
		ContourData* data = new ContourData(h5d);

		if (data->getDirectionType() != R_THETA)
			return DataPtr(data);
		delete data;

		ContourDataPolar* pdata = new ContourDataPolar(h5d);
		return DataPtr(pdata);
	}

	RendererPtr RendererFactory::creatContuorRender(Hdf5Data h5d)
	{
		std::shared_ptr<ContourData> data(new ContourData(h5d));
		if (data->getDirectionType() != R_THETA)
		{
			ContourRender* r = new ContourRender(data);
			return RendererPtr(r);
		}
		data.reset();

		std::shared_ptr<ContourDataPolar> pdata(CreateContourDataPolar(h5d));
		ContourRenderPolar* r = new ContourRenderPolar(pdata);
		return RendererPtr(r);

	}

	DataPtr RendererFactory::creatInterspaceData(Hdf5Data h5d)
	{
		InterspaceData* data = new InterspaceData(h5d);
		return DataPtr(data);
	}
	RendererPtr RendererFactory::creatStructRender(Hdf5Data h5d, DirectionType type)
	{
		//需要判断结构图是2维的还是3维的
		if (h5d.listDataSet.size() > 3)
		{
			std::shared_ptr<StructData> _structdata(new StructData(h5d, type));
			StructRender* _StructureRenderer = new StructRender(_structdata);
			return RendererPtr(_StructureRenderer);
		}
		else
		{
			std::shared_ptr<Struct2dData> _structdata(new Struct2dData(h5d));
			Struct2DRenderer* _struct2drenderer = new Struct2DRenderer(_structdata);
			return RendererPtr(_struct2drenderer);
		}
	}

	/**
	* @brief RendererFactory::creatStructRender 根据面的两个带你创建结构图
	* @param Hdf5Data h5d
	* @param const _3DPointf & start
	* @param const _3DPointf & end
	* @return RendererPtr
	*/
	RendererPtr RendererFactory::creatStructRender(Hdf5Data h5d, STRUCTTYPE md, const _3DPointf& start, const _3DPointf& end)
	{
		switch (md)
		{
		case RendererFactory::MOD_2D:
		{
			/*QPointF start2d, end2d;
			start2d.setX(start._1st);
			start2d.setY(start._2rd);
			end2d.setX(end._1st);
			end2d.setY(end._2rd);
			std::shared_ptr<Struct2dData> _structdata(new Struct2dData(h5d,start2d,end2d));*/
			//不设置范围
			std::shared_ptr<Struct2dData> _structdata(new Struct2dData(h5d));
			Struct2DRenderer* struct2drenderer = new Struct2DRenderer(_structdata);
			return RendererPtr(struct2drenderer);
		}
		break;
		case RendererFactory::MOD_3D:
		{
			std::shared_ptr<StructData> _structdata(new StructData(h5d, start, end));
			StructRender* _StructureRenderer = new StructRender(_structdata);
			return RendererPtr(_StructureRenderer);
		}
		break;
		}
	}




	RendererPtr RendererFactory::creatContourStructRender(std::shared_ptr<ContourRender>& contourRender)
	{
		_3DPointf start, end;
		auto v = contourRender->getStructFace();
		if (v.size() < 4)
			return RendererPtr();
		STRUCTTYPE md;
		//让数据兼容2d等位图数据
		if (v.size() == 4)
		{
			/*2d不分结构图方向，所以这里什么也不需要做 */
			start._1st = v[0];
			start._2rd = v[1];
			end._1st = v[2];
			end._2rd = v[3];
			md = MOD_2D;

		}
		else {
			start._1st = v[0];
			start._2rd = v[1];
			start._3th = v[2];
			end._1st = v[3];
			end._2rd = v[4];
			end._3th = v[5];
			md = MOD_3D;
		}
		RendererPtr structRenderer = creatStructRender(structData, md, start, end);
		return structRenderer;
	}

	RendererPtr RendererFactory::creatVectorRender(Hdf5Data h5d)
	{
		std::shared_ptr<phasorData> r(new phasorData(h5d));
		phasorRenderer* rd = new phasorRenderer(r);
		return RendererPtr(rd);
	}

	Renderers RendererFactory::creatMultipleTimeRenderers(std::list<std::shared_ptr<DV::TimeData>> timeDatas)
	{
		Renderers renderers;
		for (auto iter = timeDatas.begin(); iter != timeDatas.end(); iter++) {
			std::shared_ptr<TimeRenderer> renderer(new TimeRenderer(*iter));
			renderers.push_back(renderer);
		}
		return renderers;
	}

	DV::PlotAdapterPtr RendererFactory::creatMultipleTimeAdapter(Renderers renderers)
	{
		std::shared_ptr<TimeMultiplePlotAdapter> adapter(new TimeMultiplePlotAdapter(renderers));
		return adapter;
	}

	/**
	* @brief RendererFactory::findStructDataIndex 寻找结构图的索引
	* @param const std::vector<Hdf5Data>& datas datas 数据集
	* @return int -1表示寻找失败
	*/
	int RendererFactory::findStructDataIndex(const std::vector<Hdf5Data>& datas)
	{
		if (datas.size() == 0)
			return -1;
		for (int i = 0; i < datas.size(); i++)
		{
			if (datas.at(i).name == "struct")
				return i;
		}
#ifdef MY_DEBUG
		std::cerr << "RendererFactory::findHdf5Data not found struct data!" << std::endl;
#endif // MY_DEBUG
		return -1;
	}

	/**
	* @brief RendererFactory::creatPlotAdapter 根据H5数据对象生成一个图表适配器
	* @param Hdf5Data h5d 数据对象
	* @param DirectionType type 方向类型
	* @return PlotAdapterPtr 适配器
	*/
	PlotAdapterPtr RendererFactory::creatPlotAdapter(Hdf5Data h5d, DirectionType type /*= X_Y*/)
	{
		auto renders = creatRenderers(h5d, type);
		PlotAdapterPtr adapter;

		if (h5d.name == "CONTOUR") {
			adapter.reset(new ContourPlotAdapter(renders));
		}
		else if (h5d.name == "VECTOR")
		{
			adapter.reset(new PhasorPlotAdapter(renders));
		}
		else if (h5d.name == "PHASESPACE" && (*renders.begin())->getNeedStrucuType() == Data::NEED_STRUCT) {
			adapter.reset(new PlotAdapterNeedStruct);
			adapter->addRenderer(renders);
		}
		else if (h5d.name == "OBSERVE" || h5d.name == "RANGE")
		{
			adapter.reset(new TimePlotAdapter(renders));
		}
		else {
			adapter.reset(new PlotAdapter);
			adapter->addRenderer(renders);
		}

		return adapter;
	}

};
