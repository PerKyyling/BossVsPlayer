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
        string dijkstra();
    private:
        vector<string>vect;
        int py,px,by,bx,height;

        int manhattan(int ny,int nx, int fy, int fx){
            return abs(ny-fy)+abs(nx-fx);
}
};


#endif