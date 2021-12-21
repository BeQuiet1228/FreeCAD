#pragma once
#include <QDialog>
#include <QWidget>
namespace Ui
{
	class ClipPlaneWidget;
}
namespace DV3D {
	class ClipPlaneWidget :public QDialog
	{
		Q_OBJECT
	public:
		explicit ClipPlaneWidget(QWidget* parent = nullptr);
		~ClipPlaneWidget();
	private Q_SLOTS:
		void BtnClicked();
	private:
		Ui::ClipPlaneWidget* ui;
	};
}
