
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


void getOBJFromFrameSet(object3D& o, rs2::video_frame& color, rs2::points& points)
{

    auto vertices = points.get_vertices();              // get vertices
    auto tex_coords = points.get_texture_coordinates(); // and texture coordinates

    // init first time
    if (o.vertexes.size() == 0)
    {

        for (int i = 0; i < points.size(); i++)
        {
            o.vertexes.push_back(glm::vec3(0, 0, 0));
            o.tex_coords.push_back(glm::vec3(0, 0, 0));
            o.colors.push_back(glm::vec3(0, 0, 0));
        }

    }

  
    int w = color.get_width();
    int h = color.get_height();

    unsigned char* data = (unsigned char*)color.get_data();

    for (int i = 0; i < points.size(); i++)
    {
        int xi = tex_coords[i].u * w;
        int yi = tex_coords[i].v * h;

        if (tex_coords[i].u >= 0 && tex_coords[i].v >= 0 && tex_coords[i].u <= 1.0 && tex_coords[i].v <= 1.0)
        {
            int pi = yi * w * 3 + xi * 3;
            unsigned char r = data[pi + 0];
            unsigned char g = data[pi + 1];
            unsigned char b = data[pi + 2];
            o.colors[i] = glm::vec3(r, g, b);
        }
        else
        {
            o.colors[i] = glm::vec3(0, 0, 0);
        }
        o.vertexes[i] = glm::vec3(vertices[i].x, vertices[i].y, vertices[i].z);
        o.tex_coords[i] = glm::vec3(tex_coords[i].u, tex_coords[i].v, 0.0);

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


object3D readFromOBJ(std::string filename)
{

    object3D o;
    return o;
}

// -1.14069; -0.670039; 1.734; 0.0361091; -0.0373214
object3D readFromCSV(std::string filename)
{
    object3D o;
    
    /* this segment actually prints the pointcloud */
    std::ifstream inFile;
    inFile.open(filename);


    std::string line;

    while (!inFile.eof())

    {
        std::getline(inFile, line); // ommit first line

        // lat long
        std::vector<std::string> ss = splitString(line, ';');
        if (ss.size() < 5)
        {
            continue;
        }

        ///////////////////////////////////////
        glm::vec3 pos = glm::vec3(std::stof(ss[0]), std::stof(ss[1]), std::stof(ss[2]));
        glm::vec3 tex = glm::vec3(std::stof(ss[3]), std::stof(ss[4]), 0.0);

        if (ss.size() >= 8)
        {
            glm::vec3 color = glm::vec3( std::stof(ss[5]), std::stof(ss[6]), std::stof(ss[7]) ) ;

            o.colors.push_back(color);
        }

        o.vertexes.push_back(pos);
        o.tex_coords.push_back(tex);
    }

    inFile.close();

    return o;
}


void savePointsToCSV(object3D& o, std::string filename)
{
    /* this segment actually prints the pointcloud */
    std::ofstream csv;

    csv.open(filename);

   
    for (int i = 0; i < o.vertexes.size(); i++)
    {
        if (o.vertexes[i].z)
        {
            csv << o.vertexes[i].x << ";" << o.vertexes[i].y << ";" << o.vertexes[i].z << ";" << o.tex_coords[i].x << ";" << o.tex_coords[i].y;
            if (o.colors.size() > 0)
            {
                csv << ";" << o.colors[i].x << ";" << o.colors[i].y << ";" << o.colors[i].z << "\n";
            }
            else 
              csv << "\n";
        }
    }



    csv.close();

}