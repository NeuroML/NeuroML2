"""
A helper class for generating HTML docs from LEMS descriptions of the core NeuroML Component Types
"""
import libneuroml.lems.util as lemsutil

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

nml_src = "../../../../../NeuroML2/NeuroML2CoreTypes"

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
    if element.getDescription() is None:
        return ""
    desc = element.getDescription()
    desc2 = replaceUnderscoresAndUrls(desc, useHtml=True)
    return "<span %s><i>%s</i></span>"%(greyStyleDark, desc2)

def formatDescriptionSmall(element):
    if element.getDescription() is None:
        return ""
    return "<br/>%s<span %s><i>%s</i></span>"%(spacer4,greySmallStyleDark, element.getDescription())


files = ["Cells", "Synapses", "Channels", "Inputs", "Networks", "PyNN", "NeuroMLCoreDimensions", "NeuroMLCoreCompTypes"]

compTypes = {}
compTypeSrc = {}
compTypeDesc = {}

for file in files:
    fullfile = "%s/%s.xml"%(nml_src,file)
    print "\n----------  Reading LEMS file: "+fullfile
    lemscontents = lemsutil.readLems(fullfile, incIncludes=False)
    for compType in lemscontents.getComponentType():
        compTypes[compType.getName()] = compType
        compTypeSrc[compType.getName()] = file
        compTypeDesc[compType.getName()] = compType.getDescription() if compType.getDescription() is not None else "ComponentType: "+compType.getName()

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
    extCompTypeName = compTypes[compTypeName].getExtends()
    if extCompTypeName is None:
        return None
    return compTypes[extCompTypeName]

def addCompTypeAndRelated(compType,added, indent, pre, nameInfo=""):
    name = compType.getName()
    extenderPre = "<span %s><b>></b> </span>"%greyStyle
    childPre = "<span %s><b>+</b> </span>"%greyStyle
    childrenPre = "<span %s><b>++</b> </span>"%greyStyle

    contents = ""
    if name not in added or nameInfo!="":
        contents += indent+pre+nameInfo+compTypeLink(name)+"<br/>\n  \n"
        added.append(name)

        for ct in lemscontents.getComponentType():
            if ct.getExtends() == name:
                contents += addCompTypeAndRelated(ct, added, indent+spacer3, extenderPre)
        '''
            for child in compType.getChild():
                if ct.getName() == child.getType():
                    contents += addCompTypeAndRelated(ct, added, indent+spacer4, childPre)
            for children in compType.getChildren():
                if ct.getName() == children.getType():
                    contents += addCompTypeAndRelated(ct, added, indent+spacer4, childrenPre)'''

        for child in compType.getChild():
            nameInfo= "" if child.getName() == child.getType() else child.getName()+" "
            contents += addCompTypeAndRelated(compTypes[child.getType()], added, indent+spacer3, childPre, nameInfo=nameInfo)

        for children in compType.getChildren():
            nameInfo= "" if children.getName() == children.getType() else children.getName()+" "
            contents += addCompTypeAndRelated(compTypes[children.getType()], added, indent+spacer3, childrenPre, nameInfo=nameInfo)

            '''contents += indent+indent+childPre+child.getName()+" "+compTypeLink(child.getType())+"<br/>\n  \n"
            contents += addCompTypeAndRelated(ct, added, indent+spacer4, )'''
    '''else:
        contents += indent+pre+name+" ("+nameInfo+") already added...<br/>\n  \n"'''

    return contents

