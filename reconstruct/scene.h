#pragma once

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams
#include <vector>
#include <filesystem>

#include "glm/glm.hpp"


struct object3D
{
public:
	std::vector<glm::vec3> vertexes;
	std::vector<glm::vec3> tex_coords;
	std::vector<glm::vec3> colors;

	glm::vec3 min, max;
	void computeMinMax();

};



class Camera
{
public:
	std::string type,  serial, source;

	std::string name;
	int id;

	glm::vec3 camPos = { 0.0f  , 0.0f, 0.0f };
	glm::vec3 camRot = { 0.0f, 0.0f, 0.0f };

	bool is_enabled = false;
	bool is_visible = true;
	float camRange = 5.0;

	object3D o;

	Camera(std::string name, std::string serial);

};

class Scene
{
public:
	glm::vec3 roomSize = glm::vec3(7.4, 6.42, 3.0);
	glm::vec3 viewPos = glm::vec3(0,0,0);
	glm::vec3 viewRot = glm::vec3(0,0,0);

	std::vector<Camera*> cameras;
	std::vector<float> heightMap;
	bool renderHeightMap = true;
	// default resolution 10
	int hm = 10, wm = 10;
	int camerasID = 0;
	int selectedCameraIndex = 0;
	Camera* selectedCamera = NULL;

};


Scene* getScene();

bool initScene(std::string inputJSONFile, bool verbose);
void buildSceneJSON(std::string outputFile);

void buildStateJSON(std::string outputFile);
void drawCloudPoint(object3D& o, int width, int height);
void drawScene(object3D& o, glm::vec3 viewPos, glm::vec3 viewRot, bool renderSceneBox, unsigned int tex, int width, int height);
void drawCamera(Camera* cam);
void drawCube(glm::vec3 roomSize);

