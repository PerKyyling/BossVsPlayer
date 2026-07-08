#ifndef astar1_hpp
#define astar1_hpp

#include <string>
#include <vector>
#include <queue>
#include <cmath>
#include <algorithm>

struct Point {
    int y;
    int x;
};

struct cell {
    bool isWall = false;
    int heuristics;
    int dist = 1e9;
    int y; 
    int x;
};

class astar_lib {
public:
    astar_lib() : py(0), px(0), by(0), bx(0), height(0) {}
    std::string astar();
    void read_from_file(const std::string& filename);
    int get_height();

private:
    std::vector<std::string> vect; 
    int py, px, by, bx, height;

    int manhattan(int ny, int nx, int fy, int fx) {
        return std::abs(ny - fy) + std::abs(nx - fx);
    }
};

class Bfs {
public:
    Bfs() : py(0), px(0), by(0), bx(0), is_do(0), height(0) {}
    void read_from_file(const std::string& filename); 
    std::string bfs(); 
    int get_height();
    
    int py, px, by, bx, is_do, height;

private:
    std::vector<std::string> vect_;
    std::vector<std::vector<bool>> visitedMatrix_;
    std::vector<std::vector<Point>> parentMatrix_;
    std::queue<Point> vector_; 
    std::vector<std::vector<int>> normalVector_; 
    void createNormalVector();
    bool bl_ = true;
};

#endif
