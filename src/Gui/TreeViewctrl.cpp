#include "PreCompiled.h"
#include"TreeViewctrl.h"
#include "App/Document.h"
#include "App/DocumentDataManager.h"
#include <HDF5Reader/hdf5io.h>
#include "Contorl/ContorlInterface.h"
//
#include "Gui/Document.h"
namespace Gui{
	TreeViewCtrl::TreeViewCtrl(QWidget* parent):ListTreeWidget(parent){

	}
	TreeViewCtrl::~TreeViewCtrl()
	{

	}
	void TreeViewCtrl::double_clicked_event(const QModelIndex &index)
	{
		/*App::Document *doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (!docM)
			return;*/

		//QString filePath = makeFilePath(threadID);
		//if (filePath == tr(""))
		//	return;
		////打开结构图文件 获取结构图对象
		//Hdf5IO tempIO;
		//tempIO.setFilePath(filePath.toStdString());
		//tempIO.initHdf5Data();
		//if (tempIO.hdf5DataList.size() < 1)
		//	return;

		////打开h5文件 存储临时的数据
		//Hdf5IO newHdf5IO;
		//newHdf5IO.setFilePath(this->tempFilePath.toStdString());
		//auto structData = tempIO.hdf5DataList.begin();
		//auto newStructData = Hdf5IO::copyToHdf5IO(newHdf5IO, *structData);
		//docM->DisplatPlot(newStructData);

	}
};
//#include "moc_TreeViewctrl.cpp"