import uuid
import os
import shutil
import subprocess

class CodeResult():
    # ccr = compiler result, cr = code result
    def __init__(self, ccr, cr, uuid, chroot, cc):
        self.ccr = ccr
        self.cr = cr
        self.uuid = uuid
        self.chroot = chroot
        self.cc = cc

class StubSubprocess():
    def __init__(self, stdout):
        self.stdout = stdout

def run_code(lang, code):
    #TODO: handle a naming conflict (two containers with the same UUID)
    cuuid = str(uuid.uuid4())
    lang = lang.lower()

    #Setup container folder
    try:  
        os.mkdir(cuuid)
    except OSError:  
        print ("Creation of the directory %s failed" % cuuid)

    #Find lang extenstion
    lang_ext = ""
    if lang == "c":
        lang_ext = ".c"
    elif lang == "cxx" or lang == "cpp" or lang == "c++":
        lang_ext = ".cpp"

    #Write code to run
    f = open(cuuid + "/code" + lang_ext, "w")
    f.write(code)
    f.close()

    #Compile the code
    #TODO: pass compiler output to Discord
    ccr_result = None
    if lang == "c":
        ccr_result = subprocess.run(['gcc', "-static", "-o", cuuid + "/a.out", cuuid + "/code" + lang_ext], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif lang == "cxx" or lang == "cpp" or lang == "c++":
        ccr_result = subprocess.run(['g++', "-static", "-o", cuuid + "/a.out", cuuid + "/code" + lang_ext], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    cc = None
    if lang == "c":
        cc = "gcc"
    elif lang == "cxx" or lang == "cpp" or lang == "c++":
        cc = "g++"
        
    cr_result = None
    try:
        cr_result = subprocess.run(["sudo", "chroot", cuuid, "/a.out"], stdout=subprocess.PIPE)
    except:
        if not os.path.exists(cuuid + "/a.out"):
            cr_result = StubSubprocess(b"[Compiler did not produce a binary]")
        else:
            cr_result = StubSubprocess(b"[HiggsBot internal error]")

    #print(ccr_result.stdout)
    #print(ccr_result.stderr)
    #print(cr_result.stdout)
    results = CodeResult(ccr_result.stderr.decode("utf-8").replace(cuuid+"/", ""), cr_result.stdout.decode("utf-8"), cuuid, True, cc)

    #Cleanup container folder
    try:  
        shutil.rmtree(cuuid)
    except OSError:  
        print ("Deletion of the directory %s failed" % cuuid)

    return results
