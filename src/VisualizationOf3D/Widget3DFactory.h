#pragma once
#ifndef WIDGET_3D_FACTORY_H_
#define WIDGET_3D_FACTORY_H_
#include "HDF5Reader/hdf5io.h"
#include "exPortConfig.hpp"
class QWidget;
class VISUALZATION3D_EXPORT Widget3DFactory
{
public:
	Widget3DFactory();
	~Widget3DFactory();
public:
	QWidget* creat3DWidget(Hdf5Data& data);
protected:
private:
	QWidget* structWidget;
};
#endif