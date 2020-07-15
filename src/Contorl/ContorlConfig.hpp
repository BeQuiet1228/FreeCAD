#pragma once

#ifdef _CONTORL_
#define CONTROL_EXPORT __declspec(dllexport)
#else
#define CONTROL_EXPORT   __declspec(dllimport)
#endif // _CONTORL_