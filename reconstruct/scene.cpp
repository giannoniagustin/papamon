#include <filesystem>
#define GL_SILENCE_DEPRECATION
#define GLFW_INCLUDE_GLU
#include <GLFW/glfw3.h>

#include <algorithm>            // std::min, std::max
#include <array>

#include "scene.h"
#include "glm/glm.hpp"

#include "glm/gtc/matrix_transform.hpp"
#include "glm/gtx/euler_angles.hpp"



#include "rapidjson/document.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/prettywriter.h"
#include "rapidjson/filereadstream.h"
#include "rapidjson/filewritestream.h"


static std::vector<std::string> kTypeNames = { "Null", "False", "True", "Object", "Array", "String", "Number" };


rapidjson::Document readGeoJSON(const std::string& path, bool use_convert)
{
	FILE* fp = fopen(path.c_str(), "rb"); // non-Windows use "r"

	char readBuffer[65536];
	rapidjson::FileReadStream is(fp, readBuffer, sizeof(readBuffer));

	rapidjson::Document d;
	d.ParseStream(is);
	fclose(fp);

	return d;

}

#define M_PI 3.14156
Scene* _sceneInstance = NULL;

Scene* getScene()
{
	if (!_sceneInstance) _sceneInstance = new Scene();

	return _sceneInstance;
}

///CLASS CAMERA
Camera::Camera(std::string name, std::string serial)
{
	this->name = name;
	this->serial = serial;
}


