#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2003-2007 ZeroC, Inc. All rights reserved.
#
# This copy of Ice is licensed to you under the terms described in the
# ICE_LICENSE file included in this distribution.
#
# **********************************************************************
import os, sys, shutil, string, logging, compileall

#
# TODO: Setup a table for the dependencies so you don't have to 'flit'
# through the package descriptions to set the dependencies.
#
# TODO: BuildRequires needs to include our db45 package for building
# on RHEL or CentOS. It really shouldn't need it for other RPM based
# distributions
#

iceDescription = '''Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.'''

#
# Represents the 'main' package of an RPM spec file.
#
class Package:

    '''Encapsulates RPM spec file information to be used to generate a spec file on Linux and create RPMs for Ice.
    Root packages have the restriction that they cannot be noarch specific. If this becomes a problem in the future,
    the thing to do would be to remove the %ifnarch noarch/%endif pairs from Package and create a new subclass that
    writes these pairs and delegates the guts of the file populating to Package.'''

    def __init__(self, name, requires, summary, group, description, other, filelist):
        self.name = name
        self.requires = requires
        self.summary = summary
        self.group = group
        self.description = description
        self.filelist = filelist
	self.other = other
	self.prepTextGen = []
	self.buildTextGen = []
	self.installTextGen = []
        
    def writeHdr(self, ofile, version, release, installDir, targetHost):
	ofile.write('%define _unpackaged_files_terminate_build 0\n')
	ofile.write('\n%define core_arches %{ix86} x86_64\n')
	ofile.write('Summary: ' + self.summary + '\n')
	ofile.write('Name: ' + self.name + '\n')
	ofile.write('Version: ' + version + '\n')
	ofile.write('Release: ' + release + '\n')
	if len(self.requires) != 0:
            if self.requires.find('%version%'):
                self.requires = self.requires.replace('%version%', version)
	    ofile.write('Requires: ' + self.requires + '\n')
	ofile.write('License: GPL\n')
	ofile.write('Group:' + self.group + '\n')
	ofile.write('Vendor: ZeroC, Inc\n')
	ofile.write('URL: http://www.zeroc.com/\n')

	#
	# major.minor is part of the URL, this needs to be parameterized.
	#
        minorVer = version[0:3]
	ofile.write('Source0: http://www.zeroc.com/download/Ice/' + minorVer + '/Ice-%{version}.tar.gz\n')
	ofile.write('Source1: http://www.zeroc.com/download/Ice/' + minorVer + '/IceJ-%{version}-java2.tar.gz\n')
	ofile.write('Source2: http://www.zeroc.com/download/Ice/' + minorVer + '/IcePy-%{version}.tar.gz\n')
	ofile.write('Source3: http://www.zeroc.com/download/Ice/' + minorVer + '/IceCS-%{version}.tar.gz\n')
	ofile.write('Source4: http://www.zeroc.com/download/Ice/' + minorVer + '/IceJ-%{version}-java5.tar.gz\n')
	ofile.write('Source5: http://www.zeroc.com/download/Ice/' + minorVer + '/IcePHP-%{version}.tar.gz\n')
        ofile.write('Source6: http://www.zeroc.com/download/Ice/' + minorVer + '/THIRD_PARTY_LICENSE\n')
	ofile.write('Source7: http://www.zeroc.com/download/Ice/' + minorVer + '/ice.ini\n')
	ofile.write('Source8: http://www.zeroc.com/download/Ice/' + minorVer + '/README.Linux-RPM\n')
        ofile.write('Source9: http://www.zeroc.com/download/Ice/' + minorVer + '/SOURCES\n')
	if targetHost != "suse":
	    ofile.write('Source10: http://www.zeroc.com/download/Ice/' + minorVer + '/IceRuby-%{version}.tar.gz\n')

	ofile.write('\n')
	if len(installDir) != 0:
	    ofile.write('BuildRoot: ' + installDir + '\n')
	else:
	    ofile.write('BuildRoot: /var/tmp/Ice-' + version + '-' + release + '-buildroot\n')
        ofile.write('\n')
	ofile.write('''
%ifarch x86_64
%define icelibdir lib64
%else
%define icelibdir lib
%endif

%ifarch noarch
''')
        ofile.write('BuildRequires: mono-core >= 1.2.2\n')

	ofile.write('\n%endif\n')

	buildRequiresList = ['python >= 2.3.4', 'python-devel >= 2.3.4', 
		  'expat >= 0.5.0', 'libstdc++ >= 3.2', 'gcc >= 3.2', 'gcc-c++ >= 3.2', 'tar', 
		  'binutils >= 2.10', 'openssl >= 0.9.7a', 'openssl-devel >= 0.9.7a',  'ncurses >= 5.4']

	if targetHost == "suse":
	    buildRequiresList.append("bzip >= 1.0.2")
	else:
	    buildRequiresList.extend(['bzip2-devel >= 1.0.2', 'bzip2-libs >= 1.0.2', 'db45 >= 4.5.20', 
		'expat-devel >= 0.5.0'])

	for f in buildRequiresList:
            ofile.write('BuildRequires: ' + f  + '\n')

	ofile.write('\n')

	ofile.write('Provides: %s-%%{_arch}\n' % self.name)
	ofile.write('%description\n')
	ofile.write(self.description)
	ofile.write('\n')
	ofile.write('%prep\n')
	for g in self.prepTextGen:
	    g(ofile, version, targetHost)
	ofile.write('\n')
	ofile.write('%build\n')
	for g in self.buildTextGen:
	    g(ofile, version, targetHost)
	ofile.write('\n')
	ofile.write('%install\n')
	for g in self.installTextGen:
	    g(ofile, version, targetHost)
	ofile.write('\n')
	ofile.write('%clean\n')
	ofile.write('\n')
	ofile.write('%changelog\n')
	ofile.write('* Fri Dec 6 2006 ZeroC Staff\n')
	ofile.write('- See source distributions or the ZeroC website for more information\n')
	ofile.write('  about the changes in this release\n') 
	ofile.write('\n')

    def writeFileList(self, ofile, version, intVersion, installDir):
        ofile.write('%defattr(644, root, root, 755)\n\n')
        for perm, f in self.filelist:
            prefix = ''
	    
	    #
	    # Select an RPM spec file attribute depending on the type of
	    # file or directory we've specified.
	    #
            if perm == 'exe' or perm == 'lib':
                prefix = '%attr(755, root, root) '
	    elif perm == 'cfg':
		prefix = '%config'
	    elif perm == 'xdir':
		prefix = '%dir '

            if f.find('%version%'):
                f = f.replace('%version%', version)

            if perm == 'lib' and f.endswith('.VERSION'):
		fname = os.path.splitext(f)[0]
                ofile.write(prefix + '/usr/' + fname + '.' + version + '\n')
                ofile.write(prefix + '/usr/' + fname + '.' + str(intVersion) + '\n')
	    elif perm == 'cfg':
		ofile.write(f + '\n')
	    else:
		ofile.write(prefix + '/usr/' + f + '\n')
        ofile.write('\n')    

    def writePostInstall(self, ofile, version, intVersion, installDir):
	pass

    def writePostUninstall(self, ofile, version, intVersion, installDir):
	pass

    def writeFilesImpl(self, ofile, version, intVersion, installDir):
        ofile.write('%files\n')
        self.writeFileList(ofile, version, intVersion, installDir)
	ofile.write('\n')

	ofile.write('%post\n')
	self.writePostInstall(ofile, version, intVersion, installDir)

	ofile.write('%postun\n')
	self.writePostUninstall(ofile, version, intVersion, installDir)
	ofile.write('\n')

    def writeFiles(self, ofile, version, intVersion, installDir):
	ofile.write('\n%ifarch %{core_arches}\n')
	self.writeFilesImpl(ofile, version, intVersion, installDir)
	ofile.write('\n%else\n')
	ofile.write('%files\n')
	ofile.write('\n%endif\n')

    def addPrepGenerator(self, gen):
	self.prepTextGen.append(gen)

    def addBuildGenerator(self, gen):
	self.buildTextGen.append(gen)

    def addInstallGenerator(self, gen):
	self.installTextGen.append(gen)

