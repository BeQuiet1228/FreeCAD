#include "TimePlotAdapter.h"
#include "C_encoding.h"
#include "PlotAdapter.h"
#include "Renderer.h"
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include "Plot.h"
#include "TimeRenderer.h"

TimePlotAdapter::TimePlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender)
{
	addRenderer(listRender);
	initAction();
	this->listRender = listRender;
}

TimePlotAdapter::~TimePlotAdapter()
{
	delete this->Fourier;
}

void TimePlotAdapter::initAction() {
	Fourier = new QAction(this);
	Fourier->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
	Fourier->setText(QString::fromUtf8("Fourier"));
	connect(Fourier, SIGNAL(triggered()), SLOT(FourierTrigger()));
}

std::list<QAction*> TimePlotAdapter::getActions()
{
	std::list<QAction*> actions;
	actions.push_back(Fourier);

	return actions;
}

//为action添加点击函数
void TimePlotAdapter::FourierTrigger() {
	std::shared_ptr<Renderer> TimePtr = this->listRender.back();
	std::shared_ptr<TimeData> d = std::dynamic_pointer_cast<TimeRenderer>(TimePtr)->getTimedata();
	auto xd = std::dynamic_pointer_cast<XYData>(d);
	if (xd->getXTag() == "Frequence(Hz)") {
		errorDialog = new FourierDialog();
		errorDialog->exec();
		delete errorDialog;
		return;
	}

	Data::Rang xr = getAxisBottomRange();
	d->dataToFFT(xr);//对数据进行处理

	//更新渲染
	 setMainRenderer(TimePtr);
	/*float LBorder = *(d->getXYRange().begin());
	float RBorder = d->getXYRange().back();*/

	//转变后的数据范围超出10GHZ后进行范围缩小
	//RBorder = (RBorder - LBorder) > pow(10, 10) ? LBorder + pow(10, 10) : RBorder;
	
	
	xd->setXTag("Frequence(Hz)");//更新坐标Tag
	plot->updateInformationLabel();

	//setRenderXRange(LBorder, RBorder);//设置显示范围
	emit updatePlot();
	
	////FFT转换后的图形的保存
	//std::string path = "C:/Users/Administrator/Desktop//TestMode//MILO_C(1).h5";
	////MainRendererDataSaveAs(path);
	//auto data = TimePtr->getData();
	//data->saveAs(path);
}

#include "moc_TimePlotAdapter.cpp"