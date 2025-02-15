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
  string linet[10];
  string lines,linesa,tmx,ang,linees;
  string st,tm,resa,resna;
  char tmhel1[3],tmhel2[3],outeng[100];
  char al1[20], al2[20];
  string res[10],resn[10];
  double eta1[30],phi1[20],thet1[20],hpm1[20];
  double eta2[30],phi2[20],thet2[20],hpm2[20];
  double phi_new1, thet_new1, eta_new1, hpm_new1;
  double phi_new2, thet_new2, eta_new2, hpm_new2; 
  double intr11, inter11, intrv11, intrc11, intrh11, intr22, inter22, intrv22, intrc22, intrh22, inter12, interv12, interc12, interh12, tote;
  double novdw; 
  int eta_num[3] = {0},phi_num[3] = {0},thet_num[3] = {0},hpm_num[3] = {0};
  double xxa,yya,hpma,theta,phia,etaa,yay;
  double xx[10],yy[10],hpm[10],thet[10],phi[10],eta[10];
  hel1 = atoi(argv[3]);
  hel2 = atoi(argv[4]);
  sprintf(tmhel1,"TM%s",argv[3]);
  sprintf(tmhel2,"TM%s",argv[4]);
  sprintf(outeng,"super_bihelix_TM%s_TM%s.out",argv[3],argv[4]);
  ofstream energyout(outeng);
  sprintf(first,"phi%s thet%s hpm%s eta%s phi%s thet%s hpm%s eta%s   Tot_%s%s_Intra Tot_%s%s_Intra Tot_%s%s_Inter TotalE_H%s-H%s VDW_%s%s_Intra VDW_%s%s_Intra VDW_%s%s_Inter NoVDWE_H%s-H%s HB_%s%s_Inter",argv[3],argv[3],argv[3],argv[3],argv[4],argv[4],argv[4],argv[4],argv[3],argv[3],argv[4],argv[4],argv[3],argv[4],argv[3],argv[4],argv[3],argv[3],argv[4],argv[4],argv[3],argv[4],argv[3],argv[4],argv[3],argv[4]);
  energyout << first << endl;
  sprintf(s,"cp %s super.bgf",argv[1]);
  system(s);
  sprintf(t, "cp %s super.mfta",argv[2]);
  system(t); 
  system("/project/Biogroup/scripts/perl/bgf2pdb.pl super.bgf > super.pdb ");
  system("/project/Biogroup/Software/devel/GEnsemble2/programs/templates/OPM/GetTemplate.pl -m super.mfta -p super.pdb > super.template");
  system("/project/Biogroup/scripts/playWithBGF/playWithBGF super.bgf -c 1 -o super1.bgf > play_with_bgf.out");
  system("/project/Biogroup/scripts/playWithBGF/playWithBGF super.bgf -c 2 -o super2.bgf > play_with_bgf.out");
  system("/project/Biogroup/scripts/playWithBGF/playWithBGF super.bgf -c 3 -o super3.bgf > play_with_bgf.out");
  system("/project/Biogroup/scripts/playWithBGF/playWithBGF super.bgf -c 4 -o super4.bgf > play_with_bgf.out");
  system("/project/Biogroup/scripts/playWithBGF/playWithBGF super.bgf -c 5 -o super5.bgf > play_with_bgf.out");
  system("/project/Biogroup/scripts/playWithBGF/playWithBGF super.bgf -c 6 -o super6.bgf > play_with_bgf.out");
  system("/project/Biogroup/scripts/playWithBGF/playWithBGF super.bgf -c 7 -o super7.bgf > play_with_bgf.out");
  string file = "super.template";
  ifstream infile (file.c_str());
  int i = 0;
  while (!infile.eof())
  {
    i++;
    getline(infile,lines);
    istringstream line(lines);
    linet[i] = lines;
    line >> st >> tm >> xxa >> yya >> hpma >> theta >> phia >> etaa >> resa >> resna; 
//    printf ("tm is %s \n",tm);
    xx[i] = xxa;
    yy[i] = yya;
    hpm[i] = hpma;
    thet[i] = theta;
    phi[i] = phia;
    eta[i] = etaa;
    res[i] = resa;
    resn[i] = resna;
  }
 
  i = 0; 
  string filea = "angles.txt";
  ifstream infilea (filea.c_str());
  while (!infilea.eof())
  {
    i++; 
    int j = 0;
    getline(infilea,linesa);
    printf ("%s \n",linesa.c_str());
    istringstream linea(linesa);
    linea >> tmx;
    if (tmx == tmhel1)
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
        printf ("eta of %i is %.3f \n",j,eta1[j]);
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi1[j] = yay;
        phi_num[1] = j;
        printf ("phi of %i is %.3f \n",j,phi1[j]);
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet1[j] = yay;
        thet_num[1] = j;
        printf ("theta of %i is %.3f \n",j,thet1[j]);
        }
        if (ang == "HPM")
        {
        linea >> yay;
        hpm1[j] = yay;
        hpm_num[1] = j;
        printf ("hpm of %i is %.3f \n",j,hpm1[j]);
        }
      }
    printf ("there are %i etas, %i phis, %i thetas, %i hpms for tm1\n",eta_num[1],phi_num[1],thet_num[1],hpm_num[1]);
    }

    if (tmx == tmhel2)
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
        printf ("eta of %i is %.3f \n",j,eta2[j]);
        }
        if (ang == "phi")
        {
        linea >> yay;
        phi2[j] = yay;
        phi_num[2] = j;
        printf ("phi of %i is %.3f \n",j,phi2[j]);
        }
        if (ang == "theta")
        {
        linea >> yay;
        thet2[j] = yay;
        thet_num[2] = j;
        printf ("theta of %i is %.3f \n",j,thet2[j]);
        }
        if (ang == "HPM")
        {
        linea >> yay;
        hpm2[j] = yay;
        hpm_num[2] = j;
        printf ("hpm of %i is %.3f \n",j,hpm2[j]);
        }
      }
    printf ("there are %i etas, %i phis, %i thetas, %i hpms for tm2\n",eta_num[2],phi_num[2],thet_num[2],hpm_num[2]);
    }
  }

  sprintf(al1,"aligned_helix%s.bgf",argv[3]);
  sprintf(al2,"aligned_helix%s.bgf",argv[4]);
  int a1,b1,c1,d1,a2,b2,c2,d2; 
  for (a1 = 1; a1 <= phi_num[1]; a1++)
  {
/*  for (b1 = 1; b1 <= thet_num[1]; b1++)
    { */
      for (c1 = 1; c1 <= hpm_num[1]; c1++)
      {
        for (d1 = 1; d1 <= eta_num[1]; d1++)
        {     
          for (a2 = 1; a2 <= phi_num[2]; a2++)
          {
/*          for (b2 = 1; b2 <= thet_num[2]; b2++)
            { */
              for (c2 = 1; c2 <= hpm_num[2]; c2++)
              {
                for (d2 = 1; d2 <= eta_num[2]; d2++)
                {
                  ofstream tempout("template.temp");
                  for (i = 1; i <= 8; i++)
                  { 
                    if (i != hel1 && i != hel2)
                    {
                    tempout << linet[i] << endl;
                    } 
                    if (i == hel1)
                    {
                      phi_new1 = phi[i] + phi1[a1];
                      thet_new1 = thet[i] + thet1[a1];
                      hpm_new1 = hpm1[c1];
                      eta_new1 = eta[i] + eta1[d1];
                      sprintf (pr,"*  %itmpl    %.2f    %.2f   %.2f    %.2f   %.2f   %.2f    %s  %s",i,xx[i],yy[i],hpm_new1,thet_new1,phi_new1,eta_new1,res[i].c_str(),resn[i].c_str());      
                      tempout << pr << endl;
                    } 
                    if (i == hel2)
                    {
                      phi_new2 = phi[i] + phi2[a2]; 
                      thet_new2 = thet[i] + thet2[a2];
                      hpm_new2 = hpm2[c2];
                      eta_new2 = eta[i] + eta2[d2];
                      sprintf (pl,"*  %itmpl    %.2f    %.2f   %.2f    %.2f   %.2f   %.2f    %s  %s",i,xx[i],yy[i],hpm_new2,thet_new2,phi_new2,eta_new2,res[i].c_str(),resn[i].c_str());
                      tempout << pl << endl;
                    }
                  }
                system("/project/Biogroup/Software/GEnsemble/programs/superbihelix/Align2Template.pl -t template.temp -m super.mfta");  
                sprintf(mg,"/project/Biogroup/Software/GEnsemble/programs/thirdparty/python-2.4.2/bin/python /project/Biogroup/Software/GEnsemble/programs/utilities/mergeBGFs.py %s %s -s -o bihel.bgf",al1,al2);
                system(mg);
                system("/ul/jenelle/codes/other/split-chains.pl bihel.bgf bihels.bgf"); 
                system("/exec/python/python-2.4.2/bin/python /project/Biogroup/Software/GEnsemble/programs/superbihelix/Generate_Par_File_for_Bihelical.py bihels.bgf 05 FULL 0.0");
                system("/exec/python/python-2.4.2/bin/python /project/Biogroup/Software/GEnsemble/programs/scream2/scripts/SCREAM_with_BiHelix_E_output.py scream.par > scream.out"); 
                fstream fb("best_1.bgf", ios_base::in);
                int y = 0;
                if (!fb)
                {
		  system("/exec/python/python-2.4.2/bin/python /project/Biogroup/Software/GEnsemble/programs/scream2/scripts/SCREAM_with_BiHelix_E_output.py scream.par > scream.out");
		  fstream fb("best_1.bgf", ios_base::in);
                if (!fb)
                {                  
		  y++;
                  intr11 = 5000;
                  intr22 = 5000;
                  inter12 = 5000;
                  tote = 5000;
                  intrv11 = 5000;
                  intrv22 = 5000;
                  interv12 = 5000;
                  novdw = 5000;
                  interh12 = 0;
                }
		}
                system("/project/Biogroup/scripts/playWithBGF/playWithBGF best_1.bgf -s -V on -Lo side_temp.bgf  > play_with_bgf.out");
                system("/ul/caglar/Perl/runMPSim.pl side_temp.bgf -s 10 minvac -f /project/Biogroup/FF/dreiding-0.3.par > runmpsim.out");
                system("/project/Biogroup/scripts/playWithBGF/playWithBGF side_temp_minvac.fin.bgf -V on -Lo all_temp.bgf  > play_with_bgf.out");
                system("/project/Biogroup/Software/devel/GEnsemble/programs/bihelixrot2/BiHelix_MPSim.pl -b all_temp.bgf -f /project/Biogroup/FF/dreiding-0.3.par -mpsim /ul/caglar/Perl/runMPSim.pl -pwb /project/Biogroup/scripts/playWithBGF/playWithBGF > mpsim.out");
//                string crash = "CRASH.bgf";
                fstream fs("CRASH.bgf", ios_base::in);
                if (!fs)
                {
                }
                else 
		{
                  fs.close(); 
		  system("rm -f CRASH.bgf");
                  system("/ul/caglar/Perl/runMPSim.pl side_temp.bgf -s 10 minvac -f /project/Biogroup/FF/dreiding-0.3.par > runmpsim.out");
                  system("/project/Biogroup/scripts/playWithBGF/playWithBGF side_temp_minvac.fin.bgf -V on -Lo all_temp.bgf  > play_with_bgf.out");
                  system("/project/Biogroup/Software/devel/GEnsemble/programs/bihelixrot2/BiHelix_MPSim.pl -b all_temp.bgf -f /project/Biogroup/FF/dreiding-0.3.par -mpsim /ul/caglar/Perl/runMPSim.pl -pwb /project/Biogroup/scripts/playWithBGF/playWithBGF > mpsim.out");
                  fstream fs("CRASH.bgf", ios_base::in);
                  if (!fs)
                  {
                  }
                  else
                    {
                      fs.close();
                      y++;
		      ("rm -f CRASH.bgf"); 
                      intr11 = 5000;
                      intr22 = 5000;
                      inter12 = 5000;
                      tote = 5000;
                      intrv11 = 5000;
                      intrv22 = 5000;
                      interv12 = 5000;
                      novdw = 5000;
                      interh12 = 0; 
		    }
                  }
                ifstream energ("mpsim.out");
                int x = 0;
                while (!energ.eof())
                  {
                    x++; 
                    getline(energ,linees);
                    istringstream linee(linees);
                    if (x == 1)
                    {
                    if (y == 0) 
                    {
                    linee >> intr11 >> intr22 >> inter12 >> tote >> intrv11 >> intrv22 >> interv12 >> novdw >> interh12; 
                      if (tote == 0 && inter12 == -intr11)
                      {
		      intr11 = 5000;
                      intr22 = 5000;
                      inter12 = 5000;
                      tote = 5000;
                      intrv11 = 5000;
                      intrv22 = 5000;
                      interv12 = 5000;
                      novdw = 5000;
                      interh12 = 0;
                      }
                      if (tote == 0 && inter12 == -intr22)
                      {
                      intr11 = 5000;
                      intr22 = 5000;
                      inter12 = 5000;
                      tote = 5000;                     
                      intrv11 = 5000;
                      intrv22 = 5000; 
                      interv12 = 5000;
                      novdw = 5000;
                      interh12 = 0;
                      }
                    }
                    sprintf(oute,"  %.0f    %.0f   %.1f    %.0f   %.0f  %.0f    %.1f    %0.f          %.1f         %.1f        %.1f         %.1f        %.1f        %.1f        %.1f        %.1f        %.1f",phi1[a1],thet1[a1],hpm1[c1],eta1[d1],phi2[a2],thet2[a2],hpm2[c2],eta2[d2],intr11,intr22,inter12,tote,intrv11,intrv22,interv12,novdw,interh12);
                    energyout << oute << endl;
                    system("rm -f all_temp.bgf play_with_bgf.out aligned_helix* Anneal-Energies.txt Bihelical-E.txt Residue-E.txt runmpsim.out best_1.bgf bihel.bgf bihels.bgf mpsim.out scream.out scream.par side_temp*");  
                    }
                  }
                }
              }
/*          } */
          }  
        }
      }
/*  } */
  } 

char done[100], outdone[100];
sprintf(done,"super_bihelix_done.out");
ofstream doneout(done);
sprintf(outdone,"job is done");
doneout << outdone << endl;
}
