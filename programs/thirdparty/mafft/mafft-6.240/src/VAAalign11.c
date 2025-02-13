#include "mltaln.h"
#include "dp.h"

#define DEBUG 0
#define DEBUG2 0
#define XXXXXXX    0
#define USE_PENALTY_EX  1

static short localstop;

static void	searchsubopts( int lgth1, int lgth2, float **WMMTX, float threshold, LocalHom *lhmpt )
{
	int posini, posinj, lag, end1, end2, start1, start2;
	int nlocalhom;
	int status;
	float kokonoscore;
	float score;
	int totaloverlap;
	LocalHom *tmppt = lhmpt;

	nlocalhom = 0;
	totaloverlap = 0;
	for( lag=-lgth1+1; lag<lgth2; lag++ )
	{
//		fprintf( stderr, "lag = %d\n", lag );
		status = 0;
		score = 0.0;
		for( posini=MAX(0,-lag),posinj=MAX(0,lag); posini<lgth1&&posinj<lgth2; posini++,posinj++ )
		{
			kokonoscore = WMMTX[posini][posinj];
//			if( kokonoscore > threshold ) fprintf( stderr, "ok " );
			if( status == 1 && kokonoscore != score )
			{
//				fprintf( stderr, "start1=%d, end1=%d\n", start1, posini-1 );
				if( nlocalhom++ > 0 )
				{
//					fprintf( stderr, "reallocating ...\n" );
					tmppt->next = (LocalHom *)calloc( 1, sizeof( LocalHom ) );
//					fprintf( stderr, "done\n" );
					tmppt = tmppt->next;
					tmppt->next = NULL;
				}
				tmppt->start1 = start1;
				tmppt->start2 = start2;
				tmppt->end1 = posini - 1;
				tmppt->end2 = posinj - 1;

				tmppt->overlapaa = posinj - start2;
				totaloverlap += tmppt->overlapaa;
//				tmppt->opt = score / tmppt->overlapaa * 5.8 / 600; // warubekika?
				tmppt->opt = score; // warubekika?

				status = 0;
			}
			if( kokonoscore >= threshold )
			{
				if( status == 0 )
				{
					start1 = posini; start2 = posinj;
					status = 1;
					score = kokonoscore;
				}
			}
			else
			{
				status = 0;
				score = 0.0;
			}
		}

		if( kokonoscore >= threshold )
		{
			if( nlocalhom++ > 0 )
			{
//				fprintf( stderr, "reallocating ...\n" );
				tmppt->next = (LocalHom *)calloc( 1, sizeof( LocalHom ) );
//				fprintf( stderr, "done\n" );
				tmppt = tmppt->next;
				tmppt->next = NULL;
			}
			tmppt->start1 = start1;
			tmppt->start2 = start2;
			tmppt->end1 = posini-1;
			tmppt->end2 = posinj-1;

			tmppt->overlapaa = posini - start1;
			totaloverlap += tmppt->overlapaa;
//			tmppt->opt = score / tmppt->overlapaa * 5.8 / 600; // warubekika?
			tmppt->opt = score; // warubekika?
		}
	}

	for( tmppt=lhmpt; tmppt; tmppt=tmppt->next )
	{
		tmppt->overlapaa =  totaloverlap;
		tmppt->opt *=  5.8 / 600 / totaloverlap;
	}
}

static void	searchsubopts_bk( int lgth1, int lgth2, float **WMMTX, float threshold, LocalHom *lhmpt )
{
	int posini, posinj, lag, end1, end2, start1, start2;
	int nlocalhom;
	int status;
	float kokonoscore;
	float score;
	int totaloverlap;
	LocalHom *tmppt = lhmpt;

	nlocalhom = 0;
	totaloverlap = 0;
	for( lag=-lgth1+1; lag<lgth2; lag++ )
	{
		fprintf( stderr, "lag = %d\n", lag );
		status = 0;
		score = 0.0;
		for( posini=MAX(0,-lag),posinj=MAX(0,lag); posini<lgth1&&posinj<lgth2; posini++,posinj++ )
		{
			kokonoscore = WMMTX[posini][posinj];
			if( kokonoscore > threshold ) fprintf( stderr, "ok " );
			if( status == 1 && kokonoscore < threshold )
			{
				fprintf( stderr, "start1=%d, end1=%d\n", start1, posini-1 );
				if( nlocalhom++ > 0 )
				{
					fprintf( stderr, "reallocating ...\n" );
					tmppt->next = (LocalHom *)calloc( 1, sizeof( LocalHom ) );
					fprintf( stderr, "done\n" );
					tmppt = tmppt->next;
					tmppt->next = NULL;
				}
				tmppt->start1 = start1;
				tmppt->start2 = start2;
				tmppt->end1 = posini - 1;
				tmppt->end2 = posinj - 1;

				tmppt->overlapaa = posinj - start2;
				totaloverlap += tmppt->overlapaa;
//				tmppt->opt = score / tmppt->overlapaa * 5.8 / 600; // warubekika?
				tmppt->opt = score; // warubekika?

				score = 0.0;
				status = 0;
			}
			else if( kokonoscore >= threshold )
			{
				if( status == 0 )
				{
					start1 = posini; start2 = posinj;
					status = 1;
				}
				if( score < kokonoscore ) score = kokonoscore; // saidaichi de daihyo
			}
		}

		if( kokonoscore >= threshold )
		{
			if( nlocalhom++ > 0 )
			{
				fprintf( stderr, "reallocating ...\n" );
				tmppt->next = (LocalHom *)calloc( 1, sizeof( LocalHom ) );
				fprintf( stderr, "done\n" );
				tmppt = tmppt->next;
				tmppt->next = NULL;
			}
			tmppt->start1 = start1;
			tmppt->start2 = start2;
			tmppt->end1 = posini-1;
			tmppt->end2 = posinj-1;

			tmppt->overlapaa = posini - start1;
			totaloverlap += tmppt->overlapaa;
//			tmppt->opt = score / tmppt->overlapaa * 5.8 / 600; // warubekika?
			tmppt->opt = score; // warubekika?
		}
	}
	for( tmppt=lhmpt; tmppt; tmppt=tmppt->next )
	{
		tmppt->overlapaa =  totaloverlap;
		tmppt->opt *=  5.8 / 600 / totaloverlap;
	}
}

