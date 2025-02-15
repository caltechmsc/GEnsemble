#!/usr/bin/env python
#
# program to align the hydrophobic center plane, defined by the
# C-alpha atoms of residues closest to the hydrophobic centers
# of helices, to the lipid bilayer middle defined as z=0
# Usage: align_HPCplane_to_Lipid.py proteinfile.bgf
#

import os,sys,math
#
bgffile = sys.argv[1]
bgfprefix = os.path.splitext(bgffile)[0]
print bgfprefix
hpcfile = sys.argv[2]
print hpcfile
pathname = os.path.dirname(sys.argv[0])
fullpath = os.path.abspath(pathname)
alignvmd = fullpath + "/align_hpc/align.vmd"
vmdpath = fullpath + "/../../thirdparty/vmd-1.8.6/bin/vmd"
#
#
dum1 = float(os.popen("grep HELIX1 %s | awk '{print $2}'" %hpcfile).read())
dum2 = float(os.popen("grep HELIX2 %s | awk '{print $2}'" %hpcfile).read())
dum3 = float(os.popen("grep HELIX3 %s | awk '{print $2}'" %hpcfile).read())
dum4 = float(os.popen("grep HELIX4 %s | awk '{print $2}'" %hpcfile).read())
dum5 = float(os.popen("grep HELIX5 %s | awk '{print $2}'" %hpcfile).read())
dum6 = float(os.popen("grep HELIX6 %s | awk '{print $2}'" %hpcfile).read())
dum7 = float(os.popen("grep HELIX7 %s | awk '{print $2}'" %hpcfile).read())
#
idca1=int(math.floor(dum1+0.5))
idca2=int(math.floor(dum2+0.5))
idca3=int(math.floor(dum3+0.5))
idca4=int(math.floor(dum4+0.5))
idca5=int(math.floor(dum5+0.5))
idca6=int(math.floor(dum6+0.5))
idca7=int(math.floor(dum7+0.5))
#
print dum1,idca1
print dum2,idca2
print dum3,idca3
print dum4,idca4
print dum5,idca5
print dum6,idca6
print dum7,idca7
#
bgffile = sys.argv[1]
##
# get x,y,z positions for Calpha atoms of hydrophobic centers for helices 1,4,6
##
x1 = float(os.popen("grep 'A  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $7 }'" %{"#": idca1, 'ffile': bgffile}).read())
y1 = float(os.popen("grep 'A  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $8 }'" %{"#": idca1, 'ffile': bgffile}).read())
z1 = float(os.popen("grep 'A  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $9 }'" %{"#": idca1, 'ffile': bgffile}).read())
print x1,y1,z1
#
x2 = float(os.popen("grep 'D  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $7 }'" %{"#": idca4, 'ffile': bgffile}).read())
y2 = float(os.popen("grep 'D  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $8 }'" %{"#": idca4, 'ffile': bgffile}).read())
z2 = float(os.popen("grep 'D  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $9 }'" %{"#": idca4, 'ffile': bgffile}).read())
print x2,y2,z2
#
x3 = float(os.popen("grep 'F  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $7 }'" %{"#": idca6, 'ffile': bgffile}).read())
y3 = float(os.popen("grep 'F  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $8 }'" %{"#": idca6, 'ffile': bgffile}).read())
z3 = float(os.popen("grep 'F  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $9 }'" %{"#": idca6, 'ffile': bgffile}).read())
print x3,y3,z3
##
a11 = -(z1*y2-z1*y3-y1*z2+y3*z2+z3*y1-z3*y2)/(x1*y2-x1*y3-x2*y1+x2*y3+x3*y1-x3*y2)
b11 = (x2*z1-x3*z1-z2*x1+z2*x3+z3*x1-z3*x2)/(x1*y2-x1*y3-x2*y1+x2*y3+x3*y1-x3*y2)
c11 = 1.0
d11 = -(z1*x2*y3-z1*x3*y2-z2*x1*y3+z2*x3*y1+z3*x1*y2-z3*x2*y1)/(x1*y2-x1*y3-x2*y1+x2*y3+x3*y1-x3*y2)
print a11,b11,c11,d11
##
##
# get x,y,z positions for Calpha atoms of hydrophobic centers for helices 2,5,7
##
x1 = float(os.popen("grep 'B  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $7 }'" %{"#": idca2, 'ffile': bgffile}).read())
y1 = float(os.popen("grep 'B  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $8 }'" %{"#": idca2, 'ffile': bgffile}).read())
z1 = float(os.popen("grep 'B  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $9 }'" %{"#": idca2, 'ffile': bgffile}).read())
print x1,y1,z1
#
x2 = float(os.popen("grep 'E  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $7 }'" %{"#": idca5, 'ffile': bgffile}).read())
y2 = float(os.popen("grep 'E  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $8 }'" %{"#": idca5, 'ffile': bgffile}).read())
z2 = float(os.popen("grep 'E  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $9 }'" %{"#": idca5, 'ffile': bgffile}).read())
print x2,y2,z2
#
x3 = float(os.popen("grep 'G  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $7 }'" %{"#": idca7, 'ffile': bgffile}).read())
y3 = float(os.popen("grep 'G  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $8 }'" %{"#": idca7, 'ffile': bgffile}).read())
z3 = float(os.popen("grep 'G  %(#)3d' %(ffile)s | grep ' CA ' | awk '{ print $9 }'" %{"#": idca7, 'ffile': bgffile}).read())
print x3,y3,z3
##
a12 = -(z1*y2-z1*y3-y1*z2+y3*z2+z3*y1-z3*y2)/(x1*y2-x1*y3-x2*y1+x2*y3+x3*y1-x3*y2)
b12 = (x2*z1-x3*z1-z2*x1+z2*x3+z3*x1-z3*x2)/(x1*y2-x1*y3-x2*y1+x2*y3+x3*y1-x3*y2)
c12 = 1.0
d12 = -(z1*x2*y3-z1*x3*y2-z2*x1*y3+z2*x3*y1+z3*x1*y2-z3*x2*y1)/(x1*y2-x1*y3-x2*y1+x2*y3+x3*y1-x3*y2)
print a12,b12,c12,d12
##
a1 = 0.5*(a11+a12)
b1 = 0.5*(b11+b12)
c1 = 0.5*(c11+c12)
d1 = 0.5*(d11+d12)
print a1,b1,c1,d1
os.system("sed -e 's/dummyD/%s/' %s | sed -e 's/dummyC/%s/' | sed -e 's/dummyB/%s/' | sed -e 's/dummyA/%s/' | sed -e 's/fileprefix/%s/' > my_align.vmd" %(d1,alignvmd,c1,b1,a1,bgfprefix) )
os.system("%s -dispdev text -e my_align.vmd" %(vmdpath))
##
os.system("sed -e 's/H_/HC/' %s-align.pdb > %s-align2.pdb" %(bgfprefix,bgfprefix))
os.system("mv %s-align2.pdb %s-align.pdb" %(bgfprefix,bgfprefix))
os.system("echo")
