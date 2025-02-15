#include <fstream.h>
#include <iostream.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

/* program to compute the hydrophobic center by equal area method */
/* Compile using: g++ hpc_by_centroid.C -o hpc_by_centroid.x */
/* USAGE: hpc_by_centroid.x  hydrophobicity_data_file baseline tm_beg tm_end */
/*  e.g.: hpc_by_centroid.x  data12_nobasechange.txt 0.0420101 158 188 */

int main(int argc, char *argv[])
{
   char hps_data_file[100],string2[40],string3[20],string4[20];
   int start_index,end_index,beg_zero,ter_zero,start_main_index;
   int i,j,jc,imax,init,limit_l,limit_r,tmax,nmax,imax_seqid;
   double baseline,data1,data2,thres,sum,fmax,center,rcenter,half;
   double *hps_data,*hps_data_tm,*cumsum,rcenter_seqid;
   ifstream in_stream,in_stream2;
   
   strcpy(hps_data_file,argv[1]);
   strcpy(string2,argv[2]);
   strcpy(string3,argv[3]);
   strcpy(string4,argv[4]);

   baseline=atof(string2);
   start_index=atoi(string3);
   end_index=atoi(string4); 

   nmax=0;
   in_stream.open(hps_data_file);
   in_stream >> data1;
   for (i=0; !in_stream.eof(); i++) {
      nmax++;
      in_stream >> data1;
   }
   in_stream.close();
/* */
   in_stream2.open(hps_data_file);
   fmax=0.0;
   hps_data = new double [nmax];
   for (i=1; i<=nmax; i++) {
       in_stream2 >> data2;
       hps_data[i-1]=data2;
/*     printf("%d %f\n",i,hps_data[i-1]); */
       if (i >= start_index && i <= end_index) {
          if (fmax < data2) {
               fmax=data2;
               imax=i-start_index+1;
          }
       }
   }
   in_stream2.close();
/*   printf("%d %f\n",imax,fmax); */
/* */
      start_main_index=start_index+imax-1;
/* */
      init=start_main_index;
      thres=baseline;
      limit_l=start_index;
      limit_r=end_index;
/* */
      i=init;
      while (i >= limit_l && hps_data[i-1] >= thres) i--;
      beg_zero=i+1;
/* */
      i=init;
      while (i <= limit_r && hps_data[i-1] >= thres) i++;
      ter_zero=i-1;
/* */
      tmax=ter_zero-beg_zero+1;
      jc=0;
      hps_data_tm = new double [tmax];
      for (j=beg_zero; j<=ter_zero; j++) {
         hps_data_tm[jc]=hps_data[j-1];
         jc=jc+1;
      }
/* */
      sum=0.0;
      cumsum = new double [tmax];
      for (i=0; i<tmax; i++) {
         sum=sum+hps_data_tm[i]-baseline;
         cumsum[i]=sum;
      }
/* */
      half=sum*0.5;
/* */
      i=1;
      while (cumsum[i-1] < half) {
         i=i+1;
      }
/* */
      center=i-(cumsum[i-1]-half)/(cumsum[i-1]-cumsum[i-2])+0.5;
      rcenter=center+beg_zero-start_index;
      imax_seqid=imax+start_index-1;
      rcenter_seqid=rcenter+start_index-1;
/* */
      printf("Peak: %3d %4d  Area: %6.2f %7.2f\n",imax,imax_seqid,rcenter,rcenter_seqid);
/* */
      return 0;
}
