
#include "utils.h"
#include <string>       // std::string
#include <iostream>     // std::cout
#include <sstream>  

#ifdef OPENCV
#include <opencv2/core.hpp>   // Include OpenCV API
#include <opencv2/highgui.hpp>   // Include OpenCV API
#include <opencv2/imgcodecs.hpp>   // Include OpenCV API
#include <opencv2/imgproc.hpp>   // Include OpenCV API
#include "opencv2/videoio.hpp"
#include <opencv2/video.hpp>
#endif


double _pointPolygonTest(std::vector<glm::vec2> _contour, glm::vec2 pt, bool measureDist)
{
   

    double result = 0;
    int total = _contour.size(), counter = 0;

    double min_dist_num = FLT_MAX, min_dist_denom = 1;
  
    glm::vec2 v0, v = _contour[total - 1];
            for (int i = 0; i < total; i++)
            {
                double dx, dy, dx1, dy1, dx2, dy2, dist_num, dist_denom = 1;

                v0 = v;
                v = _contour[i];

                dx = v.x - v0.x; dy = v.y - v0.y;
                dx1 = pt.x - v0.x; dy1 = pt.y - v0.y;
                dx2 = pt.x - v.x; dy2 = pt.y - v.y;

                if (dx1 * dx + dy1 * dy <= 0)
                    dist_num = dx1 * dx1 + dy1 * dy1;
                else if (dx2 * dx + dy2 * dy >= 0)
                    dist_num = dx2 * dx2 + dy2 * dy2;
                else
                {
                    dist_num = (dy1 * dx - dx1 * dy);
                    dist_num *= dist_num;
                    dist_denom = dx * dx + dy * dy;
                }

                if (dist_num * min_dist_denom < min_dist_num * dist_denom)
                {
                    min_dist_num = dist_num;
                    min_dist_denom = dist_denom;
                    if (min_dist_num == 0)
                        break;
                }

                if ((v0.y <= pt.y && v.y <= pt.y) ||
                    (v0.y > pt.y && v.y > pt.y) ||
                    (v0.x < pt.x && v.x < pt.x))
                    continue;

                dist_num = dy1 * dx - dx1 * dy;
                if (dy < 0)
                    dist_num = -dist_num;
                counter += dist_num > 0;
            }

            result = std::sqrt(min_dist_num / min_dist_denom);
            if (counter % 2 == 0)
                result = -result;

    return result;
}

#ifdef OPENCV
double _pointPolygonTest(std::vector<cv::Point> contour, cv::Point p, bool measureDist)
{
    std::vector<glm::vec2> _cnt;

    for (int i = 0; i < contour.size(); i++)
    {
        _cnt.push_back(glm::vec2(contour[i].x, contour[i].y));
    }

    glm::vec2 pt = glm::vec2(p.x, p.y);

    return _pointPolygonTest(_cnt, pt, measureDist);

}
#endif

glm::vec3 convertToEulerAngle(rs2_vector accel_data)
{
    glm::vec3 euler;

    euler.x = accel_data.x;
    euler.y = accel_data.y;
    euler.z = accel_data.z;


    return euler;
}
////////////////////////////////////////////////////
/// check optimal parameters


bool check_imu_is_supported_by_cam()
{
#ifdef _WIN32
    // there is a bug with context
    bool found_gyro = false;
    bool found_accel = false;
    rs2::context ctx;
    for (auto dev : ctx.query_devices())
    {
        // The same device should support gyro and accel
        found_gyro = false;
        found_accel = false;
        for (auto sensor : dev.query_sensors())
        {
            for (auto profile : sensor.get_stream_profiles())
            {
                if (profile.stream_type() == RS2_STREAM_GYRO)
                    found_gyro = true;

                if (profile.stream_type() == RS2_STREAM_ACCEL)
                    found_accel = true;
            }
        }
        if (found_gyro && found_accel)
            break;
    }
    return found_gyro && found_accel;
#else
    return false;
#endif
}

bool prepareCameraParameters(rs2::config& cfg)
{
    try
    {
        
        if (!check_imu_is_supported_by_cam()) return false;

        // Create a configuration for configuring the pipeline with a non default profile

        // Add pose stream
        // Use a configuration object to request only depth from the pipeline
        cfg.enable_stream(RS2_STREAM_DEPTH, 1280, 0, RS2_FORMAT_Z16, 30);
        cfg.enable_stream(RS2_STREAM_COLOR, 1280, 0, RS2_FORMAT_RGB8, 30);

        

        if (check_imu_is_supported_by_cam())
        {
            cfg.enable_stream(RS2_STREAM_GYRO, RS2_FORMAT_MOTION_XYZ32F);
            cfg.enable_stream(RS2_STREAM_ACCEL, RS2_FORMAT_MOTION_XYZ32F);
        }
        else
        {
            std::cout << "IMU is not supported or not working" << "\n";
        }
        return true;
    }
    catch (std::exception e)
    {
        return false;
    }
}


