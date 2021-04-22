#include "Dataresource.h"
#include "RendererFactory.h"
#include "Plot.h"
//#include "ListTreeWidget.h"
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
	
	auto iter = RendererManger.find(name);
	if (iter!=RendererManger.end())
	{
		Renderers rd = iter->second;
		emit _reRendererEvent(rd);
	}
	else
	{
		//如果是结构图需要另外处理
		//int structindex = RendererFactory::findStructDataIndex(hdfDatelist);
		/*if (index==structindex)
		{*/
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
			Renderers rd = CreateRenderer(hdfDatelist[index], type);
			RendererManger[name] = rd;
			emit _reRendererEvent(rd);
			return;
		}
		Renderers renderer = CreateRendererList(hdfDatelist[index]);
		//先装入队列
		RendererManger[name] = renderer;
		emit _reRendererEvent(renderer);
	}
}

Renderers DataSourceManage::CreateRenderer(Hdf5Data data, int _type)
{
	Renderers rds = factoryptr->creatRenderers(data, (DirectionType)_type);
	return rds;
}
/**
* @brief DataSourceManage::CreateRendererList 获取渲染器
* @param Hdf5Data data
* @return RendererPtr
*/
Renderers DataSourceManage::CreateRendererList(Hdf5Data data){
	//从工厂获取到相关的渲染器
	//RendererPtr rd = RendererFactory::creatRenderer(data);
	Hdf5Data _data(data);
	Renderers rd=factoryptr->creatRenderers(data);
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
	Hdf5Data structDate(hdfDatelist.at(structindex));
	factoryptr = new RendererFactory(structDate);
	/****************************************************/
	_hdf5io = io;
}
/**
* @brief DataSourceManage::DataSourceManage 数据管理构造
*/
DataSourceManage::DataSourceManage(){
	RendererManger.clear();
}
/**
* @brief DataSourceManage::init 数据管理初始化
* @param ListTreeWidget* ptr
* @void
*/
void DataSourceManage::init(ListTreeWidget* ptr,Plot* _plot){

	//进行连接
	connect(this, SIGNAL(_loadhdflist(std::vector<Hdf5Data>&)), ptr, SLOT(loadHdflist(std::vector<Hdf5Data>&)));
	connect(ptr, SIGNAL(_transfromRenderer(std::string,int)), this, SLOT(tranfromRenderer(std::string,int)));
	/*p = new Plot();
	p->resize(400, 300);
	p->show();*/
	p = _plot;
	if (p)
	{
		void _reRendererEvent(const std::list<std::shared_ptr<Renderer>>& listRender);
		connect(this, SIGNAL(_reRendererEvent(const std::list<std::shared_ptr<Renderer>>&)), p, SLOT(reRendererEvent(const std::list<std::shared_ptr<Renderer>>&)));
		//p->show();
	}
}
void DataSourceManage::initStructData(Hdf5Data data)
{
	//int structindex = RendererFactory::findStructDataIndex(hdfDatelist);
	//Hdf5Data structDate(hdfDatelist.at(structindex));
	factoryptr = new RendererFactory(data);
}
DataSourceManage::~DataSourceManage(){
	RendererManger.clear();
}
void DataSourceManage::DisPlayPlot(Hdf5Data data, int _type)
{
	Renderers rds = factoryptr->creatRenderers(data, (DirectionType)_type);
	emit _reRendererEvent(rds);
}
//std::map<Hdf5Data, Renderer*> RendererManger;
#include "moc_Dataresource.cpp"