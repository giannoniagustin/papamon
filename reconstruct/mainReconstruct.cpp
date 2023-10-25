// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <iostream>     // std::cout
#include <algorithm>    // std::transform
#include <vector>       // std::vector
#include <functional>   // std::plus
#include <cctype>

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

/// Wizard parameters
bool renderSceneBox = true;
int wizardStage = 0;
int nCameras = 0;
bool finishRender = false;

// Construct an object to manage view state
#ifdef RENDER3D
glfw_state app_state;

texture tex;
#endif

// Declare RealSense pipeline, encapsulating the actual device and sensors
rs2::pipeline pipe;
rs2::align align_to_depth(RS2_STREAM_DEPTH);

// Declare pointcloud object, for calculating pointclouds and texture mappings
rs2::pointcloud pc;
// We want the points object to be persistent so we can display the last cloud when a frame drops
rs2::points points;

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
        glm::vec3 rotAdapt = cam->camRot;
        rotAdapt.x = -rotAdapt.x;
        rotAdapt.z = rotAdapt.z + 180.0f;
        auto m = UpdateModelMatrix(cam->camPos, rotAdapt);

        /* this segment actually prints the pointcloud */
        for (int i = 0; i < cam->o.vertexes.size(); i++)
        {
            if (cam->o.vertexes[i].z>=0 && cam->o.vertexes[i].z< cam->camRange)
            {
                glm::vec4 v(cam->o.vertexes[i].x, cam->o.vertexes[i].y, cam->o.vertexes[i].z, 1.0);
                // apply matrix multiplication
                v = m * v;
               
                obj.vertexes.push_back(glm::vec3(v.x, v.y, v.z));
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

bool renderCameraParameters(Camera* cam, int wW, int wH)
{
    std::string s = cam->name;
    bool changed = false;

    ImGui::BeginChild(s.c_str(), ImVec2((float)wW, (float)wH), true, 0);
    {

        ImGui::Text(" CAMERA PARAMETERS ");

        ImGui::Checkbox("Visible", &cam->is_visible);
       
        if (ImGui::SliderFloat("CamPosX", &cam->camPos.x, -2.0f, 10.0f)) { changed = true; }
        if (ImGui::SliderFloat("CamPosY", &cam->camPos.y, -2.0f, 10.0f)) { changed = true; }
        if (ImGui::SliderFloat("CamPosZ", &cam->camPos.z, -2.0f, 10.0f)) { changed = true; }
        if (ImGui::SliderFloat("PITCH", &cam->camRot.x, -180.0f, 180.0f)) { changed = true; }
        if (ImGui::SliderFloat("YAW", &cam->camRot.y, -180.0f, 180.0f)) { changed = true; }
        if (ImGui::SliderFloat("ROLL", &cam->camRot.z, -180.0f, 180.0f)) { changed = true; }
        if (ImGui::SliderFloat("CamRange", &cam->camRange, 0.10f, 10.0f)) { changed = true; }




        ImGui::EndChild();
    }

    return changed;
}

bool renderSceneParameters()
{
    if (ImGui::Button("UpView"))
    {
        // initial position
        getScene()->viewRot.x = -90;
        getScene()->viewRot.y = -180;
        getScene()->viewRot.z = 0;

        getScene()->viewPos.x = getScene()->roomSize.x / 2;
        getScene()->viewPos.z = std::max(getScene()->roomSize.x, getScene()->roomSize.z);
        getScene()->viewPos.y = getScene()->roomSize.z / 2;
    }
    ImGui::SameLine();

    if (ImGui::Button("CamView"))
    {
        if (getScene()->selectedCamera)
        {
            // initial position
            getScene()->viewRot = getScene()->selectedCamera->camRot;         

            getScene()->viewPos = -getScene()->selectedCamera->camPos;
          
        }
    }

    float roomsizeX = getScene()->roomSize.x;
    float roomsizeY = getScene()->roomSize.y;
    float roomsizeZ = getScene()->roomSize.z;

    bool changed = false;
    if (ImGui::SliderFloat("RoomSizeX", &roomsizeX, 0.50f, 30.0f)) { changed = true; }
    if (ImGui::SliderFloat("RoomSizeY", &roomsizeY, 0.50f, 30.0f)) { changed = true; }
    if (ImGui::SliderFloat("RoomSizeZ", &roomsizeZ, 0.50f, 30.0f)) { changed = true; }

    if (changed) getScene()->roomSize = glm::vec3(roomsizeX, roomsizeY, roomsizeZ);


    ImGui::SliderInt("ResolutionX", &getScene()->hm, 2, 50);
    ImGui::SliderInt("ResolutionZ", &getScene()->wm, 2, 50);

    ImGui::Separator();
    ImGui::Separator();


    ImGui::SliderFloat("ViewPosX", &getScene()->viewPos.x, -20.0f, 20.0f);
    ImGui::SliderFloat("ViewPosY", &getScene()->viewPos.y, -20.0f, 20.0f);
    ImGui::SliderFloat("ViewPosZ", &getScene()->viewPos.z, -20.0f, 20.0f);

    ImGui::SliderFloat("ViewRotX", &getScene()->viewRot.x, -180.0f, 180.0f);
    ImGui::SliderFloat("ViewRotY", &getScene()->viewRot.y, -180.0f, 180.0f);
    ImGui::SliderFloat("ViewRotZ", &getScene()->viewRot.z, -180.0f, 180.0f);

    return true;
}
/// Common UI for configurating View
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
   

    // 2. Show a simple window that we create ourselves. We use a Begin/End pair to created a named window.
    ImGui::Begin("Configuration", nullptr, 0);
    {
        ImGui::Checkbox("RenderSceneBox", &renderSceneBox);
        ImGui::Checkbox("RenderHeightMap", &getScene()->renderHeightMap);
        if (ImGui::Button("save configuration"))
        {
            buildSceneJSON("cameras.json");
        }
        ImGui::SameLine();
        if (ImGui::Button("save to OBJ"))
        {
            saveAsObj(o, "/merged.obj");
        }

        ImGui::Separator();        ImGui::Separator();
        
        renderSceneParameters();

        ImGui::Separator();        ImGui::Separator();
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
                getScene()->selectedCamera = cam; 
                getScene()->selectedCameraIndex = index;
               
            }

            index++;
           
        }

        //for (auto cam :  getScene()->cameras)
        auto cam = getScene()->selectedCamera;
        if (cam)
        {
            renderCameraParameters(cam, 400, 280);
		}
	
		ImGui::End();



	}

    ImGui::Render();

    for (auto cam : getScene()->cameras) cam->is_enabled = false;

    if (getScene()->selectedCamera)   getScene()->selectedCamera->is_enabled = true;
}

