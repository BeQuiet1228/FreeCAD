#include "AlgorMDIInter.h"
#include "QHBoxLayout"
#include "Transition/transition.h"
#include "QMessageBox"
#include "DataVisualization/C_encoding.h"
AlgorMDIInter::AlgorMDIInter(DocumentPic* pcDocument, QWidget* parent):
	MDIViewPIC(pcDocument,parent)
{

}
AlgorMDIInter::~AlgorMDIInter() {

}
bool AlgorMDIInter::isClose()
{
	return false;
}
void AlgorMDIInter::closeEvent(QCloseEvent* e)
{
	bool ok = isClose();
	if (!ok)
	{
		//弹出提示框
		QMessageBox::StandardButton result = QMessageBox::information(
			nullptr,
			GetEncodingstr("提示",ENCODING_GB2312),
			GetEncodingstr("程序正在运行,是否关闭?",ENCODING_GB2312), QMessageBox::Yes|QMessageBox::No);
		switch (result)
		{
		case QMessageBox::Yes:
			break;
		case QMessageBox::No:
		{
			e->ignore();
			return;
		}
			break;
		default:
			break;
		}
	}
	MDIViewPIC::closeEvent(e);
}