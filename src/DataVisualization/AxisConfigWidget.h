#pragma once
#include "QWidget"
#include "ConfigUnify.h"
namespace Ui
{
	class AxisConfigWidget;
};
namespace DV
{
	class AxisConfigWidget :public QWidget, public ConfigUnify
	{
		Q_OBJECT
	public:
		explicit AxisConfigWidget(QWidget* parent = nullptr);
		~AxisConfigWidget();
	protected:
		void initUi();
	private:
		Ui::AxisConfigWidget* ui;
	};
}