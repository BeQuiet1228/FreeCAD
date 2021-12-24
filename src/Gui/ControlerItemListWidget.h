#pragma once
#include <QWidget>
#include <map>
#include <QListWidgetItem>
namespace Ui {
	class ControlerItemListWidget;
}

namespace DV3D {
	class ControlerItem;
}

namespace Gui {
	class ControlerItemListWidget :public QWidget{
		Q_OBJECT
	public:
		ControlerItemListWidget(QWidget* parent = 0);
		~ControlerItemListWidget() = default;

	private:
		::Ui::ControlerItemListWidget *ui;

	public:
		void addWidget(DV3D::ControlerItem* widget);
		void clearWidget();

	private:
		void addItemWidget(DV3D::ControlerItem* widget, QListWidgetItem* item);

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