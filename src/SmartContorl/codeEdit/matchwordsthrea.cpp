#include "matchwordsthrea.h"
#include <QMetaType>
#include <QFile>
#include <QTextStream>

MatchWordsThread::MatchWordsThread()
{
    {
        QFile file("./codeEditConfig/caseWord.txt");
        if (file.open(QIODevice::ReadOnly | QIODevice::WriteOnly))
        {
            QTextStream stream(&file);
            while (!stream.atEnd()) {
                QString line = stream.readLine();
                caseWords.append(line);
             }
        }
    }
    {
        QFile file("./codeEditConfig/function.txt");
        if (file.open(QIODevice::ReadOnly | QIODevice::WriteOnly))
        {
            QTextStream stream(&file);
            while (!stream.atEnd()) {
                QString line = stream.readLine();
                caseWords.append(line);
             }
        }
    }




    qRegisterMetaType<QList<QString>>("QList<QString>");  //注册qlist<qstring> 类 使之可以用于信号与槽的参数传递
}
MatchWordsThread::~MatchWordsThread()
{

}
/*
*设置要匹配的关键字，并开始匹配
* @word 关键字
*/
void MatchWordsThread::setMatchWord(const QString &blockText)
{
    locke.lock();     //锁定互斥锁
    this->blockText = blockText;
    locke.unlock();
    if(isRunning())
        quit();
    start();        //启动线程
}
/*
*新的线程方法
* 在新线程中匹配关键字
*/
void MatchWordsThread::run()
{
    QString word;
    locke.lock();
    {              //获取分割位置
        QRegExp rex("\\s|:|;|#");      //寻找最后一个空白符
        int pos = 0,lastSpaseIndex = 0;
        while ((pos = rex.indexIn(blockText, pos)) != -1)
        {
            lastSpaseIndex = pos + rex.matchedLength();
            pos = pos + rex.matchedLength();
        }
        if(lastSpaseIndex!=-1)
            word = blockText.right(blockText.size() - lastSpaseIndex);
        else {              //如果没有找到分割符，则传入整个文本块
            word = blockText;
        }
    }
    locke.unlock();

    if(word.size() < 2)          //如果只有一个字符，则不触发提示
    {
        emit hideListWidget();
        return;
    }
    regularExpresion.setPattern(word +".+");    //添加正则表达式
    regularExpresion.setCaseSensitivity(Qt::CaseInsensitive);      //匹配时忽略大小写

    QList<QString> vipCaseWords;   //完全匹配的关键字
    QList<QString> lowCaseWords;    //模糊匹配的关键字
    for(int i = 0; i < caseWords.size();i++)    //历遍关键字字典，并匹配
    {
        locke.lock();
        int pos = regularExpresion.indexIn(caseWords.at(i),0);
        locke.unlock();
        if(pos!=-1)
        {
            if(pos == 0)
                vipCaseWords.append(caseWords.at(i));
            else {
                lowCaseWords.append(caseWords.at(i));
            }
        }

    }
     emit matchCaseWordFinished(vipCaseWords,lowCaseWords,word.size());
}

#include "codeEdit/moc_matchwordsthrea.cpp"