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

#define M_PI 3.14156
int time_elaps = 0;

bool renderSceneBox = true;


// Construct an object to manage view state
glfw_state app_state;

glm::vec3 viewPos;
glm::vec3 viewRot;
texture tex;

// Declare RealSense pipeline, encapsulating the actual device and sensors
rs2::pipeline pipe;

/// 
glm::mat4 UpdateModelMatrix(glm::vec3 Translation, glm::vec3 euler)
{
    glm::mat4 ModelMatrix = glm::mat4(1);
    

    ModelMatrix = glm::translate(ModelMatrix, Translation);
    glm::mat4 transform = glm::eulerAngleYXZ(euler.y, euler.x, euler.z);

    return ModelMatrix * transform;
}


void DrawCube(glm::vec3 roomSize)
{
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    glLineWidth(4.0);
    
    glPushMatrix();
    glTranslatef(0.0, 0.0,0.0);
  
    glScalef(roomSize.x, roomSize.y, roomSize.z);
  
    glBegin(GL_QUADS);        // Draw The Cube Using quads

    glColor3f(1.0f, 1.0f, 1.0f);    // Color Blue
    glVertex3f(1.0f, 1.0f, -1.0f);    // Top Right Of The Quad (Top)
    glVertex3f(-1.0f, 1.0f, -1.0f);    // Top Left Of The Quad (Top)
    glVertex3f(-1.0f, 1.0f, 1.0f);    // Bottom Left Of The Quad (Top)
    glVertex3f(1.0f, 1.0f, 1.0f);    // Bottom Right Of The Quad (Top)
    glColor3f(1.0f, 0.5f, 0.0f);    // Color Orange
    glVertex3f(1.0f, -1.0f, 1.0f);    // Top Right Of The Quad (Bottom)
    glVertex3f(-1.0f, -1.0f, 1.0f);    // Top Left Of The Quad (Bottom)
    glVertex3f(-1.0f, -1.0f, -1.0f);    // Bottom Left Of The Quad (Bottom)
    glVertex3f(1.0f, -1.0f, -1.0f);    // Bottom Right Of The Quad (Bottom)
    glColor3f(1.0f, 0.0f, 0.0f);    // Color Red    
    glVertex3f(1.0f, 1.0f, 1.0f);    // Top Right Of The Quad (Front)
    glVertex3f(-1.0f, 1.0f, 1.0f);    // Top Left Of The Quad (Front)
    glVertex3f(-1.0f, -1.0f, 1.0f);    // Bottom Left Of The Quad (Front)
    glVertex3f(1.0f, -1.0f, 1.0f);    // Bottom Right Of The Quad (Front)
    glColor3f(1.0f, 1.0f, 0.0f);    // Color Yellow
    glVertex3f(1.0f, -1.0f, -1.0f);    // Top Right Of The Quad (Back)
    glVertex3f(-1.0f, -1.0f, -1.0f);    // Top Left Of The Quad (Back)
    glVertex3f(-1.0f, 1.0f, -1.0f);    // Bottom Left Of The Quad (Back)
    glVertex3f(1.0f, 1.0f, -1.0f);    // Bottom Right Of The Quad (Back)
    glColor3f(0.0f, 0.0f, 1.0f);    // Color Blue
    glVertex3f(-1.0f, 1.0f, 1.0f);    // Top Right Of The Quad (Left)
    glVertex3f(-1.0f, 1.0f, -1.0f);    // Top Left Of The Quad (Left)
    glVertex3f(-1.0f, -1.0f, -1.0f);    // Bottom Left Of The Quad (Left)
    glVertex3f(-1.0f, -1.0f, 1.0f);    // Bottom Right Of The Quad (Left)
    glColor3f(1.0f, 0.0f, 1.0f);    // Color Violet
    glVertex3f(1.0f, 1.0f, -1.0f);    // Top Right Of The Quad (Right)
    glVertex3f(1.0f, 1.0f, 1.0f);    // Top Left Of The Quad (Right)
    glVertex3f(1.0f, -1.0f, 1.0f);    // Bottom Left Of The Quad (Right)
    glVertex3f(1.0f, -1.0f, -1.0f);    // Bottom Right Of The Quad (Right)
    glEnd();            // End Drawing The Cube


    glPopMatrix();
    
   
    glColor3f(1.0f, 1.0f, 1.0f);    // Color Blue
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
   
}


