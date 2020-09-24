#ifndef ABLEGLRENDER_H
#define ABLEGLRENDER_H
//#include <opencsg.h>
namespace PM3
{
class ableGLRender/*:public OpenCSG::Primitive*/
{
public:
    ableGLRender(/*OpenCSG::Operation o=OpenCSG::Intersection, unsigned int c=1*/):bCanClipping(true),bupdate_mesh_topology(true){};
    ~ableGLRender() {};
    virtual void render(){};
    virtual void gl_select(){};

    bool bCanClipping;//是否在裁剪模式下显示
    bool bupdate_mesh_topology;//是否具有结构
};
}

#endif // ABLERENDER_H
