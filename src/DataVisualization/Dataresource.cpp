#include "Dataresource.h"
#include "RendererFactory.h"
#include "Plot.h"
//结构图的方向
enum stru_dir
{
	_PIN_Z=0,
	_Z_R,
	_R_PIN,
	_X_Y,
	_Y_Z,
	_X_Z,
};
std::string StructDirection[] = { "Phi-Z",
"Z-R",
"R*cos(Phi)-R*sin(Phi)","X_Y","Y_Z","X_Z"};
/**
* @brief DataSourceManage::tranfromRenderer 树表点击事件槽
* @param std::string name
* @param int index 索引号
* @return void
*/
void DataSourceManage::tranfromRenderer(std::string name,int index){
	if (index > hdfDatelist.size())
		return;
	QString str = QString::fromStdString(name);
	str += QString("_%1").arg(index);
	std::string newname = str.toStdString();
	auto iter = RendererManger.find(newname);
	if (iter!=RendererManger.end())
	{
		auto  ad = iter->second;
		emit _reRendererEvent(ad);
	}
	else
	{
		DirectionType type=R_Z;
		int index_dir = -1;
		for (auto i = 0; i < 6;i++)
		{
			if (name.find(StructDirection[i])!=std::string::npos)
			{
				index_dir = i;
				break;
			}
		}
		if (index_dir!=-1)
		{
			switch (index_dir)
			{
			case stru_dir::_PIN_Z:
				type = DirectionType::R_Z; break;
			case stru_dir::_Z_R:
				type = DirectionType::R_Z; break;
			case stru_dir::_R_PIN:
				type = DirectionType::R_THETA; break;
			case stru_dir::_X_Y:
				type = DirectionType::X_Y; break;
			case stru_dir::_Y_Z:
				type = DirectionType::Y_Z; break;
			case stru_dir::_X_Z:
				type = DirectionType::X_Z; break;
			default:
				break;
			}
			auto ad = factoryptr->creatPlotAdapter(hdfDatelist[index], type);
			RendererManger[name] = ad;
			emit _reRendererEvent(ad);
			return;
		}
		auto ad = factoryptr->creatPlotAdapter(hdfDatelist[index]);
		//先装入队列
		RendererManger[newname] = ad;
		emit _reRendererEvent(ad);
	}
}
/**
* @brief DataSourceManage::CreateRenderer 创建渲染器
* @param Hdf5Data data h5数据
* @param int _type 方向
* @return Renderers 
*/
Renderers DataSourceManage::CreateRenderer(Hdf5Data& data, int _type)
{
	Renderers rds = factoryptr->creatRenderers(data, (DirectionType)_type);
	return rds;
}
/**
* @brief DataSourceManage::CreateRendererList 获取渲染器
* @param Hdf5Data data
* @return RendererPtr
*/
Renderers DataSourceManage::CreateRendererList(Hdf5Data& data){
	//从工厂获取到相关的渲染器
	Hdf5Data _data(data);
	Renderers rd=factoryptr->creatRenderers(_data);
	return rd;
}
/**
* @brief DataSourceManage::clearMap 清除字典
* @return void 
*/
void DataSourceManage::clearMap(){
	//RendererManger.clear();
}
/**
* @brief DataSourceManage::loadhdffile 加载hdf5文件
* @param std::string filepath 文件路径
* @return void
*/
void DataSourceManage::loadhdffile(std::string filepath)
{
	//增加删除
	DataClear();
	Hdf5IO io(filepath);
	io.initHdf5Data();
	//获取到hdf5文件
	std::vector<Hdf5Data> _hdfDatelist = io.hdf5DataList;
	emit _loadhdflist(_hdfDatelist);
	//深度交换
	hdfDatelist.swap(_hdfDatelist);
	/*****************************************************/
	//结构图初始化
	int structindex = RendererFactory::findStructDataIndex(hdfDatelist);
	if (structindex>=0)
	{
		Hdf5Data structDate(hdfDatelist.at(structindex));
		factoryptr = std::shared_ptr<RendererFactory>(new RendererFactory(structDate));
	}
	else
	{
		factoryptr = std::shared_ptr<RendererFactory>(new RendererFactory());
	}
	
	/****************************************************/
	_hdf5io = io;
}
/**
* @brief DataSourceManage::DataSourceManage 数据管理构造
*/
DataSourceManage::DataSourceManage():factoryptr(nullptr),treePtrsite(0),plotPtrsite(0){
	RendererManger.clear();
}
/**
* @brief DataSourceManage::init 数据管理初始化
* @param ListTreeWidget* ptr
* @void
*/
void DataSourceManage::init(ListTreeWidget* ptr,Plot* _plot){

	unsigned long long treeSite = reinterpret_cast<unsigned long long>(ptr);
	unsigned long long plotSite = reinterpret_cast<unsigned long long>(_plot);
	if (treeSite != 0 && treePtrsite!=treeSite)
	{
		connect(this, SIGNAL(_loadhdflist(std::vector<Hdf5Data>&)), ptr, SLOT(loadHdflist(std::vector<Hdf5Data>&)));
		connect(ptr, SIGNAL(_transfromRenderer(std::string, int)), this, SLOT(tranfromRenderer(std::string, int)));
		connect(this, SIGNAL(toTreeNewData(Hdf5Data&, int)), ptr, SLOT(fromdataManageNewData(Hdf5Data& , int )));
		treePtrsite = treeSite;
	}
	if (plotSite!=0&& plotPtrsite!=plotSite)
	{
		connect(this, SIGNAL(_reRendererEvent(std::shared_ptr<PlotAdapter>)), _plot, SLOT(reRendererEvent(std::shared_ptr<PlotAdapter>)));
		plotPtrsite = plotSite;
	}
}
/**
* @brief DataSourceManage::initStructData 传入结构体数据
* @param Hdf5Data data 结构图数据
* @return void
*/
int DataSourceManage::initStructData(Hdf5Data& data)
{
	hdfDatelist.push_back(data);
	structData = data;
	structindex=hdfDatelist.size()-1;
	if (factoryptr)
		factoryptr->setStructData(data);
	else
		factoryptr = std::shared_ptr<RendererFactory>(new RendererFactory(data));
	return structindex;
}
DataSourceManage::~DataSourceManage(){
	RendererManger.clear();
}
/**
* @brief DataSourceManage::DisPlayPlot 送显
* @oaram Hdf5Data data 送显数据
* @param int _type 方向
* @return void
*/
void DataSourceManage::DisPlayPlot(Hdf5Data data, int _type)
{
	auto adapter = factoryptr->creatPlotAdapter(data, (DirectionType)_type);
	//保存当前的hdf5Data
	hdfDatelist.push_back(data);
	emit toTreeNewData(data, hdfDatelist.size() - 1);
	emit _reRendererEvent(adapter);
}

/**
* @brief  DataSourceManage::DataClear 清除数据
* @return void  
*/
void DataSourceManage::DataClear()
{
	RendererManger.clear();
	hdfDatelist.clear();
}
///**
//* @brief  DataSourceManage::isbind 是否绑定
//* @return bool  
//*/
//bool DataSourceManage::isbind()
//{
//	//if (p == nullptr || treePtr == nullptr)
//	//	return false;
//	//else
//		return true;
//}
#include "moc_Dataresource.cpp"