#
# Represents subpackages in an RPM spec file.
#
class Subpackage(Package):

    def writeFilesImpl(self, ofile, version, intVersion, installDir):
        ofile.write('%%files %s\n' % self.name)
        self.writeFileList(ofile, version, intVersion, installDir)
	ofile.write('\n')

	ofile.write('%%post %s\n' % self.name)
	self.writePostInstall(ofile, version, intVersion, installDir)

	ofile.write('%%postun %s\n' % self.name)
	self.writePostUninstall(ofile, version, intVersion, installDir)
	ofile.write('\n')

    def writeFiles(self, ofile, version, intVersion, installDir):
	ofile.write('\n%ifarch %{core_arches}\n')
	self.writeFilesImpl(ofile, version, intVersion, installDir)
	ofile.write('\n%endif\n')

    def writeSubpackageHeader(self, ofile, version, release, installDir):
        ofile.write('%package ' + self.name + '\n')
        ofile.write('Summary: ' + self.summary + '\n')
        ofile.write('Group: ' + self.group + '\n')
	if len(self.requires) != 0:
            if self.requires.find('%version%'):
                self.requires = self.requires.replace('%version%', version)
	    ofile.write('Requires: ' + self.requires + '\n')
	if len(self.other) != 0:
	    ofile.write(self.other + '\n')
        ofile.write('%description ' + self.name + '\n')
        ofile.write(self.description)

    def writeHdr(self, ofile, version, release, installDir, targetHost):
        ofile.write('\n%ifarch %{core_arches}\n')	
	self.writeSubpackageHeader(ofile, version, release, installDir)
	ofile.write('\n%endif\n')

