#pragma once
#include <memory>
class Renderer;
class RenderTask{
public:
	enum TaskType{
		MAP = 0,	//渲染图表
		FIND_POINT	//取点
	};
public: 
	explicit RenderTask(const std::shared_ptr<Renderer> rder,const TaskType type = MAP,
		const unsigned int rank = 0);
	~RenderTask();

	//类型操作
	void setType(const TaskType& type){
		this->type = type;
	}
	TaskType getTyepe(){
		return this->type;
	}
	//渲染器操作
	void setRenderer(std::shared_ptr<Renderer> renderer){
		this->renderer = renderer;
	};
	std::shared_ptr<Renderer> getRenderer(){
		return this->renderer;
	}

public:
	unsigned int rank;

private:
	//类型
	TaskType type;
	//渲染器
	std::shared_ptr<Renderer> renderer;

};