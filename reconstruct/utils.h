#pragma once


#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams
#include <map>
#include <filesystem>

#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include "glm/glm.hpp"

#include "scene.h"

#ifdef OPENCV
#include <opencv2/core.hpp>   // Include OpenCV API
#include <opencv2/highgui.hpp>   // Include OpenCV API
#include <opencv2/imgcodecs.hpp>   // Include OpenCV API
#include <opencv2/imgproc.hpp>   // Include OpenCV API
#include "opencv2/videoio.hpp"
#include <opencv2/video.hpp>
#endif


#define WARNING_SOMEFILES_ARE_MISSING 1
#define PROCESS_OK 0
#define GENERAL_ERROR -1
#define INVALID_PATH -2
#define FILE_NOT_FOUND -3
#define CAMERA_NOT_FOUND -4
#define CAMERA_FAILED -5
#define RENDER_FAILED -6
#define SCENE_FAILED_TO_RECONSTRUCT -10



const std::map<int, std::string> list_of_messages = {
       {PROCESS_OK, "OK"},
        {WARNING_SOMEFILES_ARE_MISSING, "Warning : some files are missing"},
       {GENERAL_ERROR, "General error"},
         {INVALID_PATH, "Invalid path"},
           {FILE_NOT_FOUND, "File was not found"},
             {CAMERA_FAILED, "Camera could not return a valid image"},
                {RENDER_FAILED, "Render failed"},
       {SCENE_FAILED_TO_RECONSTRUCT, "Failed to reconstruct scene"}
};


glm::vec3 convertToEulerAngle(rs2_vector accel_data);

void savePointsToCSV(object3D& o,Camera* cam, std::string filename);

std::vector<glm::vec3> readPointsFromFile(std::string filename);


object3D readFromCSV(Camera* cam, std::string filename);

object3D readFromOBJ(std::string filename);

std::string str_toupper(std::string s);


void saveAsObj(object3D& o, std::string outputFile);

void getOBJFromFrameSet(object3D& o, rs2::video_frame& color,  rs2::points& points);

std::vector<float> bicubicInterpolation(std::vector<float>& inputHM, int w, int h, std::vector<float> mask);
void showHeightMapAsImage(std::vector<float>& inputHM, int w, int h, std::string name, bool asSeudoColor, double resize = 10.0);

void erode(std::vector<float>& inputHM, int w,  int h, int kernelSize);
void dilate(std::vector<float>& inputHM, int w, int h, int kernelSize);

bool prepareCameraParameters(rs2::config& cfg);
bool check_imu_is_supported_by_cam();


double _pointPolygonTest(std::vector<glm::vec2> _contour, glm::vec2 pt, bool measureDist);


#ifdef OPENCV
double _pointPolygonTest(std::vector<cv::Point> contour, cv::Point p, bool measureDist);
#endif

