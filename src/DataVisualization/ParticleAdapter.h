#pragma once
#include "PlotAdapterNeedStruct.h"

namespace DV {
	class PartcleAdapter :public PlotAdapterNeedStruct {
		Q_OBJECT
	public:
		PartcleAdapter();
		~PartcleAdapter();

	public:
		virtual std::list<QAction*> getActions() override;
		void initAction();
	public Q_SLOTS:
		void actionTrigger(bool);

	private:
		int getParticelTyepSize();
		void updateAcitonState();
	private:
		std::vector<QAction*> actions;
	};
}