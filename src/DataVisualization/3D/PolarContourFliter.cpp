#include "PolarContourFliter.h"
#include "vtkMath.h"
#include "../ContourDataPolar.h"
#include "memory"
DV3D::PolarContourFilter::PolarContourFilter()
{

}

DV3D::PolarContourFilter::~PolarContourFilter()
{
	rGridData.clear();
	thetaGridData.clear();
	zGridData.clear();
	vallist.clear();
}

/**
* @brief DV3D::PolarContourFilter::loadPoint 加载点位
* @param Hdf5Data & h5
* @param int resolution
* @return bool
* @time	2021/12/23
*/
bool DV3D::PolarContourFilter::loadPoint(Hdf5Data& h5, int resolution)
{
	if (4 == h5.listDataSet.size())
		return loadPoint3d(h5, resolution);
	if (3 == h5.listDataSet.size())
		return loadPoint2d(h5, resolution);
	return false;
}

std::vector<double>& DV3D::PolarContourFilter::getRGridData()
{
	return rGridData;
}

std::vector<double>& DV3D::PolarContourFilter::getThetaGridData()
{
	return thetaGridData;
}

std::vector<double>& DV3D::PolarContourFilter::getZGridData()
{
	return zGridData;
}

std::vector<double>& DV3D::PolarContourFilter::getVallist()
{
	return vallist;
}

bool DV3D::PolarContourFilter::loadPoint3d(Hdf5Data& h5, int resolution)
{
	std::vector<std::vector<float>> grid;
	grid.reserve(4);
	for (auto i = 0; i < h5.listDataSet.size(); ++i)
	{
		std::vector<float> d;
		Hdf5IO::getValue(h5.listDataSet.at(i), d);
		grid.push_back(d);
	}
	//x-y-z
	std::vector<float>& vaList = grid[0];
	std::vector<float>& rList = grid[1];
	std::vector<float>& thetaList = grid[2];
	std::vector<float>& zList = grid[3];

	auto rGridSize = rList.size();
	auto thetaSize = thetaList.size();
	auto zSize = zList.size();

	double angInterval = vtkMath::RadiansFromDegrees(360.0) / resolution;
	std::vector<double> angs;
	for (auto i = 0; i < resolution; ++i)
		angs.push_back(angInterval * i);
	
	std::map<double, std::map<double, std::map<double, double>>> maplist;
	for (int zi = 0; zi < zSize; ++zi)
	{
		for (int thetai = 0; thetai < thetaSize; ++thetai)
		{
			for (int ri = 0; ri < rGridSize; ++ri)
			{
				double rVal = rList[ri];
				double thetVal = thetaList[thetai];
				double scalVal = vaList[ri + thetai * rGridSize + zi * thetaSize * rGridSize];
				maplist[zList[zi]][thetVal][rVal] = scalVal;
				if (thetai == thetaSize - 1)
					continue;
				double thetValNext = thetaList[(thetai + 1)];
				double scalValNext = vaList[ri + (thetai + 1) * rGridSize + zi * rGridSize * thetaSize];
				auto iter = angs.begin();
				while (iter != angs.end() && thetValNext > *iter)
				{
					if (*iter <= thetVal)
					{
						iter++;
						continue;
					}
					double curScalar = (scalValNext - scalVal) * ((*iter) - thetVal) / (thetValNext - thetVal) + scalVal;
					maplist[zList[zi]][*iter][rVal] = curScalar;
					iter++;
				}
			}
		}
			
	}
	for (auto iterZ = maplist.begin(); iterZ != maplist.end(); iterZ++)
	{
		zGridData.push_back(iterZ->first);
		for (auto iterTheta = iterZ->second.begin(); iterTheta != iterZ->second.end(); iterTheta++)
		{
			thetaGridData.push_back(iterTheta->first);
			for (auto iterR = iterTheta->second.begin(); iterR != iterTheta->second.end(); iterR++)
			{
				rGridData.push_back(iterR->first);
				vallist.push_back(iterR->second);
			}
		}
	}
	eraseRedundant(zGridData);
	eraseRedundant(rGridData);
	eraseRedundant(thetaGridData);
	return true;
}

bool DV3D::PolarContourFilter::loadPoint2d(Hdf5Data& h5, int resolution)
{
	std::shared_ptr<DV::ContourDataPolar> data =
		std::shared_ptr<DV::ContourDataPolar>(DV::CreateContourDataPolar(h5));
	data->loadPoint();
	auto datas = data->getGrids();
	auto face = data->getStructFace();
	double polarZ;
	(h5.coordinateSystem == Hdf5Data::CoordinateSystem::CYLINDER) ?
		polarZ = face[0] :
		polarZ = face[2];
	//开始进行插值
	auto rGridSize = data->getWidth();
	auto thetaGridSize = data->getHeight();
	double angInterval = vtkMath::RadiansFromDegrees(360.0) / resolution;
	std::vector<double> angs;

	for (auto i = 0; i < resolution; ++i)
		angs.push_back(angInterval * i);
	//theta-r-val
	std::map<double, std::map<double, double>> maplist;
	for (int thetai = 0; thetai < thetaGridSize; ++thetai)
	{
		for (int ri = 0; ri < rGridSize; ++ri)
		{
			double rVal = datas[ri + thetai * rGridSize].x;
			double thetVal = datas[ri + thetai * rGridSize].y;
			double scalVal = datas[ri + thetai * rGridSize].value;
			maplist[thetVal][rVal] = scalVal;
			if (thetai == thetaGridSize - 1)
				continue;
			double thetValNext = datas[ri + (thetai + 1) * rGridSize].y;
			double scalValNext = datas[ri + (thetai + 1) * rGridSize].value;
			auto iter = angs.begin();
			while (iter != angs.end() && thetValNext > *iter)
			{
				if (*iter <= thetVal)
				{
					iter++;
					continue;
				}
				double curScalar = (scalValNext - scalVal) * ((*iter) - thetVal) / (thetValNext - thetVal) + scalVal;
				maplist[*iter][rVal] = curScalar;
				iter++;
			}
		}
	}
	//获取完毕
	for (auto iterTheta = maplist.begin(); iterTheta != maplist.end(); iterTheta++)
	{
		thetaGridData.push_back(iterTheta->first);
		for (auto iterR = iterTheta->second.begin(); iterR != iterTheta->second.end(); iterR++)
		{
			rGridData.push_back(iterR->first);
			vallist.push_back(iterR->second);
		}
	}
	eraseRedundant(rGridData);
	eraseRedundant(thetaGridData);
	zGridData.push_back(polarZ);
	return true;
}

/**
* @brief DV3D::PolarContourFilter::eraseRedundant 删除冗余数据
* @param std::vector<double> &
* @return void
* @time	2021/12/23
*/
void DV3D::PolarContourFilter::eraseRedundant(std::vector<double>& data)
{
	std::sort(data.begin(), data.end());
	data.erase(std::unique(data.begin(), data.end()), data.end());
}

