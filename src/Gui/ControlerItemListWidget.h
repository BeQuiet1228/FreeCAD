#pragma once
#include <QWidget>

namespace Ui {
	class ControlerItemListWidget;
}

namespace Gui {
	class ControlerItemListWidget :public QWidget{
	public:
		ControlerItemListWidget(QWidget* parent = 0);
		~ControlerItemListWidget() = default;

	private:
		::Ui::ControlerItemListWidget *ui;

	public:
		void addWidget(QWidget* widget);
		void clearWidget();

	};

	//¶ÔÐü¸¡´°¿Ú²Ù×÷
	ControlerItemListWidget* getControlerListWidget();
	ControlerItemListWidget* CreatControlerListWidget();
	void hideControlerListWidget();
	void showControlerListWidget();

}