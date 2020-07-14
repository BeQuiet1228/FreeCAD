#include "lonelinessmode.h"
#include <QtCore/qmetatype.h>
#include <qdir.h>

//初始化静态变量
LonelinessModePr LonelinessMode::intance;

LonelinessMode::LonelinessMode()
{
    modeFlag = false;
    //注册自定信号类型
    qRegisterMetaType<Message>("Message");
    //绑定接收消息信号与槽
    connect(this,SIGNAL(receiveMessageFinishedSignal(Message)),
            this,SLOT(receiveMessageFinished(Message)));
    //初始化运行模式
    useLonelinessMod();
	//初始化定时器状态
	chipicTimerState = true;
	//初始化运行模式
	onLonelinessMod = true;
	//初始化定时器
	timerId = this->startTimer(10000);
}

LonelinessMode::~LonelinessMode()
{
	if (QThread::isRunning())
	{
		//关闭内核程序
		messgaeManager.sendMessage(WM_USER,0,0);
		this->quit();
		this->wait();
	}
    
}
/**
 * @brief LonelinessMode::run 消息监听、任务监听线程
 */
void LonelinessMode::run()
{
    //初始化消息管理器
    messgaeManager.init();
    //进去消息监听与任务监听
    while (this->getLonelinessModeFlag()) {
        //判断任务列队是否有任务，有则执行一个
        if(this->getTaskCount() > 0)
        {
            Message msg = this->getTask();
            messgaeManager.sendMessage(msg.Msg,msg.wParam,msg.lParam);
        }
        //查看消息列队里是否有消息，有则读取出来
        //并阻塞50毫秒
        Message msg;
       // if(messgaeManager.receiveMessage(msg,50))
        {
			disposeWinMessage(msg);
            //Python代码使用被动式获取消息，所以不要信号触发
            Q_EMIT receiveMessageFinishedSignal(msg);
        }
		//检测chipic3d程序是否还在运行
		detectionChipic3dIsRun();
    }
}
/**
 * @brief LonelinessMode::addTask 添加任务
 * @param msg 任务
 * @return 如果开启单机模式则返回true，否则返回false
 */
bool LonelinessMode::addTask(const Message &msg)
{
    if(!getOnLonelinessMod())
        return false;

    taskStackMutex.lock();
    taskStack.append(msg);
    taskStackMutex.unlock();

    return true;
}
/**
 * @brief LonelinessMode::getTask 从栈内获取任务，并删除任务副本
 * @return 任务,如果栈为空则返回一个默认的任务。
 */
Message LonelinessMode::getTask()
{
    Message msg;
    taskStackMutex.lock();
    if(taskStack.size() > 0)
    {
        msg = taskStack.at(0);
        taskStack.removeAt(0);
    }
    taskStackMutex.unlock();

    return  msg;
}
/**
 * @brief LonelinessMode::getTaskCount 获取栈内任务数量
 * @return 任务数量
 */
int LonelinessMode::getTaskCount()
{
    taskStackMutex.lock();
    int count = taskStack.size();
    taskStackMutex.unlock();

    return count;
}
/**
 * @brief LonelinessMode::lonelinessModeOn 启动单机模式
 */
void LonelinessMode::lonelinessModeOn()
{
    flagMutex.lock();
    modeFlag = true;
    flagMutex.unlock();
    if(!this->isRunning())
        this->start();
}
/**
 * @brief LonelinessMode::lonelinessModeOff 关闭单机模式
 */
void LonelinessMode::lonelinessModeOff()
{
	//取消任务循环
    flagMutex.lock();
    modeFlag = false;
    flagMutex.unlock();
}

/**
 * @brief LonelinessMode::getLonelinessModeFlag 获取模式开启标志
 * @return 标志
 */
bool LonelinessMode::getLonelinessModeFlag(){
    flagMutex.lock();
    bool b = modeFlag;
    flagMutex.unlock();
    return b;
}
/**
 * @brief LonelinessMode::getPyMessage  获取发给Python模块的消息
 * @param msg 消息结构
 * @return 是否获取成功，是否成功取决于是否使用单机模式，而非列队中是否有消息
 */
