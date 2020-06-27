import os
import re
import shutil
import subprocess



#============== USER CONFIG SECTION ==============

print("""WARNING: read the entirety of this (short) file and make sure you understand what it does!  You
likely need to change the configuration at the top, and disable any stuff you don't want to happen.

This code has been checked and should be reasonably safe, but it was also written while enraged at
evil, make-work publishing systems.  The code is both brittle and very, very hacky.  If you choose
to run this code, you do so at your own risk!
""")
input("Press ENTER to accept, and begin trying to make the world a better place . . .")

tmpdirname = ".tmp-version"
tmpdir = tmpdirname+"/"

main_file = "main.tex"

#=================================================



#Make a temporary directory
if not os.path.exists(tmpdir):
	os.makedirs(tmpdir)



#Misc. stuff

def flatten_path(path):
	return tmpdir + path.replace("/","__")

class File(object):
	def __init__(self,path):
		self.path_orig = path[2:].replace("\\","/")
		self.path_new = flatten_path(self.path_orig)
	def do_copy(self):
		#if not os.path.exists(self.path_new):
		shutil.copyfile(self.path_orig,self.path_new)
	def print(self):
		print("\"%s\" => \"%s\""%(self.path_orig,self.path_new))



#Get a list of all the files
files = []
def scan(indir):
	for f in os.scandir(indir):
		if f.is_dir():
			if ".git" in f.path: pass
			elif tmpdirname in f.path: pass
			else:
				#dirs.append(f.path.replace("\\","/")[2:]+"/")
				scan(f.path)
		else:
			if ".py" in f.path: pass
			else:
				files.append(File(f.path))
scan("./")



#Print them out and set aside the ones that are LaTeX

print("Files:")
for f in files:
	print("  ",end=""); f.print()

print("LaTeX files:")
texfiles = [ file for file in files if ".tex" in file.path_new ]
for texfile in texfiles: print("  "+str(texfile.path_new))



#Begin munging.  Chomp chomp.
print("Munging LaTeX to accommodate other peoples' incompetency . . .")

#	Pass 1: flatten files
print("  Pass 1: flatten files . . .")
for file in files:
	file.do_copy()

#	Pass 2: tweak input files so that "latex.py" can understand them (note arguments to `\input`
#		being defined by macros is not yet implemented)
print("  Pass 2: adjust `\\input`s . . .")
for file in texfiles:
	f = open(file.path_new,"r")
	data = f.read()
	f.close()

	def fn_input(matchobj):
		path = matchobj.group("path")
		path = flatten_path(path).split("/")[-1]
		out = r"\input{"+path+"}"
		return out
	data = re.sub(r"\\input\{(?P<path>.+)\.tex\}",fn_input,data)

	f = open(file.path_new,"w")
	f.write(data)
	f.close()

#	Pass 3: run "latex.py" to evaluate macros and inline everything into one file
print("  Pass 3: run \"latex.py\" to mung LaTeX . . .")
os.chdir(tmpdir)

proc = subprocess.Popen(["python","../latex.py","-o",main_file+".tmp.tex","-M","-L",main_file], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
stdout, stderr = proc.communicate()
stdout=stdout.decode("utf-8").replace("\r\n","\n"); stderr=stderr.decode("utf-8").replace("\r\n","\n")
print(stdout)
print(stderr)
shutil.copyfile(main_file+".tmp.tex",main_file)
os.remove(main_file+".tmp.tex")

os.chdir("..")

#	Pass 4: remove now-redundant ".tex" files in the temporary directory
print("  Pass 4: removing now-redundant temporary \".tex\" files . . .")
texfiles2 = []
for file in texfiles:
	if main_file not in file.path_new:
		os.remove(file.path_new)
	else:
		texfiles2.append(file)
texfiles = texfiles2 #This should only have one file in it

#	Pass 5: fix resource paths in the ".tex" file (do it after "latex.py" so that the argument to
#		the using function *can* have depended on macros)
print("  Pass 5: adjust resource paths")
for file in texfiles:
	f = open(file.path_new,"r")
	data = f.read()
	f.close()

	for file2 in files:
		data = data.replace(file2.path_orig,file2.path_new.split("/")[-1])

	f = open(file.path_new,"w")
	f.write(data)
	f.close()

#	Pass 6: inline and delete the temporary ".csv" files into PGFPlots tables, because their system
#		is too stupid to do that (and also thinks they're videos???)
print("  Pass 6: inlining and deleting CSV files . . .")
for file in texfiles:
	f = open(file.path_new,"r")
	data = f.read()
	f.close()

	def fn_input(matchobj):
		path = matchobj.group("path")
		fcsv = open(tmpdir+path,"r")
		csv = fcsv.read()
		fcsv.close()
		out = ""
		for line in csv.split("\n"):
			out += line.replace(",",",")+"\n"
		return "{\n"+out[:-1]+"}"
	data = re.sub(r"\{(?P<path>[^\}]+\.csv)\}",fn_input,data)

	f = open(file.path_new,"w")
	f.write(data)
	f.close()
for file in files:
	if ".csv" in file.path_new:
		os.remove(file.path_new)



#Done
print("Done!")
