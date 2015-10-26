/*red-back gauss seidel*/


#include  <iostream>
#include  <cmath>                       
#include  <cstdlib>                        
#include  <unistd.h>                     
#include  <ctime>
#include  <fstream>
#include  <iostream>
using namespace std;

int main();
double cpu_time();
int main()
{
	ofstream outFile("output.txt");
	int n 		=	 100;
	int m        = 	 100;
	double h, h1;
	double a,b,c,d;
	double A[n][m];
	double f[n+1][m+1];
	double u2[n+1][m+1];
	double xn;
	double ctime;
	double ctime1;
	double ctime2;
	 ctime1=cpu_time();
	a=-1;
	b= 1;
	c=-1;
    d= 1;
    double x[n+1];
    double y[m+1];
    
    h=(b-a)/double(n);
    h1=h*h;
    
#pragma omp parallel for num_threads(24)    
    for (int i=1; i<=n+1; i++)
    {
		x[i] = a+ h*(i-1);
		y[i] = c+ h*(i-1);	
	}


#pragma omp parallel for num_threads(24)	
	for (int i=1; i<=n+1; i++)
	{
		for (int j=1; j<=n+1; j++)
		{
			f[i][j] = -2*3.141592*3.141592*cos(3.141592*x[i])*sin(3.141592*y[j]);
			u2[i][j] = 0;
		}
	}

#pragma omp parallel for num_threads(24)	
	for (int i=1; i<=n+1; i++)
	{
		u2[1][i] = cos(3.141592*a)*sin(3.141592*y[i]);
		u2[n+1][i] = cos(3.141592*b)*sin(3.141592*y[i]);
		u2[i][1] = cos(3.141592*x[i])*sin(3.141592*c);
		u2[i][n+1] = cos(3.141592*x[i])*sin(3.141592*d);
		
			
			
			}
			
	int k;
	cout <<"iteration #:   ";
	cin >> k;	
		
		
				
	for (int p=1; p<k; p++)
	{
		
	
#pragma omp parallel for num_threads(24)
		for (int i=2; i<=n; i++)
		{
			for (int j=(i%2) + 2; j<=n; j+=2)
			{
				
				u2[i][j] = (u2[i-1][j]+u2[i+1][j] + u2[i][j-1] +u2[i][j+1] ) *0.25 - h1*f[i][j]/4;
				
				
			}
		}
		
#pragma omp parallel for num_threads(24)
			for (int i=2; i<=n; i++)
		{
			for (int j=((i+1)%2) + 2; j<=n; j+=2)
			{
				
				u2[i][j] = (u2[i-1][j]+u2[i+1][j] + u2[i][j-1] +u2[i][j+1] ) *0.25 - h1*f[i][j]/4;
				
				
			}
		}
		
	}

	
	for (int i=1; i<=n+1; i++)
	{
		for (int j=1; j<=n+1; j++)
		{
	outFile << u2[i][j] <<" ";
	
}
outFile << endl;
}

ctime2 = cpu_time();
	ctime = (ctime2- ctime1)/24;
	cout<< "CPU time =" << ctime;
	
}

	
		
double cpu_time ( )


{
  double value;

  value = ( double ) clock ( ) / ( double ) CLOCKS_PER_SEC;

  return value;
}
		
					
		
			
    
		

