#pragma once
#include <QWidget>
#include "../ConfigUnify.h"
namespace Ui
{
	class ControlerConfigWidget;
}
namespace DV3D
{
	class ControlerConfigWidget :public QWidget, public DV::ConfigUnify
	{
		Q_OBJECT
	public:
		explicit ControlerConfigWidget(QWidget* parent);
		~ControlerConfigWidget();
	public:
		void initUi();
		void loadConfig();
		void saveConfig();
		void setParentGroup(std::string);
	protected Q_SLOTS:
		void slotSliderChange(int);
	private:
		Ui::ControlerConfigWidget* ui;
		std::string parentGroup;
	};
}
