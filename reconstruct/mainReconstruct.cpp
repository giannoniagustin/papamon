// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <algorithm>            // std::min, std::max

#ifdef RENDER3D
#include "example.hpp"          // Include short list of convenience functions for rendering

#include <imgui.h>
#include "imgui_impl_glfw.h"
#endif

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
#ifdef RENDER3D
glfw_state app_state;

texture tex;
#endif

// Declare RealSense pipeline, encapsulating the actual device and sensors
rs2::pipeline pipe;
rs2::align align_to_depth(RS2_STREAM_DEPTH);
/// 
glm::mat4 UpdateModelMatrix(glm::vec3 Translation, glm::vec3 euler)
{
    glm::mat4 ModelMatrix = glm::mat4(1);
    

    ModelMatrix = glm::translate(ModelMatrix, Translation);
    glm::mat4 transform = glm::eulerAngleYXZ(euler.y*M_PI/180.0, euler.x * M_PI / 180.0, euler.z * M_PI / 180.0);

    return ModelMatrix * transform;
}



//////////////////////////////////
object3D mergeAll3DData()
{
    object3D obj;

    for (auto cam : getScene()->cameras)
    {
        auto m = UpdateModelMatrix(cam->camPos, cam->camRot);

        /* this segment actually prints the pointcloud */
        for (int i = 0; i < cam->o.vertexes.size(); i++)
        {
            if (cam->o.vertexes[i].z>=0 && cam->o.vertexes[i].z< cam->camRange)
            {
                glm::vec4 v(cam->o.vertexes[i].x, cam->o.vertexes[i].y, cam->o.vertexes[i].z, 1.0);
                // apply matrix multiplication
                v = m * v;
               
                obj.vertexes.push_back(glm::vec3(v.x, v.y, -v.z));
                obj.tex_coords.push_back(glm::vec3(cam->o.tex_coords[i].x, cam->o.tex_coords[i].y,0.0));
                obj.colors.push_back(cam->o.colors[i]);
            }
        }
    }

    return obj;
}

#ifdef RENDER3D
// Helper functions
void register_glfw_callbacks(window& app, glfw_state& app_state);


void render_ui(float w, float h, object3D& o)
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
        if (ImGui::Button("save configuration"))
        {
            buildSceneJSON("cameras.json");
        }

        if (ImGui::Button("save to OBJ"))
        {
            saveAsObj(o, "/merged.obj");
        }
        float roomsizeX = getScene()->roomSize.x;
        float roomsizeY = getScene()->roomSize.y;
        float roomsizeZ = getScene()->roomSize.z;

        bool changed = false;
        if (ImGui::SliderFloat("RoomSizeX", &roomsizeX, 0.50f, 20.0f)) { changed = true; }
        if (ImGui::SliderFloat("RoomSizeY", &roomsizeY, 0.50f, 20.0f)) { changed = true; }
        if (ImGui::SliderFloat("RoomSizeZ", &roomsizeZ, 0.50f, 20.0f)) { changed = true; }

        if (changed) getScene()->roomSize = glm::vec3(roomsizeX, roomsizeY, roomsizeZ);

        ImGui::SliderFloat("ViewPosX", &getScene()->viewPos.x, -2.0f, 10.0f);
        ImGui::SliderFloat("ViewPosY", &getScene()->viewPos.y, -2.0f, 10.0f);
        ImGui::SliderFloat("ViewPosZ", &getScene()->viewPos.z, -2.0f, 10.0f);

        ImGui::SliderFloat("ViewRotX", &getScene()->viewRot.x, -180.0f, 180.0f);
        ImGui::SliderFloat("ViewRotY", &getScene()->viewRot.y, -180.0f, 180.0f);
        ImGui::SliderFloat("ViewRotZ", &getScene()->viewRot.z, -180.0f, 180.0f);
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
                        if (ImGui::SliderFloat("CamPosY", &cam->camPos.y, -2.0f, 10.0f)) { changed = true; }
                        if (ImGui::SliderFloat("CamPosZ", &cam->camPos.z, -2.0f, 10.0f)) { changed = true; }
                        if (ImGui::SliderFloat("PITCH", &cam->camRot.x, -180.0f, 180.0f)) { changed = true; }
                        if (ImGui::SliderFloat("YAW", &cam->camRot.y, -180.0f, 180.0f)) { changed = true; }
                        if (ImGui::SliderFloat("ROLL", &cam->camRot.z, -180.0f, 180.0f)) { changed = true; }
                        if (ImGui::SliderFloat("CamRange", &cam->camRange, 0.10f, 10.0f)) { changed = true; }
                       


               
            ImGui::EndChild();
        }
		}

	

	
		ImGui::End();



	}

    ImGui::End();
    ImGui::Render();

    for (auto cam : getScene()->cameras) cam->is_enabled = false;
    getScene()->cameras[getScene()->selectedCamera]->is_enabled = true;
}

