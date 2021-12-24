#pragma  once
#include <vector>
#include <HDF5Reader/hdf5io.h>
#include "Hdf5DataItem.h"
#include <memory>
#include "Hdf5DataItemEventHandler.h"
namespace Gui {
	class HDF5DataItemFactory {
	public:
		using HDF5DataItems = std::vector<HDF5DataItem*>;
	public:
		HDF5DataItemFactory() = default;
		~HDF5DataItemFactory() = default;

	public:
		virtual HDF5DataItems CreatHDF5Items(std::vector<Hdf5Data> datas) = 0;
		virtual HDF5DataItem* CreatHDF5Item(Hdf5Data& data) = 0;

		//get set
		void setEventHander(std::shared_ptr<HDF5DataItemEventHander> hander);
		std::shared_ptr<HDF5DataItemEventHander> getEventHander();

	protected:
		//为item添加事件处理器
		void itemSetHander(HDF5DataItem* item);
	private:
		std::shared_ptr<HDF5DataItemEventHander> eventHader;

	};
	
	class HDF5DataItem3DFactory :public HDF5DataItemFactory{
	public:
		HDF5DataItem3DFactory() = default;
		~HDF5DataItem3DFactory() = default;

	public:
		HDF5DataItemFactory::HDF5DataItems CreatHDF5Items(std::vector<Hdf5Data> datas) override;
		HDF5DataItem* CreatHDF5Item(Hdf5Data& data) override;

		HDF5DataItem* CreatStructDataItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatStructDataItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatParticle3DItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatParticle3DItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatContour3DItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
		HDF5DataItem* CreatContour3DItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatContour2DItem(std::vector<Hdf5Data>& datas);
		HDF5DataItem* CreatContour2DItem(Hdf5Data& data, HDF5DataItem* parentItem = nullptr);
	};
}