////////////////////////////////////////////////////
template<typename Out>
void splits(const std::string& s, char delim, Out result) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        *(result++) = item;
    }
}

std::string str_toupper(std::string s)
{
    std::transform(s.begin(), s.end(), s.begin(),
        // static_cast<int(*)(int)>(std::toupper)         // wrong
        // [](int c){ return std::toupper(c); }           // wrong
        // [](char c){ return std::toupper(c); }          // wrong
        [](unsigned char c) { return std::toupper(c); } // correct
    );
    return s;
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
            o.vertexes.push_back(glm::vec4(0, 0, 0,0));
            o.tex_coords.push_back(glm::vec3(0, 0, 0));
            o.colors.push_back(glm::vec3(0, 0, 0));
        }

    }

  
    int w = color.get_width();
    int h = color.get_height();

    unsigned char* data = (unsigned char*)color.get_data();

    for (int i = 0; i < points.size(); i++)
    {
        int xi = (int)(tex_coords[i].u * w);
        int yi = (int)(tex_coords[i].v * h);

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
        o.vertexes[i] = glm::vec4(vertices[i].x, vertices[i].y, vertices[i].z,0);
        o.tex_coords[i] = glm::vec3(tex_coords[i].u, tex_coords[i].v, 0.0);

    }
}


void saveAsObj(object3D& o, std::string outputFile)
{
    std::vector<glm::vec4> vs = o.vertexes;
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
        outfile << "v " << vs[i].x<<" "<< vs[i].y << " "<< vs[i].z << " "<< vs[i].w<< std::endl;
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
object3D readFromCSV(Camera* cam, std::string filename )
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
        // check if we have pose data
        if (ss.size() >= 4 && ss[0] == "cam_data")
        {
            cam->pose_data_enabled = true;
            cam->pose_data = glm::vec3(std::stof(ss[1]), std::stof(ss[2]), std::stof(ss[3]));
            continue;
        }
        else
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

        o.vertexes.push_back(glm::vec4(pos.x, pos.y, pos.z, cam->id));
        o.tex_coords.push_back(tex);
    }

    inFile.close();

    return o;
}


