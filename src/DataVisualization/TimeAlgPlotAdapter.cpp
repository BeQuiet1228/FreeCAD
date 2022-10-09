#include "TimeAlgPlotAdapter.h"
#include "C_encoding.h"
#include "PlotAdapter.h"
#include "Renderer.h"
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include "Plot.h"
#include "TimeRenderer.h"
#include <qcoreapplication.h>
#include <qmessagebox.h>

namespace DV {
	TimeUndoRedoData::TimeUndoRedoData(const Data::Rang& xr, const Data::Rang& yr) :UndoRedoData(xr, yr), point(NULL) {

	}

	TimeUndoRedoData::TimeUndoRedoData(int FunOfAlogrithm, Data::ValuesPtr point, std::string Xtag, std::string Ytag, const Data::Rang& xr, const Data::Rang& yr)
		: FunOfAlogrithm(FunOfAlogrithm), point(point), Xtag(Xtag), Ytag(Ytag), UndoRedoData(xr, yr) {

	}


	TimeAlgPlotAdapter::TimeAlgPlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender):TimePlotAdapter(listRender)
	{
		addRenderer(listRender);
		initAction();
		initTimeData();
	}

	TimeAlgPlotAdapter::~TimeAlgPlotAdapter()
	{
		delete this->Fourier;
		delete this->saveButton;
		delete this->gatherData;
	}

	void TimeAlgPlotAdapter::initAction() {
		Fourier = new QAction(this);
		Fourier->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
		Fourier->setText(QString::fromUtf8("Fourier"));
		connect(Fourier, SIGNAL(triggered()), SLOT(FourierTrigger()));

		saveButton = new QAction(this);
		saveButton->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
		saveButton->setText(QString::fromUtf8("Save"));
		connect(saveButton, SIGNAL(triggered()), SLOT(saveTrigger()));

		gatherData = new QAction(this);
		gatherData->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
		gatherData->setText(QString::fromUtf8("gatherData"));
		connect(gatherData, SIGNAL(triggered()), SLOT(gatherDataTrigger()));
	}

	std::list<QAction*> TimeAlgPlotAdapter::getActions()
	{
		std::list<QAction*> actions;
		actions.push_back(Fourier);
		actions.push_back(saveButton);
		actions.push_back(gatherData);
		return actions;
	}

	/*
	初始化和TimeData的关系
	*/
	void TimeAlgPlotAdapter::initTimeData() {
		std::shared_ptr<TimeRenderer> d = std::dynamic_pointer_cast<TimeRenderer>(mainRenderer);
		this->Timedata = std::dynamic_pointer_cast<TimeAlgData>(d->getData());
	}

	/*
	重写undo和redo函数
	实现在数据更改后的恢复
	*/
	bool TimeAlgPlotAdapter::undo()
	{
		UndoRedoStack::DataPtr rd;
		if (!this->URStack->undo(rd))
			return false;
		auto xr = rd->xr;
		auto yr = rd->yr;

		//通过对TimeUndoRedoData初始化构造的参数，可以适配以后的其他变换的undo和redo
		std::shared_ptr<TimeUndoRedoData> Timerd = std::dynamic_pointer_cast<TimeUndoRedoData>(rd);
		Timedata->updatePoint(Timerd->point);
		Timedata->updateData(InitData, Timerd->Xtag, Timerd->Ytag);
		autoMaxRenderRange();//重新渲染

		emit updatePlot();

		setRenderRange(xr.min, xr.max, yr.min, yr.max);
		return true;
	}

	bool TimeAlgPlotAdapter::redo()
	{
		UndoRedoStack::DataPtr rd;
		if (!this->URStack->redo(rd))
			return false;
		auto xr = rd->xr;
		auto yr = rd->yr;

		std::shared_ptr<TimeUndoRedoData> Timerd = std::dynamic_pointer_cast<TimeUndoRedoData>(rd);
		Timedata->updatePoint(Timerd->point);
		Timedata->updateData(Timerd->FunOfAlogrithm, Timerd->Xtag, Timerd->Ytag);
		autoMaxRenderRange();//重新渲染

		emit updatePlot();

		setRenderRange(xr.min, xr.max, yr.min, yr.max);
		return true;
	}

	//为action添加点击函数
	void TimeAlgPlotAdapter::FourierTrigger() {
		if (Timedata->FunOfAlogrithm != InitData) {
			return;
		}

		Data::Rang xrang = getAxisBottomRange();
		Timedata->dataToFFT(xrang);//对数据进行处理

		autoMaxRenderRange();//重新渲染
		dataIntoStack();//将操作入栈

		emit updatePlot();
	}

	//将当前的point数据添加到h5文件中
	void TimeAlgPlotAdapter::saveTrigger() {
		bool isSave = Timedata->addNewGroup();
		if (isSave) {
			QMessageBox message(QMessageBox::Information, "OK", "save successfully, Visible after reopen");
			message.exec();
		}
		else {
			QMessageBox message(QMessageBox::Warning, "Error", "Failed to save, data already exists");
			message.exec();
		}
	}

	void TimeAlgPlotAdapter::gatherDataTrigger() {
		Data::Rang xrang = getAxisBottomRange();
		Timedata->dataToGather(xrang);//对数据进行处理

		autoMaxRenderRange();//重新渲染
		dataIntoStack();//将操作入栈

		emit updatePlot();
	}

	//将操作压入栈
	void TimeAlgPlotAdapter::dataIntoStack() {
		Data::Rang xr = getAxisBottomRange();
		Data::Rang yr = getAxisLeftRange();
		URStack->push(CreateUndoRedoData(xr, yr));
	}

	//创建UndoRedoData数据,更具需求建立适合的入栈数据
	UndoRedoStack::DataPtr TimeAlgPlotAdapter::CreateUndoRedoData(const Data::Rang& xr, const Data::Rang& yr) {
		Data::ValuesPtr point = Timedata->getPointsPtr();
		int alogrithm = Timedata->FunOfAlogrithm;

		UndoRedoStack::DataPtr unData(new TimeUndoRedoData(alogrithm, point, Timedata->getXTag(), Timedata->getYTag(), xr, yr));

		return unData;
	}
};

#include "moc_TimeAlgPlotAdapter.cpp"