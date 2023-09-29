// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API
#include "example.hpp"          // Include short list of convenience functions for rendering

#include <algorithm>            // std::min, std::max


#include <imgui.h>
#include "imgui_impl_glfw.h"


#include "scene.h"
#include "utils.h"

#include "glm/glm.hpp"

#include "glm/gtc/matrix_transform.hpp"
#include "glm/gtx/euler_angles.hpp"

// [Win32] Our example includes a copy of glfw3.lib pre-compiled with VS2010 to maximize ease of testing and compatibility with old VS compilers.
// To link with VS2010-era libraries, VS2015+ requires linking with legacy_stdio_definitions.lib, which we do using this pragma.
// Your own project should not be affected, as you are likely to link with a newer binary of GLFW that is adequate for your version of Visual Studio.
#if defined(_MSC_VER) && (_MSC_VER >= 1900) && !defined(IMGUI_DISABLE_WIN32_FUNCTIONS)
#pragma comment(lib, "legacy_stdio_definitions")
#endif


int time_elaps = 0;
/// 
glm::mat4 UpdateModelMatrix(glm::vec3 Translation, glm::vec3 euler)
{
    glm::mat4 ModelMatrix = glm::mat4(1);
    

    ModelMatrix = glm::translate(ModelMatrix, Translation);
    glm::mat4 transform = glm::eulerAngleYXZ(euler.y, euler.x, euler.z);

    return ModelMatrix * transform;
}


// Handles all the OpenGL calls needed to display the point cloud
void draw_point_cloud(float width, float height, glfw_state& app_state, rs2::points& points)
{
   
    // OpenGL commands that prep screen for the pointcloud
    glLoadIdentity();
    glPushAttrib(GL_ALL_ATTRIB_BITS);

    glClearColor(153.f / 255, 153.f / 255, 153.f / 255, 1);
    glClear(GL_DEPTH_BUFFER_BIT);

    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    gluPerspective(60, width / height, 0.01f, 10.0f);

    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    gluLookAt(0, 0, 0, 0, 0, 1, 0, -1, 0);

    glTranslatef(0, 0, +0.5f + app_state.offset_y * 0.05f);
    glRotated(app_state.pitch, 1, 0, 0);
    glRotated(app_state.yaw, 0, 1, 0);
    glTranslatef(0, 0, -0.5f);

    glPointSize(width / 640);
    glEnable(GL_DEPTH_TEST);
    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, app_state.tex.get_gl_handle());
    float tex_border_color[] = { 0.8f, 0.8f, 0.8f, 0.8f };
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, tex_border_color);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, 0x812F); // GL_CLAMP_TO_EDGE
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, 0x812F); // GL_CLAMP_TO_EDGE
    glBegin(GL_POINTS);

    glm::mat4 m = glm::mat4(1);
    
    if (getScene()->cameras.size() > 0)
    {
        m = UpdateModelMatrix(getScene()->cameras[0]->camPos, getScene()->cameras[0]->camRot);
    }
    /* this segment actually prints the pointcloud */
    auto vertices = points.get_vertices();              // get vertices
    auto tex_coords = points.get_texture_coordinates(); // and texture coordinates
    for (int i = 0; i < points.size(); i++)
    {
        if (vertices[i].z)
        {
            glm::vec4 v(vertices[i].x, vertices[i].y, vertices[i].z,1.0);

            v = m * v;
            // upload the point and texture coordinates only for points we have depth data for
            glVertex3f(v.x, v.y, v.z);
            glTexCoord2fv(tex_coords[i]);
        }
    }

    // OpenGL cleanup
    glEnd();
    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    glPopMatrix();
    glPopAttrib();
}


// Helper functions
void register_glfw_callbacks(window& app, glfw_state& app_state);


