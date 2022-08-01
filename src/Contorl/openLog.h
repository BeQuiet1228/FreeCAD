#include <mutex>
#include <memory>
#include <QString>
class QProcess;
class OpenLog
{
public:
	~OpenLog();
	static std::shared_ptr<OpenLog> GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new OpenLog);
		});

		return _instance;
	}
private:
	OpenLog();
	OpenLog operator=(const OpenLog&) = delete;
	OpenLog(const OpenLog&) = delete;
	static std::shared_ptr<OpenLog> _instance;

	//命令窗口对象
	QProcess *process;
public:
	//设置当前运行的m3d路径
	void setCurrentChipicM3dPath(const std::string& path, const int& threadCount = 1);
	//打开log文件
	void openLog();
	//获取log的内容
	QString  getLogContent();
private:
	QString m3dPath;

};