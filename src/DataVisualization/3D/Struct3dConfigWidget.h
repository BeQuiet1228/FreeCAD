#pragma once
#include <QWidget>
#include "../ConfigUnify.h"
namespace Ui
{
	class Struct3dConfigWidget;
}
namespace DV3D
{
	class Struct3dConfigWidget :public QWidget,public DV::ConfigUnify
	{
		Q_OBJECT
	public :
		explicit Struct3dConfigWidget(QWidget* parent=nullptr);
		~Struct3dConfigWidget();
	public :
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::Struct3dConfigWidget* ui;
	};
}