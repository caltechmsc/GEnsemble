#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
#include <sstream>
#include <map>
#include <math.h>
using namespace std;
main (int argc, char* argv[])
{
  srand(time(0));
  char ins[50];
  char file[100];
  char outx[10];
  string linesa,tmx,ang,linese;
  char struc[200],error[200];
  char totoutx[100],interoutx[100],nointvoutx[100],hbondoutx[100];
  char tout[500],iout[500],vout[500],hout[500];
  int a1, b1, c1, d1, a2, b2, c2, d2; 
  double yay;
  double phia, theta, hpma, etaa, phib, thetb, hpmb, etab, intr11x, intr22x, inter12x, tot12x, intrv11x, intrv22x, interv12x, novdw12x, interh12x;
  string phiax,phiaxx;
  double eta1[30],phi1[20],thet1[20],hpm1[20];
  double eta2[30],phi2[20],thet2[20],hpm2[20];
  double eta3[30],phi3[20],thet3[20],hpm3[20];
  double eta4[30],phi4[20],thet4[20],hpm4[20];
  double eta5[30],phi5[20],thet5[20],hpm5[20];
  double eta6[30],phi6[20],thet6[20],hpm6[20];
  double eta7[30],phi7[20],thet7[20],hpm7[20];
  long double intr1,intr2,intr3,intr4,intr5,intr6,intr7,hbond,inter,nointv,tot;
  int eta_num[8] = {0},phi_num[8] = {0},thet_num[8] = {0},hpm_num[8] = {0};
  int eta_num2[8],phi_num2[8],thet_num2[8],hpm_num2[8];
  ifstream infile ("angles.txt");
  while (!infile.eof())  
  {
    int j = 0; 
    getline(infile,linesa);
    istringstream linea(linesa);
    linea >> tmx;
    if (tmx == "TM1")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        linea >> yay;
        eta1[j] = yay;
        eta_num[1] = j;
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi1[j] = yay;
        phi_num[1] = j;
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet1[j] = yay;
        thet_num[1] = j;
        }
        if (ang == "HPM")
        {        linea >> yay;
        hpm1[j] = yay;
        hpm_num[1] = j;
        }
      }
    }
    if (tmx == "TM2")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        linea >> yay;
        eta2[j] = yay;
        eta_num[2] = j;
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi2[j] = yay;
        phi_num[2] = j;
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet2[j] = yay;
        thet_num[2] = j;
        }
        if (ang == "HPM")
        {
        linea >> yay;
        hpm2[j] = yay;
        hpm_num[2] = j;
        }
      }
    }
    if (tmx == "TM3")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        linea >> yay;
        eta3[j] = yay;
        eta_num[3] = j;
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi3[j] = yay;
        phi_num[3] = j;
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet3[j] = yay;
        thet_num[3] = j;
        }
        if (ang == "HPM")
        {
        linea >> yay;
        hpm3[j] = yay;
        hpm_num[3] = j;
        }
      }
    }
    if (tmx == "TM4")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        linea >> yay;
        eta4[j] = yay;
        eta_num[4] = j;
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi4[j] = yay;
        phi_num[4] = j;
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet4[j] = yay;
        thet_num[4] = j;
        }
        if (ang == "HPM")
        {
        linea >> yay;
        hpm4[j] = yay;
        hpm_num[4] = j;
        }
      }
    }
    if (tmx == "TM5")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        linea >> yay;
        eta5[j] = yay;
        eta_num[5] = j;
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi5[j] = yay;
        phi_num[5] = j;
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet5[j] = yay;
        thet_num[5] = j;
        }
        if (ang == "HPM")
        {
        linea >> yay;
        hpm5[j] = yay;
        hpm_num[5] = j;
        }
      }
    }
    if (tmx == "TM6")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        linea >> yay;
        eta6[j] = yay;
        eta_num[6] = j;
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi6[j] = yay;
        phi_num[6] = j;
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet6[j] = yay;
        thet_num[6] = j;
        }
        if (ang == "HPM")
        {
        linea >> yay;
        hpm6[j] = yay;
        hpm_num[6] = j;
        }
      }
    }
    if (tmx == "TM7")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        linea >> yay;
        eta7[j] = yay;
        eta_num[7] = j;
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi7[j] = yay;
        phi_num[7] = j;
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet7[j] = yay;
        thet_num[7] = j;
        }
        if (ang == "HPM")
        {
        linea >> yay;
        hpm7[j] = yay;
        hpm_num[7] = j;
        }
      }
    }
  }
  
  for (int x = 0; x< 8; x++)
  {  
  eta_num2[x] = eta_num[x];
  phi_num2[x] = phi_num[x];
  thet_num2[x] = thet_num[x];
  hpm_num2[x] = hpm_num[x];
  }
  
  sort(eta_num2, eta_num2+8);
  sort(hpm_num2, hpm_num2+8);
  sort(thet_num2, thet_num2+8);
  sort(phi_num2, phi_num2+8);
  
  int max_eta = eta_num2[7];
  int max_hpm = hpm_num2[7];
  int max_thet = thet_num2[7];
  int max_phi = phi_num2[7];   

  int tm1[12] = {1,1,2,2,2,3,3,3,3,4,5,6};
  int tm2[12] = {2,7,3,4,7,4,5,6,7,5,6,7};

  double **********intr11 = new double*********[max_phi];
  double **********intr22 = new double*********[max_phi];
  double **********inter12 = new double*********[max_phi];
  double **********tot12 = new double*********[max_phi];
  double **********intrv11 = new double*********[max_phi];
  double **********intrv22 = new double*********[max_phi];
  double **********interv12 = new double*********[max_phi];
  double **********novdw12 = new double*********[max_phi];
  double **********interh12 = new double*********[max_phi];
  for (int a1=0;a1<max_phi;a1++)
  {
    intr11[a1] = new double********[max_thet];
    intr22[a1] = new double********[max_thet];
    inter12[a1] = new double********[max_thet];
    tot12[a1] = new double********[max_thet];
    intrv11[a1] = new double********[max_thet];
    intrv22[a1] = new double********[max_thet];
    interv12[a1] = new double********[max_thet];
    novdw12[a1] = new double********[max_thet];
    interh12[a1] = new double********[max_thet];
  }
  for (int a1=0;a1<max_phi;a1++)
  {
    for (int b1=0;b1<max_thet;b1++)
    {
      intr11[a1][b1] = new double*******[max_hpm];
      intr22[a1][b1] = new double*******[max_hpm];
      inter12[a1][b1] = new double*******[max_hpm];
      tot12[a1][b1] = new double*******[max_hpm];
      intrv11[a1][b1] = new double*******[max_hpm];
      intrv22[a1][b1] = new double*******[max_hpm];
      interv12[a1][b1] = new double*******[max_hpm];
      novdw12[a1][b1] = new double*******[max_hpm];
      interh12[a1][b1] = new double*******[max_hpm];
    }
  } 
  for (int a1=0;a1<max_phi;a1++)
  {
    for (int b1=0;b1<max_thet;b1++)
    {
      for (int c1=0;c1<max_hpm;c1++)
      {
        intr11[a1][b1][c1] = new double******[max_eta];
        intr22[a1][b1][c1] = new double******[max_eta];
        inter12[a1][b1][c1] = new double******[max_eta];
        tot12[a1][b1][c1] = new double******[max_eta];
        intrv11[a1][b1][c1] = new double******[max_eta];
        intrv22[a1][b1][c1] = new double******[max_eta];
        interv12[a1][b1][c1] = new double******[max_eta];
        novdw12[a1][b1][c1] = new double******[max_eta];
        interh12[a1][b1][c1] = new double******[max_eta];
      } 
    }
  }
  for (int a1=0;a1<max_phi;a1++)
  {
    for (int b1=0;b1<max_thet;b1++)
    {
      for (int c1=0;c1<max_hpm;c1++)
      {
        for (int d1=0;d1<max_eta;d1++)
        { 
          intr11[a1][b1][c1][d1] = new double*****[max_phi];
          intr22[a1][b1][c1][d1] = new double*****[max_phi];
          inter12[a1][b1][c1][d1] = new double*****[max_phi];
          tot12[a1][b1][c1][d1] = new double*****[max_phi];
          intrv11[a1][b1][c1][d1] = new double*****[max_phi];
          intrv22[a1][b1][c1][d1] = new double*****[max_phi];
          interv12[a1][b1][c1][d1] = new double*****[max_phi];
          novdw12[a1][b1][c1][d1] = new double*****[max_phi];
          interh12[a1][b1][c1][d1] = new double*****[max_phi];
        } 
      } 
    }
  }
  for (int a1=0;a1<max_phi;a1++)
  {
    for (int b1=0;b1<max_thet;b1++)
    {       
      for (int c1=0;c1<max_hpm;c1++)
      {
        for (int d1=0;d1<max_eta;d1++)
        {
          for (int a2=0;a2<max_phi;a2++)
          {
            intr11[a1][b1][c1][d1][a2] = new double****[max_thet];
            intr22[a1][b1][c1][d1][a2] = new double****[max_thet];
            inter12[a1][b1][c1][d1][a2] = new double****[max_thet];
            tot12[a1][b1][c1][d1][a2] = new double****[max_thet];
            intrv11[a1][b1][c1][d1][a2] = new double****[max_thet];
            intrv22[a1][b1][c1][d1][a2] = new double****[max_thet];
            interv12[a1][b1][c1][d1][a2] = new double****[max_thet];
            novdw12[a1][b1][c1][d1][a2] = new double****[max_thet];
            interh12[a1][b1][c1][d1][a2] = new double****[max_thet];
          }
        } 
      } 
    }
  }
  for (int a1=0;a1<max_phi;a1++)
  {
    for (int b1=0;b1<max_thet;b1++)
    {       
      for (int c1=0;c1<max_hpm;c1++)
      {
        for (int d1=0;d1<max_eta;d1++)
        {
          for (int a2=0;a2<max_phi;a2++)
          {
            for (int b2=0;b2<max_thet;b2++)
            {
              intr11[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
              intr22[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
              inter12[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
              tot12[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
              intrv11[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
              intrv22[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
              interv12[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
              novdw12[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
              interh12[a1][b1][c1][d1][a2][b2] = new double***[max_hpm];
            }
          }
        } 
      } 
    }
  }
  for (int a1=0;a1<max_phi;a1++)
  {
    for (int b1=0;b1<max_thet;b1++)
    {        
      for (int c1=0;c1<max_hpm;c1++)
      {
        for (int d1=0;d1<max_eta;d1++)
        {
          for (int a2=0;a2<max_phi;a2++)
          {
            for (int b2=0;b2<max_thet;b2++)
            {
              for (int c2=0;c2<max_hpm;c2++)
              {
                intr11[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
                intr22[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
                inter12[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
                tot12[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
                intrv11[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
                intrv22[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
                interv12[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
                novdw12[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
                interh12[a1][b1][c1][d1][a2][b2][c2] = new double**[max_eta];
              }
            }
          }
        } 
      } 
    }
  }
  for (int a1=0;a1<max_phi;a1++)
  {
    for (int b1=0;b1<max_thet;b1++)
    {
      for (int c1=0;c1<max_hpm;c1++)
      {
        for (int d1=0;d1<max_eta;d1++)
        {
          for (int a2=0;a2<max_phi;a2++)
          {
            for (int b2=0;b2<max_thet;b2++)
            {
              for (int c2=0;c2<max_hpm;c2++)
              {
                for (int d2=0;d2<max_eta;d2++)
                { 
                  intr11[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                  intr22[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                  inter12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                  tot12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                  intrv11[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                  intrv22[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                  interv12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                  novdw12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                  interh12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[8];
                }
              }
            }
          }
        }
      }
    }
  }
  for (int a1=0;a1<max_phi;a1++)
  {
    for (int b1=0;b1<max_thet;b1++)
    {
      for (int c1=0;c1<max_hpm;c1++)
      {
        for (int d1=0;d1<max_eta;d1++)
        {
          for (int a2=0;a2<max_phi;a2++)
          {
            for (int b2=0;b2<max_thet;b2++)
            {
              for (int c2=0;c2<max_hpm;c2++)
              {
                for (int d2=0;d2<max_eta;d2++)
                {
                  for (int a3=0;a3<7;a3++)
                  { 
                    intr11[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                    intr22[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                    inter12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                    tot12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                    intrv11[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                    intrv22[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                    interv12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                    novdw12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                    interh12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[8];
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  a1 = b1 = c1 = d1 = a2 = b2 = c2 = d2 = 0;
  for (int p = 0; p < 12; p++)
  {
    sprintf(file,"super_bihelix_H%i_H%i/super_bihelix_TM%i_TM%i.out",tm1[p],tm2[p],tm1[p],tm2[p]);
    ifstream filee (file);
    while (!filee.eof())
    {
      for (a1=0; a1 < phi_num[tm1[p]]; a1++)
      {
        for (b1=0; b1 < thet_num[tm1[p]]; b1++)
        {
          for (c1=0; c1 < hpm_num[tm1[p]]; c1++)
          {
            for (d1=0; d1 < eta_num[tm1[p]]; d1++)
            {
              for (a2=0; a2 < phi_num[tm2[p]]; a2++)
              {
                for (b2=0; b2 < thet_num[tm2[p]]; b2++)
                {
                  for (c2=0; c2 < hpm_num[tm2[p]]; c2++)
                  {
                    for (d2=0; d2 < eta_num[tm2[p]]; d2++)
                    {
                      getline(filee,linese);
                      istringstream linee(linese);
                      linee >> phiax >> theta >> hpma >> etaa >> phib >> thetb >> hpmb >> etab >> intr11x >> intr22x >> inter12x >> tot12x >> intrv11x >> intrv22x >> interv12x >> novdw12x >> interh12x;
                      if (filee.eof()) break;
//                      while (tm1[p] == 1 && etaa != eta1[1]) 
//                      {
//                        getline(filee,linese);
//                        istringstream linee(linese);
//                        linee >> phiax >> theta >> hpma >> etaa >> phib >> thetb >> hpmb >> etab >> intr11x >> intr22x >> inter12x >> tot12x >> intrv11x >> intrv22x >> interv12x >> novdw12x >> interh12x;
//                        if (filee.eof()) break;
//                      }
//                      if (filee.eof()) break;
                      phiaxx = phiax.substr(0,1);
                      if (phiaxx == "p")
                      {
                        getline(filee,linese);
                        istringstream linee(linese);
                        linee >> phiax >> theta >> hpma >> etaa >> phib >> thetb >> hpmb >> etab >> intr11x >> intr22x >> inter12x >> tot12x >> intrv11x >> intrv22x >> interv12x >> novdw12x >> interh12x;  
                      }
                      phia = atof (phiax.c_str()); 
                      intr11[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = intr11x;
                      intr22[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = intr22x;
                      inter12[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = inter12x;
                      tot12[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = tot12x;
                      intrv11[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = intrv11x;
                      intrv22[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = intrv22x;
                      interv12[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = interv12x;
                      novdw12[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = novdw12x;
                      interh12[a1][b1][c1][d1][a2][b2][c2][d2][tm1[p]][tm2[p]] = interh12x;     
                    } 
                  } 
                }
              }
            }
          }
        } 
      }
    } 
  }

  string m1lines,m2lines,m3lines,m4lines,m5lines,m6lines,m7lines;
  int m1phix,m1thetx,m1hpmx,m1etax,m2phix,m2thetx,m2hpmx,m2etax,m3phix,m3thetx,m3hpmx,m3etax,m4phix,m4thetx,m4hpmx,m4etax,m5phix,m5thetx,m5hpmx,m5etax,m6phix,m6thetx,m6hpmx,m6etax,m7phix,m7thetx,m7hpmx,m7etax;
  int m1phi[40],m1thet[40],m1hpm[40],m1eta[40],m2phi[40],m2thet[40],m2hpm[40],m2eta[40],m3phi[40],m3thet[40],m3hpm[40],m3eta[40],m4phi[40],m4thet[40],m4hpm[40],m4eta[40],m5phi[40],m5thet[40],m5hpm[40],m5eta[40],m6phi[40],m6thet[40],m6hpm[40],m6eta[40],m7phi[40],m7thet[40],m7hpm[40],m7eta[40];

  int j = 0;  
  int k = 0;
  int arr = atoi(argv[1]);
  int numb = atoi(argv[2]);
  int limt = atoi(argv[3]);
  int final = atoi(argv[4]); 
  int lst = atoi(argv[5]);
  int lstm = lst -1;
  int num1, num2, num3, num4, num5, num6, num7;
  int total;
  int limit;
//  int top = 2*arr;
//  int bot = 2*arr-1;
  int top = numb*arr;
  int bot = numb*arr-(numb-1);

  if (limt == 1)
  { 
   limit = 24;
  }
  if (limt == 2)
  {
    limit = 36;
  }
  if (limt == 3)
  {
    limit = 48;
  }

  ifstream mean1("Consensus_1.out");
  while (!mean1.eof())
  {
    j++;
    getline(mean1,m1lines);
    if (mean1.eof()) break;
    istringstream m1line(m1lines);
    m1line >> m1phix >> m1thetx >> m1hpmx >> m1etax;
    if (j <= top && j >= bot)
    {
      k++;
      m1phi[k] = m1phix;
      m1thet[k] = m1thetx;
      m1hpm[k] = m1hpmx;
      m1eta[k] = m1etax;
      num1 = k; 
    }
  }
  total = num1;

  j = 0;
  k = 0;
  ifstream mean2("Consensus_2.out");
  while (!mean2.eof())
  {
    j++;
    getline(mean2,m2lines);
    if (mean2.eof()) break;
    istringstream m2line(m2lines);
    m2line >> m2phix >> m2thetx >> m2hpmx >> m2etax;
    if (j <= limit)
    {
      k++;
      m2phi[j] = m2phix;
      m2thet[j] = m2thetx;
      m2hpm[j] = m2hpmx;
      m2eta[j] = m2etax;
    }
    num2 = k;
  }

  if (total > lst)
  {total = lst + 1;}
  else 
  {total = total*num2;}

  j = 0;
  k = 0;
  ifstream mean3("Consensus_3.out");
  while (!mean3.eof())
  {
    j++;
    getline(mean3,m3lines);
    if (mean3.eof()) break;
    istringstream m3line(m3lines);
    m3line >> m3phix >> m3thetx >> m3hpmx >> m3etax;
    if (j <= limit)
    {
      k++;
      m3phi[j] = m3phix;
      m3thet[j] = m3thetx;
      m3hpm[j] = m3hpmx;
      m3eta[j] = m3etax;
    }
    num3 = k;
  }

  if (total > lst)
  {total = lst + 1;}
  else 
  {total = total*num3;}

  j = 0;
  k = 0;
  ifstream mean4("Consensus_4.out");
  while (!mean4.eof())
  {
    j++;
    getline(mean4,m4lines);
    if (mean4.eof()) break;
    istringstream m4line(m4lines);
    m4line >> m4phix >> m4thetx >> m4hpmx >> m4etax;
    if (j <= limit)
    {
      k++;
      m4phi[j] = m4phix;
      m4thet[j] = m4thetx;
      m4hpm[j] = m4hpmx;
      m4eta[j] = m4etax;
    }
    num4 = k;
  }

  if (total > lst)
  {total = lst + 1;}
  else 
  {total = total*num4;}

  j = 0;
  k = 0;
  ifstream mean5("Consensus_5.out");
  while (!mean5.eof())
  {
    j++;
    getline(mean5,m5lines);
    if (mean5.eof()) break;
    istringstream m5line(m5lines);
    m5line >> m5phix >> m5thetx >> m5hpmx >> m5etax;
    if (j <= limit)
    {
      k++;
      m5phi[j] = m5phix;
      m5thet[j] = m5thetx;
      m5hpm[j] = m5hpmx;
      m5eta[j] = m5etax;
    }
    num5 = k;
  }

  if (total > lst)
  {total = lst + 1;}
  else 
  {total = total*num5;}

  j = 0;
  k = 0;
  ifstream mean6("Consensus_6.out");
  while (!mean6.eof())
  {
    j++;
    getline(mean6,m6lines);
    if (mean6.eof()) break;
    istringstream m6line(m6lines);
    m6line >> m6phix >> m6thetx >> m6hpmx >> m6etax;
    if (j <= limit)
    {
      k++;
      m6phi[j] = m6phix;
      m6thet[j] = m6thetx;
      m6hpm[j] = m6hpmx;
      m6eta[j] = m6etax;
    }
    num6 = k;
  }

  if (total > lst)
  {total = lst + 1;}
  else 
  {total = total*num6;}

  j = 0;
  k = 0;
  ifstream mean7("Consensus_7.out");
  while (!mean7.eof())
  {
    j++;
    getline(mean7,m7lines);
    if (mean7.eof()) break;
    istringstream m7line(m7lines);
    m7line >> m7phix >> m7thetx >> m7hpmx >> m7etax;
    if (j <= limit)
    {
      k++; 
      m7phi[j] = m7phix;
      m7thet[j] = m7thetx;
      m7hpm[j] = m7hpmx;
      m7eta[j] = m7etax;
    }
    num7 = k; 
  }

  if (total > lst)
  {total = lst + 1;}
  else 
  {total = total*num7;}

  if (total < lst)
  {
    lst = total;
    lstm = total - 1;
  }

  j = 0;
  long double tot_t[lst],inter_i[lst],nointv_v[lst],hbond_h[lst];
  map<string,long double> tot_i;  
  map<string,long double> inter_t;
  map<string,long double> nointv_t;
  map<string,long double> hbond_t;
  map<string,long double> tot_v; 
  map<string,long double> inter_v;
  map<string,long double> nointv_i;
  map<string,long double> hbond_i;
  map<string,long double> tot_h; 
  map<string,long double> inter_h;
  map<string,long double> nointv_h;
  map<string,long double> hbond_v;
  map<long double,string> struc_t;
  map<long double,string> struc_i;
  map<long double,string> struc_v;
  map<long double,string> struc_h;
  
  int a3,b3,c3,d3,a4,b4,c4,d4,a5,b5,c5,d5,a6,b6,c6,d6,a7,b7,c7,d7;
  j = 0; 
  for (int tm1 = 1; tm1 <= num1; tm1++) {
    for (int tm2 = 1; tm2 <= num2; tm2++) {
      for (int tm3 = 1; tm3 <= num3; tm3++) {
        for (int tm4 = 1; tm4 <= num4; tm4++) {
          for (int tm5 = 1; tm5 <= num5; tm5++) {
            for (int tm6 = 1; tm6 <= num6; tm6++) {
              for (int tm7 = 1; tm7 <= num7; tm7++) { 
                a1 = m1phi[tm1];
                b1 = m1thet[tm1];
                c1 = m1hpm[tm1];
                d1 = m1eta[tm1];
                a2 = m2phi[tm2];
                b2 = m2thet[tm2];
                c2 = m2hpm[tm2];
                d2 = m2eta[tm2];
                a3 = m3phi[tm3];
                b3 = m3thet[tm3];                
                c3 = m3hpm[tm3];                
                d3 = m3eta[tm3];
                a4 = m4phi[tm4];                
                b4 = m4thet[tm4];                
                c4 = m4hpm[tm4];                                
                d4 = m4eta[tm4];
                a5 = m5phi[tm5];                                
                b5 = m5thet[tm5];                               
                c5 = m5hpm[tm5];                                
                d5 = m5eta[tm5];
                a6 = m6phi[tm6];                                                
                b6 = m6thet[tm6];                  
                c6 = m6hpm[tm6];                
                d6 = m6eta[tm6];
                a7 = m7phi[tm7];                                                                
                b7 = m7thet[tm7];                                  
                c7 = m7hpm[tm7];                                
                d7 = m7eta[tm7];

//                               sprintf(struc,"H1 %*.0f %*.0f %*.1f %*.0f H2 %*.0f %*.0f %*.1f %*.0f H3 %*.0f %*.0f %*.1f %*.0f H4 %*.0f %*.0f %*.1f %*.0f H5 %*.0f %*.0f %*.1f %*.0f H6 %*.0f %*.0f %*.1f %*.0f H7 %*.0f %*.0f %*.1f %*.0f",4,phi1[a1+1],4,thet1[b1+1],5,hpm1[c1+1],4,eta1[d1+1],4,phi2[a2+1],4,thet2[b2+1],5,hpm2[c2+1],4,eta2[d2+1],4,phi3[a3+1],4,thet3[b3+1],5,hpm3[c3+1],4,eta3[d3+1],4,phi4[a4+1],4,thet4[b4+1],5,hpm4[c4+1],4,eta4[d4+1],4,phi5[a5+1],4,thet5[b5+1],5,hpm5[c5+1],4,eta5[d5+1],4,phi6[a6+1],4,thet6[b6+1],5,hpm6[c6+1],4,eta6[d6+1],4,phi7[a7+1],4,thet7[b7+1],5,hpm7[c7+1],4,eta7[d7+1]);
                               sprintf(struc,"H1 %.0f %.0f %.1f %.0f H2 %.0f %.0f %.1f %.0f H3 %.0f %.0f %.1f %.0f H4 %.0f %.0f %.1f %.0f H5 %.0f %.0f %.1f %.0f H6 %.0f %.0f %.1f %.0f H7 %.0f %.0f %.1f %.0f",phi1[a1+1],thet1[b1+1],hpm1[c1+1],eta1[d1+1],phi2[a2+1],thet2[b2+1],hpm2[c2+1],eta2[d2+1],phi3[a3+1],thet3[b3+1],hpm3[c3+1],eta3[d3+1],phi4[a4+1],thet4[b4+1],hpm4[c4+1],eta4[d4+1],phi5[a5+1],thet5[b5+1],hpm5[c5+1],eta5[d5+1],phi6[a6+1],thet6[b6+1],hpm6[c6+1],eta6[d6+1],phi7[a7+1],thet7[b7+1],hpm7[c7+1],eta7[d7+1]);
                               intr1 = (intr11[a1][b1][c1][d1][a2][b2][c2][d2][1][2]+intr11[a1][b1][c1][d1][a7][b7][c7][d7][1][7])/2;
                               intr2 = (intr22[a1][b1][c1][d1][a2][b2][c2][d2][1][2]+intr11[a2][b2][c2][d2][a3][b3][c3][d3][2][3]+intr11[a2][b2][c2][d2][a4][b4][c4][d4][2][4]+intr11[a2][b2][c2][d2][a7][b7][c7][d7][2][7])/4;
                               intr3 = (intr22[a2][b2][c2][d2][a3][b3][c3][d3][2][3]+intr11[a3][b3][c3][d3][a4][b4][c4][d4][3][4]+intr11[a3][b3][c3][d3][a5][b5][c5][d5][3][5]+intr11[a3][b3][c3][d3][a6][b6][c6][d6][3][6]+intr11[a3][b3][c3][d3][a7][b7][c7][d7][3][7])/5;
                               intr4 = (intr22[a2][b2][c2][d2][a4][b4][c4][d4][2][4]+intr22[a3][b3][c3][d3][a4][b4][c4][d4][3][4]+intr11[a4][b4][c4][d4][a5][b5][c5][d5][4][5])/3;
                               intr5 = (intr22[a3][b3][c3][d3][a5][b5][c5][d5][3][5]+intr22[a4][b4][c4][d4][a5][b5][c5][d5][4][5]+intr11[a5][b5][c5][d5][a6][b6][c6][d6][5][6])/3;
                               intr6 = (intr22[a3][b3][c3][d3][a6][b6][c6][d6][3][6]+intr22[a5][b5][c5][d5][a6][b6][c6][d6][5][6]+intr11[a6][b6][c6][d6][a7][b7][c7][d7][6][7])/3;
                               intr7 = (intr22[a1][b1][c1][d1][a7][b7][c7][d7][1][7]+intr22[a2][b2][c2][d2][a7][b7][c7][d7][2][7]+intr22[a3][b3][c3][d3][a7][b7][c7][d7][3][7]+intr22[a6][b6][c6][d6][a7][b7][c7][d7][6][7])/4;    
                               long double rnd = (rand() % 1000) + 1;
                               inter = inter12[a1][b1][c1][d1][a2][b2][c2][d2][1][2]+inter12[a1][b1][c1][d1][a7][b7][c7][d7][1][7]+inter12[a2][b2][c2][d2][a3][b3][c3][d3][2][3]+inter12[a2][b2][c2][d2][a4][b4][c4][d4][2][4]+inter12[a2][b2][c2][d2][a7][b7][c7][d7][2][7]+inter12[a3][b3][c3][d3][a4][b4][c4][d4][3][4]+inter12[a3][b3][c3][d3][a5][b5][c5][d5][3][5]+inter12[a3][b3][c3][d3][a6][b6][c6][d6][3][6]+inter12[a3][b3][c3][d3][a7][b7][c7][d7][3][7]+inter12[a4][b4][c4][d4][a5][b5][c5][d5][4][5]+inter12[a5][b5][c5][d5][a6][b6][c6][d6][5][6]+inter12[a6][b6][c6][d6][a7][b7][c7][d7][6][7];
			       tot = inter+int((intr1+intr2+intr3+intr4+intr5+intr6+intr7)*(pow(10,3)))/(pow(10,3));	
                               nointv = tot - interv12[a1][b1][c1][d1][a2][b2][c2][d2][1][2]-interv12[a1][b1][c1][d1][a7][b7][c7][d7][1][7]-interv12[a2][b2][c2][d2][a3][b3][c3][d3][2][3]-interv12[a2][b2][c2][d2][a4][b4][c4][d4][2][4]-interv12[a2][b2][c2][d2][a7][b7][c7][d7][2][7]-interv12[a3][b3][c3][d3][a4][b4][c4][d4][3][4]-interv12[a3][b3][c3][d3][a5][b5][c5][d5][3][5]-interv12[a3][b3][c3][d3][a6][b6][c6][d6][3][6]-interv12[a3][b3][c3][d3][a7][b7][c7][d7][3][7]-interv12[a4][b4][c4][d4][a5][b5][c5][d5][4][5]-interv12[a5][b5][c5][d5][a6][b6][c6][d6][5][6]-interv12[a6][b6][c6][d6][a7][b7][c7][d7][6][7];
                               hbond = interh12[a1][b1][c1][d1][a2][b2][c2][d2][1][2]+interh12[a1][b1][c1][d1][a7][b7][c7][d7][1][7]+interh12[a2][b2][c2][d2][a3][b3][c3][d3][2][3]+interh12[a2][b2][c2][d2][a4][b4][c4][d4][2][4]+interh12[a2][b2][c2][d2][a7][b7][c7][d7][2][7]+interh12[a3][b3][c3][d3][a4][b4][c4][d4][3][4]+interh12[a3][b3][c3][d3][a5][b5][c5][d5][3][5]+interh12[a3][b3][c3][d3][a6][b6][c6][d6][3][6]+interh12[a3][b3][c3][d3][a7][b7][c7][d7][3][7]+interh12[a4][b4][c4][d4][a5][b5][c5][d5][4][5]+interh12[a5][b5][c5][d5][a6][b6][c6][d6][5][6]+interh12[a6][b6][c6][d6][a7][b7][c7][d7][6][7];
                               if (j<lst)
                               {
				 if (j > 0)
				 {
				 for (int q = 0; q < j; q++)
				   {
				     if (tot == tot_t[q])
				     {
				       tot = tot + 0.000001;
				     }
				     if (inter == inter_i[q])
				     {
				       inter = inter + 0.000001;
				     }
				     if (nointv == nointv_v[q])
				     {
				       nointv = nointv + 0.000001;
				     }
				     if (hbond == hbond_h[q])
				     {
				       hbond = hbond + 0.000001;
				     }					 
				   }
				   }	  
                                 tot_t[j] = tot;
                                 inter_i[j] = inter;
                                 nointv_v[j] = nointv;
                                 hbond_h[j] = hbond;
                                 tot_i[struc] = tot;
                                 tot_v[struc] = tot;
                                 tot_h[struc] = tot;
                                 inter_t[struc] = inter;
                                 inter_v[struc] = inter;
                                 inter_h[struc] = inter;
                                 nointv_t[struc] = nointv;
                                 nointv_i[struc] = nointv;
                                 nointv_h[struc] = nointv;
                                 hbond_t[struc] = hbond;
                                 hbond_i[struc] = hbond;
                                 hbond_v[struc] = hbond;
                                 struc_t[tot_t[j]] = struc;
                                 struc_i[inter_i[j]] = struc;
                                 struc_v[nointv_v[j]] = struc;
                                 struc_h[hbond_h[j]] = struc;            
                                 if (j==lstm)
                                 {
                                 stable_sort(tot_t,tot_t+lst);
                                 stable_sort(inter_i,inter_i+lst);
                                 stable_sort(nointv_v,nointv_v+lst);
                                 stable_sort(hbond_h,hbond_h+lst);
                                 j++; 
                                 }
                                 j++; 
                               }     
                               if (j>lst)
                               {
				 if (j == lst + 2)
				 {	
                                 if (tot < tot_t[lstm])
                                 {
				   for (int q = 0; q < lst; q++)
				   {
				     if (tot == tot_t[q])
				     {
				       tot = tot + 0.000001;	
				     }	
				   }
                                   inter_t.erase (struc_t[tot_t[lstm]]);
                                   nointv_t.erase (struc_t[tot_t[lstm]]);
                                   hbond_t.erase (struc_t[tot_t[lstm]]);
                                   struc_t.erase (tot_t[lstm]);
                                   tot_t[lstm] = tot;
                                   struc_t[tot_t[lstm]] = struc;
                                   inter_t[struc] = inter;
                                   nointv_t[struc] = nointv;
                                   hbond_t[struc] = hbond;
                                   stable_sort(tot_t,tot_t+lst);
                                 }
                                 if (inter < inter_i[lstm])
                                 {
				   for (int q = 0; q < lst; q++)
                                   {
                                     if (inter == inter_i[q])
                                     {
                                       inter = inter + 0.000001;
                                     }
                                   }
                                   tot_i.erase (struc_i[inter_i[lstm]]);
                                   nointv_i.erase (struc_i[inter_i[lstm]]);
                                   hbond_i.erase (struc_i[inter_i[lstm]]);
                                   struc_i.erase (inter_i[lstm]);
                                   inter_i[lstm] = inter;
                                   struc_i[inter_i[lstm]] = struc;
                                   tot_i[struc] = tot;
                                   nointv_i[struc] = nointv;
                                   hbond_i[struc] = hbond;
                                   stable_sort(inter_i,inter_i+lst);
                                 }
                                 if (nointv < nointv_v[lstm])
                                 {
				   for (int q = 0; q < lst; q++)
                                   {
                                     if (nointv == nointv_v[q])
                                     {
                                       nointv = nointv + 0.000001;
                                     }
                                   }
                                   tot_v.erase (struc_v[nointv_v[lstm]]);
                                   inter_v.erase (struc_v[nointv_v[lstm]]);
                                   hbond_v.erase (struc_v[nointv_v[lstm]]);
                                   struc_v.erase (nointv_v[lstm]);
                                   nointv_v[lstm] = nointv;
                                   struc_v[nointv_v[lstm]] = struc;
                                   tot_v[struc] = tot;
                                   inter_v[struc] = inter;
                                   hbond_v[struc] = hbond;
                                   stable_sort(nointv_v,nointv_v+lst);
                                 }
                                 if (hbond < hbond_h[lstm])
                                 {
				   for (int q = 0; q < lst; q++)
                                   {
                                     if (hbond == hbond_h[q])
                                     {
                                       hbond = hbond + 0.000001;
                                     }
                                   }
                                   tot_h.erase (struc_h[hbond_h[lstm]]);
                                   inter_h.erase (struc_h[hbond_h[lstm]]);
                                   nointv_h.erase (struc_h[hbond_h[lstm]]);
                                   struc_h.erase (hbond_h[lstm]);
                                   hbond_h[lstm] = hbond;
                                   struc_h[hbond_h[lstm]] = struc;
                                   tot_h[struc] = tot;
                                   inter_h[struc] = inter;
                                   nointv_h[struc] = nointv;
                                   stable_sort(hbond_h,hbond_h+lst);
                                 }
			       }
			       j = lst + 2;		
                               }
   
  }}}}}}}

  sprintf(totoutx,"Total_Energy_%s",argv[1]);
  sprintf(interoutx,"Interhelical_Energy_%s",argv[1]);
  sprintf(nointvoutx,"No_Interhelical_VDW_%s",argv[1]);
  sprintf(hbondoutx,"Interhelical_Hbond_%s",argv[1]); 
  ofstream totout(totoutx);
  ofstream interout(interoutx);
  ofstream nointvout(nointvoutx);
  ofstream hbondout(hbondoutx);
  for (int i = 0; i < lst; i++)
  {
    sprintf(tout,"%s %Lf %Lf %Lf %Lf",struc_t[tot_t[i]],tot_t[i],inter_t[struc_t[tot_t[i]]],nointv_t[struc_t[tot_t[i]]],hbond_t[struc_t[tot_t[i]]]);
    sprintf(iout,"%s %Lf %Lf %Lf %Lf",struc_i[inter_i[i]],tot_i[struc_i[inter_i[i]]],inter_i[i],nointv_i[struc_i[inter_i[i]]],hbond_i[struc_i[inter_i[i]]]);
    sprintf(vout,"%s %Lf %Lf %Lf %Lf",struc_v[nointv_v[i]],tot_v[struc_v[nointv_v[i]]],inter_v[struc_v[nointv_v[i]]],nointv_v[i],hbond_v[struc_v[nointv_v[i]]]);
    sprintf(hout,"%s %Lf %Lf %Lf %Lf",struc_h[hbond_h[i]],tot_h[struc_h[hbond_h[i]]],inter_h[struc_h[hbond_h[i]]],nointv_h[struc_h[hbond_h[i]]],hbond_h[i]);
    totout << tout << endl;
    interout << iout << endl;
    nointvout << vout << endl;
    hbondout << hout << endl;
  }
  
  char end[100],filex[100];
  if (final == 1)
  {
    int v = 1;
    while (v < arr)
    {
      sprintf(filex,"Interhelical_Hbond_%i",v);
      fstream file(filex);
      if (file.is_open()) 
      {
        v++;
        file.close();
      }
    }
    lst = atoi(argv[5]);
    sprintf(end,"/project/Biogroup/Software/GEnsemble/programs/superbihelix/mean_field_order %i %i",arr,lst);
    system(end);
  }
   
}

