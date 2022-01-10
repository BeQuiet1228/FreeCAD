#pragma once
#include <QWidget>
#include "../ConfigUnify.h"
namespace Ui
{
	class Contour3dConfigWidget;
};
namespace DV
{
	class ColorBarWidget;
};
namespace DV3D
{
	class Contour3dConfigWidget :public QWidget,public DV::ConfigUnify
	{
	public:
		explicit Contour3dConfigWidget(QWidget* parent=nullptr);
		~Contour3dConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	private:
		Ui::Contour3dConfigWidget* ui;
		DV::ColorBarWidget* mColorBarWidget;
	};
};