bool LonelinessMode::getPyMessage(PyMessage &msg)
{
    //如果为开启单机模式，则返回false
    if(!getOnLonelinessMod())
        return false;

    messageStackMutex.lock();

    if(messageStack.size() > 0)
    {
        msg = messageStack.at(0);
        messageStack.removeAt(0);
    }else {
        msg.type = PyMessageType::NO_MSG;
    }
    messageStackMutex.unlock();

    return true;
}
/**
 * @brief LonelinessMode::addPyMessage 将消息放入队列
 * @param msg 消息
 */
void LonelinessMode::addPyMessage(const PyMessage &msg)
{
        messageStackMutex.lock();
        messageStack.append(msg);
        messageStackMutex.unlock();
}
/**
 * @brief LonelinessMode::startChipic3d 启动内核程序
 * @param path m3d文件路径
 * @param count 并行运算线程数
 */
void LonelinessMode::startChipic3d(const std::string path, const int &count)
{
    //判断是否已经运行
    //如果已经运行，则结束运行。
    if(getLonelinessModeFlag())
    {
        lonelinessModeOff();
        this->quit();
        this->wait();
    }

    RunChipic3d chipic3d(RunChipic3d::X32);
    //记录下线程数量
    chipic3dTreadCount = count;
	//将stdstring转换为qstring
	QString qPath = QString::fromLocal8Bit(path.data());
    //获取m3d文件名称，用于后续生成临时文件的名称
    QDir dir(qPath);
    this->m3dFileName = dir.dirName();
	this->m3dFilePath = qPath.remove(m3dFileName);
    //判断线程数量，决定是否启用并行运算
	//这里qpath的原值已被remove改变 所以不能直接使用qpath
    if(count > 1)
    {
        chipic3d.runWithNotLonelinessMode(this->m3dFilePath + this->m3dFileName,count);
    }else if (count == 1) {
		chipic3d.runWithLonelinessMode(this->m3dFilePath + this->m3dFileName);
    }

    //启动消息侦听线程
    lonelinessModeOn();
}
/**
 * @brief LonelinessMode::killChipic3d 结束chipic3d的运行
 */
void LonelinessMode::killChipic3d()
{
    //向chipic3d发送一个停止的消息
    Message msg;
    msg.Msg = WM_USER + 0;
    msg.wParam = 0;
    msg.lParam = 0;
    addTask(msg);
}

/**
 * @brief LonelinessMode::disposeWinMessage 处理chipic3d发送过来的消息
 * @param msg 消息
 */
void LonelinessMode::disposeWinMessage(Message &msg)
{
#ifdef MY_DEBUG
	std::cerr << "receive message,msg: WM_USER + " << msg.Msg - WM_USER
		<< ",wParaw:" << msg.wParam
		<< ",lParaw:" << msg.lParam << std::endl;
#endif
    //处理gui文件消息
    if(disposeGuiFileWinMessage(msg))
        return;
    //处理hdf5文件消息
    if(disposeHdf5FileWinMessage(msg))
        return;
	//处理器件结构文件消息
	if (disposeStructHdf5File(msg))
		return;
    //处理现实计算进度消息
    if(disposeRefreshMsg(msg))
        return;
    //处理chipic暂停消息
    if(disposeChipicIsPause(msg))
        return;
    //处理定时器消息
    if(disposeChipicTimerState(msg))
        return;
    //处理其他windows消息
    if(msg.Msg > WM_USER)
    {
        PyMessage pyMsg;
        pyMsg.type = PyMessageType::WIN_MSG;
        pyMsg.id = msg.Msg - WM_USER;
        pyMsg.wParam = msg.wParam;
        pyMsg.lParam = msg.lParam;

        addPyMessage(pyMsg);
    }
}
/**
 * @brief LonelinessMode::disposeGuiFileWinMessage 将id为208的消息，转为为Python文件名类型消息，放入队列
 * @param msg 消息
 * @return 如果消息不为gui文件消息则返回false
 */
bool LonelinessMode::disposeGuiFileWinMessage(Message &msg)
{
    if(msg.Msg - WM_USER == 208)
    {
        if(msg.wParam == 3
                ||msg.wParam == 4
                ||msg.wParam == 8)
        {
            PyMessage pyMsg;
			pyMsg.type = PyMessageType::GUI_FILE_NAME;
			pyMsg.fileName = makeFilePath(".gui");
			pyMsg.wParam = msg.wParam;
			pyMsg.lParam = msg.lParam;

			//将消息放入消息队列
			addPyMessage(pyMsg);

			return  true;
        }
    }

    return false;
}
/**
 * @brief LonelinessMode::disposeHdf5FileWinMessage  将消息为209的消息转换为Python文件名消息，并放入队列
 * @param msg   win消息
 * @return  消息id不为209则返回false
 */
