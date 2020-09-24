// K-3D
// Copyright (c) 1995-2009, Timothy M. Shead
//
// Contact: tshead@k-3d.com
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public
// License as published by the Free Software Foundation; either
// version 2 of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public
// License along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

/** \file
	\author Timothy M. Shead (tshead@k-3d.com)
	\author Romain Behar (romainbehar@yahoo.com)
*/

//#include <k3d-i18n-config.h>
//#include <k3dsdk/document_plugin_factory.h>
//#include <k3dsdk/imaterial.h>
//#include <k3dsdk/mesh_source.h>
//#include <k3dsdk/material_sink.h>
//#include <k3dsdk/measurement.h>
//#include <k3dsdk/node.h>
#include "polyhedron.h"

namespace module
{

namespace polyhedron
{

namespace sources
{

/////////////////////////////////////////////////////////////////////////////
// poly_cylinder

class poly_cylinder// :public k3d::material_sink<k3d::mesh_source<k3d::node > >
{
        //typedef k3d::material_sink<k3d::mesh_source<k3d::node > > base;

public:
        poly_cylinder()://(k3d::iplugin_factory& Factory, k3d::idocument& Document) :
                //base(Factory, Document),
                m_u_segments(32),
                m_v_segments(5),
                m_top(true),
                m_bottom(true),
                m_radius(5.0),//0.1
                m_zmax(5.0),//0.1
                m_zmin(-5.0),//0.1
                m_u_power(1.0),//0.1
                m_top_segments(0),
                m_bottom_segments(0)
	{
                /*m_material.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_u_segments.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_v_segments.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_top.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_bottom.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_radius.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_zmax.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_zmin.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_u_power.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_top_segments.changed_signal().connect(k3d::hint::converter<
			k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));
		m_bottom_segments.changed_signal().connect(k3d::hint::converter<
                        k3d::hint::convert<k3d::hint::any, k3d::hint::none> >(make_update_mesh_slot()));*/
	}
//public slots:
	void on_update_mesh_topology(k3d::mesh& Output)
	{
		Output = k3d::mesh();

                k3d::imaterial* const material = m_material;
                const k3d::int32_t u_segments = m_u_segments;
                const k3d::int32_t v_segments = m_v_segments;
                const k3d::double_t radius = m_radius;
                const k3d::double_t zmax = m_zmax;
                const k3d::double_t zmin = m_zmin;
                const k3d::double_t u_power = m_u_power;
		const k3d::double_t inv_u_power = u_power ? 1.0 / u_power : 1.0;
                const k3d::bool_t top = m_top;
                const k3d::bool_t bottom = m_bottom;
                const k3d::int32_t top_segments = m_top_segments;
                const k3d::int32_t bottom_segments = m_bottom_segments;

                //boost::scoped_ptr<k3d::polyhedron::primitive> polyhedron(k3d::polyhedron::create(Output));
                k3d::polyhedron::primitive *polyhedron = k3d::polyhedron::create(Output);

		polyhedron->shell_types.push_back(k3d::polyhedron::POLYGONS);
		k3d::polyhedron::add_cylinder(Output, *polyhedron, 0, v_segments, u_segments, material);

		k3d::mesh::points_t& points = Output.points.writable();
		k3d::mesh::selection_t& point_selection = Output.point_selection.writable();

		// Shape the cylinder points
		for(k3d::int32_t v = 0; v <= v_segments; ++v)
		{
			const k3d::double_t height = k3d::ratio(v, v_segments);

			for(k3d::int32_t u = 0; u != u_segments; ++u)
			{
				const k3d::double_t theta = k3d::pi_times_2() * k3d::ratio(u, u_segments);

				k3d::double_t x = cos(theta);
				k3d::double_t y = -sin(theta);
				k3d::double_t z = k3d::mix(zmax, zmin, height);

				x = radius * k3d::sign(x) * std::pow(std::abs(x), inv_u_power);
				y = radius * k3d::sign(y) * std::pow(std::abs(y), inv_u_power);

				points[v * u_segments + u] = k3d::point3(x, y, z);
			}
		}

		const k3d::uint_t top_rim_offset = 0;
		const k3d::uint_t bottom_rim_offset = v_segments * u_segments;

		// Optionally cap the top of the cylinder ...
		if(top)
		{
			if(!top_segments)
			{
				polyhedron->face_shells.push_back(0);
				polyhedron->face_first_loops.push_back(polyhedron->loop_first_edges.size());
				polyhedron->face_loop_counts.push_back(1);
				polyhedron->face_selections.push_back(0);
				polyhedron->face_materials.push_back(material);

				polyhedron->loop_first_edges.push_back(polyhedron->clockwise_edges.size());

				for(k3d::int32_t u = 0; u != u_segments; ++u)
				{
					polyhedron->clockwise_edges.push_back(polyhedron->clockwise_edges.size() + 1);
					polyhedron->edge_selections.push_back(0);

					polyhedron->vertex_points.push_back((u_segments - u) % u_segments);
					polyhedron->vertex_selections.push_back(0);
				}
				polyhedron->clockwise_edges.back() = polyhedron->loop_first_edges.back();
			}
			else
			{
				const k3d::uint_t middle_point_index = points.size();
				const k3d::point3 middle_point(0, 0, zmax);
				points.push_back(middle_point);
				point_selection.push_back(0);

				// Create segment quads
				k3d::uint_t last_ring_point_offset = 0;
				k3d::uint_t current_ring_point_offset = 0;
				for(k3d::int32_t n = top_segments; n > 1; --n)
				{
					current_ring_point_offset = points.size();
					const k3d::double_t factor = k3d::ratio(n - 1, top_segments);
					for(k3d::int32_t u = 0; u < u_segments; ++u)
					{
						points.push_back(middle_point + factor * (points[u] - middle_point));
						point_selection.push_back(0);
					}

					for(k3d::int32_t u = 0; u < u_segments; ++u)
					{
						k3d::polyhedron::add_quadrilateral(
							Output,
							*polyhedron,
							0,
							last_ring_point_offset + (u + 1) % u_segments,
							last_ring_point_offset + (u + 0) % u_segments,
							current_ring_point_offset + (u + 0) % u_segments,
							current_ring_point_offset + (u + 1) % u_segments,
							material);
					}

					last_ring_point_offset = current_ring_point_offset;
				}

				// Create middle triangle fan
				for(k3d::int32_t u = 0; u != u_segments; ++u)
				{
					k3d::polyhedron::add_triangle(
						Output,
						*polyhedron,
						0, 
						current_ring_point_offset + (u + 1) % u_segments,
						current_ring_point_offset + (u + 0) % u_segments,
						middle_point_index,
						material);
				}
			}
		}

		// Optionally cap the bottom of the cylinder ...
		if(bottom)
		{
			if(!bottom_segments)
			{
				polyhedron->face_shells.push_back(0);
				polyhedron->face_first_loops.push_back(polyhedron->loop_first_edges.size());
				polyhedron->face_loop_counts.push_back(1);
				polyhedron->face_selections.push_back(0);
				polyhedron->face_materials.push_back(material);

				polyhedron->loop_first_edges.push_back(polyhedron->clockwise_edges.size());

				for(k3d::int32_t u = 0; u != u_segments; ++u)
				{
					polyhedron->clockwise_edges.push_back(polyhedron->clockwise_edges.size() + 1);
					polyhedron->edge_selections.push_back(0);

					polyhedron->vertex_points.push_back(bottom_rim_offset + u);
					polyhedron->vertex_selections.push_back(0);
				}
				polyhedron->clockwise_edges.back() = polyhedron->loop_first_edges.back();
			}
			else
			{
				const k3d::uint_t middle_point_index = points.size();
				const k3d::point3 middle_point(0, 0, zmin);
				points.push_back(middle_point);
				point_selection.push_back(0);

				// Create segment quads
				k3d::uint_t last_ring_point_offset = v_segments * u_segments;
				k3d::uint_t current_ring_point_offset = v_segments * u_segments;
				for(k3d::int32_t n = bottom_segments; n > 1; --n)
				{
					current_ring_point_offset = points.size();
					const k3d::double_t factor = k3d::ratio(n - 1, bottom_segments);
					for(k3d::int32_t u = 0; u < u_segments; ++u)
					{
						points.push_back(middle_point + factor * (points[(v_segments * u_segments) + u] - middle_point));
						point_selection.push_back(0);
					}

					for(k3d::int32_t u = 0; u < u_segments; ++u)
					{
						k3d::polyhedron::add_quadrilateral(
							Output,
							*polyhedron,
							0,
							last_ring_point_offset + (u + 0) % u_segments,
							last_ring_point_offset + (u + 1) % u_segments,
							current_ring_point_offset + (u + 1) % u_segments,
							current_ring_point_offset + (u + 0) % u_segments,
							material);
					}

					last_ring_point_offset = current_ring_point_offset;
				}

				// Create middle triangle fan
				for(k3d::int32_t u = 0; u != u_segments; ++u)
				{
					k3d::polyhedron::add_triangle(
						Output,
						*polyhedron,
						0,
						current_ring_point_offset + (u + 0) % u_segments,
						current_ring_point_offset + (u + 1) % u_segments,
						middle_point_index,
						material);
				}
			}
		}
	}

