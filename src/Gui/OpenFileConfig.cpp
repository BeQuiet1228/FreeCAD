#include "PreCompiled.h"

#include "OpenFileConfig.h"
#include <iostream>
#include <Application.h>
#include <QDir>
#include "App/DocumentM3dText.h"
#include "LuaEditView.h"
#include "MainWindow.h"
#include <FileDialog.h>
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
	{
		auto format = new FileFormatM3DText;
		formats.push_back(format);
	}

	{
		auto format = new FileFormatM2DText;
		formats.push_back(format);
	}
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
	std::cerr << "this is open m3d text! path :" << std::endl;


	for (auto i = fileList.begin(); i != fileList.end(); i++)
	{
		openOnce(*i);
	}
	
}

void FileFormatM3DText::openOnce(const QString& filePath)
{
	QDir dir(filePath);
	QString fileName = dir.dirName();
	App::Document* doc = App::GetApplication().newDocumentM3dText(fileName.toUtf8(), "");
	doc->FileName.setValue(filePath.toUtf8());
	DocumentM3dText *docText = static_cast<DocumentM3dText*>(doc);

	if (!docText)
		return;
	docText->loadfile(filePath);
	auto  guiDoc = Gui::Application::Instance->getDocument(doc);
	auto view = guiDoc->getActiveView();

	LuaEditView *edit = static_cast<LuaEditView*>(view);
	if (!edit)
		return;
	edit->setWindowTitle(QString::fromLocal8Bit(docText->getName()));
	edit->setText(docText->getContent());
	Gui::FileDialog::setWorkingDirectory(QString(filePath).remove(fileName));
}