class NoarchSubpackage(Subpackage):
    def writeHdr(self, ofile, version, release, installDir, targetHost):
        ofile.write('\n%ifarch noarch\n')	
	self.writeSubpackageHeader(ofile, version, release, installDir)
	ofile.write('\n%endif\n')

    def writeFiles(self, ofile, version, intVersion, installDir):
        ofile.write('\n%ifarch noarch\n')	
	self.writeFilesImpl(ofile, version, intVersion, installDir)
	ofile.write('\n%endif\n')

class DotNetPackage(Subpackage):
    def writePostInstall(self, ofile, version, intVersion, installDir):
	ofile.write('\n%ifnarch noarch\n')
	ofile.write('''
pklibdir="%{icelibdir}"

for f in icecs glacier2cs iceboxcs icegridcs icepatch2cs icestormcs;
do
    sed -i.bak -e "s/^mono_root.*$/mono_root = \/usr/" /usr/$pklibdir/pkgconfig/$f.pc ; 
done
	''')
	ofile.write('\n%endif\n')


class DotNetPackage(Subpackage):
    def writePostInstall(self, ofile, version, intVersion, installDir):
	ofile.write('\n%ifnarch noarch\n')
	ofile.write('''
pklibdir="lib"

%ifarch x86_64
pklibdir="lib64"
%endif

for f in icecs glacier2cs iceboxcs icegridcs icepatch2cs icestormcs;
do
    sed -i.bak -e "s/^mono_root.*$/mono_root = \/usr/" /usr/$pklibdir/pkgconfig/$f.pc ; 
done
	''')
	ofile.write('\n%endif\n')

