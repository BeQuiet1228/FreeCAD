#pragma once
#include "QWidget"
#include "ConfigUnify.h"
namespace Ui
{
	class VectorConfigWidget;
};
namespace DV
{
	class VectorConfigWidget :public QWidget, public ConfigUnify
	{
		Q_OBJECT
	public:
		explicit VectorConfigWidget(QWidget* parent = nullptr);
		~VectorConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::VectorConfigWidget* ui;
	};
}