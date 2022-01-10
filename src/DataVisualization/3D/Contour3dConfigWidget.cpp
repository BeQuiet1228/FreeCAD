#include "Contour3dConfigWidget.h"
#include "ui_Contour3dConfigWidget.h"
#include "../ColorBarWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
DV3D::Contour3dConfigWidget::Contour3dConfigWidget(QWidget* parent/*=nullptr*/)
	:QWidget(parent),ui(new Ui::Contour3dConfigWidget)
{
	ui->setupUi(this);
	initUi();
}
DV3D::Contour3dConfigWidget::~Contour3dConfigWidget()
{

}
void DV3D::Contour3dConfigWidget::loadConfig()
{

}
void DV3D::Contour3dConfigWidget::saveConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto contourGroup = Group.getGroup("contour3d");
	/*
		3Œ¨µ»ŒªÕº
	*/
	std::vector<float> values = mColorBarWidget->getValue();
	std::vector<QColor> colors = mColorBarWidget->getColors(values);
	contourGroup.
		setSetting("valueNumber"
			,QString("%1")
			.arg(values.size())
			.toStdString());
	for (auto index = 0; index < values.size(); index++)
	{
		contourGroup
			.getGroup(QString("level_%1").arg(index).toStdString())
			.setSetting("value", QString("%1").arg(values[index]).toStdString());
		contourGroup
			.getGroup(QString("level_%1").arg(index).toStdString())
			.setSetting("color", DV::QColorToQstring(colors[index]).toStdString());
	}
}
void DV3D::Contour3dConfigWidget::initUi()
{
	mColorBarWidget = new DV::ColorBarWidget(ui->colorScalar);
}