#
# NOTE: File transforms should be listed before directory transforms.
#
transforms = [ ('file', 'ice.ini', 'etc/php.d/ice.ini'),
	       ('dir', 'lib', 'usr/lib'),
	       ('dir', '%{icelibdir}', 'usr/%{icelibdir}'),
	       ('file', 'usr/%{icelibdir}/IcePHP.so', 'usr/%{icelibdir}/php/modules/IcePHP.so'),
	       ('file', 'usr/lib/Ice.jar', 'usr/lib/Ice-%version%/Ice.jar' ),
	       ('dir', 'usr/lib/java2', 'usr/lib/Ice-%version%/java2' ),
	       ('file', 'usr/lib/IceGridGUI.jar', 'usr/lib/Ice-%version%/IceGridGUI.jar' ),
	       ('file', 'bin/icecs.dll', 'usr/lib/mono/gac/icecs/%version%.0__1f998c50fec78381/icecs.dll'),
	       ('file', 'bin/glacier2cs.dll',
		       'usr/lib/mono/gac/glacier2cs/%version%.0__1f998c50fec78381/glacier2cs.dll'),
	       ('file', 'bin/iceboxcs.dll',
		       'usr/lib/mono/gac/iceboxcs/%version%.0__1f998c50fec78381/iceboxcs.dll'),
	       ('file', 'bin/icegridcs.dll',
		       'usr/lib/mono/gac/icegridcs/%version%.0__1f998c50fec78381/icegridcs.dll'),
	       ('file', 'bin/icepatch2cs.dll',
		       'usr/lib/mono/gac/icepatch2cs/%version%.0__1f998c50fec78381/icepatch2cs.dll'),
	       ('file', 'bin/icestormcs.dll',
		       'usr/lib/mono/gac/icestormcs/%version%.0__1f998c50fec78381/icestormcs.dll'),
	       ('dir', 'ant', 'usr/lib/Ice-%version%/ant'),
	       ('dir', 'config', 'usr/share/Ice-%version%'),
	       ('dir', 'slice', 'usr/share/slice'),
	       ('dir', 'bin', 'usr/bin'),
	       ('dir', 'include', 'usr/include'),
	       ('dir', 'python', 'usr/%{icelibdir}/Ice-%version%/python'),
	       ('dir', 'ruby', 'usr/%{icelibdir}/Ice-%version%/ruby'),
               ('dir', 'doc', 'usr/share/doc/Ice-%version%/doc'),
               ('file', 'README', 'usr/share/doc/Ice-%version%/README'),
               ('file', 'ICE_LICENSE', 'usr/share/doc/Ice-%version%/ICE_LICENSE'),
               ('file', 'LICENSE', 'usr/share/doc/Ice-%version%/LICENSE'),
               ('file', 'THIRD_PARTY_LICENSE', 'usr/share/doc/Ice-%version%/THIRD_PARTY_LICENSE'),
               ('file', 'SOURCES', 'usr/share/doc/Ice-%version%/SOURCES')
               ]

