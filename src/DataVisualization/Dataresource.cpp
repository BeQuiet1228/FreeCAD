#include "Dataresource.h"

void DataSourceManage::tranfromRenderer(std::string name,Hdf5Data data){
	auto iter = RendererManger.find(name);
	if (iter!=RendererManger.end())
	{
		RendererPtr rd = iter->second;
		/*	rd->dataInit();
			rd->setDefaultRang();*/
		p.setMainRenderer(rd);
		p.update();
	}
	else
	{
		RendererPtr renderer = CreateRendererList(data);
		//先装入队列
		RendererManger[name] = renderer;
		renderer->dataInit();
		renderer->setDefaultRang();
		p.setMainRenderer(renderer);
		p.update();
	}
}

RendererPtr DataSourceManage::CreateRendererList(Hdf5Data data){
	//从工厂获取到相关的渲染器
	//RendererPtr rd = RendererFactory::creatRenderer(data);
	RendererPtr rd = RendererFactory::creatStructRender(data,R_THETA);
	return rd;
}

void DataSourceManage::clearMap(){
	//RendererManger.clear();
}


void DataSourceManage::loadhdffile(std::string filepath)
{
	Hdf5IO io(filepath);
	io.initHdf5Data();
	//获取到hdf5文件
	std::vector<Hdf5Data> _hdfDatelist = io.hdf5DataList;
	emit _loadhdflist(_hdfDatelist);
	//深度交换
	hdfDatelist.swap(_hdfDatelist);
	
}

DataSourceManage::DataSourceManage(){
	RendererManger.clear();

}

void DataSourceManage::init(){
	p.resize(400, 300);
	p.show();
}
//std::map<Hdf5Data, Renderer*> RendererManger;
#include "moc_Dataresource.cpp"