/// Render UI for configurating View
void render_wizard_ui(float w, float h, object3D& o)
{
    // Flags for displaying ImGui window
    static const int flags = ImGuiWindowFlags_NoCollapse
        | ImGuiWindowFlags_NoScrollbar
        | ImGuiWindowFlags_NoSavedSettings
        | ImGuiWindowFlags_NoTitleBar
        | ImGuiWindowFlags_NoResize
        | ImGuiWindowFlags_NoMove;

    ImGui_ImplGlfw_NewFrame(1);

 
    ImGui::SetWindowFontScale(1.2f);

    ImGui::Begin("SCENE", nullptr,  0);
    renderSceneParameters();
    ImGui::End();

    ImGui::Begin("WIZARD", nullptr,  0);
    {
        ImGui::Checkbox("RenderSceneBox", &renderSceneBox);
        ImGui::Checkbox("RenderHeightMap", &getScene()->renderHeightMap);
        
        ImGui::Separator();

        for (int i=0;i<getScene()->cameras.size() + 2; i++)
        {
            ImGui::SameLine();
            std::string mess;

            if (i == 0) mess = "Start";
            else if (i == getScene()->cameras.size() + 1) mess = "End";
            else mess = "cam" + std::to_string(i - 1);

            if (wizardStage == i)
            {               
                mess = str_toupper(mess);
            }
            
            if (ImGui::Button(mess.c_str()))
            {
                wizardStage = i;
            }
        }

        if (wizardStage == 0)
        {
            ImGui::BeginChild("end", ImVec2(350, 250), true, 0);

            ImGui::InputInt("#cameras", &nCameras);

           
            ImGui::SameLine();
            if (ImGui::Button("OK"))
            {
                getScene()->cameras.clear();
                for (int i = 0; i < nCameras; i++)
                {
                    getScene()->cameras.push_back(new Camera("cam" + std::to_string(i), ""));
                }
            }

            ImGui::EndChild();
        }
        else
        if (wizardStage == nCameras+1)
        {
            ImGui::BeginChild("end", ImVec2(350, 250), true, 0);
            {
                if (ImGui::Button("Save Cfg"))
                {
                    buildSceneJSON("cameras.json");
                }
                
                if (ImGui::Button("Finish"))
                {
                    finishRender = true;
                }
            }
            ImGui::EndChild();
        }
        else
        {
            getScene()->selectedCamera = getScene()->cameras[wizardStage - 1];
            renderCameraParameters(getScene()->selectedCamera,  350, 250);
        }

        ImGui::Separator();
        if (ImGui::Button("<<")) { wizardStage = std::max(wizardStage - 1, 0); } ImGui::SameLine();
        if (ImGui::Button(">>")) { wizardStage = std::min(wizardStage + 1, nCameras+2); } ImGui::SameLine();
       
     

    }
    ImGui::End();


    ImGui::Render();

    for (auto cam : getScene()->cameras) cam->is_enabled = false;

    if (getScene()->selectedCamera)   getScene()->selectedCamera->is_enabled = true;
}
#endif

