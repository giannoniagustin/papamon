
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




void saveAsObj(object3D& o, std::string outputFile)
{
    std::vector<glm::vec3> vs = o.vertexes;
//    # wavefront obj fit3d
//        v 53.5864 114.006 453.241
//       v 53.4813 113.924 453.239
//        v 53.7436 116.868 449.656
//        v 50.1834 114.041 449.612
     // open a file in write mode.
    std::ofstream outfile;
    outfile.open(outputFile);

    // write inputted data into the file.
    outfile << "# wavefront obj" << std::endl;


    // again write inputted data into the file.
    for (int i = 0; i < vs.size(); i++)
    {
        outfile << "v " << vs[i].x<<" "<< vs[i].y << " "<< vs[i].z << std::endl;
    }
    // close the opened file.
    outfile.close();
}


std::vector<std::string> splitString(const std::string& s, char delim) {
    std::vector<std::string> elems;
    splits(s, delim, std::back_inserter(elems));
    return elems;
}


// -1.14069; -0.670039; 1.734; 0.0361091; -0.0373214
object3D readOBJFromFile(std::string filename)
{
    object3D o;
    return o;
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