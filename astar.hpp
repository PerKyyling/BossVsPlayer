#ifndef astar_hpp
#define astar_hpp

#include <string>
#include <vector>
#include <queue>
#include <map>
#include <cmath>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <unordered_map>
#include <unordered_set>
#include <sstream>

using namespace std;

const int INF = 1e9;

struct cell{
    bool isWall=false;
    int heuristics;
    int dist=INF;
    int y; int x;
};




class  astar_lib{
    public:
        astar_lib() : py(0), px(0), by(0), bx(0) {}
        string astar();
        void read_from_file(const string& filename);
        int get_height();

    private:

        vector<string> vect; // 1 - wall (. P B) - можно ходить
        int py /* str */, px /* column */, by, bx, height;

        int manhattan(int ny,int nx, int fy, int fx){
            return abs(ny-fy)+abs(nx-fx);
}
};
// класс для реализации BFS
class Bfs {
    public:
        void read_from_file(const string& filename); // просто копипаст из astar
        std::string bfs(); // функция для нахождения маршрута на bfs, возвращает инструкцию {R/L/U/D}
        int py, px, by, bx, is_do, height;

    private:
        std::vector<std::string> vect_;
        std::unordered_set<std::string> vectIsVisited_; // список для проверки посещенных координат
        std::queue<std::vector<int>> vector_; // список вершин графа
        std::unordered_map<std::string, 
        std::vector<std::vector<int>>> map_; // мапа для предков
        std::vector<std::vector<int>> normalVector_; // я задолбался..
        void createNormalVector();
        bool bl_ = true;
};
#endif