//////////////////////////////////////////////////////////////////////////
std::vector<float> computeHeightMap(object3D& o,int wm, int hm)
{

    std::vector<float> values;

    o.computeMinMax();

    for (int i=0;i<wm*hm;i++)   values.push_back(0);

    for (int i = 0; i < o.vertexes.size(); i++)
    {
        int ix = (int)(wm * (o.vertexes[i].x ) / getScene()->roomSize.x);
        int iz = (int)(hm * (o.vertexes[i].z ) / getScene()->roomSize.z);

        if (ix >= 0 && iz >= 0 && ix < wm && iz < hm)
        {
            values[iz * wm + ix] = std::max(0.0f, std::max(values[iz * wm + ix], o.vertexes[i].y));
        }

    }

    return values;
}

bool updateCamera(Camera* cam)
{
    // get LIVE camera
    try
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
        return true;

    }
    catch (const std::exception& e)
    {

        std::cout << list_of_messages.find(CAMERA_FAILED)->second << e.what() << "\n";

        return false;
    }
}

bool readDataFromFile(Camera* cam, std::string srcDir)
{
    std::cout << "Trying to read Vertexes info " << "\n";

    if (std::filesystem::exists(srcDir + "points.csv"))
    {
        cam->o = readFromCSV(srcDir + "points.csv");
        return true;
    }
    else
    {
        std::cout << "File not found " << srcDir + "points.csv" << "\n";
        return false;
    }
}

/// //////////////////////////////////////
bool Wizard(std::string inputDir)
{
#ifdef RENDER3D
    // Create a simple OpenGL window for rendering:
    try
    {
        window app(1280, 720, "Papamon - 3D Viewer");
        ImGui_ImplGlfw_Init(app, false);
        // Setup Platform/Renderer bindings

        // register callbacks to allow manipulation of the pointcloud
        register_glfw_callbacks(app, app_state);

        // Start streaming with default recommended configuration
        pipe.start();

        getScene()->cameras.clear();

        getScene()->renderHeightMap = false;

    
        Camera* live_cam = NULL;
        int frameIndex = 0;

        // initial position
        getScene()->viewRot.x = -90;
        getScene()->viewRot.y = -180;
        getScene()->viewRot.z = 0;

        getScene()->viewPos.x = getScene()->roomSize.x/2;
        getScene()->viewPos.z = 10;
        getScene()->viewPos.y = getScene()->roomSize.z/2;
    
   

        while (app && !finishRender) // Application still alive?
        {


            float w = static_cast<float>(app.width());
            float h = static_cast<float>(app.height());

            if (getScene()->selectedCamera != NULL)
            {
                live_cam = getScene()->selectedCamera;
                updateCamera(live_cam);
            }
            object3D o = mergeAll3DData();

            std::vector<float> heights = computeHeightMap(o, getScene()->hm, getScene()->wm);

            getScene()->heightMap.swap(heights);

            // render scene
            drawScene(o, getScene()->viewPos, getScene()->viewRot, true, 0, (int)w, (int)h);

            // render ui
            render_wizard_ui(200, 200, o);

            o.vertexes.clear();
            o.tex_coords.clear();
            o.colors.clear();

            frameIndex++;

        }

        return true;
    }
    catch (const std::exception& e)
    {

        std::cout << list_of_messages.find(RENDER_FAILED)->second << e.what() << "\n";

        return false;
    }
#else
    std::cout << "Not compiled with RENDER 3D mode" << "\n";
#endif
}


