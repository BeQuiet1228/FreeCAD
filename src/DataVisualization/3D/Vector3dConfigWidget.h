#pragma once
#include <QWidget>
#include "../ConfigUnify.h"
namespace Ui
{
	class Vector3dConfigWidget;
};
class QBoxLayout;
namespace DV
{
	class ArrowCtrl;
	class ColorTab;
};
namespace DV3D
{
	class Vector3dConfigWidget :public QWidget, public DV::ConfigUnify
	{
		Q_OBJECT
	public:
		explicit Vector3dConfigWidget(QWidget* parent = nullptr);
		~Vector3dConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::Vector3dConfigWidget* ui;
		QBoxLayout* boxLayout;
		DV::ColorTab* mColorTab;
		DV::ArrowCtrl* arrowCtrl;
	};
};