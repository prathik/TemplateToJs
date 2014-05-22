from BeautifulSoup import BeautifulSoup
import sys, getopt

def main(argv):
    inputFile=''
    outputFile=''
    try:
        opts, args = getopt.getopt(argv, "i:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print "Error!"
        print "template.py -i <inputfile> -o <outputfile>"
        sys.exit(2)
    
    for opt,arg in opts:
        if opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg
    
    if inputFile == '' or outputFile == '':
        print "Error!"
        print "template.py -i <inputfile> -o <outputfile>"
        sys.exit(2)

    f = open(inputFile)
    y = BeautifulSoup(f.read())
    scripts = y.findAll(type="text/template")
    templates = []
    for script in scripts:
        s = script.getText().replace('"', '\\"');
        s = s.split("\n");
        t = map(lambda y: "[\""+y+"\"],", s)
        u = "\n".join(t);
        u = u[:-1]
        id = script["id"]
        u = "Template."+id.replace("-","_")+" = ["+u+"].join('\\n');"
        templates.append(u)
    f1 = open(outputFile,"w")
    templateHolder = ""
    for template in templates:
        templateHolder += "\n\n"+template
    templateString = '''
    (function(template) {
    window.Template = window.Template || {};
    template(window.jQuery, window.Template, window, window.document);
    }(function($,Template,window,document) {
    //Templates

    %s

    //Dom is ready
    $(function() {

    });

    //Rest of the code

    }));
    '''
    templateString = templateString % templateHolder
    f1.write(templateString)
    f.close()
    f1.close()

if __name__ == "__main__":
    main(sys.argv[1:])
