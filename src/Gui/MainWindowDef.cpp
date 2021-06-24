#include "PreCompiled.h"
#include "MainWindowDef.h"
#include "ui_MainWindowDef.h"
#include <QToolBar>
#include <QAction>
#include <QApplication>
#include "MainWindow.h"
/**
* @brief  TitleBar::TitleBar
* @param  QWidget * parent  
* @return   
*/
TitleBar::TitleBar(QWidget* parent /*= 0*/)
	:QWidget(parent)
{
	setObjectName(QString::fromLocal8Bit("titleBar"));
	setCursor(Qt::ArrowCursor);
}

/**
* @brief  TitleBar::mouseMoveEvent  鼠标移动事件
* @param  QMouseEvent * event  
* @return void  
*/
void TitleBar::mouseMoveEvent(QMouseEvent *event)
{
	QWidget::mouseMoveEvent(event);
	if (mouseIsPress)
		Q_EMIT toMove(event->pos() - mouseStartPoint);
}

/**
* @brief  TitleBar::mousePressEvent 鼠标点击事件
* @param  QMouseEvent * event  
* @return void  
*/
void TitleBar::mousePressEvent(QMouseEvent *event)
{
	QWidget::mousePressEvent(event);
	if (event->button() == Qt::LeftButton)
	{
		mouseIsPress = true;
		mouseStartPoint = event->pos();
	}
}

/**
* @brief  TitleBar::mouseReleaseEvent 点击事件释放
* @param  QMouseEvent * event  
* @return void  
*/
void TitleBar::mouseReleaseEvent(QMouseEvent *event)
{
	QWidget::mouseReleaseEvent(event);
	if (event->button() == Qt::LeftButton)
	{
		mouseIsPress = false;
	}
}

/**
* @brief  TitleBar::mouseDoubleClickEvent 鼠标双击
* @param  QMouseEvent * event  
* @return void  
*/
void TitleBar::mouseDoubleClickEvent(QMouseEvent *event)
{
	Q_EMIT doubleClick();
}

/**
* @brief  MainWindowDef::MainWindowDef
* @param  QWidget * parent  
* @return   
*/
MainWindowDef::MainWindowDef(QWidget *parent /*= 0*/)
:QWidget(parent), ui(new Ui::WindowDef())
{
	ui->setupUi(this);
	setCursor(Qt::ArrowCursor);
	this->setWindowFlags(Qt::FramelessWindowHint);
	connect(ui->titleBar, SIGNAL(toMove(QPoint)), this, SLOT(titleBarMove(QPoint)));
	connect(ui->btMini, SIGNAL(clicked(bool)), this, SLOT(toolButtonClicked(bool)));
	connect(ui->btClose, SIGNAL(clicked(bool)), this, SLOT(toolButtonClicked(bool)));
	connect(ui->btMaxShow, SIGNAL(clicked(bool)), this, SLOT(toolButtonClicked(bool)));
	connect(ui->titleBar, SIGNAL(doubleClick()), this, SLOT(titleBarDoubleClicked()));

	boundaryWidth = 4;
	/*
		设置鼠标移动事件追踪。
		如果不设置此选项，那么仅当鼠标按下时才会触发moveEvent
	*/
	this->setMouseTracking(true);


	//初始化顶部的快捷栏
	toolbar = new QToolBar();
	ui->ToolbarWidget->layout()->addWidget(toolbar);

	//测试选项卡接口
	tabWidgetInterface = new Ribbon();
	tabWidgetInterface->setObjectName(QString::fromLocal8Bit("ribbonTabWidget"));
	ui->widgetTab->layout()->addWidget(tabWidgetInterface);
	auto desktopWidget = QApplication::desktop();
	this->resize(1000, 500);
	//获取窗口数量
	unsigned int screenCount = QApplication::desktop()->screenCount();
	screens.clear();
	//装填Rect至每个屏幕的
	for (auto index = 0; index < screenCount;index++)
	{
		QRect rect = QApplication::desktop()->availableGeometry(index);
		screens.push_back(rect);
	}
	setMinimumSize(0,0);
	tabWidgetInterface->setParentWidget(this);
	LastSize = this->size();
}


MainWindowDef::~MainWindowDef()
{
	delete ui;
}

void MainWindowDef::mouseMoveEvent(QMouseEvent *event)
{
	QWidget::mouseMoveEvent(event);
	changeCursor(event->pos());
	changeSize(event->pos());

	
	/*QSize size= tabWidgetInterface->size();
	qDebug() <<"size--"<< size;*/
}

void MainWindowDef::mousePressEvent(QMouseEvent *event)
{
	QWidget::mousePressEvent(event);
	if (event->button() == Qt::LeftButton)
	{
		leftButtonIsPress = true;
		leftButtonPressPos = event->pos();
	}
}

void MainWindowDef::mouseReleaseEvent(QMouseEvent *event)
{
	QWidget::mouseReleaseEvent(event);

	if (event->button() == Qt::LeftButton)
	{
		leftButtonIsPress = false;
	}
	setCursor(Qt::ArrowCursor);
	cursorState = NONE;
}

void MainWindowDef::resizeEvent(QResizeEvent *event)
{
	QWidget::resizeEvent(event);
	if (isMax)
		isMax = false;
	test();
}

