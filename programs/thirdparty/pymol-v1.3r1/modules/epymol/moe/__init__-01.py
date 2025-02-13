# PyMOL epymol.moe module

from dotmoe import MOEReader, MOEReaderException
from chempy import Atom,Bond
from chempy.models import Indexed
from pymol import cmd
from chempy import cpv
import string
import math
import copy
import re

from pymol.cgo import *

_atom_prop_map = {
    'aName' : 'name',
    'aElement' : 'symbol',
    'aCharge' : 'partial_charge',
    'aTempFactor' : 'b',
    'aIon' : 'formal_charge',
    'aGeometry' : 'hybridization',
    }

_atom_coord_map = {
    'aPosX' : 0,
    'aPosY' : 1,
    'aPosZ' : 2
    }

_atom_label_map = {
    'aLabelElement' : None,
    'aLabelName' : None,
    'aLabelRes' : None
    }

_atom_vis_map = {
    'aBondLook' : None,
    'aNucleusLook' : None,
    'aHidden' : None,
    }
_atom_color_map = {
    'aRGB' : None,
    'aColorBy' : None,
    }

_residue_prop_map = {
    'rAtomCount' : None,
    'rColorBy' : None,
    'rName' : None,
    'rUID' : None,
    'rRGB' : None,
    'rINS' : None,
    'rType' : None,
    'rRibbonMode' : None,
    'rRibbonColorBy' : None,
    'rRibbonRGB' : None,
    }

_chain_prop_map = {
    'cResidueCount' : None,
    'cName' : None,
    'cRGB' : None,
    'cColorBy' : None,
}

_default_visible = 0x0880 # nonbonded and line

_ch_colors = [ 0xF31111, 0x54F311, 0x1141F3, 0xF311DB,
               0xF3FE3A, 0xF34611, 0x11F3F3, 0x5D0FD3,
               0xB2360C, 0x1E6806, 0x888d79 ]

def make_valid_name(name):
    name = string.strip(name)
    name = re.sub("[^ \.A-Za-z0-9_\-\+]",'_',name) # validate name
    name = re.sub("[ \.]",'_',name)
    name = re.sub("_+","_",name)
    return name

