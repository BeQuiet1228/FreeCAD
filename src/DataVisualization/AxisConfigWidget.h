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
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::AxisConfigWidget* ui;
	};
}