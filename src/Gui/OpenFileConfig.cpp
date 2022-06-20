#include "PreCompiled.h"

#include "OpenFileConfig.h"
#include <iostream>
#include <Application.h>
#include <QDir>
#include "App/DocumentM3dText.h"
#include "MDIEditView.h"
#include "MainWindow.h"
#include <FileDialog.h>
#include "FileFormatH5.h"
#include "Transition/transition.h"
std::shared_ptr<OpenFileConfig> OpenFileConfig::_instance;
OpenFileConfig::~OpenFileConfig()
{
	for (auto i = formats.begin(); i != formats.end(); i++)
	{
		delete (*i);
	}
	formats.clear();
}

/**
* @brief OpenFileConfig::init 初始化所有的format
* @return void
*/
void OpenFileConfig::init()
{
	formats.push_back(new FileFormatM3DText);
	formats.push_back(new FileFormatM2DText);
	formats.push_back(new FileFormatM2dMod);
	formats.push_back(new FileFormatH5);
	formats.push_back(new FileFormatM3dMod);
}

/**
* @brief OpenFileConfig::callOpen 
* @param const QStringList & fileList
* @return void
*/
void OpenFileConfig::callOpen(QStringList& fileList)
{
	for (auto formatIter = formats.begin(); formatIter != formats.end(); formatIter++)
	{
		QStringList pathList = (*formatIter)->isFormat(fileList);
		if (pathList.size() > 0)
			(*formatIter)->open(pathList);
	}
}

void OpenFileConfig::callOpen(std::list<std::string> fileList)
{
	QStringList sl;
	for (auto iter = fileList.begin(); iter != fileList.end(); iter++)
	{
		sl.push_back(gbkStdstringToQstring(*iter));
	}
	callOpen(sl);
}

/**
* @brief OpenFileConfig::makeFormatString 根据已初始化的文件格式 生成文件浏览器需要的文件格式
* @return QString
*/
QString OpenFileConfig::makeFormatString()
{
	QString temp;
	for (auto i = formats.begin(); i != formats.end(); i++)
	{
		temp += QString::fromLocal8Bit(" *.")  + (*i)->getFormat();
	}
	return temp;
}

/**
* @brief FileFormat::isFormat 检查导入文件中是否有
* @param const QStringList & fileList
* @return QStringList 
*/
QStringList  FileFormat::isFormat(QStringList& fileList)
{
	QStringList list;
	
	int formatLen = format.length();
	for (auto i = fileList.begin(); i != fileList.end();)
	{
		auto temp = i->right(formatLen).toLower();
		if (format.toLower() == temp)
		{
			list.append(QString(*i));
			//在这里移除掉已经匹配的文件格式
			i = fileList.erase(i);
		}else{
			i++;
		}
				
	}
	return list;
}

FileFormatM3DText::FileFormatM3DText()
{
	this->format = QString::fromLocal8Bit("m3d");
}

void FileFormatM3DText::open(const QStringList& fileList)
{
	for (auto i = fileList.begin(); i != fileList.end(); i++)
	{
		QDir dir(*i);
		QString fileName = dir.dirName();
		App::Document* doc = App::GetApplication().newDocumentM3dText(i->toUtf8().data(),fileName.toUtf8(), "");
		openOnce(*i,doc);
		Gui::FileDialog::setWorkingDirectory(QString(*i).remove(fileName));
	}
	
}

void FileFormatM3DText::openOnce(const QString& filePath, App::Document* doc)
{
	doc->FileName.setValue(filePath.toUtf8());
	DocumentM3dText *docText = static_cast<DocumentM3dText*>(doc);	
	if (!docText)
		return;
	docText->loadfile(filePath);
	auto  guiDoc = Gui::Application::Instance->getDocument(doc);
	auto view = guiDoc->getActiveView();

	MDIEditView *edit = static_cast<MDIEditView*>(view);
	if (!edit)
		return;
	edit->setWindowTitle(QString::fromLocal8Bit(docText->getName()));
	edit->setText(docText->getContent());
	//??	
	Gui::Application::Instance->ToSubItemTree();

}

void FileFormatM2dMod::open(const QStringList& fileList)
{
	for (auto iter = fileList.begin(); iter != fileList.end(); iter++)
	{
		App::GetApplication().openDocument2dMod(iter->toUtf8());
		Base::Interpreter().runString("FreeCADGui.runCommand('InitWhenOpenFcStd2d')");
	}
}

void FileFormatM2DText::open(const QStringList& fileList)
{
	for (auto i = fileList.begin(); i != fileList.end(); i++)
	{
		QDir dir(*i);
		QString fileName = dir.dirName();
		App::Document* doc = App::GetApplication().newDocumentM2dText(i->toUtf8().data(), fileName.toUtf8(), "");
		openOnce(*i, doc);
		Gui::FileDialog::setWorkingDirectory(QString(*i).remove(fileName));
	}
}

void FileFormatM3dMod::open(const QStringList& fileList)
{
	for (auto iter = fileList.begin(); iter != fileList.end(); iter++)
	{
		App::GetApplication().openDocument3dMod(iter->toUtf8());
		Base::Interpreter().runString("import Modeling\nModeling.Common.Tools.DocumentTools.initWhenOpenFCStdFile()\n");
	}
}
