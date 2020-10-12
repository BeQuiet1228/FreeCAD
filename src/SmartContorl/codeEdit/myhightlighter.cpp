#include "myhightlighter.h"
#include <QRegExp>
#include <QFile>
#include <QTextStream>
myHightLighter::myHightLighter(QTextDocument *parent)
    :QSyntaxHighlighter(parent)
{
    {       //载入关键字
        QFile file("./codeEditConfig/caseWord.txt");
        if (file.open(QIODevice::ReadOnly | QIODevice::WriteOnly))
        {
            QTextStream stream(&file);
            while (!stream.atEnd()) {
              QString line = stream.readLine();
             // caseWords.append(line);
              QRegExp regularExpression("\\b" + line + "\\b");    //创建正则表达式
              regularExpression.setCaseSensitivity(Qt::CaseInsensitive);      //匹配时忽略大小写

              QTextCharFormat myClassFormat;
              myClassFormat.setFontWeight(QFont::Bold);
              myClassFormat.setForeground(Qt::blue);

              HighlightingRule r;
              r.pattern = regularExpression;
              r.format = myClassFormat;
              rule.append(r);
            }
         }
    }
    {       //载入函数
        QFile file("./codeEditConfig/functioHielighter.txt");
        if (file.open(QIODevice::ReadOnly | QIODevice::WriteOnly))
        {
            QTextStream stream(&file);
            while (!stream.atEnd()) {
              QString line = stream.readLine();
              //functions.append(line);
              QRegExp regularExpression(line);    //创建正则表达式
              regularExpression.setCaseSensitivity(Qt::CaseInsensitive);      //匹配时忽略大小写

              QTextCharFormat myClassFormat;
              myClassFormat.setFontWeight(QFont::Bold);
              myClassFormat.setForeground(Qt::darkRed);

              HighlightingRule r;
              r.pattern = regularExpression;
              r.format = myClassFormat;
              rule.append(r);
            }
         }
    }
    //载入注释
    {
        QTextCharFormat myClassFormat;
        myClassFormat.setFontWeight(QFont::Bold);
        myClassFormat.setForeground(Qt::darkGreen);
        QRegExp rex("!.*");    //创建正则表达式

        HighlightingRule r;
        r.pattern = rex;
        r.format = myClassFormat;
        rule.append(r);
    }
}

void myHightLighter::highlightBlock(const QString &text)
{
//    for(int i = 0;i < caseWords.size();i++) //高亮关键字
//    {
//        highlightCaseWord(caseWords.at(i),text);
//    }

//    for(int i = 0;i < functions.size();i++) //高亮函数
//    {
//        highlightFunctio(functions.at(i),text);
//    }

//    QTextCharFormat myClassFormat;
//    myClassFormat.setFontWeight(QFont::Bold);
//    myClassFormat.setForeground(Qt::darkGreen);
//    QRegExp rex("!.*");    //创建正则表达式
//    int pos = 0;
//    if((pos = rex.indexIn(text, pos)) != -1) {
//        setFormat(pos,rex.matchedLength(),myClassFormat);
//    }
    for(int i= 0;i < rule.size();i++)
    {
        highlightCaseWord(rule.at(i).pattern,rule.at(i).format,text);
    }
}
/*
*高亮一个关键字
* @word 关键字
* @format 高亮规则
* &text 文本块
*/
void myHightLighter::highlightCaseWord(const QString &word,const QTextCharFormat &format,const QString &text)
{

    QRegExp regularExpression("\\b" + word + "\\b");    //创建正则表达式
    regularExpression.setCaseSensitivity(Qt::CaseInsensitive);      //匹配时忽略大小写
    int pos = 0;
    while ((pos = regularExpression.indexIn(text, pos)) != -1) {
        setFormat(pos,word.size(),format);
        pos += regularExpression.matchedLength();
    }
}
/*
*高亮一个关键字
* @word 关键字
* @format 高亮规则
* &text 文本块
*/
void myHightLighter::highlightCaseWord(const QRegExp &rex,const QTextCharFormat &format,const QString &text)
{
    int pos = 0;
    while ((pos = rex.indexIn(text, pos)) != -1) {
        setFormat(pos,rex.matchedLength(),format);
        pos += rex.matchedLength();
    }
}
/*
*高亮一个关键字
* @word 关键字
* &text 文本块
*/
void myHightLighter::highlightCaseWord(const QString &word, const QString &text)
{
    QTextCharFormat myClassFormat;
    myClassFormat.setFontWeight(QFont::Bold);
    myClassFormat.setForeground(Qt::blue);
    highlightCaseWord(word,myClassFormat,text);
}
/*
*高亮一个函数
* @function 函数
* @format 高亮规则
* &text 文本块
*/
void myHightLighter::highlightFunctio(const QString &function, const QTextCharFormat &format, const QString &text)
{
    QRegExp regularExpression(function);    //创建正则表达式
    regularExpression.setCaseSensitivity(Qt::CaseInsensitive);      //匹配时忽略大小写
    int pos = 0;
    while ((pos = regularExpression.indexIn(text, pos)) != -1) {
        setFormat(pos,function.size() - 6,format);
        pos += regularExpression.matchedLength();
    }

}
/*
*高亮一个函数
* @function 函数
* &text 文本块
*/
void myHightLighter::highlightFunctio(const QString &function, const QString &text)
{
    QTextCharFormat myClassFormat;
    myClassFormat.setFontWeight(QFont::Bold);
    myClassFormat.setForeground(Qt::darkRed);
    highlightFunctio(function,myClassFormat,text);
}
