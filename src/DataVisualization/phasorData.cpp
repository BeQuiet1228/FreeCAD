#include"phasorData.h"
#include "DataInformationGetter.h"
namespace DV {
	phasorData::phasorData(Hdf5Data& heData, const RunMod& mod) :DirData(heData, mod)
	{
		disMode = sizeToColor;
	}
	phasorData::~phasorData() {
	}

	float phasorData::getStructFaceAnchor()
	{
		if (headList.size() < 16)
			return 0;
		

		QString qstr = QString::fromStdString(headList[15]);
		QStringList sl = qstr.split(",");
		if (sl.size() != 2)
			return 0;
		qstr = sl[0];
		auto str = qstr.toStdString();
		sl = qstr.split("(");
		if (sl.size() != 2)
			return 0;
		qstr = sl[0];
		str = qstr.toStdString();
		sl = qstr.split("=");
		if (sl.size() != 3)
			return 0;
		auto value = sl[2];
		str = value.toStdString();

		return value.toFloat();
	}


	void phasorData::restorDeriveData()
	{

	}
	/**
	* @brief phasorData::loadPoint 加载数据
	* @return bool
	*/
	bool phasorData::loadPoint()
	{
		//需要先清空数据
		mPiflist_rect.clear();
		p1.clear();
		p2.clear();
		len_coef.clear();
		/*************************************/
		Data::ListValuesPtr ListValues;
		//获取原始数据
		bool ok = autoModGetSourceData(ListValues);
		if (!ok && !ListValues && ListValues->size() == 0)
			return false;
		auto it = (ListValues->begin());
		auto xtag = getXTag();
		auto ytag = getYTag();
		this->istrue = isTruedir();
		//矢量图R_Z轴方向取值反向，这里做特殊处理，将判断后获得得值做取反。
		if (directionTyp == R_Z || directionTyp == Y_Z || directionTyp == X_Z || directionTyp == X_Y)
		{
			this->istrue = !this->istrue;
		}
		//获取横坐标的个数
		if (this->istrue)
		{
			posySize = (*it)->size(); it++;
			posxSize = (*it)->size();
		}
		else
		{
			posxSize = (*it)->size(); it++;
			posySize = (*it)->size();
		}

		//初始化范围
		initXYRang();
		initData();
		initVectorData();
		return true;
	}
	/**
	* @brief phasorData::initXYRang 初始化X-Y的范围
	* @return bool
	*/
	bool phasorData::initXYRang() {
		if (posxSize < 2 || posySize < 2)
			return false;
		//获取x,y轴的取值范围
		Rang xr, yr;
		Data::ListValuesPtr ListValues;
		bool ok = autoModGetSourceData(ListValues);
		if (!ok && !ListValues && ListValues->size() == 0)
			return false;
		//获取成功
		auto it = ListValues->begin();
		Data::ValuesPtr datasetEmA = *it; it++;
		Data::ValuesPtr datasetEmB = *it;
		if (this->istrue)
		{
			//x
			xr.min = *(datasetEmB->begin());
			xr.max = *(datasetEmB->end() - 1);
			setXRang(xr);
			//y
			yr.min = *(datasetEmA->begin());
			yr.max = *(datasetEmA->end() - 1);
			setYRang(yr);
		}
		else
		{
			auto itx = datasetEmA->begin();
			xr.min = *(datasetEmA->begin());
			itx = datasetEmA->end() - 1;
			xr.max = *itx;
			setXRang(xr);
			//y
			auto ity = datasetEmB->begin();
			yr.min = *ity;
			ity = datasetEmB->end() - 1;
			yr.max = *ity;
			setYRang(yr);
		}
		defXrang = xr;
		defYrang = yr;
		return true;
	}
	/**
	* @brief phasorData::findIndexFromXValueL 查找该横坐标的左边的索引
	*/
	unsigned int phasorData::findIndexFromXValueL(const float& x)
	{
		return 0;
	}
	/**
	* @brief phasorData::initData 初始化相关数据
	* @return bool
	*/
	bool phasorData::initData()
	{
		//先获取H5F中的全部数据
		mPiflist_rect.clear();
		//std::vector<QPointF> pointlist;
		//获取x轴上的全部点
		std::vector<qreal> valuesA_list = getaxis_x();
		//获取y轴上的全部点
		std::vector<qreal> valueB_list = getaxis_y();
		//获取全部的切割空间
#pragma region 
		if (this->istrue)
		{
			for (auto valueA = 0; valueA < valuesA_list.size() - 1; valueA++)
			{
				for (auto valueB = 0; valueB < valueB_list.size() - 1; valueB++)
				{
					//获取切割矩形
					QRectF _rectf;
					_rectf.setLeft(valuesA_list[valueA]);
					_rectf.setRight(valuesA_list[valueA + 1]);
					_rectf.setTop(valueB_list[valueB + 1]);
					_rectf.setBottom(valueB_list[valueB]);
					mPiflist_rect.push_back(_rectf);
				}
			}
		}
		else
		{
			for (auto valueB = 0; valueB < valueB_list.size() - 1; valueB++)
			{
				for (auto valueA = 0; valueA < valuesA_list.size() - 1; valueA++)
				{
					//获取切割矩形
					QRectF _rectf;
					_rectf.setLeft(valuesA_list[valueA]);
					_rectf.setRight(valuesA_list[valueA + 1]);
					_rectf.setTop(valueB_list[valueB + 1]);
					_rectf.setBottom(valueB_list[valueB]);
					mPiflist_rect.push_back(_rectf);
				}
			}
		}

#pragma endregion
		return true;
	}
	/**
	* @brief phasorData::getaxis_x 获取x轴上的刻度
	* @return std::vector<qreal>
	*/
	std::vector<qreal> phasorData::getaxis_x()
	{
		std::vector<qreal> axis_xlist;
		Data::ListValuesPtr ListValues;
		bool ok = autoModGetSourceData(ListValues);
		if (!ok && !ListValues && 0 == ListValues->size())
			return axis_xlist;
		//获取EMA的全部数据
		auto iter = ListValues->begin();
		if (this->istrue)
		{
			iter++;
		}
		Data::ValuesPtr datasetEmA = *iter;
		axis_xlist.push_back(0);
		for (auto iter_A = datasetEmA->begin(); iter_A != datasetEmA->end(); iter_A++)
		{
			axis_xlist.push_back(*iter_A);
		}
		return axis_xlist;
	}
	/**
	* @brief phasorData::getaxis_y 获取y轴上的全部刻度
	* @return std::vector<qreal>
	*/
	std::vector<qreal> phasorData::getaxis_y()
	{
		std::vector<qreal> axis_ylist;
		Data::ListValuesPtr ListValues;
		bool ok = autoModGetSourceData(ListValues);
		if (!ok && !ListValues && ListValues->size() == 0)
			return axis_ylist;
		auto iter = ListValues->begin();
		if (!(this->istrue))
		{
			iter++;
		}
		Data::ValuesPtr datasetEmB = *iter;
		axis_ylist.push_back(0);
		for (auto iterb = datasetEmB->begin(); iterb != datasetEmB->end(); iterb++)
		{
			axis_ylist.push_back(*iterb);
		}
		return axis_ylist;
	}

