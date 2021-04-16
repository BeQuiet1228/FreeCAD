#include "Dataresource.h"


//结构图的方向
enum stru_dir
{
	PIN_Z=0,
	Z_R,
	R_PIN,
};
std::string StructDirection[] = { "Phi-Z",
"Z-R",
"R*cos(Phi)-R*sin(Phi)"};
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
		/*	rd->dataInit();
			rd->setDefaultRang();*/
		p.addRenderer(rd);
		p.reRender();
	}
	else
	{
		//如果是结构图需要另外处理
		int structindex = RendererFactory::findStructDataIndex(hdfDatelist);
		if (index==structindex)
		{
			DirectionType type=R_Z;
			int index_dir = 0;
			for (auto i = 0; i < 3;i++)
			{
				if (name.find(StructDirection[i])!=std::string::npos)
				{
					index_dir = i;
					break;
				}
			}
			switch (index_dir)
			{
			case PIN_Z:
				type = R_Z; break;
			case Z_R:
				type = R_Z; break;
			case R_PIN:
				type = R_THETA; break;
			default:
				break;
			}
			//是结构体
			Renderers rd = CreateRenderer(hdfDatelist[index], type);
			RendererManger[name] = rd;
			p.addRenderer(rd);
			p.reRender();
			return;
		}
		Renderers renderer = CreateRendererList(hdfDatelist[index]);
		//先装入队列
		RendererManger[name] = renderer;
		/*renderer->dataInit();
		renderer->setDefaultRang();*/
		p.addRenderer(renderer);
		p.reRender();
	}
}

Renderers DataSourceManage::CreateRenderer(Hdf5Data data, DirectionType _type)
{
	Renderers rds;
	RendererPtr rd = factoryptr->creatStructRender(data,_type);
	rds.push_back(rd);
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
	if (data.name.find("CONTOUR")!=std::string::npos)
	{

	}
	else if (data.name.find("PHASEPACE")!=std::string::npos)
	{

	}
	else if (data.name.find("RANGE")!=std::string::npos)
	{

	}
	else if (data.name.find("VECTOR")!=std::string::npos)
	{

	}
	else if (data.name.find("struct")!=std::string::npos)
	{
	}

	Renderers rd=factoryptr->creatRenderers(data);
	//RendererPtr rd = RendererFactory::creatStructRender(data, R_Z);
	//RendererFactory factor();
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
	int structindex = RendererFactory::findStructDataIndex(hdfDatelist);
	Hdf5Data structDate(hdfDatelist.at(structindex));
	factoryptr = new RendererFactory(structDate);
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
void DataSourceManage::init(ListTreeWidget* ptr){

	//进行连接
	connect(this, SIGNAL(_loadhdflist(std::vector<Hdf5Data>&)), ptr, SLOT(loadHdflist(std::vector<Hdf5Data>&)));
	connect(ptr, SIGNAL(_transfromRenderer(std::string,int)), this, SLOT(tranfromRenderer(std::string,int)));
	p.resize(400, 300);
	p.show();
}
//std::map<Hdf5Data, Renderer*> RendererManger;
#include "moc_Dataresource.cpp"