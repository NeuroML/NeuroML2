"""
A script for generating HTML docs from LEMS descriptions of the core NeuroML 2 Component Types
"""

from lems.model.model import Model
from lems.model.dynamics import OnStart
from lems.model.dynamics import OnCondition
from lems.model.dynamics import OnEvent
from lems.model.dynamics import OnEntry
from lems.model.dynamics import Transition
from lems.model.dynamics import StateAssignment
from lems.model.dynamics import EventOut

nml2_version = "beta5"
nml2_branch = "master"

col_width_left = "70"
col_width_right = "100"

spacer2 = "&nbsp;&nbsp;"
spacer3 = "&nbsp;&nbsp;&nbsp;"
spacer4 = "&nbsp;&nbsp;&nbsp;&nbsp;"
spacer8 = spacer4+spacer4

grey_style = " style=\"color:darkgrey\""
grey_small_style = " style=\"color:darkgrey;font-size:12px\""
grey_style_dark = " style=\"color:dimgrey\""
grey_style_dark_ital = " style=\"color:dimgrey;font-style:italic\""
grey_blue_style = " style=\"color:#85ACE1;font-style:italic\""
grey_small_style_dark = " style=\"color:dimgrey;font-size:12px\""

lems_xml_url = "https://github.com/NeuroML/NeuroML2/blob/%s/NeuroML2CoreTypes/"%nml2_branch
bioportal_url = "http://bioportal.bioontology.org/ontologies/46856/?p=terms&conceptid=cno:"

nml_src = "../NeuroML2CoreTypes"

IF="IF"
THEN="THEN"

def category(name, rows=1, type="label-info"):
    return ("  <td width=\"%s\" rowspan='%i'>\n"+ \
           "    <span class=\"label %s\">%s</span>\n"+ \
           "  </td>\n")%(col_width_left, rows, type, name)

def exposed_as(name):
    if name is None:
        return ""
    return " (exposed as <b>"+name+"</b>)\n"

def dimension(name, pre="",post=""):
    if name is None or name == "none":
        return ""+pre+"Dimensionless"+post
    return ""+pre+"<a href=\"NeuroMLCoreDimensions.html#"+name+"\">"+name+"</a>"+post+""

def format_expression(expr):
    expr2 = expr.replace(".gt.", "&gt;")
    expr2 = expr2.replace(".geq.", "&gt;=")
    expr2 = expr2.replace(".lt.", "&lt;")
    expr2 = expr2.replace(".leq.", "&lt;=")
    expr2 = expr2.replace(".and.", "AND")
    expr2 = expr2.replace(".eq.", "=")
    expr2 = expr2.replace(".neq.", "!=")

    return expr2

def replace_underscores_and_urls(text, useHtml=True):
    words = text.split(" ")
    text2 = ""
    for word in words:
        if len(word)>0:
            if word.startswith("http://"):
                if useHtml:
                    word = "<a href=\"%s\">%s</a>"%(word, word)
            elif word.count('_')==2:
                pre = word[0:word.find('_')]
                ct = word[word.find('_')+1:word.rfind('_')]
                post = word[word.rfind('_')+1:]
                if useHtml:
                    word = pre+""+comp_type_link(ct)+""+post
                else:
                    word = pre+ct+post
            elif word[0]=='_':
                if useHtml:
                    word = "<b>%s</b>"%word[1:]
                else:
                    word = word[1:]

        text2 = text2+word+" "
    return text2

def format_description(element):
    if element is None or (not isinstance(element, str) and (element.description is None or len(element.description)==0)):
        return ""
    if isinstance(element, str):
        desc = element
    else:
        desc = element.description
    desc2 = replace_underscores_and_urls(desc, useHtml=True)
    return "<span %s><i>%s</i></span>"%(grey_style_dark, desc2)

def format_description_small(element):
    if isinstance(element, str):
        desc = element
    elif element.description is None:
        return ""
    else:
        desc = element.description
        
    if len(desc)==0:
        return ""
    return "<br/>%s<span %s><i>%s</i></span>"%(spacer4,grey_small_style_dark, desc)


files = ["Cells", "Synapses", "Channels", "Inputs", "Networks", "PyNN", "NeuroMLCoreDimensions", "NeuroMLCoreCompTypes"]