//// Parse a JSON with Scene Data	
void parseSceneData(rapidjson::Document& geoD,  bool verboseOut)
{

	// remove existante elements
	
	getScene()->cameras.clear();

	int procMask = 0;
	double imageWidth = 0;
	double imageHeight = 0;
	bool handAreContaminated = false;
	bool elemtsAreContaminated = false;

	if (!geoD.HasMember("info"))
	{
		std::cout << "Not found INFO member";
	}
	else
	{
		const rapidjson::Value& info = geoD["info"];

		if (verboseOut) std::cout << "Reading [info] section " << "\n";

		if (info.HasMember("width"))
		{
			auto fid = info.FindMember("width");
			if (verboseOut) std::cout << "width type:" << kTypeNames[fid->value.GetType()] << "\n";
			imageWidth = fid->value.GetInt();

		}

		if (info.HasMember("height"))
		{
			auto fid = info.FindMember("height");
			if (verboseOut) std::cout << "height type:" << kTypeNames[fid->value.GetType()] << "\n";
			imageHeight = fid->value.GetInt();

		}


	
	}

	//////////////////////
	// Scene information
	if (geoD.HasMember("cameras"))
	{
		const rapidjson::Value& camerasI = geoD["cameras"];

		if (verboseOut) std::cout << "Reading [cameras] section " << "\n";

		for (rapidjson::SizeType i = 0; i < camerasI.Size(); i++)
		{
			try
			{
				auto camera = camerasI[i].GetObject();

				Camera* cam = NULL;
				if (camera.HasMember("type"))
				{
					auto fid = camera.FindMember("type");
					auto fid2 = camera.FindMember("name");

					std::string types = fid->value.GetString();
					auto fSerial = camera.HasMember("serial");
					if (camera.HasMember("serial"))
						{
							if (verboseOut) std::cout << "Reading [realSense camera] with serial " << camera.FindMember("serial")->value.GetString() << "\n";
							
							cam = new Camera(fid2->value.GetString(), camera.FindMember("serial")->value.GetString());
						}
					
					// save this data
					if (camera.HasMember("type")) cam->type = camera.FindMember("type")->value.GetString();
					if (camera.HasMember("serial")) cam->serial = camera.FindMember("serial")->value.GetString();
					if (camera.HasMember("source")) cam->source = camera.FindMember("source")->value.GetString();

					
					
				}
				else
				{
					cam = new Camera("","");
				}


				if (camera.HasMember("name")) cam->name = camera.FindMember("name")->value.GetString();

				if (camera.HasMember("location"))
				{
					auto fid = camera.FindMember("location");
					if (verboseOut)  std::cout << "id type:" << kTypeNames[fid->value.GetType()] << "\n";
					auto coordsM = fid->value.GetArray();

					cam->camPos.x = coordsM[0].GetFloat();
					cam->camPos.y = coordsM[1].GetFloat();
					cam->camPos.z = coordsM[2].GetFloat();
				}

				if (camera.HasMember("range"))
				{
					auto fid = camera.FindMember("range");
					if (verboseOut) std::cout << "width type:" << kTypeNames[fid->value.GetType()] << "\n";
					cam->camRange = fid->value.GetFloat();
				}



				if (camera.HasMember("orientation"))
				{
					auto fid = camera.FindMember("orientation");
					if (verboseOut)  std::cout << "id type:" << kTypeNames[fid->value.GetType()] << "\n";
					auto coordsM = fid->value.GetArray();

					cam->camRot.x = coordsM[0].GetFloat();
					cam->camRot.y = coordsM[1].GetFloat();
					cam->camRot.z = coordsM[2].GetFloat();
				}

				getScene()->cameras.push_back(cam);
			}
			catch (std::exception ex)
			{
				std::cout << "Failed to read camera info " << ex.what() << "\n";
			}
		}
	}

	

	if (geoD.HasMember("scene"))
	{
		const rapidjson::Value& scene = geoD["scene"];

		if (verboseOut) std::cout << "Reading [scene] section " << "\n";

		if (scene.HasMember("scene_width"))
		{
			auto fid = scene.FindMember("scene_width");
			if (verboseOut) std::cout << "width type:" << kTypeNames[fid->value.GetType()] << "\n";
			getScene()->roomSize.x = fid->value.GetFloat();
		}



		if (scene.HasMember("scene_height"))
		{
			auto fid = scene.FindMember("scene_height");
			if (verboseOut) std::cout << "height type:" << kTypeNames[fid->value.GetType()] << "\n";
			getScene()->roomSize.y = fid->value.GetFloat();
		}

		if (scene.HasMember("scene_depth"))
		{
			auto fid = scene.FindMember("scene_depth");
			if (verboseOut) std::cout << "depth type:" << kTypeNames[fid->value.GetType()] << "\n";
			getScene()->roomSize.z = fid->value.GetFloat();
		}


		if (scene.HasMember("view_offset"))
		{
			auto fid = scene.FindMember("view_offset");
			if (verboseOut)  std::cout << "id type:" << kTypeNames[fid->value.GetType()] << "\n";
			auto coordsM = fid->value.GetArray();

			getScene()->viewPos.x = coordsM[0].GetFloat();
			getScene()->viewPos.y = coordsM[1].GetFloat();
			getScene()->viewPos.z = coordsM[2].GetFloat();
		}


		if (scene.HasMember("view_rotation"))
		{
			auto fid = scene.FindMember("view_rotation");
			if (verboseOut)  std::cout << "id type:" << kTypeNames[fid->value.GetType()] << "\n";
			auto coordsM = fid->value.GetArray();

			getScene()->viewRot.x = coordsM[0].GetFloat();
			getScene()->viewRot.y = coordsM[1].GetFloat();
			getScene()->viewRot.z = coordsM[2].GetFloat();
		}


	
	}


}

void object3D::computeMinMax()
{
	this->min = glm::vec3(10000, 10000, 10000);
	this->max = glm::vec3(-10000, -10000, -10000);

	for (int i = 0; i < this->vertexes.size(); i++)
	{
		this->min.x = std::min(this->min.x, this->vertexes[i].x-0.01f);
		this->min.y = std::min(this->min.y, this->vertexes[i].y - 0.01f);
		this->min.z = std::min(this->min.z, this->vertexes[i].z - 0.01f);

		this->max.x = std::max(this->max.x, this->vertexes[i].x+0.01f);
		this->max.y = std::max(this->max.y, this->vertexes[i].y + 0.01f);
		this->max.z = std::max(this->max.z, this->vertexes[i].z + 0.01f);

	}


}

