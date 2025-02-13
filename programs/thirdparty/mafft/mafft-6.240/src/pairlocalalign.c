#include "mltaln.h"

#define DEBUG 0
#define IODEBUG 0
#define SCOREOUT 0



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
	scoremtx = 1;
	kobetsubunkatsu = 0;
	divpairscore = 0;
	dorp = NOTSPECIFIED;
	ppenalty = NOTSPECIFIED;
	ppenalty_OP = NOTSPECIFIED;
	ppenalty_ex = NOTSPECIFIED;
	ppenalty_EX = NOTSPECIFIED;
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
					--argc;
					goto nextoption;
				case 'g':
					ppenalty_ex = (int)( atof( *++argv ) * 1000 - 0.5 );
					--argc;
					goto nextoption;
				case 'O':
					ppenalty_OP = (int)( atof( *++argv ) * 1000 - 0.5 );
					--argc;
					goto nextoption;
				case 'E':
					ppenalty_EX = (int)( atof( *++argv ) * 1000 - 0.5 );
					--argc;
					goto nextoption;
				case 'h':
					poffset = (int)( atof( *++argv ) * 1000 - 0.5 );
					--argc;
					goto nextoption;
				case 'k':
					kimuraR = atoi( *++argv );
//					fprintf( stderr, "kimuraR = %d\n", kimuraR );
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
					TMorJTT = JTT;
					fprintf( stderr, "jtt %d\n", pamN );
					--argc;
					goto nextoption;
				case 'm':
					pamN = atoi( *++argv );
					scoremtx = 0;
					TMorJTT = TM;
					fprintf( stderr, "TM %d\n", pamN );
					--argc;
					goto nextoption;
				case 'l':
					ppslocal = (int)( atof( *++argv ) * 1000 + 0.5 );
					pslocal = (int)( 600.0 / 1000.0 * ppslocal + 0.5);
//					fprintf( stderr, "ppslocal = %d\n", ppslocal );
//					fprintf( stderr, "pslocal = %d\n", pslocal );
					--argc;
					goto nextoption;
#if 1
				case 'a':
					fmodel = 1;
					break;
#endif
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
#if 0
				case 'O':
					fftNoAnchStop = 1;
					break;
				case 'R':
					fftRepeatStop = 1;
					break;
#endif
				case 'Q':
					calledByXced = 1;
					break;
				case 's':
					treemethod = 's';
					break;
				case 'x':
					disp = 1;
					break;
				case 'p':
					treemethod = 'p';
					break;
#if 0
				case 'a':
					alg = 'a';
					break;
#endif
				case 'S':
					alg = 'S';
					break;
				case 'L':
					alg = 'L';
					break;
				case 'M':
					alg = 'M';
					break;
				case 'N':
					alg = 'N';
					break;
				case 'A':
					alg = 'A';
					break;
				case 'V':
					alg = 'V';
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

