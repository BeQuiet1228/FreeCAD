#include "File.h"
#include "iostream"
File::File()
	:path("")
{

}

File::~File()
{
	if (file.isOpen())
		file.close();
}

/**
* @brief File::openForReadonly 只读打开文件
* @return bool
*/
bool File::openForReadonly()
{
	if (file.isOpen())
		file.close();

	file.setFileName(path);

	return file.open(QIODevice::ReadOnly);
}

/**
* @brief File::openForReadonly 只读打开文件
* @param const std::string & path
* @return bool
*/
bool File::openForReadonly(const std::string& path)
{
	this->setPath(path);
	return this->openForReadonly();
}

/**
* @brief File::openForAppend 以追加文件的方式打开文件,写入文件时总是写入到文件末尾
* @return bool
*/
bool File::openForAppend()
{
	if (file.isOpen())
		file.close();

	file.setFileName(path);

	return file.open(QIODevice::WriteOnly | QIODevice::ReadOnly | QIODevice::Append);
}

/**
* @brief File::openForAppend 以追加文件的方式打开文件,写入文件时总是写入到文件末尾
* @param const std::string & path
* @return bool
*/
bool File::openForAppend(const std::string& path)
{
	this->setPath(path);
	return this->openForAppend();
}

/**
* @brief File::readNextData 读取下一块数据
* @param QByteArray & bytes 
* @param const int & maxLength 一块数据的长度  默认为2m
* @return bool 读取是否成功
*/
bool File::readNextData(QByteArray& bytes, const int& maxLength /*= 2*1024*1024*/)
{
	if (!file.isOpen())
	{
#ifdef MY_LOG
		std::cerr << "File::readNextData file is not open!" << std::endl;
#endif // MY_LOG
		return false;
	}

	bytes = file.read(maxLength);
	if (bytes.isEmpty())
		return false;

	return true;
}

/**
* @brief File::writeData 向文件末尾写入数据
* @param const QByteArray & bytes
* @return bool
*/
bool File::writeData(const QByteArray& bytes)
{
	if (!file.isOpen())
	{
#ifdef MY_LOG
		std::cerr << "File::writeData file is not open!" << std::endl;
#endif // MY_LOG
		return false;
	}

	int error = file.write(bytes);
	if (error == -1)
		return false;
	return true;

}

