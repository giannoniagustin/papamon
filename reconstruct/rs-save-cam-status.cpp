// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams

#include <map>

#include <filesystem>

// 3rd party header for writing png files
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
#include "utils.h"

#ifdef RENDER3D
#include "example.hpp"          // Include short list of convenience functions for rendering
#include <algorithm>            // std::min, std::max
// Helper functions
void register_glfw_callbacks(window& app, glfw_state& app_state);
#endif


class imageData
{
public:
    int w, h;
    unsigned char* data = NULL;
    int bytes_per_pixel;
    int stride_data;

};

////////////////////////////
// GLOBAL VARS

// Declare depth colorizer for pretty visualization of depth data
rs2::colorizer color_map;

// Declare pointcloud object, for calculating pointclouds and texture mappings
rs2::pointcloud pc;
// We want the points object to be persistent so we can display the last cloud when a frame drops
rs2::points points;

// Declare RealSense pipeline, encapsulating the actual device and sensors
rs2::pipeline pipe;

// Declare filters
rs2::decimation_filter dec_filter;  // Decimation - reduces depth frame density
rs2::threshold_filter thr_filter;   // Threshold  - removes values outside recommended range
rs2::spatial_filter spat_filter;    // Spatial    - edge-preserving spatial smoothing
rs2::temporal_filter temp_filter;   // Temporal   - reduces temporal noise
rs2::align align_to_depth(RS2_STREAM_DEPTH);


// Declaring two concurrent queues that will be used to enqueue and dequeue frames from different threads
rs2::frame_queue original_data;
rs2::frame_queue filtered_data;

// Initialize a vector that holds filters and their options
std::map<std::string, rs2::filter* > filters;
imageData* filtered_depth = NULL;
imageData* color_frame = NULL;

object3D o;



///
void setImageDataDepth(imageData* iD, rs2::depth_frame f)
{
    iD->w = f.get_width();
    iD->h = f.get_height();
    iD->bytes_per_pixel = f.get_bits_per_pixel();
    iD->stride_data = f.get_stride_in_bytes();

    unsigned char* data = (unsigned char*)f.get_data();
    int dataSize = f.get_data_size();

    if (iD->data == NULL)
    {
       iD->data = new unsigned char[dataSize];     
    }

    for (int i = 0; i < dataSize; i++)
        iD->data[i] = data[i];
}
///////////////////////////////////////////////////////////////////
void setImageDataColor(imageData* iD, rs2::video_frame f)
{
    iD->w = f.get_width();
    iD->h = f.get_height();
    iD->bytes_per_pixel = f.get_bits_per_pixel();
    iD->stride_data = f.get_stride_in_bytes();

    unsigned char* data = (unsigned char*)f.get_data();
    int dataSize = f.get_data_size();

    if (iD->data == NULL)
    {
        iD->data = new unsigned char[dataSize];
    }

    for (int i = 0; i < dataSize; i++)
        iD->data[i] = data[i];
}

/////////////////////////////////////////////////////////////////////////


