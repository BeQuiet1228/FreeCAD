#include "ClipPlaneWidget.h"
#include "ui_ClipPlaneWidget.h"
#include "controler.h"
#include "vtkPlane.h"
#include "actorPipeline.h"
#include "QString"
DV3D::ClipPlaneWidget::ClipPlaneWidget(QWidget* parent /*= nullptr*/) :
	QDialog(parent), ui(new Ui::ClipPlaneWidget)
{
	ui->setupUi(this);
	//setWindowFlags(Qt::CustomizeWindowHint | Qt::WindowMinimizeButtonHint | Qt::WindowMaximizeButtonHint);
	connect(ui->okButton,SIGNAL(clicked()),this,SLOT(BtnClicked()));
}

DV3D::ClipPlaneWidget::~ClipPlaneWidget()
{

}


void DV3D::ClipPlaneWidget::setControler(std::shared_ptr<Controler> controler)
{
	controlerPtr = controler;
	vtkSmartPointer<vtkPlane> planeptr;
	controler->getActorPipeline()->getClipPlane(planeptr);
	auto centerPoint = planeptr->GetOrigin();
	auto normalPoint = planeptr->GetNormal();
	//获取点
	ui->centerX->setText(QString("%1").arg(centerPoint[0]));
	ui->centerY->setText(QString("%1").arg(centerPoint[1]));
	ui->centerZ->setText(QString("%1").arg(centerPoint[2]));
	//获取法向
	ui->normalX->setText(QString("%1").arg(normalPoint[0]));
	ui->normalY->setText(QString("%1").arg(normalPoint[1]));
	ui->normalZ->setText(QString("%1").arg(normalPoint[2]));
}

void DV3D::ClipPlaneWidget::BtnClicked()
{
	if (sender() == ui->okButton)
	{
		//获取点位
		double center_X = ui->centerX->text().toDouble();
		double center_Y = ui->centerY->text().toDouble();
		double center_Z = ui->centerZ->text().toDouble();
		//获取法向
		double normal_X = ui->normalX->text().toDouble();
		double normal_Y = ui->normalY->text().toDouble();
		double normal_Z = ui->normalZ->text().toDouble();
		//设置Palne
		vtkSmartPointer<vtkPlane> planeF = vtkSmartPointer<vtkPlane>::New();
		planeF->SetOrigin(center_X, center_Y, center_Z);
		planeF->SetNormal(normal_X, normal_Y, normal_Z);
		controlerPtr->getActorPipeline()->setClipPlane(planeF);
	}
}
