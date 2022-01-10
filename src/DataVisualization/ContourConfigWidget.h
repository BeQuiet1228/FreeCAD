#pragma once
#include "QWidget"
#include "ConfigUnify.h"
namespace Ui
{
	class ContourConfigWidget;
};
class QBoxLayout;
namespace DV
{
	class ColorTab;
	class ArrowCtrl;
	class ContourConfigWidget :public QWidget, public ConfigUnify
	{
		Q_OBJECT
	public:
		explicit ContourConfigWidget(QWidget* parent = nullptr);
		~ContourConfigWidget();
	public:
		void loadConfig();
		void saveConfig();
	protected:
		void initUi();
	protected Q_SLOTS:
		void btnClicked();
	private:
		Ui::ContourConfigWidget* ui;
		QBoxLayout* boxLayout;
		ColorTab* mColorTab;
		ArrowCtrl* arrowCtrl;
	};
}