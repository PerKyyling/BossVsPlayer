#include "astar.hpp"
//#include <pybind11/pybind11.h>

//namespace py = pybind11;

struct cmpCell{
    bool operator()(cell c1, cell c2){
        return (c1.dist + c1.heuristics > c2.dist + c2.heuristics);
    }
};



void astar_lib::read_from_file(const string& filename){
    vect.clear();
    ifstream input(filename);
    input>>py>>px>>by>>bx>>height;

    for (int i=0;i<height;++i){
        string t_string;
        input>>t_string;
        vect.push_back(t_string);
    }

}


/*
bool operator>(cell c1, cell c2){
    if (c1.dist+c1.heuristics<c2.dist+c2.heuristics){
        return true;
    }
    return false;
}
*/

string astar_lib::astar(){
    /*for (auto item : py_vect) {
        vect.push_back(item.cast<string>());
    }*/

    int height = vect.size();
    int width = vect[0].size();


    if (py < 0 || py >= height || px < 0 || px >= width || 
        by < 0 || by >= height || bx < 0 || bx >= width) {
        return "";
    }

    pair<int, int> moves[4]={{1,0},{0,1},{-1,0},{0,-1}};
    char direction[4]={'D','R','U','L'};

    vector<vector<cell>> mp (height, vector<cell>(width));

    for (int i=0;i<height;++i){
        for (int j=0;j<width;++j){
            cell tc;
            tc.y=i;tc.x=j;
            if (vect[i][j]=='1'){
                tc.isWall=true;
            }
            tc.heuristics=manhattan(i,j,py,px);
            mp[i][j]=tc;
            
        }
    }

    vector<vector<char>> parent(height, vector<char>(width,'N'));
    priority_queue<cell, vector<cell>, cmpCell>pq;
    mp[by][bx].dist=0;
    pq.push(mp[by][bx]);
    bool flag=true;
    while (!pq.empty()&&flag){
        cell cur = pq.top();
        int cx=cur.x;
        int cy=cur.y;
        int cd=cur.dist;
        pq.pop();
        for (int i=0;i<4&&flag;++i){
            int ty=moves[i].first+cy;
            int tx=moves[i].second+cx;
            if (ty >= 0 && ty < height && tx >= 0 && tx < width){
                if (!mp[ty][tx].isWall){
                    if (mp[ty][tx].dist>cd+1){
                        mp[ty][tx].dist=cd+1;
                        parent[ty][tx]=direction[i];

                        if (ty==py &&tx==px){flag=false; break;}

                        pq.push(mp[ty][tx]);
                    }
                }
            }
        }
    }

    if (parent[py][px] == 'N') {
        return "";
    }

    string ans="";
    map<char, pair<int,int>> bck={{'R',{0,-1}}, {'L',{0,1}}, {'U',{1,0}},{'D',{-1,0}}};
    int cuy=py; int cux=px;
    while (cuy!=by||cux!=bx){
        if (parent[cuy][cux] == 'N') break;
        ans.push_back(parent[cuy][cux]);
        pair<int,int> dir=bck[parent[cuy][cux]];
        cuy+=dir.first;
        cux+=dir.second;
    }
    reverse(ans.begin(),ans.end());
    return ans;
}

int astar_lib::get_height(){
    return height;
}

/*
int main(){
    vector<string> v={
        "111111",
        "100011",
        "100001",
        "111111"
    };
    cout<<astar(v,1,1,2,4);
}*/

/*PYBIND11_MODULE(astar_lib, m) {
    m.doc() = "a* path finding function";
    m.def("astar", &astar, "for game");
}*/
