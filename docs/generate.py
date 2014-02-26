"""
A script for generating HTML docs from LEMS descriptions of the core NeuroML 2 Component Types
"""

from lems.model.model import Model

nml2_version = "beta2"
nml2_branch = "development"

colWidthLeft = "70"
colWidthRight = "100"

spacer2 = "&nbsp;&nbsp;"
spacer3 = "&nbsp;&nbsp;&nbsp;"
spacer4 = "&nbsp;&nbsp;&nbsp;&nbsp;"
spacer8 = spacer4+spacer4

greyStyle = " style=\"color:darkgrey\""
greySmallStyle = " style=\"color:darkgrey;font-size:12px\""
greyStyleDark = " style=\"color:dimgrey\""
greyStyleDarkItal = " style=\"color:dimgrey;font-style:italic\""
greyBlueStyle = " style=\"color:#85ACE1;font-style:italic\""
greySmallStyleDark = " style=\"color:dimgrey;font-size:12px\""

lemsXmlUrl = "https://github.com/NeuroML/NeuroML2/blob/%s/NeuroML2CoreTypes/"%nml2_branch
bioportalUrl = "http://bioportal.bioontology.org/ontologies/46856/?p=terms&conceptid=cno:"

nml_src = "../NeuroML2CoreTypes"

def category(name, rows=1, type="label-info"):
    return ("  <td width=\"%s\" rowspan='%i'>\n"+ \
           "    <span class=\"label %s\">%s</span>\n"+ \
           "  </td>\n")%(colWidthLeft, rows, type, name)

def exposedAs(name):
    if name is None:
        return ""
    return " (exposed as <b>"+name+"</b>)\n"

def dimension(name, pre="",post=""):
    if name is None or name == "none":
        return ""+pre+"Dimensionless"+post
    return ""+pre+"<a href=\"NeuroMLCoreDimensions.html#"+name+"\">"+name+"</a>"+post+""

def formatExpression(expr):
    expr2 = expr.replace(".gt.", "&gt;")
    expr2 = expr2.replace(".geq.", "&gt;=")
    expr2 = expr2.replace(".lt.", "&lt;")
    expr2 = expr2.replace(".leq.", "&lt;=")
    expr2 = expr2.replace(".and.", "AND")
    expr2 = expr2.replace(".eq.", "=")

    return expr2

def replaceUnderscoresAndUrls(text, useHtml=True):
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
                    word = pre+""+compTypeLink(ct)+""+post
                else:
                    word = pre+ct+post
            elif word[0]=='_':
                if useHtml:
                    word = "<b>%s</b>"%word[1:]
                else:
                    word = word[1:]

        text2 = text2+word+" "
    return text2

def formatDescription(element):
    if element.description is None:
        return ""
    desc = element.description
    desc2 = replaceUnderscoresAndUrls(desc, useHtml=True)
    return "<span %s><i>%s</i></span>"%(greyStyleDark, desc2)

def formatDescriptionSmall(element):
    if isinstance(element, str):
        desc = element
    elif element.description is None:
        return ""
    else:
        desc = element.description
    return "<br/>%s<span %s><i>%s</i></span>"%(spacer4,greySmallStyleDark, desc)


files = ["Cells", "Synapses", "Channels", "Inputs", "Networks", "PyNN", "NeuroMLCoreDimensions", "NeuroMLCoreCompTypes"]

compTypes = {}
compTypeSrc = {}
compTypeDesc = {}


for file in files:
    fullfile = "%s/%s.xml"%(nml_src,file)
    print "\n----------  Reading LEMS file: "+fullfile
    model = Model(include_includes=False)
    model.import_from_file(fullfile)
    
    for compType in model.component_types:
        compTypes[compType.name] = compType
        compTypeSrc[compType.name] = file
        compTypeDesc[compType.name] = compType.description if compType.description is not None else "ComponentType: "+compType.name

print("Read in all files")
print compTypeSrc