////////////////////////////////////
////
bool initScene(std::string inputJSONFile,  bool verbose)
{
	std::cout << "Trying to init Scene data..." << "\n";
	try
	{
		if (std::filesystem::exists(inputJSONFile))
		{
			std::cout << "Init Scene data" << "\n";
			rapidjson::Document gdoc = readGeoJSON(inputJSONFile, true);

			std::cout << "Prepare to parse JSON " << "\n";
			parseSceneData(gdoc,  verbose);
			std::cout << "Scene data loaded OK." << getScene()->cameras.size() << " cameras " << "\n";
			return true;
		}
		else {
			std::cout << "File Scene not found: " << inputJSONFile << "\n";
			return false;
		}

	}
	catch (const std::exception& e)
	{

		std::cout << "Failed to load scene" << e.what() << "\n";
		return false;
	}

	return false;
}

////////////
rapidjson::Value vecToArray(glm::vec3 v, rapidjson::Document::AllocatorType& allocator)
{
	rapidjson::Value v_array(rapidjson::kArrayType);
	v_array.PushBack(rapidjson::Value(v.x), allocator);
	v_array.PushBack(rapidjson::Value(v.y), allocator);
	v_array.PushBack(rapidjson::Value(v.z), allocator);

	return v_array;
}


rapidjson::Value vecToArray(std::vector<float>& vs, rapidjson::Document::AllocatorType& allocator)
{
	rapidjson::Value v_array(rapidjson::kArrayType);
	for (auto v : vs)
		v_array.PushBack(rapidjson::Value(v), allocator);

	return v_array;
}


/// 
void buildSceneJSON(std::string outputFile)
{

	rapidjson::Document document;

	// define the document as an object rather than an array
	document.SetObject();


	// must pass an allocator when the object may need to allocate memory
	rapidjson::Document::AllocatorType& allocator = document.GetAllocator();

	// create a rapidjson object type
	rapidjson::Value info(rapidjson::kObjectType);
	info.AddMember("version", "50", allocator);
	document.AddMember("info", info, allocator);
	//  fromScratch["object"]["hello"] = "Yourname";


	// create a rapidjson object type
	rapidjson::Value scene(rapidjson::kObjectType);
	scene.AddMember("scene_width", getScene()->roomSize.x, allocator);
	scene.AddMember("scene_height", getScene()->roomSize.y, allocator);
	scene.AddMember("scene_depth", getScene()->roomSize.z, allocator);
	scene.AddMember("view_offset", vecToArray(getScene()->viewPos, allocator), allocator);
	scene.AddMember("view_rotation", vecToArray(getScene()->viewRot, allocator), allocator);
	document.AddMember("scene", scene, allocator);

	

	// chain methods as rapidjson provides a fluent interface when modifying its objects

	// create a rapidjson array type with similar syntax to std::vector
	rapidjson::Value cameras_array(rapidjson::kArrayType);
	
	for (auto cam : getScene()->cameras)
	{
		if (cam->name != "live")
		{
			rapidjson::Value camO(rapidjson::kObjectType);
			camO.AddMember("id", cam->id, allocator);
			camO.AddMember("range", cam->camRange, allocator);
			camO.AddMember("name",rapidjson::Value().SetString((char*)cam->name.c_str(), cam->name.length()), allocator);
			camO.AddMember("serial", rapidjson::Value().SetString((char*)cam->serial.c_str(), cam->serial.length()), allocator);
			camO.AddMember("location", vecToArray(cam->camPos, allocator), allocator);
			camO.AddMember("orientation", vecToArray(cam->camRot, allocator), allocator);

			cameras_array.PushBack(camO, allocator);
		}
	}
		
	document.AddMember("cameras", cameras_array, allocator);

	
	rapidjson::StringBuffer strbuf;
	rapidjson::Writer<rapidjson::StringBuffer> writer(strbuf);
	document.Accept(writer);

	std::ofstream file(outputFile);
	file << strbuf.GetString() << std::endl;

	file.close();

}

