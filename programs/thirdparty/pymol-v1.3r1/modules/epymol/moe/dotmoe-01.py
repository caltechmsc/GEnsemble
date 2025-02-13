import time
#
# dotmoe (.moe) file reader

import re,string

# regular expressions for parsing

_crlf_re = re.compile(r"\r\n|\r")
_filter_re = re.compile(r"[^#A-Za-z0-9+/\$%&~ \\()+\-*.,/:;=?![_\]{|}\^]")
_prefix_re = re.compile(r"[$%&~]")
_encode_re = re.compile(r"[A-Za-z0-9+/]")
_clean_int_re = re.compile(r"[^\-+0-9]")
_clean_hex_re = re.compile(r"[^0-9A-Fa-f]")
_escape_re = re.compile(r"([^$%&~]*)([$%&~][A-Za-z0-9+/\$%&~ \\()+\-*.,/:;=?![_\]{|}\^])(.*)")

# dictionaries for decoding .MOE encoding

_prefix_byte = { '$':0, '%':64, '&':128, '~':192 }
_encode_byte = { 'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H':7,
                 'I': 8, 'J': 9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14,
                 'P':15, 'Q':16, 'R':17, 'S':18, 'T':19, 'U':20, 'V':21,
                 'W':22, 'X':23, 'Y':24, 'Z':25, 'a':26, 'b':27, 'c':28,
                 'd':29, 'e':30, 'f':31, 'g':32, 'h':33, 'i':34, 'j':35,
                 'k':36, 'l':37, 'm':38, 'n':39, 'o':40, 'p':41, 'q':42,
                 'r':43, 's':44, 't':45, 'u':46, 'v':47, 'w':48, 'x':49,
                 'y':50, 'z':51, '0':52, '1':53, '2':54, '3':55, '4':56,
                 '5':57, '6':58, '7':59, '8':60, '9':61, '+':62, '/':63 }

_encode_keys = _encode_byte.keys()

def _decode_char(pat):
    if pat[1] in _encode_keys:
        return chr(_prefix_byte[pat[0]]+_encode_byte[pat[1]])
    else:
        return pat[0]
    
def _decode(inp):
    out = ''
    inp = _filter_re.sub('',inp)
    out = inp # TODO: decode pairs
    mo = _escape_re.search(inp)
    if mo == None:
        out = inp
    else:
        out = ''
        while mo!=None:
            list = mo.groups()
            out = out + list[0] + _decode_char(list[1])
            inp = list[2]
            mo = _escape_re.search(inp)
        out = out + inp
    if out=='$': return ''
    return out.replace("!"," ") 

def _decode_default(format,inp):
    if format=='i':
        return int(_clean_int_re.sub('',inp))
    if format=='r':
        return float(inp)
    if format in [ 'c', 't', 'tt', 'ss' ]:
        return _decode(inp)
    if format=='ix':
        return eval("0x"+_clean_hex_re.sub('',inp))        

class MOEReaderException(Exception):

    def __init__(self,value):
        self.value = value
    def __str__(self):
        return `self.value`
    
