#include "Dataresource.h"
void DataSourceManage::tranfromRenderer(std::string name,Hdf5Data data){
	auto iter = RendererManger.find(name);
	if (iter!=RendererManger.end())
	{
		std::shared_ptr<Renderer> rd = std::dynamic_pointer_cast<Renderer>(iter->second);
	}
	else
	{
		Renderer* renderer = CreateRendererList(data);
		std::shared_ptr<Renderer> rd(renderer);
		//先装入队列
		RendererManger[name] = rd;
	}
}

Renderer* DataSourceManage::CreateRendererList(Hdf5Data data){
	//从工厂获取到相关的渲染器
	Renderer* render;
	return render;
}

void DataSourceManage::clearMap(){
	RendererManger.clear();
}


void DataSourceManage::loadhdffile(std::string filepath)
{
	Hdf5IO io(filepath);
	io.initHdf5Data();
	//获取到hdf5文件
	std::vector<Hdf5Data> _hdfDatelist = io.hdf5DataList;
	//深度交换
	hdfDatelist.swap(_hdfDatelist);
}
//std::map<Hdf5Data, Renderer*> RendererManger;