#endif

void updateCamera(Camera* cam)
{
    // Declare pointcloud object, for calculating pointclouds and texture mappings
    rs2::pointcloud pc;
    // We want the points object to be persistent so we can display the last cloud when a frame drops
    rs2::points points;

    // get LIVE camera
    

    {
        // Wait for the next set of frames from the camera
        auto frames = pipe.wait_for_frames();

        auto color = frames.get_color_frame();

        // Align all frames to depth viewport
        frames = align_to_depth.process(frames);

#ifdef RENDER3D
        // Upload the color frame to OpenGL
        app_state.tex.upload(color);
#endif

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

        getOBJFromFrameSet(cam->o, color, points);

#ifdef RENDER3D
        tex = app_state.tex;
#endif

    }
}

void readDataFromFile(Camera* cam, std::string srcDir)
{
    std::cout << "Trying to read Vertexes info " << "\n";

    if (std::filesystem::exists(srcDir + "points.csv"))
    {
        cam->o = readFromCSV(srcDir + "points.csv");
    }
    else
    {
        std::cout << "File not found " << srcDir + "points.csv" << "\n";
    }
}

/// //////////////////////////////////////
/// //////////////////////////////////////

int main(int argc, char* argv[]) try
{
    /////////////////////////////////////////////////////
    std::cout << "Project Reconstruct 5Oct2023" << "\n";

    bool showOutput = false;
    std::string inputDir = "";
    bool useLiveCamera = false;

    if (argc > 1)
    {
        for (int i = 0; i < argc; i++)
        {
            if (std::string(argv[i]) == "-show")
            {
                showOutput = true;
            }


            if (std::string(argv[i]) == "-dir")
            {
                inputDir = argv[i + 1];
                std::cout << "Using path " << inputDir << "\n";
            }

            if (std::string(argv[i]) == "-live")
            {
                useLiveCamera = true;
            }
        }
    }

    if (showOutput)
    {

#ifdef RENDER3D
        try
        {
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

            initScene("cameras.json", true);

            Camera* live_cam = NULL;
            if (useLiveCamera)
            {
                live_cam = new Camera("live", "1");
                getScene()->cameras.push_back(live_cam);
     
            }

           
            readDataFromFile(getScene()->cameras[0], "D:/Proyects/Lifia/Releases/1/");
            readDataFromFile(getScene()->cameras[1], "D:/Proyects/Lifia/Releases/2/");

            while (app) // Application still alive?
            {
                float w = static_cast<float>(app.width());
                float h = static_cast<float>(app.height());

                if (live_cam)
                {
                    updateCamera(live_cam);
                }
                object3D o = mergeAll3DData();

                // render scene
                drawScene(o, getScene()->viewPos, getScene()->viewRot, true, tex.get_gl_handle(), w, h);
            
                // render ui
                render_ui(200, 200,o);

                o.vertexes.clear();
                o.tex_coords.clear();
                o.colors.clear();

            }
        }
        catch (const std::exception& e)
        {

            std::cout << "Failed to reconstruct scene" << e.what() << "\n";
            return false;
        }
#elif
    std::cout << "Visualization not supported" << "\n";
#endif
        return EXIT_SUCCESS;
    }
    else
    {
        try
        {
            initScene("case_Sample0.json", true);

            // read data from camera
            std::cout << "Getting 3D points from files \n";
            for (auto cam : getScene()->cameras)
            {
                readDataFromFile(cam, inputDir);
            }

            std::cout << "Merge points  \n";
            object3D o = mergeAll3DData();


            std::cout << "Save as OBJ  \n";
            saveAsObj(o, inputDir + "/merged.obj");
        }
        catch (const std::exception& e)
        {

            std::cout << "Failed to reconstruct scene" << e.what() << "\n";
            return false;
        }

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