comp_types = {}
comp_type_src = {}
comp_type_desc = {}
ordered_comp_types = {}


for file in files:
    fullfile = "%s/%s.xml"%(nml_src,file)
    print("\n----------  Reading LEMS file: "+fullfile)
    model = Model(include_includes=False)
    model.import_from_file(fullfile)
    
    for comp_type in model.component_types:
        comp_types[comp_type.name] = comp_type
        comp_type_src[comp_type.name] = file
        comp_type_desc[comp_type.name] = comp_type.description if comp_type.description is not None else "ComponentType: "+comp_type.name
    ordered_comp_type_list = []
    with open(fullfile) as fp:
        for line in fp:
            s = '<ComponentType name='
            if s in line:
                i = line.index(s)
                e = line.find('"', i+len(s)+1)
                comp_type_defined = line[i+len(s)+1: e]
                ordered_comp_type_list.append(comp_type_defined)
    ordered_comp_types[file] = ordered_comp_type_list

print("Read in all files")


def comp_type_link(name):
    if name is None or name == "none" or not comp_type_src.has_key(name):
        return "???"
    compName = name
    if name.startswith("base"): compName = "<span %s>%s</span>"% (grey_blue_style, name)
    desc= replace_underscores_and_urls(comp_type_desc[name], False)
    return "<a href=\"%s.html#%s\" title=\"%s\">%s</a>"%(comp_type_src[name],name,desc,compName)

def get_extended_from_comp_type(comp_type_name):
    if not comp_types.has_key(comp_type_name):
        return None
    extCompTypeName = comp_types[comp_type_name].extends
    if extCompTypeName is None:
        return None
    return comp_types[extCompTypeName]

def add_comp_type_and_related(comp_type, added, indent, pre, nameInfo=""):
    name = comp_type.name
    extender_pre = "<span %s><b>></b> </span>"%grey_style
    child_pre = "<span %s><b>+</b> </span>"%grey_style
    children_pre = "<span %s><b>++</b> </span>"%grey_style

    contents = ""
    if name not in added or nameInfo!="":
        contents += indent+pre+nameInfo+comp_type_link(name)+"<br/>\n  \n"
        added.append(name)

        for ct in model.component_types:
            if ct.extends == name:
                contents += add_comp_type_and_related(ct, added, indent+spacer3, extender_pre)

        '''
        for child in comp_type.getChild():
            nameInfo= "" if child.name == child.type else child.name+" "
            contents += add_comp_type_and_related(comp_types[child.type], added, indent+spacer3, child_pre, nameInfo=nameInfo)
        '''
        for child_or_children in comp_type.children:
            nameInfo= "" if child_or_children.name == child_or_children.type else child_or_children.name+" "
            pre = children_pre if child_or_children.multiple else child_pre
            ctype = child_or_children.type
            ctype = ctype.replace('rdf:','rdf_')
            contents += add_comp_type_and_related(comp_types[ctype], added, indent+spacer3, pre, nameInfo=nameInfo)

    return contents