// This sample captures 30 frames and writes the last frame to disk.
// It can be useful for debugging an embedded system with no display.
int main(int argc, char* argv[]) try
{
    std::cout << "Project PapaMon 24Oct2023" << "\n";

    bool demoMode = false;

    std::string instanceID = "0";

   
    std::string outputDir = "";

    bool showOutput = false;
    if (argc > 1)
    {
        for (int i = 0; i < argc; i++)
        {
            if (std::string(argv[i]) == "-show")
            {
                showOutput = true;
            }

            if (std::string(argv[i]) == "-demo")
            {
                demoMode = true;
            }

            if (std::string(argv[i]) == "-dir")
            {
                outputDir = argv[i+1];
                std::cout << "Using path " << outputDir << "\n";
            }

            if (std::string(argv[i]) == "-id")
            {
                instanceID = argv[i + 1];
                std::cout << "Setting ID " << instanceID << "\n";
            }


        }
    }

    if (demoMode)
    {
        std::cout << "Executing in demo mode" << "\n";

        
        std::string destination = outputDir;
        std::filesystem::path sourceFileRGB = "./demo/"+ instanceID +"/rgb.png";
        std::filesystem::path sourceFileDEPTH = "./demo/" + instanceID + "/depth.png";
        std::filesystem::path sourceFilePOINTS = "./demo/" + instanceID + "/points.csv";

        if (!std::filesystem::exists(sourceFileRGB) || !std::filesystem::exists(sourceFileDEPTH) || !std::filesystem::exists(sourceFilePOINTS))
        {
            std::cout << "Source files for demo " << sourceFileRGB << " were not found. Now EXIT" << "\n";
            return -1;
        }

        std::filesystem::path targetParent = destination + "/" + instanceID + "/";
        auto targetRGB = targetParent / sourceFileRGB.filename();
        auto targetDEPTH = targetParent / sourceFileDEPTH.filename();
        auto targetPOINTS = targetParent / sourceFilePOINTS.filename();

        try
        {
            std::filesystem::create_directories(targetParent); // Recursively create the target directory path if it does not exist.
            std::filesystem::copy_file(sourceFileRGB, targetRGB, std::filesystem::copy_options::overwrite_existing);
            std::filesystem::copy_file(sourceFileDEPTH, targetDEPTH, std::filesystem::copy_options::overwrite_existing);
            std::filesystem::copy_file(sourceFilePOINTS, targetPOINTS, std::filesystem::copy_options::overwrite_existing);

        }
        catch (std::exception& e) //If any filesystem error
        {
            std::cout << e.what();
        }


        if (std::filesystem::exists(targetRGB) && std::filesystem::exists(targetDEPTH) && std::filesystem::exists(targetPOINTS))
        {
            std::cout <<  " Files were create OK. Now EXIT" << "\n";
            return 1;
        }
        else
        {
            std::cout << " One of the files could not be created. Now EXIT" << "\n";
            return -1;
        }


    }

     
    try
    {
        std::filesystem::create_directories(outputDir); // Recursively create the target directory path if it does not exist.
     
    }
    catch (std::exception& e) //If any filesystem error
    {
        std::cout << e.what();
    }

   
    // Start streaming with default recommended configuration
    pipe.start();


    // The following order of emplacement will dictate the orders in which filters are applied
    filters["Decimate"] = &dec_filter;
    filters["Threshold"] = &thr_filter;
    filters["Spatial"] = &spat_filter;
    filters["Temporal"] = &temp_filter;


    std::cout << "waiting for frames .." << "\n";
    // Capture 30 frames to give autoexposure, etc. a chance to settle
    for (auto i = 0; i < 30; ++i) pipe.wait_for_frames();

    std::cout << "Ready for capturing frames" << "\n";

   
  

    int maxFrames = 2000;

   
     // only process
    if (!showOutput)
    {
        try
        {
            // Wait for the next set of frames from the camera
            auto frames = pipe.wait_for_frames();

            // Align all frames to depth viewport
            frames = align_to_depth.process(frames);

            auto color = frames.get_color_frame();

            // For cameras that don't have RGB sensor, we'll map the pointcloud to infrared instead of color
            if (!color)
                color = frames.get_infrared_frame();

            int w = color.get_width();
            int h = color.get_height();

            std::cout << "Read color image. W" << w << " height " << h << "\n";

            // Tell pointcloud object to map to this color frame
            pc.map_to(color);

            auto depth = frames.get_depth_frame();

            int wd = depth.get_width();
            int hd = depth.get_height();

            std::cout << "Read depth image. W" << wd << " height " << hd << "\n";


            rs2::depth_frame filtered = depth; // Does not copy the frame, only adds a reference

            std::cout << "Try to apply filters " << "\n";

            for (auto filter : filters)
            {
                filtered = filter.second->process(filtered);

            }

            std::cout << "Aplyed filters OK " << "\n";


            points = pc.calculate(filtered);

            if (!filtered_depth) filtered_depth = new imageData();
            if (!color_frame) color_frame = new imageData();


            std::cout << "Try to fill structures " << "\n";

            // Convert data
            setImageDataDepth(filtered_depth, depth);

            setImageDataColor(color_frame, color);

            getOBJFromFrameSet(o, color, points);

            std::cout << "Structures ok " << "\n";


        }
        catch (std::exception e)
        {
            std::cout << e.what() << "\n";
        }

    }
    else
    {
#ifdef RENDER3D

        try
        { 
            // Create a simple OpenGL window for rendering:
            window app(1280, 720, "Papamon Viewer - 2023");
            // Construct an object to manage view state
            glfw_state app_state;
            // register callbacks to allow manipulation of the pointcloud
            register_glfw_callbacks(app, app_state);

            int frameIndex = 0;

            while (app) // Application still alive?
            {
                // Wait for the next set of frames from the camera
                auto frames = pipe.wait_for_frames();

                // Align all frames to depth viewport
                frames = align_to_depth.process(frames);

                auto color = frames.get_color_frame();

                // For cameras that don't have RGB sensor, we'll map the pointcloud to infrared instead of color
                if (!color)
                    color = frames.get_infrared_frame();

                int w = color.get_width();
                int h = color.get_height();

                std::cout << "Read color image. W" << w << " height " << h << "\n";

                // Tell pointcloud object to map to this color frame
                pc.map_to(color);

                auto depth = frames.get_depth_frame();

                int wd = depth.get_width();
                int hd = depth.get_height();

                std::cout << "Read depth image. W" << wd << " height " << hd << "\n";


                rs2::depth_frame filtered = depth; // Does not copy the frame, only adds a reference

                std::cout << "Try to apply filters " << "\n";

                for (auto filter : filters)
                {
                    filtered = filter.second->process(filtered);

                }

                std::cout << "Aplyed filters OK " << "\n";

             
                points = pc.calculate(filtered);
                
                if (!filtered_depth) filtered_depth = new imageData();
                if (!color_frame) color_frame = new imageData();


                std::cout << "Try to fill structures " << "\n";

                // Convert data
                setImageDataDepth(filtered_depth, depth);

                setImageDataColor(color_frame, color);

                getOBJFromFrameSet(o, color, points);

                std::cout << "Structures ok " << "\n";

                // Upload the color frame to OpenGL
                app_state.tex.upload(color);


                // Draw the pointcloud
                //draw_pointcloud(app.width(), app.height(), app_state, points);
                drawCloudPoint(o, (int)app.width(), (int)app.height());

                frameIndex++;

                if (frameIndex > maxFrames) break;
            }
            }
        catch (std::exception e)
        {
            std::cout << "Exception at render loop :" << e.what() << "\n";
        }


     
#else
        std::cout << "3d rendering not supported" << "\n";
#endif 
    }

  
    try
    {
        std::cout << "Preparing to save files " << "\n";

        // Write images to disk
        std::string png_file_rgb = outputDir + "/" + instanceID + "/rgb.png";

        std::string png_file_depth = outputDir + "/" + instanceID + "/depth.png";

        std::filesystem::create_directories(outputDir + "/" + instanceID + "/"); // Recursively create the target directory path if it does not exist.

        if (color_frame != NULL)
        {
            int wd = color_frame->w;
            int hd = color_frame->h;


            // SAVING RGB FILE
            stbi_write_png(png_file_rgb.c_str(), wd, hd,
                color_frame->bytes_per_pixel / 8, color_frame->data, color_frame->stride_data);
            std::cout << "Saved " << png_file_rgb.c_str() << std::endl;
        }
        else
        {
            std::cout << "Color frame could not be saved" << std::endl;
        }
        // SAVING DEPTH FILE
        if (filtered_depth != NULL)
        {
            stbi_write_png(png_file_depth.c_str(), filtered_depth->w, filtered_depth->h,
                filtered_depth->bytes_per_pixel / 8, filtered_depth->data, filtered_depth->stride_data);
            std::cout << "Saved " << png_file_depth.c_str() << std::endl;
        }

        if (points.get_data_size() > 0)
        {
            savePointsToCSV(o, outputDir + "/" + instanceID + "/points.csv");
            std::cout << "Saved points.csv " << std::endl;
        }
        else
        {
            std::cout << "Points file could not be saved" << std::endl;
        }

        return EXIT_SUCCESS;
    }
    catch (std::exception e)
    {
        std::cout << "Exception at render loop :" << e.what() << "\n";
    }

   
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
