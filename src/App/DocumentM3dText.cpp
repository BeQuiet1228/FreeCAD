#include "PreCompiled.h"
#include "DocumentM3dText.h"
#include <QTextIStream>
#include <QFile>
#include <iostream>
#include <boost\filesystem\fstream.hpp>
#include <codecvt>
DocumentM3dText::DocumentM3dText()
{
	classID = 1;
}

DocumentM3dText::~DocumentM3dText()
{

}

void DocumentM3dText::Save(Base::Writer &writer) const
{

}

bool DocumentM3dText::save()
{
	auto  filePath = this->FileName.getValue();

	boost::filesystem::path path(filePath);
	boost::filesystem::path::imbue(
		std::locale(std::locale(), new std::codecvt_utf8_utf16<wchar_t>()));
	boost::filesystem::fstream fs(path, std::ios::out);
	fs.clear();
	fs << this->content.toStdString();
	fs.close();

	return true;
}


bool DocumentM3dText::loadfile(const QString& filePath)
{
	QFile file(filePath);

	if (!file.open(QIODevice::ReadOnly))
		return false;
	//设置文件路径
	this->FileName.setValue(filePath.toUtf8());
	

	QTextStream stream(&file);
	content = stream.readAll();
	file.close();
	return true;
}