void savePointsToCSV(object3D& o,Camera* cam, std::string filename)
{
    /* this segment actually prints the pointcloud */
    std::ofstream csv;

    csv.open(filename);

    if (cam && cam->pose_data_enabled)
    {
        csv << "cam_data;" << cam->pose_data.x << ";" << cam->pose_data.y << ";" << cam->pose_data.z << "\n";
    }

   
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

#ifdef OPENCV

cv::Mat vectorToImg(std::vector<float> ihm, int w, int h, double resize)
{
    cv::Mat m(h,w, CV_32FC1);

    m.data = (uchar*)ihm.data();

    cv::resize(m, m, cv::Size(), resize, resize);

    return m;
}
#endif


void erode(std::vector<float>& inputHM, int w, int h, int kernelSize)
{
    std::vector<float> result ;

    for (int i = 0; i < inputHM.size(); i++) result.push_back(inputHM[i]);


    for (int x = kernelSize / 2; x < w - kernelSize / 2; x++)
    {
        for (int y = kernelSize / 2; y < h - kernelSize / 2; y++)
        {
            int count = 0;
            float avg = 0;

            for (int i = -kernelSize / 2; i < kernelSize / 2; i++)
                for (int j = -kernelSize / 2; j < kernelSize / 2; j++)
                {
                    int index = (y + j) * w + x + i;

                    if (inputHM[index] > 0)
                    {
                        count++;  avg += inputHM[index];
                    }
                }

            if (count < kernelSize * kernelSize / 2)
                result[y * w + x] = 0;
        }
    }
    
    for (int i = 0; i < inputHM.size(); i++) inputHM[i] = result[i];
}
void dilate(std::vector<float>& inputHM, int w, int h, int kernelSize)
{
    std::vector<float> result;
    for (int i = 0; i < inputHM.size(); i++) result.push_back(inputHM[i]);

    for (int y = kernelSize / 2; y < h - kernelSize / 2; y++)
    {

        for (int x = kernelSize / 2; x < w - kernelSize / 2; x++)
        
        {
            int count = 0;
            float mx = 0;

            for (int i = -kernelSize / 2; i < kernelSize / 2; i++)
                for (int j = -kernelSize / 2; j < kernelSize / 2; j++)
                {
                    int index = (y + j) * w + x + i;

                    if (inputHM[index] > 0)
                    {
                        count++;  mx = std::max(mx, inputHM[index]);
                    }
                }

            if (count > 1)
                result[y * w + x] = mx;
        }
    }
    for (int i = 0; i < inputHM.size(); i++) inputHM[i] = result[i];
}

void showHeightMapAsImage(std::vector<float>& inputHM, int w, int h,std::string name, bool asSeudoColor, double resize)
{

#ifdef OPENCV
    cv::Mat m = vectorToImg(inputHM, w, h, resize);


    if (asSeudoColor)
    {
        // Convert the float image to a pseudo color image using a colormap
        cv::Mat pseudoColorImage;
        //Initialize m
        double minVal, maxVal;
        cv::Point minLoc, maxLoc;

        minMaxLoc(m, &minVal, &maxVal, &minLoc, &maxLoc);

        cv::Mat imgG;
        m.convertTo(imgG, CV_8UC1, 255.0 / maxVal, 0);

        // Holds the colormap version of the image:
        cv::Mat img_color;
        // Apply the colormap:
        cv::applyColorMap(imgG, pseudoColorImage, cv::COLORMAP_JET); //COLORMAP_JET
        cv::imshow(name, pseudoColorImage);
    }
    else
        cv::imshow(name, m);

#endif 
}


//////////////////////////////////////////

// Bilinear interpolation function
float bilinearInterpolation(const std::vector<float>& matrix, int x, int y, int w, int h) {
    int x0 = x;
    int y0 = y;
    int x1 = x;
    int y1 = y;

    if (x0 < 0 || x1 >= w-1 || y0 < 0 || y1 >= h-1) {
        // Out of bounds, cannot interpolate
        return 0.0f;
    }

    // search left
    while (x0 > 1) {   if (matrix[y * w + x0] > 0) break; x0--;}
    // search right
    while (x1 < w-1) { if (matrix[y * w + x1] > 0) break; x1++; }
    // search up
    while (y0 > 1) { if (matrix[y0 * w + x] > 0) break; y0--; }
    // search down
    while (y1 < h-1) { if (matrix[y1 * w + x] > 0) break; y1++; }

    float dx = (1.0f*(x - x0))/std::max(1,x1-x0);
    float dy = (1.0f*(y - y0))/ std::max(1, y1-y0);

    float value00 = (float)matrix[ y * w + x0];
    float value01 = (float)matrix[ y1 * w + x];
    float value10 = (float)matrix[ y * w + x1];
    float value11 = (float)matrix[ y1 * w + x];

    float interpolatedValue = (1 - dx) *(1-dy)  * value00 +
        dx *(1-dy)  * value10 +
        (1 - dx) *dy * value01 +
         dy *dx * value11;

    return interpolatedValue;
}

std::vector<float> bicubicInterpolation(std::vector<float>& inputHM, int w, int h, std::vector<float> mask)
{
   // first, add external bordes 0

    std::vector<float> outputHM ;
    std::vector<float> tempM;


   // second, copy the content 
    for (int y = 0; y < h; y++)
        for (int x = 0; x < w; x++)
        {
             outputHM.push_back(0);
             tempM.push_back(0);
         }

    int nw = w ;
    int nh = h ;

    for (int y = 0; y < h ; y++)
        for (int x = 0; x < w ; x++)
        {
                int indexSrc =  y * w + x;
                int indexDst = y * nw + x;
                
                tempM[indexDst] = inputHM[indexSrc];
            
        }

   
   // third, for each element x,y
  
   for (int y = 1; y < nh - 1; y++)
   {
       for (int x = 1; x < nw - 1; x++)
       {
           try
           {
               // outside mask
               if (mask.size() > 0 && mask[y * nw + x] == 0)
               {
                   outputHM[y * nw + x] = 0;
                   continue;
               }
               
              // check if this value is empty
               if (inputHM[y * nw + x] == 0)
               {
                   outputHM[y * nw + x] = bilinearInterpolation(inputHM, x, y, nw, nh);
               }
               else
               {
                   outputHM[y * nw + x] = inputHM[y * nw + x];
               }
           }
           catch (std::exception e)
           {
               std::cout << " index" << y << " " << x << "\n";
           }
       }
   }
  
#ifdef OPENCV
   cv::Mat firstm = vectorToImg(inputHM, w, h,5);
   cv::Mat m = vectorToImg(outputHM, nw, nh,5);

  // showHeightMapAsImage(inputHM,w,h, "orig", false);

  // showHeightMapAsImage(outputHM, nw, nh, "interpolated", false);

  // showHeightMapAsImage(outputHM, nw, nh, "seudoColor", false);

  
    cv::waitKey(1);

#endif


    return outputHM;

}