static void gyakuseq( char *out, char *in )
{
	int len = strlen( in );
	char *pt;

	fprintf( stderr, "len = %d\n", len );

	pt = in + len - 1;
	while( len-- )
		*out++ = *pt--;
	*out = 0;
}

static void match_calc( float *match, char **s1, char **s2, int i1, int lgth2 )
{
	int j;

	for( j=0; j<lgth2; j++ )
		match[j] = amino_dis[(*s1)[i1]][(*s2)[j]];
}
static void match_calc_bk( float *match, float **cpmx1, float **cpmx2, int i1, int lgth2, float **floatwork, int **intwork, int initialize )
{
	int j, k, l;
	float scarr[26];
	float **cpmxpd = floatwork;
	int **cpmxpdn = intwork;
	int count = 0;

	if( initialize )
	{
		for( j=0; j<lgth2; j++ )
		{
			count = 0;
			for( l=0; l<26; l++ )
			{
				if( cpmx2[l][j] )
				{
					cpmxpd[count][j] = cpmx2[l][j];
					cpmxpdn[count][j] = l;
					count++;
				}
			}
			cpmxpdn[count][j] = -1;
		}
	}

	for( l=0; l<26; l++ )
	{
		scarr[l] = 0.0;
		for( k=0; k<26; k++ )
			scarr[l] += n_dis[k][l] * cpmx1[k][i1];
	}
#if 0 /* これを使うときはfloatworkのアロケートを逆にする */
	{
		float *fpt, **fptpt, *fpt2;
		int *ipt, **iptpt;
		fpt2 = match;
		iptpt = cpmxpdn;
		fptpt = cpmxpd;
		while( lgth2-- )
		{
			*fpt2 = 0.0;
			ipt=*iptpt,fpt=*fptpt;
			while( *ipt > -1 )
				*fpt2 += scarr[*ipt++] * *fpt++;
			fpt2++,iptpt++,fptpt++;
		} 
	}
#else
	for( j=0; j<lgth2; j++ )
	{
		match[j] = 0.0;
		for( k=0; cpmxpdn[k][j]>-1; k++ )
			match[j] += scarr[cpmxpdn[k][j]] * cpmxpd[k][j];
	} 
#endif
}

static float gentracking(  
						char **seq1, char **seq2, 
                        char **mseq1, char **mseq2, 
                        float **cpmx1, float **cpmx2, 
                        short **ijpi, short **ijpj, int *off1pt, int *off2pt, int endi, int endj )
{
	int i, j, l, iin, jin, ifi, jfi, lgth1, lgth2, k, limk;
	char gap[] = "-";
	float wm;
	lgth1 = strlen( seq1[0] );
	lgth2 = strlen( seq2[0] );

 
    for( i=0; i<lgth1+1; i++ ) 
    {
        ijpi[i][0] = localstop;
        ijpj[i][0] = localstop;
    }
    for( j=0; j<lgth2+1; j++ ) 
    {
        ijpi[0][j] = localstop;
        ijpj[0][j] = localstop;
    }

	mseq1[0] += lgth1+lgth2;
	*mseq1[0] = 0;
	mseq2[0] += lgth1+lgth2;
	*mseq2[0] = 0;
	iin = endi; jin = endj;
	limk = lgth1+lgth2;
	for( k=0; k<=limk; k++ ) 
	{
		ifi = ( ijpi[iin][jin] );
		jfi = ( ijpj[iin][jin] );
//		fprintf( stderr, "k=%d, i = %d->%d, j = %d->%d\n", k, iin, ifi, jin, jfi );
		l = iin - ifi;
//		if( ijpi[iin][jin] < 0 || ijpj[iin][jin] < 0 )
//		{
//			fprintf( stderr, "skip! %d-%d\n", ijpi[iin][jin], ijpj[iin][jin] );
//			fprintf( stderr, "1: %c-%c\n", seq1[0][iin], seq1[0][ifi] );
//			fprintf( stderr, "2: %c-%c\n", seq2[0][jin], seq2[0][jfi] );
//		}
		while( --l ) 
		{
			*--mseq1[0] = seq1[0][ifi+l];
			*--mseq2[0] = *gap;
			k++;
		}
		l= jin - jfi;
		while( --l )
		{
			*--mseq1[0] = *gap;
			*--mseq2[0] = seq2[0][jfi+l];
			k++;
		}
//		fprintf( stderr, "iin = %d, jin= %d\n", iin, jin );

		if( iin <= 0 || jin <= 0 ) break;
		*--mseq1[0] = seq1[0][ifi];
		*--mseq2[0] = seq2[0][jfi];
		if( ijpi[ifi][jfi] == localstop ) break;
		if( ijpj[ifi][jfi] == localstop ) break; /*いらない*/
		k++;
		iin = ifi; jin = jfi;
	}
	if( ifi == -1 ) *off1pt = 0; else *off1pt = ifi;
	if( jfi == -1 ) *off2pt = 0; else *off2pt = jfi;

//	fprintf( stderr, "ifn = %d, jfn = %d\n", ifi, jfi );


	return( 0.0 );
}