fileLists = [
    Package('ice',
            '',
	    'The Ice base runtime and services',
            'System Environment/Libraries',
	    iceDescription,
	    'Provides: ice-%{_arch}',
            [('xdir', 'share/doc/Ice-%version%'),
             ('doc', 'share/doc/Ice-%version%/ICE_LICENSE'),
             ('doc', 'share/doc/Ice-%version%/LICENSE'),
             ('doc', 'share/doc/Ice-%version%/README'),
             ('doc', 'share/doc/Ice-%version%/SOURCES'),
             ('doc', 'share/doc/Ice-%version%/THIRD_PARTY_LICENSE'),
             ('exe', 'bin/dumpdb'),
             ('exe', 'bin/transformdb'),
             ('exe', 'bin/glacier2router'),
             ('exe', 'bin/icebox'),
             ('exe', 'bin/iceboxadmin'),
             ('exe', 'bin/icecpp'),
             ('exe', 'bin/icepatch2calc'),
             ('exe', 'bin/icepatch2client'),
             ('exe', 'bin/icepatch2server'),
             ('exe', 'bin/icestormadmin'),
             ('exe', 'bin/slice2docbook'), 
             ('exe', 'bin/icegridadmin'), 
             ('exe', 'bin/icegridnode'), 
             ('exe', 'bin/icegridregistry'),
             ('exe', 'bin/iceca'),
             ('file', 'bin/ImportKey.class'),
             ('lib', '%{icelibdir}/libFreeze.so.VERSION'),
             ('lib', '%{icelibdir}/libGlacier2.so.VERSION'),
             ('lib', '%{icelibdir}/libIceBox.so.VERSION'),
             ('lib', '%{icelibdir}/libIcePatch2.so.VERSION'),
             ('lib', '%{icelibdir}/libIce.so.VERSION'),
             ('lib', '%{icelibdir}/libIceSSL.so.VERSION'),
             ('lib', '%{icelibdir}/libIceStormService.so.VERSION'),
             ('lib', '%{icelibdir}/libIceStorm.so.VERSION'),
             ('lib', '%{icelibdir}/libIceUtil.so.VERSION'),
             ('lib', '%{icelibdir}/libIceXML.so.VERSION'),
             ('lib', '%{icelibdir}/libSlice.so.VERSION'),
             ('lib', '%{icelibdir}/libIceGrid.so.VERSION'),
             ('xdir', 'lib/Ice-%version%'),
	     ('file', 'lib/Ice-%version%/IceGridGUI.jar'),
             ('dir', 'share/slice'),
             ('dir', 'share/doc/Ice-%version%/doc'),
	     ('xdir', 'share/Ice-%version%'),
	     ('file', 'share/Ice-%version%/templates.xml'),
	     ('exe', 'share/Ice-%version%/convertssl.py'),
             ('exe', 'share/Ice-%version%/upgradeicegrid.py'),
             ('file', 'share/Ice-%version%/icegrid-slice.3.1.ice.gz')]),
    Subpackage('c++-devel',
               'ice = %version%',
               'Tools for developing Ice applications in C++',
               'Development/Tools',
	       iceDescription,
	       'Requires: ice-%{_arch}',
               [('exe', 'bin/slice2cpp'),
                ('exe', 'bin/slice2freeze'),
                ('dir', 'include'),
		('lib', '%{icelibdir}/libFreeze.so'),
		('lib', '%{icelibdir}/libGlacier2.so'),
		('lib', '%{icelibdir}/libIceBox.so'),
		('lib', '%{icelibdir}/libIceGrid.so'),
		('lib', '%{icelibdir}/libIcePatch2.so'),
		('lib', '%{icelibdir}/libIce.so'),
		('lib', '%{icelibdir}/libIceSSL.so'),
		('lib', '%{icelibdir}/libIceStormService.so'),
		('lib', '%{icelibdir}/libIceStorm.so'),
		('lib', '%{icelibdir}/libIceUtil.so'),
		('lib', '%{icelibdir}/libIceXML.so'),
		('lib', '%{icelibdir}/libSlice.so')
		]),
    DotNetPackage('csharp-devel',
	          'ice-dotnet = %version%',
		  'Tools for developing Ice applications in C#',
		  'Development/Tools',
		  iceDescription,
		  'Requires: ice-%{_arch}',
		  [('exe', 'bin/slice2cs'),
		  ('xdir', 'share/doc/Ice-%version%'),
		  ('file', '%{icelibdir}/pkgconfig/icecs.pc'),
		  ('file', '%{icelibdir}/pkgconfig/glacier2cs.pc'),
		  ('file', '%{icelibdir}/pkgconfig/iceboxcs.pc'),
		  ('file', '%{icelibdir}/pkgconfig/icegridcs.pc'),
		  ('file', '%{icelibdir}/pkgconfig/icepatch2cs.pc'),
		  ('file', '%{icelibdir}/pkgconfig/icestormcs.pc')]),
    Subpackage('java-devel',
               'ice-java = %version%',
               'Tools for developing Ice applications in Java',
               'Development/Tools',
	       iceDescription,
	       'Requires: ice-%{_arch}',
               [('exe', 'bin/slice2java'),
                ('exe', 'bin/slice2freezej'),
		('xdir', 'lib/Ice-%version%'),
		('dir', 'lib/Ice-%version%/ant'), ]),
    Subpackage('python',
               'ice = %version%, python >= 2.3.4',
               'The Ice runtime for Python applications',
               'System Environment/Libraries',
	       iceDescription,
	       'Requires: ice-%{_arch}',
               [('dir', '%{icelibdir}/Ice-%version%/python')]),
    Subpackage('python-devel',
               'ice-python = %version%',
               'Tools for developing Ice applications in Python',
               'Development/Tools',
	       iceDescription,
	       'Requires: ice-%{_arch}',
               [('exe', 'bin/slice2py')]),
    Subpackage('ruby',
               'ice = %version%, ruby >= 1.8.1',
               'The Ice runtime for Ruby applications',
               'System Environment/Libraries',
	       iceDescription,
	       'Requires: ice-%{_arch}',
               [('dir', '%{icelibdir}/Ice-%version%/ruby')]),
    Subpackage('ruby-devel',
               'ice-ruby = %version%',
               'Tools for developing Ice applications in Python',
               'Development/Tools',
	       iceDescription,
	       'Requires: ice-%{_arch}',
               [('exe', 'bin/slice2rb')]),
    Subpackage('php',
	       'ice = %version%, php = 5.1.6',
	       'The Ice runtime for PHP applications',
	       'System Environment/Libraries',
	       iceDescription,
	       'Requires: ice-%{_arch}',
	       [('lib', '%{icelibdir}/php/modules'), ('cfg', '/etc/php.d/ice.ini')]
	       ),
    NoarchSubpackage('java',
		     'ice = %version%, db45-java >= 4.5.20',
		     'The Ice runtime for Java',
		     'System Environment/Libraries',
		     iceDescription,
		     '',
		     [ ('xdir', 'lib/Ice-%version%'),
		     ('file', 'lib/Ice-%version%/Ice.jar'),
                     ('xdir', 'lib/Ice-%version%/java2'),
		     ('file', 'lib/Ice-%version%/java2/Ice.jar')
		     ]),
    NoarchSubpackage('dotnet',
                     'ice = %version%, mono-core >= 1.2.2',
		     'The Ice runtime for C# applications',
		     'System Environment/Libraries',
		     iceDescription,
		     '',
		     [('dll', 'lib/mono/gac/glacier2cs/%version%.0__1f998c50fec78381/glacier2cs.dll'),
		     ('dll', 'lib/mono/gac/icecs/%version%.0__1f998c50fec78381/icecs.dll'),
		     ('dll', 'lib/mono/gac/iceboxcs/%version%.0__1f998c50fec78381/iceboxcs.dll'),
		     ('dll', 'lib/mono/gac/icegridcs/%version%.0__1f998c50fec78381/icegridcs.dll'),
		     ('dll', 'lib/mono/gac/icepatch2cs/%version%.0__1f998c50fec78381/icepatch2cs.dll'),
		     ('dll', 'lib/mono/gac/icestormcs/%version%.0__1f998c50fec78381/icestormcs.dll'),
		     ('exe', 'bin/iceboxnet.exe'),
		     ('exe', 'bin/iceboxadminnet.exe')])
    ]