static void pairalign( char name[M][B], int nlen[M], char **seq, char **aseq, char **mseq1, char **mseq2, double *effarr, int alloclen )
{
	int i, j, ilim;
	int clus1, clus2;
	int off1, off2;
	float pscore;
	static char *indication1, *indication2;
	FILE *hat2p, *hat3p;
	static double **distancemtx;
	static double *effarr1 = NULL;
	static double *effarr2 = NULL;
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
			localhomtable[i][j].nokori = 0;
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


//	writePre( njob, name, nlen, aseq, 0 );

	for( i=0; i<njob; i++ ) for( j=0; j<njob; j++ ) pair[i][j] = 0;
	for( i=0; i<njob; i++ ) pair[i][i] = 1;

	ilim = njob - 1;
	for( i=0; i<ilim; i++ ) 
	{
		fprintf( stderr, "% 5d / %d\r", i, njob );
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
	
#if 1
			if( use_fft )
			{
				pscore = Falign( mseq1, mseq2, effarr1, effarr2, clus1, clus2, alloclen, &intdum );
				off1 = off2 = 0;
			}
			else
#endif
			{
				switch( alg )
				{
					case( 'a' ):
						pscore = Aalign( mseq1, mseq2, effarr1, effarr2, clus1, clus2, alloclen );
						off1 = off2 = 0;
						break;
					case( 'A' ):
						pscore = G__align11( mseq1, mseq2, alloclen );
						off1 = off2 = 0;
						break;
#if 1
					case( 'V' ):
						pscore = VAalign11( mseq1, mseq2, alloclen, &off1, &off2, localhomtable[i]+j );
						fprintf( stderr, "i,j = %d,%d, score = %f\n", i,j, pscore );
						break;
					case( 'S' ):
						fprintf( stderr, "aligning %d-%d\n", i, j );
						pscore = suboptalign11( mseq1, mseq2, alloclen, &off1, &off2, localhomtable[i]+j );
						fprintf( stderr, "i,j = %d,%d, score = %f\n", i,j, pscore );
						break;
#endif
					case( 'N' ):
						pscore = genL__align11( mseq1, mseq2, alloclen, &off1, &off2 );
//						fprintf( stderr, "pscore = %f\n", pscore );
						break;
					case( 'L' ):
						pscore = L__align11( mseq1, mseq2, alloclen, &off1, &off2 );
//						fprintf( stderr, "pscore = %f\n", pscore );
						break;
					case( 'M' ):
						pscore = MSalignmm( mseq1, mseq2, effarr1, effarr2, clus1, clus2, alloclen, NULL, NULL, NULL, NULL );
//						fprintf( stderr, "pscore = %f\n", pscore );
						break;
					default:
						ErrorExit( "ERROR IN SOURCE FILE" );
				}
			}
			distancemtx[i][j] = pscore;
#if SCOREOUT
			fprintf( stderr, "score = %10.2f (%d,%d)\n", pscore, i, j );
#endif
//			fprintf( stderr, "pslocal = %d\n", pslocal );
//			offset = makelocal( *mseq1, *mseq2, pslocal );
#if 0
			fprintf( stderr, "off1 = %d, off2 = %d\n", off1, off2 );
			fprintf( stderr, ">%d\n%s\n>%d\n%s\n>\n", i, mseq1[0], j, mseq2[0] );
#endif

//			putlocalhom2( mseq1[0], mseq2[0], localhomtable[i]+j, countamino( *mseq1, off1 ), countamino( *mseq2, off2 ), pscore, strlen( mseq1[0] ) );
//			fprintf( stderr, "pscore = %f\n", pscore );
			if( alg != 'S' && alg != 'V' )
				putlocalhom2( mseq1[0], mseq2[0], localhomtable[i]+j, off1, off2, (int)pscore, strlen( mseq1[0] ) );
		}
	}
	for( i=0; i<njob; i++ )
	{
		pscore = 0.0;
		for( pt=seq[i]; *pt; pt++ )
			pscore += amino_dis[(int)*pt][(int)*pt];
		distancemtx[i][i] = pscore;

	}

	ilim = njob-1;	
	for( i=0; i<ilim; i++ )
	{
		for( j=i+1; j<njob; j++ )
		{
			distancemtx[i][j] = ( 1.0 - distancemtx[i][j] / MIN( distancemtx[i][i], distancemtx[j][j] ) ) * 2.0;
		}
	}

	hat2p = fopen( hat2file, "w" );
	if( !hat2p ) ErrorExit( "Cannot open hat2." );
	WriteHat2( hat2p, njob, name, distancemtx );
	fclose( hat2p );

	fprintf( stderr, "##### writing hat3\n" );
	hat3p = fopen( "hat3", "w" );
	if( !hat3p ) ErrorExit( "Cannot open hat3." );
	ilim = njob-1;	
	for( i=0; i<ilim; i++ ) 
	{
		for( j=i+1; j<njob; j++ )
		{
			for( tmpptr=localhomtable[i]+j; tmpptr; tmpptr=tmpptr->next )
			{
				if( tmpptr->opt == -1.0 ) continue;
				fprintf( hat3p, "%d %d %d %7.5f %d %d %d %d %p\n", i, j, tmpptr->overlapaa, tmpptr->opt, tmpptr->start1, tmpptr->end1, tmpptr->start2, tmpptr->end2, tmpptr->next ); 
			}
		}
	}
	fclose( hat3p );
#if DEBUG
	fprintf( stderr, "calling FreeLocalHomTable\n" );
#endif
	FreeLocalHomTable( localhomtable, njob );
#if DEBUG
	fprintf( stderr, "done. FreeLocalHomTable\n" );
#endif
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
	static double *eff;
	int i;
	FILE *infp;
	char c;
	int alloclen;

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
	if( njob > M )
	{
		fprintf( stderr, "The number of sequences must be < %d\n", M );
		fprintf( stderr, "Please try the splittbfast program for such large data.\n" );
		exit( 1 );
	}

	seq = AllocateCharMtx( njob, nlenmax*9+1 );
	aseq = AllocateCharMtx( njob, nlenmax*9+1 );
	bseq = AllocateCharMtx( njob, nlenmax*9+1 );
	mseq1 = AllocateCharMtx( njob, 0 );
	mseq2 = AllocateCharMtx( njob, 0 );
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

//	writePre( njob, name, nlen, seq, 0 );

	for( i=0; i<njob; i++ ) eff[i] = 1.0;


	for( i=0; i<njob; i++ ) gappick0( bseq[i], seq[i] );

	pairalign( name, nlen, bseq, aseq, mseq1, mseq2, eff, alloclen );

	fprintf( trap_g, "done.\n" );
#if DEBUG
	fprintf( stderr, "closing trap_g\n" );
#endif
	fclose( trap_g );

//	writePre( njob, name, nlen, aseq, !contin );
#if 0
	writeData( stdout, njob, name, nlen, aseq );
#endif
#if IODEBUG
	fprintf( stderr, "OSHIMAI\n" );
#endif
	SHOWVERSION;
	return( 0 );
}
