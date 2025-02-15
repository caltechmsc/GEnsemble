#include <iostream>
#include <string>
#include <stdio.h>
#include <fstream>
#include <sstream>
#include <map>
using namespace std;
main (int argc, char* argv[])
{
  char totf[50];
  string linetots;
  int phi1,thet1,eta1,phi2,thet2,eta2,phi3,thet3,eta3,phi4,thet4,eta4,phi5,thet5,eta5,phi6,thet6,eta6,phi7,thet7,eta7;
  double hpm1,hpm2,hpm3,hpm4,hpm5,hpm6,hpm7;
  string h1,h2,h3,h4,h5,h6,h7;
  long double tot,inter,nointv,hbond;
  char struc[500];
  int num = atoi(argv[1]);
  int lst = atoi(argv[2]);
  int numth = lst*num;
  static long double tot_t[300000];
  map<long double,string> struc_t;
  map<string,long double> inter_t;
  map<string,long double> nointv_t;
  map<string,long double> hbond_t;
  int total,totalx;
  int j = 0;
  for (int i=1; i <= num; i++)
  {
    sprintf(totf,"Total_Energy_%i",i);
    ifstream tots(totf);
    while (!tots.eof())
    {
      getline(tots,linetots);
      istringstream linetot(linetots);
      linetot >> h1 >> phi1 >> thet1 >> hpm1 >> eta1 >> h2 >> phi2 >> thet2 >> hpm2 >> eta2 >> h3 >> phi3 >> thet3 >> hpm3 >> eta3 >> h4 >> phi4 >> thet4 >> hpm4 >> eta4 >> h5 >> phi5 >> thet5 >> hpm5 >> eta5 >> h6 >> phi6 >> thet6 >> hpm6 >> eta6 >> h7 >> phi7 >> thet7 >> hpm7 >> eta7 >> tot >> inter >> nointv >> hbond;
      if (tots.eof()) break;
//      sprintf(struc,"H1 %*i %*i %*.1f %*i H2 %*i %*i %*.1f %*i H3 %*i %*i %*.1f %*i H4 %*i %*i %*.1f %*i H5 %*i %*i %*.1f %*i H6 %*i %*i %*.1f %*i H7 %*i %*i %*.1f %*i",4,phi1,4,thet1,5,hpm1,4,eta1,4,phi2,4,thet2,5,hpm2,4,eta2,4,phi3,4,thet3,5,hpm3,4,eta3,4,phi4,4,thet4,5,hpm4,4,eta4,4,phi5,4,thet5,5,hpm5,4,eta5,4,phi6,4,thet6,5,hpm6,4,eta6,4,phi7,4,thet7,5,hpm7,4,eta7);
      sprintf(struc,"Thet %*i %*i %*i %*i %*i %*i %*i Phi %*i %*i %*i %*i %*i %*i %*i Eta %*i %*i %*i %*i %*i %*i %*i HPM %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f",4,thet1,4,thet2,4,thet3,4,thet4,4,thet5,4,thet6,4,thet7,4,phi1,4,phi2,4,phi3,4,phi4,4,phi5,4,phi6,4,phi7,4,eta1,4,eta2,4,eta3,4,eta4,4,eta5,4,eta6,4,eta7,5,hpm1,5,hpm2,5,hpm3,5,hpm4,5,hpm5,5,hpm6,5,hpm7);
      if (j != 0)
      {
        if (tot == tot_t[j-1])
        {
          tot = tot + 0.000001;
        } 
        for (int p=1; p < j; p++)
        {
          if (tot == tot_t[p])
          {
            tot = tot + 0.000001;
          } 
        } 
      }
      tot_t[j] = tot;
      struc_t[tot_t[j]] = struc;
      inter_t[struc] = inter;
      nointv_t[struc] = nointv;
      hbond_t[struc] = hbond;
      j++;
    }
    stable_sort(tot_t,tot_t+j);
  }
  total = j;
  stable_sort(tot_t,tot_t+total);

  char interf[50];
  string lineinters;
  static long double inter_i[300000];
  map<long double,string> struc_i;
  map<string,long double> tot_i;
  map<string,long double> nointv_i;
  map<string,long double> hbond_i;
  j = 0;
  for (int i=1; i <= num; i++)
  {
    sprintf(interf,"Interhelical_Energy_%i",i);
    ifstream inters(interf);
    while (!inters.eof())
    {
      getline(inters,lineinters);
      istringstream lineinter(lineinters);
      lineinter >> h1 >> phi1 >> thet1 >> hpm1 >> eta1 >> h2 >> phi2 >> thet2 >> hpm2 >> eta2 >> h3 >> phi3 >> thet3 >> hpm3 >> eta3 >> h4 >> phi4 >> thet4 >> hpm4 >> eta4 >> h5 >> phi5 >> thet5 >> hpm5 >> eta5 >> h6 >> phi6 >> thet6 >> hpm6 >> eta6 >> h7 >> phi7 >> thet7 >> hpm7 >> eta7 >> tot >> inter >> nointv >> hbond;
      if (inters.eof()) break;
//      sprintf(struc,"H1 %*i %*i %*.1f %*i H2 %*i %*i %*.1f %*i H3 %*i %*i %*.1f %*i H4 %*i %*i %*.1f %*i H5 %*i %*i %*.1f %*i H6 %*i %*i %*.1f %*i H7 %*i %*i %*.1f %*i",4,phi1,4,thet1,5,hpm1,4,eta1,4,phi2,4,thet2,5,hpm2,4,eta2,4,phi3,4,thet3,5,hpm3,4,eta3,4,phi4,4,thet4,5,hpm4,4,eta4,4,phi5,4,thet5,5,hpm5,4,eta5,4,phi6,4,thet6,5,hpm6,4,eta6,4,phi7,4,thet7,5,hpm7,4,eta7);
      sprintf(struc,"Thet %*i %*i %*i %*i %*i %*i %*i Phi %*i %*i %*i %*i %*i %*i %*i Eta %*i %*i %*i %*i %*i %*i %*i HPM %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f",4,thet1,4,thet2,4,thet3,4,thet4,4,thet5,4,thet6,4,thet7,4,phi1,4,phi2,4,phi3,4,phi4,4,phi5,4,phi6,4,phi7,4,eta1,4,eta2,4,eta3,4,eta4,4,eta5,4,eta6,4,eta7,5,hpm1,5,hpm2,5,hpm3,5,hpm4,5,hpm5,5,hpm6,5,hpm7);
      if (j != 0)
      {
        if (inter == inter_i[j-1])
        {
          inter = inter + 0.000001;
        }
        for (int p=1; p < j; p++)
        {
          if (inter == inter_i[p])
          {
            inter = inter + 0.000001;
          }
        }
      }
      inter_i[j] = inter;
      struc_i[inter_i[j]] = struc;
      tot_i[struc] = tot;
      nointv_i[struc] = nointv;
      hbond_i[struc] = hbond;
      j++;
    }
    stable_sort(inter_i,inter_i+j);
  }
  stable_sort(inter_i,inter_i+total);

  char nointvf[50];
  string linenointvs;
  static long double nointv_v[300000];
  map<long double,string> struc_v;
  map<string,long double> tot_v;
  map<string,long double> inter_v;
  map<string,long double> hbond_v;
  j = 0;
  for (int i=1; i <= num; i++)
  {
    sprintf(nointvf,"No_Interhelical_VDW_%i",i);
    ifstream nointvs(nointvf);
    while (!nointvs.eof())
    {
      getline(nointvs,linenointvs);
      istringstream linenointv(linenointvs);
      linenointv >> h1 >> phi1 >> thet1 >> hpm1 >> eta1 >> h2 >> phi2 >> thet2 >> hpm2 >> eta2 >> h3 >> phi3 >> thet3 >> hpm3 >> eta3 >> h4 >> phi4 >> thet4 >> hpm4 >> eta4 >> h5 >> phi5 >> thet5 >> hpm5 >> eta5 >> h6 >> phi6 >> thet6 >> hpm6 >> eta6 >> h7 >> phi7 >> thet7 >> hpm7 >> eta7 >> tot >> inter >> nointv >> hbond;
      if (nointvs.eof()) break;
//      sprintf(struc,"H1 %*i %*i %*.1f %*i H2 %*i %*i %*.1f %*i H3 %*i %*i %*.1f %*i H4 %*i %*i %*.1f %*i H5 %*i %*i %*.1f %*i H6 %*i %*i %*.1f %*i H7 %*i %*i %*.1f %*i",4,phi1,4,thet1,5,hpm1,4,eta1,4,phi2,4,thet2,5,hpm2,4,eta2,4,phi3,4,thet3,5,hpm3,4,eta3,4,phi4,4,thet4,5,hpm4,4,eta4,4,phi5,4,thet5,5,hpm5,4,eta5,4,phi6,4,thet6,5,hpm6,4,eta6,4,phi7,4,thet7,5,hpm7,4,eta7);
      sprintf(struc,"Thet %*i %*i %*i %*i %*i %*i %*i Phi %*i %*i %*i %*i %*i %*i %*i Eta %*i %*i %*i %*i %*i %*i %*i HPM %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f",4,thet1,4,thet2,4,thet3,4,thet4,4,thet5,4,thet6,4,thet7,4,phi1,4,phi2,4,phi3,4,phi4,4,phi5,4,phi6,4,phi7,4,eta1,4,eta2,4,eta3,4,eta4,4,eta5,4,eta6,4,eta7,5,hpm1,5,hpm2,5,hpm3,5,hpm4,5,hpm5,5,hpm6,5,hpm7);
      if (j != 0)
      {
        if (nointv == nointv_v[j-1])
        {
          nointv = nointv + 0.000001;
        }
        for (int p=1; p < j; p++)
        {
          if (nointv == nointv_v[p])
          {
            nointv = nointv + 0.000001;
          }
        }
      }
      nointv_v[j] = nointv;
      struc_v[nointv_v[j]] = struc;
      tot_v[struc] = tot;
      inter_v[struc] = inter;
      hbond_v[struc] = hbond;
      j++;
    }
    stable_sort(nointv_v,nointv_v+j);
  }
  stable_sort(nointv_v,nointv_v+total);

  char hbondf[50];
  string linehbonds;
  static long double hbond_h[300000];
  map<long double,string> struc_h;
  map<string,long double> tot_h;
  map<string,long double> inter_h;
  map<string,long double> nointv_h;
  j = 0;
  for (int i=1; i <= num; i++)
  {
    sprintf(hbondf,"Interhelical_Hbond_%i",i);
    ifstream hbonds(hbondf);
    while (!hbonds.eof())
    {
      getline(hbonds,linehbonds);
      istringstream linehbond(linehbonds);
      linehbond >> h1 >> phi1 >> thet1 >> hpm1 >> eta1 >> h2 >> phi2 >> thet2 >> hpm2 >> eta2 >> h3 >> phi3 >> thet3 >> hpm3 >> eta3 >> h4 >> phi4 >> thet4 >> hpm4 >> eta4 >> h5 >> phi5 >> thet5 >> hpm5 >> eta5 >> h6 >> phi6 >> thet6 >> hpm6 >> eta6 >> h7 >> phi7 >> thet7 >> hpm7 >> eta7 >> tot >> inter >> nointv >> hbond;
      if (hbonds.eof()) break;
//      sprintf(struc,"H1 %*i %*i %*.1f %*i H2 %*i %*i %*.1f %*i H3 %*i %*i %*.1f %*i H4 %*i %*i %*.1f %*i H5 %*i %*i %*.1f %*i H6 %*i %*i %*.1f %*i H7 %*i %*i %*.1f %*i",4,phi1,4,thet1,5,hpm1,4,eta1,4,phi2,4,thet2,5,hpm2,4,eta2,4,phi3,4,thet3,5,hpm3,4,eta3,4,phi4,4,thet4,5,hpm4,4,eta4,4,phi5,4,thet5,5,hpm5,4,eta5,4,phi6,4,thet6,5,hpm6,4,eta6,4,phi7,4,thet7,5,hpm7,4,eta7);
      sprintf(struc,"Thet %*i %*i %*i %*i %*i %*i %*i Phi %*i %*i %*i %*i %*i %*i %*i Eta %*i %*i %*i %*i %*i %*i %*i HPM %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f %*.1f",4,thet1,4,thet2,4,thet3,4,thet4,4,thet5,4,thet6,4,thet7,4,phi1,4,phi2,4,phi3,4,phi4,4,phi5,4,phi6,4,phi7,4,eta1,4,eta2,4,eta3,4,eta4,4,eta5,4,eta6,4,eta7,5,hpm1,5,hpm2,5,hpm3,5,hpm4,5,hpm5,5,hpm6,5,hpm7);  
      if (j != 0)
      {
        if (hbond == hbond_h[j-1])
        {
          hbond = hbond + 0.000001;
        }
        for (int p=1; p < j; p++)
        {
          if (hbond == hbond_h[p])
          {
            hbond = hbond + 0.000001;
          }
        }
  
      }
      hbond_h[j] = hbond;
      struc_h[hbond_h[j]] = struc;
      tot_h[struc] = tot;
      inter_h[struc] = inter;
      nointv_h[struc] = nointv;
      j++;
    }
    stable_sort(hbond_h,hbond_h+j);
  }
  stable_sort(hbond_h,hbond_h+total);

  ofstream out_t("Super_Bihelix_TotalE.out");
  ofstream out_i("Super_Bihelix_InterHelE.out");
  ofstream out_v("Super_Bihelix_NoInterVDW.out");
  ofstream out_h("Super_Bihelix_HBondE.out");
  char out_tx[500],out_ix[500],out_vx[500],out_hx[500],top[500],top_t1[500],top_i1[500],top_v1[500],top_h1[500];
  sprintf(top_t1,"                                                                                                                                                                         Ordered by\n");
  sprintf(top_i1,"                                                                                                                                                                                      Ordered by\n");
  sprintf(top_v1,"                                                                                                                                                                                                 Ordered by\n");
  sprintf(top_h1,"                                                                                                                                                                                                             Ordered by\n");
  sprintf(top,"Thet   H1   H2   H3   H4   H5   H6   H7 Phi   H1   H2   H3   H4   H5   H6   H7 Eta   H1   H2   H3   H4   H5   H6   H7 HPM    H1    H2    H3    H4    H5    H6    H7        TotalE     InterHelE  NoInterVDW     HBond\n");  
  out_t << top_t1 << top;
  out_i << top_i1 << top;
  out_v << top_v1 << top;
  out_h << top_h1 << top;
  totalx = lst;
  if (total < lst)
  {
    totalx = total;
  } 
  for (int k = 0; k < totalx; k++)
  {
    sprintf(out_tx,"%s  %*.1Lf  %*.1Lf  %*.1Lf  %*.1Lf\n",struc_t[tot_t[k]],12,tot_t[k],12,inter_t[struc_t[tot_t[k]]],10,nointv_t[struc_t[tot_t[k]]],8,hbond_t[struc_t[tot_t[k]]]);
    sprintf(out_ix,"%s  %*.1Lf  %*.1Lf  %*.1Lf  %*.1Lf\n",struc_i[inter_i[k]],12,tot_i[struc_i[inter_i[k]]],12,inter_i[k],10,nointv_i[struc_i[inter_i[k]]],8,hbond_i[struc_i[inter_i[k]]]);
    sprintf(out_vx,"%s  %*.1Lf  %*.1Lf  %*.1Lf  %*.1Lf\n",struc_v[nointv_v[k]],12,tot_v[struc_v[nointv_v[k]]],12,inter_v[struc_v[nointv_v[k]]],10,nointv_v[k],8,hbond_v[struc_v[nointv_v[k]]]);
    sprintf(out_hx,"%s  %*.1Lf  %*.1Lf  %*.1Lf  %*.1Lf\n",struc_h[hbond_h[k]],12,tot_h[struc_h[hbond_h[k]]],12,inter_h[struc_h[hbond_h[k]]],10,nointv_h[struc_h[hbond_h[k]]],8,hbond_h[k]);
    out_t << out_tx;
    out_i << out_ix;
    out_v << out_vx;
    out_h << out_hx;
  }

} 
