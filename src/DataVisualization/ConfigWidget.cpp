#include "ConfigWidget.h"
#include "ui_ConfigWidget.h"
#include "qwt/qwt_scale_widget.h"
#include"qwt/qwt_scale_engine.h";
#include "qwt/qwt_color_map.h"
#include "Plot.h"
#include "ConfigUnify.h"
#include "CustomConfig.h"
#include "C_encoding.h"
#include "ConfigFactory.h"
#include"qboxlayout.h"
#include"QFormLayout"
namespace DV {
	/**
	* @brief ConfigWidget::ConfigWidget
	* @param QWidget* panter
	*/
	ConfigWidget::ConfigWidget(QWidget* panter) :QWidget(panter), ui(new Ui::ConfigWidget)
	{
		ui->setupUi(this);
		initUI();
		//loadxmlConfig();
	}
	/**
	* @brief ConfigWidget::~ConfigWidget
	*/
	ConfigWidget::~ConfigWidget() {

	}
	/*
	* @brief  ConfigWidget::initUI 初始化UI
	* @return void
	*/
	void ConfigWidget::initUI()
	{
		qformlayout = new QFormLayout(ui->mTab);
		qformlayout->setSpacing(1);
		ui->mTab->setLayout(qformlayout);
		//qBoxLayout = new QBoxLayout(QBoxLayout::BottomToTop,ui->mTab);
		auto widgets = ConfigPageFactory::CreateConfigWidget();
		addTabWidget(widgets);
		connect(ui->applicButtom,SIGNAL(clicked()),this,SLOT(btnClicked()));
		connect(ui->cancleButtom,SIGNAL(clicked()),this,SLOT(btnClicked()));
	}
	/*
	* @brief  saveclicked 应用按钮
	* @return void
	*/
	void ConfigWidget::saveclicked()
	{
		/*
			三维模块
		*/
		//auto tabCount = ui->mTab->count();
		auto widgetCount = qformlayout->count();
		for (auto tabIndex = 0; tabIndex < widgetCount; ++tabIndex)
		{
			auto tabWidget = qformlayout->itemAt(tabIndex)->widget();
			ConfigUnify* configunify = dynamic_cast<ConfigUnify*>(tabWidget);
			if (nullptr != configunify)
				configunify->saveConfig();
		}
		/*
			二维模块
		*/
		ui->applicButtom->setEnabled(true);
#ifdef MY_DEBUG
		printf("saveclicked\n");
#endif
		emit plotLoadconfig();
	}

	void ConfigWidget::btnClicked()
	{
		if (sender() == ui->applicButtom)
			saveclicked();
		else if (sender() == ui->cancleButtom)
			canclelicked();
	}

	/**
	* @brief  ConfigWidget::loadxmlConfig 读取xml配置信息
	* @return void
	*/
	void ConfigWidget::loadxmlConfig() {
		/*
			三维模块
		*/
		//auto tabCount=ui->mTab->count();
		auto widgetCount = qformlayout->count();
		for (auto index=0;index< widgetCount;++index)
		{
			//auto tabWidget = ui->mTab->widget(index);
			auto tabWidget = qformlayout->itemAt(index)->widget();
			ConfigUnify* configunify = dynamic_cast<ConfigUnify*>(tabWidget);
			if (nullptr != configunify)
				configunify->loadConfig();
		}
	}
	/**
	* @brief  ConfigWidget::canclelicked 取消按钮
	* @return void
	*/
	void ConfigWidget::canclelicked()
	{
		this->close();
	}
	/**
	* @brief  ConfigWidget::getQwtLinearColorMap 返回颜色
	* @return QwtLinearColorMap*
	*/
	QwtLinearColorMap* ConfigWidget::getQwtLinearColorMap()
	{
		//读取xml文件
		Config::GetInstance()->loadConfig();
		ConfigGroup mGroup = Config::GetInstance()->getRootGroup();
		if (!mGroup.GroupIsempty("contour"))
		{
			ConfigGroup contourGroup = mGroup.getGroup("contour");
			bool isres = contourGroup.empty();
			QwtLinearColorMap::Mode mode;
			if (contourGroup.getGroup("lineMapColors").getValue("value").find("ScaleColors") != std::string::npos)
				mode = QwtLinearColorMap::Mode::ScaledColors;
			else
				mode = QwtLinearColorMap::Mode::FixedColors;
			std::vector<float> vals;
			std::vector<QColor> colors;
			auto lineMapColorGroup = contourGroup.getGroup("lineMapColorval");
			int count = atoi(lineMapColorGroup.getValue("valueNumber").c_str());
			vals.clear(); vals.reserve(count);
			colors.clear(); colors.reserve(count);
			for (auto index = 0; index < count; index++)
			{
				float val;
				QColor color;
				val = atof(
					lineMapColorGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("value").c_str());
				color = QStringToQColor(QString::fromStdString(
					lineMapColorGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("color")));
				vals.push_back(val);
				colors.push_back(color);
			}
			QwtLinearColorMap* colormap = new QwtLinearColorMap(*(colors.begin()), *(colors.end() - 1));
			for (auto index = 1; index < count - 1; index++)
			{
				colormap->addColorStop(vals[index], colors[index]);
			}
			colormap->setMode(mode);
			return colormap;
		}
		else
		{
			QwtLinearColorMap* map = new QwtLinearColorMap(Qt::darkBlue, Qt::darkRed);
			map->addColorStop(0.2, Qt::blue);
			map->addColorStop(0.4, Qt::cyan);
			map->addColorStop(0.6, Qt::yellow);
			map->addColorStop(0.8, Qt::red);
			return map;
		}

	}
	void ConfigWidget::bindplot(Plot* lp)
	{
		if (lp)
		{
			connect(this, SIGNAL(plotLoadconfig()), lp, SLOT(setappEvent()));
		}
	}

	void ConfigWidget::addTabWidget(std::vector<QWidget*>& widgets)
	{
		for (auto iter=widgets.begin();iter!=widgets.end();iter++)
		{
			(*iter)->setParent(this);
			//ui->mTab->addTab(*iter,(*iter)->windowTitle());
			qformlayout->addWidget(*iter);
		}
	}
};

#include "moc_ConfigWidget.cpp"

