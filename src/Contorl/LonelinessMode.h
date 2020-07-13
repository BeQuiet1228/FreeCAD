#ifndef LONELINESSMODE_H
#define LONELINESSMODE_H
#include <memory>
#include <mutex>
#include <qthread.h>
#include <Windows.h>
#include <qlist.h>
#include "RunChipic3dListener.h"
#include "runchipic3d.h"
#include <qcoreevent.h>
class LonelinessMode;
struct Message;
struct PyMessage;
using LonelinessModePr = std::shared_ptr<LonelinessMode>;

/**
 * @brief 单机模式线程
 */
class LonelinessMode:public QThread
{
    Q_OBJECT
public:
    /**
     * @brief getIntance 获取对象
     * @return  对象
     */
    static LonelinessModePr getIntance()
    {
        //保证构造函数值被调用一次，且不能被多个线程同时调用
        static std::once_flag flag;
        std::call_once(flag,[&](){
            intance.reset(new LonelinessMode);
        });

        return intance;
    }

    ~LonelinessMode();
private:
    LonelinessMode();
    LonelinessMode(const LonelinessMode&) = delete;
    LonelinessMode& operator=(const LonelinessMode&) = delete;

    static LonelinessModePr intance;

protected:
    void run() override;

public:
    //添加任务
    bool addTask(const Message &msg);
    //获取任务
    Message getTask();
    //查看栈内任务数量
    int getTaskCount();
    //启动单机模式
    void lonelinessModeOn();
    //关闭单机
    void lonelinessModeOff();
    //获取标志
    bool getLonelinessModeFlag();
    //获取一个列队中的消息
    bool getPyMessage(PyMessage &msg);
    //将消息放入消息队列
    void addPyMessage(const PyMessage &msg);
    //启动chipic3d
    void startChipic3d(const std::string path,const int &count = 1);
    //结束chipic3d的运行
    void killChipic3d();
    /**
     * @brief getOnLonelinessMod 获取是否启用单机模式
     * @return 启用返回true
     */
    bool getOnLonelinessMod(){ return onLonelinessMod;}
    /**
     * @brief useLonelinessMod 启用单机模式
     */
    void useLonelinessMod(){ onLonelinessMod = true;}
    /**
     * @brief uselongRangeMod 启用远程模式
     */
    void uselongRangeMod(){ onLonelinessMod = false;}
    /**
     * @brief getCchipicIsPause 获取chipic的暂停状态
     * @return 如果chipic为暂停状态，则返回true。运行状态则返回false
     */
    bool getCchipicIsPause(){return  chipicIsPause;}
    /**
     * @brief getChipicTimerState 返回chipic定时器的状态
     * @return 如果定时器为开，则返回true
     */
    bool getChipicTimerState(){return  chipicTimerState;}
	//定时器事件
	virtual void timerEvent(QTimerEvent *event);
private:
    //处理chipic3d发送过来的消息
    void disposeWinMessage(Message &msg);
    //处理gui文件消息
    bool disposeGuiFileWinMessage(Message &msg);
    //处理查看计算结果图形消息
    bool disposeHdf5FileWinMessage(Message &msg);
	//生成对应的文件路径
	std::string makeFilePath(const std::string &fileName);
	//处理器件结构文件消息
	bool disposeStructHdf5File(Message &msg);
    //检测chipic3d是否还在运行
    void detectionChipic3dIsRun();
    //处理刷新计算进度消息
    bool disposeRefreshMsg(Message &msg);
    //处理迭代次数
    bool disposeChipicCount(Message &msg);
    //处理chipic运算消耗时间
    bool disposeChipicUsedTime(Message &msg);
    //处理chipic的暂停状态消息
    bool disposeChipicIsPause(Message &msg);
    //处理定时器状态消息
    bool disposeChipicTimerState(Message &msg);
private:
    //任务列队锁
    std::mutex taskStackMutex;
    //标志锁
    std::mutex flagMutex;
    //接收消息队列锁
    std::mutex messageStackMutex;
    //消息栈
    QList<PyMessage> messageStack;
    //任务栈
    QList<Message> taskStack;
    //是否开启单机模式标志
    bool modeFlag;
    //消息管理器
	RunChipic3dListener messgaeManager;
    //内核计算时的线程数量
    int chipic3dTreadCount;
    //m3d文件名称
    QString  m3dFileName;
	//m3d文件路径
	QString m3dFilePath;
    //是否启用单机模式
    bool onLonelinessMod;
    //内核的运行状态
    bool chipicIsPause;
    //内核定时器的状态
    bool chipicTimerState;
	//定时器id
	int timerId;
public Q_SLOTS:
    //接收消息完成槽
    void receiveMessageFinished(Message msg);

Q_SIGNALS:
    //接收消息完成信号
    void receiveMessageFinishedSignal(Message msg);

};

/**
 * @brief The PyMessageType enum python消息的类型
 */
enum PyMessageType
{
    NO_MSG = 0,     //没有消息
    WIN_MSG,    //单纯的winmesg消息
    STRING,     //字符消息
	FILE_NANE,   //文件名，各种图的文件名
	STRUCT_FILE_NAME, //结构图文件名
    GUI_FILE_NAME,	//.gui类型文件
    CHIPIC_IS_OVER, //chipic程序已退出
    CHIPIC_COUNT, //chipic运算次数
    CHIPIC_USED_TIME, //chipic计算使用的时间
    CHIPIC_PAUSE_STATE, //chipic暂停状态消息
    CHIPIC_TIMER_STATE //chipic定时器消息
};
/**
 * @brief The PyMessage struct 发送给Python的消息结构
 */
struct PyMessage
{
	PyMessage(){
		type = PyMessageType::NO_MSG;
		id = 0;
		wParam = 0;
		lParam = 0;
		str = "";
		fileName = "";
	}
    PyMessageType type; //消息类型
    UINT id; //消息id
    WPARAM wParam; //短参数
    LPARAM lParam; //长参数
    std::string str;    //字符信息
    std::string fileName;   //文件名称
};
#endif // LONELINESSMODE_H
