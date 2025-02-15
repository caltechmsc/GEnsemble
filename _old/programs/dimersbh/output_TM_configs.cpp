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
  string linesa,tmx,ang,lines1,lines2,lines3,lines4,lines5,lines6,lines7;
  char phiz[5],etaz[5],thetz[5],hpmz[5];
  int phizn,etazn,thetzn,hpmzn;
  char TM1outx[100],TM2outx[100],TM3outx[100],TM4outx[100],TM5outx[100],TM6outx[100],TM7outx[100];
  char out1[200],out2[200],out3[200],out4[200],out5[200],out6[200],out7[200];
  char out1p[200],out2p[200],out3p[200],out4p[200],out5p[200],out6p[200],out7p[200];
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
        {        
	linea >> yay;
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

  sprintf(TM1outx,"TM1_configs.out");
  ofstream TM1out(TM1outx); 
  sprintf(out1p,"Thet1         Phi1         Eta1         HPM1         Rank");
  TM1out << out1p << endl;
  ifstream cons1 ("Consensus_1.out");
  int r = 0;
  while (!cons1.eof())
  {
    r++;
    getline(cons1,lines1);
    istringstream line1(lines1);
    if (cons1.eof()) break;
    line1 >> phizn >> thetzn >> hpmzn >> etazn;
    sprintf(out1,"%*.0f   %*.0f   %*.0f   %*.1f   %*i",5,thet1[thetzn+1],10,phi1[phizn+1],10,eta1[etazn+1],10,hpm1[hpmzn+1],10,r);
    TM1out << out1 << endl;
  }

  sprintf(TM2outx,"TM2_configs.out");
  ofstream TM2out(TM2outx);
  sprintf(out2p,"Thet2         Phi2         Eta2         HPM2         Rank");
  TM2out << out2p << endl;
  ifstream cons2 ("Consensus_2.out");
  r = 0;
  while (!cons2.eof())
  {
    r++;
    getline(cons2,lines2);
    istringstream line2(lines2);
    if (cons2.eof()) break;
    line2 >> phizn >> thetzn >> hpmzn >> etazn;
    sprintf(out2,"%*.0f   %*.0f   %*.0f   %*.1f   %*i",5,thet2[thetzn+1],10,phi2[phizn+1],10,eta2[etazn+1],10,hpm2[hpmzn+1],10,r);
    TM2out << out2 << endl;
  }

  sprintf(TM3outx,"TM3_configs.out");
  ofstream TM3out(TM3outx);
  sprintf(out3p,"Thet3         Phi3         Eta3         HPM3         Rank");
  TM3out << out3p << endl;
  ifstream cons3 ("Consensus_3.out");
  r = 0;
  while (!cons3.eof())
  {
    r++;
    getline(cons3,lines3);
    istringstream line3(lines3);
    if (cons3.eof()) break;
    line3 >> phizn >> thetzn >> hpmzn >> etazn;
    sprintf(out3,"%*.0f   %*.0f   %*.0f   %*.1f   %*i",5,thet3[thetzn+1],10,phi3[phizn+1],10,eta3[etazn+1],10,hpm3[hpmzn+1],10,r);
    TM3out << out3 << endl;
  }

  sprintf(TM4outx,"TM4_configs.out");
  ofstream TM4out(TM4outx);
  sprintf(out4p,"Thet4         Phi4         Eta4         HPM4         Rank");
  TM4out << out4p << endl;
  ifstream cons4 ("Consensus_4.out");
  r = 0;
  while (!cons4.eof())
  {
    r++;
    getline(cons4,lines4);
    istringstream line4(lines4);
    if (cons4.eof()) break;
    line4 >> phizn >> thetzn >> hpmzn >> etazn;
    sprintf(out4,"%*.0f   %*.0f   %*.0f   %*.1f   %*i",5,thet4[thetzn+1],10,phi4[phizn+1],10,eta4[etazn+1],10,hpm4[hpmzn+1],10,r);
    TM4out << out4 << endl;
  }

  sprintf(TM5outx,"TM5_configs.out");
  ofstream TM5out(TM5outx);
  sprintf(out5p,"Thet5         Phi5         Eta5         HPM5         Rank");
  TM5out << out5p << endl;
  ifstream cons5 ("Consensus_5.out");
  r = 0;
  while (!cons5.eof())
  {
    r++;
    getline(cons5,lines5);
    istringstream line5(lines5);
    if (cons5.eof()) break;
    line5 >> phizn >> thetzn >> hpmzn >> etazn;
    sprintf(out5,"%*.0f   %*.0f   %*.0f   %*.1f   %*i",5,thet5[thetzn+1],10,phi5[phizn+1],10,eta5[etazn+1],10,hpm5[hpmzn+1],10,r);
    TM5out << out5 << endl;
  }

  sprintf(TM6outx,"TM6_configs.out");
  ofstream TM6out(TM6outx);
  sprintf(out6p,"Thet6         Phi6         Eta6         HPM6         Rank");
  TM6out << out6p << endl;
  ifstream cons6 ("Consensus_6.out");
  r = 0;
  while (!cons6.eof())
  {
    r++;
    getline(cons6,lines6);
    istringstream line6(lines6);
    if (cons6.eof()) break;
    line6 >> phizn >> thetzn >> hpmzn >> etazn;
    sprintf(out6,"%*.0f   %*.0f   %*.0f   %*.1f   %*i",5,thet6[thetzn+1],10,phi6[phizn+1],10,eta6[etazn+1],10,hpm6[hpmzn+1],10,r);
    TM6out << out6 << endl;
  }

  sprintf(TM7outx,"TM7_configs.out");
  ofstream TM7out(TM7outx);
  sprintf(out7p,"Thet7         Phi7         Eta7         HPM7         Rank");
  TM7out << out7p << endl;
  ifstream cons7 ("Consensus_7.out");
  r = 0;
  while (!cons7.eof())
  {
    r++;
    getline(cons7,lines7);
    istringstream line7(lines7);
    if (cons7.eof()) break;
    line7 >> phizn >> thetzn >> hpmzn >> etazn;
    sprintf(out7,"%*.0f   %*.0f   %*.0f   %*.1f   %*i",5,thet7[thetzn+1],10,phi7[phizn+1],10,eta7[etazn+1],10,hpm7[hpmzn+1],10,r);
    TM7out << out7 << endl;
  }

}
