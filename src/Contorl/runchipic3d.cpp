#include "runchipic3d.h"
#include <iostream>
#include <qfile.h>
#include <qdir.h>
#include <qtextstream.h>
#include <qbytearray.h>
#include <qtextcodec.h>
/**
 * @brief RunChipic3d::RunChipic3d 初始化启动器
 * @param mode 运行模式 x32模式 x64模式
 */
RunChipic3d::RunChipic3d()
{
    //初始化变量
    mpiProcess = nullptr;

}

RunChipic3d::~RunChipic3d()
{
	if (chipicProcess != nullptr)
		delete chipicProcess;
	if (mpiProcess != nullptr)
		delete mpiProcess;
}

/**
* @brief RunChipic3d::runWithLonelinessMode 单线程启动chipic
* @param const QString & m3dPath 文件路径
* @param const CoreType & coreType 运算程序类型
* @return void
*/
void RunChipic3d::runWithLonelinessMode(const QString &m3dPath, const CoreType &coreType)
{
	if (chipicProcess != nullptr)
		delete chipicProcess;

	QString tempPath = (coreType == M3D)?chipicM3dPath:chipicM2dPath;
	chipicProcess = new QProcess;
	QString cmd = tempPath + q2s(" \"") + m3dPath + q2s("\"");
#ifdef MY_DEBUG
	std::cerr << "lonelinessMod start cmd:" << cmd.toStdString() << std::endl;
#endif
	chipicProcess->start(cmd);
}

/**
* @brief RunChipic3d::runWithNotLonelinessMode 并行启动chipic
* @param const QString & m3dpath 路径
* @param const int & count 并行数量
* @param const CoreType & coreType 内核类型
* @return void
*/
void RunChipic3d::runWithNotLonelinessMode(const QString &m3dpath, const int &count, const CoreType& coreType)
{
	//获取文件路径跟文件名
	QDir dir(m3dpath);
	QString m3dName = dir.dirName();
	QString path = m3dpath;
	path = path.remove(m3dName);
	//初始化mpi
	initMpi();
	//生成配置文件
	makeCfgFile(path, m3dName, count);

	//执行并行运算
	if (mpiProcess != nullptr)
	{
		delete  mpiProcess;
	}
	mpiProcess = new QProcess;

	//启动mpi
	QString cmd = mpiPath + q2s("smpd.exe -d 0");
	mpiProcess->start(cmd);
#ifdef MY_DEBUG
	std::cerr << "notLonelinessMod init cmd:" << cmd.toStdString() << std::endl;
#endif

	//启动chipic3d
	if (chipicProcess != nullptr)
		delete chipicProcess;
	chipicProcess = new QProcess;
	cmd = mpiPath + q2s("mpiexec.exe -configfile ") + path + q2s("cfg.txt -phrase 0");
	chipicProcess->start(cmd);
#ifdef MY_DEBUG
	std::cerr << "notLonelinessMod start cmd:" << cmd.toStdString() << std::endl;
#endif
}

/**
* @brief RunChipic3d::run 运行chipic程序
* @param const std::string & m3dpath m3d文件路径
* @param const int & count 线程数
* @return void
*/
void RunChipic3d::run(const std::string &m3dpath, const int &count /*= 1*/)
{
	
	QString qstr = QString::fromLocal8Bit(m3dpath.c_str());
	//根据路径后缀来判断需要调用的运算程序类型
	qstr = qstr.right(3).toLower();
	CoreType type = (qstr == "m3d") ? M3D : M2D;

	if (count == 1)
	{
		runWithLonelinessMode(QString::fromStdString(m3dpath),type);
	}
	else if (count > 1)
	{
		runWithNotLonelinessMode(QString::fromStdString(m3dpath), count);
	}
}

/**
 * @brief RunChipic3d::makeCfgFile 在工程目录生成配置文件cfg.txt
 * @param path 工程目录
 * @param fileName 文件名
 * @param count 并行数量
 */
void RunChipic3d::makeCfgFile(const QString &path, const QString &fileName, const int &count)
{
    QFile file(path + fileName);
    QDir dir;
    QStringList directories,filenames;
    //新建并行文件夹并把工程拷贝进去
    for(int i = 1; i <= count; i++)
    {
        QString d = path.arg(q2s("%1"));
        d += QString(q2s("%1")).arg(i);
        directories.append(d);
        dir.mkdir(d);
        d.append(q2s("\\"));
        QFile f(d+fileName);
        if(f.exists())
            f.remove();
        file.copy(d+fileName);
        filenames.append(d+fileName);
    }

    //根据格式生成cfg文件夹
    QFile cfg(path+q2s("cfg.txt"));
    if (!cfg.open(QIODevice::WriteOnly)) {
		std::cerr << "RunChipic3d::makeCfgFile open cfg.txt failed" << std::endl;
        return;
    }
    QTextStream out(&cfg);
	out.setCodec("GB2312");
    for(int i = 1; i <= count; i++)
    {
        out << q2s("-n 1 -wdir") << QLatin1Char(' ')
            << directories[i-1] << QLatin1Char(' ')
            << chipicM3dPath << QLatin1Char(' ')
            << filenames[i-1] << QLatin1Char('\n');
    }
    cfg.close();
}
/**
 * @brief RunChipic3d::initMpi 初始化mpi，需要程序拥有管理员权限才能初始化成功
 */
void RunChipic3d::initMpi()
{
    QProcess process;
    QString cmd = mpiPath + q2s("smpd.exe -install -phrase behappy");
    process.start(cmd);
    process.waitForFinished();
	cmd = mpiPath + q2s("smpd.exe -stop");
	process.start(cmd);
	process.waitForFinished();
#ifdef MY_DEBUG
    std::cerr << "init MPI output: " << QString(process.readAll()).toStdString() << std::endl;
#endif
}
/**
 * @brief RunChipic3d::q2s std::string转换为qstring
 * @param str std::string
 * @return qstring
 */
QString RunChipic3d::q2s(const char *s)
{
    return  QObject::tr(s);
}
