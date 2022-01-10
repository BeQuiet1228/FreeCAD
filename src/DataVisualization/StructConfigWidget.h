#pragma once
#include "QWidget"
#include "ConfigUnify.h"
#include "CustomConfig.h"
namespace Ui
{
	class StructConfigWidget;
};
class StructButton;
namespace DV
{
	class StructConfigWidget :public QWidget, public ConfigUnify
	{
		Q_OBJECT
	public:
		explicit StructConfigWidget(QWidget* parent = nullptr);
		~StructConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
		void saveData(ConfigGroup&,StructButton*);
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::StructConfigWidget* ui;
		std::list<StructButton*> btnList;
	};
}