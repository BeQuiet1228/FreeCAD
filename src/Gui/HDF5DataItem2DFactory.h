#pragma once
#include"hdf5DataItemFactory.h"
namespace Gui
{
	class HDF5DataItem2DFactory :public HDF5DataItemFactory
	{
	public :
		HDF5DataItem2DFactory() = default;
		~HDF5DataItem2DFactory() = default;
	public :
		HDF5DataItemFactory::HDF5DataItems CreatHDF5Items(std::vector<Hdf5Data> datas) override;
		HDF5DataItem* CreatHDF5Item(Hdf5Data& data) override;

		HDF5DataItem* CreatStructDataItem(Hdf5Data& data,HDF5DataItem* parentItem=nullptr);
		HDF5DataItem* CreatStructDataItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatContourDataItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatContourDataItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatPhasespaceDataItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatPhasespaceDataItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatVectorDataItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatVectorDataItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatObserveDataItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatObserveDataItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatRangDataItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatRangDataItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatSmartControlDataItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatSmartControlDataItem(std::vector<Hdf5Data>& datas);
		void setStructData(Hdf5Data data);

	public:
		//初始化hander 结构图
		bool initDoubleClickHanderStructData(Hdf5Data& data);
		bool initDoubleClickHanderStructData(std::vector<Hdf5Data>& datas);
	private:
		std::string getEffePartStr(std::string str);
		HDF5DataItem* findTypeItem(HDF5DataItem* parentItem,std::string typeNodestr);
	};
}