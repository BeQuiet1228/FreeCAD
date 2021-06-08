#ifndef MATCHWORDSTHREAD_H
#define MATCHWORDSTHREAD_H
#include <QThread>
#include <qobject.h>
#include <QMutex>
#include <QRegExp>
#include <QTextCursor>
class MatchWordsThread:public QThread
{
    Q_OBJECT
public:
    MatchWordsThread();
    ~MatchWordsThread();
    QList<QString> caseWords;
    void setMatchWord(const QString &blockText);
private:
        QMutex locke;
        QRegExp regularExpresion;
        QString blockText;
        QTextCursor cursor;
protected:
    void run();
signals:
    void matchCaseWordFinished(QList<QString> vipCaseWords,QList<QString> lowCaseWords,int caseWordSize);
    void hideListWidget();
};

#endif // MATCHWORDSTHREA_H