static void do_dp2( short **ijpi, short **ijpj, int *mp, int *Mp, int *endali, int *endalj, int lgth1, int lgth2, char **seq1, char **seq2, float *w1, float *w2, float *m, float *largeM, float **WMMTX, float *initverticalw, float *lastverticalw, int gyakuflag, float *maxwm )
{
	float *currentw, *previousw, *wtmp, *prept, *curpt;
	int lasti, lastj, i, j;
	int mpi, Mpi;
	int *mpjpt, *Mpjpt;
	short *ijpipt, *ijpjpt;
	float wm, g;
	float mi, Mi;
	float *mjpt, *Mjpt;
	float tbk;
	int tbki;
	int tbkj;
	float fpenalty = (float)penalty;
	float fpenalty_OP = (float)penalty_OP;
	float fpenalty_ex = (float)penalty_ex;
	float fpenalty_EX = (float)penalty_EX;
	float foffset = (float)offset;
	float localthr = -foffset;
	float localthr2 = -foffset;
	float pps;
	float *WMMTXpt;

	currentw = w1;
	previousw = w2;

	match_calc( initverticalw, seq2, seq1, 0, lgth1 );

	match_calc( currentw, seq1, seq2, 0, lgth2 );

	if( gyakuflag )
	{
		fprintf( stderr, "gyakudping\n" );
	}


	lastj = lgth2+1;
	for( j=1; j<lastj; ++j ) 
	{
		m[j] = currentw[j-1]; 
		mp[j] = 0;
		largeM[j] = currentw[j-1]; 
		Mp[j] = 0;
	}


	lastverticalw[0] = currentw[lgth2-1];



#if 0
fprintf( stderr, "currentw = \n" );
for( i=0; i<lgth1+1; i++ )
{
	fprintf( stderr, "%5.2f ", currentw[i] );
}
fprintf( stderr, "\n" );
fprintf( stderr, "initverticalw = \n" );
for( i=0; i<lgth2+1; i++ )
{
	fprintf( stderr, "%5.2f ", initverticalw[i] );
}
fprintf( stderr, "\n" );
#endif
#if DEBUG2
	fprintf( stderr, "\n" );
	fprintf( stderr, "       " );
	for( j=0; j<lgth2+1; j++ )
		fprintf( stderr, "%c     ", seq2[0][j] );
	fprintf( stderr, "\n" );
#endif

	localstop = lgth1+lgth2+1;
	*maxwm = -999.9;
	*endali = *endalj = 0;
#if DEBUG2
	fprintf( stderr, "\n" );
	fprintf( stderr, "%c   ", seq1[0][0] );

	for( j=0; j<lgth2+1; j++ )
		fprintf( stderr, "%5.0f ", currentw[j] );
	fprintf( stderr, "\n" );
#endif

	lasti = lgth1+1; //???
	for( i=1; i<lasti; i++ )
	{
		wtmp = previousw; 
		previousw = currentw;
		currentw = wtmp;

		previousw[0] = initverticalw[i-1];

		match_calc( currentw, seq1, seq2, i, lgth2 );
#if DEBUG2
		fprintf( stderr, "%c   ", seq1[0][i] );
		fprintf( stderr, "%5.0f ", currentw[0] );
#endif

#if XXXXXXX
fprintf( stderr, "\n" );
fprintf( stderr, "i=%d\n", i );
fprintf( stderr, "currentw = \n" );
for( j=0; j<lgth2; j++ )
{
	fprintf( stderr, "%5.2f ", currentw[j] );
}
fprintf( stderr, "\n" );
#endif
#if XXXXXXX
fprintf( stderr, "\n" );
fprintf( stderr, "i=%d\n", i );
fprintf( stderr, "currentw = \n" );
for( j=0; j<lgth2; j++ )
{
	fprintf( stderr, "%5.2f ", currentw[j] );
}
fprintf( stderr, "\n" );
#endif
		currentw[0] = initverticalw[i];

		mi = previousw[0]; 
		mpi = 0;
		Mi = previousw[0]; 
		Mpi = 0;

#if 0
		if( mi < localthr ) mi = localthr2;
#endif

		ijpipt = ijpi[i] + 1;
		ijpjpt = ijpj[i] + 1;
		mjpt = m + 1;
		Mjpt = largeM + 1;
		prept = previousw;
		curpt = currentw + 1;
		mpjpt = mp + 1;
		Mpjpt = Mp + 1;
		tbk = -999999.9;
		tbki = 0;
		tbkj = 0;
		lastj = lgth2+1; //???
		for( j=1; j<lastj; j++ )
		{
			wm = *prept;
			*ijpipt = i-1;
			*ijpjpt = j-1;


//			fprintf( stderr, "i,j=%d,%d %c-%c\n", i, j, seq1[0][i], seq2[0][j] );
//			fprintf( stderr, "wm=%f\n", wm );
#if 0
			fprintf( stderr, "%5.0f->", wm );
#endif
			g = mi + fpenalty;
#if 0
			fprintf( stderr, "%5.0f?", g );
#endif
			if( g > wm )
			{
				wm = g;
				*ijpjpt = mpi;
			}
			g = *prept;
			if( g > mi )
			{
				mi = g;
				mpi = j-1;
			}

#if USE_PENALTY_EX
			mi += fpenalty_ex;
#endif

#if 0
			fprintf( stderr, "%5.0f->", wm );
#endif
			g = *mjpt + fpenalty;
#if 0
			fprintf( stderr, "m%5.0f?", g );
#endif
			if( g > wm )
			{
				wm = g;
				*ijpipt = *mpjpt;
			}
			g = *prept;
			if( g > *mjpt )
			{
				*mjpt = g;
				*mpjpt = i-1;
			}
#if USE_PENALTY_EX
			*mjpt += fpenalty_ex;
#endif


			g =  tbk + fpenalty_OP; /*別の方がいいかも*/
			if( g > wm )
			{
				wm = g;
				*ijpipt = tbki;
				*ijpjpt = tbkj;
			}
			g = Mi;
			if( g > tbk )
			{
				tbk = g;
				tbki = i-1;
				tbkj = Mpi;
			}
			g = *Mjpt;
			if( g > tbk )
			{
				tbk = g;
				tbki = *Mpjpt;
				tbkj = j-1;
			}
//			tbk += fpenalty_EX;// + foffset;

			g = *prept;
			if( g > *Mjpt )
			{
				*Mjpt = g;
				*Mpjpt = i-1;
			}
//			*Mjpt += fpenalty_EX;// + foffset;

			g = *prept;
			if( g > Mi )
			{
				Mi = g;
				Mpi = j-1;
			}
//			Mi += fpenalty_EX;// + foffset;


//			fprintf( stderr, "wm=%f, tbk=%f(%c-%c), mi=%f, *mjpt=%f\n", wm, tbk, seq1[0][tbki], seq2[0][tbkj], mi, *mjpt );
//			fprintf( stderr, "ijp=%d-%d, ijp = %c,%c\n", *ijpipt, *ijpjpt, seq1[0][*ijpipt], seq2[0][*ijpjpt] );

			if( *maxwm < wm )
			{
				*maxwm = wm;
				*endali = i;
				*endalj = j;
			}
#if 0
			if( wm < localthr )
			{
//				fprintf( stderr, "stop i=%d, j=%d, curpt=%f\n", i, j, *curpt );
				*ijpipt = localstop;
//				*ijpjpt = localstop; /*いらない*/
				wm = localthr2;
			}
#endif
#if 0
			fprintf( stderr, "*curpt = %5.0f , wm=%f\n", *curpt, wm );
			fprintf( stderr, "WMMTX[i][j] =%f\n\n", WMMTX[i][j] );
#endif
#if DEBUG2
			fprintf( stderr, "%5.0f ", wm );
//			fprintf( stderr, "%c-%c *ijppt = %d, localstop = %d\n", seq1[0][i], seq2[0][j], *ijppt, localstop );
#endif
			if( gyakuflag )
			{
//				if ( *ijpipt != localstop && *ijpjpt != localstop )
//					WMMTX[lgth1-*ijpipt-1][lgth2-*ijpjpt-1]++;
			}
			else
			{
				fprintf( stderr, "*ijpipt=%d, ijpjpt=%d\n", *ijpipt, *ijpjpt );
				if ( *ijpipt != localstop && *ijpjpt != localstop )
					WMMTX[*ijpipt][*ijpjpt]++;
			}

			ijpipt++;
			ijpjpt++;
			mjpt++;
			Mjpt++;
			prept++;
			mpjpt++;
			Mpjpt++;
			curpt++;
		}
#if DEBUG2
		fprintf( stderr, "\n" );
#endif

		lastverticalw[i] = currentw[lgth2-1];
	}
}
static void do_dp( short **ijpi, short **ijpj, int *mp, int *Mp, int *endali, int *endalj, int lgth1, int lgth2, char **seq1, char **seq2, float *w1, float *w2, float *m, float *largeM, float **WMMTX, float *initverticalw, float *lastverticalw, int gyakuflag, float *maxwm )
{
	float *currentw, *previousw, *wtmp, *prept, *curpt;
	int lasti, lastj, i, j;
	int mpi, Mpi;
	int *mpjpt, *Mpjpt;
	short *ijpipt, *ijpjpt;
	float wm, g;
	float mi, Mi;
	float *mjpt, *Mjpt;
	float tbk;
	int tbki;
	int tbkj;
	float fpenalty = (float)penalty;
	float fpenalty_OP = (float)penalty_OP;
	float fpenalty_ex = (float)penalty_ex;
	float fpenalty_EX = (float)penalty_EX;
	float foffset = (float)offset;
	float localthr = -foffset;
	float localthr2 = -foffset;
	float pps;
	float *WMMTXpt;

	currentw = w1;
	previousw = w2;

	match_calc( initverticalw, seq2, seq1, 0, lgth1 );

	match_calc( currentw, seq1, seq2, 0, lgth2 );

	if( gyakuflag )
	{
//		for( i=1; i<lgth1; i++ ) WMMTX[lgth1-i-1][0] = initverticalw[i];
//		for( j=1; j<lgth2; j++ ) WMMTX[0][lgth2-j-1] = currentw[j];
//		WMMTX[lgth1-1][lgth2-1] = currentw[0];
		fprintf( stderr, "gyakudping\n" );
	}
	else
	{
		for( i=1; i<lgth1; i++ ) WMMTX[i][0] = initverticalw[i];
		for( j=1; j<lgth2; j++ ) WMMTX[0][j] = currentw[j];
		WMMTX[0][0] = currentw[0];
		fprintf( stderr, "in do_dp WMMTX[0][0] = %f\n", WMMTX[0][0] );
	}


	lastj = lgth2+1;
	for( j=1; j<lastj; ++j ) 
	{
		m[j] = currentw[j-1]; 
		mp[j] = 0;
		largeM[j] = currentw[j-1]; 
		Mp[j] = 0;
	}


	lastverticalw[0] = currentw[lgth2-1];



#if 0
fprintf( stderr, "currentw = \n" );
for( i=0; i<lgth1+1; i++ )
{
	fprintf( stderr, "%5.2f ", currentw[i] );
}
fprintf( stderr, "\n" );
fprintf( stderr, "initverticalw = \n" );
for( i=0; i<lgth2+1; i++ )
{
	fprintf( stderr, "%5.2f ", initverticalw[i] );
}
fprintf( stderr, "\n" );
#endif
#if DEBUG2
	fprintf( stderr, "\n" );
	fprintf( stderr, "       " );
	for( j=0; j<lgth2+1; j++ )
		fprintf( stderr, "%c     ", seq2[0][j] );
	fprintf( stderr, "\n" );
#endif

	localstop = lgth1+lgth2+1;
	*maxwm = -999.9;
	*endali = *endalj = 0;
#if DEBUG2
	fprintf( stderr, "\n" );
	fprintf( stderr, "%c   ", seq1[0][0] );

	for( j=0; j<lgth2+1; j++ )
		fprintf( stderr, "%5.0f ", currentw[j] );
	fprintf( stderr, "\n" );
#endif

	lasti = lgth1+1; //???
	for( i=1; i<lasti; i++ )
	{
		wtmp = previousw; 
		previousw = currentw;
		currentw = wtmp;

		previousw[0] = initverticalw[i-1];

		match_calc( currentw, seq1, seq2, i, lgth2 );
#if DEBUG2
		fprintf( stderr, "%c   ", seq1[0][i] );
		fprintf( stderr, "%5.0f ", currentw[0] );
#endif

#if XXXXXXX
fprintf( stderr, "\n" );
fprintf( stderr, "i=%d\n", i );
fprintf( stderr, "currentw = \n" );
for( j=0; j<lgth2; j++ )
{
	fprintf( stderr, "%5.2f ", currentw[j] );
}
fprintf( stderr, "\n" );
#endif
#if XXXXXXX
fprintf( stderr, "\n" );
fprintf( stderr, "i=%d\n", i );
fprintf( stderr, "currentw = \n" );
for( j=0; j<lgth2; j++ )
{
	fprintf( stderr, "%5.2f ", currentw[j] );
}
fprintf( stderr, "\n" );
#endif
		currentw[0] = initverticalw[i];

		mi = previousw[0]; 
		mpi = 0;
		Mi = previousw[0]; 
		Mpi = 0;

#if 0
		if( mi < localthr ) mi = localthr2;
#endif

		ijpipt = ijpi[i] + 1;
		ijpjpt = ijpj[i] + 1;
		mjpt = m + 1;
		Mjpt = largeM + 1;
		prept = previousw;
		curpt = currentw + 1;
		mpjpt = mp + 1;
		Mpjpt = Mp + 1;
		tbk = -999999.9;
		tbki = 0;
		tbkj = 0;
		lastj = lgth2+1; //???
		for( j=1; j<lastj; j++ )
		{
			wm = *prept;
			*ijpipt = i-1;
			*ijpjpt = j-1;


//			fprintf( stderr, "i,j=%d,%d %c-%c\n", i, j, seq1[0][i], seq2[0][j] );
//			fprintf( stderr, "wm=%f\n", wm );
#if 0
			fprintf( stderr, "%5.0f->", wm );
#endif
			g = mi + fpenalty;
#if 0
			fprintf( stderr, "%5.0f?", g );
#endif
			if( g > wm )
			{
				wm = g;
				*ijpjpt = mpi;
			}
			g = *prept;
			if( g > mi )
			{
				mi = g;
				mpi = j-1;
			}

#if USE_PENALTY_EX
			mi += fpenalty_ex;
#endif

#if 0
			fprintf( stderr, "%5.0f->", wm );
#endif
			g = *mjpt + fpenalty;
#if 0
			fprintf( stderr, "m%5.0f?", g );
#endif
			if( g > wm )
			{
				wm = g;
				*ijpipt = *mpjpt;
			}
			g = *prept;
			if( g > *mjpt )
			{
				*mjpt = g;
				*mpjpt = i-1;
			}
#if USE_PENALTY_EX
			*mjpt += fpenalty_ex;
#endif


			g =  tbk + fpenalty_OP; /*別の方がいいかも*/
			if( g > wm )
			{
				wm = g;
				*ijpipt = tbki;
				*ijpjpt = tbkj;
			}
			g = Mi;
			if( g > tbk )
			{
				tbk = g;
				tbki = i-1;
				tbkj = Mpi;
			}
			g = *Mjpt;
			if( g > tbk )
			{
				tbk = g;
				tbki = *Mpjpt;
				tbkj = j-1;
			}
//			tbk += fpenalty_EX;// + foffset;

			g = *prept;
			if( g > *Mjpt )
			{
				*Mjpt = g;
				*Mpjpt = i-1;
			}
//			*Mjpt += fpenalty_EX;// + foffset;

			g = *prept;
			if( g > Mi )
			{
				Mi = g;
				Mpi = j-1;
			}
//			Mi += fpenalty_EX;// + foffset;


//			fprintf( stderr, "wm=%f, tbk=%f(%c-%c), mi=%f, *mjpt=%f\n", wm, tbk, seq1[0][tbki], seq2[0][tbkj], mi, *mjpt );
//			fprintf( stderr, "ijp=%d-%d, ijp = %c,%c\n", *ijpipt, *ijpjpt, seq1[0][*ijpipt], seq2[0][*ijpjpt] );

//			if( *maxwm < wm )
//			{
//				*maxwm = wm;
//				*endali = i;
//				*endalj = j;
//			}
#if 1
			if( wm < localthr )
			{
//				fprintf( stderr, "stop i=%d, j=%d, curpt=%f\n", i, j, *curpt );
				*ijpipt = localstop;
//				*ijpjpt = localstop; /*いらない*/
				wm = localthr2;
			}
#endif
#if 0
			fprintf( stderr, "*curpt = %5.0f , wm=%f\n", *curpt, wm );
			fprintf( stderr, "WMMTX[i][j] =%f\n\n", WMMTX[i][j] );
#endif
#if DEBUG2
			fprintf( stderr, "%5.0f ", wm );
//			fprintf( stderr, "%c-%c *ijppt = %d, localstop = %d\n", seq1[0][i], seq2[0][j], *ijppt, localstop );
#endif

			pps = *curpt;
			*curpt += wm;
			if( i < lgth1 && j < lgth2 )
			{
//				fprintf( stderr, "i=%d, j=%d, WMMTX = %f -> ", i, j, WMMTX[i][j] );
				if( gyakuflag )
				{
					WMMTXpt = WMMTX[lgth1-i-1] + lgth2-j-1;
					*WMMTXpt += *curpt - pps;
					if( *maxwm < *WMMTXpt )
					{
						*maxwm = *WMMTXpt;
						*endali = i;
						*endalj = j;
					}
				}
				else
				{
					WMMTX[i][j] = *curpt;
				}
//				fprintf( stderr, "%f \n", WMMTX[i][j] );
			}
			ijpipt++;
			ijpjpt++;
			mjpt++;
			Mjpt++;
			prept++;
			mpjpt++;
			Mpjpt++;
			curpt++;
		}
#if DEBUG2
		fprintf( stderr, "\n" );
#endif

		lastverticalw[i] = currentw[lgth2-1];
	}
}

