#pragma once
#include <memory>
#include <mutex>
#include <vector>
#include <QStringList>
#include <QString>
class FileFormat{
public:
	FileFormat(){}
	virtual ~FileFormat(){}
protected:
	QString format;
public:
	//打开文件的触发函数
	virtual void open(const QStringList& fileList) = 0;
	//判断文件格式函数
	QStringList isFormat(QStringList& fileList);
	//获取文件格式的后缀
	QString getFormat(){
		return format;
	}
};
class FileFormatM3DText:public FileFormat{
public:
	FileFormatM3DText();
	~FileFormatM3DText() = default;

	void open(const QStringList& fileList) override;

private:
	void openOnce(const QString& filePath);
};
class FileFormatM2DText :public FileFormatM3DText
{
public:
	FileFormatM2DText(){
		this->format = QString::fromLocal8Bit("m2d");
	}
	~FileFormatM2DText() = default;
};
/*
	改变原有的freecad增加新的文件格式框架。
	单例负责为外部调用提供文件格式与触发函数。
	新增新的文件打开方式，在OpenFIleConfig.init()中注册即可
*/
class OpenFileConfig{
public:
	~OpenFileConfig();
	static std::shared_ptr<OpenFileConfig> GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new OpenFileConfig);
		});
		return _instance;
	}
	OpenFileConfig(const OpenFileConfig&) = delete;
	OpenFileConfig operator =(const OpenFileConfig&) = delete;

private:
	OpenFileConfig(){init();};
	static std::shared_ptr<OpenFileConfig> _instance;
	//格式对象容器
	std::vector<FileFormat*> formats;
private:
	//初始化
	void init();
public:
	//根据文件路径，调用open函数
	void callOpen(QStringList& fileList);
	//所有文件格式，生成文件浏览器需要的字符串
	QString makeFormatString();
};