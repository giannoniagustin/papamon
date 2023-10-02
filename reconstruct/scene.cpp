#include <filesystem>
#define GL_SILENCE_DEPRECATION
#define GLFW_INCLUDE_GLU
#include <GLFW/glfw3.h>


#include "scene.h"

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
	this->camera_serial = serial;
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
					if (camera.HasMember("type")) cam->camera_type = camera.FindMember("type")->value.GetString();
					if (camera.HasMember("serial")) cam->camera_serial = camera.FindMember("serial")->value.GetString();
					if (camera.HasMember("source")) cam->camera_source = camera.FindMember("source")->value.GetString();

					
					
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


		if (scene.HasMember("exclusion_zone"))
		{
			auto fid = scene.FindMember("exclusion_zone");
			if (verboseOut) std::cout << "exclusion_zone:" << kTypeNames[fid->value.GetType()] << "\n";

			auto coordsM = fid->value.GetArray();

		}
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