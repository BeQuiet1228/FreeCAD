#pragma once
#include <QObject>
#include <map>
#include <Windows.h>
#include <memory>
class Chipic;
class LoadingDialog;
class  ChipicManager:public QObject
{
	Q_OBJECT
public:
	ChipicManager();
	~ChipicManager();
private:
	//计算程序集合
	std::map<DWORD, std::shared_ptr<Chipic>> chipicMap;
	//载入提示框
	LoadingDialog *loadingDialog;
public:
	//当前管理的计算程序
	std::shared_ptr<Chipic> CurrentChipic;
Q_SIGNALS:
	//当前计算程序有信息更新
	void currentChipicStateUpdate();
public Q_SLOTS:
	void hasNewMessage();
	//更新ui状态
	void chipicStateUpdate(DWORD threadId);
	//运行按钮被点击
	void runButtonClicked(const std::string& m3dPath = "");
	//关闭当前运行的chipic
	void closeCurrentChipic();

public:
	//并行按钮被点击
	void ButtonParalleRunClicked(const std::string& m3dPath);

private:
	//检测路径是否存在
	bool detectionFilePathUTF8(const std::string& path);
	//处理消息
	bool disposeMessage(const std::string& json);
	//处理关闭chipic的消息
	bool disposeCloseChipicMessage(const DWORD& threadId);
	//处理启动chipic的消息
	bool dispoesStartChipicMessage(const std::string json);
};