def compTypeLink(name):
    if name is None or name == "none" or not compTypeSrc.has_key(name):
        return "???"
    compName = name
    if name.startswith("base"): compName = "<span %s>%s</span>"% (greyBlueStyle, name)
    desc= replaceUnderscoresAndUrls(compTypeDesc[name], False)
    return "<a href=\"%s.html#%s\" title=\"%s\">%s</a>"%(compTypeSrc[name],name,desc,compName)

def getExtendedFromCompType(compTypeName):
    if not compTypes.has_key(compTypeName):
        return None
    extCompTypeName = compTypes[compTypeName].extends
    if extCompTypeName is None:
        return None
    return compTypes[extCompTypeName]

def addCompTypeAndRelated(compType,added, indent, pre, nameInfo=""):
    name = compType.name
    extenderPre = "<span %s><b>></b> </span>"%greyStyle
    childPre = "<span %s><b>+</b> </span>"%greyStyle
    childrenPre = "<span %s><b>++</b> </span>"%greyStyle

    contents = ""
    if name not in added or nameInfo!="":
        contents += indent+pre+nameInfo+compTypeLink(name)+"<br/>\n  \n"
        added.append(name)

        for ct in model.component_types:
            if ct.extends == name:
                contents += addCompTypeAndRelated(ct, added, indent+spacer3, extenderPre)
        '''
            for child in compType.getChild():
                if ct.name == child.type:
                    contents += addCompTypeAndRelated(ct, added, indent+spacer4, childPre)
            for children in compType.children:
                if ct.name == children.type:
                    contents += addCompTypeAndRelated(ct, added, indent+spacer4, childrenPre)'''
        '''
        for child in compType.getChild():
            nameInfo= "" if child.name == child.type else child.name+" "
            contents += addCompTypeAndRelated(compTypes[child.type], added, indent+spacer3, childPre, nameInfo=nameInfo)
        '''
        for children in compType.children:
            nameInfo= "" if children.name == children.type else children.name+" "
            contents += addCompTypeAndRelated(compTypes[children.type], added, indent+spacer3, childrenPre, nameInfo=nameInfo)

            '''contents += indent+indent+childPre+child.name+" "+compTypeLink(child.type)+"<br/>\n  \n"
            contents += addCompTypeAndRelated(ct, added, indent+spacer4, )'''
    '''else:
        contents += indent+pre+name+" ("+nameInfo+") already added...<br/>\n  \n"'''

    return contents