def read_moestr(moestr,name,state=0,finish=1,discrete=1,quiet=1,
                zoom=-1,_self=cmd):
    pymol=_self._pymol
    cmd=_self
    mr = MOEReader()
    mr.appendFromStr(moestr)
    split_chains = int(cmd.get_setting_legacy("moe_separate_chains"))
    cmd.group(name)
    if hasattr(mr,'system'):
        have_valences = 0
        chain_count = 0
        cmd.set_color("_aseg0",[1.0,1.0,1.0])
        aseg_color = cmd.get_color_index("_aseg0")
        aseg_flag = 0
        aseg_rep = {}
        model = Indexed()
        molecule = mr.system['molecule']
        if molecule.has_key('atoms'):
            n_atom = molecule['atoms']
            model.atom = map(lambda x:Atom(),xrange(n_atom))
        residues = {}
        chains = {}
        for columns,data in molecule['attr']:
            for row in data:
                cur_atom = None
                for key,value in map(None,columns,row):
                    key = key[0]
                    if key=='ID':
                        ID = value
                    else:
                        aProp = _atom_prop_map.get(key,None)
                        if aProp != None:
                            setattr(model.atom[ID-1],aProp,value)
                        else:
                            xyz = _atom_coord_map.get(key,None)
                            if xyz != None:
                                coord = list(model.atom[ID-1].coord)
                                coord[xyz] = value
                                model.atom[ID-1].coord = coord
                            elif _atom_vis_map.has_key(key):
                                atom = model.atom[ID-1]
                                if hasattr(atom,'visible'):
                                    visible = atom.visible
                                else:
                                    visible = _default_visible
                                if key=='aBondLook':
                                    if value=='cylinder':
                                        atom.visible = 0x00000001 | visible
                                    elif value=='line':
                                        atom.visible = 0x00000080 | visible
                                    elif value=='none': 
                                        atom.visible = -129 & Visible # 0xFFFFFF7F 
                                elif key=='aNucleusLook':
                                    if value=='sphere':
                                        atom.visible = 0x00000002 | visible
                                    elif value=='small-sphere': # need to set sphere_scale=0.2 for these atoms
                                        atom.visible = 0x00000002 | visible
                                        atom.sphere_scale = 0.2
                                    elif value=='point': # nonbonded
                                        atom.visible = 0x00000800 | visible
                                    elif value=='none':
                                        atom.visible = -2067 & visible # 0xFFFFF7ED 
                                elif key=='aHidden':
                                    atom.visible = 0
                                    atom.hidden = 1
                                if hasattr(atom,'hidden'): # be sure that hidden atoms aren't shown
                                    atom.visible = 0
                            elif _atom_color_map.has_key(key):
                                if key=='aRGB':
                                    model.atom[ID-1].trgb = value
                                elif key=='aColorBy':
                                    model.atom[ID-1].aColorBy = value
                            elif _atom_label_map.has_key(key):
                                atom = model.atom[ID-1]
                                if hasattr(atom,'label_dict'):
                                    atom.label_dict[key] = None
                                else:
                                    atom.label_dict = { key : None }
                            elif _residue_prop_map.has_key(key):
                                resi_dict = residues.get(ID,{})
                                resi_dict[key] = value
                                residues[ID] = resi_dict
                            elif _chain_prop_map.has_key(key):
                                chain_dict = chains.get(ID,{})
                                if not chains.has_key(ID):
                                    chain_count = chain_count + 1
                                    chain_dict['count'] = chain_count
                                chain_dict[key] = value
                                chains[ID] = chain_dict
        chn_keys = chains.keys()
        chn_keys.sort()
        res_keys = residues.keys()
        res_keys.sort()
        # map chain properties onto residues
        chn_resi = 0
        ch_colors = copy.deepcopy(_ch_colors)
        unique_chain_names = {}
        for chn_idx in chn_keys:
            chain_dict = chains[chn_idx]
            cName = make_valid_name(chain_dict.get('cName',''))
            segi = cName[0:4]
            chain = cName[-1:]
            if not len(cName):
                if chain_dict.has_key('count'):
                    cName = "chain_"+str(chain_dict['count'])
                else:
                    cName = str(chn_idx)
            if not unique_chain_names.has_key(cName):
                unique_chain_names[cName] = cName
            else:
                cnt = 2
                while unique_chain_names.has_key(cName+"_"+str(cnt)):
                    cnt = cnt + 1
                newCName = cName+"_"+str(cnt)
                unique_chain_names[newCName] = cName
                cName = newCName
            chain_dict['chain_color'] = ch_colors[0]
            ch_colors = ch_colors[1:] + [ch_colors[0]]
            cResCount = chain_dict.get('cResidueCount',0)
            for res_idx in range(chn_resi,chn_resi+cResCount):
                resi_dict = residues[res_keys[res_idx]]
                resi_dict['chain'] = chain
                resi_dict['segi'] = segi
                resi_dict['cName'] = cName
                resi_dict['chain_dict'] = chain_dict
            chn_resi = chn_resi + cResCount
        # map residue properties onto atoms
        res_atom = 0
        for res_idx in res_keys:
            resi_dict = residues[res_idx]
            rRibbonMode = resi_dict.get('rRibbonMode','none')
            rAtomCount = resi_dict['rAtomCount']
            rType = resi_dict.get('rType','')
            if rAtomCount>0:
                for at_idx in range(res_atom,res_atom+rAtomCount):
                    atom = model.atom[at_idx]
                    setattr(atom,'resi',
                            string.strip(str(resi_dict.get('rUID','')) +
                                         resi_dict.get('rINS','')))
                    setattr(atom,'resn',resi_dict.get('rName',''))
                    setattr(atom,'chain',resi_dict.get('chain',''))
                    setattr(atom,'segi',resi_dict.get('segi',''))
                    setattr(atom,'text_type',resi_dict.get('cName',''))
                    # add labels
                    if hasattr(atom,'label_dict'):
                        label = ''
                        label_dict = atom.label_dict
                        if label_dict.has_key('aLabelElement'):
                            label = atom.symbol
                        if label_dict.has_key('aLabelRes'):
                            if len(label):
                                label = label + ","
                            label = label + atom.resn + "_" + atom.resi
                        if label_dict.has_key('aLabelName'):
                            if len(label):
                                label = label + "."
                            label = label + atom.name
                        atom.label = label
                    if rType not in [ 'none', 'heme' ]:
                        atom.hetatm = 0 # all normal atoms
                    else:
                        atom.flags = 0x02000000 # hetatom or ligand -- ignore when surfacing

                    if rRibbonMode != 'none':
                        if hasattr(atom,'visible'):
                            visible = atom.visible
                        else:
                            visible = _default_visible

                        rRibbonColorBy = resi_dict['rRibbonColorBy']
                        repeat = 1
                        while repeat:
                            repeat = 0
                            if rRibbonColorBy in ['rgb','r:rgb']: # handled automatically
                                pass
                            elif rRibbonColorBy=='chain':
                                chain_dict = resi_dict['chain_dict']
                                cColorBy = chain_dict['cColorBy']
                                if cColorBy=='rgb':
                                    cColorBy = 'c:rgb'
                                rRibbonColorBy = cColorBy
                                repeat = 1

                        rRibbon_color = 0
                        rRibbon_trgb = 0xFFFFFF # default -- white

                        # now color ribbon
                        if rRibbonColorBy=='r:rgb':
                            rRibbon_trgb = resi_dict.get('rRGB',0xFFFFFF)
                        elif rRibbonColorBy=='rgb':
                            rRibbon_trgb = resi_dict.get('rRibbonRGB',0xFFFFFF)
                        elif rRibbonColorBy=='c:rgb':
                            chain_dict = resi_dict['chain_dict']
                            rRibbon_trgb = chain_dict.get('cRGB',0xFFFFFF)
                        elif rRibbonColorBy=='r:aseg':
                            rRibbon_trgb = None
                            rRibbon_color = aseg_color
                            aseg_flag = 1
                        elif rRibbonColorBy=='tempfactor':
                            pass # TO DO
                        elif rRibbonColorBy=='c:number': # per chain colors
                            rRibbon_trgb = chain_dict['chain_color']
                        if rRibbonMode in ['line', 'trace']: 
                            atom.visible = 0x00000040 | visible # PyMOL ribbon
                            if rRibbon_trgb != None:
                                atom.ribbon_trgb = rRibbon_trgb
                            else:
                                atom.ribbon_color = rRibbon_color
                            aseg_rep['ribbon'] = 1
                        else:
                            atom.visible = 0x00000020 | visible # PyMOL cartoon
                            if rRibbon_trgb != None:
                                atom.cartoon_trgb = rRibbon_trgb
                            else:
                                atom.cartoon_color = rRibbon_color
                            aseg_rep['cartoon'] = 1
                            
                    if hasattr(atom,'label'):
                        if hasattr(atom,'visible'):
                            visible = atom.visible
                        else:
                            visible = _default_visible
                        atom.visible = 0x00000028 | visible # labels
                    if not hasattr(atom,'aColorBy'):
                        atom.aColorBy = 'element'
                    if hasattr(atom,'aColorBy'):
                        aColorBy = atom.aColorBy
                        repeat = 1
                        while repeat:
                            repeat = 0
                            if aColorBy=='ribbon':                                
                                aColorBy = resi_dict.get('rRibbonColorBy')
                                if aColorBy=='rgb':
                                    aColorBy = 'rib:rgb'
                                else:
                                    repeat = 1
                                # TO DO still need to handle "cartoon_color", "ribbon_color"
                            elif aColorBy=='element': 
                                if hasattr(atom,'trgb'):
                                    del atom.trgb
                            elif aColorBy in ['rgb','a:rgb']: # handled automatically
                                pass
                            elif aColorBy=='residue':
                                rColorBy = resi_dict.get('rColorBy')
                                if rColorBy=='rgb':
                                    rColorBy = 'r:rgb'
                                aColorBy = rColorBy
                                repeat = 1
                            elif aColorBy=='chain':
                                chain_dict = resi_dict['chain_dict']
                                cColorBy = chain_dict['cColorBy']
                                if cColorBy=='rgb':
                                    cColorBy = 'c:rgb'
                                aColorBy = cColorBy
                                repeat = 1
                        
                        # now color atom...
                        if aColorBy=='r:rgb':
                            atom.trgb = resi_dict.get('rRGB',0xFFFFFF)
                        elif aColorBy=='rib:rgb':
                            atom.trgb = resi_dict.get('rRibbonRGB',0xFFFFFF)
                        elif aColorBy=='c:rgb':
                            chain_dict = resi_dict['chain_dict']
                            atom.trgb = chain_dict.get('cRGB',0xFFFFFF)
                        elif aColorBy=='r:aseg':
                            pass # TO DO
                        elif aColorBy=='tempfactor':
                            pass # TO DO
                        elif aColorBy=='c:number': # per chain colors
                            atom.trgb = chain_dict['chain_color']
                                
                res_atom = res_atom + rAtomCount
        bond_list = molecule.get('bond',[])
        for bond in bond_list:
            new_bond = Bond()
            new_bond.index = [bond[0]-1,bond[1]-1]
            if len(bond)>2:
                new_bond.order = bond[2]
                if bond[2]==2: # work around .MOE bug with triple bonds
                    if model.atom[new_bond.index[0]].hybridization == 'sp':
                      if model.atom[new_bond.index[1]].hybridization == 'sp':
                          new_bond.order = 3
                have_valences = 1
            model.bond.append(new_bond)
        if mr.system.has_key('ViewOrientationY'):
            vy = mr.system['ViewOrientationY']
            vz = mr.system['ViewOrientationZ']
            pos = mr.system['ViewLookAt']
            scale = mr.system['ViewScale']
            vx = cpv.cross_product(vy,vz)
            m = [ cpv.normalize(vx),
                  cpv.normalize(vy),
                  cpv.normalize(vz)]
            m = cpv.transpose(m)
            asp_rat = 0.8 # MOE default (versus 0.75 for PyMOL)
            cmd.set("field_of_view",25.0)
            fov = float(cmd.get("field_of_view"))
            window_height = scale*asp_rat;
            dist = (0.5*window_height)/math.atan(3.1415*(0.5*fov)/180.0)
            new_view = tuple( m[0] + m[1] + m[2] + [ 0.0, 0.0, -dist] + pos + [ dist*0.5,dist*1.5, 0.0 ])
            cmd.set_view(new_view)
            zoom=0
        cmd.unset("auto_color")
        cmd.set_color("carbon",[0.5,0.5,0.5]) # default MOE grey

        obj_name = name+".system"
        if split_chains<0: # by default, don't split chains if over 50 objects would be created
            if len(unique_chain_names.keys())>50:
                split_chains = 0
        if not split_chains:
            cmd.load_model(model,obj_name,state=state,
                           finish=finish,discrete=discrete,quiet=quiet,zoom=zoom)
            obj_name_list = [ obj_name ]
        else:
            cmd.load_model(model,obj_name,state=state,
                           finish=finish,discrete=discrete,quiet=1,zoom=zoom)
            obj_name_list = []
            system_name = obj_name
            for chain in unique_chain_names.keys():
                obj_name = name+"."+chain
                obj_name_list.append(obj_name)
                cmd.select("_moe_ext_tmp","text_type %s"%chain,domain=system_name)
                cmd.extract(obj_name,"_moe_ext_tmp",quiet=quiet,zoom=0)
                # cmd.extract(obj_name,system_name+" and text_type %s"%chain,quiet=quiet)
                cmd.delete("_moe_ext_tmp")
            if not cmd.count_atoms(system_name):
                cmd.delete(system_name)
            else:
                obj_name_list.append(system_name)
            cmd.order(name+".*",sort=1)
        for obj_name in obj_name_list:
            cmd.set("stick_radius",0.1,obj_name)
            cmd.set("line_width",2.0,obj_name)
            cmd.set("label_color","white",obj_name)
            cmd.set("cull_spheres",0,obj_name)
            cmd.set("nonbonded_size",0.05,obj_name) # temporary workaround...
            if have_valences: # if this MOE file has valences, then show em!
                cmd.set("valence",1,obj_name)
                cmd.set("stick_valence_scale",1.25,obj_name)
            if aseg_flag:
                cmd.dss(obj_name)
                if aseg_rep.has_key('cartoon'):
                    cmd.set("cartoon_color","red",obj_name+" and cartoon_color _aseg0 and ss h") 
                    cmd.set("cartoon_color","yellow",obj_name+" and cartoon_color _aseg0 and ss s")
                    cmd.set("cartoon_color","cyan",obj_name+" and cartoon_color _aseg0 and not ss h+s")
                if aseg_rep.has_key('ribbon'):
                    cmd.set("ribbon_color","red",obj_name+" and ribbon_color _aseg0 and ss h") # need selection op ribbon_color
                    cmd.set("ribbon_color","yellow",obj_name+" and ribbon_color _aseg0 and ss s")
                    cmd.set("ribbon_color","cyan",obj_name+" and ribbon_color _aseg0 and not ss h+s")
        if mr.system.has_key('ViewZFront'): 
            moe_front = mr.system['ViewZFront']
            moe_width = mr.system['ViewZWidth']
            extent = cmd.get_extent(name) # will this work with groups? TO DO: check!
            dx = (extent[0][0]-extent[1][0])
            dy = (extent[0][1]-extent[1][1])
            dz = (extent[0][2]-extent[1][2])
            half_width = 0.5*math.sqrt(dx*dx+dy*dy+dz*dz)
            cmd.clip("atoms",0.0,name)
            cur_view = cmd.get_view()
            center = (cur_view[-3]+cur_view[-2])*0.5 # center of clipping slab
            front = center - half_width
            back = center + half_width
            width = half_width * 2
            new_view = tuple(list(cur_view[0:15]) + [ front + width * moe_front,
                                          front + width * (moe_front + moe_width),
                                          0.0 ])
            cmd.set_view(new_view)
        if mr.system.has_key('graphics'):
            cgo_cnt = 1
            lab_cnt = 1
            unique_cgo_names = {}
            for graphics in mr.system['graphics']:
                cgo = []
                for gvertex in graphics.get('gvertex',[]):
                    vrt = gvertex[0]
                    seg_list = gvertex[1]['seg']
                    idx = gvertex[1]['idx']
                    len_idx = len(idx)
                    if not cmd.is_list(seg_list):
                        seg_list = [ seg_list ] * (len_idx / seg_list)
                    last_seg = None
                    ix_start = 0
                    for seg in seg_list:
                        if seg != last_seg:
                            if last_seg != None:
                                cgo.append(END)
                            if seg == 3:
                                cgo.extend([BEGIN, TRIANGLES])
                            elif seg == 2:
                                cgo.extend([BEGIN, LINES])
                            elif seg == 1:
                                cgo.extend([BEGIN, POINTS])
                        ix_stop = seg+ix_start
                        if seg==3:
                            for s in idx[ix_start:ix_stop]:
                                v = vrt[s-1]
                                cgo.extend([COLOR,
                                            (0xFF & (v[0]>>16))/255.0,
                                            (0xFF & (v[0]>>8))/255.0,
                                            (0xFF & (v[0]))/255.0])
                                if len(v)>4:
                                    cgo.extend([NORMAL,v[4],v[5],v[6]])
                                cgo.extend([VERTEX, v[1], v[2], v[3]])
                        elif seg==2:
                            for s in idx[ix_start:ix_stop]:
                                v = vrt[s-1]
                                cgo.extend([COLOR,
                                            (0xFF & (v[0]>>16))/255.0,
                                            (0xFF & (v[0]>>8))/255.0,
                                            (0xFF & (v[0]))/255.0])
                                if len(v)>4:
                                    cgo.extend([NORMAL,v[4],v[5],v[6]])
                                cgo.extend([VERTEX, v[1], v[2], v[3]])
                        elif seg==1:
                            for s in idx[ix_start:ix_stop]:
                                v = vrt[s-1]
                                cgo.extend([COLOR,
                                            (0xFF & (v[0]>>16))/255.0,
                                            (0xFF & (v[0]>>8))/255.0,
                                            (0xFF & (v[0]))/255.0])
                                if len(v)>4:
                                    cgo.extend([NORMAL,v[4],v[5],v[6]])
                                cgo.extend([VERTEX, v[1], v[2], v[3]])
                        ix_start = ix_stop
                        last_seg = seg
                    if last_seg != None:
                        cgo.append(END)
                for gtext in graphics.get('gtext',[]):
                    lab_name = name+".label_%02d"%lab_cnt
                    exists = 0
                    for entry in gtext:
                        exists = 1
                        cmd.pseudoatom(lab_name,pos=[float(entry[1]),
                                                   float(entry[2]),
                                                   float(entry[3])],
                                       color="0x%06x"%entry[0],label=entry[4])
                    if exists:
                        cmd.set('label_color',-1,lab_name)
                        lab_cnt = lab_cnt + 1
                    # TO DO -- via CGO's?

                if len(cgo):
                    cgo_name = name + "." + make_valid_name(graphics.get('GTitle','graphics'))
                    if not unique_cgo_names.has_key(cgo_name):
                        unique_cgo_names[cgo_name] = cgo_name
                    else:
                        cnt = 2
                        while unique_cgo_names.has_key(cgo_name+"_"+str(cnt)):
                            cnt = cnt + 1
                        new_name = cgo_name+"_"+str(cnt)
                        unique_cgo_names[new_name] = new_name
                        cgo_name = new_name
                    cmd.load_cgo(cgo,cgo_name,state=state,quiet=quiet,zoom=0)
                    cgo_cnt = cgo_cnt + 1
                    cmd.set("two_sided_lighting",1) # global setting...
                    cmd.set("cgo_line_width",2,cgo_name)
                    if graphics.has_key('GTransparency'):
                        g_trans = graphics['GTransparency']
                        if len(g_trans) >= 2:
                            if g_trans[0]!=0:
                                cmd.set('cgo_transparency','%1.6f'%(g_trans[0]/255.0),cgo_name)
                                cmd.set('transparency_global_sort');
        if mr.system.has_key('meter'):
            meter_name = name+".meter"
            exists = 0
            for meter_block in mr.system['meter']:
                if meter_block[0][0:2]==['type','atoms']:
                    for meter in meter_block[1]:
                        (type,atoms) = meter[0:2]
                        arg = tuple([meter_name]+map(lambda x,o=name:o+" and id "+str(x-1),atoms))
                        apply(getattr(cmd,type),arg)
                        exists = 1
            if exists:
                cmd.color("green",meter_name)
#            print mr.system['meter']
    elif hasattr(mr,'feature'):
        model = Indexed()
        cols = mr.feature[0]
        rows = mr.feature[1]
        col = {}
        cnt = 0
        for a in cols:
            col[a] = cnt
            cnt = cnt + 1
        for row in rows:
            atom = Atom()
            atom.coord = [ row[col['x']], row[col['y']], row[col['z']] ]
            atom.vdw = row[col['r']]
            atom.text_type = row[col['expr']]
            model.atom.append(atom)
        obj_name = name + ".feature"
        cmd.load_model(model,obj_name,state=state,
                       finish=finish,discrete=discrete,quiet=quiet,zoom=zoom)
        rank = 1
        for row in rows:
            cmd.color("0x%06x"%row[col['color']],obj_name+" & id %d"%(rank-1))
            rank = rank + 1
        cmd.show("mesh",obj_name)
        cmd.set("min_mesh_spacing",0.55,obj_name)
        cmd.label(obj_name,"' '+text_type")
        cmd.set("label_font_id",4,obj_name)
        cmd.set("label_color","yellow",obj_name)
    else:
        print dir(mr)
