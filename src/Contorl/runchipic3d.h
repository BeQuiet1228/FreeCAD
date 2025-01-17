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
	enum CoreType{
		M2D = 0,
		M3D,
        FIX,
        TYPE_SIZE
	};
    RunChipic3d();
	~RunChipic3d();
    //单机模式启动
    void runWithLonelinessMode(const QString &m3dPath,const CoreType &coreType = M3D);
    //并行模式启动
    void runWithNotLonelinessMode(const QString &m3dpath,const int &count,const CoreType& coreType = M3D);
	//启动chipic
	void run(const std::string &m3dpath, const int &count = 1);
    void runfix(const std::string& m3dpath);
private:
    QString chipicPath[TYPE_SIZE];
    //m3d运算程序类型
    const QString chipicM3dPath = q2s("core/m3d/Chipic3d.exe");
    const QString chipicFixPath = q2s("core/m3d/Chipic3dfix.exe");
    //mpi的路径
    const QString mpiPath = q2s("MPICH2/bin/");
	//m2d的chipic路径
	const QString chipicM2dPath = q2s("core/m2d/Chipic3d.exe");


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