	bool phasorData::getDataDirection()
	{
		if (this->headList.size() < 11)
			return false;
		QString str = QString::fromStdString(this->headList[11]);
		auto sl = str.split("(");
		if (sl.size() < 2)
			return false;
		str = sl[1];
		sl = str.split(",");
		if (sl.size() < 2)
			return false;
		str = sl[0];
		str = str.right(str.size() - 1);

		std::string s = str.toStdString();

		if (s == "x")
		{
			if (std::string::npos == getXTag().find("X"))
				return false;
			return true;
		}
		else if(s == "y")
		{
			if (std::string::npos == getXTag().find("Y"))
				return false;
			return true;
		}
		else if (s == "z")
		{
			if (std::string::npos == getXTag().find("Z"))
				return false;
			return true;
		}
		else if (s == "phi")
		{
			if (std::string::npos == getXTag().find("sin"))
				return false;
			return true;
		}
		else if (s == "rho")
		{
			if (std::string::npos == getXTag().find("cos"))
				return false;
			return true;
		}
		return false;
	}

	/**
	* @brief phasorData::getAllCutRoom 获取全部切割空间
	* @return QVector<QRectF>
	*/
	QVector<QRectF> phasorData::getAllCutRoom() {
		return mPiflist_rect;
	}
	/**
	* @brief phasorData::initVectorData 初始化向量相关数据
	* @return bool
	*/
	bool phasorData::initVectorData()
	{
		Data::ListValuesPtr DataValueslist;
		bool ok = autoModGetSourceData(DataValueslist);
		if (!ok && !DataValueslist && DataValueslist->size() == 0)
			return false;
		auto iter = DataValueslist->begin();
		Data::ValuesPtr datasetEmA;
		Data::ValuesPtr datasetEmB;
		Data::ValuesPtr datasetEmC;
		if (this->istrue)
		{
			datasetEmB = *iter; iter++;
			datasetEmA = *iter; iter++;
			datasetEmC = *iter;
		}
		else
		{
			datasetEmA = *iter; iter++;
			datasetEmB = *iter; iter++;
			datasetEmC = *iter;
		}
#if 0
		//如果数据与结构是反的，那么需要对调场数据
		if (!getDataDirection())
		{
			auto size = datasetEmC->size() / 2;
			float temp = 0;
			for (int i = 0; i < size; i++)
			{
				temp = (*datasetEmC)[i];
				(*datasetEmC)[i] = (*datasetEmC)[i + size];
				(*datasetEmC)[i + size] = temp;
			}
		}
#endif

		if (mPiflist_rect.empty())
			return false;
		//获取起点p1
		QVector<qreal> dataC;
		for (auto iterC = datasetEmC->begin(); iterC != datasetEmC->end(); iterC++)
			dataC.push_back(*iterC);
		for (auto i = 0; i < mPiflist_rect.size(); i++)
		{
			p1.push_back(QPointF(mPiflist_rect[i].left(), mPiflist_rect[i].bottom()));
		}
		float Svector = 0;//最大系数
		unsigned int index_vector = 0;//
		for (auto i = 0; i < mPiflist_rect.size(); i++)
		{
			float curlen = sqrt(dataC[i] * dataC[i] + dataC[i + mPiflist_rect.size()] * dataC[i + mPiflist_rect.size()]);
			if (Svector < curlen)
			{
				Svector = curlen;
				index_vector = i;
			}
		}
		sizeScale.clear();
		sizeScale.reserve(mPiflist_rect.size());
		for (auto i = 0; i < mPiflist_rect.size(); i++)
		{
			float x_coef;
			float y_coef;
			if (this->istrue)
			{
				y_coef = dataC[i];
				x_coef = dataC[i + mPiflist_rect.size()];
			}
			else
			{
				x_coef = dataC[i];
				y_coef = dataC[i + mPiflist_rect.size()];
			}
			if (x_coef<0.0000001 && x_coef>-0.0000001 &&
				y_coef<0.0000001 && y_coef>-0.0000001)
			{
				p2.push_back(QPointF(0.0, 0.0));
				len_coef.push_back(QPointF(0.0, 0.0));
				sizeScale.push_back(0);
			}
			else
			{
				len_coef.push_back(QPointF(x_coef, y_coef));
				float _p2Len = sqrt(x_coef * x_coef + y_coef * y_coef);
				float rotation = _p2Len / Svector;
				sizeScale.push_back(rotation);
				QPointF _p2;
				_p2.setX(x_coef / _p2Len);
				_p2.setY(y_coef / _p2Len);
				p2.push_back(_p2);
			}

		}
		//去除不必要的向量
		for (auto i = p1.size() - 1; i >= 0; i--)
		{
			if (sizeScale[i] > -0.000001 && sizeScale[i] < 0.000001)
			{
				p1.erase(p1.begin() + i);
				len_coef.erase(len_coef.begin() + i);
				p2.erase(p2.begin() + i);
				sizeScale.erase(sizeScale.begin() + i);
			}
		}
		return true;
	}
	/**
	* @brief phasorData::Getp1Point 获取向量的起始点位集合
	* @return QVector<QPointF>
	*/
	QVector<QPointF> phasorData::Getp1Point() {
		return p1;
	}
	/**
	* @brief phasorData::Getp2Point 获取向量的终点集合
	* @return QVector<QPointF>
	*/
	QVector<QPointF> phasorData::Getp2Point() {
		return p2;
	}
	/**
	* @brief phasorData::findindexlen_coef 索引向量的长度系数
	* @param int index
	* @return QPointF
	*/
	QPointF phasorData::findindexlen_coef(int index)
	{
		auto iter = len_coef.begin() + index;
		if (iter != len_coef.end())
		{
			return *iter;
		}
		return QPointF(0.0, 0.0);
	}
	/**
	* @brief phasorData::findindexP1 索引向量的起点
	* @param int index
	* @return QPointF
	*/
	QPointF phasorData::findindexP1(int index)
	{
		auto iter = p1.begin() + index;
		if (iter != p1.end())
		{
			return *iter;
		}
		return QPointF(0.0, 0.0);
	}

