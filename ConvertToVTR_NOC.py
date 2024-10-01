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
        print('\tmodes: ' + str(pb['modes']))
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
            pbinfo['inputs'] = COFFE2VTR_NOC.extractinputs(pb, debug=debug)
            if(debug):
                print('\nAfter Inputs:')
                COFFE2VTR_NOC.printPB(pbinfo)
            #get output port data
            pbinfo['outputs'] = COFFE2VTR_NOC.extractoutputs(pb, debug=debug)
            if(debug):
                print('\nAfter Outputs:')
                COFFE2VTR_NOC.printPB(pbinfo)
            #get clock data
            pbinfo['clocks'] = COFFE2VTR_NOC.extractclocks(pb, debug=debug)
            if(debug):
                print('\nAfter Clocks:')
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
        for mode in pb.findall('modes'):
            


if __name__=='__main__':
    print('starting')
    xml_file_path = 'vpr_arch.xml'
    tree = COFFE2VTR_NOC.read_xml(xml_file_path)
    # tree.write('output.xml', encoding='unicode')
    # with open('output.xml', 'r') as file:
    #     print(file.read())
    COFFE2VTR_NOC.convertPB(tree, debug=True)