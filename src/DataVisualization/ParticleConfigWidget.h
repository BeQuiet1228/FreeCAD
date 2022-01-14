#pragma once
#include "QWidget"
#include "ConfigUnify.h"
namespace Ui
{
	class ParticleConfigWidget;
};
namespace DV
{
	class ParticleConfigWidget :public QWidget, public ConfigUnify
	{
		Q_OBJECT
	public:
		explicit ParticleConfigWidget(QWidget* parent = nullptr);
		~ParticleConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::ParticleConfigWidget* ui;
	};
}