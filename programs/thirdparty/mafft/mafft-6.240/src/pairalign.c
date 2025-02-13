#include "mltaln.h"

#define DEBUG 0
#define IODEBUG 0
#define SCOREOUT 1


void arguments( int argc, char *argv[] )
{
    int c;

	inputfile = NULL;
	fftkeika = 0;
	pslocal = -1000.0;
	constraint = 0;
	nblosum = 62;
	fmodel = 0;
	calledByXced = 0;
	devide = 0;
	use_fft = 0;
	fftscore = 1;
	fftRepeatStop = 0;
	fftNoAnchStop = 0;
    weight = 3;
    utree = 1;
	tbutree = 1;
    refine = 0;
    check = 1;
    cut = 0.0;
    disp = 0;
    outgap = 1;
    alg = 'A';
    mix = 0;
	tbitr = 0;
	scmtd = 5;
	tbweight = 0;
	tbrweight = 3;
	checkC = 0;
	treemethod = 'x';
	contin = 0;
	scoremtx = 0;
	kobetsubunkatsu = 0;
	divpairscore = 0;
	dorp = NOTSPECIFIED;
	ppenalty = NOTSPECIFIED;
	ppenalty_ex = NOTSPECIFIED;
	poffset = NOTSPECIFIED;
	kimuraR = NOTSPECIFIED;
	pamN = NOTSPECIFIED;
	geta2 = GETA2;
	fftWinSize = NOTSPECIFIED;
	fftThreshold = NOTSPECIFIED;

    while( --argc > 0 && (*++argv)[0] == '-' )
	{
        while ( c = *++argv[0] )
		{
            switch( c )
            {
				case 'i':
					inputfile = *++argv;
					fprintf( stderr, "inputfile = %s\n", inputfile );
					--argc;
					goto nextoption;
				case 'f':
					ppenalty = (int)( atof( *++argv ) * 1000 - 0.5 );
					fprintf( stderr, "ppenalty = %d\n", ppenalty );
					--argc;
					goto nextoption;
				case 'g':
					ppenalty_ex = (int)( atof( *++argv ) * 1000 - 0.5 );
					fprintf( stderr, "ppenalty_ex = %d\n", ppenalty_ex );
					--argc;
					goto nextoption;
				case 'h':
					poffset = (int)( atof( *++argv ) * 1000 - 0.5 );
					fprintf( stderr, "poffset = %d\n", poffset );
					--argc;
					goto nextoption;
				case 'k':
					kimuraR = atoi( *++argv );
					fprintf( stderr, "kimuraR = %d\n", kimuraR );
					--argc;
					goto nextoption;
				case 'b':
					nblosum = atoi( *++argv );
					scoremtx = 1;
					fprintf( stderr, "blosum %d\n", nblosum );
					--argc;
					goto nextoption;
				case 'j':
					pamN = atoi( *++argv );
					scoremtx = 0;
					fprintf( stderr, "jtt %d\n", pamN );
					--argc;
					goto nextoption;
				case 'l':
					ppslocal = (int)( atof( *++argv ) * 1000 + 0.5 );
					pslocal = (int)( 600.0 / 1000.0 * ppslocal + 0.5);
					fprintf( stderr, "ppslocal = %d\n", ppslocal );
					fprintf( stderr, "pslocal = %d\n", pslocal );
					--argc;
					goto nextoption;
				case 'm':
					fmodel = 1;
					break;
				case 'r':
					fmodel = -1;
					break;
				case 'D':
					dorp = 'd';
					break;
				case 'P':
					dorp = 'p';
					break;
				case 'e':
					fftscore = 0;
					break;
				case 'O':
					fftNoAnchStop = 1;
					break;
				case 'R':
					fftRepeatStop = 1;
					break;
				case 'Q':
					calledByXced = 1;
					break;
				case 's':
					treemethod = 's';
					break;
				case 'x':
					treemethod = 'x';
					break;
				case 'p':
					treemethod = 'p';
					break;
				case 'a':
					alg = 'a';
					break;
				case 'A':
					alg = 'A';
					break;
				case 'S':
					alg = 'S';
					break;
				case 'C':
					alg = 'C';
					break;
				case 'F':
					use_fft = 1;
					break;
				case 'v':
					tbrweight = 3;
					break;
				case 'd':
					divpairscore = 1;
					break;
				case 'o':
					outgap = 0;
					break;
/* Modified 01/08/27, default: user tree */
				case 'J':
					tbutree = 0;
					break;
/* modification end. */
				case 'z':
					fftThreshold = atoi( *++argv );
					--argc; 
					goto nextoption;
				case 'w':
					fftWinSize = atoi( *++argv );
					--argc;
					goto nextoption;
				case 'Z':
					checkC = 1;
					break;
                default:
                    fprintf( stderr, "illegal option %c\n", c );
                    argc = 0;
                    break;
            }
		}
		nextoption:
			;
	}
    if( argc == 1 )
    {
        cut = atof( (*argv) );
        argc--;
    }
    if( argc != 0 ) 
    {
        fprintf( stderr, "options: Check source file !\n" );
        exit( 1 );
    }
	if( tbitr == 1 && outgap == 0 )
	{
		fprintf( stderr, "conflicting options : o, m or u\n" );
		exit( 1 );
	}
	if( alg == 'C' && outgap == 0 )
	{
		fprintf( stderr, "conflicting options : C, o\n" );
		exit( 1 );
	}
}

