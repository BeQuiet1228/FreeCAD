#pragma once
#include "QWidget"
#include "exportConfig.hpp"
class QBoxLayout;
namespace DV
{
	class ColorTab;
	class ArrowCtrl;
	class DATA_VISUALIZATION_EXPORT ColorBarWidget :public QWidget
	{
		Q_OBJECT
	public:
		explicit ColorBarWidget(QWidget* parent=nullptr);
		~ColorBarWidget();
	public:
		std::vector<float> getValue();
		std::vector<QColor> getColors(std::vector<float>&);
	protected:
		void initUi();
	private:
		QBoxLayout* boxLayout;
		ColorTab* mColorTab;
		ArrowCtrl* arrowCtrl;
	};
}