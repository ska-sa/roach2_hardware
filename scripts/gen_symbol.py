#!/usr/bin/python

import string

in_file = '240-pin_ddr3_dimm.csv'
out_filename = 'symbol_gen.pas'

component_name = 'ddr3_dimm_240'
component_refdes = 'P?'
component_part = '*'
component_manufacturer = '*'
component_comment = '240-pin DDR3 DIMM '

def put_early_info(fid,component_name, part_count, refdes, comment):
  fid.write('  {.Generated from CSV info.}\n')
  fid.write('\n')
  fid.write('\n')
  fid.write('Procedure GenerateSymbol;\n')
  fid.write('Var\n')
  fid.write('  CurrentLib   : ISch_Lib;\n');
  fid.write('  SchComponent : ISch_Component;\n')
  fid.write('  Pin          : ISch_Pin;\n')
  fid.write('Begin\n')
  fid.write('  If SchServer = Nil Then Exit;\n')
  fid.write('  CurrentLib := SchServer.GetCurrentSchDocument;\n')
  fid.write('  If CurrentLib = Nil Then Exit;\n')
  fid.write('\n')
  fid.write('  // Check if the document is a Schematic Libary document first\n')
  fid.write('  If CurrentLib.ObjectID <> eSchLib Then\n')
  fid.write('  Begin\n')
  fid.write('     ShowError(\'Please open schematic library.\');\n')
  fid.write('     Exit;\n')
  fid.write('  End;\n')
  fid.write('\n')
  fid.write('  // Create a library component (a page of the library is created).\n')
  fid.write('  SchComponent := SchServer.SchObjectFactory(eSchComponent, eCreate_Default);\n')
  fid.write('  If SchComponent = Nil Then Exit;\n')
  fid.write('\n')
  fid.write('\n')
  fid.write('  // Set up parameters for the library component.\n')
  fid.write('  SchComponent.CurrentPartID := 1;\n')
  fid.write('  SchComponent.PartCount := %d;\n'%(part_count))
  fid.write('  SchComponent.DisplayMode   := 0;\n')
  fid.write('\n')
  fid.write('  // Define the LibReference and add the component to the library.\n')
  fid.write('  SchComponent.LibReference := \'%s\';\n'%(component_name))
  fid.write('  SchComponent.Designator.Text      := \'%s\';\n'%(refdes))
  fid.write('  SchComponent.ComponentDescription := \'%s\';\n'%(comment))


def put_late_info(fid):
  fid.write('  CurrentLib.AddSchComponent(SchComponent);\n')
  fid.write('  SchServer.RobotManager.SendMessage(nil, c_BroadCast, SCHM_PrimitiveRegistration, SCHComponent.I_ObjectAddress);\n')
  fid.write('  CurrentLib.CurrentSchComponent := SchComponent;\n')
  fid.write('  CurrentLib.GraphicallyInvalidate;\n')
  fid.write('End;\n')

  
 
def put_pin_info(fid, name, xpos, ypos, colour, orientation, loc, label, bank):
  fid.write('  %s := SchServer.SchObjectFactory(ePin, eCreate_Default);\n'%(name))
  fid.write('  If %s = Nil Then Exit;\n'%(name))
  fid.write('  %s.Location                := Point(MilsToCoord(%d), MilsToCoord(%d));\n'%(name, xpos, ypos))
  fid.write('  %s.PinLength               := %d;\n'%(name, 3000000))
  fid.write('  %s.Color                   := %d;\n'%(name, colour))
  fid.write('  %s.Orientation             := eRotate0;\n'%(name))
  fid.write('  %s.Designator              := \'%s\';\n'%(name, loc))
  fid.write('  %s.Name                    := \'%s\';\n'%(name, label))
  fid.write('  %s.OwnerPartId             := %d;\n'%(name, bank))
  fid.write('  %s.OwnerPartDisplayMode    := CurrentLib.CurrentSchComponent.DisplayMode;\n'%(name))
  fid.write('  SchComponent.AddSchObject(%s);\n'%(name))
  

in_data = open(in_file,'r').readlines()
in_pins = []
for i in in_data :
  in_pins.append(string.split(string.split(i, '\n')[0], ','))

bank_table = []
banked_pins = []
for pin in in_pins :
  new_bank = 1;
  for i in range(0,len(bank_table)) :
    if pin[1] == bank_table[i] :
      new_bank = 0 
      banked_pins[i].append(pin)

  if new_bank :
    bank_table.append(pin[1]);
    banked_pins.append([])
    banked_pins[len(bank_table)-1].append(pin)

f = open(out_filename, 'w')
put_early_info(f, component_name, len(bank_table), component_refdes, component_comment)
for i in range(0,len(banked_pins)):
  for j in range(0,len(banked_pins[i])) :
    put_pin_info(f, 'Pin', (j/80)*2000, (j%80)*100, 0, 0, banked_pins[i][j][0], banked_pins[i][j][2], i+1);

put_late_info(f);
f.close();
