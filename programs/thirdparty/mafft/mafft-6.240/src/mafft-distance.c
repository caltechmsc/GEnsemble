#include "mltaln.h"
#include "mtxutl.h"

#define DEBUG 0
#define TEST  0

#define END_OF_VEC -1

static int maxl;
static int tsize;

void arguments( int argc, char *argv[] )
{
	int c;

	inputfile = NULL;
	scoremtx = 1;
	nblosum = 62;
	dorp = NOTSPECIFIED;
	alg = 'X';

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
				case 'D':
					dorp = 'd';
					break;
				case 'P':
					dorp = 'p';
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
	if( inputfile == NULL )
	{
		argc--;
		inputfile = *argv;
		fprintf( stderr, "inputfile = %s\n", inputfile );
	}
    if( argc != 0 )
    {
        fprintf( stderr, "Usage: mafft-distance [-PD] [-i inputfile] inputfile > outputfile\n" );
        exit( 1 );
    }
}

void seq_grp_nuc( int *grp, char *seq )
{
	int tmp;
	while( *seq )
	{
		tmp = amino_grp[*seq++];
		if( tmp < 4 )
			*grp++ = tmp;
		else
			fprintf( stderr, "WARNING : Unknown character %c\r", *(seq-1) );
	}
	*grp = END_OF_VEC;
}

void seq_grp( int *grp, char *seq )
{
	int tmp;
	while( *seq )
	{
		tmp = amino_grp[*seq++];
		if( tmp < 6 )
			*grp++ = tmp;
		else
			fprintf( stderr, "WARNING : Unknown character %c\r", *(seq-1) );
	}
	*grp = END_OF_VEC;
}

void makecompositiontable_p( short *table, int *pointt )
{
	int point;

	while( ( point = *pointt++ ) != END_OF_VEC )
		table[point]++;
}

int commonsextet_p( short *table, int *pointt )
{
	int value = 0;
	short tmp;
	int point;
	static short *memo = NULL;
	static int *ct = NULL;
	static int *cp;

	if( !memo )
	{
		memo = (short *)calloc( tsize, sizeof( short ) );
		if( !memo ) ErrorExit( "Cannot allocate memo\n" );
		ct = (int *)calloc( MIN( maxl, tsize)+1, sizeof( int ) );
		if( !ct ) ErrorExit( "Cannot allocate memo\n" );
	}

	cp = ct;
	while( ( point = *pointt++ ) != END_OF_VEC )
	{
		tmp = memo[point]++;
		if( tmp < table[point] )
			value++;
		if( tmp == 0 ) *cp++ = point;
//		fprintf( stderr, "cp - ct = %d (tsize = %d)\n", cp - ct, tsize );
	}
	*cp = END_OF_VEC;
	
	cp =  ct;
	while( *cp != END_OF_VEC )
		memo[*cp++] = 0;

	return( value );
}

void makepointtable_nuc( int *pointt, int *n )
{
	int point;
	register int *p;

	p = n;
	point  = *n++ *  1024;
	point += *n++ *   256;
	point += *n++ *    64;
	point += *n++ *    16;
	point += *n++ *     4;
	point += *n++;
	*pointt++ = point;

	while( *n != END_OF_VEC )
	{
		point -= *p++ * 1024;
		point *= 4;
		point += *n++;
		*pointt++ = point;
	}
	*pointt = END_OF_VEC;
}

void makepointtable( int *pointt, int *n )
{
	int point;
	register int *p;

	p = n;
	point  = *n++ *  7776;
	point += *n++ *  1296;
	point += *n++ *   216;
	point += *n++ *    36;
	point += *n++ *     6;
	point += *n++;
	*pointt++ = point;

	while( *n != END_OF_VEC )
	{
		point -= *p++ * 7776;
		point *= 6;
		point += *n++;
		*pointt++ = point;
	}
	*pointt = END_OF_VEC;
}

int main( int argc, char **argv )
{
	int i, j;
	FILE *fp, *infp;
	char **seq;
	int *grpseq;
	char *tmpseq;
	int  **pointt;
	static char **name;
	static int *nlen;
	double *mtxself;
	double score, score0;
	static short *table1;
	char b[B];

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

#if 0
	PreRead( stdin, &njob, &nlenmax );
#else
	getnumlen( infp );
#endif
	rewind( infp );
	if( njob < 2 )
	{
		fprintf( stderr, "At least 2 sequences should be input!\n"
						 "Only %d sequence found.\n", njob );
		exit( 1 );
	}

	tmpseq = AllocateCharVec( nlenmax+1 );
	seq = AllocateCharMtx( njob, nlenmax+1 );
	grpseq = AllocateIntVec( nlenmax+1 );
	pointt = AllocateIntMtx( njob, nlenmax+1 );
	mtxself = AllocateDoubleVec( njob );
	pamN = NOTSPECIFIED;
	name = AllocateCharMtx( njob, B );
	nlen = AllocateIntVec( njob );

#if 0
	FRead( infp, name, nlen, seq );
#else
	readData_pointer( infp, name, nlen, seq );
#endif

	fclose( infp );

	constants( njob, seq );

	if( dorp == 'd' ) tsize = (int)pow( 4, 6 );
	else              tsize = (int)pow( 6, 6 );

	maxl = 0;
	for( i=0; i<njob; i++ ) 
	{
		gappick0( tmpseq, seq[i] );
		nlen[i] = strlen( tmpseq );
		if( nlen[i] < 6 )
		{
			fprintf( stderr, "Seq %d, too short, %d characters\n", i+1, nlen[i] );
			exit( 1 );
		}
		if( nlen[i] > maxl ) maxl = nlen[i];
		if( dorp == 'd' ) /* nuc */
		{
			seq_grp_nuc( grpseq, tmpseq );
			makepointtable_nuc( pointt[i], grpseq );
		}
		else                 /* amino */
		{
			seq_grp( grpseq, tmpseq );
			makepointtable( pointt[i], grpseq );
		}
	}
	fprintf( stderr, "\nCalculating i-i scores ... " );
	for( i=0; i<njob; i++ )
	{
		table1 = (short *)calloc( tsize, sizeof( short ) );
		if( !table1 ) ErrorExit( "Cannot allocate table1\n" );
		makecompositiontable_p( table1, pointt[i] );

		score = (double)commonsextet_p( table1, pointt[i] );
		mtxself[i] = score;
		free( table1 );
	}

	fprintf( stderr, "done.\n" );
	fprintf( stderr, "\nCalculating i-j scores ... \n" );
	for( i=0; i<njob; i++ )
	{
		table1 = (short *)calloc( tsize, sizeof( short ) );
		if( !table1 ) ErrorExit( "Cannot allocate table1\n" );
		if( i % 10 == 0 )
		{
			fprintf( stderr, "%#4d / %#4d\r", i+1, njob );
		}
		makecompositiontable_p( table1, pointt[i] );


        for( j=i; j<njob; j++ ) 
        {
            score = (double)commonsextet_p( table1, pointt[j] );
			fprintf( stdout, "%d-%d d=%4.2f l=%d,%d\n", i+1, j+1, ( 1.0 - score / MIN( mtxself[i], mtxself[j] ) ) * 3, nlen[i], nlen[j] );


		} 
		free( table1 );
	}
		
	fprintf( stderr, "\n" );
	SHOWVERSION;
	exit( 0 );
}