float VAalign11( char **seq1, char **seq2, int alloclen, int *off1pt, int *off2pt, LocalHom *lhmpt )
/* score no keisan no sai motokaraaru gap no atukai ni mondai ga aru */
{
//	int k;
	register int i, j;
	int lasti;                      /* outgap == 0 -> lgth1, outgap == 1 -> lgth1+1 */
	int lgth1, lgth2;
	int resultlen;
	float wm;   /* int ?????? */
//	float g;
//	float *currentw, *previousw;
#if 1
//	float *wtmp;
//	short *ijpipt;
//	short *ijpjpt;
//	float *mjpt, *Mjpt, *prept, *curpt;
//	int *mpjpt, *Mpjpt;
#endif
	static float mi, *m;
	static float Mi, *largeM;
	static short **ijpi;
	static short **ijpj;
	static int mpi, *mp;
	static int Mpi, *Mp;
	static float *w1, *w2;
//	static float *match;
	static float *initverticalw;    /* kufuu sureba iranai */
	static float *lastverticalw;    /* kufuu sureba iranai */
	static char **mseq1;
	static char **mseq2;
	static char **gseq1, **gseq2;
	static char **mseq;
	static float **cpmx1;
	static float **cpmx2;
	static int **intwork;
	static float **floatwork;
	static float **WMMTX;
	static int orlgth1 = 0, orlgth2 = 0;
	float maxwm;
	float tbk;
	int tbki, tbkj;
	int endali, endalj;
	float dumm;
//	float localthr = 0.0;
//	float localthr2 = 0.0;


//	fprintf( stderr, "@@@@@@@@@@@@@ penalty_OP = %f, penalty_EX = %f, pelanty = %f\n", fpenalty_OP, fpenalty_EX, fpenalty );

	if( orlgth1 == 0 )
	{
		mseq1 = AllocateCharMtx( njob, 0 );
		mseq2 = AllocateCharMtx( njob, 0 );
	}


	lgth1 = strlen( seq1[0] );
	lgth2 = strlen( seq2[0] );

	if( lgth1 > orlgth1 || lgth2 > orlgth2 )
	{
		int ll1, ll2;

		if( orlgth1 > 0 && orlgth2 > 0 )
		{
			FreeFloatVec( w1 );
			FreeFloatVec( w2 );
//			FreeFloatVec( match );
			FreeFloatVec( initverticalw );
			FreeFloatVec( lastverticalw );

			FreeFloatVec( m );
			FreeIntVec( mp );
			FreeFloatVec( largeM );
			FreeIntVec( Mp );

			FreeCharMtx( mseq );
			FreeCharMtx( gseq1 );
			FreeCharMtx( gseq2 );

			FreeFloatMtx( cpmx1 );
			FreeFloatMtx( cpmx2 );

			FreeFloatMtx( floatwork );
			FreeIntMtx( intwork );

		}

		ll1 = MAX( (int)(1.3*lgth1), orlgth1 ) + 100;
		ll2 = MAX( (int)(1.3*lgth2), orlgth2 ) + 100;

#if DEBUG
		fprintf( stderr, "\ntrying to allocate (%d+%d)xn matrices ... ", ll1, ll2 );
#endif

		w1 = AllocateFloatVec( ll2+2 );
		w2 = AllocateFloatVec( ll2+2 );
//		match = AllocateFloatVec( ll2+2 );

		initverticalw = AllocateFloatVec( ll1+2 );
		lastverticalw = AllocateFloatVec( ll1+2 );

		m = AllocateFloatVec( ll2+2 );
		mp = AllocateIntVec( ll2+2 );
		largeM = AllocateFloatVec( ll2+2 );
		Mp = AllocateIntVec( ll2+2 );

		mseq = AllocateCharMtx( 2, ll1+ll2 );

		gseq1 = AllocateCharMtx( 1, ll1+ll2 );
		gseq2 = AllocateCharMtx( 1, ll1+ll2 );

		cpmx1 = AllocateFloatMtx( 26, ll1+2 );
		cpmx2 = AllocateFloatMtx( 26, ll2+2 );

		floatwork = AllocateFloatMtx( 26, MAX( ll1, ll2 )+2 ); 
		intwork = AllocateIntMtx( 26, MAX( ll1, ll2 )+2 ); 


#if DEBUG
		fprintf( stderr, "succeeded\n" );
#endif

		orlgth1 = ll1 - 100;
		orlgth2 = ll2 - 100;
	}


	mseq1[0] = mseq[0];
	mseq2[0] = mseq[1];


	if( orlgth1 > commonAlloc1 || orlgth2 > commonAlloc2 )
	{
		int ll1, ll2;

		if( commonAlloc1 && commonAlloc2 )
		{
			FreeShortMtx( commonIP );
			FreeShortMtx( commonJP );
			FreeFloatMtx( WMMTX );
		}

		ll1 = MAX( orlgth1, commonAlloc1 );
		ll2 = MAX( orlgth2, commonAlloc2 );

#if DEBUG
		fprintf( stderr, "\n\ntrying to allocate %dx%d matrices ... ", ll1+1, ll2+1 );
#endif

		commonIP = AllocateShortMtx( ll1+10, ll2+10 );
		commonJP = AllocateShortMtx( ll1+10, ll2+10 );
		fprintf( stderr, "allocating WMMTX\n" );
		WMMTX = AllocateFloatMtx( ll1+10, ll2+10 );
		fprintf( stderr, "done\n" );

#if DEBUG
		fprintf( stderr, "succeeded\n\n" );
#endif

		commonAlloc1 = ll1;
		commonAlloc2 = ll2;
	}
	ijpi = commonIP;
	ijpj = commonJP;


#if 0
	for( i=0; i<lgth1; i++ ) 
		fprintf( stderr, "ogcp1[%d]=%f\n", i, ogcp1[i] );
#endif

	for( i=0; i<lgth1; i++ ) for( j=0; j<lgth2; j++ ) WMMTX[i][j] = 0.0; //dp2 no toki dake
	do_dp2( ijpi, ijpj, mp, Mp, &endali, &endalj, lgth1, lgth2, seq1, seq2, w1, w2, m, largeM, WMMTX, initverticalw, lastverticalw, 0, &dumm );


#if 0
	fprintf( stderr, "WMMTXX = \n" );
	for( j=0; j<lgth2; j++ )
		fprintf( stderr, "% 8.0d ", j );
	for( i=0; i<lgth1; i++ )
	{
		fprintf( stderr, "i=%d ", i );
		for( j=0; j<lgth2; j++ )
			fprintf( stderr, "% 8.2f ", WMMTX[i][j] );
		fprintf( stderr, "\n" );
	}

	fprintf( stderr, "ijp = \n" );
	for( i=0; i<lgth1; i++ )
	{
		fprintf( stderr, "i=%d ", i );
		for( j=0; j<lgth2; j++ )
			fprintf( stderr, "%d-%d ", ijpi[i][j], ijpj[i][j] );
		fprintf( stderr, "\n" );
	}
#endif


#if 0
	fprintf( stderr, "endali = %d\n", endali );
	fprintf( stderr, "endalj = %d\n", endalj );
#endif
		
#if 0
	gentracking( seq1, seq2, mseq1, mseq2, cpmx1, cpmx2, ijpi, ijpj, off1pt, off2pt, endali, endalj );

//	fprintf( stderr, "### impmatch = %f\n", *impmatch );

	resultlen = strlen( mseq1[0] );
	if( alloclen < resultlen || resultlen > N )
	{
		fprintf( stderr, "alloclen=%d, resultlen=%d, N=%d\n", alloclen, resultlen, N );
		ErrorExit( "LENGTH OVER!\n" );
	}


	fprintf( stderr, "\n" );
	fprintf( stderr, ">\n%s\n", mseq1[0] );
	fprintf( stderr, ">\n%s\n", mseq2[0] );
#endif


#if 0
	fprintf( stderr, "WMMTXX = \n" );
	for( i=0; i<lgth1; i++ )
	{
		fprintf( stderr, "i=%d ", i );
		for( j=0; j<lgth2; j++ )
			fprintf( stderr, "% 8.2f ", WMMTX[i][j] );
		fprintf( stderr, "\n" );
	}
#endif

	gyakuseq( gseq1[0], seq1[0] );
	gyakuseq( gseq2[0], seq2[0] );

#if 0
	fprintf( stderr, "gseq1[0] = %s\n", gseq1[0] );
	fprintf( stderr, "gseq2[0] = %s\n", gseq2[0] );

	fprintf( stderr, "lgth1,lgth2=%d,%d\n", lgth1, lgth2 );
#endif

	do_dp2( ijpi, ijpj, mp, Mp, &endali, &endalj, lgth1, lgth2, gseq1, gseq2, w1, w2, m, largeM, WMMTX, initverticalw, lastverticalw, 1, &maxwm  );
#if 0
	fprintf( stderr, "tracking n" );
	gentracking( gseq1, gseq2, mseq1, mseq2, cpmx1, cpmx2, ijpi, ijpj, off1pt, off2pt, endali, endalj );
	fprintf( stderr, "\n" );
	fprintf( stderr, ">\n%s\n", mseq1[0] );
	fprintf( stderr, ">\n%s\n", mseq2[0] );

	fprintf( stderr, "maxwm = %f\n", maxwm );

#endif
#if 1

	fprintf( stderr, "WMMTXX = \n" );
	fprintf( stderr, "  " );
	for( j=0; j<20; j++ )
		fprintf( stderr, "% 6.0d ", j );
	fprintf( stderr, "\n" );
	for( j=0; j<20; j++ )
		fprintf( stderr, "% 6.0c ", seq2[0][j] );
	fprintf( stderr, "\n" );
	for( i=0; i<20; i++ )
	{
		fprintf( stderr, "% 2.0d ", i );
		fprintf( stderr, "% 2.0c ", seq1[0][i] );
		for( j=0; j<20; j++ )
			fprintf( stderr, "% 6.0f ", WMMTX[i][j] );
		fprintf( stderr, "\n" );
	}
	fprintf( stderr, "ijpmtx = \n" );
	fprintf( stderr, "  " );
	for( j=0; j<20; j++ )
		fprintf( stderr, "% 6.0d ", j );
	fprintf( stderr, "\n" );
	for( j=0; j<20; j++ )
		fprintf( stderr, "% 6.0c ", seq2[0][j] );
	fprintf( stderr, "\n" );
	for( i=0; i<20; i++ )
	{
		fprintf( stderr, "% 2.0d ", i );
		fprintf( stderr, "% 2.0c ", seq1[0][i] );
		for( j=0; j<20; j++ )
			fprintf( stderr, " %02d,%02d", (int)ijpi[i][j], (int)ijpj[i][j] );
		fprintf( stderr, "\n" );
	}
#endif

	searchsubopts( lgth1, lgth2, WMMTX, maxwm*0.999, lhmpt );

	strcpy( seq1[0], mseq1[0] );
	strcpy( seq2[0], mseq2[0] );

	return( maxwm );
}

