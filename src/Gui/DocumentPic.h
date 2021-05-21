#pragma once
#include "Document.h"
#include "app/Document.h"
#include "Application.h"
class DocumentPic :public Gui::Document {
public:
	DocumentPic(App::Document* pcDocument, Gui::Application* app);
	~DocumentPic() = default;

public:
	//初始化mdi窗口
	void initMDIView();
	//获取app doc
	App::Document* getAppDocument();
	//释放doc中的h5文件对象
	void releaseH5Object();
};