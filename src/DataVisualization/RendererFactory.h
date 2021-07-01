#pragma  once
#include <memory>
#include "HDF5Reader/hdf5io.h"
#include <vector>
#include <list>
#include "Data.h"
#include "StructData.h"
class Data;
class Renderer;
class ContourRender;
using RendererPtr = std::shared_ptr<Renderer>;
using Renderers = std::list<RendererPtr>;
using DataPtr = std::shared_ptr<Data>;
class RendererFactory{
public:
	RendererFactory(Hdf5Data h5d);
	//新增默认构造
	RendererFactory();
	~RendererFactory() =default;

public:
	Renderers creatRenderers(Hdf5Data h5d,DirectionType type = X_Y);
	RendererPtr creatContourStructRender(std::shared_ptr<ContourRender>& contourRender);
	static RendererPtr creatRenderer(Hdf5Data h5d,DirectionType type = X_Y);
	static RendererPtr creatRenderer(DataPtr data);
	static DataPtr creatData(Hdf5Data h5d);
	static DataPtr creatTimeData(Hdf5Data h5d);
	static DataPtr creatParticleData(Hdf5Data h5d);
	static DataPtr creatContuorData(Hdf5Data h5d);
	static RendererPtr creatContuorRender(Hdf5Data h5d);
	static DataPtr creatInterspaceData(Hdf5Data h5d);

	static RendererPtr creatStructRender(Hdf5Data h5d, DirectionType type = X_Y);
	static RendererPtr creatStructRender(Hdf5Data h5d, const _3DPointf& start,const _3DPointf& end);
	static RendererPtr creatVectorRender(Hdf5Data h5d);

	//寻找结构图
	static int  findStructDataIndex(const std::vector<Hdf5Data>& datas);
private:
	Hdf5Data structData;
	bool ishaveStruct;

public: 
	void setStructData(const Hdf5Data& data) {
		this->structData = data;
		ishaveStruct = true;
	}

};