#pragma  once
#include "Renderer.h"
class RenderGrid :public Renderer {
public:
	RenderGrid(const unsigned int &xl = 7,const unsigned int& yl = 7);
	~RenderGrid() = default;
public:
	//‰÷»æ
	virtual bool drawImage() override;
	virtual bool drawPointImage() override;
	virtual bool setDefaultRang() override;
	virtual void dataInit() override;

	void setXLevel(const unsigned int& level){
		xLevel = level;
	};
	void setYLevel(const unsigned int& level) {
		yLevel = level;
	};

private:
	unsigned int xLevel, yLevel;
};