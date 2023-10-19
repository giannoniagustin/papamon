#pragma once


#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams

#include <filesystem>
#include "glm/glm.hpp"

#include "scene.h"

void savePointsToCSV(object3D& o, std::string filename);

std::vector<glm::vec3> readPointsFromFile(std::string filename);


object3D readFromCSV(std::string filename);

object3D readFromOBJ(std::string filename);

std::string str_toupper(std::string s);


void saveAsObj(object3D& o, std::string outputFile);

void getOBJFromFrameSet(object3D& o, rs2::video_frame& color,  rs2::points& points);
