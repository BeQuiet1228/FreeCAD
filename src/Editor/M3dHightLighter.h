#ifndef MYHIGHTLIGHTER_H
#define MYHIGHTLIGHTER_H
#include <QSyntaxHighlighter>
#include <qstring.h>
#include <qobject.h>
#include <qlist.h>

class M3dHightLighter:public QSyntaxHighlighter
{
public:
    struct HighlightingRule
    {
        QRegExp pattern;
        QTextCharFormat format;
    };
    M3dHightLighter(QTextDocument *parent);
    QList<QString> caseWords;
    QList<QString> functions;
    QList<HighlightingRule> rule;
protected:
    void highlightBlock(const QString &text); //高亮规则设置
private:
    void highlightCaseWord(const QString &word,const QString &text);    //高亮关键字
    void highlightCaseWord(const QString &word,const QTextCharFormat &format,const QString &text);
    void highlightCaseWord(const QRegExp &rex,const QTextCharFormat &format,const QString &text);
    void highlightFunctio(const QString &function,const QTextCharFormat &format,const QString &text);
    void highlightFunctio(const QString &function,const QString &text); //高亮函数
	//高亮z注释
	void higlightAnnotation(const QString& text);
};

#endif // M3dHightLighter_H
