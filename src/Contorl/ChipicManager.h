#pragma once
#include <QObject>
#include <map>
#include <Windows.h>
#include <memory>
#include "ContorlConfig.hpp"
class Chipic;
class LoadingDialog;
class ContorlButtonBar;
class ContorlDataBar;
class CONTROL_EXPORT ChipicManager :public QObject
{
	Q_OBJECT
public:
	ChipicManager();
	~ChipicManager();
	enum RunType{
		AUTO,
		MANUAL
	};
private:
	//载入提示框
	LoadingDialog *loadingDialog;
	//运行类似
	RunType runType = MANUAL;
public:
	//当前管理的计算程序
	std::shared_ptr<Chipic> CurrentChipic;
	//计算程序集合
	std::map<DWORD, std::shared_ptr<Chipic>> chipicMap;
Q_SIGNALS:
	//当前计算程序有信息更新
	void currentChipicStateUpdate();
	//chipic计算完成 并将文件路径发送出去
	void finishChipicM3dPath(unsigned long);
	//chipic成功启动信号
	void chipicStartFinished(unsigned long);
public Q_SLOTS:
	void hasNewMessage();
	//更新ui状态
	void chipicStateUpdate(DWORD threadId);
	//运行按钮被点击
	void runButtonClicked(const std::string& m3dPath = "");
	//关闭当前运行的chipic
	void closeCurrentChipic();
	//chipic计算完成
	void chipicWorkFinished();
	//chipic解析完成信号
	void chipicAnalysisFinished();
	//load提示框被关闭
	void loadDialogClose();
public:
	//关闭一个chipic
	void closeChipic(const unsigned long threadID);
	//初始化消息发射器
	void initMessageSender();
	//并行按钮被点击
	void ButtonParalleRunClicked(const std::string& m3dPath);
	//发送启动消息
	void sendStartChipicMessage(const std::string& path, const int& threadCount);
	//设置运行状态
	void setRunType(const RunType& runType){
		this->runType = runType;
	}
	//获取一个chipic的m3d路径
	QString getM3dpathForThreadID(unsigned long threadID);
private:
	//检测路径是否存在
	bool detectionFilePathUTF8(const std::string& path);
	//处理消息
	bool disposeMessage(const std::string& json);
	//处理关闭chipic的消息
	bool disposeCloseChipicMessage(const DWORD& threadId,const int& errorCode = 0);
	//处理启动chipic的消息
	bool dispoesStartChipicMessage(const std::string json);
	//弹出启动载入提示框
	void showLoadDailog();
	//弹出计算完成提示框
	void showWorkFinishedBox();
	//弹出一个提示框
	void showDailLog(const std::string& title, const std::string& content);
};