	std::string phasorData::getInformationTitle()
	{
		std::string title;
		const std::string end = "  ";
		title += "观察时间";
		title += DataInformationGetter::getObserveTime(headList.at(13)) + end;
		title += "观察分量:";
		title += DataInformationGetter::getVectorParam(headList.at(11)) + end;

		return title;
	}
	//获取取值范围
	Data::Rang phasorData::getXRang()
	{
		std::lock_guard<std::mutex> am(xRangMutex);
		return xRang;
	}
	Data::Rang phasorData::getYRang()
	{
		std::lock_guard<std::mutex> am(yRangMutex);
		return yRang;
	}
	//设置取值范围
	void phasorData::setXRang(const Rang& xr)
	{
		std::lock_guard<std::mutex> am(xRangMutex);
		xRang = xr;
	}
	void phasorData::setYRang(const Rang& yr) {
		std::lock_guard<std::mutex> am(yRangMutex);
		yRang = yr;
	}
	phasorData::DISMODE phasorData::GetdisMode() {
		return disMode;
	}
	std::vector<float> phasorData::getScaleVal() {
		return sizeScale;
	}
	void phasorData::setdisMode(DISMODE a) {
		disMode = a;
	}
	//2021年5月19日---新增加
	Data::Rang phasorData::getdefXrang()
	{
		return defXrang;
	}
	Data::Rang phasorData::getdefYrang()
	{
		return defYrang;
	}
	int phasorData::getXsize()
	{
		return posxSize;
	}
	int phasorData::getYsize()
	{
		return posySize;
	}
	/********************************************/
	phasorinfo::phasorinfo() :p1(0.0, 0.0), p2(0.0, 0.0), phasor_room(0.0, 0.0, 0.0, 0.0), room_property(0) {}
	void phasorinfo::SetRectF(QRectF _rectf) {
		phasor_room = _rectf;
	}
};
