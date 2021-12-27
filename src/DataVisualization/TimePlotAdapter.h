#pragma once
#include "PlotAdapter.h"
#include <QAction>
#include <QSize>
#include "FourierDialog.h"
#include "TimeData.h"

namespace DV {
	class TimePlotAdapter :public PlotAdapter {
		Q_OBJECT
	public:
		TimePlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender);
		~TimePlotAdapter();

	public Q_SLOTS:
		void FourierTrigger();
		void saveDataFunc();

	public:
		std::list<QAction*> getActions() override;
		bool undo() override;
		bool redo() override;
		void dataInStack();//将操作压入栈

	private:
		QAction* Fourier;
		QAction* saveData;
		QDialog* errorDialog;
		std::list<std::shared_ptr<Renderer>> listRender;
		std::shared_ptr<TimeData> Timedata;

	private:
		void initAction();

	private:
		std::string undoSignal;//记录功能键的undo操作信号
	};
};
