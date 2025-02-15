#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
#include <sstream>
#include <map>
using namespace std;
main (int argc, char* argv[])
{
  int i,a1[20000],b1[20000],c1[20000],d1[20000],a2[20000],b2[20000],c2[20000],d2[20000],a3[20000],b3[20000],c3[20000],d3[20000],a7[20000],b7[20000],c7[20000],d7[20000];
  int a2x[20000],b2x[20000],c2x[20000],d2x[20000],a3x[20000],b3x[20000],c3x[20000],d3x[20000],a4[20000],b4[20000],c4[20000],d4[20000],a5[20000],b5[20000],c5[20000],d5[20000];
  int a3y[20000],b3y[20000],c3y[20000],d3y[20000],a5x[20000],b5x[20000],c5x[20000],d5x[20000],a6[20000],b6[20000],c6[20000],d6[20000],a7x[20000],b7x[20000],c7x[20000],d7x[20000];
  int a1f[20000],b1f[20000],c1f[20000],d1f[20000];
  int a4f[20000],b4f[20000],c4f[20000],d4f[20000];
  int a2f1[20000],b2f1[20000],c2f1[20000],d2f1[20000];
  int a2f2[20000],b2f2[20000],c2f2[20000],d2f2[20000];
  int a3f1[20000],b3f1[20000],c3f1[20000],d3f1[20000];
  int a3f2[20000],b3f2[20000],c3f2[20000],d3f2[20000];
  int a3f3[20000],b3f3[20000],c3f3[20000],d3f3[20000];
  int a5f1[20000],b5f1[20000],c5f1[20000],d5f1[20000];
  int a5f2[20000],b5f2[20000],c5f2[20000],d5f2[20000];
  int a6f[20000],b6f[20000],c6f[20000],d6f[20000];
  int a7f1[20000],b7f1[20000],c7f1[20000],d7f1[20000];
  int a7f2[20000],b7f2[20000],c7f2[20000],d7f2[20000];
  int a2f[20000],b2f[20000],c2f[20000],d2f[20000];
  int a5f[20000],b5f[20000],c5f[20000],d5f[20000];
  int a7f[20000],b7f[20000],c7f[20000],d7f[20000];
  int a3f[20000],b3f[20000],c3f[20000],d3f[20000];
  int a3fx[20000],b3fx[20000],c3fx[20000],d3fx[20000];
  int tot1, tot2a, tot2b, tot3a, tot3b, tot3c, tot4, tot5a, tot5b, tot6, tot7a, tot7b, tot2, tot3, tot5, tot7, tot3x;
  char outx1[20],outx2[20],outx2b[20],outx3[20],outx3b[20],outx3c[20],outx4[20],outx5[20],outx5b[20],outx6[20],outx7[20],outx7b[20];
  string lines1, lines2, lines3;
  int wrt1,wrt2,wrt3;
  int numb,numb1,numb2,numb3;
  numb = atoi(argv[1]);
  ifstream infile1 ("Total_Energy_1_temp");
  i = 0;
  while(!infile1.eof())
  {
    getline(infile1,lines1);
    istringstream line1(lines1);
    if (infile1.eof()) break;
    line1 >> a1[i] >> b1[i] >> c1[i] >> d1[i] >> a2[i] >> b2[i] >> c2[i] >> d2[i] >> a3[i] >> b3[i] >> c3[i] >> d3[i] >> a7[i] >> b7[i] >> c7[i] >>d7[i];    
//    printf("%i %i %i %i %i\n",i,a1[i],b1[i],c1[i],d1[i]);
    i++;
  }
  numb1 = i;

  ifstream infile2 ("Total_Energy_2_temp");
  i = 0;
  while(!infile2.eof())
  {
    getline(infile2,lines2);
    istringstream line2(lines2);
    if (infile2.eof()) break;
    line2 >> a2x[i] >> b2x[i] >> c2x[i] >> d2x[i] >> a3x[i] >> b3x[i] >> c3x[i] >> d3x[i] >> a4[i] >> b4[i] >> c4[i] >> d4[i] >> a5[i] >> b5[i] >> c5[i] >> d5[i];
//    printf("%i %i %i %i %i\n",i,a2x[i],b2x[i],c2x[i],d2x[i]);
    i++;
  }
  numb2 = i;

  ifstream infile3 ("Total_Energy_3_temp");
  i = 0;
  while(!infile3.eof())
  {
    getline(infile3,lines3);
    istringstream line3(lines3);
    if (infile3.eof()) break;
    line3 >> a3y[i] >> b3y[i] >> c3y[i] >> d3y[i] >> a5x[i] >> b5x[i] >> c5x[i] >> d5x[i] >> a6[i] >> b6[i] >> c6[i] >> d6[i] >> a7x[i] >> b7x[i] >> c7x[i] >> d7x[i];
//    printf("%i %i %i %i %i\n",i,a3y[i],b3y[i],c3y[i],d3y[i]);
    i++;
  }
  numb3 = i;
 
  a1f[0] = a1[0];
  b1f[0] = b1[0];
  c1f[0] = c1[0];
  d1f[0] = d1[0];
  int k = 1;
  int t = 0;
  int j,p; 
  for (j = 1; j < numb1; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a1[j] != a1f[p] || b1[j] != b1f[p] || c1[j] != c1f[p] || d1[j] != d1f[p])
      {
        t++;
      }
      if (t == k)
      {
        a1f[k] = a1[j];
        b1f[k] = b1[j];
        c1f[k] = c1[j];
        d1f[k] = d1[j];
//        printf("new of %i is %i %i %i %i\n",k,a1f[k],b1f[k],c1f[k],d1f[k]);
        k++;
      }
    }
  } 
  tot1 = k;

  ofstream out1("Consensus_1.out");
  for (int a = 0; a < tot1; a++)
  {
    sprintf(outx1,"%i %i %i %i",a1f[a],b1f[a],c1f[a],d1f[a]);
    out1 << outx1 << endl;
  } 

  a2f1[0] = a2[0];
  b2f1[0] = b2[0];
  c2f1[0] = c2[0];
  d2f1[0] = d2[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb1; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a2[j] != a2f1[p] || b2[j] != b2f1[p] || c2[j] != c2f1[p] || d2[j] != d2f1[p])
      {
        t++;
      }
      if (t == k)
      {
        a2f1[k] = a2[j];
        b2f1[k] = b2[j];
        c2f1[k] = c2[j];
        d2f1[k] = d2[j];
//        printf("new1 of %i is %i %i %i %i\n",k,a2f1[k],b2f1[k],c2f1[k],d2f1[k]);
        k++;
      }
    }
  }
  tot2a = k;

  a2f2[0] = a2x[0];
  b2f2[0] = b2x[0];
  c2f2[0] = c2x[0];
  d2f2[0] = d2x[0];
  k = 1; 
  t = 0; 
  for (j = 1; j < numb2; j++)
  { 
    t = 0; 
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a2x[j] != a2f2[p] || b2x[j] != b2f2[p] || c2x[j] != c2f2[p] || d2x[j] != d2f2[p])
      {
        t++;
      }
      if (t == k)
      {
        a2f2[k] = a2x[j];
        b2f2[k] = b2x[j];
        c2f2[k] = c2x[j];
        d2f2[k] = d2x[j];
//        printf("new2 of %i is %i %i %i %i\n",k,a2f2[k],b2f2[k],c2f2[k],d2f2[k]);
        k++;
      } 
    }   
  }   
  tot2b = k;

  int n = 0;
  int l,m;
  for (l = 0; l < tot2a; l++)
  {
    for (m = 0; m < tot2b; m++)
    {
      if (a2f1[l] == a2f2[m] && b2f1[l] == b2f2[m] && c2f1[l] == c2f2[m] && d2f1[l] == d2f2[m])
      {
        a2f[n] = a2f1[l];
        b2f[n] = b2f1[l];
        c2f[n] = c2f1[l];
        d2f[n] = d2f1[l];
//        printf("same of %i is %i %i %i %i\n",n,a2f[n],b2f[n],c2f[n],d2f[n]); 
        n++; 
      }
    } 
  }
  tot2 = n;

  int tot2max;
  if (tot2a > tot2b) tot2max = tot2a;
  if (tot2a <= tot2b) tot2max = tot2b;

  ofstream out2("Consensus_2.out");
  for (int a = 0; a < tot2max; a++)
  {
    wrt1 = 0;
    wrt2 = 0; 
    if (a < tot2a)
    {
      for (int b = 0; b <= a; b++)
      {
        if (a2f1[a] == a2f2[b] && b2f1[a] == b2f2[b] && c2f1[a] == c2f2[b] && d2f1[a] == d2f2[b])
        {
          wrt1 = 1;
        }
        if (b == tot2b - 1) break;
      }
      if (wrt1 == 0)
      {
        sprintf(outx2,"%i %i %i %i",a2f1[a],b2f1[a],c2f1[a],d2f1[a]);
        out2 << outx2 << endl;
      }
    }
    if (a < tot2b)
    {
      for (int b = 0; b < a; b++)
      {
        if (a2f2[a] == a2f1[b] && b2f2[a] == b2f1[b] && c2f2[a] == c2f1[b] && d2f2[a] == d2f1[b])
        {
          wrt2 = 1;
        }
        if (b == tot2a - 1) break;
      } 
      if (wrt2 == 0)
      {
        sprintf(outx2b,"%i %i %i %i",a2f2[a],b2f2[a],c2f2[a],d2f2[a]);
        out2 << outx2b << endl;
      }
    }
  }

  a3f1[0] = a3[0];
  b3f1[0] = b3[0];
  c3f1[0] = c3[0];
  d3f1[0] = d3[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb1; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a3[j] != a3f1[p] || b3[j] != b3f1[p] || c3[j] != c3f1[p] || d3[j] != d3f1[p])
      {
        t++;
      }
      if (t == k)
      {
        a3f1[k] = a3[j];
        b3f1[k] = b3[j];
        c3f1[k] = c3[j];
        d3f1[k] = d3[j];
        printf("new1 of %i is %i %i %i %i\n",k,a3f1[k],b3f1[k],c3f1[k],d3f1[k]);
        k++;
      }
    }
  }
  tot3a = k;

  a3f2[0] = a3x[0];
  b3f2[0] = b3x[0];
  c3f2[0] = c3x[0];
  d3f2[0] = d3x[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb2; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a3x[j] != a3f2[p] || b3x[j] != b3f2[p] || c3x[j] != c3f2[p] || d3x[j] != d3f2[p])
      {
        t++;
      }
      if (t == k)
      {
        a3f2[k] = a3x[j];
        b3f2[k] = b3x[j];
        c3f2[k] = c3x[j];
        d3f2[k] = d3x[j];
        printf("new2 of %i is %i %i %i %i\n",k,a3f2[k],b3f2[k],c3f2[k],d3f2[k]);
        k++;
      }
    }
  }
  tot3b = k;

  a3f3[0] = a3y[0];
  b3f3[0] = b3y[0];
  c3f3[0] = c3y[0];
  d3f3[0] = d3y[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb3; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a3y[j] != a3f3[p] || b3y[j] != b3f3[p] || c3y[j] != c3f3[p] || d3y[j] != d3f3[p])
      {
        t++;
      }
      if (t == k)
      {
        a3f3[k] = a3y[j];
        b3f3[k] = b3y[j];
        c3f3[k] = c3y[j];
        d3f3[k] = d3y[j];
        printf("new3 of %i is %i %i %i %i\n",k,a3f3[k],b3f3[k],c3f3[k],d3f3[k]);
        k++;
      }
    }
  }
  tot3c = k;

  n = 0;
  for (l = 0; l < tot3a; l++)
  {
    for (m = 0; m < tot3b; m++)
    {
      if (a3f1[l] == a3f2[m] && b3f1[l] == b3f2[m] && c3f1[l] == c3f2[m] && d3f1[l] == d3f2[m])
      {
        a3fx[n] = a3f1[l];
        b3fx[n] = b3f1[l];
        c3fx[n] = c3f1[l];
        d3fx[n] = d3f1[l];
//        printf("same of %i is %i %i %i %i\n",n,a3fx[n],b3fx[n],c3fx[n],d3fx[n]); 
        n++;
      }
    }
  }
  tot3x = n;

  n = 0;
  for (l = 0; l < tot3c; l++)
  {
    for (m = 0; m < tot3x; m++)
    {
      if (a3f3[l] == a3fx[m] && b3f3[l] == b3fx[m] && c3f3[l] == c3fx[m] && d3f3[l] == d3fx[m])
      {
        a3f[n] = a3f3[l];
        b3f[n] = b3f3[l];
        c3f[n] = c3f3[l];
        d3f[n] = d3f3[l];
//        printf("same2 of %i is %i %i %i %i\n",n,a3f[n],b3f[n],c3f[n],d3f[n]);
        n++;
      }
    }
  }
  tot3 = n;

  int tot3max;
  if (tot3a >= tot3b && tot3a >= tot3c) tot3max = tot3a;
  if (tot3b >= tot3a && tot3b >= tot3c) tot3max = tot3b;
  if (tot3c >= tot3a && tot3c >= tot3b) tot3max = tot3c;

  ofstream out3("Consensus_3.out");
  for (int a = 0; a < tot3max; a++)
  {
    wrt1 = 0;
    wrt2 = 0;
    wrt3 = 0;
    if (a < tot3a)
    {
      for (int b = 0; b <= a; b++)
      {
        if (a3f1[a] == a3f2[b] && b3f1[a] == b3f2[b] && c3f1[a] == c3f2[b] && d3f1[a] == d3f2[b])
        {
          wrt1 = 1;
        }
        if (b == tot3b - 1) break;
      }
      for (int b = 0; b <= a; b++)
      {
        if (a3f1[a] == a3f3[b] && b3f1[a] == b3f3[b] && c3f1[a] == c3f3[b] && d3f1[a] == d3f3[b])
        {
          wrt1 = 1;
        }
        if (b == tot3c - 1) break;
      }
      if (wrt1 == 0)
      {
        sprintf(outx3,"%i %i %i %i",a3f1[a],b3f1[a],c3f1[a],d3f1[a]);
        out3 << outx3 << endl;
      }
    }

    if (a < tot3b)
    {
      for (int b = 0; b < a; b++)
      {
        if (a3f2[a] == a3f1[b] && b3f2[a] == b3f1[b] && c3f2[a] == c3f1[b] && d3f2[a] == d3f1[b])
        {
          wrt2 = 1;
        }
        if (b == tot3a - 1) break;
      }
      for (int b = 0; b <= a; b++)
      {
        if (a3f2[a] == a3f3[b] && b3f2[a] == b3f3[b] && c3f2[a] == c3f3[b] && d3f2[a] == d3f3[b])
        {
          wrt2 = 1;
        }
        if (b == tot3c - 1) break;
      }
      if (wrt2 == 0)
      {
        sprintf(outx3b,"%i %i %i %i",a3f2[a],b3f2[a],c3f2[a],d3f2[a]);
        out3 << outx3b << endl;
      }
    }

    if (a < tot3c)
    {
      for (int b = 0; b < a; b++)
      {
        if (a3f3[a] == a3f1[b] && b3f3[a] == b3f1[b] && c3f3[a] == c3f1[b] && d3f3[a] == d3f1[b])
        {
          wrt3 = 1;
        }
        if (b == tot3a - 1) break;
      }
      for (int b = 0; b < a; b++)
      {
        if (a3f3[a] == a3f2[b] && b3f3[a] == b3f2[b] && c3f3[a] == c3f2[b] && d3f3[a] == d3f2[b])
        {
          wrt3 = 1;
        }
        if (b == tot3b - 1) break;
      }
      if (wrt3 == 0)
      {
        sprintf(outx3c,"%i %i %i %i",a3f3[a],b3f3[a],c3f3[a],d3f3[a]);
        out3 << outx3c << endl;
      }
    }

  }

  a4f[0] = a4[0];
  b4f[0] = b4[0];
  c4f[0] = c4[0];
  d4f[0] = d4[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb2; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a4[j] != a4f[p] || b4[j] != b4f[p] || c4[j] != c4f[p] || d4[j] != d4f[p])
      {
        t++;
      }
      if (t == k)
      {
        a4f[k] = a4[j];
        b4f[k] = b4[j];
        c4f[k] = c4[j];
        d4f[k] = d4[j];
//        printf("new of %i is %i %i %i %i\n",k,a4f[k],b4f[k],c4f[k],d4f[k]);
        k++;
      }
    }
  }
  tot4 = k;

  ofstream out4("Consensus_4.out");
  for (int a = 0; a < tot4; a++)
  {
    sprintf(outx4,"%i %i %i %i",a4f[a],b4f[a],c4f[a],d4f[a]);
    out4 << outx4 << endl;
  }

  a5f1[0] = a5[0];
  b5f1[0] = b5[0];
  c5f1[0] = c5[0];
  d5f1[0] = d5[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb2; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a5[j] != a5f1[p] || b5[j] != b5f1[p] || c5[j] != c5f1[p] || d5[j] != d5f1[p])
      {
        t++;
      }
      if (t == k)
      {
        a5f1[k] = a5[j];
        b5f1[k] = b5[j];
        c5f1[k] = c5[j];
        d5f1[k] = d5[j];
//        printf("new1 of %i is %i %i %i %i\n",k,a5f1[k],b5f1[k],c5f1[k],d5f1[k]);
        k++;
      }
    }
  }
  tot5a = k;
 
  a5f2[0] = a5x[0];
  b5f2[0] = b5x[0];
  c5f2[0] = c5x[0];
  d5f2[0] = d5x[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb3; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a5x[j] != a5f2[p] || b5x[j] != b5f2[p] || c5x[j] != c5f2[p] || d5x[j] != d5f2[p])
      {
        t++;
      }
      if (t == k)
      {
        a5f2[k] = a5x[j];
        b5f2[k] = b5x[j];
        c5f2[k] = c5x[j];
        d5f2[k] = d5x[j];
//        printf("new2 of %i is %i %i %i %i\n",k,a5f2[k],b5f2[k],c5f2[k],d5f2[k]);
        k++;
      }
    }
  }
  tot5b = k;

  n = 0;
  for (l = 0; l < tot5a; l++)
  {
    for (m = 0; m < tot5b; m++)
    {
      if (a5f1[l] == a5f2[m] && b5f1[l] == b5f2[m] && c5f1[l] == c5f2[m] && d5f1[l] == d5f2[m])
      {
        a5f[n] = a5f1[l];
        b5f[n] = b5f1[l];
        c5f[n] = c5f1[l];
        d5f[n] = d5f1[l];
//        printf("same of %i is %i %i %i %i\n",n,a5f[n],b5f[n],c5f[n],d5f[n]);
        n++;
      }
    }
  }
  tot5 = n;

  int tot5max;
  if (tot5a > tot5b) tot5max = tot5a;
  if (tot5a <= tot5b) tot5max = tot5b;

  ofstream out5("Consensus_5.out");
  for (int a = 0; a < tot5max; a++)
  {
    wrt1 = 0;
    wrt2 = 0;
    if (a < tot5a)
    {
      for (int b = 0; b <= a; b++)
      {
        if (a5f1[a] == a5f2[b] && b5f1[a] == b5f2[b] && c5f1[a] == c5f2[b] && d5f1[a] == d5f2[b])
        {
          wrt1 = 1;
        }
        if (b == tot5b - 1) break;
      }
      if (wrt1 == 0)
      {
        sprintf(outx5,"%i %i %i %i",a5f1[a],b5f1[a],c5f1[a],d5f1[a]);
        out5 << outx5 << endl;
      }
    }
    if (a < tot5b)
    {
      for (int b = 0; b < a; b++)
      {
        if (a5f2[a] == a5f1[b] && b5f2[a] == b5f1[b] && c5f2[a] == c5f1[b] && d5f2[a] == d5f1[b])
        {
          wrt2 = 1;
        }
        if (b == tot5a - 1) break;
      }
      if (wrt2 == 0)
      {
        sprintf(outx5b,"%i %i %i %i",a5f2[a],b5f2[a],c5f2[a],d5f2[a]);
        out5 << outx5b << endl;
      }
    }
  }

  a6f[0] = a6[0];
  b6f[0] = b6[0];
  c6f[0] = c6[0];
  d6f[0] = d6[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb3; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a6[j] != a6f[p] || b6[j] != b6f[p] || c6[j] != c6f[p] || d6[j] != d6f[p])
      {
        t++;
      }
      if (t == k)
      {
        a6f[k] = a6[j];
        b6f[k] = b6[j];
        c6f[k] = c6[j];
        d6f[k] = d6[j];
//        printf("new of %i is %i %i %i %i\n",k,a6f[k],b6f[k],c6f[k],d6f[k]);
        k++;
      }
    }
  }
  tot6 = k;

  ofstream out6("Consensus_6.out");
  for (int a = 0; a < tot6; a++)
  {
    sprintf(outx6,"%i %i %i %i",a6f[a],b6f[a],c6f[a],d6f[a]);
    out6 << outx6 << endl;
  }

  a7f1[0] = a7[0];
  b7f1[0] = b7[0];
  c7f1[0] = c7[0];
  d7f1[0] = d7[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb1; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a7[j] != a7f1[p] || b7[j] != b7f1[p] || c7[j] != c7f1[p] || d7[j] != d7f1[p])
      {
        t++;
      }
      if (t == k)
      {
        a7f1[k] = a7[j];
        b7f1[k] = b7[j];
        c7f1[k] = c7[j];
        d7f1[k] = d7[j];
//        printf("new1 of %i is %i %i %i %i\n",k,a7f1[k],b7f1[k],c7f1[k],d7f1[k]);
        k++;
      }
    }
  }
  tot7a = k;

  a7f2[0] = a7x[0];
  b7f2[0] = b7x[0];
  c7f2[0] = c7x[0];
  d7f2[0] = d7x[0];
  k = 1;
  t = 0;
  for (j = 1; j < numb3; j++)
  {
    t = 0;
//    printf("line %i is %i %i %i %i\n",j,a1[j],b1[j],c1[j],d1[j]);
    for (p = 0; p < k; p++)
    {
      if (a7x[j] != a7f2[p] || b7x[j] != b7f2[p] || c7x[j] != c7f2[p] || d7x[j] != d7f2[p])
      {
        t++;
      }
      if (t == k)
      {
        a7f2[k] = a7x[j];
        b7f2[k] = b7x[j];
        c7f2[k] = c7x[j];
        d7f2[k] = d7x[j];
//        printf("new2 of %i is %i %i %i %i\n",k,a7f2[k],b7f2[k],c7f2[k],d7f2[k]);
        k++;
      }
    }
  }
  tot7b = k;

  n = 0;
  for (l = 0; l < tot7a; l++)
  {
    for (m = 0; m < tot7b; m++)
    {
      if (a7f1[l] == a7f2[m] && b7f1[l] == b7f2[m] && c7f1[l] == c7f2[m] && d7f1[l] == d7f2[m])
      {
        a7f[n] = a7f1[l];
        b7f[n] = b7f1[l];
        c7f[n] = c7f1[l];
        d7f[n] = d7f1[l];
//        printf("same of %i is %i %i %i %i\n",n,a7f[n],b7f[n],c7f[n],d7f[n]);
        n++;
      }
    }
  }
  tot7 = n;

  int tot7max;
  if (tot7a > tot7b) tot7max = tot7a;
  if (tot7a <= tot7b) tot7max = tot7b;

  ofstream out7("Consensus_7.out");
  for (int a = 0; a < tot7max; a++)
  {
    wrt1 = 0;
    wrt2 = 0;
    if (a < tot7a)
    {
      for (int b = 0; b <= a; b++)
      {
        if (a7f1[a] == a7f2[b] && b7f1[a] == b7f2[b] && c7f1[a] == c7f2[b] && d7f1[a] == d7f2[b])
        {
          wrt1 = 1;
        }
        if (b == tot7b - 1) break;
      }
      if (wrt1 == 0)
      {
        sprintf(outx7,"%i %i %i %i",a7f1[a],b7f1[a],c7f1[a],d7f1[a]);
        out7 << outx7 << endl;
      }
    }
    if (a < tot7b)
    {
      for (int b = 0; b < a; b++)
      {
        if (a7f2[a] == a7f1[b] && b7f2[a] == b7f1[b] && c7f2[a] == c7f1[b] && d7f2[a] == d7f1[b])
        {
          wrt2 = 1;
        }
        if (b == tot7a - 1) break;
      }
      if (wrt2 == 0)
      {
        sprintf(outx7b,"%i %i %i %i",a7f2[a],b7f2[a],c7f2[a],d7f2[a]);
        out7 << outx7b << endl;
      }
    }
  }

}