def _transformDirectories(transforms, version, installDir):
    """Transforms a directory tree that was created with 'make installs'
    to an RPM friendly directory tree.  NOTE, this will not work on all
    transforms, there are certain types of transforms in certain orders
    that will break it."""
    cwd = os.getcwd()
    os.chdir(installDir)
    for type, source, dest in transforms:
	dest = dest.replace('%version%', version)
	source = source.replace('%version%', version)

	libdir = 'lib' # Key on architecture.
	dest = dest.replace('%{icelibdir}', libdir)
	source = source.replace('%{icelibdir}', libdir)

        sourcedir = source
        destdir = dest

	if os.path.exists('./tmp'):
	    shutil.rmtree('./tmp')

	try:
	    if not os.path.isdir(sourcedir):
		if os.path.exists(source):
		    os.renames(source, dest)
	    else:
		# 
		# This is a special problem.  What this implies is that
		# we are trying to move the contents of a directory into
		# a subdirectory of itself.  The regular shutil.move()
		# won't cut it.
		# 
		if os.path.isdir(sourcedir) and sourcedir.split("/")[0] == destdir.split("/")[0]:
		    os.renames(sourcedir, "./tmp/" + sourcedir)
		    os.renames("./tmp/" + sourcedir, destdir)	
		else:
		    print 'Renaming ' + source + ' to ' + dest
		    if os.path.exists(source):
			os.renames(source, dest)

	except OSError:
	    print "Exception occurred while trying to transform " + source + " to " + dest
	    raise

    os.chdir(cwd)

def createArchSpecFile(ofile, installDir, version, soVersion, targetHost):
    for v in fileLists:
	v.writeHdr(ofile, version, "1", installDir, targetHost)
	ofile.write("\n\n\n")
    for v in fileLists:
	v.writeFiles(ofile, version, soVersion, installDir)
	ofile.write("\n")

def createFullSpecFile(ofile, installDir, version, soVersion, targetHost):
    fullFileList = fileLists 
    fullFileList[0].addPrepGenerator(writeUnpackingCommands)
    fullFileList[0].addBuildGenerator(writeBuildCommands)
    fullFileList[0].addInstallGenerator(writeInstallCommands)
    fullFileList[0].addInstallGenerator(writeTransformCommands)

    for v in fullFileList:
	v.writeHdr(ofile, version, "1", '', targetHost)
	ofile.write("\n\n\n")
    for v in fullFileList:
	v.writeFiles(ofile, version, soVersion, '')
	ofile.write("\n")

