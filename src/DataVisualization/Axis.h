#pragma once

#ifndef AXIS_H
#define AXIS_H

#include <QWidget>
#include<QVector>
typedef struct
{
    double min;
    double max;
}valrange;
enum Axisstyle
{
    Axisleft,
    AxisRight,
    AxisTop,
    AxisBottom
};
class Axis : public QWidget
{
    Q_OBJECT
public:
    explicit Axis(QWidget *parent = nullptr);
    ~Axis();
private:
public:
    //添加功能函数
    void setAxisText(QString,int fontsize);
    void setAxisRange(double min,double max);
    //设置大刻度个数
    void SetAxisNumber(int);
    void _update();
    void setAxixStyle(Axisstyle);
public:
    void paintEvent(QPaintEvent* event);
private:
    bool isstart;
    unsigned int Axisnumber;//大刻度个数
    QString Axisunit;//单位
    int Axisunitfontsize;//单位字体大小
    valrange axisvalrange;//刻度数值区间
    QRectF AxisRect;
    Axisstyle mAxisstyle;
};

#endif // AXIS_H