	void on_update_mesh_geometry(k3d::mesh& Output)
	{
	}

        /*static k3d::iplugin_factory& get_factory()
	{
		static k3d::document_plugin_factory<poly_cylinder, k3d::interface_list<k3d::imesh_source > > factory(
			k3d::uuid(0xd8c4d9fd, 0x42334a54, 0xa4b48185, 0xd8506489),
			"PolyCylinder",
			_("Generates a polygonal cylinder with optional endcaps"),
			"Polyhedron",
			k3d::iplugin_factory::STABLE);

		return factory;
        }*/
protected:
        k3d::imaterial* m_material;
private:
        k3d::int32_t m_u_segments;
        k3d::int32_t m_v_segments;
        k3d::bool_t m_top;
        k3d::bool_t m_bottom;
        k3d::double_t m_radius;
        k3d::double_t m_zmax;
        k3d::double_t m_zmin;
        k3d::double_t m_u_power;
        k3d::int32_t m_top_segments;
        k3d::int32_t m_bottom_segments;
};

/////////////////////////////////////////////////////////////////////////////
// poly_cylinder_factory

/*k3d::iplugin_factory& poly_cylinder_factory()
{
	return poly_cylinder::get_factory();
}*/

} // namespace sources

} // namespace polyhedron

} // namespace module

