#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
#include <sstream>
using namespace std;
main (int argc, char* argv[])
{
  int hel1, hel2;
  int p;
  char pr[100],pl[100],mg[300];
  char c[100];
  char s[100], t[100],oute[300],first[300];
  string linet[10],lineta[10];
  string lines,linesa,tmx,ang,linees;
  string st,tm,resa,resna;
  char tmhel1[3],tmhel2[3],outeng[100];
  char al1[20], al2[20];
  string res[10],resn[10];
  double eta1[30],phi1[20],thet1[20],hpm1[20];
  double eta2[30],phi2[20],thet2[20],hpm2[20];
  double eta3[30],phi3[20],thet3[20],hpm3[20];
  double eta4[30],phi4[20],thet4[20],hpm4[20];
  double eta5[30],phi5[20],thet5[20],hpm5[20];
  double eta6[30],phi6[20],thet6[20],hpm6[20];
  double eta7[30],phi7[20],thet7[20],hpm7[20];
  double phi_new1, thet_new1, eta_new1, hpm_new1;
  double phi_new2, thet_new2, eta_new2, hpm_new2;
  double intr11, inter11, intrv11, intrc11, intrh11, intr22, inter22, intrv22, intrc22, intrh22, inter12,
 interv12, interc12, interh12, tote;
  double novdw;
  int eta_num[8] = {0},phi_num[8] = {0},thet_num[8] = {0},hpm_num[8] = {0};
  double xxa,yya,hpma,theta,phia,etaa,yay;
  double xx[10],yy[10],hpm[10],thet[10],phi[10],eta[10];
  sprintf(s,"cp %s super.bgf",argv[1]);
  system(s);
  sprintf(t, "cp %s super.mfta",argv[2]);
  system(t);
  system("/project/Biogroup/scripts/perl/bgf2pdb.pl super.bgf > super.pdb ");
  system("/project/Biogroup/Software/devel/GEnsemble2/programs/templates/OPM/GetTemplate.pl -m super.mfta -p super.pdb > super.template");
  string filea = "super.template";
  ifstream infilea (filea.c_str());
  int i = 0;
  while (!infilea.eof())
  {
    i++;
    getline(infilea,linesa);
    istringstream linea(linesa);
    lineta[i] = linesa;
    linea >> st >> tm >> xxa >> yya >> hpma >> theta >> phia >> etaa >> resa >> resna;
    xx[i] = xxa;
    yy[i] = yya;
    hpm[i] = hpma;
    thet[i] = theta;
    phi[i] = phia;
    eta[i] = etaa;
    res[i] = resa;
    resn[i] = resna;
  }
  int etaz1=0,etaz2=0,etaz3=0,etaz4=0,etaz5=0,etaz6=0,etaz7=0;
  int phiz1=0,phiz2=0,phiz3=0,phiz4=0,phiz5=0,phiz6=0,phiz7=0;
  int hpmz1=0,hpmz2=0,hpmz3=0,hpmz4=0,hpmz5=0,hpmz6=0,hpmz7=0;
  int thetz1=0,thetz2=0,thetz3=0,thetz4=0,thetz5=0,thetz6=0,thetz7=0; 
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
        etaz1++;
        linea >> yay;
        eta1[j] = yay;
        eta_num[1] = j;
        }
        if (ang == "phi")
        {
        phiz1++;
        linea >> yay;
        phi1[j] = yay;
        phi_num[1] = j;
        }
        if (ang == "theta")
        {
        thetz1++;
        linea >> yay;
        thet1[j] = yay;
        thet_num[1] = j;
        }
        if (ang == "HPM")
        {
        hpmz1++;        
        linea >> yay;
        hpm1[j] = yay;
        hpm_num[1] = j;
        }
      }
    }

    if (etaz1 == 0)
    {
      eta1[1] = 0;
      eta_num[1] = 1;
    }
    if (phiz1 == 0)
    {
      phi1[1] = 0;
      phi_num[1] = 1;
    }
    if (thetz1 == 0)
    {
      thet1[1] = 0;
      thet_num[1] = 1;
    }
    if (hpmz1 == 0)
    {
      hpm1[1] = hpm[1];
      hpm_num[1] = 1;
    }

    if (tmx == "TM2")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        etaz2++;
        linea >> yay;
        eta2[j] = yay;
        eta_num[2] = j;
        }
        if (ang == "phi")
        {
        phiz2++;
        linea >> yay;
        phi2[j] = yay;
        phi_num[2] = j;
        }
        if (ang == "theta")
        {
        thetz2++;
        linea >> yay;
        thet2[j] = yay;
        thet_num[2] = j;
        }
        if (ang == "HPM")
        {
        hpmz2++;
        linea >> yay;
        hpm2[j] = yay;
        hpm_num[2] = j;
        }
      }
    }

    if (etaz2 == 0)
    {
      eta2[1] = 0;
      eta_num[2] = 1;
    } 
    if (phiz2 == 0)
    { 
      phi2[1] = 0; 
      phi_num[2] = 1;
    }
    if (thetz2 == 0)
    {
      thet2[1] = 0;
      thet_num[2] = 1;
    }
    if (hpmz2 == 0)
    {
      hpm2[1] = hpm[2];
      hpm_num[2] = 1;
    }

    if (tmx == "TM3")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        etaz3++;
        linea >> yay;
        eta3[j] = yay;
        eta_num[3] = j;
        }
        if (ang == "phi")
        {
        phiz3++;
        linea >> yay;
        phi3[j] = yay;
        phi_num[3] = j;
        }
        if (ang == "theta")
        {
        thetz3++;
        linea >> yay;
        thet3[j] = yay;
        thet_num[3] = j;
        }
        if (ang == "HPM")
        {
        hpmz3++; 
        linea >> yay;
        hpm3[j] = yay;
        hpm_num[3] = j;
        }
      }
    }

    if (etaz3 == 0)
    {
      eta3[1] = 0;
      eta_num[3] = 1;
    } 
    if (phiz3 == 0)
    {
      phi3[1] = 0;
      phi_num[3] = 1;
    }
    if (thetz3 == 0)
    {
      thet3[1] = 0;
      thet_num[3] = 1;
    }
    if (hpmz3 == 0)
    {
      hpm3[1] = hpm[3];
      hpm_num[3] = 1;
    }

    if (tmx == "TM4")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        etaz4++;
        linea >> yay;
        eta4[j] = yay;
        eta_num[4] = j;
        }
        if (ang == "phi")
        {
        phiz4++;
        linea >> yay;
        phi4[j] = yay;
        phi_num[4] = j;
        }
        if (ang == "theta")
        {
        thetz4++;
        linea >> yay;
        thet4[j] = yay;
        thet_num[4] = j;
        }
        if (ang == "HPM")
        {
        hpmz4++;
        linea >> yay;
        hpm4[j] = yay;
        hpm_num[4] = j;
        }
      }
    }

    if (etaz4 == 0)
    {
      eta4[1] = 0;
      eta_num[4] = 1;
    } 
    if (phiz4 == 0)
    { 
      phi4[1] = 0;
      phi_num[4] = 1;
    }
    if (thetz4 == 0)
    {
      thet4[1] = 0;
      thet_num[4] = 1;
    }
    if (hpmz4 == 0)
    {
      hpm4[1] = hpm[4];
      hpm_num[4] = 1;
    }

    if (tmx == "TM5")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        etaz5++;
        linea >> yay;
        eta5[j] = yay;
        eta_num[5] = j;
        }
        if (ang == "phi")
        {
        phiz5++;
        linea >> yay;
        phi5[j] = yay;
        phi_num[5] = j;
        }
        if (ang == "theta")
        {
        thetz5++;
        linea >> yay;
        thet5[j] = yay;
        thet_num[5] = j;
        }
        if (ang == "HPM")
        {
        hpmz5++;
        linea >> yay;
        hpm5[j] = yay;
        hpm_num[5] = j;
        }
      }
    }

    if (etaz5 == 0)
    {
      eta5[1] = 0;
      eta_num[5] = 1;
    }
    if (phiz5 == 0)
    {
      phi5[1] = 0;
      phi_num[5] = 1;
    }
    if (thetz5 == 0)
    {
      thet5[1] = 0;
      thet_num[5] = 1;
    }
    if (hpmz5 == 0)
    {
      hpm5[1] = hpm[5];
      hpm_num[5] = 1;
    }

    if (tmx == "TM6")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        etaz6++;
        linea >> yay;
        eta6[j] = yay;
        eta_num[6] = j;
        }
        if (ang == "phi")
        {
        phiz6++;
        linea >> yay;
        phi6[j] = yay;
        phi_num[6] = j;
        }
        if (ang == "theta")
        {
        thetz6++;
        linea >> yay;
        thet6[j] = yay;
        thet_num[6] = j;
        }
        if (ang == "HPM")
        {
        hpmz6++;
        linea >> yay;
        hpm6[j] = yay;
        hpm_num[6] = j;
        }
      }
    }

    if (etaz6 == 0)
    {
      eta6[1] = 0;
      eta_num[6] = 1;
    }
    if (phiz6 == 0)
    {
      phi6[1] = 0;
      phi_num[6] = 1;
    }
    if (thetz6 == 0)
    {
      thet6[1] = 0;
      thet_num[6] = 1;
    }
    if (hpmz6 == 0)
    {
      hpm6[1] = hpm[6];
      hpm_num[6] = 1;
    }

    if (tmx == "TM7")
    {
      linea >> ang;
      while (linea.good())
      {
      j++;
        if (ang == "eta")
        {
        etaz7++;
        linea >> yay;
        eta7[j] = yay;
        eta_num[7] = j;
        }
        if (ang == "phi")
        {
        phiz7++;
        linea >> yay;
        phi7[j] = yay;
        phi_num[7] = j;
        }
        if (ang == "theta")
        {
        thetz7++;
        linea >> yay;
        thet7[j] = yay;
        thet_num[7] = j;
        }
        if (ang == "HPM")
        {
        hpmz7++;
        linea >> yay;
        hpm7[j] = yay;
        hpm_num[7] = j;
        }
      }
    }

    if (etaz7 == 0)
    {
      eta7[1] = 0;
      eta_num[7] = 1;
    } 
    if (phiz7 == 0)
    {
      phi7[1] = 0;
      phi_num[7] = 1;
    }
    if (thetz7 == 0)
    {
      thet7[1] = 0;
      thet_num[7] = 1;
    }
    if (hpmz7 == 0)
    {
      hpm7[1] = hpm[7];
      hpm_num[7] = 1;
    }
  }

  system("mv angles.txt angles.txt.original");

  char outang[100], outxx[100];  
  sprintf(outang,"angles.txt");
  ofstream outangout(outang);
  int bb;

  sprintf(outxx,"TM1 eta");
  outangout << outxx;
  for (bb = 1; bb <= eta_num[1]; bb++)
  {
    outangout << " ";
    outangout << eta1[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM1 HPM");
  outangout << outxx;
  for (bb = 1; bb <= hpm_num[1]; bb++)
  {
    outangout << " ";
    outangout << hpm1[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM1 phi");
  outangout << outxx;
  for (bb = 1; bb <= phi_num[1]; bb++)
  {
    outangout << " ";
    outangout << phi1[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM1 theta");
  outangout << outxx;
  for (bb = 1; bb <= thet_num[1]; bb++)
  {
    outangout << " ";
    outangout << thet1[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM2 eta");
  outangout << outxx;
  for (bb = 1; bb <= eta_num[2]; bb++)
  {
    outangout << " ";
    outangout << eta2[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM2 HPM");
  outangout << outxx;
  for (bb = 1; bb <= hpm_num[2]; bb++)
  {
    outangout << " ";
    outangout << hpm2[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM2 phi");
  outangout << outxx;
  for (bb = 1; bb <= phi_num[2]; bb++)
  {
    outangout << " ";
    outangout << phi2[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM2 theta");
  outangout << outxx;
  for (bb = 1; bb <= thet_num[2]; bb++)
  {
    outangout << " ";
    outangout << thet2[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM3 eta");
  outangout << outxx;
  for (bb = 1; bb <= eta_num[3]; bb++)
  {
    outangout << " ";
    outangout << eta3[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM3 HPM");
  outangout << outxx;
  for (bb = 1; bb <= hpm_num[3]; bb++)
  {
    outangout << " ";
    outangout << hpm3[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM3 phi");
  outangout << outxx;
  for (bb = 1; bb <= phi_num[3]; bb++)
  {
    outangout << " ";
    outangout << phi3[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM3 theta");
  outangout << outxx;
  for (bb = 1; bb <= thet_num[3]; bb++)
  {
    outangout << " ";
    outangout << thet3[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM4 eta");
  outangout << outxx;
  for (bb = 1; bb <= eta_num[4]; bb++)
  {
    outangout << " ";
    outangout << eta4[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM4 HPM");
  outangout << outxx;
  for (bb = 1; bb <= hpm_num[4]; bb++)
  {
    outangout << " ";
    outangout << hpm4[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM4 phi");
  outangout << outxx;
  for (bb = 1; bb <= phi_num[4]; bb++)
  {
    outangout << " ";
    outangout << phi4[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM4 theta");
  outangout << outxx;
  for (bb = 1; bb <= thet_num[4]; bb++)
  {
    outangout << " ";
    outangout << thet4[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM5 eta");
  outangout << outxx;
  for (bb = 1; bb <= eta_num[5]; bb++)
  {
    outangout << " ";
    outangout << eta5[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM5 HPM");
  outangout << outxx;
  for (bb = 1; bb <= hpm_num[5]; bb++)
  {
    outangout << " ";
    outangout << hpm5[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM5 phi");
  outangout << outxx;
  for (bb = 1; bb <= phi_num[5]; bb++)
  {
    outangout << " ";
    outangout << phi5[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM5 theta");
  outangout << outxx;
  for (bb = 1; bb <= thet_num[5]; bb++)
  {
    outangout << " ";
    outangout << thet5[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM6 eta");
  outangout << outxx;
  for (bb = 1; bb <= eta_num[6]; bb++)
  {
    outangout << " ";
    outangout << eta6[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM6 HPM");
  outangout << outxx;
  for (bb = 1; bb <= hpm_num[6]; bb++)
  {
    outangout << " ";
    outangout << hpm6[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM6 phi");
  outangout << outxx;
  for (bb = 1; bb <= phi_num[6]; bb++)
  {
    outangout << " ";
    outangout << phi6[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM6 theta");
  outangout << outxx;
  for (bb = 1; bb <= thet_num[6]; bb++)
  {
    outangout << " ";
    outangout << thet6[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM7 eta");
  outangout << outxx;
  for (bb = 1; bb <= eta_num[7]; bb++)
  {
    outangout << " ";
    outangout << eta7[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM7 HPM");
  outangout << outxx;
  for (bb = 1; bb <= hpm_num[7]; bb++)
  {
    outangout << " ";
    outangout << hpm7[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM7 phi");
  outangout << outxx;
  for (bb = 1; bb <= phi_num[7]; bb++)
  {
    outangout << " ";
    outangout << phi7[bb];
  }
  outangout << endl;

  sprintf(outxx,"TM7 theta");
  outangout << outxx;
  for (bb = 1; bb <= thet_num[7]; bb++)
  {
    outangout << " ";
    outangout << thet7[bb];
  }
  outangout << endl;

}