void MainWindowDef::moveEvent(QMoveEvent *event)
{
	QWidget::moveEvent(event);
	isMax = false;
}

void MainWindowDef::titleBarMove(QPoint pos)
{
	QPoint posing = this->pos() + pos;
	for (auto index = 0; index < screens.size();index++)
	{
		if (posing.y()-screens[index].topLeft().y()<2)
		{
			showMax();
			return ;
		}
	}
	if (isMax)
	{
		resize(this->width()*0.7, this->height()*0.7);
		isMax = false;
	}
	this->move(this->pos() + pos);
}

void MainWindowDef::toolButtonClicked(bool b)
{
	if (sender() == ui->btMini){
		//最小化窗口
		this->showMinimized();
	}else if (sender() == ui->btClose){
		/*
			这里不能直接关闭本窗口，关闭本窗口会释放掉其子窗口。
			而再释放mainwndow之前应该触发其关闭事件，里面有一些很重要的调用。
			否则会有异常抛出。
		*/
		auto mw = Gui::MainWindow::getInstance();
		//mw->setParent(0);
		mw->close();
	}else if (sender() == ui->btMaxShow)
	{
		if (!isMax)
		{
			showMax();
		}else{
			showOld();
		}
		
	}
}

/**
* @brief  MainWindowDef::titleBarDoubleClicked 双击事件
* @return void  
*/
void MainWindowDef::titleBarDoubleClicked()
{
	if (!isMax)
	{
		showMax();
	}
	else{
		showOld();
	}
}

/**
* @brief  MainWindowDef::changeCursor 改变光标状态
* @param  const QPoint & pos  
* @return void  
*/
void MainWindowDef::changeCursor(const QPoint& pos)
{
	//防止已经在拖拽状态的时候改变光标的状态
	if (leftButtonIsPress)
	{
		return;
	}
		
	//如果已经最大化 则不允许拖拽
	if (isMax)
	{
		cursorState = NONE;
		return;
	}
	/*if (this->width() < 100 || this->height() < 100)
		return;*/
	auto rpos = this->pos() - pos;
	bool bright , bbottom ;
	bright = bbottom = false;

	if ((pos.x() + boundaryWidth - this->width()) > 0)
		bright = true;
	if ((pos.y() + boundaryWidth - this->height()) > 0)
		bbottom = true;
	 if (bbottom && bright)
	{
		setCursor(Qt::SizeFDiagCursor);
		cursorState = RIGHT_BOTTOM;
	}else if (bbottom)
	{
		setCursor(Qt::SizeVerCursor);
		cursorState = BOTTOM;
	}else if (bright){
		setCursor(Qt::SizeHorCursor);
		cursorState = RIGHT;
	}else{
		setCursor(Qt::ArrowCursor);
		cursorState = NONE;
	}
}

/**
* @brief  MainWindowDef::changeSize 改变大小
* @param  const QPoint & pos  
* @return void  
*/
void MainWindowDef::changeSize(const QPoint& pos)
{
	if (cursorState == NONE)
		return;
	if (!leftButtonIsPress)
		return;
	int w, h;
	w = pos.x() - leftButtonPressPos.x();
	h = pos.y() - leftButtonPressPos.y();
	leftButtonPressPos = pos;
	switch (cursorState)
	{
	case BOTTOM:
		this->resize(this->width(), this->height() + h);
		break;
	case RIGHT:
		this->resize(this->width() + w, this->height());
		break;
	case RIGHT_BOTTOM:
		this->resize(this->width() + w, this->height() + h);
		break;
	default:
		break;
	}
}


void MainWindowDef::addCenterWidget(QWidget *widget)
{
	ui->centerWidget->layout()->addWidget(widget);
}

void MainWindowDef::addTitleShortcutAction(QAction* action)
{
	auto  actions = toolbar->actions();
	for (auto i = actions.begin(); i != actions.end(); i++)
	{
		if ((*i)->text() == action->text())
			return;
	}
	toolbar->addAction(action);
}

/**
* @brief  MainWindowDef::showMax 最大化
* @return void  
*/
void MainWindowDef::showMax()
{
	oldSize = this->size();
	oldPoint = this->pos();
	QPoint centerPos = this->geometry().center();
	//QPoint screenPos = this->mapToGlobal(centerPos);
	for (auto index = 0; index < screens.size();index++)
	{
		//窗口中心点是否在该屏幕内？
		if (screens[index].contains(centerPos))
		{
			//存在
			resize(screens[index].size());
			move(screens[index].topLeft());
			isMax = true;
			break;
			
		}
	}
	//resize(QApplication::desktop()->availableGeometry().size());
	//move(0, 0);
	show();
	
}

/**
* @brief  MainWindowDef::showOld 
* @return void  
*/
void MainWindowDef::showOld()
{
	if (oldSize == this->size()) resize(this->width()*0.7,this->height()*0.7);
	else resize(oldSize);
	move(oldPoint);
	show();
}
/**
* @brief  MainWindowDef::test
* @return void  
*/
void MainWindowDef::test()
{
	if (LastSize.width()>this->width())
	{
		LastSize = this->size();
		tabWidgetInterface->setScale(this->size(),false);
	}
	else if (LastSize.width()<this->width())
	{
		LastSize = this->size();
		tabWidgetInterface->setScale(this->size(), true);
	}
}
#include "moc_MainWindowDef.cpp"
