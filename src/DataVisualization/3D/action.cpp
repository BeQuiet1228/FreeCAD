#include "action.h"


DV3D::ActionSwitch::ActionSwitch()
	:state(OFF)
{
	QIcon on(":/action/on.svg");
	QIcon off(":/action/off.svg");
	setOnIcon(on);
	setOffIcon(off);
}

DV3D::ActionSwitch::ActionSwitch(const QIcon& onIcon, const QString& onText, const QIcon& offIcon, const QString& offText)
	: state(OFF)
{
	setOnIcon(onIcon);
	setOffIcon(offIcon);
	setOffText(offText);
	setOnText(onText);

	on();
}

DV3D::ActionSwitch::ActionSwitch(const QIcon& onIcon, const QIcon& offIcon)
	:state(OFF)
{
	setOnIcon(onICon);
	setOnIcon(offIcon);
	on();
}

void DV3D::Action::update(QToolButton* button)
{
	button->setText(text);
	button->setIcon(getIcon());
}

void DV3D::Action::setText(const QString& t)
{
	this->text = text;
}

QString DV3D::Action::getText()
{
	return text;
}

void DV3D::Action::setIcon(const QIcon& icon)
{
	this->icon = icon;
}

QIcon DV3D::Action::getIcon()
{
	return icon;
}



void DV3D::ActionSwitch::setOnIcon(const QIcon& icon)
{
	this->onICon = icon;
}

QIcon DV3D::ActionSwitch::getOnIcon()
{
	return onICon;
}

void DV3D::ActionSwitch::setOffIcon(const QIcon& icon)
{
	this->offIcon = icon;
}

QIcon DV3D::ActionSwitch::getOffIcon()
{
	return offIcon;
}

void DV3D::ActionSwitch::setOnText(const QString& text)
{
	this->onText = text;
}

QString DV3D::ActionSwitch::getOnText()
{
	return onText;
}

void DV3D::ActionSwitch::setOffText(const QString& text)
{
	this->offText = text;
}

QString DV3D::ActionSwitch::getOffText()
{
	return offText;
}

void DV3D::ActionSwitch::setState(const State& s)
{
	this->state = s;
}

DV3D::ActionSwitch::State DV3D::ActionSwitch::getState()
{
	return state;
}

void DV3D::ActionSwitch::on()
{
	setIcon(getOnIcon());
	setText(getOnText());
	setState(ON);
}

void DV3D::ActionSwitch::off()
{
	setIcon(getOffIcon());
	setText(getOffText());
	setState(OFF);
}
