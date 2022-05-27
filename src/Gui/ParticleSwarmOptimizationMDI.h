#pragma once
//#include "MDIEditView.h"
#include "AlgorMDIInter.h"
#include <QHBoxLayout>
class ParticleSwarmOptimizationMDI :public AlgorMDIInter {
public:
	ParticleSwarmOptimizationMDI(DocumentPic* pcDocument, QWidget* parent = 0);
	~ParticleSwarmOptimizationMDI();

public:
	//初始化优化模块
	void init(const std::string& path);
	virtual bool isClose() override;
	QWidget* smartControlWidget;
};

class GeneticAlgorithmView :public ParticleSwarmOptimizationMDI {
public:
	GeneticAlgorithmView(DocumentPic* pcDocument, QWidget* parent = 0);
	~GeneticAlgorithmView();
public:
	//初始化优化模块
	void init(const std::string& path);

};

class ProcessingBatchView :public AlgorMDIInter {
public:
	ProcessingBatchView(DocumentPic* pcDocument, QWidget* parent = 0);
	~ProcessingBatchView() = default;
public:
	void init(const std::string& path);
	virtual bool isClose() override;
	QWidget* calcWidget;
};