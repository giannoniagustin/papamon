#pragma once

#include <fstream>              // File IO
#include <iostream>             // Terminal IO
#include <sstream>              // Stringstreams
#include <vector>
#include <filesystem>

#include "glm/glm.hpp"


#define M_PI 3.14156


struct object3D
{
public:
	std::vector<glm::vec4> vertexes;
	std::vector<glm::vec3> tex_coords;
	std::vector<glm::vec3> colors;

	glm::vec3 min, max;
	bool visible = true;
	void computeMinMax();

};

class Plane
{
public:
	glm::vec3 normal;
	float distance;
	bool enabled;

	Plane(glm::vec3 n, float d);
};

class Mark
{
public:
	bool enabled = true;

	float posX = 0;
	float posZ = 0;
	int indexX, indexZ;

	void calcIndex();
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
	float camRange = 12.0f;
	float minRange = 0.4f;
	bool use_for_reconstruction = true;

	bool pose_data_enabled = false;
	glm::vec3 pose_data = { 0.0f  , 0.0f, 0.0f };

	object3D o;

	Camera(std::string name, std::string serial);
	std::vector<glm::vec3> generatePolygonVisibleArea();

};

class Scene
{
public:
	glm::vec3 roomSize = glm::vec3(7.4, 6.42, 3.0);
	glm::vec3 viewPos = glm::vec3(0,0,0);
	glm::vec3 viewRot = glm::vec3(0,0,0);

	std::vector<Camera*> cameras;
	std::vector<float> heightMap;
	std::vector<float> raw_heightMap;
	bool renderHeightMap = true;
	// default resolution 20
	int heightMap_width = 20, heightMap_depth = 40;
	int camerasID = 0;
	int min_amounts_of_points = 5;
	int selectedCameraIndex = 0;
	Camera* selectedCamera = NULL;
	std::vector<Mark*> marks;
	bool colorEachCamera = false;
	int pointSize = 1;

	Scene();
	double getCellW();
	double getCellD();

};


Scene* getScene();

double computeVolumeBetweenMarkers();
double computeSurfaceBetweenMarkers();
double computeLinearDistance();
double computeLinearHDistance();
double computeLinearVDistance();
void computeMinMaxHeight(float& _min, float& _max);



bool initScene(std::string inputJSONFile, bool verbose);
void buildSceneJSON(std::string outputFile, std::string code_version);

void buildStateJSON(std::string outputFile);
void drawCloudPoint(object3D& o, int width, int height);
void drawScene(object3D& o, glm::vec3 viewPos, glm::vec3 viewRot, bool renderSceneBox, unsigned int tex, int width, int height);
void drawCamera(Camera* cam);
void drawCube(glm::vec3 roomSize);

