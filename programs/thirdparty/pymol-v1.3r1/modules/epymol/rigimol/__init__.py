# rigimol.py

# Copyright (C) 2009 DeLano Scientific LLC.  All Rights Reserved.

from pymol import movie
from pymol import cmd
import os
import sys
import string
import traceback
import threading

_rigimol_exe = None

def quote_exe(exe):
    if ' ' in exe:
        if sys.platform == 'win32':
           exe = '"'+exe+'"'
    return exe

def validate():
    '''
    make sure that the FREEMOL environment variable is defined and
    that it contains a valid directory path
    
    returns 1 if valid, 0 if not
    '''
    ok = 0
    global _rigimol_exe
    if _rigimol_exe != None: # _rigimol_exe assigned, so presume valid
       ok = 1
    else:
       test_path = os.path.join(os.path.split(__file__)[0],"rigimol.exe")
       if os.path.exists(test_path) and os.path.isfile(test_path):
          _rigimol_exe = quote_exe(test_path)
          ok = 1
    return ok

def cat_stream(stream):
    try:
        while 1:
            line = stream.readline()
            if not line:
                break
            sys.stdout.write(line)
        stream.close()
    except:
        pass
    
def run(input):
    result = None
    global _rigimol_exe
    if _rigimol_exe == None:
        validate()
    if _rigimol_exe != None:
        try:
            rigimol_in, rigimol_out, rigimol_err = os.popen3(_rigimol_exe)
            rigimol_in.write(input)
            rigimol_in.close()
            thread = threading.Thread(target=cat_stream,args=(rigimol_err,))
            thread.setDaemon(1)
            thread.start()
            output = rigimol_out.read()
            rigimol_out.close()
            result = output
        except:
            print "Error: rigimol did not run"
            traceback.print_exc()
    else:
        print "Morph-Error: unable to locate rigimol"
    return result
    
def quote(st):
    if not len(st):
        st = '""'
    return st

def model_to_p2b(mdl):
    result = []
    result.append("+ NAME RESI RESN CHAIN SEGI        X        Y        Z     B   ")
    for atom in mdl.atom:
      coord = quote(atom.coord)
      name = quote(atom.name)
      resn = quote(atom.resn)
      resi = int(atom.resi)
      chain = quote(atom.chain)
      segi = quote(atom.segi)
      result.append("| %-4s %-4d %-4s %-5s %-4s %8.3f %8.3f %8.3f %5.2f"%
                    (name, resi, resn, chain, segi,
                     coord[0], coord[1], coord[2], atom.b))
    result.append('')
    result.append("+    FROM      TO")
    for bond in mdl.bond:
        result.append("| %7d %7d"%(bond.index[0],bond.index[1]))
    result.append('')
    return string.join(result,'\n')    

def run_morph(source,target,refinement,_self=cmd):
    cmd=_self
    job = []
    job.append("load\n");
    n_state = cmd.count_states(source)
    for state in range(n_state):
        job.append("p2b\ninline\n");
        job.append( model_to_p2b(cmd.get_model(source,state+1)))
        job.append("\nend\n")
    job.append("end\n")
    job.append("""
# determine connectivity 

reference

   # how much VDW overlap generally determines a bond
   bond_cutoff    = 0.4

   # how far out are our neighbors?
   neighbor_cutoff = 8.0

   # should we treat HIS, ASN, GLN as symmetric (1=yes, 0=no)
   coarse_symmetry = 1 

end

# generate the difference distance matrix

compare end

# now cluster (the settings rarely need to be changed).

analyze

   group_distance_cutoff     =    0.50  #  Distance (Angstroms)
   group_angle_cutoff        =   90.00  #  Angle (Degrees) 0-180
   group_shape_cutoff        =  100.00  #  Shape Ratio (25-500)

   cluster_distance_cutoff   =    1.75  #  Distance (Angstroms)
   cluster_angle_cutoff      =  180.00  #  Angle (Degrees) 0-180
   cluster_shape_cutoff      =  250.00  #  Shape Ratio (25-500)

   domain_similarity_cutoff  =    2.50  #  Ratio > 1.0
   domain_size_cutoff        =   10     #  Atom Count
   domain_shape_cutoff       =  500.00  #  Shape Ratio (25-500)

end

# write out the interpolation

write 

   interpolation
      steps = 30
      from 1 to 2
   end

end

# terminate RigiMOL
   
stop

""")
    input = string.join(job,'')
    result = run(input)
    if (result == None) or len(result) == 0:
        print "Morph-Error: no rigimol output received!"
        open("rigimol.inp",'wb').write(input)
        print "Saved 'rigimol.inp' for troubleshooting..."
        return
    cmd.create(target,source)
    print " Morph: Loading rough coordinates..."
    cmd.read_pdbstr(result,target,1)
    cmd.disable()
    cmd.enable(target)
    cmd.set("defer_builds_mode",1)
    if refinement>0:
       print " Morph: Refining morph (refinement level %d)..."%refinement
       refine(refinement,target)
    movie.sweep(10)
    cmd.mplay()
    print " Morph: Refinement complete."

