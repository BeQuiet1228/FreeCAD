#ifndef RUNCHIPIC3D_H
#define RUNCHIPIC3D_H
#include <qprocess.h>
#include <qstring.h>
#include <qobject.h>
/**
 * @brief The RunChipic3d class chipic3d启动器
 */
class RunChipic3d
{
public:
    enum RunMode{
      X32,
      X64
    };
    RunChipic3d() = delete ;
    RunChipic3d(const RunMode &mode = X32);
	~RunChipic3d();
    //单机模式启动
    void runWithLonelinessMode(const QString &m3dPath);
    //并行模式启动
    void runWithNotLonelinessMode(const QString &m3dpath,const int &count);
	//启动chipic
	void run(const std::string &m3dpath, const int &count = 1);
private:
    //32位chipic路径
    const QString chipicX32Path = q2s("w32dll/Chipic3d.exe");
    //64位chipic路径
    const QString chipicX64Path = q2s("");
    //32位mpi的路径
    const QString mpiX32Path = q2s("MPICH2/bin/");
    //64位mpi路径
    const QString mpiX64Path = q2s("");
	//chipic路径 mpi路径
    QString chipicPath,mpiPath;

private:
    //生成配置文件
    void makeCfgFile(const QString &path,const QString &fileName,const int &count);
    //初始化mpi
    void initMpi();
    //std::string 转换为qstring
    QString q2s(const char *s);

private:
    //mpi启动窗口
    QProcess *mpiProcess = nullptr;
	//chipic cmd对象
	QProcess *chipicProcess = nullptr;

};

#endif // RUNCHIPIC3D_H
