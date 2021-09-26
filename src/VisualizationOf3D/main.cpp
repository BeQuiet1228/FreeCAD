//#include<QWidget>
#include"DataProcess.h"
#include<QApplication>
#include"QFileDialog"
#include"HDF5Reader/hdf5io.h"
//#include"qtextcodec.h"
int main(int argc, char* argv[])
{
	QApplication a(argc, argv);
	DataProcess dataprocess;
	QFileDialog* fileDialog = new QFileDialog();
	fileDialog->setWindowTitle("OpenFile");
	fileDialog->setDirectory(".");
	fileDialog->setFilter(("H5 Files(*.h5 *.H5)"));
	if (fileDialog->exec() == QDialog::Accepted)
	{
		QString h5fFilePath = fileDialog->selectedFiles()[0];
		
		Hdf5IO io(h5fFilePath.toStdString());
		io.initHdf5Data();
		auto datalist = io.hdf5DataList;
		for (auto iter = datalist.begin(); iter != datalist.end(); iter++)
		{
			if (iter->headList.size() >= 4 && iter->headList[3].find("PLANE") != std::string::npos)
			{
				dataprocess.initData(*iter);
				break;
			}
		}
	}
	return a.exec();
}