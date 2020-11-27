#pragma once
#include "Document.h"
#include <QString>
class AppExport DocumentM3dText :public App::Document{
public:
	DocumentM3dText();
	~DocumentM3dText();

public:
	//继承顶级父类的save函数
	void Save(Base::Writer &writer) const override;

	//快捷调用的save函数 这个会在命令里被调用
	bool save() override;
	//撤销与恢复 这里暂时用不到，所以在这里继承之后不做操作
	bool undo() override{ return true; };
	bool redo() override{ return true; };

public:
	//载入文本文件
	bool loadfile(const QString& filePath);
	//获取文本
	QString getContent(){
		return content;
	}
	//设置文本
	void setContent(const QString& c){
		content = c;
	}
	//添加文本
	void appendContent(const QString& c){
		content += c;
	}

private:
	QString content;

};