void DrawCamera(glm::vec3 camPos, glm::vec3 camRot) {
    int i, j;

    double r = 0.05;
    int lats = 10, longs = 10;


    const float fov = 45.0f;

    glm::vec3 cameraPos = camPos;
    glm::vec3 cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);
    glm::vec3 cameraRight = glm::vec3(1.0f, 0.0f, 0.0f);
    glm::vec3 cameraForward = glm::normalize(glm::cross(cameraUp, cameraRight));

    glm::mat4 initialCameraProjection = glm::perspective(glm::radians(fov), (float)1.33f, 0.1f, 8.0f);

    glm::mat4 initialCameraView = glm::lookAt(
        cameraPos,
        cameraPos + cameraForward,
        cameraUp);

    std::array<glm::vec3, 8> _cameraFrustumCornerVertices{
    {
        { -1.0f, -1.0f, 1.0f }, { 1.0f, -1.0f, 1.0f }, { 1.0f, 1.0f, 1.0f }, { -1.0f, 1.0f, 1.0f },
        { -1.0f, -1.0f, -1.0f }, { 1.0f, -1.0f, -1.0f }, { 1.0f, 1.0f, -1.0f }, { -1.0f, 1.0f, -1.0f },
    }
    };

    const auto proj = glm::inverse(initialCameraProjection * initialCameraView);

    std::array<glm::vec3, 8> _frustumVertices;

    std::transform(
        _cameraFrustumCornerVertices.begin(),
        _cameraFrustumCornerVertices.end(),
        _frustumVertices.begin(),
        [&](glm::vec3 p) {
            auto v = proj * glm::vec4(p, 1.0f);
            return glm::vec3(v) / v.w;
        }
    );

    std::vector<int> lines = { 0,1,0,2,3,1,3,2,4,5,4,6,7,5,7,6,0,4,1,5,3,7,2,6 };

    glBegin(GL_LINES);
    glLineWidth(2.0f);

    for (int i = 0; i < lines.size(); i = i + 2)
    {
        glVertex3f(_frustumVertices[lines[i]].x, _frustumVertices[lines[i]].y, _frustumVertices[lines[i]].z);
        glVertex3f(_frustumVertices[lines[i+1]].x, _frustumVertices[lines[i+1]].y, _frustumVertices[lines[i+1]].z);
    }
    glEnd();

    glPushMatrix();

    glTranslatef(camPos.x, camPos.y, camPos.z);

    for (i = 0; i <= lats; i++) {
        double lat0 = M_PI * (-0.5 + (double)(i - 1) / lats);
        double z0 = sin(lat0);
        double zr0 = cos(lat0);

        double lat1 = M_PI * (-0.5 + (double)i / lats);
        double z1 = sin(lat1);
        double zr1 = cos(lat1);

        glBegin(GL_QUAD_STRIP);
        for (j = 0; j <= longs; j++) {
            double lng = 2 * M_PI * (double)(j - 1) / longs;
            double x = cos(lng);
            double y = sin(lng);

            glNormal3d(x * zr0, y * zr0, z0);
            glVertex3d(r * x * zr0, r * y * zr0, r * z0);
            glNormal3d(x * zr1, y * zr1, z1);
            glVertex3d(r * x * zr1, r * y * zr1, r * z1);
        }
        glEnd();
    }

    glPopMatrix();
}

