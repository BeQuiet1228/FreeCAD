#pragma once
#include <QWidget>
#include <memory>
#include <QToolButton>
#include <map>
#include "DataVisualization3DExport.hpp"
#include <QResizeEvent>
namespace Ui {
	class ControlerItem ;
}
namespace DV3D {
	class Controler;
	class ControlerAction;

	using ToolButtonMap = std::map<QToolButton*, std::shared_ptr<ControlerAction>>;

	class DATA_VISUALIZATION_3D_EXPORT ControlerItem :public QWidget{
		Q_OBJECT
	public:
		ControlerItem(QWidget* parent =0);
		~ControlerItem();

	public:
		//set get
		std::shared_ptr<Controler> getControler();
		void setControler(std::shared_ptr<Controler> controler);

		//添加action
		void addAction(std::shared_ptr<ControlerAction> action);
		void setName(const QString& name);
	protected:
		void resizeEvent(QResizeEvent* event);
	private:
		void initGui();


	private:
		Ui::ControlerItem* ui;

		//控制器
		std::shared_ptr<Controler> controler;
		//按钮
		ToolButtonMap toolButtonMap;
		//控制模型是否可见
		std::shared_ptr<ControlerAction> visibleAction;
	public Q_SLOTS:
		void toolButtonClicked(bool);
		void transParentSliderValueChange(int value);
		void closeButtonClicked(bool);
	 Q_SIGNALS:
		 void itemClose();

	};
}