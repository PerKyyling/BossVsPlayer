#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <cmath>
#include <map>
#include <algorithm>
#include <pybind11/pybind11.h>
using namespace std;
const int INF = 1e9;

struct cell{
    bool isWall=false;
    int heuristics;
    int dist=INF;
    int y; int x;
};


struct cmpCell{
    bool operator()(cell c1, cell c2){
        return (c1.dist + c1.heuristics > c2.dist + c2.heuristics);
    }
};

int manhattan(int ny,int nx, int fy, int fx){
    return abs(ny-fy)+abs(nx-fx);
}


/*
bool operator>(cell c1, cell c2){
    if (c1.dist+c1.heuristics<c2.dist+c2.heuristics){
        return true;
    }
    return false;
}
*/

string astar(vector<string> vect, int py, int px, int by, int bx){
    int height = vect.size();
    int width = vect[0].size();
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
    string ans="";
    map<char, pair<int,int>> bck={{'R',{0,-1}}, {'L',{0,1}}, {'U',{1,0}},{'D',{-1,0}}};
    int cuy=py; int cux=px;
    while (cuy!=by||cux!=bx){
        ans.push_back(parent[cuy][cux]);
        pair<int,int> dir=bck[parent[cuy][cux]];
        cuy+=dir.first;
        cux+=dir.second;
    }
    reverse(ans.begin(),ans.end());
    return ans;
}

int main(){
    vector<string> v={
        "111111",
        "100011",
        "100001",
        "111111"
    };
    cout<<astar(v,1,1,2,4);
}