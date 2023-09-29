// License: Apache 2.0. See LICENSE file in root directory.
// Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams

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



// This sample captures 30 frames and writes the last frame to disk.
// It can be useful for debugging an embedded system with no display.
int main(int argc, char* argv[]) try
{
    std::cout << "Project PapaMon 27Sep2023" << "\n";

    bool showOutput = false;
    if (argc > 1)
    {
        for (int i = 0; i < argc; i++)
        {
            if (std::string(argv[i]) == "-show")
            {
                showOutput = true;
            }
        }
    }

    // Declare depth colorizer for pretty visualization of depth data
    rs2::colorizer color_map;

    // Declare pointcloud object, for calculating pointclouds and texture mappings
    rs2::pointcloud pc;
    // We want the points object to be persistent so we can display the last cloud when a frame drops
    rs2::points points;

    // Declare RealSense pipeline, encapsulating the actual device and sensors
    rs2::pipeline pipe;
    // Start streaming with default recommended configuration
    pipe.start();

    // Declare filters
    rs2::decimation_filter dec_filter;  // Decimation - reduces depth frame density
    rs2::threshold_filter thr_filter;   // Threshold  - removes values outside recommended range
    rs2::spatial_filter spat_filter;    // Spatial    - edge-preserving spatial smoothing
    rs2::temporal_filter temp_filter;   // Temporal   - reduces temporal noise

  
    
    // Declaring two concurrent queues that will be used to enqueue and dequeue frames from different threads
    rs2::frame_queue original_data;
    rs2::frame_queue filtered_data;

    // Initialize a vector that holds filters and their options
    std::map<std::string, rs2::filter* > filters;

    // The following order of emplacement will dictate the orders in which filters are applied
    filters["Decimate"] = &dec_filter;
    filters["Threshold"] = &thr_filter;
    filters["Spatial"] = &spat_filter;
    filters["Temporal"] = &temp_filter;


#ifdef RENDER3D
    // Create a simple OpenGL window for rendering:
    window app(1280, 720, "Papamon Viewer - 2023");
    // Construct an object to manage view state
    glfw_state app_state;
    // register callbacks to allow manipulation of the pointcloud
    register_glfw_callbacks(app, app_state);
#endif

    // Capture 30 frames to give autoexposure, etc. a chance to settle
    for (auto i = 0; i < 30; ++i) pipe.wait_for_frames();

    std::string outputDir = "";
    rs2::depth_frame* filtered_depth = NULL;
    rs2::video_frame* color_frame = NULL;

    if (!showOutput)
    {
        // Wait for the next set of frames from the camera. Now that autoexposure, etc.
        // has settled, we will write these to disk
        auto frames = pipe.wait_for_frames();

        auto color = frames.get_color_frame();

        auto depth = frames.get_depth_frame();
        auto depth_color = color_map.process(depth);

        rs2::frame filtered = depth; // Does not copy the frame, only adds a reference

        for (auto filter : filters)
        {
            filtered = filter.second->process(filtered);
            
        }

        // Generate the pointcloud and texture mappings
        filtered_depth = static_cast<rs2::depth_frame*>(&filtered);
        color_frame = static_cast<rs2::video_frame*>(&color);
        points = pc.calculate(filtered);


    }
    else
    {
#ifdef RENDER3D
        int frameIndex = 0;

        while (app) // Application still alive?
        {
            // Wait for the next set of frames from the camera
            auto frames = pipe.wait_for_frames();

            auto color = frames.get_color_frame();

            // For cameras that don't have RGB sensor, we'll map the pointcloud to infrared instead of color
            if (!color)
                color = frames.get_infrared_frame();

            // Tell pointcloud object to map to this color frame
            pc.map_to(color);

            auto depth = frames.get_depth_frame();

            rs2::frame filtered = depth; // Does not copy the frame, only adds a reference

            for (auto filter : filters)
            {
                filtered = filter.second->process(filtered);

            }


            // Generate the pointcloud and texture mappings
            filtered_depth = static_cast<rs2::depth_frame*>(&filtered);
            color_frame = static_cast<rs2::video_frame*>(&color);
            points = pc.calculate(filtered);


            // Upload the color frame to OpenGL
            app_state.tex.upload(color);

            // Draw the pointcloud
            draw_pointcloud(app.width(), app.height(), app_state, points);

            frameIndex++;

            if (frameIndex > 100) break;
        }

        // Write images to disk
        std::string png_file_rgb = outputDir +"rs-save-to-disk-output-rgb.png";
        std::string png_file_depth_color = outputDir + "rs-save-to-disk-output-depth_color.png";
        std::string png_file_depth = outputDir +  "rs-save-to-disk-output-depth.png";

        if (color_frame != NULL)
        {
            // SAVING RGB FILE
            stbi_write_png(png_file_rgb.c_str(), color_frame->get_width(), color_frame->get_height(),
                color_frame->get_bytes_per_pixel(), color_frame->get_data(), color_frame->get_stride_in_bytes());
            std::cout << "Saved " << png_file_rgb.c_str() << std::endl;
        }
        else
        {
            std::cout << "Color frame could not be saved" << std::endl;
        }
        // SAVING DEPTH FILE
        if (color_frame != NULL)
        {
            stbi_write_png(png_file_depth.c_str(), filtered_depth->get_width(), filtered_depth->get_height(),
                filtered_depth->get_bytes_per_pixel(), filtered_depth->get_data(), filtered_depth->get_stride_in_bytes());
            std::cout << "Saved " << png_file_depth_color.c_str() << std::endl;
        }

        if (points.get_data_size() > 0)
        {
            savePointsToCSV(points, outputDir + "/points.csv");
            std::cout << "Saved points.csv " << std::endl;
        }
        else
        {
            std::cout << "Points file could not be saved" << std::endl;
        }
        
#else
        std::cout << "3d rendering not supported" << "\n";
#endif 
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
