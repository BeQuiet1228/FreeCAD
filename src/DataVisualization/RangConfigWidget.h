#pragma once
#include "QWidget"
#include "ConfigUnify.h"
namespace Ui
{
	class RangConfigWidget;
};
namespace DV
{
	class RangConfigWidget :public QWidget, public ConfigUnify
	{
		Q_OBJECT
	public:
		explicit RangConfigWidget(QWidget* parent = nullptr);
		~RangConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::RangConfigWidget* ui;
	};
}