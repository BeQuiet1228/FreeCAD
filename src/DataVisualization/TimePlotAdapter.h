#pragma once
#include "PlotAdapter.h"
#include <QAction>
#include <QSize>
#include "FourierDialog.h"

namespace DV {
	class TimePlotAdapter :public PlotAdapter {
		Q_OBJECT
	public:
		TimePlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender);
		~TimePlotAdapter();

	public Q_SLOTS:
		void FourierTrigger();

	public:
		std::list<QAction*> getActions() override;
		void dataInStack();//½«²Ù×÷Ñ¹ÈëÕ»

	private:
		QAction* Fourier;
		QDialog* errorDialog;
		std::list<std::shared_ptr<Renderer>> listRender;

	private:
		void initAction();
	};
};