int countamino( char *s, int end )
{
	int val = 0;
	while( end-- )
		if( *s++ != '-' ) val++;
	return( val );
}

void pairalign( char name[M][B], int nlen[M], char **seq, char **aseq, char **mseq1, char **mseq2, double *effarr, int alloclen )
{
	int i, j, l;
	int clus1, clus2;
	int s1, s2, r1, r2, offset;
	float pscore;
	static char *indication1, *indication2;
	FILE *trap;
	FILE *hat2p, *hat3p;
	static char name1[M][B], name2[M][B];
	static double **distancemtx;
	static double *effarr1 = NULL;
	static double *effarr2 = NULL;
	float dumfl;
	double total;
	char *pt;
	char *hat2file = "hat2";
	LocalHom **localhomtable, *tmpptr;
	static char **pair;
	int intdum;

	localhomtable = (LocalHom **)calloc( njob, sizeof( LocalHom *) );
	for( i=0; i<njob; i++)
	{
		localhomtable[i] = (LocalHom *)calloc( njob, sizeof( LocalHom ) );
		for( j=0; j<njob; j++)
		{
			localhomtable[i][j].start1 = -1;
			localhomtable[i][j].end1 = -1;
			localhomtable[i][j].start2 = -1; 
			localhomtable[i][j].end2 = -1; 
			localhomtable[i][j].opt = -1.0;
			localhomtable[i][j].next = NULL;
		}
	}

	if( effarr1 == NULL ) 
	{
		distancemtx = AllocateDoubleMtx( njob, njob );
		effarr1 = AllocateDoubleVec( njob );
		effarr2 = AllocateDoubleVec( njob );
		indication1 = AllocateCharVec( 150 );
		indication2 = AllocateCharVec( 150 );
#if 0
#else
		pair = AllocateCharMtx( njob, njob );
#endif
	}

#if 0
	fprintf( stderr, "##### fftwinsize = %d, fftthreshold = %d\n", fftWinSize, fftThreshold );
#endif

#if 0
	for( i=0; i<njob; i++ )
		fprintf( stderr, "TBFAST effarr[%d] = %f\n", i, effarr[i] );
#endif


	writePre( njob, name, nlen, aseq, 0 );

	for( i=0; i<njob; i++ ) for( j=0; j<njob; j++ ) pair[i][j] = 0;
	for( i=0; i<njob; i++ ) pair[i][i] = 1;

	for( i=0; i<njob-1; i++ ) 
	{
		fprintf( stderr, "%d / %d\r", i, njob );
		for( j=i+1; j<njob; j++ )
		{
	
			strcpy( aseq[i], seq[i] );
			strcpy( aseq[j], seq[j] );
			clus1 = conjuctionfortbfast( pair, i, aseq, mseq1, effarr1, effarr, indication1 );
			clus2 = conjuctionfortbfast( pair, j, aseq, mseq2, effarr2, effarr, indication2 );
	//		fprintf( stderr, "mseq1 = %s\n", mseq1[0] );
	//		fprintf( stderr, "mseq2 = %s\n", mseq2[0] );
	
	#if 0
			fprintf( stderr, "group1 = %.66s", indication1 );
			fprintf( stderr, "\n" );
			fprintf( stderr, "group2 = %.66s", indication2 );
			fprintf( stderr, "\n" );
	#endif
	//		for( l=0; l<clus1; l++ ) fprintf( stderr, "## STEP-eff for mseq1-%d %f\n", l, effarr1[l] );
	
			if( use_fft )
			{
				pscore = Falign( mseq1, mseq2, effarr1, effarr2, clus1, clus2, alloclen, &intdum );
			}
			else
			{
				switch( alg )
				{
					case( 'a' ):
						pscore = Aalign( mseq1, mseq2, effarr1, effarr2, clus1, clus2, alloclen );
						break;
					case( 'A' ):
						pscore = G__align11( mseq1, mseq2, alloclen );
						break;
					default:
						ErrorExit( "ERROR IN SOURCE FILE" );
				}
			}
			distancemtx[i][j] = pscore;
	#if SCOREOUT
	//		fprintf( stderr, "score = %10.2f\n", pscore );
	#endif
//			fprintf( stderr, "pslocal = %d\n", pslocal );
			offset = makelocal( *mseq1, *mseq2, pslocal );
			offset = 0;
			fprintf( stderr, "offset = %d\n", offset );
			if( offset ) exit( 1 ) ;

#if 0
			fprintf( stderr, "*mseq1 = %s\n", *mseq1+offset );
			fprintf( stderr, "*mseq2 = %s\n", *mseq2+offset );
			fprintf( stderr, "offset in 1 = %d\n", countamino( *mseq1, offset ) );
			fprintf( stderr, "offset in 2 = %d\n", countamino( *mseq2, offset ) );
#endif
			putlocalhom( mseq1[0]+offset, mseq2[0]+offset, localhomtable[i]+j, countamino( *mseq1, offset ), countamino( *mseq2, offset ), pscore, strlen( mseq1[0] ) );
//			putlocalhom2( mseq1[0], mseq2[0], localhomtable[i]+j, 0, 0, pscore, strlen( mseq1[0] ) );
		}
	}
	for( i=0; i<njob; i++ )
	{
		pscore = 0.0;
		for( pt=seq[i]; *pt; pt++ )
			pscore += amino_dis[(int)*pt][(int)*pt];
		distancemtx[i][i] = pscore;
//		fprintf( stderr, "distancemtx[%d][%d] = %f\n", i, i, distancemtx[i][i] );

	}

	for( i=0; i<njob-1; i++ )
	{
		for( j=i+1; j<njob; j++ )
		{
//			fprintf( stderr, "distancemtx[%d][%d] = %f\n", i, j, distancemtx[i][j] );
			distancemtx[i][j] = ( 1.0 - distancemtx[i][j] / MIN( distancemtx[i][i], distancemtx[j][j] ) ) * 2.0;
//			fprintf( stderr, "distancemtx2[%d][%d] = %f\n", i, j, distancemtx[i][j] );
		}
	}

	hat2p = fopen( hat2file, "w" );
	if( !hat2p ) ErrorExit( "Cannot open hat2." );
	WriteHat2( hat2p, njob, name, distancemtx );
	fclose( hat2p );

	fprintf( stderr, "##### writing hat3\n" );
	hat3p = fopen( "hat3", "w" );
	if( !hat3p ) ErrorExit( "Cannot open hat3." );
	for( i=0; i<njob-1; i++ ) for( j=i+1; j<njob; j++ )
	{
		for( tmpptr=localhomtable[i]+j; tmpptr; tmpptr=tmpptr->next )
		{
			if( tmpptr->opt == -1.0 ) continue;
			fprintf( hat3p, "%d %d %d %6.3f %d %d %d %d %p\n", i, j, tmpptr->overlapaa, tmpptr->opt, tmpptr->start1, tmpptr->end1, tmpptr->start2, tmpptr->end2, tmpptr->next ); 
		}
	}
	fclose( hat3p );
}

