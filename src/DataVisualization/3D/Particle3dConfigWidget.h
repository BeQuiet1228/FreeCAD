#pragma once
#include <QWidget>
#include "../ConfigUnify.h"
namespace Ui
{
	class Particle3dConfigWidget;
};
namespace DV3D
{
	class Particle3dConfigWidget :public QWidget,public DV::ConfigUnify
	{
		Q_OBJECT
	public:
		explicit Particle3dConfigWidget(QWidget* parent=nullptr);
		~Particle3dConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::Particle3dConfigWidget* ui;
	};
};