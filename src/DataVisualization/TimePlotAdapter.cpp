#include "TimePlotAdapter.h"
#include "C_encoding.h"
#include "PlotAdapter.h"
#include "Renderer.h"
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include "Plot.h"
#include "TimeRenderer.h"

namespace DV {
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
		if (xd->getXTag() == "Frequency(Hz)") {
			errorDialog = new FourierDialog();
			errorDialog->exec();
			delete errorDialog;
			return;
		}

		Data::Rang xr = getAxisBottomRange();
		dataInStack();
		d->dataToFFT(xr);//对数据进行处理
		
		//重新渲染
		setMainRenderer(TimePtr);

		xd->setXTag("Frequency(Hz)");//更新坐标Tag
		//xd->setYTag("Watts\\GHz");
		plot->updateInformationLabel();

		//setRenderXRange(LBorder, RBorder);//设置显示范围
		emit updatePlot();
		//d->recoverData();

		////FFT转换后的图形的保存
		//std::string path = "C:/Users/Administrator/Desktop//TestMode//MILO_C(1).h5";
		////MainRendererDataSaveAs(path);
		//auto data = TimePtr->getData();
		//data->saveAs(path);
	}

	//将操作压入栈
	void TimePlotAdapter::dataInStack() {
		//auto URStack = adapter->getUndoRedoStack();
		Data::Rang xr = getAxisBottomRange();
		Data::Rang yr = getAxisLeftRange();
		UndoRedoStack::DataPtr unData(new UndoRedoData(xr, yr));
		URStack->push(unData);
	}
};

#include "moc_TimePlotAdapter.cpp"