bool LonelinessMode::disposeHdf5FileWinMessage(Message &msg)
{
    if(msg.Msg - WM_USER == 209)
    {
        if(msg.wParam != -1000 && msg.lParam != -1000)
        {
            PyMessage pyMsg;
            pyMsg.type = PyMessageType::FILE_NANE;
            pyMsg.fileName = makeFilePath("_Temp.h5");
			pyMsg.wParam = msg.wParam;
			pyMsg.lParam = msg.lParam;

            //将消息放入消息队列
            addPyMessage(pyMsg);

            return  true;
        }
    }

    return false;
}
/**
* @brief LonelinessMode::makeFilePath 按照路径的格式，生成相应的文件路径
* @param fileName 文件名
* @return 生成的文件路径
*/
std::string LonelinessMode::makeFilePath(const std::string &fileName)
{
	//将winmsg消息转换为文件消息
	//使Python代码直接打开文件
	std::string filePath;
	//去掉文件名的后缀
	QString name = this->m3dFileName.left(this->m3dFileName.size() - 4);
	//将qstring转换为stdstring
	//直接tostdstring中文转换会有问题
	std::string m3dFileName = std::string(name.toLocal8Bit());
	std::string path = std::string(this->m3dFilePath.toLocal8Bit());
	if (chipic3dTreadCount > 1)
	{
		filePath = path + "\\1\\" + m3dFileName + fileName;
	}
	else if (chipic3dTreadCount == 1) {
		filePath = path + m3dFileName + fileName;
	}

	return filePath;
}
/**
* @brief LonelinessMode::disposeStructHdf5File 处理器件结构文件消息
* @param msg 消息
* @return 判断消息是否为对应的消息，不是则返回false
*/
bool LonelinessMode::disposeStructHdf5File(Message &msg){
	
	if (msg.Msg - WM_USER == 208)
	{
		if (msg.wParam == 100 && msg.lParam == 0)
		{
            PyMessage pyMsg;
			pyMsg.type = PyMessageType::STRUCT_FILE_NAME;
			pyMsg.fileName = makeFilePath("_Temp.h5");
			pyMsg.id = msg.Msg;
			pyMsg.wParam = msg.wParam;
			pyMsg.lParam = msg.lParam;
			addPyMessage(pyMsg);
			return true;
		}
	}
	
    return false;
}
/**
 * @brief LonelinessMode::detectionChipic3dIsRun 检测chipic3d是否还在运行，如果没有在运行则发消息给Python，更改运行状态
 */
void LonelinessMode::detectionChipic3dIsRun()
{
    if(!messgaeManager.testSendMessage())
    {
		//关闭消息监听
		lonelinessModeOff();
		//发送Python消息，刷新按钮状态
        PyMessage pyMsg;
        pyMsg.type =PyMessageType::CHIPIC_IS_OVER;
        addPyMessage(pyMsg);
        Message msg;
        Q_EMIT receiveMessageFinishedSignal(msg);
    }
}
/**
 * @brief LonelinessMode::disposeRefreshMsg 处理刷新界面显示消息
 * @param msg   消息
 * @return  如果是对应的消息 则返回true
 */
bool LonelinessMode::disposeRefreshMsg(Message &msg)
{
    if(msg.Msg -WM_USER == 204)
    {
        //处理迭代时间
        if(disposeChipicCount(msg))
            return true;
        //处理消耗时间
        if(disposeChipicUsedTime(msg))
            return true;
    }
    return false;
}
/**
 * @brief LonelinessMode::disposeChipicCount 处理迭代次数消息
 * @param msg   消息
 * @return  如果是对应消息则返回true
 */
