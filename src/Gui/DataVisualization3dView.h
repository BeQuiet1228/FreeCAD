#pragma once
#include "MDIEditView.h"
#include "DocumentPic.h"
#include "DataVisualization/3D/widget3D.h"
namespace Gui {
	/*
		3d后处理Gui窗口
	*/
	class DataVisualizationView :public MDIViewPIC{
	public:
		DataVisualizationView(DocumentPic* doc);
		~DataVisualizationView() = default;

		DV3D::Widget3D* getWidget3D();
	private:
		void initGui();

	protected:
		void closeEvent(QCloseEvent* e);
	private:
		DV3D::Widget3D *widget3d;
	};
}