#pragma once
#include <QWidget>
#include "../ConfigUnify.h"

namespace Ui
{
	class Contour3dConfigWidget;
};
class QBoxLayout;
namespace DV
{
	class ArrowCtrl;
	class ColorTab;
};
namespace DV3D
{
	class ControlerConfigWidget;
	class Contour3dConfigWidget :public QWidget,public DV::ConfigUnify
	{
		Q_OBJECT
	public:
		explicit Contour3dConfigWidget(QWidget* parent=nullptr);
		~Contour3dConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::Contour3dConfigWidget* ui;
		ControlerConfigWidget* controlerConfigWidget;
		QBoxLayout* boxLayout;
		DV::ColorTab* mColorTab;
		DV::ArrowCtrl* arrowCtrl;
	};
};