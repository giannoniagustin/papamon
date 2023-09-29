
#include "utils.h"
#include <string>       // std::string
#include <iostream>     // std::cout
#include <sstream>  

template<typename Out>
void splits(const std::string& s, char delim, Out result) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        *(result++) = item;
    }
}




std::vector<std::string> splitString(const std::string& s, char delim) {
    std::vector<std::string> elems;
    splits(s, delim, std::back_inserter(elems));
    return elems;
}


std::vector<glm::vec3> readPointsFromFile(std::string filename)
{
    /* this segment actually prints the pointcloud */
    std::ifstream inFile;
    inFile.open(filename);


    std::string line;

    std::vector<glm::vec3> points;

    while (!inFile.eof())

    {
        std::getline(inFile, line); // ommit first line

      

        // lat long
        std::vector<std::string> ss = splitString(line, '"');
        if (ss.size() < 5)
        {
           
            continue;
        }

        ///////////////////////////////////////
        glm::vec3 pos = glm::vec3(std::stof(ss[0]), std::stof(ss[1]), std::stof(ss[2]));

        points.push_back(pos);
    }

    inFile.close();

    return points;
}

void savePointsToCSV(rs2::points& points, std::string filename)
{
    /* this segment actually prints the pointcloud */
    std::ofstream csv;

    csv.open(filename);

    auto vertices = points.get_vertices();              // get vertices
    auto tex_coords = points.get_texture_coordinates(); // and texture coordinates
    for (int i = 0; i < points.size(); i++)
    {
        if (vertices[i].z)
        {
            csv << vertices[i].x << ";" << vertices[i].y << ";" << vertices[i].z << ";" << tex_coords[i].u << ";" << tex_coords[i].v << "\n";
        }
    }



    csv.close();

}