/// Create JSON with state of
void buildStateJSON(std::string outputFile)
{
	rapidjson::Document document;

	// define the document as an object rather than an array
	document.SetObject();


	// must pass an allocator when the object may need to allocate memory
	rapidjson::Document::AllocatorType& allocator = document.GetAllocator();


	int numActive_Cameras = getScene()->cameras.size();

	// create a rapidjson object type
	rapidjson::Value info(rapidjson::kObjectType);
	info.AddMember("date", "50", allocator);
	info.AddMember("active_cameras", numActive_Cameras, allocator);
	document.AddMember("info", info, allocator);
	//  fromScratch["object"]["hello"] = "Yourname";

	// create a rapidjson object type
	rapidjson::Value scene(rapidjson::kObjectType);
	scene.AddMember("heightMap_width", getScene()->hm, allocator);
	scene.AddMember("heightMap_depth", getScene()->wm, allocator);
	scene.AddMember("heightMap", vecToArray(getScene()->heightMap, allocator), allocator);
	document.AddMember("estimation", scene, allocator);



	rapidjson::StringBuffer strbuf;
	rapidjson::Writer<rapidjson::StringBuffer> writer(strbuf);
	document.Accept(writer);

	std::ofstream file(outputFile);
	file << strbuf.GetString() << std::endl;

	file.close();
}
#ifdef RENDER3D
void renderHeightMap(std::vector<float>& hs, int h, int w)
{
	glColor3f(1.0f, 1.0f, 1.0f);    // Color Blue

	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

	glPushMatrix();

	glScalef(getScene()->roomSize.x, 1.0, getScene()->roomSize.z);
	// Draw reference grid
	for (int i=0;i<h;i++)
		for (int j = 0; j < w; j++)
		{
			float height = 0; // hs[i * w + j];
			glBegin(GL_QUADS);
		
			glVertex3f((1.0*(j+1))/w,height, (1.0*i)/h);
			glVertex3f((1.0*j)/w, height, (1.0 * i) / h);
			glVertex3f((1.0 * j) / w, height, (1.0*(i+1))/h);
			glVertex3f((1.0 * (j + 1)) / w, height, (1.0 * (i + 1)) / h);

			glEnd();

		}
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
	glColor3f(0.5, 0.5, 0.5);
	for (int i = 0; i < h-1; i++)
		for (int j = 0; j < w-1; j++)
		{
			
			glBegin(GL_QUADS);

			glVertex3f((1.0 * (j + 1)) / w, hs[i * w + (j+1)], (1.0 * i) / h);
			glVertex3f((1.0 * j) / w, hs[i * w + (j )], (1.0 * i) / h);
			glVertex3f((1.0 * j) / w, hs[(i+1) * w + (j + 1)], (1.0 * (i + 1)) / h);
			glVertex3f((1.0 * (j + 1)) / w, hs[(i+1) * w + (j + 1)], (1.0 * (i + 1)) / h);

			glEnd();

		}

	glPopMatrix();
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

}

void drawAxes()
{

	glLineWidth(5.0f);
	glBegin(GL_LINES);
	// X
	glColor3f(1.0f, 0.0f, 0.0f);
	glVertex3f(0.0f, 0.0f, 0.0f);
	glVertex3f(50.0f, 0.0f, 0.0f);
	// Y
	glColor3f(0.0f, 1.0f, 0.0f);
	glVertex3f(0.0f, 0.0f, 0.0f);
	glVertex3f(0.0f, 50.0f, 0.0f);
	// Z
	glColor3f(0.0f, 0.0f, 1.0f);
	glVertex3f(0.0f, 0.0f, 0.0f);
	glVertex3f(0.0f, 0.0f, 50.0f);

	glEnd();
}

