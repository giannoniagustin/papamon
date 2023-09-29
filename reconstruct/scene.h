#pragma once

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams
#include <vector>
#include <filesystem>

#include "glm/glm.hpp"


class Size2f
{
public:
	float width, height;

	Size2f(float w, float h) { this->width = w; this->height = h; }
};


class Camera
{
public:
	std::string camera_type,  camera_serial, camera_source;

	std::string name;

	glm::vec3 camPos = { 0.0f  , 0.0f, 0.0f };
	glm::vec3 camRot = { 0.0f, 0.0f, 0.0f };

	bool is_enabled = true;
	float camRange = 5.0;

	std::vector<glm::vec3> points;

	Camera(std::string src, std::string serial);

};

class Scene
{
public:
	Size2f roomSize = Size2f(7.4, 6.42);
	std::vector<Camera*> cameras;

};


Scene* getScene();

bool initScene(std::string inputJSONFile, bool verbose);

