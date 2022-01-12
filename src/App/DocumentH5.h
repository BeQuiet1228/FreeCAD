#pragma once
#include "Document.h"
#include <HDF5Reader/hdf5io.h>
#include <memory>
namespace App {
	class AppExport DocumentH5 :public Document {
	public:
		DocumentH5();
		~DocumentH5();

	public:
		//继承顶级父类的save函数
		void Save(Base::Writer& writer) const override;

		//快捷调用的save函数 这个会在命令里被调用
		bool save() override;
		//撤销与恢复 这里暂时用不到，所以在这里继承之后不做操作
		bool undo() override ;
		bool redo() override ;

		//载入hdf5文件
		void loadHdf5File(const std::string& path);
		std::shared_ptr<Hdf5IO> getHdf5IO();
	private:
		std::shared_ptr<Hdf5IO> hdff5IO;

	};

}