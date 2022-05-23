#pragma once
#include <QStandardItem>
#include <HDF5Reader/hdf5io.h>
#include <memory>
#include <QList>
namespace Gui {
	class HDF5DataItemEventHander;
	/*
	* 注意：
		所有设置了parent的item的内存会交给Qt管理，
		在合并，或者添加是会有一些多余的item产生，那么这个时候会自动释放掉这些item。
		尽管有些多余的item是从外部传入的，所以传入item时尽量不要在外部保留指针，或者对指针进行释放操作。
	*/
	class HDF5DataItem :public QStandardItem{
	public:
		enum ItemType {
			FILE = 0,	//文件
			FOLDER		//文件夹
		};
	public:
		HDF5DataItem() = delete;
		HDF5DataItem(const QString& name, const ItemType& type = FOLDER);
		HDF5DataItem(const Hdf5Data &h5data,const QString &name,const ItemType& type = FILE);
		HDF5DataItem(const HDF5DataItem& item);
		~HDF5DataItem();

	public:
		int type() const override;

		//get set
		void setDoubleClickEventHander(std::shared_ptr<HDF5DataItemEventHander> hander);
		std::shared_ptr<HDF5DataItemEventHander> getDoubleClickEventHander();

		void setHdf5Data(const Hdf5Data& data);
		Hdf5Data getHdf5Data();

		void setName(const QString& name);
		QString getNmae();


		//触发双击事件
		virtual void triggerDoubleClickEvent();

		//添加子节点
		HDF5DataItem* addSubItem(HDF5DataItem* subItem);
		//获取所有子节点
		std::vector<HDF5DataItem*> getSubItems();
		//合并两个相同的item
		bool mergeItem(HDF5DataItem* item);
		bool mergeItem(QStandardItem* item, HDF5DataItem* h5item);

	public:
		//重写运算符
		bool operator==(const HDF5DataItem& item);
		bool operator!=(const HDF5DataItem & item);
		bool operator>(const HDF5DataItem& item);
		bool operator<(const HDF5DataItem& item);
	public:
		void deleteQlistQStandardItem(QList<QStandardItem*> listItem);
		//从一个list中拿走第一个并转换类型
		HDF5DataItem* getHDF5DataItemFromQListItem(QList<QStandardItem*> listItem);
	private:
		Hdf5Data hdf5data;
		QString name;
		ItemType itemType;
		static const QString IconPath[2];
		//双击事件处理器
		std::shared_ptr<HDF5DataItemEventHander> doubleClickEventHander;

	};
}