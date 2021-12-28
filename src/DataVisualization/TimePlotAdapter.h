#pragma once
#include "PlotAdapter.h"
#include <QAction>
#include <QSize>
#include "FourierDialog.h"
#include "TimeData.h"

namespace DV {
	class TimeUndoRedoData :public UndoRedoData{
	public:
		TimeUndoRedoData(const Data::Rang& xr, const Data::Rang& yr);
		/*
		根据需求导入参数
		point记录每个节点的数据
		*/
		TimeUndoRedoData(int FunOfAlogrithm, std::vector<float> point, std::string Xtag, std::string Ytag, const Data::Rang& xr, const Data::Rang& yr);
		TimeUndoRedoData() = default;

		Data::Rang xr, yr;
		std::string Xtag, Ytag;
		std::vector<float> point;
		int FunOfAlogrithm;
	};

	class TimePlotAdapter :public PlotAdapter {
		Q_OBJECT
	public:
		TimePlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender);
		~TimePlotAdapter();

	public Q_SLOTS:
		void FourierTrigger();

	public:
		std::list<QAction*> getActions() override;
		UndoRedoStack::DataPtr CreateUndoRedoData(const Data::Rang& xr, const Data::Rang& yr) override;
		bool undo() override;
		bool redo() override;
		void dataIntoStack();//将操作压入栈

	private:
		QAction* Fourier;
		QDialog* errorDialog;
		std::shared_ptr<TimeData> Timedata;//初始和TimeData的关系，通过initTimeData在构造函数中被初始化

	private:
		void initAction();
		void initTimeData();
	};
};