class MOEReader:
    
    def __init__(self):
        self.__dict__['next_r*'] = self.next_r_star
        self.__dict__['next_i*'] = self.next_i_star
        self.__dict__['next_**'] = self.next_star_star
        
    def next_word(self):
        if len(self.word):
            return self.word.pop() 
        else:
            try:
                if self.line[0][0:1]=='#':
                    return None
                while 1:
                    line = self.line.pop(0)
                    self.line_1st_ch.pop(0)
                    if len(line):
                        self.word = line.split()
                        if len(self.word):
                            self.word.reverse() # pop() faster than pop(0)
                            break
            except IndexError:
                return None
            return self.word.pop()

    def force_next_word(self):
        if len(self.word):
            return self.word.pop()
        else:
            try:
                while 1:
                    line = self.line.pop(0)
                    self.line_1st_ch.pop(0)
                    if len(line):
                        self.word = line.split()
                        if len(self.word):
                            self.word.reverse() # pop() faster than pop(0)
                            break
            except IndexError:
                return None
            return self.word.pop()

    def next_long(self):
        result = []
        count = self.next_i()
        while count>0:
            result.append(self.next_word())
            count = count - 1
        return string.join(result)

    def next_fields(self):
        fields = self.word
        fields.reverse()
        self.word = []
        return fields

    def next_columns(self):
        result = []
        fields = self.next_fields()
        inp_cnt = 0
        while 1:
            try:
                name = fields.pop(0)
            except IndexError:
                break
            format = fields.pop(0)
            try:
                dispatch = getattr(self,"next_"+format)
                inp_cnt = inp_cnt + 1
            except AttributeError:
                if '=' in format:
                    ix = format.find("=")
                    dispatch = lambda v=_decode_default(format[:ix],format[ix+1:]):v
                else:
                    raise MOEReaderException("unknown format:"+format)
            result.append((name,format,dispatch,inp_cnt))
        return result

    def next_ss(self):
        enc_str = self.next_word()
        if enc_str == None:
            raise MOEReaderException("bad 'ss'")
        return _decode(enc_str)

    def next_s(self):
        enc_str = self.next_word()
        if enc_str == None:
            raise MOEReaderException("bad 's'")
        elif enc_str == '~':
            enc_str = self.next_long()
        return _decode(enc_str)

    def next_tt(self):
        enc_str = self.next_word()
        if enc_str == None:
            raise MOEReaderException("bad 'tt'")
        return _decode(enc_str) 

    def next_c(self):
        enc_str = self.next_word()
        if enc_str == None:
            raise MOEReaderException("bad 'c'")
        return _decode(enc_str) 

    def next_t(self):
        enc_str = self.next_word()
        if enc_str == None:
            raise MOEReaderException("bad 't'")
        elif enc_str == '~':
            enc_str = self.next_long()
        return _decode(enc_str)
    
    def next_i(self):
        i_str = self.next_word()
        if i_str == None:
            raise MOEReaderException("bad 'i': [%s]"%i_str)
        else:
            return int(_clean_int_re.sub('',i_str))

    def fast_i_star(self,count):
        line_no = self.line_1st_ch.index('#')                            
        data = self.line[0:line_no]
        self.line = self.line[line_no:]
        self.line_1st_ch = self.line_1st_ch[line_no:]
        self.word.reverse()
        data = string.join(data,' ')
        split_list = re.split("([^0-9 \n])",data,maxsplit=1)
        if len(split_list)>1:
            data = split_list[0]
            new_word_list = string.join(split_list[1:],'').split()
            new_word_list.reverse()
        else:
            new_word_list = []
        queue = self.word + data.split()
        self.word = new_word_list
        return map(int, queue)

    def next_i_star(self):
        cnt = self.next_i()
        result = []
        if cnt>100:
            return self.fast_i_star(cnt)
        else:
            for a in xrange(cnt):
                result.append(self.next_i())
            return result

    def next_r(self):
        enc_str = self.next_word()
        if enc_str == None:
            raise MOEReaderException("bad 'r'")
        return float(enc_str)

    def fast_r_star(self,count):
        line_no = self.line_1st_ch.index('#')                            
        data = self.line[0:line_no]
        self.line = self.line[line_no:]
        self.line_1st_ch = self.line_1st_ch[line_no:]
        self.word.reverse()        
        data = string.join(data,' ')
        split_list = re.split("([^0-9.\- \n])",data,maxsplit=1)
        if len(split_list)>1:
            data = split_list[0]
            new_word_list = string.join(split_list[1:],'').split()
            new_word_list.reverse()
        else:
            new_word_list = []
        queue = self.word + data.split()
        self.word = new_word_list
        return map(float, queue)

    def next_r_star(self):
        cnt = self.next_i()
        result = []
        if cnt>100:
            return fast_r_star(cnt)
        else:
            for a in xrange(cnt):
                result.append(self.next_r())
            return result

    def next_star_star(self):
        cnt = self.next_i()
        result = []
        for a in xrange(cnt):
            format = "next_"+self.next_t()
            try:
                dispatch = getattr(self,format)
            except AttributeError:
                raise MOEReaderException("unknown format: "+format)
            result.append(apply(dispatch))
        return result
        
    def next_ix(self):
        hex_str = self.next_word()
        if hex_str == None:
            raise MOEReaderException("bad 'ix'")
        return eval("0x"+_clean_hex_re.sub('',hex_str))

    def next_paraTags(self,count):
        result = {}
        while count>0:
            count = count - 1
            tag = self.next_t()
            format = "next_"+self.next_t()
            try:
                dispatch = getattr(self,format)
            except AttributeError:
                raise MOEReaderException("unknown format: "+format)
            result[tag] = apply(dispatch)
        return result

    def next_paraTable_slow(self,count,columns):
        methods = map(lambda x:x[2],columns)
        return map(lambda x: map(apply, methods), xrange(count))
        
    def next_paraTable(self,count,columns):
        if (count>100) and len(columns):
            if (columns[0][3]==1) and (columns[-1][3]==1): # one and only one input in the table
                if columns[0][1]=='i': # simple table of ints (probably IDs)
                    uniform_part = map(apply,map(lambda x:x[2],columns)[1:])
                    variable_part = self.fast_i_star(count)
                    return map(lambda v,u=uniform_part:[v] + u, variable_part)
                
        # consolidate lines and divide words all at once
        if (count>100):
            line_no = self.line_1st_ch.index('#')                            
            data = self.line[0:line_no]
            self.line = self.line[line_no:]
            self.line_1st_ch = self.line_1st_ch[line_no:]
            queue = string.join(data,' ').split()
            queue.reverse()
            self.word = queue + self.word
        methods = map(lambda x:x[2],columns)
        return map(lambda x: map(apply, methods), xrange(count))

    def _txf_ixrrrrrr(self,value):  # isn't there something like a "group" operation in Python?
        self._txf_row.append(value)
        if self._txf_cnt.pop(0):
            row = self._txf_row
            self._txf_result.append([int(row[0],16)] + map(float,row[1:7]))
            self._txf_row = []
            self._txf_cnt = [0,0,0,0,0,0,1]

    def fast_ixrrrrrr(self,count):
        line_no = self.line_1st_ch.index('$')                    
        data = self.line[0:line_no]
        self.line = self.line[line_no:]
        self.line_1st_ch = self.line_1st_ch[line_no:]        
        queue = string.join(data,' ').split()
        self._txf_result = []
        self._txf_row = []
        self._txf_cnt = [0,0,0,0,0,0,1]
        map(self._txf_ixrrrrrr, queue)
        result = self._txf_result
        del self._txf_result
        return result

    def _txf_ii2(self,value):  # isn't there something like a "group" operation in Python?
        if self._txf_prior == None:
            self._txf_prior = value
        else:
            self._txf_result.append([int(self._txf_prior),int(value),2])
            self._txf_prior = None

    def fast_ii2(self,count):
        line_no = self.line_1st_ch.index('#')                    
        data = self.line[0:line_no]
        self.line = self.line[line_no:]
        self.line_1st_ch = self.line_1st_ch[line_no:]        
        queue = string.join(data,' ').split()
        self._txf_result = []
        self._txf_prior = None
        map(self._txf_ii2, queue)
        result = self._txf_result
        del self._txf_result
        return result

    def _txf_ii1(self,value):  # isn't there something like a "group" operation in Python?
        if self._txf_prior == None:
            self._txf_prior = value
        else:
            self._txf_result.append([int(self._txf_prior),int(value),1])
            self._txf_prior = None

    def fast_ii1(self,count):
        line_no = self.line_1st_ch.index('#')                    
        data = self.line[0:line_no]
        self.line = self.line[line_no:]
        self.line_1st_ch = self.line_1st_ch[line_no:]        
        queue = string.join(data,' ').split()
        self._txf_result = []
        self._txf_prior = None
        map(self._txf_ii1, queue)
        result = self._txf_result
        del self._txf_result
        return result

    def _txf_ii(self,value):  # isn't there something like a "group" operation in Python?
        if self._txf_prior == None:
            self._txf_prior = value
        else:
            self._txf_result.append([int(self._txf_prior),int(value)])
            self._txf_prior = None

    def fast_ii(self,count):
        line_no = self.line_1st_ch.index('#')                    
        data = self.line[0:line_no]
        self.line = self.line[line_no:]
        self.line_1st_ch = self.line_1st_ch[line_no:]        
        queue = string.join(data,' ').split()
        self._txf_result = []
        self._txf_prior = None
        map(self._txf_ii, queue)
        result = self._txf_result
        del self._txf_result
        return result

    def next_gvertex(self,count,columns):
        test_columns = map(lambda x:(x[1],x[3]),columns)
        if test_columns == [('ix',1),('r',2),('r',3),('r',4),
                            ('r',5),('r',6),('r',7)]:
            vrt = self.fast_ixrrrrrr(count)
        else:
            vrt = self.next_paraTable_slow(count,columns)
        self.force_next_word() # skip the '$'
        rec_cnt = self.next_i()
        fields = self.next_fields()
        if fields != [ 'tag', 't', 'value', '*' ]:
            raise MOEReaderException("unknown gvertex format")
        else:
            seg_idx = self.next_paraTags(rec_cnt)
        return (vrt,seg_idx)
    
    def _kw_moe(self):
        self.force_next_word()
        self.moe_version = self.force_next_word()
        
    def _kw_moe_colon_ph4que(self):
        self.force_next_word()
        self.moe_version = self.force_next_word()
        
    def _kw_pharmacophore(self):
        self.force_next_word()
        count = self.next_i()
        fields = self.next_fields()
        if fields != [ 'tag', 't', 'value', '*' ]:
            raise MOEReaderException("unknown pharmacophore format")
        self.cur_pharmacophore = self.next_paraTags(count)

    def _kw_endpharmacophore(self):
        self.force_next_word()

    def _kw_system(self):
        self.force_next_word()
        count = self.next_i()
        fields = self.next_fields()
        if fields != [ 'tag', 't', 'value', '*' ]:
            raise MOEReaderException("unknown system format")
        self.system = self.next_paraTags(count)

    def _kw_endsystem(self):
        self.force_next_word()

    def _kw_molecule(self):
        self.force_next_word()
        count = self.next_i()
        fields = self.next_fields()
        if fields != [ 'tag', 't', 'value', '*' ]:
            raise MOEReaderException("unknown molecule format")
        self.system['molecule'] = self.next_paraTags(count)

    def _kw_endmolecule(self):
        self.force_next_word()
        
    def _kw_bond(self):
        self.force_next_word()
        count = self.next_i()
        columns = self.next_columns()
        test_columns = map(lambda x:(x[1],x[3]),columns)
        if test_columns == [('i',1),('i',2)]:
            bond = self.fast_ii(count)
        elif test_columns == [('i', 1), ('i', 2), ('i=1', 2)]:
            bond = self.fast_ii1(count)        
        elif test_columns == [('i', 1), ('i', 2), ('i=2', 2)]:
            bond = self.fast_ii2(count)        
        else:
            bond = self.next_paraTable(count,columns)
        molecule = self.system['molecule']
        if not molecule.has_key('bond'):
            molecule['bond'] = []
        molecule['bond'].extend(bond)

    def _kw_attr(self):
        self.force_next_word()
        count = self.next_i()
        columns = self.next_columns()