def writeUnpackingCommands(ofile, version, targetHost):
    ofile.write('%setup -n Ice-%{version} -q -T -D -b 0\n')
    ofile.write("""#
# The Ice make system does not allow the prefix directory to be specified
# through an environment variable or a command line option.  So we edit some
# files in place with sed.
#
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/Ice-%{version}/config/Make.rules
%setup -q -n IceJ-%{version}-java2 -T -D -b 1
%setup -q -n IcePy-%{version} -T -D -b 2
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/IcePy-%{version}/config/Make.rules
%setup -q -n IceCS-%{version} -T -D -b 3 
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/IceCS-%{version}/config/Make.rules.cs
sed -i -e 's/^cvs_build.*$/cvs_build = no/' $RPM_BUILD_DIR/IceCS-%{version}/config/Make.rules.cs
%setup -q -n IceJ-%{version}-java5 -T -D -b 4
%setup -q -n IcePHP-%{version} -T -D -b5 
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/IcePHP-%{version}/config/Make.rules
cd $RPM_BUILD_DIR
cp $RPM_SOURCE_DIR/ice.ini $RPM_BUILD_DIR/IcePHP-%{version}
""")
    if targetHost != "suse":
	ofile.write("""
%setup -q -n IceRuby-%{version} -T -D -b 10
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/IceRuby-%{version}/config/Make.rules
	""")
    ofile.write("""

#
# Create links to the Berkeley DB that we want. This should allow us to bypass
# the older installed links.
#
if ! test -h $RPM_BUILD_DIR/Ice-%{version}/include/db.h; then
    ln -s /usr/include/db45/db.h $RPM_BUILD_DIR/Ice-%{version}/include/db.h
fi
if ! test -h $RPM_BUILD_DIR/Ice-%{version}/include/db_cxx.h; then
    ln -s /usr/include/db45/db_cxx.h $RPM_BUILD_DIR/Ice-%{version}/include/db_cxx.h
fi
if ! test -h $RPM_BUILD_DIR/Ice-%{version}/lib/libdb.so; then
    ln -s /lib/libdb-4.5.so $RPM_BUILD_DIR/Ice-%{version}/lib/libdb.so
fi
if ! test -h $RPM_BUILD_DIR/Ice-%{version}/lib/libdb_cxx.so; then
    ln -s /usr/lib/libdb_cxx-4.5.so $RPM_BUILD_DIR/Ice-%{version}/lib/libdb_cxx.so
fi

""")

def writeBuildCommands(ofile, version, targetHost):
    ofile.write("""
cd $RPM_BUILD_DIR/Ice-%{version}/src
gmake OPTIMIZE=yes RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix=""
cd $RPM_BUILD_DIR/IcePy-%{version}
gmake  OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix=""
cd $RPM_BUILD_DIR/IceCS-%{version}
export PATH=$RPM_BUILD_DIR/Ice-%{version}/bin:$PATH
export LD_LIBRARY_PATH=$RPM_BUILD_DIR/Ice-%{version}/lib:$LD_LIBRARY_PATH
gmake OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/IcePHP-%{version}
gmake OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix=""
""")
    if targetHost != "suse":
	ofile.write("""
cd $RPM_BUILD_DIR/IceRuby-%{version}
gmake OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix=""
	""")

