#pragma once


#include <librealsense2/rs.hpp> // Include RealSense Cross Platform API

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams

#include <filesystem>
#include "glm/glm.hpp"


void savePointsToCSV(rs2::points& points, std::string filename);

std::vector<glm::vec3> readPointsFromFile(std::string filename);