void drawCube(glm::vec3 roomSize)
{
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

	glPushMatrix();
	glTranslatef(0.0, 0.0, 0.0);

	glScalef(roomSize.x, roomSize.y, roomSize.z);

	glBegin(GL_QUADS);        // Draw The Cube Using quads

	glColor3f(1.0f, 1.0f, 1.0f);    // Color Blue
	glVertex3f(0.0f, 1.0f, 0.0f);    // Top Right Of The Quad (Top)
	glVertex3f(0.0f, 1.0f, -1.0f);    // Top Left Of The Quad (Top)
	glVertex3f(0.0f, 1.0f, 1.0f);    // Bottom Left Of The Quad (Top)
	glVertex3f(1.0f, 1.0f, 1.0f);    // Bottom Right Of The Quad (Top)
	
	glColor3f(1.0f, 0.5f, 0.0f);    // Color Orange
	glVertex3f(1.0f, 0.0f, 1.0f);    // Top Right Of The Quad (Bottom)
	glVertex3f(0.0f, 0.0f, 1.0f);    // Top Left Of The Quad (Bottom)
	glVertex3f(0.0f, 0.0f, 0.0f);    // Bottom Left Of The Quad (Bottom)
	glVertex3f(1.0f, 0.0f, 0.0f);    // Bottom Right Of The Quad (Bottom)
	
	glColor3f(1.0f, 0.0f, 0.0f);    // Color Red    
	glVertex3f(1.0f, 1.0f, 1.0f);    // Top Right Of The Quad (Front)
	glVertex3f(0.0f, 1.0f, 1.0f);    // Top Left Of The Quad (Front)
	glVertex3f(0.0f, 0.0f, 1.0f);    // Bottom Left Of The Quad (Front)
	glVertex3f(1.0f, 0.0f, 1.0f);    // Bottom Right Of The Quad (Front)
	
	glColor3f(1.0f, 1.0f, 0.0f);    // Color Yellow
	glVertex3f(1.0f, 0.0f, 0.0f);    // Top Right Of The Quad (Back)
	glVertex3f(0.0f, 0.0f, 0.0f);    // Top Left Of The Quad (Back)
	glVertex3f(0.0f, 1.0f, 0.0f);    // Bottom Left Of The Quad (Back)
	glVertex3f(1.0f, 1.0f, 0.0f);    // Bottom Right Of The Quad (Back)
	
	glColor3f(0.0f, 0.0f, 1.0f);    // Color Blue
	glVertex3f(0.0f, 1.0f, 1.0f);    // Top Right Of The Quad (Left)
	glVertex3f(0.0f, 1.0f, 0.0f);    // Top Left Of The Quad (Left)
	glVertex3f(0.0f, 0.0f, 0.0f);    // Bottom Left Of The Quad (Left)
	glVertex3f(0.0f, 0.0f, 1.0f);    // Bottom Right Of The Quad (Left)
	
	glColor3f(1.0f, 0.0f, 1.0f);    // Color Violet
	glVertex3f(1.0f, 1.0f, 0.0f);    // Top Right Of The Quad (Right)
	glVertex3f(1.0f, 1.0f, 1.0f);    // Top Left Of The Quad (Right)
	glVertex3f(1.0f, 0.0f, 1.0f);    // Bottom Left Of The Quad (Right)
	glVertex3f(1.0f, 0.0f, 0.0f);    // Bottom Right Of The Quad (Right)
	glEnd();            // End Drawing The Cube


	glPopMatrix();


	glColor3f(1.0f, 1.0f, 1.0f);    // Color Blue
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

}


