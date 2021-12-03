#pragma once
#include <QWidget>
#include <memory>
#include <QToolButton>
#include <map>
namespace Ui {
	class ControlerItem ;
}
namespace DV3D {
	class Controler;
	class ControlerAction;

	using ToolButtonMap = std::map<QToolButton*, std::shared_ptr<ControlerAction>>;

	class ControlerItem :public QWidget{
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
	private:
		Ui::ControlerItem* ui;

		//控制器
		std::shared_ptr<Controler> controler;
		//按钮
		ToolButtonMap toolButtonMap;
		//控制模型是否可见
		std::shared_ptr<ControlerAction> visibleAction;
	public slots:
		void toolButtonClicked(bool);
		void transParentSliderValueChange(int value);

	};
}