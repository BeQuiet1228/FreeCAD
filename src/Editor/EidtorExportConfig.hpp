#pragma once
#ifdef _EDITOR_
#define EIDTOR_EXPORT __declspec(dllexport)
#else
#define EIDTOR_EXPORT   __declspec(dllimport)
#endif 