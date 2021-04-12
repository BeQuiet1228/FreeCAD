#include "ContourDataPolar.h"
CountourDataPolar::CountourDataPolar(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:ContourData(h5Data,mod)
{

}

CountourDataPolar::~CountourDataPolar()
{

}

QwtMatrixRasterData* CountourDataPolar::getQwtMatrixRasterData()
{
	QVector<double> data;
	Rang xr = getXRang();
	Rang yr = getYRang();


	float xBlock = xr.length() / width;
	float yBlock = yr.length() / height;

	auto grid = grids.begin();
	for (int i = 0; i < grids.size() && grid != grids.end();)
	{
#if 0 //是否处理非均匀网格
		int w = i % width;
		int h = i / width;
		if (grid->x > (w*xBlock + xr.min) && grid->y > (h*yBlock + yr.min))
		{
			data.append(grid->value);
			i++;
		}
		else{
			grid++;
		}
#else
		data.append(grid->value);
		grid++;
#endif			
	}
	QwtMatrixRasterData *rasterData = new QwtMatrixRasterData;
	rasterData->setValueMatrix(data, width);

	rasterData->setInterval(Qt::XAxis,
		QwtInterval(xr.min, xr.max, QwtInterval::ExcludeMaximum));
	rasterData->setInterval(Qt::YAxis,
		QwtInterval(0, yr.max, QwtInterval::ExcludeMaximum));

	Rang vr = getVlaueRange();
	rasterData->setInterval(Qt::ZAxis, QwtInterval(vr.min, vr.max));
	rasterData->setResampleMode(QwtMatrixRasterData::BilinearInterpolation);
	return rasterData;
}

