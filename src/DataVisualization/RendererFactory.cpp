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
#include "Renderer.h"
RendererFactory::RendererFactory(std::vector<Hdf5Data> d)
	:datas(d)
{

}

/**
* @brief RendererFactory::creatRenderers 根据类型创建所有渲染器
* @param Hdf5Data h5d
* @return Renderers
*/
Renderers RendererFactory::creatRenderers(Hdf5Data h5d)
{
	return Renderers();
}

RendererPtr RendererFactory::creatRenderer(Hdf5Data h5d)
{
	if (h5d.name == "OBSERVE")
	{
		std::shared_ptr<TimeData> d(new TimeData(h5d));
		TimeRenderer *r = new TimeRenderer(d);
		return RendererPtr(r);

	}else if (h5d.name == "PHASESPACE"){
		std::shared_ptr<ParticleData> d(new ParticleData(h5d));
		ParticleRenderer *r = new ParticleRenderer(d);
		return RendererPtr(r);
	}
	else if (h5d.name == "CONTOUR"){
		return creatContuorRender(h5d);
		
	}
	else if (h5d.name == "RANGE"){
		std::shared_ptr<InterspaceData> d(new InterspaceData(h5d));
		InterspaceRender* r = new InterspaceRender(d);
		return RendererPtr(r);
	}

	return RendererPtr();
}


DataPtr RendererFactory::creatTimeData(Hdf5Data h5d)
{
	TimeData *data = new TimeData(h5d);
	return DataPtr(data);
}

DataPtr RendererFactory::creatParticleData(Hdf5Data h5d)
{
	ParticleData *data = new ParticleData(h5d);
	return DataPtr(data);
}

DataPtr RendererFactory::creatContuorData(Hdf5Data h5d)
{
	ContourData *data = new ContourData(h5d);
	
	if (data->getDirectionType() != R_THETA)
		return DataPtr(data);
	delete data;

	ContourDataPolar *pdata = new ContourDataPolar(h5d);
	return DataPtr(pdata);
}

RendererPtr RendererFactory::creatContuorRender(Hdf5Data h5d)
{
	std::shared_ptr<ContourData> data(new ContourData(h5d));
	data->initDiretion();
	if (data->getDirectionType() != R_THETA)
	{
		ContourRender* r = new ContourRender(data);
		return RendererPtr(r);
	}
	data.reset();
	
	std::shared_ptr<ContourDataPolar> pdata(new ContourDataPolar(h5d));
	ContourRenderPolar *r = new ContourRenderPolar(pdata);
	return RendererPtr(r);
	
}

DataPtr RendererFactory::creatInterspaceData(Hdf5Data h5d)
{
	InterspaceData *data = new InterspaceData(h5d);
	return DataPtr(data);
}

