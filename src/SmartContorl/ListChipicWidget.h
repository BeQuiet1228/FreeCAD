#pragma once
#include <QListWidget>
namespace SMC{
	class ListChipicWidget :public QListWidget{
		Q_OBJECT
	public:
		ListChipicWidget(QWidget* parent = 0);
		~ListChipicWidget();

	public Q_SLOTS:
		void addListWidgetItem(QListWidgetItem* item, QWidget* widget);
	};
}