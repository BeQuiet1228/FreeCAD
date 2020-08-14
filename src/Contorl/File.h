#pragma once
#include <QFile>
class File
{
public:
	File();
	~File();

public:
	//只读打开
	bool openForReadonly();
	bool openForReadonly(const std::string& path);
	//只写打开
	bool openForAppend();
	bool openForAppend(const std::string& path);
	//设置路径
	void setPath(const std::string& path){
		this->path = QString::fromLocal8Bit(path.c_str());
	}
	void setPath(const QString& path){
		this->path = path;
	}
	//读取下一个块数据
	bool readNextData(QByteArray& bytes, const int& maxLength = 2*1024*1024);
	//写入数据
	bool writeData(const QByteArray& bytes);
private:
	//路径
	QString path;
	//文件对象
	QFile file;

};