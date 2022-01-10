#include "ConfigUnify.h"
#include "QPushButton"
#include "QColorDialog"
#include "QPalette"
#include "C_encoding.h"
/**
* @time	2022/01/10
* @brief DV::ConfigUnify::SetAllreRenderer 设置按钮为可渲染
* @param QPushButton * button
* @return void
*/
void DV::ConfigUnify::SetAllreRenderer(QPushButton* button)
{
	button->setAutoFillBackground(true);
	button->setFlat(true);
}

QColor DV::ConfigUnify::setButtonColor(QPushButton* button)
{
	QColor lastColor = button->palette().button().color();
	{
		QColorDialog dlg;
		dlg.setOptions(QColorDialog::ShowAlphaChannel);
		dlg.setCurrentColor(lastColor);
		if (dlg.exec() == QColorDialog::Accepted)
		{
			QColor color = dlg.currentColor();
			QPalette qpalette = button->palette();
			qpalette.setColor(QPalette::Button,color);
			button->setPalette(qpalette);
			button->setText(QString("#%1").arg(QColorToQstring(color)));
			return color;
		}
	}
	return lastColor;
}
QColor DV::ConfigUnify::setButtonColor(QPushButton* button, std::string color)
{
	QColor rgba = QStringToQColor(QString::fromStdString(color));
	QPalette qpalette = button->palette();
	qpalette.setColor(QPalette::Button, rgba);
	button->setPalette(qpalette);
	button->setText(QString("#%1").arg(QString::fromStdString(color)));
	return rgba;
}
std::string DV::ConfigUnify::getButtonColorstr(QPushButton* button)
{
	QColor lastColor = button->palette().button().color();
	auto qstr=QColorToQstring(lastColor);
	return qstr.toStdString();
}
