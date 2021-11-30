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

		//Ìí¼Óaction
		void addAction(std::shared_ptr<ControlerAction> action);
	private:
		Ui::ControlerItem* ui;

		//¿ØÖÆÆ÷
		std::shared_ptr<Controler> controler;
		//°´Å¥
		ToolButtonMap toolButtonMap;

	public slots:
		void toolButtonClicked(bool);
		void transParentSliderValueChange(int value);

	};
}