static void WriteOptions( FILE *fp )
{

	if( dorp == 'd' ) fprintf( fp, "DNA\n" );
	else
	{
		if     ( scoremtx ==  0 ) fprintf( fp, "JTT %dPAM\n", pamN );
		else if( scoremtx ==  1 ) fprintf( fp, "BLOSUM %d\n", nblosum );
		else if( scoremtx ==  2 ) fprintf( fp, "M-Y\n" );
	}
    fprintf( stderr, "Gap Penalty = %+5.2f, %+5.2f, %+5.2f\n", (double)ppenalty/1000, (double)ppenalty_ex/1000, (double)poffset/1000 );
    if( use_fft ) fprintf( fp, "FFT on\n" );

	fprintf( fp, "tree-base method\n" );
	if( tbrweight == 0 ) fprintf( fp, "unweighted\n" );
	else if( tbrweight == 3 ) fprintf( fp, "clustalw-like weighting\n" );
	if( tbitr || tbweight ) 
	{
		fprintf( fp, "iterate at each step\n" );
		if( tbitr && tbrweight == 0 ) fprintf( fp, "  unweighted\n" ); 
		if( tbitr && tbrweight == 3 ) fprintf( fp, "  reversely weighted\n" ); 
		if( tbweight ) fprintf( fp, "  weighted\n" ); 
		fprintf( fp, "\n" );
	}

   	 fprintf( fp, "Gap Penalty = %+5.2f, %+5.2f, %+5.2f\n", (double)ppenalty/1000, (double)ppenalty_ex/1000, (double)poffset/1000 );

	if( alg == 'a' )
		fprintf( fp, "Algorithm A\n" );
	else if( alg == 'A' ) 
		fprintf( fp, "Algorithm A+\n" );
	else if( alg == 'S' ) 
		fprintf( fp, "Apgorithm S\n" );
	else if( alg == 'C' ) 
		fprintf( fp, "Apgorithm A+/C\n" );
	else
		fprintf( fp, "Unknown algorithm\n" );

	if( treemethod == 'x' )
		fprintf( fp, "Tree = UPGMA (3).\n" );
	else if( treemethod == 's' )
		fprintf( fp, "Tree = UPGMA (2).\n" );
	else if( treemethod == 'p' )
		fprintf( fp, "Tree = UPGMA (1).\n" );
	else
		fprintf( fp, "Unknown tree.\n" );

    if( use_fft )
    {
        fprintf( fp, "FFT on\n" );
        if( dorp == 'd' )
            fprintf( fp, "Basis : 4 nucleotides\n" );
        else
        {
            if( fftscore )
                fprintf( fp, "Basis : Polarity and Volume\n" );
            else
                fprintf( fp, "Basis : 20 amino acids\n" );
        }
        fprintf( fp, "Threshold   of anchors = %d%%\n", fftThreshold );
        fprintf( fp, "window size of anchors = %dsites\n", fftWinSize );
    }
	else
        fprintf( fp, "FFT off\n" );
	fflush( fp );
}
	 