def writeInstallCommands(ofile, version, targetHost):
    ofile.write("""
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/Ice-%{version}
gmake RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix="" install

if test ! -d $RPM_BUILD_ROOT/lib;
then
    mkdir -p $RPM_BUILD_ROOT/lib
fi
cp -p $RPM_BUILD_DIR/IceJ-%{version}-java5/lib/Ice.jar $RPM_BUILD_ROOT/lib/Ice.jar
cp -pR $RPM_BUILD_DIR/IceJ-%{version}-java5/ant $RPM_BUILD_ROOT

if test ! -d $RPM_BUILD_ROOT/lib/java2;
then
    mkdir -p $RPM_BUILD_ROOT/lib/java2
fi
cp -p $RPM_BUILD_DIR/IceJ-%{version}-java2/lib/Ice.jar $RPM_BUILD_ROOT/lib/java2/Ice.jar
cp -p $RPM_BUILD_DIR/IceJ-%{version}-java2/lib/IceGridGUI.jar $RPM_BUILD_ROOT/lib/IceGridGUI.jar

cd $RPM_BUILD_DIR/IcePy-%{version}
gmake ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix="" install
cd $RPM_BUILD_DIR/IceCS-%{version}
export PATH=$RPM_BUILD_DIR/Ice-%{version}/bin:$PATH
export LD_LIBRARY_PATH=$RPM_BUILD_DIR/Ice-%{version}/lib:$LD_LIBRARY_PATH
gmake NOGAC=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT install
cp $RPM_SOURCE_DIR/README.Linux-RPM $RPM_BUILD_ROOT/README
cp $RPM_SOURCE_DIR/THIRD_PARTY_LICENSE $RPM_BUILD_ROOT/THIRD_PARTY_LICENSE
cp $RPM_SOURCE_DIR/SOURCES $RPM_BUILD_ROOT/SOURCES
cp $RPM_SOURCE_DIR/ice.ini $RPM_BUILD_ROOT/ice.ini
if test ! -d $RPM_BUILD_ROOT/%{icelibdir};
then
    mkdir -p $RPM_BUILD_ROOT/%{icelibdir}
fi
cd $RPM_BUILD_DIR/IcePHP-%{version}
gmake NOGAC=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT install
cp $RPM_BUILD_DIR/IceJ-%{version}-java2/config/build.properties $RPM_BUILD_ROOT/config
if test ! -d $RPM_BUILD_ROOT/%{icelibdir}/pkgconfig ; 
then 
    mkdir $RPM_BUILD_ROOT/%{icelibdir}/pkgconfig
fi

for f in icecs glacier2cs iceboxcs icegridcs icepatch2cs icestormcs; 
do 
    cp $RPM_BUILD_DIR/IceCS-%{version}/bin/$f.dll $RPM_BUILD_ROOT/bin
    cp $RPM_BUILD_DIR/IceCS-%{version}/lib/pkgconfig/$f.pc $RPM_BUILD_ROOT/%{icelibdir}/pkgconfig 
done

""")
    if targetHost != "suse":
	ofile.write("""
cd $RPM_BUILD_DIR/IceRuby-%{version}
gmake OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix="" install
	""")

def writeTransformCommands(ofile, version, targetHost):
    #
    #  XXX- this needs serious revisiting after changing how the
    #  transforms work to accomodate files for /etc.
    #
    ofile.write('#\n')
    ofile.write('# The following commands transform a standard Ice installation directory\n')
    ofile.write('# structure to a directory structure more suited to integrating into a\n')
    ofile.write('# Linux system.\n')
    ofile.write('#\n\n')
    for type, source, dest in transforms:
	dest = dest.replace('%version%', version)
	source = source.replace('%version%', version)
	if type == 'file':
	    ofile.write('# Rule 1\n')
	    ofile.write('mkdir -p $RPM_BUILD_ROOT/' + os.path.dirname(dest) + '\n')
	    ofile.write('mv $RPM_BUILD_ROOT/' + source + ' $RPM_BUILD_ROOT/' + dest + '\n')
	elif type == 'dir':
	    if os.path.dirname(dest) <> '' and source.split('/')[0] == dest.split('/')[0]:
		ofile.write('# Rule 2\n')
		ofile.write('mkdir -p $RPM_BUILD_ROOT/arraftmp\n')
		ofile.write('mkdir -p $RPM_BUILD_ROOT/arraftmp/%s\n' % os.path.dirname(source))
		ofile.write('mv $RPM_BUILD_ROOT/' + source + ' $RPM_BUILD_ROOT/arraftmp/' + source + '\n')
		ofile.write('mkdir -p $RPM_BUILD_ROOT/' + os.path.dirname(dest) + '\n')
		ofile.write('mv $RPM_BUILD_ROOT/arraftmp/' + source + ' $RPM_BUILD_ROOT/' + dest + '\n')
		ofile.write('rm -rf $RPM_BUILD_ROOT/arraftmp\n')
	    elif os.path.dirname(dest) <> '':
		ofile.write('# Rule 3\n')
		ofile.write('if test -d $RPM_BUILD_ROOT/' + source + '\n')
		ofile.write('then\n')
		ofile.write('    mkdir -p $RPM_BUILD_ROOT/' + os.path.dirname(dest) + '\n')
		ofile.write('    mv $RPM_BUILD_ROOT/' + source + ' $RPM_BUILD_ROOT/' + dest + '\n')
		ofile.write('fi\n')
	    else:
		ofile.write('# Rule 4\n')
		ofile.write('mv $RPM_BUILD_ROOT/usr/' + source + ' $RPM_BUILD_ROOT/usr/' + dest + '\n')
	
if __name__ == "main":
    print 'Ice RPM Tools module'
