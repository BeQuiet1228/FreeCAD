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
#include "QStandardItem"
#include"qdebug.h"
#include "TreeItem3D.h"
QString Treeicon[] = {":/TreeIcon/model.svg"};
/**
* @brief Widget3D::Widget3D
* @param QWidget * parent
* @return 
*/

Widget3D::Widget3D(QWidget* parent) :BaseWidget(parent) {
	initUi();
}
/**
* @brief Widget3D::~Widget3D
* @return 
*/

Widget3D::~Widget3D(){
	mflp(dataMPtr, false);
	if (items.size() <= 0)
		return;
	auto iter=items.begin();
	auto parentItem=(*iter)->parent();
	if (nullptr != parentItem && parentItem->hasChildren()>0)
	{
		parentItem->removeRows(0, parentItem->rowCount());
	}
	items.clear();
}
/**
* @brief Widget3D::transfromPolyData
* @param __int64 porPer
* @param vtkPolyData * polyData
* @return void
*/

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
	render->AddActor(actor);
	//´´½¨
	TreeItem3D* treeItem = new TreeItem3D(QIcon(Treeicon[0]),QString("%1").arg(porPer));
	treeItem->setParent(this);
	treeItem->setCheckable(true);
	treeItem->setCheckState(Qt::Checked);
	items.push_back(treeItem);
	actorS[treeItem] = actor;
}
/**
* @brief Widget3D::resizeEvent
* @param QResizeEvent *
* @return void
*/

void Widget3D::resizeEvent(QResizeEvent*)
{
	mVtkWidget->resize(this->size());
	QSize subsize = QSize(this->size().width()/15,this->size().height());
}
void Widget3D::Updata()
{
}
void Widget3D::drawImage()
{
	render->SetBackground(0.529, 0.8078, 0.92157);
	render->SetBackground2(1.0, 1.0, 1.0);
	render->SetGradientBackground(1);
}

void Widget3D::initUi()
{
	render = vtkSmartPointer<vtkRenderer>::New();
	mVtkWidget = new QVTKWidget(this);
	mVtkWidget->GetRenderWindow()->AddRenderer(render);
	mVtkWidget->setAutomaticImageCacheEnabled(true);
}
void Widget3D::setFunction(void* lp, fLp flp)
{
	mflp = flp;
	dataMPtr = lp;
}
void Widget3D::slotitemStateChange(QStandardItem* mItem)
{
	BaseWidget::slotitemStateChange(mItem);
	auto iter = actorS.find(mItem);
	if (iter != actorS.end())
	{
		if (iter->first->checkState() == Qt::Checked)
		{
			iter->second->GetProperty()->SetOpacity(1.0);
		}
		else
		{
			iter->second->GetProperty()->SetOpacity(0.0);
		}
		render->Render();
		mVtkWidget->GetInteractor()->Render();
	}
}
void Widget3D::clearItem(TreeItem* lp)
{
	if (nullptr == lp)
		return;
	for (auto iter = items.begin(); iter != items.end(); iter++)
	{
		if (lp == *iter)
		{
			items.erase(iter);
			break;
		}
	}
}
#include"moc_Widget3D.cpp"