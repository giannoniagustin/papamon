#pragma once

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams
#include <vector>
#include <filesystem>

#include "glm/glm.hpp"



class Camera
{
public:
	std::string camera_type,  camera_serial, camera_source;

	std::string name;

	glm::vec3 camPos = { 0.0f  , 0.0f, 0.0f };
	glm::vec3 camRot = { 0.0f, 0.0f, 0.0f };

	bool is_enabled = true;
	float camRange = 5.0;

	std::vector<glm::vec3> vertices;
	std::vector<glm::vec3> tex_coords;
	std::vector<glm::vec3> colors;

	Camera(std::string name, std::string serial);

};

class Scene
{
public:
	glm::vec3 roomSize = glm::vec3(7.4, 6.42, 3.0);
	std::vector<Camera*> cameras;
	int camerasID = 0;
	int selectedCamera = 0;

};


Scene* getScene();

bool initScene(std::string inputJSONFile, bool verbose);

