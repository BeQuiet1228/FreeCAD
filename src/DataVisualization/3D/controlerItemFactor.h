#pragma once
#include "ControlerItem.h"
#include "DataVisualization3DExport.hpp"
namespace DV3D {
	 class  DATA_VISUALIZATION_3D_EXPORT ControlerItemFactor {
	public:
		ControlerItemFactor() = default;
		~ControlerItemFactor() = default;

	public:
		static ControlerItem* CreatControlerItem();
		static ControlerItem* CreatContour3dControlerItem();

	};
}