#pragma once
#include <QWidget>
#include "../ConfigUnify.h"
#include"XmlGroup3D.h"
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
		void loadConfig(XmlData::ControlerXml&);
		void saveConfig(XmlData::ControlerXml&);

		void setParentGroup(std::string);
	protected Q_SLOTS:
		void slotSliderChange(int);
	private:
		Ui::ControlerConfigWidget* ui;
		std::string parentGroup;
	};
}
