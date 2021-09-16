#pragma once
#include "MDIEditView.h"
#include <QHBoxLayout>
class ParticleSwarmOptimizationMDI :public MDIViewPIC {
public:
	ParticleSwarmOptimizationMDI(DocumentPic* pcDocument, QWidget* parent = 0);
	~ParticleSwarmOptimizationMDI();

public:
	//初始化优化模块
	void init(const std::string& path);

};

class ProcessingBatchView :public MDIViewPIC{
public:
	ProcessingBatchView(DocumentPic* pcDocument, QWidget* parent = 0);
	~ProcessingBatchView() = default;
public:
	void init(const std::string& path);
};