#include "sc_Protein.hpp"
#include "scream_tools.hpp"
#include <iostream>
#include <string>
#include "Rotlib.hpp"
#include "Rotamer.hpp"
#include "AARotamer.hpp"
#include "sc_bgf_handler.hpp"

using namespace std;

class cmp_BGF_ptn_atom_ordering {
 public:
  bool operator()(SCREAM_ATOM* a1, SCREAM_ATOM* a2) {
    bool order = false;
    // Comparision order: 0 means a1 < a2, 1 means a2 > a1.
    // 1. chain name
    // " " (space) is < "A", but want A > " " (space).
    if (a1->chain == " " and a2->chain != " ") { order = false; return order; }  
    else if (a2->chain == " " and a1->chain != " ") { order = true; return order;}
    else if (a1->chain < a2->chain) { order = true; return order; }
    else if (a1->chain > a2->chain) { order = false; return order; }
    // below: cases where a1->chain == a2->chain
    // 2. res_pstn
    else if ( a1->resNum != a2->resNum) { order = (a1->resNum < a2->resNum) ? true : false ;}
    // if the two atoms have same resName
    else if ( scream_tools::strip_whitespace(a1->resName) == scream_tools::strip_whitespace(a2->resName) ) {
	// 3.1 if res_name defined (defined means one of the 20 natural AMINO acids)
      if (scream_tools::is_natural_AA(a1->resName)) {
	return scream_tools::AA_atom_order(a1, a2);
      }
      // 3.2 maintain current order if res_name not defined (meaning not being of of the 20 natural AMINO acids)
      else // i.e. not a natural 
	{
	  //a1->dump(); a2->dump();
	  return (a1->n < a2->n);  // maintain original ordering
	}
      
    }
    else {  // if the above rules don't decide anything, use what's already in place.
      return (a1->n < a2->n);
    }
    return order;
  }
};


int main(int argc, char *argv[]) {

   if (argv[1] == NULL) {
    cout << "Must provide bgf file!" << endl;
    cout << "Function: puts atoms in correct BIOGRAF standard ordering." << endl;
    cout << "Usage: " << argv[0] << " <bgf_file> <output_file_name>" << endl;
    cout << "E.g.: " << argv[0] << " temp.bgf ordered.bgf" << endl;
    exit(8);
   }
   
   if (argv[2] == NULL) {
     cout << "Must specify input AND output file names.  For usage, enter command without arguments." << endl;
   }

   string bgf_file = string(argv[1]);
   string output_file = string(argv[2]);


   bgf_handler BGF(bgf_file);
   sort(BGF.atom_list.begin(), BGF.atom_list.end(), cmp_BGF_ptn_atom_ordering());

   int c = 1;
   for (ScreamAtomVItr itr = BGF.atom_list.begin(); itr != BGF.atom_list.end(); itr++) {
     (*itr)->n = c;
     c++;
   }

   //Protein ptn(BGF.atom_list);

   //ptn.fix_entire_atom_list_ordering();
   
   ofstream OUTPUT(output_file.c_str());
   
   //BGF.printfile(ptn.getAtomList(), &OUTPUT);
   BGF.printfile(BGF.atom_list, &OUTPUT);

}