bool LonelinessMode::disposeChipicCount(Message &msg)
{
    //由于信息分两次传达，所以定义静态变量储存上一次消息的信息
    static WPARAM count = 0;
    if(msg.wParam == 1)
    {
        count = msg.lParam;
        return true;
    }
    if(msg.wParam == 2)
    {
        PyMessage pyMsg;
        pyMsg.wParam = count;
        pyMsg.lParam = msg.lParam;
        pyMsg.type = PyMessageType::CHIPIC_COUNT;
        addPyMessage(pyMsg);
        return true;
    }

    return false;

}
/**
 * @brief LonelinessMode::disposeChipicUsedTime 处理chipic计算消耗时间消息
 * @param msg  消息
 * @return 如果为对应消息则返回true
 */
bool LonelinessMode::disposeChipicUsedTime(Message &msg)
{
    //由于信息分两次传达，所以定义静态变量储存信息
    static std::string usedTiem;
    switch (msg.wParam) {
        case 3:
        case 4:
            usedTiem += QString::number(msg.lParam).toStdString() + ":";
            return true;
        case 5:
            usedTiem += QString::number(msg.lParam).toStdString() + "/";
            return true;
        case 6:
        case 7:
            usedTiem += QString::number(msg.lParam).toStdString() + ":";
            return true;
        case 8:
            usedTiem += QString::number(msg.lParam).toStdString();
            //由于消息传递给Python的时候只有fileName为字符型，先暂时用这个变量
            PyMessage pyMsg;
            pyMsg.fileName = usedTiem;
            pyMsg.type = PyMessageType::CHIPIC_USED_TIME;
            addPyMessage(pyMsg);
			//清空静态变量
			usedTiem = "";
            return true;
    }

    return false;
}
/**
 * @brief LonelinessMode::disposeChipicIsPause 处理chipic暂停状态消息
 * @param msg 消息
 * @return  如果是对应的消息则返回true
 */
bool LonelinessMode::disposeChipicIsPause(Message &msg)
{
    //如果不是对应的消息，则返回false
    if(msg.Msg - WM_USER !=201
            &&msg.Msg - WM_USER != 202
            &&msg.Msg - WM_USER != 205)
        return false;

    if(msg.Msg - WM_USER == 201)
        chipicIsPause = false;
    if(msg.Msg - WM_USER == 202)
        chipicIsPause = true;
    //同样的功能的消息定义了两次，所以需要处理两次，不知何意
    if(msg.Msg - WM_USER == 205)
    {
        if(msg.wParam == 0)
            chipicIsPause = true;
        else {
            chipicIsPause = false;
        }
    }

    PyMessage pyMsg;
    pyMsg.type = PyMessageType::CHIPIC_PAUSE_STATE;

    addPyMessage(pyMsg);
    return  true;

}
/**
 * @brief LonelinessMode::disposeChipicTimerState 处理定时器状态消息
 * @param msg 消息
 * @return 如果为对应消息则返回true
 */
bool LonelinessMode::disposeChipicTimerState(Message &msg)
{
    if(msg.Msg - WM_USER == 203)
    {
     if(msg.wParam == 1)
         chipicTimerState = true;
     else {
         chipicTimerState = false;
     }
        PyMessage pyMsg;
        pyMsg.type = PyMessageType::CHIPIC_TIMER_STATE;

        addPyMessage(pyMsg);
        return true;
    }
    return false;
}

/**
 * @brief LonelinessMode::receiveMessageFinished 消息接收完成槽函数
 * @param msg 消息
 */
void LonelinessMode::receiveMessageFinished(Message msg)
{
	//Base::Interpreter().runString("FreeCADGui.runCommand('LonelinessCmd')");
	
}
/** 
* @brief LonelinessMode::timerEvent 定时器触发事件
*/
void LonelinessMode::timerEvent(QTimerEvent *event)
{
	//如果chipic已运行
	if (this->getLonelinessModeFlag())
	{
		if (event->timerId() == timerId)
		{
#ifdef MY_DEBUG
			std::cerr << "timer event-> send message!" << std::endl;
#endif
			{
				Message msg;
				msg.Msg = WM_USER + 105;
				msg.wParam = 0;
				msg.lParam = 0;
				addTask(msg);
			}
			{
				Message msg;
				msg.Msg = WM_USER + 104;
				msg.wParam = 1;
				msg.lParam = 0;
				addTask(msg);
			}
			{
				Message msg;
				msg.Msg = WM_USER + 106;
				msg.wParam = 0;
				msg.lParam = 0;
				addTask(msg);
			}
		}
	}
}
#ifndef MY_QTCMY_DEBUG
#include "moc_LonelinessMode.cpp"
#endif
