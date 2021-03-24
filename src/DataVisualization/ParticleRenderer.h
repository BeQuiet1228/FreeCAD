#pragma  once
#include "Renderer.h"
#include <memory>
class ParticleData;
class ParticleRenderer :public Renderer{
public:
	ParticleRenderer(std::shared_ptr<ParticleData> data);
	~ParticleRenderer();


public:
	bool drawImage() override;
	bool setDefaultRang() override;
	void dataInit() override;
	bool drawPointImage() override{ return true; };
};