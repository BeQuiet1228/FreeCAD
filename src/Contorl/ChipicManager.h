#pragma once
#include <QObject>
#include <map>
#include <Windows.h>
#include <memory>
#include <list>
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
	//等待启动
	std::list<std::shared_ptr<Chipic>> waitStartChipic;
Q_SIGNALS:
	//当前计算程序有信息更新
	void currentChipicStateUpdate();
	//chipic计算完成 并将文件路径发送出去
	void finishChipicM3dPath(unsigned long);
	//chipic成功启动信号
	void chipicStartFinished(unsigned long);
	//解析完成消息
	void chipicAnalysisFinished(unsigned long);
	//chipic异常退出
	void chipicErrorClose(unsigned long);
	//有新的结果图文件被生成
	void newResultFIleSignal(unsigned long);
	//输出结构图
	void outputStructFileSignal(unsigned long);
	//打开输出结果
	void openH5Result(std::string path);
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
	//有新的结果图文件被生成
	void newResultFIleSlot(unsigned long threadID);
	//输出结构图
	void outputStructFileSlot(unsigned long threadID);
public:
	//关闭所有的chipic
	void closeAllChipic();
	//关闭一个chipic
	void closeChipic(const unsigned long threadID);
	//初始化消息发射器
	void initMessageSender();
	//并行按钮被点击
	bool ButtonParalleRunClicked(const std::string& m3dPath);
	//发送启动消息
	void sendStartChipicMessage(const std::string& path, const int& threadCount);
	//获取chipic的运行线程数
	int getChipicThreadCount(unsigned long threadID);
	//设置运行状态
	void setRunType(const RunType& runType){
		this->runType = runType;
	}
	RunType getRunType(){
		return this->runType;
	}
	//获取一个chipic的m3d路径
	QString getM3dpathForThreadID(unsigned long threadID);
	//清理掉所有chipic数据，但是不关闭内核
	void clearChipicData();
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
	//处理内核解析完成消息
	bool disposAnalysisFinished(const std::string& json);
};