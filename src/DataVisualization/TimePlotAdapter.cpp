#include "TimePlotAdapter.h"
#include "C_encoding.h"
#include "PlotAdapter.h"
#include "Renderer.h"
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include "Plot.h"
#include "TimeRenderer.h"
#include <qcoreapplication.h>

namespace DV {
	TimeUndoRedoData::TimeUndoRedoData(const Data::Rang& xr, const Data::Rang& yr) :UndoRedoData(xr, yr), point(NULL) {

	}

	TimeUndoRedoData::TimeUndoRedoData(int FunOfAlogrithm, std::vector<float> point, std::string Xtag, std::string Ytag, const Data::Rang& xr, const Data::Rang& yr)
		: FunOfAlogrithm(FunOfAlogrithm), point(point), Xtag(Xtag), Ytag(Ytag), UndoRedoData(xr, yr) {
		
	}


	TimePlotAdapter::TimePlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender)
	{
		addRenderer(listRender);
		initAction();
		initTimeData();
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

	/*
	初始化和TimeData的关系
	*/
	void TimePlotAdapter::initTimeData() {
		std::shared_ptr<TimeRenderer> d = std::dynamic_pointer_cast<TimeRenderer>(mainRenderer);
		this->Timedata = std::dynamic_pointer_cast<TimeData>(d->getData());
	}

	/*
	重写undo和redo函数
	实现在数据更改后的恢复
	*/
	bool TimePlotAdapter::undo()
	{
		/*
		根据不同的坐标标签采用不同的恢复
		以后的功能可以仿照
		*/
		UndoRedoStack::DataPtr rd;
		if (!this->URStack->undo(rd))
			return false;
		auto xr = rd->xr;
		auto yr = rd->yr;
		
		std::shared_ptr<TimeUndoRedoData> Timerd = std::dynamic_pointer_cast<TimeUndoRedoData>(rd);

		*(Timedata->getPointsPtr()) = Timerd->point;
		setMainRenderer(mainRenderer);

		//更新坐标Tag
		Timedata->setXTag(Timerd->Xtag);
		Timedata->setYTag(Timerd->Ytag);
		Timedata->FunOfAlogrithm = InitData;//还原变换
		emit updatePlot();

		setRenderRange(xr.min, xr.max, yr.min, yr.max);
		return true;
	}

	bool TimePlotAdapter::redo()
	{
		UndoRedoStack::DataPtr rd;
		if (!this->URStack->redo(rd))
			return false;
		auto xr = rd->xr;
		auto yr = rd->yr;

		std::shared_ptr<TimeUndoRedoData> Timerd = std::dynamic_pointer_cast<TimeUndoRedoData>(rd);

		*(Timedata->getPointsPtr()) = Timerd->point;
		setMainRenderer(mainRenderer);

		//更新坐标Tag
		Timedata->setXTag(Timerd->Xtag);
		Timedata->setYTag(Timerd->Ytag);
		Timedata->FunOfAlogrithm = Timerd->FunOfAlogrithm;//还原变换
		emit updatePlot();

		setRenderRange(xr.min, xr.max, yr.min, yr.max);
		return true;
	}

	//为action添加点击函数
	void TimePlotAdapter::FourierTrigger() {
		if (Timedata->FunOfAlogrithm == DataForFFT) {
			errorDialog = new FourierDialog();
			errorDialog->exec();
			delete errorDialog;
			return;
		}

		Data::Rang xr = getAxisBottomRange();
		Timedata->dataToFFT(xr);//对数据进行处理

		//重新渲染
		setMainRenderer(mainRenderer);
		Timedata->FunOfAlogrithm = DataForFFT;//更新FFT标识符
		Timedata->setXTag("Frequency(Hz)");//更新坐标Tag
		Timedata->setYTag("Watts\\GHz");

		dataIntoStack();//将操作入栈

		emit updatePlot();
	}

	//将操作压入栈
	void TimePlotAdapter::dataIntoStack() {
		Data::Rang xr = getAxisBottomRange();
		Data::Rang yr = getAxisLeftRange();
		URStack->push(CreateUndoRedoData(xr, yr));
	}

	//创建UndoRedoData数据
	UndoRedoStack::DataPtr TimePlotAdapter::CreateUndoRedoData(const Data::Rang& xr, const Data::Rang& yr) {
		std::vector<float> point = *(Timedata->getPointsPtr());
		int FunOfAlogrithm = Timedata->FunOfAlogrithm;

		UndoRedoStack::DataPtr unData(new TimeUndoRedoData(FunOfAlogrithm, point, Timedata->getXTag(), Timedata->getYTag(), xr, yr));
		return unData;
	}
};

#include "moc_TimePlotAdapter.cpp"