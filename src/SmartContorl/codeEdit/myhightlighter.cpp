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
	higlightAnnotation(text);
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


/**
* @brief myHightLighter::higlightAnnotation 对z开头的文本进行注释
* @param const QString & text
* @return void
*/
void myHightLighter::higlightAnnotation(const QString& text)
{
	/*
		--这个注释以z开始，z的两边必须时单词的边界，才可以，然后以分号结尾
		--可以跨行，如果在注释所在的一行没有找到分号，那么注释的效果将延续到下一行
	*/

	//生成注释的正则 --设置为静态时为了节省每次初始化正则表达式的时间（这个时间貌似挺长的）
	static QRegExp rex("\\b[zZ]\\b");
	static QRegExp rexf(";");
	//设置高亮色
	QTextCharFormat myClassFormat;
	myClassFormat.setFontWeight(QFont::Bold);
	myClassFormat.setForeground(Qt::darkGreen);

	int pos = 0;
	//在这里判断上一行的状态来确定是否直接在该行的开始进行注释高亮
	if (this->previousBlockState() != 1)
		pos = rex.indexIn(text, pos);
	while (pos != -1) {
		int posf = 0;
		int len = 0;
		//查找分号
		if ((posf = rexf.indexIn(text, pos)) != -1)
		{
			len = posf - pos + 1;
			//设置当前行是否有找到注释的结尾
			setCurrentBlockState(0);
		}else{
			len = text.length() - pos;
			//设置当前行是否有找到注释的结尾
			setCurrentBlockState(1);
		}

		setFormat(pos, len, myClassFormat);
		pos += len;
		pos = rex.indexIn(text, pos);
	}

}
