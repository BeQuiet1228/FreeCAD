#include "TimePlotAdapter.h"
#include "C_encoding.h"
#include "PlotAdapter.h"
#include "Renderer.h"
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include "Plot.h"
#include "TimeRenderer.h"
#include <qdir.h>
#include <qcoreapplication.h>
#include "HDF5Reader/hdf5io.h"

namespace DV {
	TimePlotAdapter::TimePlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender)
	{
		addRenderer(listRender);
		initAction();
		this->listRender = listRender;
		undoSignal = "";
	}

	TimePlotAdapter::~TimePlotAdapter()
	{
		delete this->Fourier;
		//delete this->saveData;
	}

	void TimePlotAdapter::initAction() {
		Fourier = new QAction(this);
		//saveData = new QAction(this);
		Fourier->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
		Fourier->setText(QString::fromUtf8("Fourier"));
		//saveData->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
		//saveData->setText(QString::fromUtf8("Save Data"));
		connect(Fourier, SIGNAL(triggered()), SLOT(FourierTrigger()));
		//connect(saveData, SIGNAL(triggered()), SLOT(saveDataFunc()));
	}

	std::list<QAction*> TimePlotAdapter::getActions()
	{
		std::list<QAction*> actions;
		actions.push_back(Fourier);
		actions.push_back(saveData);
		return actions;
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
		
		auto xd = std::dynamic_pointer_cast<XYData>(Timedata);
		if (xd != nullptr && xd->getXTag() == "Frequency(Hz)" && Timedata->recoverInitData(xr.min, xr.max)) {
			setMainRenderer(this->listRender.back());
			xd->setXTag("Time(ns)");//更新坐标Tag
			xd->setYTag("Watts");
			plot->updateInformationLabel();
			undoSignal = "Fourier";
		}
		
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

		auto xd = std::dynamic_pointer_cast<XYData>(Timedata);
		if (this->undoSignal == "Fourier" && Timedata->recoverNowData(xr.min, xr.max)) {
			setMainRenderer(this->listRender.back());
			xd->setXTag("Frequency(Hz)");//更新坐标Tag
			xd->setYTag("Watts\\GHz");
			plot->updateInformationLabel();
			undoSignal = "";
		}
		
		setRenderRange(xr.min, xr.max, yr.min, yr.max);
		return true;
	}

	//为action添加点击函数
	void TimePlotAdapter::FourierTrigger() {
		std::shared_ptr<Renderer> TimePtr = this->listRender.back();
		std::shared_ptr<TimeData> d = std::dynamic_pointer_cast<TimeRenderer>(TimePtr)->getTimedata();
		this->Timedata = d;
		auto xd = std::dynamic_pointer_cast<XYData>(d);
		if (xd->getXTag() == "Frequency(Hz)") {
			errorDialog = new FourierDialog();
			errorDialog->exec();
			delete errorDialog;
			return;
		}

		Data::Rang xr = getAxisBottomRange();
		d->dataToFFT(xr);//对数据进行处理
		
		//重新渲染
		setMainRenderer(TimePtr);
		//Hdf5IO::getCurPath();
		xd->setXTag("Frequency(Hz)");//更新坐标Tag
		xd->setYTag("Watts\\GHz");
		plot->updateInformationLabel();
		dataInStack();//将操作入栈
		
		emit updatePlot();
	}

	//将操作压入栈
	void TimePlotAdapter::dataInStack() {
		Data::Rang xr = getAxisBottomRange();
		Data::Rang yr = getAxisLeftRange();
		UndoRedoStack::DataPtr unData(new UndoRedoData(xr, yr));
		URStack->push(unData);
	}

	//void TimePlotAdapter::saveDataFunc() {
	//	//std::string path = "C:/Users/Administrator/Desktop/TestMode/test_data/chipic//GYRO-C.h5";
	//	////MainRendererDataSaveAs(path); 
	//	//auto data = TimePtr->getData();
	//	//data->saveAs(path);
	//	plot->SaveAs("./FFT.png");
	//	
	//	QDir temDir("./FFT.png");
	//	QString filePath = temDir.absolutePath();
	//	std::string tmp = filePath.toStdString();
	//	QString applicationDirPath;
	//	applicationDirPath = QCoreApplication::applicationDirPath();
	//	std::string tmp1 = applicationDirPath.toStdString();
	//	applicationDirPath = QCoreApplication::applicationFilePath();
	//	std::string tmp2 = applicationDirPath.toStdString();
	//	
	//}
};

#include "moc_TimePlotAdapter.cpp"