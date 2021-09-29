#include"Widget3D.h"
#include"vtk-7.0/vtkAutoInit.h"
#include"vtk-7.0/vtkRenderer.h"
#include"vtk-7.0/vtkPolyData.h"
#include"vtk-7.0/vtkSmartPointer.h"
#include"vtk-7.0/vtkActor.h"
#include"vtk-7.0/vtkPolyDataMapper.h"
#include"vtk-7.0/vtkProperty.h"
#include"vtk-7.0/QVTKWidget.h"
#include"vtk-7.0/vtkRenderWindow.h"
#include"qcheckbox.h"
#include"qgridlayout.h"
#include"qpalette.h"
#include"qdebug.h"
Widget3D::Widget3D(QWidget* parent) :QWidget(parent) {
	initUi();
}
Widget3D::~Widget3D(){

}
void Widget3D::transfromPolyData(__int64 porPer,vtkPolyData* polyData)
{
	if (0 == polyData->GetNumberOfCells() || 0 == polyData->GetNumberOfPoints())
		return;
	vtkSmartPointer<vtkPolyData> curData = vtkSmartPointer<vtkPolyData>::New();
	curData->ShallowCopy(polyData);
	vtkSmartPointer<vtkPolyDataMapper> mapper = vtkSmartPointer<vtkPolyDataMapper>::New();
	mapper->SetInputData(curData);
	mapper->ScalarVisibilityOff();
	vtkSmartPointer<vtkActor> actor = vtkSmartPointer<vtkActor>::New();
	actor->SetMapper(mapper);
	actor->GetProperty()->SetColor(0.5,0.5,0.5);
	actorS[porPer] = actor;
	render->AddActor(actor);
	QCheckBox* checkBox = new QCheckBox(mVtkWidget);
	checkBox->setText(QString("%1").arg(porPer));
	checkBox->setCheckState(Qt::CheckState::Checked);
	checkBox->setMinimumSize(32, 32);
	checks[porPer] = checkBox;
	layout->addWidget(checkBox);
	connect(checkBox,SIGNAL(stateChanged(int)),this, SLOT(slotStateChanged(int)));
}
void Widget3D::resizeEvent(QResizeEvent*)
{
	mVtkWidget->resize(this->size());
	QSize subsize = QSize(this->size().width()/9,this->size().height());
	subwidget->resize(subsize);
	subwidget->move(QPoint(0, 0));
}
void Widget3D::Updata()
{
}
void Widget3D::drawImage()
{
	render->SetBackground(1,1,1);
}

void Widget3D::initUi()
{
	render = vtkSmartPointer<vtkRenderer>::New();
	mVtkWidget = new QVTKWidget(this);
	mVtkWidget->GetRenderWindow()->AddRenderer(render);
	layout = new QGridLayout();
	subwidget = new QWidget(mVtkWidget);
	subwidget->setLayout(layout);
	QPalette pal = subwidget->palette();
	pal.setColor(QPalette::Background,QColor(0xff,0xff,0xff,0xff));
	subwidget->setPalette(pal);
	subwidget->setAutoFillBackground(true);
}
void Widget3D::slotStateChanged(int state)
{
	for (auto iter = checks.begin(); iter != checks.end(); iter++)
	{
		if (sender() == iter->second)
		{
			auto itactor=actorS.find(iter->first);
			if (itactor != actorS.end())
			{
				switch (state)
				{
				case 0:
				{
					itactor->second->GetProperty()->SetOpacity(0.0);
				}
				break;
				case 2:
				{
					itactor->second->GetProperty()->SetOpacity(1.0);
				}
				break;
				}
				render->Render();
			}
		}
	}
}
#include"moc_Widget3D.cpp"