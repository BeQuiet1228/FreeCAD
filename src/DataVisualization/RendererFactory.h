#pragma  once
#include <memory>
#include "HDF5Reader/hdf5io.h"
#include <vector>
#include <list>
#include "Data.h"
class Data;
class Renderer;
using RendererPtr = std::shared_ptr<Renderer>;
using Renderers = std::list<RendererPtr>;
using DataPtr = std::shared_ptr<Data>;
class RendererFactory{
public:
	RendererFactory(std::vector<Hdf5Data> d);
	~RendererFactory();

public:
	Renderers creatRenderers(Hdf5Data h5d);
	static RendererPtr creatRenderer(Hdf5Data h5d);
	static RendererPtr creatRenderer(DataPtr data);
	static DataPtr creatData(Hdf5Data h5d);
	static DataPtr creatTimeData(Hdf5Data h5d);
	static DataPtr creatParticleData(Hdf5Data h5d);
	static DataPtr creatContuorData(Hdf5Data h5d);
	static RendererPtr creatContuorRender(Hdf5Data h5d);
	static DataPtr creatInterspaceData(Hdf5Data h5d);

	static RendererPtr creatStructRender(Hdf5Data h5d, DirectionType type = X_Y);
	static RendererPtr creatVectorRender(Hdf5Data h5d);
private:
	std::vector<Hdf5Data> datas;
};