void render_ui(float w, float h)
{
    // Flags for displaying ImGui window
    static const int flags = ImGuiWindowFlags_NoCollapse
        | ImGuiWindowFlags_NoScrollbar
        | ImGuiWindowFlags_NoSavedSettings
        | ImGuiWindowFlags_NoTitleBar
        | ImGuiWindowFlags_NoResize
        | ImGuiWindowFlags_NoMove;

    ImGui_ImplGlfw_NewFrame(1);
    ImGui::SetNextWindowSize({ w, h });
    ImGui::Begin("app", nullptr, flags);

	// 2. Show a simple window that we create ourselves. We use a Begin/End pair to created a named window.
	ImGui::Begin("Configuration", nullptr, 0);
	{
        for (auto cam :  getScene()->cameras)
        {
            std::string s = cam->name;

            ImGui::BeginChild(s.c_str(), ImVec2(400, 380), 1);
            {

                        ImGui::Text(" CAMERA PARAMETERS ");
                        bool changed = false;
                        if (ImGui::SliderFloat("CamPosX", &cam->camPos.x, -2.0f, 10.0f)) { changed = true; }
                        if (ImGui::SliderFloat("CamPosZ", &cam->camPos.z, -2.0f, 10.0f)) { changed = true; }
                        if (ImGui::SliderFloat("PITCH", &cam->camRot.x, -180.0f, 180.0f)) { changed = true; }
                        if (ImGui::SliderFloat("YAW", &cam->camRot.y, -180.0f, 180.0f)) { changed = true; }
                        if (ImGui::SliderFloat("CamRange", &cam->camRange, 0.10f, 10.0f)) { changed = true; }
                        if (ImGui::SliderFloat("RoomSizeX", &getScene()->roomSize.width, 0.50f, 10.0f)) { changed = true; }
                        if (ImGui::SliderFloat("RoomSizeY", &getScene()->roomSize.height, 0.50f, 10.0f)) { changed = true; }


               
            ImGui::EndChild();
        }
		}

	

	
		ImGui::End();



	}

    ImGui::End();
    ImGui::Render();
}


int main(int argc, char* argv[]) try
{
    /////////////////////////////////////////////////////

    
    // Create a simple OpenGL window for rendering:
    window app(1280, 720, "Papamon - 3D Viewer");
    ImGui_ImplGlfw_Init(app, false);
    // Setup Platform/Renderer bindings


    // Construct an object to manage view state
    glfw_state app_state;
    // register callbacks to allow manipulation of the pointcloud
    register_glfw_callbacks(app, app_state);

    // Declare pointcloud object, for calculating pointclouds and texture mappings
    rs2::pointcloud pc;
    // We want the points object to be persistent so we can display the last cloud when a frame drops
    rs2::points points;

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    // Start streaming with default recommended configuration
    pipe.start();

    initScene("case_Sample0.json", true);


#ifdef IMGUI
    std::thread renderThread;
    if (renderUI) renderThread = std::thread(renderLoop);
#endif	//std::thread inferenceThread(runInference);

    while (app) // Application still alive?
    {
        float w = static_cast<float>(app.width());
        float h = static_cast<float>(app.height());

        // Render the GUI
        render_ui(w, h);

        // Wait for the next set of frames from the camera
        auto frames = pipe.wait_for_frames();

        auto color = frames.get_color_frame();

        // For cameras that don't have RGB sensor, we'll map the pointcloud to infrared instead of color
        if (!color)
            color = frames.get_infrared_frame();

        // Tell pointcloud object to map to this color frame
        pc.map_to(color);

        auto depth = frames.get_depth_frame();

        // Generate the pointcloud and texture mappings
        points = pc.calculate(depth);

        // Upload the color frame to OpenGL
        app_state.tex.upload(color);

        // Draw the pointcloud
        draw_point_cloud(app.width(), app.height(), app_state, points);

        render_ui(200, 200);
    }

    return EXIT_SUCCESS;
}
catch (const rs2::error& e)
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return EXIT_FAILURE;
}
catch (const std::exception& e)
{
    std::cerr << e.what() << std::endl;
    return EXIT_FAILURE;
}
