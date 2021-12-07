#include "ContourDataPolar.h"
#include "qwt/qwt_math.h"
#include "DataInformationGetter.h"
namespace DV {
	ContourDataPolar::ContourDataPolar(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
		:ContourData(h5Data, mod)
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
			//是否处理非均匀网格  
			//2021 -7-16
			//从算法层面解决了非均匀网格的问题，这里的代码已舍弃
#if 0 
			int w = i % width;
			int h = i / width;
			if (grid->x > (w * xBlock + xr.min) && grid->y > (h * yBlock + yr.min))
			{
				data.append(grid->value);
				i++;
			}
			else {
				grid++;
			}
#else
			data.append(grid->value);
			grid++;
#endif			
		}

		PolarMatrixRasterData* rasterData = new PolarMatrixRasterData;
		rasterData->setXScale(xScale);
		rasterData->setYScale(yScale);
		rasterData->setValueMatrix(data, width);

		rasterData->setInterval(Qt::XAxis,
			QwtInterval(xr.min, xr.max, QwtInterval::ExcludeMaximum));
		rasterData->setInterval(Qt::YAxis,
			QwtInterval(yr.min, yr.max, QwtInterval::ExcludeMaximum));

		Rang vr = getVlaueRange();
		rasterData->setInterval(Qt::ZAxis, QwtInterval(vr.min, vr.max));
		rasterData->setResampleMode(QwtMatrixRasterData::BilinearInterpolation);
		return rasterData;
	}


	bool ContourDataPolar::loadPoint()
	{
		bool ok = ContourData::loadPoint();
		return ok;
	}

	//! Approximation of arc tangent ( error below 0,005 radians )
	double PolarMatrixRasterData::FastAtan(double x)
	{
		if (x < -1.0)
			return -M_PI_2 - x / (x * x + 0.28);

		if (x > 1.0)
			return M_PI_2 - x / (x * x + 0.28);

		return x / (1.0 + x * x * 0.28);
	}

	//! Approximation of arc tangent ( error below 0,005 radians )
	double PolarMatrixRasterData::FastAtan2(double y, double x)
	{
		if (x > 0)
			return FastAtan(y / x);

		if (x < 0)
		{
			const double d = FastAtan(y / x);
			return (y >= 0) ? d + M_PI : d - M_PI;
		}

		if (y < 0.0)
			return -M_PI_2;

		if (y > 0.0)
			return M_PI_2;

		return 0.0;
	}

	double PolarMatrixRasterData::value(double x, double y) const
	{
		double r, theta;
		theta = qAtan2(x, y);
		r = sqrt(pow(x, 2) + pow(y, 2));

		theta = FastAtan2(y, x);
		if (theta < 0 && theta < interval(Qt::YAxis).minValue())
			theta += 2 * M_PI;

		return DefineMatrixRasterData::value(r, theta);
	}

	ContourDataPloarHalfGridFullCircle::ContourDataPloarHalfGridFullCircle(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
		:ContourDataPolar(h5Data, mod)
	{

	}

	QwtMatrixRasterData* ContourDataPloarHalfGridFullCircle::getQwtMatrixRasterData()
	{
		QVector<double> data;
		Rang xr = getXRang();
		Rang yr = getYRang();


		float xBlock = xr.length() / width;
		float yBlock = yr.length() / height;

		int w = 0; int h = (yScale.size() - 1) * xScale.size();
		for (; w < grids.size() && h < grids.size(); w++, h++)
		{
			data.append((grids.at(w).value - grids.at(h).value) / 2 + grids.at(h).value);
		}

		auto grid = grids.begin();
		for (int i = 0; i < grids.size() && grid != grids.end();)
		{
			//是否处理非均匀网格  
			//2021 -7-16
			//从算法层面解决了非均匀网格的问题，这里的代码已舍弃
#if 0 
			int w = i % width;
			int h = i / width;
			if (grid->x > (w * xBlock + xr.min) && grid->y > (h * yBlock + yr.min))
			{
				data.append(grid->value);
				i++;
			}
			else {
				grid++;
			}
#else
			data.append(grid->value);
			grid++;
#endif			
		}
		w = 0; h = (yScale.size() - 1) * xScale.size();
		for (; w < grids.size() && h < grids.size(); w++, h++)
		{
			data.append((grids.at(w).value - grids.at(h).value) / 2 + grids.at(h).value);
		}
		std::vector<float> nys;
		nys.push_back(0.0);
		for (auto iter = yScale.begin(); iter != yScale.end(); iter++)
		{
			nys.push_back(*iter);
		}
		nys.push_back(M_PI * 2);
		PolarMatrixRasterData* rasterData = new PolarMatrixRasterData;
		rasterData->setXScale(xScale);
		rasterData->setYScale(nys);
		rasterData->setValueMatrix(data, width);

		rasterData->setInterval(Qt::XAxis,
			QwtInterval(xr.min, xr.max, QwtInterval::ExcludeMaximum));
		rasterData->setInterval(Qt::YAxis,
			QwtInterval(yr.min, yr.max, QwtInterval::ExcludeMaximum));

		Rang vr = getVlaueRange();
		rasterData->setInterval(Qt::ZAxis, QwtInterval(vr.min, vr.max));
		rasterData->setResampleMode(QwtMatrixRasterData::BilinearInterpolation);
		return rasterData;
	}

	ContourDataPolar* CreateContourDataPolar(Hdf5Data& h5)
	{
		if (h5.headList.size() < 3)
			return nullptr;
		//获取观测对象
		auto temp = DataInformationGetter::getObserveObejct(h5.headList.at(2));
		temp = QString::fromStdString(temp).toLower().toStdString();

		//在半网格上的观测对象
		std::vector<std::string> listOb;
		listOb.push_back("ephi");
		listOb.push_back("bz");
		listOb.push_back("brho");

		bool ok = false;
		for (auto iter = listOb.begin(); iter != listOb.end(); iter++)
		{
			if (temp == *iter)
				ok = true;
		}

		auto polarData = new ContourDataPolar(h5);
		if (!ok)
			return polarData;

		std::vector<float> face = polarData->getStructFace();
		if (face.size() < 6)
			return polarData;

		//获取theta的起始位置
		float start = 0, end = 0;
		if (h5.coordinateSystem == Hdf5Data::CYLINDER)
		{
			start = face[2];
			end = face[5];
		}
		else {
			start = face[1];
			end = face[4];
		}

		if (abs(start) < 0.001 && abs(end - 2 * M_PI) < 0.001)
		{
			delete polarData;
			return new ContourDataPloarHalfGridFullCircle(h5);
		}
		else {
			return polarData;
		}
	}

};
