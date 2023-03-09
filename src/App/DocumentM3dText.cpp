#include "PreCompiled.h"
#include "DocumentM3dText.h"
#include <QTextIStream>
#include <QFile>
#include <iostream>
#include <boost\filesystem\fstream.hpp>
#include <codecvt>
#include <QByteArray>
#include <QTextCodec>
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

	boost::filesystem::path::imbue(
		std::locale(std::locale(), new std::codecvt_utf8_utf16<wchar_t>()));
	boost::filesystem::path path(filePath);
	boost::filesystem::fstream fs(path, std::ios::out);
	if (fs.is_open()) {
		fs.clear();
		auto temp = this->content.toStdString();
		fs << this->content.toStdString();
		fs.close();
		return true;
	}else{
		std::cerr << " DocumentM3dText::save() fstream not open file ！" << std::endl;
		return false;
	}


	return false;
}


bool DocumentM3dText::loadfile(const QString& filePath)
{
	QFile file(filePath);

	if (!file.open(QIODevice::ReadOnly))
		return false;
	//设置文件路径
	this->FileName.setValue(filePath.toUtf8());
	
	/*
		临时增加编码的判断。
		由于utf8与gbk的编码规则有一定的重合，所以再某些特殊情况下没有办法正确的判断编码方式。
		在那时先这样。
	*/
	QByteArray byte = file.readAll();
	if (isGbk(byte.data()))
	{
		QTextCodec* pCodec = QTextCodec::codecForName("gb2312");
		if (!pCodec) 
			return false;
		this->content = pCodec->toUnicode(byte.data(), byte.length());

	}else{
		this->content = QString::fromUtf8(byte.data());
	}
	file.close();
	return true;
}

bool DocumentM3dText::isGbk(const char* str)
{
	unsigned int nBytes = 0;//GBK可用1-2个字节编码,中文两个 ,英文一个
	unsigned char chr = *str;
	bool bAllAscii = true; //如果全部都是ASCII,
	for (unsigned int i = 0; str[i] != '\0'; ++i){
		chr = *(str + i);
		if ((chr & 0x80) != 0 && nBytes == 0){// 判断是否ASCII编码,如果不是,说明有可能是GBK
			bAllAscii = false;
		}
		if (nBytes == 0) {
			if (chr >= 0x80) {
				if (chr >= 0x81 && chr <= 0xFE){
					nBytes = +2;
				}
				else{
					return false;
				}
				nBytes--;
			}
		}
		else{
			if (chr < 0x40 || chr>0xFE){
				return false;
			}
			nBytes--;
		}//else end
	}
	if (nBytes != 0) {   //违返规则
		return false;
	}
	if (bAllAscii){ //如果全部都是ASCII, 也是GBK
		return true;
	}
	return true;
}