#        print count,map(lambda x:(x[0],x[1],x[3]),columns)
        attr = self.next_paraTable(count,columns)
        molecule = self.system['molecule']        
        if not molecule.has_key('attr'):
            molecule['attr'] = []
        molecule['attr'].append( (columns,attr) )

    def _kw_gvertex(self):
        self.force_next_word()
        count = self.next_i()
        columns = self.next_columns()
        gvertex = self.next_gvertex(count,columns)
        graphics = self.system['graphics'][-1]
        if not graphics.has_key('gvertex'):
            graphics['gvertex'] = []
        graphics['gvertex'].append(gvertex)
        
    def _kw_gtext(self):
        self.force_next_word()
        count = self.next_i()
        columns = self.next_columns()
        gtext = self.next_paraTable(count,columns)
        graphics = self.system['graphics'][-1]
        if not graphics.has_key('gtext'):
            graphics['gtext'] = []
        graphics['gtext'].append(gtext)
        
    def _kw_graphics(self):
        self.force_next_word()
        count = self.next_i()
        fields = self.next_fields()
        if fields != [ 'tag', 't', 'value', '*' ]:
            raise MOEReaderException("unknown pharmacophore format")
        if not self.system.has_key('graphics'):
            self.system['graphics'] = []
        self.system['graphics'].append(self.next_paraTags(count))

        
    def _kw_meter(self):
        self.force_next_word()
        count = self.next_i()
        columns = self.next_columns()
        meter = self.next_paraTable(count,columns)
        columns = map(lambda x:x[0], columns)
        if not self.system.has_key('meter'):
            self.system['meter'] = []
        self.system['meter'].append( (columns,meter) )
        
    def _kw_feature(self):
        self.force_next_word()
        count = self.next_i()
        columns = self.next_columns()
        feature = self.next_paraTable(count,columns)
        columns = map(lambda x:x[0], columns)
        self.feature = (columns,feature)
        
    def appendFromStr(self,moe_st):
        if moe_st.find('\r'):
            moe_st = _crlf_re.sub('\n',moe_st)
        line = moe_st.split('\n')
        self.line = line
        self.line_1st_ch = map(lambda x:x[0:1],line)
        while 1:
            self.word = []
            try:
                line[0] = _filter_re.sub('',line[0])
            except IndexError:
                break
            cur_line = line[0]
            if not len(cur_line):
                line.pop(0)
                line_1st_ch.pop(0)
                continue
            if cur_line[0]!='#':
                line.pop(0)
                line_1st_ch.pop(0)
                continue
            keyword = "_kw_"+cur_line.split(' ',1)[0][1:]
            keyword = keyword.replace(':','_colon_')
            try:
                dispatch = getattr(self,keyword)
            except AttributeError:
                line.pop(0)
                line_1st_ch.pop(0)
                continue
#            start = time.time()
#            print keyword
            apply(dispatch)
#            print "done %8.3f"%(time.time()-start)
            # these may have changed, so reassign
            line = self.line 
            line_1st_ch = self.line_1st_ch
            
