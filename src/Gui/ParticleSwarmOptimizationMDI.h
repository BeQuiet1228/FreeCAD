#pragma once
#include "MDIView.h"
#include <QHBoxLayout>
class ParticleSwarmOptimizationMDI :public Gui::MDIView {
public:
	ParticleSwarmOptimizationMDI(Gui::Document* pcDocument, QWidget* parent = 0, Qt::WindowFlags wflags = 0);
	~ParticleSwarmOptimizationMDI();

public:
	//初始化优化模块
	void init(const std::string& path);

};