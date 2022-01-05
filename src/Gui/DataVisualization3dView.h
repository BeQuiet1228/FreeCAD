#pragma once
#include "MDIEditView.h"
#include "DocumentPic.h"
#include "DataVisualization/3D/widget3D.h"
#include "DataVisualization/3D/controler.h"
#include <memory>
namespace Gui {
	/*
		3d后处理Gui窗口
	*/
	class DataVisualizationView :public MDIViewPIC{
	public:
		DataVisualizationView(DocumentPic* doc);
		~DataVisualizationView() = default;

		DV3D::Widget3D* getWidget3D();

		//添加控制器
		void addControler(std::shared_ptr<DV3D::Controler> controler);
	private:
		void initGui();
		//移除结构图
		void removeStructControler();
		//移除除结构图外其他图
		void removeOtherControler();
		//移除listWidget中的item
		void removeControlerItemWidget(DV3D::Controler* controler);
	protected:
		void closeEvent(QCloseEvent* e);
	private:
		DV3D::Widget3D *widget3d;
	};
}