def morph(source,target,first=0,last=-1,refinement=10,async=-1,quiet=1):
    source = str(source)
    target = str(target)
    refinement = int(refinement)
    async = int(async)
    quiet = int(quiet)
    if async<0: # by default, run asynch when interactive, sync when not
        async = not quiet
    if int(async):
        thread = threading.Thread(target=run_morph,args=(source,target,refinement))
        thread.setDaemon(1)
        thread.start()
    else:
        run_morph(source, target, refinement)

def refine(level,object_name,dec_factor=1.4,sculpt_ratio=4,sculpt_field_mask=2047,
           template_state=None, cutover_state=None,_self=cmd):
   start_cycles = int(level)
   pass_ = 1
   
   n_state = _self.count_states(object_name)
   if template_state == None:
       template_state = (1,n_state)
   if cutover_state == None:
      cutover_state = (n_state/2)+1
      
   window = (2*(n_state/30))+1
   if window < 3:
       window = 3

   _self.set("sculpting",0)
   _self.set("sculpt_field_mask",sculpt_field_mask)      
   _self.deprotect()
   _self.protect("flag 3")

   _self.set("sculpt_min_weight",2.25) # try to restore sanity
   _self.set("sculpt_max_weight",2.25) 
   
   _self.set("sculpt_bond_weight",2) 

   for prime in range(0,3):
       _self.set("sculpt_vdw_weight", 0.5 + 0.25*prime)           

       # try to relax the middle 20% to something physically reasonable
       # (eliminate major overlaps, clashes, etc).

       middle_start = (n_state * 4) / 10
       middle_stop = (n_state * 6) / 10 

       _self.sculpt_deactivate(object_name)
       _self.sculpt_purge()
       _self.frame(1)
       _self.sculpt_activate(object_name,match_state=n_state)
       for state in range(middle_start,cutover_state):
           _self.frame(state)
           print " Refine: relaxing state %d (pass %d of 3)"%(state,prime+1) 
           for i in range(level):
               _self.sculpt_iterate(object_name,state,level)
               _self.refresh()

       _self.sculpt_deactivate(object_name)
       _self.sculpt_purge()
       _self.frame(n_state)
       _self.sculpt_activate(object_name,match_state=1)
       for state in range(cutover_state,middle_stop+1):
           _self.frame(state)
           print " Refine: relaxing state %d (pass %d of 3)"%(state,prime+1)
           for i in range(level):
               _self.sculpt_iterate(object_name,state,level)
               _self.refresh()

       _self.smooth(object_name+" and not flag 3",10,window,middle_start-1,middle_stop+1)

   _self.set("sculpt_min_weight",2.25)
   _self.set("sculpt_max_weight",0.75)
   
   n_rep = 1
   x = start_cycles   
   while x>=0:
      y = n_rep
      while y>0:
         
         _self.set("sculpt_vdw_weight",0.45+(1.35*x)/start_cycles) # start with strong sterics, then relax
         _self.set("sculpt_bond_weight",2.25+(1.00*x)/start_cycles) # kill long bonds
         _self.set("sculpt_plan_weight",1.00+(2.00*x)/start_cycles) # insist on flat rings
         _self.set("sculpt_max_weight",0.75-float(x)/start_cycles) # increasingly allow breathing

         # try to force sidechains to fit backbone motion and not the reverse
         
         if x == start_cycles:
            _self.protect("(name ca+cb+c+n+o) and (q>3)")
         elif (x ==(start_cycles-1)) and (y == n_rep):
            _self.deprotect("not flag 3")
            _self.protect("(name ca+cb) and (q>5)")
         else:
            _self.deprotect("not flag 3")
            
         _self.sculpt_deactivate(object_name)
         _self.sculpt_purge()
         _self.frame(template_state[0])
         _self.sculpt_activate(object_name,match_state=n_state)

         for a in range(2,cutover_state):
            print " Refine: pass %d.%d on state %d."%(pass_,1+n_rep-y,a)
            _self.frame(a)
            _self.sculpt_iterate(object_name,a,sculpt_ratio*(x+1))
            _self.refresh()

         # switch over to second set of constraints

         _self.set("suspend_updates")
         _self.sculpt_deactivate(object_name)
         _self.sculpt_purge()
         _self.frame(template_state[1])
         _self.sculpt_activate(object_name,match_state=1)
         _self.frame(cutover_state)
         _self.unset("suspend_updates")

         for a in range(cutover_state,n_state):
            print " Refine: pass %d.%d on state %d."%(pass_,1+n_rep-y,a)
            _self.frame(a)
            _self.sculpt_iterate(object_name,a,sculpt_ratio*(x+1))
            _self.refresh()

         
         # do main smoothing pass
         _self.smooth(object_name+" and not flag 3",x/2+1,window,1,n_state)

         # smooth out distortion near the ends...
         while window>=3:
            _self.smooth(object_name+" and not flag 3",1,3,1,1+window)
            _self.smooth(object_name+" and not flag 3",1,3,n_state-window,n_state)
            window = window - 1
            
         y = y - 1

      n_rep = n_rep + 1
      x = x - int(((x-(x/dec_factor))+1))
      pass_ = pass_ + 1 
