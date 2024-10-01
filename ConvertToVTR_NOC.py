import xml.etree.ElementTree as ET
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
    
    def convertPB(archtree:ET, debug=False):
        root = archtree.getroot()
        complexblocks = root.find('complexblocklist')
        
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
                'num_pins' : clock.attrib.get('num_pins')
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

if __name__=='__main__':
    print('starting')
    xml_file_path = 'generated_arch.xml'
    tree = COFFE2VTR_NOC.read_xml(xml_file_path)
    # tree.write('output.xml', encoding='unicode')
    # with open('output.xml', 'r') as file:
    #     print(file.read())
    COFFE2VTR_NOC.convertPB(tree, debug=True)