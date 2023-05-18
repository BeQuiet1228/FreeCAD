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
	virtual void initMDIView();
	//获取app doc
	App::Document* getAppDocument();
	//释放doc中的h5文件对象
	void releaseH5Object();
	//获取m3d路径
	std::string getTextPath();
	//打开一个h5文件
	void openH5File(const std::string & path);
	//运行仿真程序
	void runChipic();
	//停止仿真程序
	void stopChipic();
	//并行运行
	void paralleRunChipic();
	//显示粒子群优化算法窗口
	void showParticleSwarmOptimizationView();
	//显示批处理窗口
	void showProcessingBatchView();
	//显示遗传算法窗口
	void showGeneticAlgorithmView();
	//显示多目标遗传算法
	void showMultipleTargetGeneticAlgorithmView();
	//显示G占优多目标遗传算法
	void showMultipleTargetGeneticAlgorithmGView();
	//检测加密狗是否存在
	bool disposSuperDog();

	//保存与另存为
	virtual void save();
	virtual void saveAs();

	//处理一些通用消息
	virtual bool onMsg(const char* pMsg, const char** ppReturn);
	virtual bool onHasMsg(const char* pMsg) const ;
};

class Document2DPic :public DocumentPic {
public:
	Document2DPic(App::Document* pcDocument, Gui::Application* app);
	virtual bool onHasMsg(const char* pMsg) const override;
};

class DocumentText :public DocumentPic {

public:
	DocumentText(App::Document* pcDocument, Gui::Application* app);
	~DocumentText() = default;

	void save() override;
	void saveAs() override;

	void initMDIView();

};
class DocumentText2D :public DocumentText {
public:
	DocumentText2D(App::Document* pcDocument, Gui::Application* app);
	virtual bool onHasMsg(const char* pMsg) const override;

};

class DocumentH5File :public DocumentPic {
public:
	DocumentH5File(App::Document* pcDocument, Gui::Application* app);
	~DocumentH5File() = default;;

	void  save() override {};
	void saveAs() override {};

	bool onHasMsg(const char* pMsg) const;
};

DocumentPic* CreatePICDocument(App::Document* doc,Gui::Application* app);