void drawCamera(Camera *cam) 
{
	int i, j;

	double r = 0.05;
	int lats = 10, longs = 10;
	glm::vec3 camPos = cam->camPos;
		
	glm::vec3 camRot = cam->camRot;

	const float fov = 45.0f;

	glm::vec3 cameraPos = camPos;
	glm::vec3 cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);
	glm::vec3 cameraRight = glm::vec3(1.0f, 0.0f, 0.0f);
	glm::vec3 cameraForward = glm::normalize(glm::cross(cameraUp, cameraRight));

	// camara view add 180
	auto mY = glm::rotate(glm::mat4(1.0f), (cam->camRot.y+180.0f) * (float)(M_PI / 180.0f), glm::vec3(0.0f, 1.0f, 0.0f));
	auto mX = glm::rotate(glm::mat4(1.0f), cam->camRot.x * (float)(M_PI / 180.0f), glm::vec3(1.0f, 0.0f, 0.0f));

	cameraForward =  mY * mX * glm::vec4(cameraForward.x, cameraForward.y, cameraForward.z, 1.0f);

	glm::mat4 initialCameraProjection = glm::perspective(glm::radians(fov), (float)1.33f, 0.1f, cam->camRange);

	glm::mat4 initialCameraView = glm::lookAt(
		cameraPos,
		cameraPos + cameraForward,
		cameraUp);

	std::array<glm::vec3, 8> _cameraFrustumCornerVertices{
	{
		{ -1.0f, -1.0f, 1.0f }, { 1.0f, -1.0f, 1.0f }, { 1.0f, 1.0f, 1.0f }, { -1.0f, 1.0f, 1.0f },
		{ -1.0f, -1.0f, -1.0f }, { 1.0f, -1.0f, -1.0f }, { 1.0f, 1.0f, -1.0f }, { -1.0f, 1.0f, -1.0f },
	}
	};

	const auto proj = glm::inverse(initialCameraProjection * initialCameraView);

	std::array<glm::vec3, 8> _frustumVertices;

	std::transform(
		_cameraFrustumCornerVertices.begin(),
		_cameraFrustumCornerVertices.end(),
		_frustumVertices.begin(),
		[&](glm::vec3 p) {
			auto v = proj * glm::vec4(p, 1.0f);
			return glm::vec3(v) / v.w;
		}
	);

	std::vector<int> lines = { 0,1,0,2,3,1,3,2,4,5,4,6,7,5,7,6,0,4,1,5,3,7,2,6 };

	if (cam->is_enabled)
	{
		glColor3f(1.0f, 1.0f, 0.0f);
		glBegin(GL_LINES);

		for (int i = 0; i < lines.size(); i = i + 2)
		{
			glVertex3f(_frustumVertices[lines[i]].x, _frustumVertices[lines[i]].y, _frustumVertices[lines[i]].z);
			glVertex3f(_frustumVertices[lines[i + 1]].x, _frustumVertices[lines[i + 1]].y, _frustumVertices[lines[i + 1]].z);
		}
		glEnd();
	}
	else
	{
		glColor3f(1.0f, 1.0f, 1.0f);
	}
	glPushMatrix();

	// render circle
	glTranslatef(camPos.x, camPos.y, camPos.z);

	for (i = 0; i <= lats; i++) {
		double lat0 = M_PI * (-0.5 + (double)(i - 1) / lats);
		double z0 = sin(lat0);
		double zr0 = cos(lat0);

		double lat1 = M_PI * (-0.5 + (double)i / lats);
		double z1 = sin(lat1);
		double zr1 = cos(lat1);

		glBegin(GL_QUAD_STRIP);
		for (j = 0; j <= longs; j++) {
			double lng = 2 * M_PI * (double)(j - 1) / longs;
			double x = cos(lng);
			double y = sin(lng);

			glNormal3d(x * zr0, y * zr0, z0);
			glVertex3d(r * x * zr0, r * y * zr0, r * z0);
			glNormal3d(x * zr1, y * zr1, z1);
			glVertex3d(r * x * zr1, r * y * zr1, r * z1);
		}
		glEnd();
	}

	glPopMatrix();
}

void drawCloudPoint(object3D& o, int width, int height)
{
	// OpenGL commands that prep screen for the pointcloud
	glLoadIdentity();
	glPushAttrib(GL_ALL_ATTRIB_BITS);

	glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
	glClear(GL_DEPTH_BUFFER_BIT);


	glMatrixMode(GL_PROJECTION);
	glPushMatrix();
	gluPerspective(60.0, (1.0*width) / height, 0.01f, 50.0f);

	glMatrixMode(GL_MODELVIEW);
	glPushMatrix();
	gluLookAt(0, 0, 0, 0, 0, 1, 0, -1, 0);

	glTranslatef(0, 0, +0.5f + 2 * 0.05f);
	glRotated(15, 1, 0, 0);
	glRotated(15, 0, 1, 0);

	glTranslatef(0, 0, -0.5f);

	glColor3f(1.0, 1.0, 1.0);
	glEnable(GL_DEPTH_TEST);
	glPointSize(width / 640);
	
	glBegin(GL_POINTS);

	glm::mat4 m = glm::mat4(1);


	/* this segment actually prints the pointcloud */
	for (int i = 0; i < o.vertexes.size(); i++)
		{
			if (o.colors.size() > 0)
			{
				glColor3f(o.colors[i].x / 255.0, o.colors[i].y / 255.0, o.colors[i].z / 255.0);
			}
			else
				glTexCoord2f(o.tex_coords[i].x, o.tex_coords[i].y);

			glVertex3f(o.vertexes[i].x, o.vertexes[i].y, o.vertexes[i].z);

		}



	// OpenGL cleanup
	glEnd();
	glPopMatrix();
	glMatrixMode(GL_PROJECTION);
	glPopMatrix();
	glPopAttrib();

	glColor3f(1.0, 1.0, 1.0);

}

