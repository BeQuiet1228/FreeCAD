#pragma once
#ifdef _EDITOR_
#define EDITOR_EXPORT __declspec(dllexport)
#else
#define EDITOR_EXPORT   __declspec(dllimport)
#endif 