#pragma once

class Contorl;
class _declspec(dllexport) ContorlInterface
{
public:
	ContorlInterface();
	~ContorlInterface();
public:
	Contorl *contorl;

public:
	void * getContorlButtonBar();
	void * getContorlDataBar();
};