// Handles all the OpenGL calls needed to display the point cloud
void drawScene(float width, float height)
{
   
    
    // OpenGL commands that prep screen for the pointcloud
    glLoadIdentity();
    glPushAttrib(GL_ALL_ATTRIB_BITS);

    glClearColor(153.f / 255, 153.f / 255, 153.f / 255, 1);
    glClear(GL_DEPTH_BUFFER_BIT);

    
    glMatrixMode(GL_PROJECTION);
    glPushMatrix();
    gluPerspective(60, width / height, 0.01f, 50.0f);

    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    gluLookAt(0, 0, 0, 0, 0, 1, 0, -1, 0);

    glTranslatef(viewPos.x, viewPos.y, viewPos.z);
    glRotated(viewRot.x, 1, 0, 0);
    glRotated(viewRot.y, 0, 1, 0);
    glRotated(viewRot.z, 0, 0, 1);
    glTranslatef(0, 0, -0.5f);

    glColor3f(1.0, 1.0, 1.0);
    glEnable(GL_DEPTH_TEST);
    if (renderSceneBox)
    {
        DrawCube(getScene()->roomSize);
    }
    DrawCamera(getScene()->cameras[0]->camPos, getScene()->cameras[0]->camRot);

    glPointSize(width / 640);

    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, tex.get_gl_handle());
    float tex_border_color[] = { 0.8f, 0.8f, 0.8f, 0.8f };
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, tex_border_color);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, 0x812F); // GL_CLAMP_TO_EDGE
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, 0x812F); // GL_CLAMP_TO_EDGE
    glBegin(GL_POINTS);

    glm::mat4 m = glm::mat4(1);

    if (getScene()->cameras.size() > 0)
    {

        for (auto cam : getScene()->cameras)
        {
            m = UpdateModelMatrix(cam->camPos, cam->camRot);

            /* this segment actually prints the pointcloud */
            for (int i = 0; i < cam->vertices.size(); i++)
            {
                if (cam->vertices[i].z)
                {
                    glm::vec4 v(cam->vertices[i].x, cam->vertices[i].y, cam->vertices[i].z, 1.0);
                    v = m * v;
                    //glColor3b(cam->colors[i].x, cam->colors[i].y, cam->colors[i].z);
                    // upload the point and texture coordinates only for points we have depth data for
                    glVertex3f(v.x, v.y, -v.z);
                    glTexCoord2f(cam->tex_coords[i].x, cam->tex_coords[i].y);
                }
            }
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
        ImGui::Checkbox("RenderSceneBox", &renderSceneBox);
        float roomsizeX = getScene()->roomSize.x;
        float roomsizeY = getScene()->roomSize.y;
        float roomsizeZ = getScene()->roomSize.z;

        bool changed = false;
        if (ImGui::SliderFloat("RoomSizeX", &roomsizeX, 0.50f, 20.0f)) { changed = true; }
        if (ImGui::SliderFloat("RoomSizeY", &roomsizeY, 0.50f, 20.0f)) { changed = true; }
        if (ImGui::SliderFloat("RoomSizeZ", &roomsizeZ, 0.50f, 20.0f)) { changed = true; }

        if (changed) getScene()->roomSize = glm::vec3(roomsizeX, roomsizeY, roomsizeZ);

        ImGui::SliderFloat("ViewPosX", &viewPos.x, -2.0f, 10.0f);
        ImGui::SliderFloat("ViewPosY", &viewPos.y, -2.0f, 10.0f);
        ImGui::SliderFloat("ViewPosZ", &viewPos.z, -2.0f, 10.0f);

        ImGui::SliderFloat("ViewRotX", &viewRot.x, -180.0f, 180.0f);
        ImGui::SliderFloat("ViewRotY", &viewRot.y, -180.0f, 180.0f);
        ImGui::SliderFloat("ViewRotZ", &viewRot.z, -180.0f, 180.0f);
        if (ImGui::Button("New camera"))
        {
            getScene()->cameras.push_back(new Camera(std::to_string(getScene()->camerasID), ""));
            getScene()->camerasID += 1;
        }
        int index = 0;
        for (auto cam : getScene()->cameras)
        {
            ImGui::SameLine();
            if (ImGui::Button(cam->name.c_str()))
            {
                getScene()->selectedCamera = index;
            }

            index++;
           
        }

        //for (auto cam :  getScene()->cameras)
        auto cam = getScene()->cameras[getScene()->selectedCamera];
        {
            
            std::string s = cam->name;

            ImGui::BeginChild(s.c_str(), ImVec2(400, 280), true,0);
            {

                        ImGui::Text(" CAMERA PARAMETERS ");
                        changed = false;
                        if (ImGui::SliderFloat("CamPosX", &cam->camPos.x, -2.0f, 10.0f)) { changed = true; }
                        if (ImGui::SliderFloat("CamPosZ", &cam->camPos.z, -2.0f, 10.0f)) { changed = true; }
                        if (ImGui::SliderFloat("PITCH", &cam->camRot.x, -180.0f, 180.0f)) { changed = true; }
                        if (ImGui::SliderFloat("YAW", &cam->camRot.y, -180.0f, 180.0f)) { changed = true; }
                        if (ImGui::SliderFloat("CamRange", &cam->camRange, 0.10f, 10.0f)) { changed = true; }
                       


               
            ImGui::EndChild();
        }
		}

	

	
		ImGui::End();



	}

    ImGui::End();
    ImGui::Render();
}


