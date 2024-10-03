import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

#TODO: Check for port_class at the top level. It might be a mode/submodule thing

class COFFE2VTR_NOC:
    def read_xml(xmlfile):
        tree = ET.parse(xmlfile)
        # tree.getroot().
        return tree

    def printPB(pb: dict):
        print('{')
        print('\tname: ' + str(pb['name']))
        print('\tarea: ' + str(pb['area']))
        print('\tcapacity' + str(pb['capacity']))
        print('\tinputs: ' + str(pb['inputs']))
        print('\toutptus: ' + str(pb['outputs']))
        print('\tclocks: ' + str(pb['clocks']))
        print('\tnumber of modes (shortened for readability): ' + str(len(pb['modes'])))
        print('\tnumber of pb_types (shortened for readability): ' + str(len(pb['pb_types'])))
        print('\tfc: ' + str(pb['fc']))
        print('\tpinlocations' + str(pb['pinlocations']))
        print('}')
    
    def extractComplexBlockInfo(archtree:ET, debug=False):
        root = archtree.getroot()
        complexblocks = root.find('complexblocklist')
        pbs = []
        for pb in complexblocks.findall('pb_type'):
            pbinfo = {
                'name': pb.attrib.get('name'),
                'capacity' : pb.attrib.get('capacity') if pb.attrib.get('capacity') is not None else '0',
                'area' : pb.attrib.get('area') if pb.attrib.get('area') is not None else '0',
                'inputs' : [],
                'outputs' : [],
                'clocks' : [],
                'modes' : [],
                'pb_types': [],
                'fc' : {},
                'pinlocations' : {}
            }
            debug = False
            if(debug):
                print(pbinfo)
            #get input port data
            pbinfo['inputs'] = COFFE2VTR_NOC.extractinputs(pb, debug=False)
            if(debug):
                print('\nAfter Inputs:')
                COFFE2VTR_NOC.printPB(pbinfo)
            #get output port data
            pbinfo['outputs'] = COFFE2VTR_NOC.extractoutputs(pb, debug=False)
            if(debug):
                print('\nAfter Outputs:')
                COFFE2VTR_NOC.printPB(pbinfo)
            #get clock data
            pbinfo['clocks'] = COFFE2VTR_NOC.extractclocks(pb, debug=False)
            if(debug):
                print('\nAfter Clocks:')
                COFFE2VTR_NOC.printPB(pbinfo)
            #get modes
            pbinfo['modes'] = COFFE2VTR_NOC.extractmodes(pb, debug=False)
            if(debug):
                print('\nAfter Modes:')
                COFFE2VTR_NOC.printPB(pbinfo)
            #get pbtypes
            pbinfo['pb_types'] = COFFE2VTR_NOC.extractpb(pb, debug=False)
            if(debug):
                print('\nAfter Pb_types:')
                COFFE2VTR_NOC.printPB(pbinfo)
            #get fc #assume there is only one fc element per pb
            pbinfo['fc'] = COFFE2VTR_NOC.extractfc(pb, debug=False)
            # debug = True
            if(debug):
                print('\nAfter fc:')
                COFFE2VTR_NOC.printPB(pbinfo)
            #get pinlocation data
            pbinfo['pinlocations'] = COFFE2VTR_NOC.extractpinlocations(pb, debug=False)
            # debug=True
            if(debug):
                print('\nAfter pinlocations:')
                COFFE2VTR_NOC.printPB(pbinfo)
            pbs.append(pbinfo)
        return pbs

    def extractinputs(pb, debug=False):
        inputs = []
        for input in pb.findall('input'):
            portdata = {
                'name' : input.attrib.get('name'),
                'num_pins' : input.attrib.get('num_pins'),
                'equivalent' : input.attrib.get('equivalent')
            }
            inputs.append(portdata)
        if(debug):
            print('\n inputs:')
            print(inputs)
        return inputs
    
    def extractoutputs(pb, debug=False):
        outputs = []
        for output in pb.findall('output'):
            portdata = {
                'name' : output.attrib.get('name'),
                'num_pins' : output.attrib.get('num_pins'),
                'equivalent' : output.attrib.get('equivalent')
            }
            outputs.append(portdata)
        if(debug):
            print('\n outputs:')
            print(outputs)
        return outputs

    def extractclocks(pb, debug=False):
        clocks = []
        for clock in pb.findall('clock'):
            data = {
                'name' : clock.attrib.get('name'),
                'num_pins' : clock.attrib.get('num_pins'),
                'equivalent' : clock.attrib.get('equivalent')
            }
            clocks.append(data)
        return clocks

    def extractmodes(pb, debug=False):
        modes = []
        for mode in pb.findall('mode'):
            data = ET.tostring(mode, encoding='unicode', method='xml')
            modes.append(data)
        if debug:
            print('\n modes:')
            print(modes)
        return modes
    
    def extractpb(pb, debug=False): #method to extract pb nested in the current pb. Saved as entire strings
        pbs = []
        for p in pb.findall('pb_type'):
            data = ET.tostring(p, encoding='unicode', method='xml')
            pbs.append(data)
        if(debug):
            print('\n pb_types:')
            print(pbs)
        return pbs

    def extractfc(pb, debug=False):
        fc = pb.find('fc')
        # print(ET.tostring(fc, encoding='unicode'))
        if fc is not None:
            data = {
                'default_in_type': fc.attrib.get('default_in_type'),
                'default_in_val' : float(fc.attrib.get('default_in_val')),
                'default_out_type' : fc.attrib.get('default_out_type'),
                'default_out_val' : float(fc.attrib.get('default_out_val'))
            }
            return data
        return None

    def extractpinlocations(pb, debug=False):
        pl = pb.find('pinlocations')
        data = {}
        if pl is not None:
            data['pattern'] = pl.attrib.get('pattern')
            data['locations'] = [] #locations is a list of dictionaries
            if data['pattern'] == 'custom':
                for loc in pl.findall('loc'):
                    locdata = {
                        'side' : loc.attrib.get('side'),
                        'pins' : loc.text.strip().split() #should return all the pins as a list
                    }
                    data['locations'].append(locdata)
            return data
        return None

    def addIndentAtBeginning(instring: str, indents: int) -> str:
        outstring = ''
        for i in range(0,indents):
            outstring += '\t'
        outstring = outstring + instring
        return outstring

                # 'name': pb and tile
                # 'capacity' : tile
                # 'area' : tile
                # 'inputs' : pb and tile
                # 'outputs' : pb and tile
                # 'clocks' : pb and tile
                # 'modes' : pb
                # 'pb_types': pb
                # 'fc' : tile
                # 'pinlocations' : tile
                # equivalent on both tile and pb

    def generateComplexBlockListStr(pb_list, debug=False):
        pb_types = ''
        for pb in pb_list:
            # COFFE2VTR_NOC.printPB(pb)
            pb_str = COFFE2VTR_NOC.generatePB_TypeStr(pb, debug=False)
            pb_types += '\n' + pb_str
        return pb_types
        
    def generatePB_TypeStr(pb:dict, debug=False) -> str:
        opennerstr = '\t\t<pb_type name="' + pb['name'] + '">'
        closerstr = '</pb_type>'
        inputstr = COFFE2VTR_NOC.generateInputPBStr(pb['inputs'], initial_indent=3)
        outputstr = COFFE2VTR_NOC.generateOutputPBStr(pb['outputs'], initial_indent=3)
        clockstr = COFFE2VTR_NOC.generateOutputPBStr(pb['clocks'], initial_indent=3)
        modestr = COFFE2VTR_NOC.generateModesStr(pb['modes'])
        pbsstr = COFFE2VTR_NOC.generateSubPBStr(pb['pb_types'])
        if debug:
            print('input str: ')
            print(inputstr)
            print('output str: ')
            print(outputstr)
            print('clock str: ')
            print(clockstr)
            print('mode str: ')
            print(modestr)
            print('nested pb_types str:')
            print(pbsstr)
        finalstr = opennerstr + inputstr + outputstr + clockstr + modestr + pbsstr + closerstr
        return finalstr

    def generateInputPBStr(inputs: list, initial_indent=2) -> str: #input is a list of dictionaries
        inputstrings = []
        indent = initial_indent
        i = 0
        for input in inputs:
            portstr = ''
            portstr += '<input name="'
            portstr += str(input['name'])
            portstr += '" num_pins="'
            portstr += str(input['num_pins'])
            if input['equivalent'] is not None:
                portstr += '" equivalent="'
                if str.lower(str(input['equivalent'])) == 'true': #convert true to full and false to none.
                    #assume true==full and false==none
                    portstr += 'full'
                else:
                    portstr += 'none'
                portstr += '"'
                portstr += '/>'
            else:
                portstr += '"/>'
            inputstrings.append(portstr)
        
        finalstring = ''
        for portstr in inputstrings:
            line = COFFE2VTR_NOC.addIndentAtBeginning(portstr, indent)
            finalstring += line
            finalstring += '\n'
        return finalstring

    def generateOutputPBStr(outputs: list, initial_indent=2) -> str:
        outputstrings = []
        indent = initial_indent
        i = 0
        for output in outputs:
            portstr = ''
            portstr += '<output name="'
            portstr += str(output['name'])
            portstr += '" num_pins="'
            portstr += str(output['num_pins'])
            if output['equivalent'] is not None:
                portstr += '" equivalent="'
                if str.lower(str(output['equivalent'])) == 'true': #convert true to full and false to none.
                    #assume true==full and false==none
                    portstr += 'full'
                else:
                    portstr += 'none'
                portstr += '"'
                portstr += '/>'
            else:
                portstr += '"/>'
            outputstrings.append(portstr)
        
        finalstring = ''
        for portstr in outputstrings:
            line = COFFE2VTR_NOC.addIndentAtBeginning(portstr, indent)
            finalstring += line
            finalstring += '\n'
        return finalstring
    
    def generateClockPBStr(clocks: list, initial_indent=2) -> str:
        clockstrings = []
        indent = initial_indent
        i = 0
        for clock in clocks:
            portstr = ''
            portstr += '<clock name="'
            portstr += str(clock['name'])
            portstr += '" num_pins="'
            portstr += str(clock['num_pins'])
            if clock['equivalent'] is not None:
                portstr += '" equivalent="'
                if str.lower(str(clock['equivalent'])) == 'true': #convert true to full and false to none.
                    #assume true==full and false==none
                    portstr += 'full'
                else:
                    portstr += 'none'
                portstr += '"'
                portstr += '/>'
            else:
                portstr += '"/>'
            clockstrings.append(portstr)
        
        finalstring = ''
        for portstr in clockstrings:
            line = COFFE2VTR_NOC.addIndentAtBeginning(portstr, indent)
            finalstring += line
            finalstring += '\n'
        return finalstring

    def generateModesStr(modes: list, initial_indent=2) -> str:
        modestr = ''
        for i in range(0,initial_indent):
            modestr += '\t'
        for mode in modes:
            modestr += mode
        return modestr

    def generateSubPBStr(pbs: list, initial_indent=2) -> str:
        pbstr = ''
        for i in range(0,initial_indent):
            pbstr+='\t'
        for pb in pbs:
            pbstr += pb
        return pbstr

    def formatXML(xml: str):
        dom = parseString(xml)
        outText =  dom.toprettyxml(indent="  ", newl='\n')
        lines = [line for line in outText.splitlines() if line.strip()]
        outText="\n".join(lines)
        return outText

    def generateTileSetStr(pb_list, debug=False) -> str:
        tileset = ''
        for pb in pb_list:
            tile_str = COFFE2VTR_NOC.generateTileStr(pb, debug=debug)
            tileset += '\n'
            tileset += tile_str
    
    #<tile>
    #   <subtile>
    #       <equivalent_sites> <site pb_type=something pin_mapping="direct"/>
    
    def generateTileStr(pb, debug=False):
        opennerstr = '\t\t<tile name="'
        opennerstr += pb['name']
        opennerstr += '"'
        if pb['area'] is not None:
            opennerstr += ' area="' + str(pb['area']) + '"'
        opennerstr == '>'
        
        closerstr = '\t\t</tile>'

if __name__=='__main__':
    print('starting')
    xml_file_path = 'generated_arch.xml'
    tree = COFFE2VTR_NOC.read_xml(xml_file_path)
    # tree.write('output.xml', encoding='unicode')

    pb_info = COFFE2VTR_NOC.extractComplexBlockInfo(tree, debug=True)
    complexBlockList = COFFE2VTR_NOC.generateComplexBlockListStr(pb_info, debug=True)
    tiles = COFFE2VTR_NOC
    
    with open('temp.xml', 'w+') as file:
        file.write(complexBlockList)