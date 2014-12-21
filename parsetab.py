
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'q\xf5X\xfc\x8b\xfa\xfdP\xca\xd7\xc4c\xe9Bv\x05'
    
_lr_action_items = {'WORD':([2,3,4,5,6,7,18,],[10,10,10,10,10,10,10,]),'SPACE':([10,],[18,]),'H2':([0,17,],[2,2,]),'H3':([0,17,],[3,3,]),'H1':([0,17,],[4,4,]),'H6':([0,17,],[5,5,]),'H4':([0,17,],[6,6,]),'H5':([0,17,],[7,7,]),'CR':([8,9,10,11,12,13,14,15,16,19,20,],[17,-2,-10,-5,-6,-4,-9,-7,-8,-3,-11,]),'$end':([1,8,9,10,11,12,13,14,15,16,19,20,],[0,-1,-2,-10,-5,-6,-4,-9,-7,-8,-3,-11,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'body':([0,],[1,]),'expression':([0,17,],[9,19,]),'statement':([0,],[8,]),'factor':([2,3,4,5,6,7,18,],[11,12,13,14,15,16,20,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> body","S'",1,None,None,None),
  ('body -> statement','body',1,'p_body','md2html.py',62),
  ('statement -> expression','statement',1,'p_state','md2html.py',66),
  ('statement -> statement CR expression','statement',3,'p_state','md2html.py',67),
  ('expression -> H1 factor','expression',2,'p_exp_cr','md2html.py',74),
  ('expression -> H2 factor','expression',2,'p_exp_cr','md2html.py',75),
  ('expression -> H3 factor','expression',2,'p_exp_cr','md2html.py',76),
  ('expression -> H4 factor','expression',2,'p_exp_cr','md2html.py',77),
  ('expression -> H5 factor','expression',2,'p_exp_cr','md2html.py',78),
  ('expression -> H6 factor','expression',2,'p_exp_cr','md2html.py',79),
  ('factor -> WORD','factor',1,'p_factor_text','md2html.py',92),
  ('factor -> WORD SPACE factor','factor',3,'p_factor_text','md2html.py',93),
]