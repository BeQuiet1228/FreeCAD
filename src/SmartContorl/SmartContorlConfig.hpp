#pragma once
#ifdef _SMARTCONTORL_
#define SMARTCONTORL_EXPORT __declspec(dllexport)
#else
#define SMARTCONTORL_EXPORT   __declspec(dllimport)
#endif // _CONTORL_