void updateCamera()
{
    // Declare pointcloud object, for calculating pointclouds and texture mappings
    rs2::pointcloud pc;
    // We want the points object to be persistent so we can display the last cloud when a frame drops
    rs2::points points;

    // get LIVE camera
    auto cam = getScene()->cameras[0];

    {
        // Wait for the next set of frames from the camera
        auto frames = pipe.wait_for_frames();

        auto color = frames.get_color_frame();

        // Upload the color frame to OpenGL
        app_state.tex.upload(color);

        int w = color.get_width();
        int h = color.get_height();

        // For cameras that don't have RGB sensor, we'll map the pointcloud to infrared instead of color
        if (!color)
            color = frames.get_infrared_frame();

        // Tell pointcloud object to map to this color frame
        pc.map_to(color);

        auto depth = frames.get_depth_frame();

        // Generate the pointcloud and texture mappings
        points = pc.calculate(depth);



        auto vertices = points.get_vertices();              // get vertices
        auto tex_coords = points.get_texture_coordinates(); // and texture coordinates

        // init first time
        if (cam->vertices.size() == 0)
        {
          
            for (int i = 0; i < points.size(); i++)
            {
                cam->vertices.push_back(glm::vec3(0, 0, 0));
                cam->tex_coords.push_back(glm::vec3(0, 0, 0));
                cam->colors.push_back(glm::vec3(0, 0, 0));
            }
           
        }

        unsigned char* data = (unsigned char*)color.get_data();

        for (int i = 0; i < points.size(); i++)
        {
            int xi = tex_coords[i].u * w;
            int yi = tex_coords[i].v * h;

            if (tex_coords[i].u >= 0 && tex_coords[i].v >= 0 && tex_coords[i].u <= 1.0 && tex_coords[i].v <= 1.0)
            {
                int pi = yi * w * 3 + xi * 3;
                unsigned char r = data[pi + 0];
                unsigned char g = data[pi + 1];
                unsigned char b = data[pi + 2];
                cam->colors[i] = glm::vec3(r, g, b);
            }
            cam->vertices[i] = glm::vec3(vertices[i].x, vertices[i].y, vertices[i].z);
            cam->tex_coords[i] = glm::vec3(tex_coords[i].u, tex_coords[i].v, 0.0);

        }


        tex = app_state.tex;

    }
}
int main(int argc, char* argv[]) try
{
    /////////////////////////////////////////////////////

    
    // Create a simple OpenGL window for rendering:
    window app(1280, 720, "Papamon - 3D Viewer");
    ImGui_ImplGlfw_Init(app, false);
    // Setup Platform/Renderer bindings


    // register callbacks to allow manipulation of the pointcloud
    register_glfw_callbacks(app, app_state);

    // Declare pointcloud object, for calculating pointclouds and texture mappings
    rs2::pointcloud pc;
    // We want the points object to be persistent so we can display the last cloud when a frame drops
    rs2::points points;

   
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


        updateCamera();

       
        
        // Draw the pointcloud
        drawScene(app.width(), app.height());

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
