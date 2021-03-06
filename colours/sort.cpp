/* HOW TO COMPILE 'g++-7 hello.cpp -fopenmp' */
#include <sstream>
#include <iostream>
#include <stdlib.h>
#include <math.h>                           /* math functions */
#include <vector>
#include <algorithm>

using namespace std;



void isort(int arr[], int idx[], int NS){

vector<int> x (arr, arr + NS );
vector<int> y (arr, arr + NS );

int ic=0;

    //std::vector<int> y(x.size());
    std::size_t n(0);
    std::generate(std::begin(y), std::end(y), [&]{ return n++; });

    std::sort(  std::begin(y), 
                std::end(y),
                [&](int i1, int i2) { return x[i1] < x[i2]; } );

    for (auto v : y){
        //std::cout << v << ' ';
        idx[ic]=v;
        ic = ic + 1;
        }
   
}


int main(){
int n = 14,i1=0;
int myints[] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14};
int idsort[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0};

isort(myints,idsort,n);
cout << "\n";
for (i1=0;i1<n;i1=i1+1) cout << idsort[i1] << " ";
cout << "\n";
for (i1=0;i1<n;i1=i1+1) cout << myints[i1] << " ";
cout << "\n";
for (i1=0;i1<n;i1=i1+1) cout << myints[idsort[i1]] << " ";
cout << "\n";

}