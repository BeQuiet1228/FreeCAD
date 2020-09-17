#pragma  once
#include <qwidget.h>
#include <QTimer>
#include <memory>
/*
	chipic有时候会有过快的信息更新，为了节省数据刷新时的性能。
	用定时器去刷新界面信息的显示。
*/
class Chipic;
class ContorlBar:public QWidget
{
	Q_OBJECT
public:
	ContorlBar(QWidget *parent = 0);
	virtual ~ContorlBar();
private:
	//刷新所有界面的定时器
	static std::shared_ptr<QTimer> timer;
	//定时器刷新频率 单位时ms
	const int timerTime = 500;
protected:
	//chipic信息
	std::shared_ptr<Chipic> chipic;
public:
	//刷新界面信息
	virtual void updateUI() = 0;
	//设置chipic
	void setChipicData(std::shared_ptr<Chipic> chipic);

public Q_SLOTS:
	void uiTimerOut();

};