bool Configurator(bool useLiveCamera, std::string inputDir)
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

        // Start streaming with default recommended configuration
        pipe.start();

        Camera* live_cam = NULL;
        if (useLiveCamera)
        {
            live_cam = new Camera("live", "1");
            getScene()->cameras.push_back(live_cam);

        }


        int frameIndex = 0;

        try
        {
            while (app && !finishRender) // Application still alive?
            {
                float w = static_cast<float>(app.width());
                float h = static_cast<float>(app.height());

                if (live_cam)
                {
                    updateCamera(live_cam);
                }
                object3D o = mergeAll3DData();

                std::vector<float> heights = computeHeightMap(o, getScene()->hm, getScene()->wm);

                getScene()->heightMap.swap(heights);

                // render scene
                drawScene(o, getScene()->viewPos, getScene()->viewRot, true, 0, (int)w, (int)h);

                // render ui
                render_ui(200, 200, o);

                if (frameIndex % 100 == 0)
                {
                    saveAsObj(o, inputDir + "/merged.obj");
                    buildStateJSON(inputDir + "/reconstruction.json");
                }

                o.vertexes.clear();
                o.tex_coords.clear();
                o.colors.clear();

                frameIndex++;

            }
        }
        catch (const std::exception& e)
        {

            std::cout << list_of_messages.find(RENDER_FAILED)->second << e.what() << "\n";

            return false;
        }

        return true;
    }
    catch (const std::exception& e)
    {

        std::cout << list_of_messages.find(SCENE_FAILED_TO_RECONSTRUCT)->second << e.what() << "\n";

        return false;
    }
#else
    std::cout << "Configurator : Not compiled with RENDER 3D mode" << "\n";
#endif
}
/// //////////////////////////////////////
/// 

bool Reconstruct(std::string inputDir)
{
    try
    {
        // read data from camera
        std::cout << "Merge points  \n";
        object3D o = mergeAll3DData();

        std::cout << "Compute Heightmap  \n";

        std::vector<float> heights = computeHeightMap(o, getScene()->hm, getScene()->wm);

        getScene()->heightMap.swap(heights);

        std::cout << "Save as OBJ  \n";
        saveAsObj(o, inputDir + "merged.obj");

        std::cout << "Save STATE  \n";
        buildStateJSON(inputDir + "reconstruction.json");

        std::cout << "Process finish ok \n";

        return true;

    }
    catch (const std::exception& e)
    {
        std::cout << list_of_messages.find(SCENE_FAILED_TO_RECONSTRUCT)->second << e.what() << "\n";
      
        return false;
    }
}


int main(int argc, char* argv[]) try
{
    /////////////////////////////////////////////////////
    std::cout << "Project Reconstruct 24Oct2023" << "\n";

    bool showOutput = false;
    std::string inputDir = "";
    bool useLiveCamera = false;
    bool runWizard = false;
    bool verbose = false;

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


            if (std::string(argv[i]) == "-wizard")
            {
                runWizard = true;
            }

            if (std::string(argv[i]) == "-verbose")
            {
                verbose = true;
            }
        }
    }

    // Load scene
    try
    {
        std::cout << "Reading cameras info " << "\n";

        if (!std::filesystem::exists("cameras.json"))
        {
            std::cout << list_of_messages.find(FILE_NOT_FOUND)->second << ". Cameras.json not found . Now eXIT " "\n";
          
            return FILE_NOT_FOUND;
        }

        initScene("cameras.json", verbose);
        std::cout << "Camera info  read OK" << "\n";

        std::cout << "Getting 3D points from files \n";
        for (int i = 0; i < getScene()->cameras.size(); i++)
        {
            if (!readDataFromFile(getScene()->cameras[i], inputDir + "/" + std::to_string(i + 1) + "/"))
            {
                std::cout << list_of_messages.find(WARNING_SOMEFILES_ARE_MISSING)->second  << "\n";
           }
        }

        std::cout << "3D points info  read OK" << "\n";

        getScene()->hm = 10;
        getScene()->wm = 10;
    }
    catch (const std::exception& e)
    {

        std::cout << list_of_messages.find(SCENE_FAILED_TO_RECONSTRUCT)->second << e.what() << "\n";
        return false;
    }

    /// Run different modes
    if (runWizard)
    {
        std::cout << "RUNNING IN WIZARD MODE " << "\n";
        Wizard(inputDir);
    }
    else
    if (showOutput)
    {

#ifdef RENDER3D
        std::cout << "RUNNING IN ONLINE CONFIGURATION MODE " << "\n";
        Configurator(useLiveCamera, inputDir);
#else
    std::cout << "Visualization not supported" << "\n";
#endif
        
    }
    else
    {
        std::cout << "RUNNING RECONSTRUCTION WITHOUT UI " << "\n";
        Reconstruct(inputDir);
    }

return PROCESS_OK;
}
catch (const rs2::error& e) 
{
    std::cerr << "RealSense error calling " << e.get_failed_function() << "(" << e.get_failed_args() << "):\n    " << e.what() << std::endl;
    return GENERAL_ERROR;
}
catch (const std::exception& e)
{
    std::cerr << e.what() << std::endl;
    return GENERAL_ERROR;
}