for file in files:
    fullfile = "%s/%s.xml"%(nml_src,file)
    print("\n----------  Reading LEMS file: "+fullfile)

    model = Model(include_includes=False)
    model.import_from_file(fullfile)

    #contents = HTMLgen.Simplecontentsument(title=file)
    doc = open("%s.html"%file, 'w')

    contents = ("<html>\n  <head>\n    <title>%s</title>\n"+ \
               "    <link href=\"assets/css/bootstrap.css\" rel=\"stylesheet\">\n"+ \
               "    <style type=\"text/css\"> td { font-size: 14; } </style>\n"+ \
               "    <!--<style type=\"text/css\"> body { padding-top: 90px; padding-bottom: 30px;  padding-left: 50px;  padding-right:50px; } </style>-->\n"+ \
               "  </head>\n<body>\n\n")%file


    contents += "<div class=\"navbar \">\n"+ \
                "  <div class=\"navbar-inner\">\n"+ \
                "    <div class=\"container\">\n"+ \
                "      <a class=\"btn btn-navbar\" data-toggle=\"collapse\" data-target=\".nav-collapse\">\n"+ \
                "        <span class=\"icon-bar\"></span>\n"+ \
                "        <span class=\"icon-bar\"></span>\n"+ \
                "        <span class=\"icon-bar\"></span>\n"+ \
                "      </a>\n"+ \
                "      <a class=\"brand\" href=\"#\">NeuroML v2%s Component Types</a>\n"%nml2_version+ \
                "      <div class=\"nav-collapse\">\n"+ \
                "        <ul class=\"nav\">\n"

    for file2 in files:
        active = " class=\"active\"" if file2==file else ""
        contents += "          <li"+active+"><a href=\""+file2+".html\">"+file2+"</a></li>\n"
            

    contents += "        </ul>\n"+ \
                "      </div><!--/.nav-collapse -->\n"+ \
                "    </div>\n"+ \
                "    </div>\n"+ \
                "    </div>\n"+ \
                "    <div class=\"container-fluid\">\n"+ \
                "    <div class=\"row-fluid\">\n"+ \
                "    <div class=\"span3\">\n"+ \
                "    <div class=\"well sidebar-nav\">\n"

    if len(model.dimensions) > 0:
        contents += "      <b>Dimensions</b><br/>\n"
        dimensions = model.dimensions
        dimensions = sorted(dimensions, key=lambda dim: dim.name)
        for dim in dimensions:
            contents += "      &nbsp;&nbsp"+dimension(dim.name)+"<br/>\n"
    if len(model.units) > 0:
        contents += "      <br/><b>Units</b><br/>\n"
        units = model.units
        units = sorted(units, key=lambda unit: unit.symbol)
        for unit in units:
            contents += "      &nbsp;&nbsp"+dimension(unit.symbol)+"<br/>\n"

    if len(model.component_types) > 0:
        contents += "      <b>Component Types</b><br/>\n"
    added = []
    
    
    for o_comp_type in ordered_comp_types[file]:
        o_comp_type = o_comp_type.replace('rdf:','rdf_')
        comp_type = model.component_types[o_comp_type]
        contents += add_comp_type_and_related(comp_type, added, "", "")

    contents += "    </div><!--/.well -->\n"+ \
                "    </div><!--/span-->\n"+ \
                "    <div class=\"span7\">\n"

    desc = "NeuroML2 ComponentType definitions from %s.xml"%file
    if model.description:
        desc = model.description
    contents += ("   <div class=\"alert alert-error\">For more information on NeuroML 2 and LEMS see <a href=\"http://www.neuroml.org/neuromlv2\">here</a>. <br/>Note: these descriptions have been updated to the latest "
                     "   <a href=\"https://github.com/NeuroML/NeuroML2/tree/%s/Schemas/NeuroML2\">NeuroML v2%s</a> definitions, using "
                     "   <a href=\"https://github.com/LEMS/LEMS/tree/master/Schemas/LEMS\">the latest version of LEMS</a>!</div>\n"+ \
                    "    <table class=\"table table-bordered\"><tr><td ><h3>%s</h3></td></tr>\n"+ \
                    "    <tr><td>%s</td></tr>\n"+ \
                    "    <tr><td>Original LEMS ComponentType definitions: <a href=\"%s%s.xml\">%s.xml</a><br/>"+ \
                    "    Schema against which NeuroML based on these should be valid: <a href=\"https://github.com/NeuroML/NeuroML2/tree/%s/Schemas/NeuroML2/NeuroML_v2%s.xsd\">NeuroML_v2%s.xsd</a></td></tr>\n"+ \
                    "    </table><br/>\n")%(nml2_branch,nml2_version,file,format_description(desc),lems_xml_url,file,file, nml2_branch, nml2_version, nml2_version)

    '''
    for inc in model.getInclude():
        contents += "<p>Included file: <a href=\"%s\">%s</a></p>\n"%(inc.getFile().replace(".xml", ".html"),inc.getFile())'''

    if "Dimensions" in file:

        dimensions = model.dimensions
        dimensions = sorted(dimensions, key=lambda dim: dim.name)
        for dim in dimensions:

            contents += "<a name=\""+dim.name+"\">&nbsp;</a>\n"
            contents += "<table class=\"table table-bordered\">\n"

            contents += "  <tr>\n"
            contents += "    <td>\n"
            contents += "       <b>"+dim.name+"</b>\n"
            contents += "    </td>\n"
            contents += "  </tr>\n"
            contents += "  <tr>\n"
            contents += "    <td>\n"

            contents2 = ""
            format = "%s<sup>%i</sup> "
            if dim.m is not None and dim.m != 0: contents += format%("M",dim.m)
            if dim.l is not None and dim.l != 0: contents += format%("L",dim.l)
            if dim.t is not None and dim.t != 0: contents += format%("T",dim.t)
            if dim.i is not None and dim.i != 0: contents += format%("I",dim.i)
            if dim.k is not None and dim.k != 0: contents += format%("K",dim.k)
            if dim.n is not None and dim.n != 0: contents += format%("N",dim.n)

            contents += "<br/>"
            
            for unit in units:
                if unit.dimension == dim.name:
                    contents += "<br/>"+spacer4+"Defined unit: <a href='#%s'>%s</a>"%(unit.symbol,unit.symbol)+"\n"
                    
            contents += "    </td>\n"
            contents += "  </tr>\n"
            contents += "</table>\n"
            
        units = model.units
        units = sorted(units, key=lambda unit: unit.symbol)
        for unit in units:


            contents += "<a name=\""+unit.symbol+"\">&nbsp;</a>\n"
            contents += "<table class=\"table table-bordered\">\n"

            contents += "  <tr>\n"
            contents += "    <td>\n"
            contents += "       <b>"+unit.symbol+"</b>\n"
            contents += "    </td>\n"
            contents += "  </tr>\n"
            contents += "  <tr>\n"
            contents += "    <td>\n"

            offset = ""
            if unit.offset is not None and unit.offset != 0:
                offset = "<br/>"+spacer4+"Offset: "+str(unit.offset)
                
            scale = ""
            if unit.scale is not None and unit.scale != 1:
                scale = "<br/>"+spacer4+"Scale: "+str(unit.scale)

            contents += spacer4+"Dimension: "+dimension(unit.dimension, "", "")+"<br/>"+spacer4+"Power of 10: "+str(unit.power)+offset+scale+"<br/>\n"

            for unit2 in model.units:
                if unit.symbol != unit2.symbol and unit.dimension == unit2.dimension:
                    '''diff = unit.power - unit2.power
                    factor = "10<sup>%i</sup>"%diff
                    if diff == 0:
                        factor = 1'''
                    factor1 = model.get_numeric_value("1%s"%unit.symbol, unit.dimension)
                    factor2 = model.get_numeric_value("1%s"%unit2.symbol, unit2.dimension)
                    contents += "<br/>"+spacer4+"1 %s = %s <a href='#%s'>%s</a>" % (unit.symbol, "%s"%(factor1/factor2), unit2.symbol, unit2.symbol)

            contents += "    </td>\n"
            contents += "  </tr>\n"
            contents += "</table>\n"





    for o_comp_type in ordered_comp_types[file]:
        o_comp_type = o_comp_type.replace('rdf:','rdf_')
        comp_type = model.component_types[o_comp_type]
        #print "ComponentType %s is %s"%(comp_type.name, comp_type.description)

        ext = "" if comp_type.extends is None else "<p>%sextends %s</p>"%(spacer4,comp_type_link(comp_type.extends))
        #ext = "" if comp_type.extends is None else "%s<small>extends <a href=\"#%s\">%s</a></small>"%(spacer4,comp_type.extends,comp_type.extends)


        contents += "<a name=\""+comp_type.name+"\">&nbsp;</a>\n"
        contents += "<table class=\"table table-bordered\">\n"

        contents += "  <tr>\n"
        contents += "    <td colspan='3'>\n"
        classInfo = ""

        if comp_type.name.startswith("base"):
            contents += "       <b><span "+grey_style_dark_ital+">"+  comp_type.name+"</span></b>\n"
        else:
            contents += "       <b>"+  comp_type.name+"</b>\n"
        contents += ext
        contents += "    </td>\n"
        contents += "  </tr>\n"

        desc = "<i>--- no description yet ---</i>" if comp_type.description is None else format_description(comp_type)
        cnoLink = ""
        
        if " cno_00" in str(comp_type.description):
           cno = comp_type.description.split(" ")[-1]
           desc = desc.replace(cno, "")
           title = "Link to Bioportal entry for Computational Neuroscience Ontology related to: "+comp_type.name
           cnoLink = "<br/><br/><a class=\"btn\" title=\"%s\" href=\"%s%s\" target=\"CNO\">%s</a>"%(title,bioportal_url,cno,cno)
        
        contents += "  <tr>\n"
        contents += "    <td colspan='3'>\n"
        contents += "      "+desc+cnoLink
        contents += "    </td>\n"
        contents += "  </tr>\n"


        params = {}
        derived_params = {}
        texts = {}
        paths = {}
        exposures = {}
        requirements = {}
        eventPorts = {}

        for param in comp_type.parameters:
            params[param] = comp_type.name
        for derived_param in comp_type.derived_parameters:
            derived_params[derived_param] = comp_type.name
        for text in comp_type.texts:
            texts[text] = comp_type.name
        for path in comp_type.paths:
            paths[path] = comp_type.paths
        for exp in comp_type.exposures:
            exposures[exp] = comp_type.name
        for req in comp_type.requirements:
            requirements[req] = comp_type.name
        for ep in comp_type.event_ports:
            eventPorts[ep] = comp_type.name

        extd_comp_type = get_extended_from_comp_type(comp_type.name)

        while extd_comp_type is not None:
            for param in extd_comp_type.parameters:
                params[param] = extd_comp_type.name
            for derived_param in extd_comp_type.derived_parameters:
                derived_params[derived_param] = extd_comp_type.name
            for text in extd_comp_type.texts:
                texts[text] = extd_comp_type.name
            for path in extd_comp_type.paths:
                paths[path] = extd_comp_type.paths
            for exp in extd_comp_type.exposures:
                exposures[exp] = extd_comp_type.name
            for req in extd_comp_type.requirements:
                requirements[req] = extd_comp_type.name
            for ep in extd_comp_type.event_ports:
                eventPorts[ep] = extd_comp_type.name
                
            extd_comp_type = get_extended_from_comp_type(extd_comp_type.name)


        if len(params) > 0:
            contents += "  <tr>\n"
            contents += category("Parameters", len(params), type="label-success")
            keysort = sorted(params.keys(), key=lambda param: param.name)
            #print keysort
            for param in keysort:
                ct = params[param]
                origin = format_description_small(param)
                style = ""
                if ct is not comp_type.name:
                    origin = spacer4+"(from "+comp_type_link(ct)+")"
                    style = grey_style
                contents += "    <td"+style+"><b>"+param.name+"</b>"+origin+"</td>\n    <td width=\""+col_width_right+"\">"+dimension(param.dimension)+"</td>\n  </tr>\n"
                
                
        if len(derived_params) > 0:
            contents += "  <tr>\n"
            contents += category("Derived Parameters", len(derived_params), type="label-success")
            keysort = sorted(derived_params.keys(), key=lambda derived_param: derived_param.name)
            for dp in keysort:
                ct = derived_params[dp]
                origin = ""
                style = ""
                if ct is not comp_type.name:
                    origin = spacer4+"(from "+comp_type_link(ct)+")"
                    style = grey_style
                contents += "    <td"+style+"><b>"+dp.name+" = "+dp.value+"</b>"+origin+"</td>\n    <td width=\""+col_width_right+"\">"+dimension(dp.dimension)+"</td>\n  </tr>\n"


        if len(comp_type.texts) > 0: # TODO: Check if Text elements are inherited...
            contents += "  <tr>\n"
            contents += category("Text fields", len(comp_type.texts), type="label-success")
            for text in comp_type.texts:
                contents += "    <td colspan='2'><b>"+text.name+"</b></td>\n  </tr>\n"

        if len(comp_type.paths) > 0: # TODO: Check if Path elements are inherited...
            contents += "  <tr>\n"
            contents += category("Paths", len(comp_type.paths), type="label-success")
            for path in comp_type.paths:
                contents += "    <td colspan='2'><b>"+path.name+"</b></td>\n  </tr>\n"

        #TODO: check if ComponentRef are inherited...
        if len(comp_type.component_references) > 0:
            contents += "  <tr>\n"
            contents += category("Component References", len(comp_type.component_references), type="label-success")
            for cr in comp_type.component_references:
                contents += "    <td><b>"+cr.name+"</b></td>\n    <td width=\""+col_width_right+"\">"+comp_type_link(cr.type)+"</td>\n  </tr>\n"

        #TODO: check if Childrens are inherited...
        if len(comp_type.children) > 0:
            contents += "  <tr>\n"
            child_contents = ""
            children_contents = ""
            child_count = 0
            children_count = 0
            #contents += category("Children elements", len(comp_type.children), type="label-success")
            for child_or_children in comp_type.children:
                if not child_or_children.multiple:
                    child_count+=1
                    child_contents += "    <td><b>"+child_or_children.name+"</b></td>\n    <td width=\""+col_width_right+"\">"+comp_type_link(child_or_children.type)+"</td>\n  </tr>\n"
                else:
                    children_count+=1
                    children_contents += "    <td><b>"+child_or_children.name+"</b></td>\n    <td width=\""+col_width_right+"\">"+comp_type_link(child_or_children.type)+"</td>\n  </tr>\n"
                
            if child_count>0:
                contents += category("Child elements", child_count, type="label-success")
                contents += child_contents
            if children_count>0:
                contents += category("Children elements", children_count, type="label-success")
                contents += children_contents


        if len(comp_type.constants) > 0:
            contents += "  <tr>\n"
            contents += category("Constants", len(comp_type.constants))
            for const in comp_type.constants:
                contents += "    <td><b>"+const.name+"</b> = "+const.value+format_description_small(const)+"</td>\n    <td width=\""+col_width_right+"\">"+dimension(const.dimension)+"</td>\n  </tr>\n"

        if len(exposures) > 0:
            contents += "  <tr>\n"
            contents += category("Exposures", len(exposures))
            for exp in sorted(exposures, key=lambda entry: entry.name):
                ct = exposures[exp]
                origin = format_description_small(exp)
                style = ""
                if ct is not comp_type.name:
                    origin = spacer4+"(from "+comp_type_link(ct)+")"
                    style = grey_style
                contents += "    <td"+style+"><b>"+exp.name+"</b>"+origin+"</td>\n    <td width=\""+col_width_right+"\">"+dimension(exp.dimension)+"</td>\n  </tr>\n"

        if len(requirements) > 0:
            contents += "  <tr>\n"
            contents += category("Requirements", len(requirements))
            for req in sorted(requirements, key=lambda entry: entry.name):
                ct = requirements[req]
                origin = format_description_small(req)
                style = ""
                if ct is not comp_type.name:
                    origin = spacer4+"(from "+comp_type_link(ct)+")"
                    style = grey_style
                contents += "    <td"+style+"><b>"+req.name+"</b>"+origin+"</td>\n    <td width=\""+col_width_right+"\">"+dimension(req.dimension)+"</td>\n  </tr>\n"

        if len(eventPorts) > 0:
            contents += "  <tr>\n"
            contents += category("Event Ports", len(eventPorts))
            for ep in sorted(eventPorts, key=lambda entry: entry.name):
                ct = eventPorts[ep]
                origin = format_description_small(ep)
                style = ""
                if ct is not comp_type.name:
                    origin = spacer4+"(from "+comp_type_link(ct)+")"
                    style = grey_style
                contents += "    <td"+style+"><b>"+ep.name+"</b>"+origin+"</td>\n    <td width=\""+col_width_right+"\">Direction: "+ep.direction+"</td>\n  </tr>\n"


        #TODO: check if Attachments are inherited...
        if len(comp_type.attachments) > 0:
            contents += "  <tr>\n"
            contents += category("Attachments", len(comp_type.attachments))
            for att in comp_type.attachments:
                contents += "    <td><b>"+att.name+"</b></td>\n    <td width=\""+col_width_right+"\">"+comp_type_link(att.type)+"</td>\n  </tr>\n"



        if comp_type.dynamics and comp_type.dynamics.has_content():
                dynamics = comp_type.dynamics
                contents += "<tr>\n"
                contents += category("Dynamics", type="")
                contents += "<td colspan='2'>\n"

                structure = None
                if comp_type.structure is not None:
                    structure = comp_type.structure

                if structure is not None and \
                    len(structure.withs)+len(structure.child_instances)+ \
                    len(structure.multi_instantiates)+len(structure.event_connections)>0:
                        
                    contents += "<span class=\"label\">Structure</span><br/><br/>\n"
                    for w in structure.withs:
                        contents += spacer4+"WITH <b>"+w.instance+"</b> AS <b>"+w.as_+"</b><br/>\n"
                    for ci in structure.child_instances:
                        contents += spacer4+"CHILD INSTANCE: <b>"+ci.component+"</b><br/>\n"
                    for mi in structure.multi_instantiates:
                        contents += spacer4+"INSTANTIATE <b>"+mi.number+"</b> COMPONENTS OF TYPE <b>"+mi.component+"</b><br/>\n"
                    for ec in structure.event_connections:
                        targetPort = "" if ec.target_port is None else ", TARGET PORT: <b>"+ec.target_port+"</b>"
                        receiver = "" if ec.receiver is None else ", RECEIVER: <b>"+ec.receiver+"</b>"
                        delay = "" if not hasattr(ec, 'delay') or ec.delay is None else ", DELAY: <b>"+ec.delay+"</b>"

                        contents += spacer4+"EVENT CONNECTION from <b>"+ec.from_+"</b> TO <b>"+ec.to+"</b>"+receiver+targetPort+delay+"<br/>\n"
                        if hasattr(ec, 'assign') and ec.assign is not None:
                            contents += spacer4+spacer4+"ASSIGN <b>"+ec.assign.property+"</b> = "+ec.assign.value+"<br/>\n"

                    contents += "<br/>\n"

                if len(dynamics.state_variables) > 0:
                    contents += "<span class=\"label\">State Variables</span><br/><br/>\n"
                    for sv in dynamics.state_variables:
                        contents += spacer4+"<b>"+sv.name+"</b>"+spacer4+dimension(sv.dimension)+exposed_as(sv.exposure)+"<br/>\n"
                    if len(dynamics.state_variables) > 0: contents += "<br/>\n"

                if dynamics.event_handlers is not None:
                    os_content = ""
                    oc_content = ""
                    oe_content = ""
                    for eh in dynamics.event_handlers:
                        if isinstance(eh, OnStart):
                            if len(os_content)==0: os_content += "<span class=\"label\">On Start</span><br/><br/>\n"
                            
                            os = eh
                            for ac in os.actions:
                                if isinstance(ac, StateAssignment):
                                    os_content += spacer4+"<b>"+ac.variable+"</b> = "+ac.value+"<br/>\n"
                            os_content += "<br/>\n"
                            
                        if isinstance(eh, OnCondition):
                            if len(oc_content)==0: oc_content += "<span class=\"label\">On Conditions</span><br/><br/>\n"
                            
                            oc = eh
                            test = format_expression(oc.test)
                            oc_content += spacer4+IF+" "+test+" "+THEN+"<br/>\n"
                            
                            for ac in oc.actions:
                                if isinstance(ac, StateAssignment):
                                    oc_content += spacer4+spacer4+"<b>"+ac.variable+"</b> = "+ac.value+"<br/>\n"
                                if isinstance(ac, EventOut):
                                    oc_content += spacer4+spacer4+"EVENT OUT on port <b>"+ac.port+"</b><br/>\n"
                            oc_content += "<br/>\n"
                            
                        if isinstance(eh, OnEvent):
                            if len(oe_content)==0: oe_content += "<span class=\"label\">On Events</span><br/><br/>\n"
                            
                            oe = eh
                            oe_content += spacer4+"EVENT IN on port: <b>"+oe.port+"</b><br/>\n"
                            
                            for ac in oe.actions:
                                if isinstance(ac, StateAssignment):
                                    oe_content += spacer4+spacer4+"<b>"+ac.variable+"</b> = "+ac.value+"<br/>\n"
                                if isinstance(ac, EventOut):
                                    oe_content += spacer4+spacer4+"EVENT OUT on port <b>"+ac.port+"</b><br/>\n"
                                
                            oe_content += "<br/>\n"
                            
                    contents += os_content
                    contents += oc_content
                    contents += oe_content


                if len(dynamics.derived_variables) > 0:
                    contents += "<span class=\"label\">Derived Variables</span><br/><br/>\n"
                    for dv in dynamics.derived_variables:
                        res = dv.value
                        if res is None:
                            res = str.replace(dv.select, '/', '->')
                            if dv.reduce:
                                res=res+" (reduce method: "+dv.reduce+")"
                        contents += spacer4+"<b>"+dv.name+"</b> = "+res+spacer4+exposed_as(dv.exposure)+"<br/>\n"
                    if len(dynamics.derived_variables) > 0: contents += "<br/>\n"

                if len(dynamics.conditional_derived_variables) > 0:
                    contents += "<span class=\"label\">Conditional Derived Variables</span><br/><br/>\n"
                    for cdv in dynamics.conditional_derived_variables:
                        for case in cdv.cases:
                            res = case.value
                            cond = IF+" "+format_expression(case.condition)+" "+THEN+"<br/>"+spacer4+spacer4 if case.condition else "OTHERWISE<br/>"+spacer4+spacer4
                            contents += spacer4+cond+"<b>"+cdv.name+"</b> = "+res+spacer4+exposed_as(cdv.exposure)+"<br/>\n"
                            
                        contents += "<br/>\n"
                        
                    if len(dynamics.conditional_derived_variables) > 0: contents += "<br/>\n"
                

                if len(dynamics.time_derivatives) > 0:
                    contents += "<span class=\"label\">Time Derivatives</span><br/><br/>\n"
                    for td in dynamics.time_derivatives:

                        contents += spacer4+"d <b>"+td.variable+"</b> /dt = "+td.value+"<br/>\n"
                    if len(dynamics.time_derivatives) > 0: contents += "<br/>\n"


                if len(dynamics.regimes) > 0:
                    for rg in dynamics.regimes:

                        initial = "" if rg.initial== None or rg.initial== "false" else " (initial)"
                        contents += "<span class=\"label\">Regime: "+rg.name+initial+"</span><br/><br/>\n"

                        oc_content = ""
                        for eh in rg.event_handlers:
                            if isinstance(eh, OnEntry):
                                contents += spacer8+"<span class=\"label\">On Entry</span><br/><br/>\n"
                                oe = eh
                                for ac in oe.actions:
                                    if isinstance(ac, StateAssignment):
                                        contents += spacer8+spacer4+"<b>"+ac.variable+"</b> = "+ac.value+"<br/>\n"
                                    
                                contents += "<br/>\n"
                                
                            if isinstance(eh, OnCondition):
                                if len(oc_content)==0: oc_content += spacer8+"<span class=\"label\">On Conditions</span><br/><br/>\n"

                                oc = eh
                                test = format_expression(oc.test)
                                oc_content += spacer8+spacer4+IF+" "+test+" "+THEN+"<br/>\n"

                                for ac in oc.actions:
                                    if isinstance(ac, StateAssignment):
                                        oc_content += spacer8+spacer4+spacer4+"<b>"+ac.variable+"</b> = "+ac.value+"<br/>\n"
                                    if isinstance(ac, EventOut):
                                        oc_content += spacer8+spacer4+spacer4+"EVENT OUT on port <b>"+ac.port+"</b><br/>\n"
                                    if isinstance(ac, Transition):
                                        oc_content += spacer8+spacer4+spacer4+"TRANSITION to REGIME <b>"+ac.regime+"</b><br/>\n"
                                oc_content += "<br/>\n"
                                
                        contents += oc_content
                            
                        if len(rg.time_derivatives) > 0:
                            contents += spacer8+ "<span class=\"label\">Time Derivatives</span><br/><br/>\n"
                            for td in rg.time_derivatives:

                                contents += spacer8+spacer4+"d <b>"+td.variable+"</b> /dt = "+td.value+"<br/>\n"
                            if len(rg.time_derivatives) > 0: contents += "<br/>\n"

                    if len(dynamics.regimes) > 0: contents += "<br/>\n"


                contents += "</td>\n"
                contents += "</tr>\n"

            
        contents += "</table>\n\n"

    contents += "</div>\n"
    contents += "</div>\n"
    contents += "</div>\n"
    contents += "</body>\n"
     
    for line in contents.split('\n'):
        #print("Writing: "+line)
        doc.write(line+'\n')
    doc.close()
