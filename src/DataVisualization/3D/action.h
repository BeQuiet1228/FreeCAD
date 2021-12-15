#pragma  once
#include <QIcon>
#include <QString>
#include <memory>
#include <QToolButton>
namespace DV3D {
	/*
		按钮数据对象
	*/
	class Action {
	public:
		Action() = default;
		virtual ~Action() = default;
	public:
		//被触发
		virtual void active() = 0;
		//将信息更新到按钮
		virtual void update(QToolButton* button);

		//get set
		void setText(const QString& t);
		QString getText();
		void setIcon(const QIcon& icon);
		QIcon getIcon();
	private:
		//文本
		QString text;
		//图标
		QIcon icon;
	};
	/*
		开关按钮对象
	*/
	class ActionSwitch :public Action{
	public:
		enum State{
			OFF = 0,
			ON
			
		};
	public:
		ActionSwitch();
		ActionSwitch(const QIcon& onIcon, const QIcon& offIcon);
		ActionSwitch(const QIcon& onIcon, const QString& onText, const QIcon& offIcon, const QString& offText);
		~ActionSwitch() = default;

		//get set
		void setOnIcon(const QIcon& icon);
		QIcon getOnIcon();
		void setOffIcon(const QIcon& icon);
		QIcon getOffIcon();
		void setOnText(const QString& text);
		QString getOnText();
		void setOffText(const QString& text);
		QString getOffText();
		void setState(const State& s);
		State getState();

		//打开
		void on();
		//关闭
		void off();
	private:
		//状态对应的图标和文本
		QString onText, offText;
		QIcon onICon, offIcon;
		//状态
		State state;

	};
}