for file in files:
    fullfile = "%s/%s.xml"%(nml_src,file)
    print "\n----------  Reading LEMS file: "+fullfile

    lemscontents = lemsutil.readLems(fullfile, incIncludes=False)

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

    if len(lemscontents.getDimension()) > 0:
        contents += "      <b>Dimensions</b><br/>\n"
    for dim in lemscontents.getDimension():
        contents += "      &nbsp;&nbsp"+dimension(dim.getName())+"<br/>\n"
    if len(lemscontents.getUnit()) > 0:
        contents += "      <br/><b>Units</b><br/>\n"
    for unit in lemscontents.getUnit():
        contents += "      &nbsp;&nbsp"+dimension(unit.getSymbol())+"<br/>\n"

    if len(lemscontents.getComponentType()) > 0:
        contents += "      <b>Component Types</b><br/>\n"
    added = []
    for compType in lemscontents.getComponentType():
        contents += addCompTypeAndRelated(compType, added, "", "")

    contents += "    </div><!--/.well -->\n"+ \
                "    </div><!--/span-->\n"+ \
                "    <div class=\"span7\">\n"

    if lemscontents.getDescription() is not None:
        contents += ("   <div class=\"alert alert-error\">Note: these descriptions have been updated to the latest "
                     "   <a href=\"https://github.com/NeuroML/NeuroML2/tree/development/Schemas/NeuroML2\">NeuroML v2%s</a> definitions, using "
                     "   <a href=\"https://github.com/LEMS/LEMS/tree/master/Schemas/LEMS\">the latest version of LEMS</a>!</div>\n"+ \
                    "    <table class=\"table table-bordered\"><tr><td ><h3>%s</h3></td></tr>\n"+ \
                    "    <tr><td>%s</td></tr>\n"+ \
                    "    <tr><td>Original LEMS ComponentType definitions: <a href=\"%s%s.xml\">%s.xml</a><br/>"+ \
                    "    Schema against which NeuroML based on these should be valid: <a href=\"https://github.com/NeuroML/NeuroML2/tree/%s/Schemas/NeuroML2/NeuroML_v2%s.xsd\">NeuroML_v2%s.xsd</a></td></tr>\n"+ \
                    "    </table><br/>\n")%(nml2_version,file,formatDescription(lemscontents),lemsXmlUrl,file,file, nml2_branch, nml2_version, nml2_version)

    '''
    for inc in lemscontents.getInclude():
        contents += "<p>Included file: <a href=\"%s\">%s</a></p>\n"%(inc.getFile().replace(".xml", ".html"),inc.getFile())'''

    if "Dimensions" in file:

        for dim in lemscontents.getDimension():

            contents += "<a name=\""+dim.getName()+"\">&nbsp;</a>\n"
            contents += "<table class=\"table table-bordered\">\n"

            contents += "  <tr>\n"
            contents += "    <td>\n"
            contents += "       <b>"+dim.getName()+"</b>\n"
            contents += "    </td>\n"
            contents += "  </tr>\n"
            contents += "  <tr>\n"
            contents += "    <td>\n"

            contents2 = ""
            format = "%s<sup>%i</sup> "
            if dim.getM() is not None and dim.getM() != 0: contents += format%("M",dim.getM())
            if dim.getL() is not None and dim.getL() != 0: contents += format%("L",dim.getL())
            if dim.getT() is not None and dim.getT() != 0: contents += format%("T",dim.getT())
            if dim.getI() is not None and dim.getI() != 0: contents += format%("I",dim.getI())
            if dim.getK() is not None and dim.getK() != 0: contents += format%("K",dim.getK())
            if dim.getN() is not None and dim.getN() != 0: contents += format%("N",dim.getN())

            contents += "    </td>\n"
            contents += "  </tr>\n"
            contents += "</table>\n"

        for unit in lemscontents.getUnit():


            contents += "<a name=\""+unit.getSymbol()+"\">&nbsp;</a>\n"
            contents += "<table class=\"table table-bordered\">\n"

            contents += "  <tr>\n"
            contents += "    <td>\n"
            contents += "       <b>"+unit.getSymbol()+"</b>\n"
            contents += "    </td>\n"
            contents += "  </tr>\n"
            contents += "  <tr>\n"
            contents += "    <td>\n"

            offset = ""
            if unit.getOffset() is not None and unit.getOffset() != 0:
                offset = "<br/>"+spacer4+"Offset: "+str(unit.getOffset())

            contents += spacer4+"Dimension: "+dimension(unit.getDimension(), "", "")+"<br/>"+spacer4+"Power of 10: "+str(unit.getPower())+offset+"\n"

            for unit2 in lemscontents.getUnit():
                if unit.getSymbol() != unit2.getSymbol() and unit.getDimension() == unit2.getDimension():
                    diff = unit.getPower() - unit2.getPower()
                    factor = "10<sup>%i</sup>"%diff
                    if diff == 0:
                        factor = 1
                    contents += "<br/>"+spacer4+"1 %s = %s <a href='#%s'>%s</a>" % (unit.getSymbol(), factor, unit2.getSymbol(), unit2.getSymbol())

            contents += "    </td>\n"
            contents += "  </tr>\n"
            contents += "</table>\n"





    for compType in lemscontents.getComponentType():
        print "ComponentType %s is %s"%(compType.getName(), compType.getDescription())

        ext = "" if compType.getExtends() is None else "<p>%sextends %s</p>"%(spacer4,compTypeLink(compType.getExtends()))
        #ext = "" if compType.getExtends() is None else "%s<small>extends <a href=\"#%s\">%s</a></small>"%(spacer4,compType.getExtends(),compType.getExtends())


        contents += "<a name=\""+compType.getName()+"\">&nbsp;</a>\n"
        contents += "<table class=\"table table-bordered\">\n"

        contents += "  <tr>\n"
        contents += "    <td colspan='3'>\n"
        classInfo = ""

        if compType.getName().startswith("base"):
            contents += "       <b><span "+greyStyleDarkItal+">"+  compType.getName()+"</span></b>\n"
        else:
            contents += "       <b>"+  compType.getName()+"</b>\n"
        contents += ext
        contents += "    </td>\n"
        contents += "  </tr>\n"

        desc = "<i>--- no description yet ---</i>" if compType.getDescription() is None else formatDescription(compType)
        cnoLink = ""
        
        if " cno_00" in str(compType.getDescription()):
           cno = compType.getDescription().split(" ")[-1]
           desc = desc.replace(cno, "")
           title = "Link to Bioportal entry for Computational Neuroscience Ontology related to: "+compType.getName()
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

        for param in compType.getParameter():
            params[param] = compType.getName()
        for text in compType.getText():
            texts[text] = compType.getName()
        for path in compType.getPath():
            paths[path] = compType.getPath()
        for exp in compType.getExposure():
            exposures[exp] = compType.getName()
        for req in compType.getRequirement():
            requirements[req] = compType.getName()
        for ep in compType.getEventPort():
            eventPorts[ep] = compType.getName()

        extdCompType = getExtendedFromCompType(compType.getName())

        while extdCompType is not None:
            for param in extdCompType.getParameter():
                params[param] = extdCompType.getName()
            for text in extdCompType.getText():
                texts[text] = extdCompType.getName()
            for path in extdCompType.getPath():
                paths[path] = extdCompType.getPath()
            for exp in extdCompType.getExposure():
                exposures[exp] = extdCompType.getName()
            for req in extdCompType.getRequirement():
                requirements[req] = extdCompType.getName()
            for ep in extdCompType.getEventPort():
                eventPorts[ep] = extdCompType.getName()
                
            extdCompType = getExtendedFromCompType(extdCompType.getName())


        if len(params) > 0:
            contents += "  <tr>\n"
            contents += category("Parameters", len(params), type="label-success")
            keysort = sorted(params.keys(), key=lambda param: param.name)
            print keysort
            for param in keysort:
                ct = params[param]
                origin = formatDescriptionSmall(param)
                style = ""
                if ct is not compType.getName():
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+param.getName()+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(param.getDimension())+"</td>\n  </tr>\n"


        if len(compType.getText()) > 0: # TODO: Check if Text elements are inherited...
            contents += "  <tr>\n"
            contents += category("Text fields", len(compType.getText()), type="label-success")
            for text in compType.getText():
                contents += "    <td colspan='2'><b>"+text.getName()+"</b></td>\n  </tr>\n"

        if len(compType.getPath()) > 0: # TODO: Check if Path elements are inherited...
            contents += "  <tr>\n"
            contents += category("Paths", len(compType.getPath()), type="label-success")
            for path in compType.getPath():
                contents += "    <td colspan='2'><b>"+path.getName()+"</b></td>\n  </tr>\n"

        #TODO: check if ComponentRef are inherited...
        if len(compType.getComponentReference()) > 0:
            contents += "  <tr>\n"
            contents += category("Component References", len(compType.getComponentReference()), type="label-success")
            for cr in compType.getComponentReference():
                contents += "    <td><b>"+cr.getName()+"</b></td>\n    <td width=\""+colWidthRight+"\">"+compTypeLink(cr.getType())+"</td>\n  </tr>\n"


        #TODO: check if Childs are inherited...
        if len(compType.getChild()) > 0:
            contents += "  <tr>\n"
            contents += category("Child elements", len(compType.getChild()), type="label-success")
            for child in compType.getChild():
                contents += "    <td><b>"+child.getName()+"</b></td>\n    <td width=\""+colWidthRight+"\">"+compTypeLink(child.getType())+"</td>\n  </tr>\n"

        #TODO: check if Childrens are inherited...
        if len(compType.getChildren()) > 0:
            contents += "  <tr>\n"
            contents += category("Children elements", len(compType.getChildren()), type="label-success")
            for children in compType.getChildren():
                contents += "    <td><b>"+children.getName()+"</b></td>\n    <td width=\""+colWidthRight+"\">"+compTypeLink(children.getType())+"</td>\n  </tr>\n"


        if len(compType.getConstant()) > 0:
            contents += "  <tr>\n"
            contents += category("Constants", len(compType.getConstant()))
            for const in compType.getConstant():
                contents += "    <td><b>"+const.getName()+"</b> = "+const.getValue()+formatDescriptionSmall(const)+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(const.getDimension())+"</td>\n  </tr>\n"

        if len(exposures) > 0:
            contents += "  <tr>\n"
            contents += category("Exposures", len(exposures))
            for exp in sorted(exposures, key=lambda entry: entry.name):
                ct = exposures[exp]
                origin = formatDescriptionSmall(exp)
                style = ""
                if ct is not compType.getName():
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+exp.getName()+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(exp.getDimension())+"</td>\n  </tr>\n"

        if len(requirements) > 0:
            contents += "  <tr>\n"
            contents += category("Requirements", len(requirements))
            for req in sorted(requirements, key=lambda entry: entry.name):
                ct = requirements[req]
                origin = formatDescriptionSmall(req)
                style = ""
                if ct is not compType.getName():
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+req.getName()+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">"+dimension(req.getDimension())+"</td>\n  </tr>\n"

        if len(eventPorts) > 0:
            contents += "  <tr>\n"
            contents += category("Event Ports", len(eventPorts))
            for ep in sorted(eventPorts, key=lambda entry: entry.name):
                ct = eventPorts[ep]
                origin = formatDescriptionSmall(ep)
                style = ""
                if ct is not compType.getName():
                    origin = spacer4+"(from "+compTypeLink(ct)+")"
                    style = greyStyle
                contents += "    <td"+style+"><b>"+ep.getName()+"</b>"+origin+"</td>\n    <td width=\""+colWidthRight+"\">Direction: "+ep.getDirection()+"</td>\n  </tr>\n"


        #TODO: check if Attachments are inherited...
        if len(compType.getAttachments()) > 0:
            contents += "  <tr>\n"
            contents += category("Attachments", len(compType.getAttachments()))
            for att in compType.getAttachments():
                contents += "    <td><b>"+att.getName()+"</b></td>\n    <td width=\""+colWidthRight+"\">"+compTypeLink(att.getType())+"</td>\n  </tr>\n"



        if len(compType.getDynamics()) > 0:
            for dynamics in compType.getDynamics():
                contents += "<tr>\n"
                contents += category("Dynamics", type="")
                contents += "<td colspan='2'>\n"

                structure = None
                if compType.getStructure() is not None:
                    structure = compType.getStructure()

                if structure is not None:
                    contents += "<span class=\"label\">Structure</span><br/><br/>\n"
                    for w in structure.getWith():
                        contents += spacer4+"WITH <b>"+w.getInstance()+"</b> AS <b>"+w.getAs()+"</b><br/>\n"
                    if structure.getChildInstance() is not None:
                        contents += spacer4+"CHILD INSTANCE: <b>"+structure.getChildInstance().getComponent()+"</b><br/>\n"
                    if structure.getMultiInstantiate() is not None:
                        mi = structure.getMultiInstantiate()
                        contents += spacer4+"INSTANTIATE <b>"+mi.getNumber()+"</b> COMPONENTS OF TYPE <b>"+mi.getComponent()+"</b><br/>\n"
                    if structure.getEventConnection() is not None:
                        ec = structure.getEventConnection()
                        targetPort = "" if ec.getTargetPort() is None else ", TARGET PORT: <b>"+ec.getTargetPort()+"</b>"
                        receiver = "" if ec.getReceiver() is None else ", RECEIVER: <b>"+ec.getReceiver()+"</b>"
                        delay = "" if ec.getDelay() is None else ", DELAY: <b>"+ec.getDelay()+"</b>"

                        contents += spacer4+"EVENT CONNECTION from <b>"+ec.getFrom()+"</b> TO <b>"+ec.getTo()+"</b>"+receiver+targetPort+delay+"<br/>\n"
                        if ec.getAssign() is not None:
                            contents += spacer4+spacer4+"ASSIGN <b>"+ec.getAssign().getProperty()+"</b> = "+ec.getAssign().getValue()+"<br/>\n"

                    contents += "<br/>\n"

                if len(dynamics.getStateVariable()) > 0:
                    contents += "<span class=\"label\">State Variables</span><br/><br/>\n"
                    for sv in dynamics.getStateVariable():
                        contents += spacer4+"<b>"+sv.getName()+"</b>"+spacer4+dimension(sv.getDimension())+exposedAs(sv.getExposure())+"<br/>\n"
                    if len(dynamics.getStateVariable()) > 0: contents += "<br/>\n"

                if dynamics.getOnStart() is not None:
                    contents += "<span class=\"label\">On Start</span><br/><br/>\n"
                    os = dynamics.getOnStart()
                    for sa in os.getStateAssignment():
                        contents += spacer4+"<b>"+sa.getVariable()+"</b> = "+sa.getValue()+"<br/>\n"
                    contents += "<br/>\n"

                if len(dynamics.getOnCondition()) > 0:
                    contents += "<span class=\"label\">On Conditions</span><br/><br/>\n"
                    for oc in dynamics.getOnCondition():
                        test = formatExpression(oc.getTest())
                        contents += spacer4+"IF "+test+" THEN<br/>\n"
                        for sa in oc.getStateAssignment():
                            contents += spacer4+spacer4+"<b>"+sa.getVariable()+"</b> = "+sa.getValue()+"<br/>\n"
                        for eo in oc.getEventOut():
                            contents += spacer4+spacer4+"EVENT OUT on port <b>"+eo.getPort()+"</b><br/>\n"
                        contents += "<br/>\n"


                if len(dynamics.getOnEvent()) > 0:
                    contents += "<span class=\"label\">On Events</span><br/><br/>\n"
                    for oe in dynamics.getOnEvent():
                        contents += spacer4+"EVENT IN on port: <b>"+oe.getPort()+"</b><br/>\n"
                        for sa in oe.getStateAssignment():
                            contents += spacer4+spacer4+"<b>"+sa.getVariable()+"</b> = "+sa.getValue()+"<br/>\n"
                        for eo in oe.getEventOut():
                            contents += spacer4+spacer4+"EVENT OUT on port <b>"+eo.getPort()+"</b><br/>\n"
                        contents += "<br/>\n"


                if len(dynamics.getDerivedVariable()) > 0:
                    contents += "<span class=\"label\">Derived Variables</span><br/><br/>\n"
                    for dv in dynamics.getDerivedVariable():
                        res = dv.getValue()
                        if res is None:
                            res = dv.getSelect()
                        contents += spacer4+"<b>"+dv.getName()+"</b> = "+res+spacer4+exposedAs(dv.getExposure())+"<br/>\n"
                        ''' TODO:
                        if dv.getOnAbsent() is not None:
                            contents += spacer4+spacer4+spacer4+"IF "+dv.getSelect()+" IS ABSENT: <b>"+dv.getName()+"</b> = "+dv.getOnAbsent()+"<br/>\n"'''
                    if len(dynamics.getDerivedVariable()) > 0: contents += "<br/>\n"

                if len(dynamics.getDerivedParameter()) > 0:
                    contents += "<span class=\"label\">Derived Parameters</span><br/><br/>\n"
                    for dp in dynamics.getDerivedParameter():
                        res = dp.getValue()
                        contents += spacer4+"<b>"+dp.getName()+"</b> = "+res+spacer4+"<br/>\n"
                    if len(dynamics.getDerivedParameter()) > 0: contents += "<br/>\n"
                

                if len(dynamics.getTimeDerivative()) > 0:
                    contents += "<span class=\"label\">Time Derivatives</span><br/><br/>\n"
                    for td in dynamics.getTimeDerivative():

                        contents += spacer4+"d <b>"+td.getVariable()+"</b> /dt = "+td.getValue()+"<br/>\n"
                    if len(dynamics.getTimeDerivative()) > 0: contents += "<br/>\n"


                if len(dynamics.getRegime()) > 0:
                    for rg in dynamics.getRegime():

                        initial = "" if rg.getInitial()== None or rg.getInitial()== "false" else " (initial)"
                        contents += "<span class=\"label\">Regime: "+rg.getName()+initial+"</span><br/><br/>\n"


                        if rg.getOnEntry() is not None:
                            contents += spacer8+"<span class=\"label\">On Entry</span><br/><br/>\n"
                            oe = rg.getOnEntry()
                            for sa in oe.getStateAssignment():
                                contents += spacer8+spacer4+"<b>"+sa.getVariable()+"</b> = "+sa.getValue()+"<br/>\n"
                            contents += "<br/>\n"

                        if len(rg.getOnCondition()) > 0:
                            contents += spacer8+"<span class=\"label\">On Conditions</span><br/><br/>\n"
                            for oc in rg.getOnCondition():
                                test = formatExpression(oc.getTest())
                                contents += spacer8+spacer4+"IF "+test+" THEN<br/>\n"
                                for sa in oc.getStateAssignment():
                                    contents += spacer8+spacer4+spacer4+"<b>"+sa.getVariable()+"</b> = "+sa.getValue()+"<br/>\n"
                                for eo in oc.getEventOut():
                                    contents += spacer8+spacer4+spacer4+"EVENT OUT on port <b>"+eo.getPort()+"</b><br/>\n"
                                if oc.getTransition() != None:
                                    contents += spacer8+spacer4+spacer4+"TRANSITION to REGIME <b>"+oc.getTransition().getRegime()+"</b><br/>\n"
                                contents += "<br/>\n"

                        if len(rg.getTimeDerivative()) > 0:
                            contents += spacer8+ "<span class=\"label\">Time Derivatives</span><br/><br/>\n"
                            for td in rg.getTimeDerivative():

                                contents += spacer8+spacer4+"d <b>"+td.getVariable()+"</b> /dt = "+td.getValue()+"<br/>\n"
                            if len(rg.getTimeDerivative()) > 0: contents += "<br/>\n"

                    if len(dynamics.getRegime()) > 0: contents += "<br/>\n"




                contents += "</td>\n"
                contents += "</tr>\n"

            
        contents += "</table>\n\n"

    contents += "</div>\n"
    contents += "</div>\n"
    contents += "</div>\n"
    contents += "</body>\n"

    doc.write(contents)
    doc.close()
