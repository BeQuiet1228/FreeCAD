#pragma once
#include <QImage>
#include <mutex>
#include <QSize>
#include "Data.h"
#include <memory>
#include <list>
#include <QImage>
#include <map>
namespace DV {
	class Renderer {
	public:
		using AutoMutex = std::lock_guard<std::mutex>;
	public:
		Renderer(std::shared_ptr<Data> data);
		virtual ~Renderer();
		friend class Plot;
	public:
		//操作渲染图
		void setImage(const QImage& map);
		QImage getImage();
		//设置渲染大小
		void setSize(const QSize& size);
		void setSize(const int& width, const int& hegiht);
		QSize getSize();
		//设置取点的位置
		void setFindPosition(const QPointF& pos);
		QPointF getFindPosition();
		//操作范围
		void setXRang(const Data::Rang& rang);
		Data::Rang getXRang();
		void setYRang(const Data::Rang& rang);
		Data::Rang getYRang();
		//获取图类型
		Data::NeedStructType getNeedStrucuType() {
			return data->getNeedStructType();
		}
		//获取方向
		DirectionType getDirection() {
			return data->getDirectionType();
		}
		//绘制取点信息
		void displayPointInformation(QPainter*, QPointF*, std::map<QString, float>);
		void setRatioDisplay(const double& horizontal, const double& vertical);
		std::shared_ptr<Data> getData();
	private:
		//渲染图
		QImage image;
		std::mutex imageMutex;
		//渲染大小
		QSize imageSize;
		std::mutex imageSizeMutex;
		//点的位置
		QPointF findPosition;
		std::mutex findPositionMutex;
		//渲染范围
		Data::Rang xRang, yRang;
		std::mutex xRangMutex, yRangMutex;
	protected:
		//数据类
		std::shared_ptr<Data> data;
		//获取屏幕与数据之间的缩放比例
		bool getTransitionScale(float& xScale, float& yScale);
		//数据转换
		float transitionDataToScreen(const  float& d, const float scale, Data::Rang rang);
	public:
		virtual bool drawImage() = 0;
		virtual bool addListRang(std::list<Data::Rang> listRang);
		virtual bool drawPointImage() = 0;
		//设置为默认渲染范围
		virtual bool setDefaultRang() = 0;
		virtual bool setDefaultRang(QSize&);
		//初始化数据
		virtual void dataInit();
		virtual void loadconfig() {};
		//获取图表信息
		virtual std::string getInformationTitile();
	};

	class RendererValueRangeInterface {
	public:
		RendererValueRangeInterface() = default;
		virtual ~RendererValueRangeInterface() {};
	public:
		virtual Data::Rang getValueRange() = 0;

	};
};
