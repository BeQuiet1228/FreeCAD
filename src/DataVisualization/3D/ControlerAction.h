#pragma once
#include "action.h"
#include "ClipPlaneWidget.h"
#include <HDF5Reader/hdf5io.h>
#include <QString>

namespace DV3D {
	class Controler;
	
	class ControlerAction :public ActionSwitch{
	public:
		void active() {};
		virtual void active(std::shared_ptr<Controler> controler) = 0;
		virtual void initState(std::shared_ptr<Controler> controler) = 0;
	};

	class ControlerVisible :public ControlerAction {
	public:
		void active(std::shared_ptr<Controler> controler) override;
		void initState(std::shared_ptr<Controler> controler) override;
	};

	class ControlerEdgeVisible :public ControlerAction {

	public:
		void active(std::shared_ptr<Controler> controler) override;
		void initState(std::shared_ptr<Controler> controler) override;
	};

	class ControlerClipEnable :public ControlerAction {

	public:
		void active(std::shared_ptr<Controler> controler) override;
		void initState(std::shared_ptr<Controler> controler) override;
	};
	class ControlerClipPlan :public ControlerAction
	{
	public:
		void active(std::shared_ptr<Controler> controler) override;
		virtual void initState(std::shared_ptr<Controler> controler) override;
	private:
		void showWidget(std::shared_ptr<Controler> controler);
	};
	class ControlerSave :public ControlerAction {
	public:
		void active(std::shared_ptr<Controler> controler) override;
		void initState(std::shared_ptr<Controler> controler) override;
		//set get
		void setHdf5Data(const Hdf5Data& data);
		Hdf5Data getHdf5Data();
		void setPath(const QString& pt);
		QString getPath();
	private:
		Hdf5Data hdf5data;
		//文件浏览器打开的路径
		QString path;
	};
}