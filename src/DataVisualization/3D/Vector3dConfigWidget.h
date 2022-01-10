#pragma once
#include <QWidget>
#include "../ConfigUnify.h"
namespace Ui
{
	class Vector3dConfigWidget;
};
namespace DV3D
{
	class Vector3dConfigWidget :public QWidget,public DV::ConfigUnify
	{
	public:
		explicit Vector3dConfigWidget(QWidget* parent=nullptr);
		~Vector3dConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	private:
		Ui::Vector3dConfigWidget* ui;
	};
};