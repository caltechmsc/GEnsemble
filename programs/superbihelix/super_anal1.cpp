#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
#include <sstream>
#include <map>
using namespace std;
main (int argc, char* argv[])
{
  char ins[50];
  char file[100];
  char outx[10];
  string linesa,tmx,ang,linese;
  char struc[200],struc2[200];
  char totoutx[100],totout0x[100],interoutx[100],nointvoutx[100],hbondoutx[100];
  char tout[500],tout0[500],iout[500],vout[500],hout[500];
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
  
  int max_eta = eta_num2[7]+1;
  int max_hpm = hpm_num2[7]+1;
  int max_thet = thet_num2[7]+1;
  int max_phi = phi_num2[7]+1;   

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
                  intr11[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
                  intr22[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
                  inter12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
                  tot12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
                  intrv11[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
                  intrv22[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
                  interv12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
                  novdw12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
                  interh12[a1][b1][c1][d1][a2][b2][c2][d2] = new double*[7];
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
                    intr11[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
                    intr22[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
                    inter12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
                    tot12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
                    intrv11[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
                    intrv22[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
                    interv12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
                    novdw12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
                    interh12[a1][b1][c1][d1][a2][b2][c2][d2][a3] = new double[7];
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
  int total, numb, numb1;
  numb = 2000;
  total = (phi_num[1])*(thet_num[1])*(hpm_num[1])*(eta_num[1])*(phi_num[2])*(thet_num[2])*(hpm_num[2])*(eta_num[2])*(phi_num[3])*(thet_num[3])*(hpm_num[3])*(eta_num[3])*(phi_num[7])*(thet_num[7])*(hpm_num[7])*(eta_num[7]);
  if (total < 2000)
  {numb = total;}
  numb1 = numb - 1;  
  
  int j = 0;
  long double tot_t[2000],inter_i[2000],nointv_v[2000],hbond_h[2000];
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
  map<long double,string> struc_0;
  map<long double,string> struc_i;
  map<long double,string> struc_v;
  map<long double,string> struc_h;
  srand(time(0));

  j = 0; 
  for (int a1 = 0; a1 < phi_num[1]; a1++) {
   for (int b1 = 0; b1 < thet_num[1]; b1++) {
    for (int c1 = 0; c1 < hpm_num[1]; c1++) {
     for (int d1 = 0; d1 < eta_num[1]; d1++) { 
      for (int a2 = 0; a2 < phi_num[2]; a2++) {
       for (int b2 = 0; b2 < thet_num[2]; b2++) {
        for (int c2 = 0; c2 < hpm_num[2]; c2++) {
         for (int d2 = 0; d2 < eta_num[2]; d2++) {
          for (int a3 = 0; a3 < phi_num[3]; a3++) {
           for (int b3 = 0; b3 < thet_num[3]; b3++) {
            for (int c3 = 0; c3 < hpm_num[3]; c3++) {
             for (int d3 = 0; d3 < eta_num[3]; d3++) {
                          for (int a7 = 0; a7 < phi_num[7]; a7++) {
                           for (int b7 = 0; b7 < thet_num[7]; b7++) {
                            for (int c7 = 0; c7 < hpm_num[7]; c7++) {
                             for (int d7 = 0; d7 < eta_num[7]; d7++) {
                               sprintf(struc,"H1 %.0f %.0f %.0f %.0f H2 %.0f %.0f %.0f %.0f H3 %.0f %.0f %.0f %.0f H7 %.0f %.0f %.0f %.0f",phi1[a1+1],thet1[b1+1],hpm1[c1+1],eta1[d1+1],phi2[a2+1],thet2[b2+1],hpm2[c2+1],eta2[d2+1],phi3[a3+1],thet3[b3+1],hpm3[c3+1],eta3[d3+1],phi7[a7+1],thet7[b7+1],hpm7[c7+1],eta7[d7+1]);
                               sprintf(struc2,"%i %i %i %i %i %i %i %i %i %i %i %i %i %i %i %i",a1,b1,c1,d1,a2,b2,c2,d2,a3,b3,c3,d3,a7,b7,c7,d7);  
                               intr1 = (intr11[a1][b1][c1][d1][a2][b2][c2][d2][1][2]+intr11[a1][b1][c1][d1][a7][b7][c7][d7][1][7])/2;
                               intr2 = (intr22[a1][b1][c1][d1][a2][b2][c2][d2][1][2]+intr11[a2][b2][c2][d2][a3][b3][c3][d3][2][3]+intr11[a2][b2][c2][d2][a7][b7][c7][d7][2][7])/3;
                               intr3 = (intr22[a2][b2][c2][d2][a3][b3][c3][d3][2][3]+intr11[a3][b3][c3][d3][a7][b7][c7][d7][3][7])/2;
                               intr7 = (intr22[a1][b1][c1][d1][a7][b7][c7][d7][1][7]+intr22[a2][b2][c2][d2][a7][b7][c7][d7][2][7]+intr22[a3][b3][c3][d3][a7][b7][c7][d7][3][7])/3;    
                               long double rnd = (rand() % 1000) + 1;
                               inter = (rnd/10000)+inter12[a1][b1][c1][d1][a2][b2][c2][d2][1][2]+inter12[a1][b1][c1][d1][a7][b7][c7][d7][1][7]+inter12[a2][b2][c2][d2][a3][b3][c3][d3][2][3]+inter12[a2][b2][c2][d2][a7][b7][c7][d7][2][7]+inter12[a3][b3][c3][d3][a7][b7][c7][d7][3][7];
                               tot = intr1+intr2+intr3+intr7+inter;
                               nointv = tot - interv12[a1][b1][c1][d1][a2][b2][c2][d2][1][2]-interv12[a1][b1][c1][d1][a7][b7][c7][d7][1][7]-interv12[a2][b2][c2][d2][a3][b3][c3][d3][2][3]-interv12[a2][b2][c2][d2][a7][b7][c7][d7][2][7]-interv12[a3][b3][c3][d3][a7][b7][c7][d7][3][7];
                               hbond = (rnd/10000)+interh12[a1][b1][c1][d1][a2][b2][c2][d2][1][2]+interh12[a1][b1][c1][d1][a7][b7][c7][d7][1][7]+interh12[a2][b2][c2][d2][a3][b3][c3][d3][2][3]+interh12[a2][b2][c2][d2][a7][b7][c7][d7][2][7]+interh12[a3][b3][c3][d3][a7][b7][c7][d7][3][7];
                               if (j<numb)
                               {
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
                                 struc_0[tot_t[j]] = struc2;
                                 struc_t[tot_t[j]] = struc;
                                 struc_i[inter_i[j]] = struc;
                                 struc_v[nointv_v[j]] = struc;
                                 struc_h[hbond_h[j]] = struc;            
                                 if (j==numb1)
                                 {
                                 stable_sort(tot_t,tot_t+numb);
                                 stable_sort(inter_i,inter_i+numb);
                                 stable_sort(nointv_v,nointv_v+numb);
                                 stable_sort(hbond_h,hbond_h+numb);
                                 j++; 
                                 }
                                 j++; 
                               }     
                               if (j>2000)
                               { 
                                 j = numb+1; 
                                 if (tot < tot_t[numb1])
                                 {
                                   inter_t.erase (struc_t[tot_t[numb1]]);
                                   nointv_t.erase (struc_t[tot_t[numb1]]);
                                   hbond_t.erase (struc_t[tot_t[numb1]]);
                                   struc_t.erase (tot_t[numb1]);
                                   struc_0.erase (tot_t[numb1]);
                                   tot_t[numb1] = tot;
                                   struc_t[tot_t[numb1]] = struc;
                                   struc_0[tot_t[numb1]] = struc2;
                                   inter_t[struc] = inter;
                                   nointv_t[struc] = nointv;
                                   hbond_t[struc] = hbond;
                                   stable_sort(tot_t,tot_t+numb);
                                 }
                                 if (inter < inter_i[numb1])
                                 {
                                   tot_i.erase (struc_i[inter_i[numb1]]);
                                   nointv_i.erase (struc_i[inter_i[numb1]]);
                                   hbond_i.erase (struc_i[inter_i[numb1]]);
                                   struc_i.erase (inter_i[numb1]);
                                   inter_i[numb1] = inter;
                                   struc_i[inter_i[numb1]] = struc;
                                   tot_i[struc] = tot;
                                   nointv_i[struc] = nointv;
                                   hbond_i[struc] = hbond;
                                   stable_sort(inter_i,inter_i+numb);
                                 }
                                 if (nointv < nointv_v[numb1])
                                 {
                                   tot_v.erase (struc_v[nointv_v[numb1]]);
                                   inter_v.erase (struc_v[nointv_v[numb1]]);
                                   hbond_v.erase (struc_v[nointv_v[numb1]]);
                                   struc_v.erase (nointv_v[numb1]);
                                   nointv_v[numb1] = nointv;
                                   struc_v[nointv_v[numb1]] = struc;
                                   tot_v[struc] = tot;
                                   inter_v[struc] = inter;
                                   hbond_v[struc] = hbond;
                                   stable_sort(nointv_v,nointv_v+numb);
                                 }
                                 if (hbond < hbond_h[numb1])
                                 {
                                   tot_h.erase (struc_h[hbond_h[numb1]]);
                                   inter_h.erase (struc_h[hbond_h[numb1]]);
                                   nointv_h.erase (struc_h[hbond_h[numb1]]);
                                   struc_h.erase (hbond_h[numb1]);
                                   hbond_h[numb1] = hbond;
                                   struc_h[hbond_h[numb1]] = struc;
                                   tot_h[struc] = tot;
                                   inter_h[struc] = inter;
                                   nointv_h[struc] = nointv;
                                   stable_sort(hbond_h,hbond_h+numb);
                                 }
                               }
   
  }}}}}}}}}}}}}}}}

  sprintf(totout0x,"Total_Energy_1_temp");
  ofstream totout0(totout0x);
  for (int i = 0; i < numb; i++)
  {
    sprintf(tout0,"%s",struc_0[tot_t[i]]);
    totout0 << tout0 << endl;
  }
}