// Handles all the OpenGL calls needed to display the point cloud
void drawScene(object3D& o,glm::vec3 viewPos, glm::vec3 viewRot, bool renderSceneBox,unsigned int tex,int width, int height)
{


	// OpenGL commands that prep screen for the pointcloud
	glLoadIdentity();
	glPushAttrib(GL_ALL_ATTRIB_BITS);

	glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
	glClear(GL_DEPTH_BUFFER_BIT);


	glMatrixMode(GL_PROJECTION);
	glPushMatrix();
	gluPerspective(60, (1.0*width) / height, 0.01f, 50.0f);

	glMatrixMode(GL_MODELVIEW);
	glPushMatrix();
	gluLookAt(0, 0, 0, 0, 0, 1, 0, 1, 0);

	glTranslatef(viewPos.x, viewPos.y, viewPos.z);
	glRotated(viewRot.x, 1, 0, 0);
	glRotated(viewRot.y, 0, 1, 0);
	glRotated(viewRot.z, 0, 0, 1);
	glTranslatef(0, 0, -0.5f);

	drawAxes();

	glColor3f(1.0, 1.0, 1.0);
	glEnable(GL_DEPTH_TEST);
	if (renderSceneBox)
	{
		glLineWidth(2.0f);
		drawCube(getScene()->roomSize);
	}

	for (auto cam : getScene()->cameras)
	{
		
		glLineWidth(1.0f);
		
		if (cam->is_visible)
		{
			drawCamera(cam);
		}
	}

	glPointSize(width / 640);

	if (tex > 0)
	{
		glEnable(GL_TEXTURE_2D);
		glBindTexture(GL_TEXTURE_2D, tex);
		float tex_border_color[] = { 0.8f, 0.8f, 0.8f, 0.8f };
		glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, tex_border_color);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, 0x812F); // GL_CLAMP_TO_EDGE
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, 0x812F); // GL_CLAMP_TO_EDGE
	}

	glm::mat4 m = glm::mat4(1);
	
	glColor3f(1.0, 1.0, 1.0);

	if (getScene()->cameras.size() > 0)
	{
		glBegin(GL_POINTS);

		
		/* this segment actually prints the pointcloud */
		for (int i = 0; i < o.vertexes.size(); i++)
		{
			if (o.colors.size() > 0)
			{
				glColor3f(o.colors[i].x / 255.0, o.colors[i].y / 255.0, o.colors[i].z / 255.0);
			}
			else
				glTexCoord2f(o.tex_coords[i].x, o.tex_coords[i].y);

			glVertex3f(o.vertexes[i].x, o.vertexes[i].y, o.vertexes[i].z);

		}

		glEnd();

		o.vertexes.clear();
		o.tex_coords.clear();
		o.colors.clear();
	}
	glColor3f(1.0, 1.0, 1.0);

	if (getScene()->heightMap.size() > 0 && getScene()->renderHeightMap)
	{
		renderHeightMap(getScene()->heightMap, getScene()->wm, getScene()->hm);
	}

	// OpenGL cleanup
	
	glPopMatrix();
	glMatrixMode(GL_PROJECTION);
	glPopMatrix();
	glPopAttrib();

}
#endif