int main( int argc, char *argv[] )
{
	static int  nlen[M];	
	static char name[M][B], **seq;
	static char **mseq1, **mseq2;
	static char **aseq;
	static char **bseq;
	static double **pscore;
	static double *eff;
	static double **node0, **node1;
	int i, j;
	int identity;
	static int ***topol;
	static double **len;
	FILE *prep, *infp;
	char c;
	int alloclen;
	double total;

	arguments( argc, argv );

	if( inputfile )
	{
		infp = fopen( inputfile, "r" );
		if( !infp )
		{
			fprintf( stderr, "Cannot open %s\n", inputfile );
			exit( 1 );
		}
	}
	else
		infp = stdin;

	getnumlen( infp );
	rewind( infp );

	if( njob < 2 )
	{
		fprintf( stderr, "At least 2 sequences should be input!\n"
						 "Only %d sequence found.\n", njob ); 
		exit( 1 );
	}

	seq = AllocateCharMtx( njob, nlenmax*9+1 );
	aseq = AllocateCharMtx( njob, nlenmax*9+1 );
	bseq = AllocateCharMtx( njob, nlenmax*9+1 );
	mseq1 = AllocateCharMtx( njob, 1 );
	mseq2 = AllocateCharMtx( njob, 1 );
	alloclen = nlenmax*9;

	eff = AllocateDoubleVec( njob );

#if 0
	Read( name, nlen, seq );
#else
	readData( infp, name, nlen, seq );
#endif
	fclose( infp );

	constants( njob, seq );

#if 0
	fprintf( stderr, "params = %d, %d, %d\n", penalty, penalty_ex, offset );
#endif

	initSignalSM();

	initFiles();

	WriteOptions( trap_g );

	c = seqcheck( seq );
	if( c )
	{
		fprintf( stderr, "Illeagal character %c\n", c );
		exit( 1 );
	}

	writePre( njob, name, nlen, seq, 0 );

	for( i=0; i<njob; i++ ) eff[i] = 1.0;


	for( i=0; i<njob; i++ ) gappick0( bseq[i], seq[i] );

	pairalign( name, nlen, bseq, aseq, mseq1, mseq2, eff, alloclen );


	fprintf( trap_g, "done.\n" );
	fclose( trap_g );

	writePre( njob, name, nlen, aseq, !contin );
#if 0
	writeData( stdout, njob, name, nlen, aseq );
#endif
#if IODEBUG
	fprintf( stderr, "OSHIMAI\n" );
#endif
	SHOWVERSION;
	return( 0 );
}