for file in files:
    fullfile = "%s/%s.xml"%(nml_src,file)
    print "\n----------  Reading LEMS file: "+fullfile

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
    for compType in model.component_types:
        contents += addCompTypeAndRelated(compType, added, "", "")

    contents += "    </div><!--/.well -->\n"+ \
                "    </div><!--/span-->\n"+ \
                "    <div class=\"span7\">\n"

    if model.description is not None:
        contents += ("   <div class=\"alert alert-error\">Note: these descriptions have been updated to the latest "
                     "   <a href=\"https://github.com/NeuroML/NeuroML2/tree/development/Schemas/NeuroML2\">NeuroML v2%s</a> definitions, using "
                     "   <a href=\"https://github.com/LEMS/LEMS/tree/master/Schemas/LEMS\">the latest version of LEMS</a>!</div>\n"+ \
                    "    <table class=\"table table-bordered\"><tr><td ><h3>%s</h3></td></tr>\n"+ \
                    "    <tr><td>%s</td></tr>\n"+ \
                    "    <tr><td>Original LEMS ComponentType definitions: <a href=\"%s%s.xml\">%s.xml</a><br/>"+ \
                    "    Schema against which NeuroML based on these should be valid: <a href=\"https://github.com/NeuroML/NeuroML2/tree/%s/Schemas/NeuroML2/NeuroML_v2%s.xsd\">NeuroML_v2%s.xsd</a></td></tr>\n"+ \
                    "    </table><br/>\n")%(nml2_version,file,formatDescription(lemscontents),lemsXmlUrl,file,file, nml2_branch, nml2_version, nml2_version)

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

            contents += spacer4+"Dimension: "+dimension(unit.dimension, "", "")+"<br/>"+spacer4+"Power of 10: "+str(unit.power)+offset+scale+"\n"

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





    for compType in model.component_types:
        #print "ComponentType %s is %s"%(compType.name, compType.description)

        ext = "" if compType.extends is None else "<p>%sextends %s</p>"%(spacer4,compTypeLink(compType.extends))
        #ext = "" if compType.extends is None else "%s<small>extends <a href=\"#%s\">%s</a></small>"%(spacer4,compType.extends,compType.extends)


        contents += "<a name=\""+compType.name+"\">&nbsp;</a>\n"
        contents += "<table class=\"table table-bordered\">\n"

        contents += "  <tr>\n"
        contents += "    <td colspan='3'>\n"
        classInfo = ""

        if compType.name.startswith("base"):
            contents += "       <b><span "+greyStyleDarkItal+">"+  compType.name+"</span></b>\n"
        else:
            contents += "       <b>"+  compType.name+"</b>\n"
        contents += ext
        contents += "    </td>\n"
        contents += "  </tr>\n"

        desc = "<i>--- no description yet ---</i>" if compType.description is None else formatDescription(compType)
        cnoLink = ""
        
        if " cno_00" in str(compType.description):
           cno = compType.description.split(" ")[-1]
           desc = desc.replace(cno, "")
           title = "Link to Bioportal entry for Computational Neuroscience Ontology related to: "+compType.name
           cnoLink = "<br/><br/><a class=\"btn\" title=\"%s\" href=\"%s%s\" target=\"CNO\">%s</a>"%(title,bioportalUrl,cno,cno)
        
        contents += "  <tr>\n"
        contents += "    <td colspan='3'>\n"
        contents += "      "+desc+cnoLink
        contents += "    </td>\n"
        contents += "  </tr>\n"


        params = {}
        texts = {}
        paths = {}
        exposures = {}
        requirements = {}
        eventPorts = {}

        for param in compType.parameters:
            params[param] = compType.name
        for text in compType.texts:
            texts[text] = compType.name
        for path in compType.paths:
            paths[path] = compType.paths
        for exp in compType.exposures:
            exposures[exp] = compType.name
        for req in compType.requirements:
            requirements[req] = compType.name
        for ep in compType.event_ports:
            eventPorts[ep] = compType.name

        extdCompType = getExtendedFromCompType(compType.name)

        while extdCompType is not None:
            for param in extdCompType.parameters:
                params[param] = extdCompType.name
            for text in extdCompType.texts:
                texts[text] = extdCompType.name
            for path in extdCompType.paths:
                paths[path] = extdCompType.paths
            for exp in extdCompType.exposures:
                exposures[exp] = extdCompType.name
            for req in extdCompType.requirements:
                requirements[req] = extdCompType.name
            for ep in extdCompType.event_ports:
                eventPorts[ep] = extdCompType.name
                
            extdCompType = getExtendedFromCompType(extdCompType.name)


        if len(params) > 0:
            contents += "  <tr>\n"
            contents += category("Parameters", len(params), type="label-success")
            keysort = sorted(params.keys(), key=lambda param: param.name)
            #print keysort
            for param in keysort:
                ct = params[param]
                origin = formatDescriptionSmall(param)
                style = ""
                if ct is not compType.name:
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+param.name+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(param.dimension)+"</td>\n  </tr>\n"
                
                
        if len(compType.derived_parameters) > 0:
            contents += "  <tr>\n"
            contents += category("Derived Parameters", len(compType.derived_parameters), type="label-success")
            for dp in compType.derived_parameters:
                origin = formatDescriptionSmall(dp.name)
                style = ""
                if ct is not compType.name:
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+dp.name+" = "+dp.value+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(dp.dimension)+"</td>\n  </tr>\n"


        if len(compType.texts) > 0: # TODO: Check if Text elements are inherited...
            contents += "  <tr>\n"
            contents += category("Text fields", len(compType.texts), type="label-success")
            for text in compType.texts:
                contents += "    <td colspan='2'><b>"+text.name+"</b></td>\n  </tr>\n"

        if len(compType.paths) > 0: # TODO: Check if Path elements are inherited...
            contents += "  <tr>\n"
            contents += category("Paths", len(compType.paths), type="label-success")
            for path in compType.paths:
                contents += "    <td colspan='2'><b>"+path.name+"</b></td>\n  </tr>\n"

        #TODO: check if ComponentRef are inherited...
        if len(compType.component_references) > 0:
            contents += "  <tr>\n"
            contents += category("Component References", len(compType.component_references), type="label-success")
            for cr in compType.component_references:
                contents += "    <td><b>"+cr.name+"</b></td>\n    <td width=\""+colWidthRight+"\">"+compTypeLink(cr.type)+"</td>\n  </tr>\n"

        '''
        #TODO: check if Childs are inherited...
        if len(compType.getChild()) > 0:
            contents += "  <tr>\n"
            contents += category("Child elements", len(compType.getChild()), type="label-success")
            for child in compType.getChild():
                contents += "    <td><b>"+child.name+"</b></td>\n    <td width=\""+colWidthRight+"\">"+compTypeLink(child.type)+"</td>\n  </tr>\n"
        '''
        #TODO: check if Childrens are inherited...
        if len(compType.children) > 0:
            contents += "  <tr>\n"
            contents += category("Children elements", len(compType.children), type="label-success")
            for children in compType.children:
                contents += "    <td><b>"+children.name+"</b></td>\n    <td width=\""+colWidthRight+"\">"+compTypeLink(children.type)+"</td>\n  </tr>\n"


        if len(compType.constants) > 0:
            contents += "  <tr>\n"
            contents += category("Constants", len(compType.constants))
            for const in compType.constants:
                contents += "    <td><b>"+const.name+"</b> = "+const.value+formatDescriptionSmall(const)+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(const.dimension)+"</td>\n  </tr>\n"

        if len(exposures) > 0:
            contents += "  <tr>\n"
            contents += category("Exposures", len(exposures))
            for exp in sorted(exposures, key=lambda entry: entry.name):
                ct = exposures[exp]
                origin = formatDescriptionSmall(exp)
                style = ""
                if ct is not compType.name:
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+exp.name+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(exp.dimension)+"</td>\n  </tr>\n"

        if len(requirements) > 0:
            contents += "  <tr>\n"
            contents += category("Requirements", len(requirements))
            for req in sorted(requirements, key=lambda entry: entry.name):
                ct = requirements[req]
                origin = formatDescriptionSmall(req)
                style = ""
                if ct is not compType.name:
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+req.name+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(req.dimension)+"</td>\n  </tr>\n"

        if len(eventPorts) > 0:
            contents += "  <tr>\n"
            contents += category("Event Ports", len(eventPorts))
            for ep in sorted(eventPorts, key=lambda entry: entry.name):
                ct = eventPorts[ep]
                origin = formatDescriptionSmall(ep)
                style = ""
                if ct is not compType.name:
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+ep.name+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">Direction: "+ep.direction+"</td>\n  </tr>\n"


        #TODO: check if Attachments are inherited...
        if len(compType.attachments) > 0:
            contents += "  <tr>\n"
            contents += category("Attachments", len(compType.attachments))
            for att in compType.attachments:
                contents += "    <td><b>"+att.name+"</b></td>\n    <td width=\""+colWidthRight+"\">"+compTypeLink(att.type)+"</td>\n  </tr>\n"



        if compType.dynamics:
                dynamics = compType.dynamics
                contents += "<tr>\n"
                contents += category("Dynamics", type="")
                contents += "<td colspan='2'>\n"

                structure = None
                if compType.structure is not None:
                    structure = compType.structure

                if structure is not None:
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
                        contents += spacer4+"<b>"+sv.name+"</b>"+spacer4+dimension(sv.dimension)+exposedAs(sv.exposure)+"<br/>\n"
                    if len(dynamics.state_variables) > 0: contents += "<br/>\n"


                '''
                if dynamics.on_start is not None:
                    contents += "<span class=\"label\">On Start</span><br/><br/>\n"
                    os = dynamics.on_start
                    for sa in os.state_assignments:
                        contents += spacer4+"<b>"+sa.variable+"</b> = "+sa.value+"<br/>\n"
                    contents += "<br/>\n"

                if len(dynamics.on_conditions) > 0:
                    contents += "<span class=\"label\">On Conditions</span><br/><br/>\n"
                    for oc in dynamics.on_conditions:
                        test = formatExpression(oc.test)
                        contents += spacer4+"IF "+test+" THEN<br/>\n"
                        for sa in oc.state_assignments:
                            contents += spacer4+spacer4+"<b>"+sa.variable+"</b> = "+sa.value+"<br/>\n"
                        for eo in oc.event_outs:
                            contents += spacer4+spacer4+"EVENT OUT on port <b>"+eo.port+"</b><br/>\n"
                        contents += "<br/>\n"


                if len(dynamics.on_events) > 0:
                    contents += "<span class=\"label\">On Events</span><br/><br/>\n"
                    for oe in dynamics.on_events:
                        contents += spacer4+"EVENT IN on port: <b>"+oe.port+"</b><br/>\n"
                        for sa in oe.state_assignments:
                            contents += spacer4+spacer4+"<b>"+sa.variable+"</b> = "+sa.value+"<br/>\n"
                        for eo in oe.event_outs:
                            contents += spacer4+spacer4+"EVENT OUT on port <b>"+eo.port+"</b><br/>\n"
                        contents += "<br/>\n"'''


                if len(dynamics.derived_variables) > 0:
                    contents += "<span class=\"label\">Derived Variables</span><br/><br/>\n"
                    for dv in dynamics.derived_variables:
                        res = dv.value
                        if res is None:
                            res = dv.select
                        contents += spacer4+"<b>"+dv.name+"</b> = "+res+spacer4+exposedAs(dv.exposure)+"<br/>\n"
                        ''' TODO:
                        if dv.getOnAbsent() is not None:
                            contents += spacer4+spacer4+spacer4+"IF "+dv.select+" IS ABSENT: <b>"+dv.name+"</b> = "+dv.getOnAbsent()+"<br/>\n"'''
                    if len(dynamics.derived_variables) > 0: contents += "<br/>\n"
                

                if len(dynamics.time_derivatives) > 0:
                    contents += "<span class=\"label\">Time Derivatives</span><br/><br/>\n"
                    for td in dynamics.time_derivatives:

                        contents += spacer4+"d <b>"+td.variable+"</b> /dt = "+td.value+"<br/>\n"
                    if len(dynamics.time_derivatives) > 0: contents += "<br/>\n"


                if len(dynamics.regimes) > 0:
                    for rg in dynamics.regimes:

                        initial = "" if rg.initial== None or rg.initial== "false" else " (initial)"
                        contents += "<span class=\"label\">Regime: "+rg.name+initial+"</span><br/><br/>\n"

                        '''
                        if rg.on_entry is not None:
                            contents += spacer8+"<span class=\"label\">On Entry</span><br/><br/>\n"
                            oe = rg.on_entry
                            for sa in oe.state_assignments:
                                contents += spacer8+spacer4+"<b>"+sa.variable+"</b> = "+sa.value+"<br/>\n"
                            contents += "<br/>\n"

                        if len(rg.on_conditions) > 0:
                            contents += spacer8+"<span class=\"label\">On Conditions</span><br/><br/>\n"
                            for oc in rg.on_conditions:
                                test = formatExpression(oc.test)
                                contents += spacer8+spacer4+"IF "+test+" THEN<br/>\n"
                                for sa in oc.state_assignments:
                                    contents += spacer8+spacer4+spacer4+"<b>"+sa.variable+"</b> = "+sa.value+"<br/>\n"
                                for eo in oc.event_outs:
                                    contents += spacer8+spacer4+spacer4+"EVENT OUT on port <b>"+eo.port+"</b><br/>\n"
                                if oc.getTransition() != None:
                                    contents += spacer8+spacer4+spacer4+"TRANSITION to REGIME <b>"+oc.getTransition().regimes+"</b><br/>\n"
                                contents += "<br/>\n"
                        '''
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

    doc.write(contents)
    doc.close()
