#pragma once
#include <QWidget>
#include <map>
#include <QListWidgetItem>
namespace Ui {
	class ControlerItemListWidget;
}

namespace DV3D {
	class ControlerItem;
	class Controler;
}

namespace Gui {
	class ControlerItemListWidget :public QWidget{
		Q_OBJECT
	public:
		ControlerItemListWidget(QWidget* parent = 0);
		~ControlerItemListWidget() = default;

	private:
		Ui::ControlerItemListWidget *ui;

	public:
		void addWidget(DV3D::ControlerItem* widget);
		void clearWidget();

		//¸ù¾Ý¿ØÖÆÆ÷ÒÆ³ýitem
		void removeControlerItemWithControler(DV3D::Controler* controler);
	private:
		void addItemWidget(DV3D::ControlerItem* widget, QListWidgetItem* item);
		//ÒÆ³ýitem
		void removeControlerItem(DV3D::ControlerItem* controlerItem);
	private:
		std::map<DV3D::ControlerItem*, QListWidgetItem*> widgetMap;

	public Q_SLOTS:
		void itemClose();
	};

	//¶ÔÐü¸¡´°¿Ú²Ù×÷
	ControlerItemListWidget* getControlerListWidget();
	ControlerItemListWidget* CreatControlerListWidget();
	void hideControlerListWidget();
	void showControlerListWidget();

}