#include "ContourDataPolar.h"
#include <qmath.h>
ContourDataPolar::ContourDataPolar(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:ContourData(h5Data,mod)
{

}

ContourDataPolar::~ContourDataPolar()
{

}

QwtMatrixRasterData* ContourDataPolar::getQwtMatrixRasterData()
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
	QwtMatrixRasterData *rasterData = new PolarMatrixRasterData;
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


bool ContourDataPolar::loadPoint()
{
	bool ok = ContourData::loadPoint();

	//角项最大最小值必须是0 - 2PI，否则画出来不圆
	Rang yr = getYRang();
	yr.min = 0;
	yr.max = 2 * M_PI;
	setYRang(yr);
	return ok;
}

double PolarMatrixRasterData::value(double x, double y) const
{
	double r, theta;
	theta = qAtan2(x, y);
	r = sqrt(pow(x, 2) + pow(y, 2));

	if (theta < 0.0)
		theta += 2 * M_PI;


	return QwtMatrixRasterData::value(r, theta);
}
