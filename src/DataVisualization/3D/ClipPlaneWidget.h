#pragma once
#include <QDialog>
#include <QWidget>
#include <memory>
namespace Ui
{
	class ClipPlaneWidget;
}
namespace DV3D {
	class Controler;
	class ClipPlaneWidget :public QDialog
	{
		Q_OBJECT
	public:
		explicit ClipPlaneWidget(QWidget* parent = nullptr);
		~ClipPlaneWidget();
	public:
		void setControler(std::shared_ptr<Controler> controler);
	private Q_SLOTS:
		void BtnClicked();
	private:
		std::shared_ptr<Controler> controlerPtr;
		Ui::ClipPlaneWidget* ui;
	};
}
