#ifndef SDK_RENDER_STATE_GL_H
#define SDK_RENDER_STATE_GL_H


class CCamera;


/// Used to pass (potentially) useful rendering state from the engine to the object being rendered
class render_state
{
public:
        render_state(CCamera& _camera) :
                camera(_camera),
		orthographic(false),
		draw_two_sided(true)
	{
	}

	/// Stores the camera used for drawing
        CCamera& camera;

	/// Set to true iff the OpenGL viewing frustum used for drawing is orthographic
	bool orthographic;
	
	bool draw_two_sided;
	
	//@{
	/** Stores the OpenGL viewing frustum used for drawing (perspective or orthographic).
	 * Note: these are the actual values passed to glFrustum() or glOrtho() to fill the
	 * render window, in general they will be different from the viewing frustum defined
	 * by the camera for rendering. */
	double gl_window_frustum_left;
	double gl_window_frustum_right;
	double gl_window_frustum_top;
	double gl_window_frustum_bottom;
	double gl_window_frustum_near;
	double gl_window_frustum_far;
	//@}
	
	//@{
	/** Stores an imaginary OpenGL viewing frustum that represents the viewing frustum
	 * defined by the camera for rendering.  Note that the values may not be the same
	 * as those returned by the camera object.  */
	double gl_camera_frustum_left;
	double gl_camera_frustum_right;
	double gl_camera_frustum_top;
	double gl_camera_frustum_bottom;
	double gl_camera_frustum_near;
	double gl_camera_frustum_far;
	//@}

	/// Stores the current OpenGL projection matrix
	float gl_projection_matrix[16];
	/// Stores the current OpenGL viewport
	GLint gl_viewport[4];
	
	/// Stores the selection state of the calling node
	double node_selection;
	/// Stores the selection state of the parent of the calling node
	double parent_selection;
};


#endif

