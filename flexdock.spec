# Copyright (c) 2005-2008 oc2pus
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments to toni@links2linux.de

# norootforbuild

Name:			flexdock
Summary:		Swing windowing and docking framework
URL:			https://flexdock.dev.java.net/
Group:			Development/Java
Version:		0.5.1
Release:		%mkrel 0.0.2
License:		MIT
BuildRequires:	ant
BuildRequires:	dos2unix
BuildRequires:	fmj
BuildRequires:	jakarta-commons-logging
BuildRequires:	java-rpmbuild >= 1.5
BuildRequires:	jpackage-utils
BuildRequires:	jgoodies-looks
BuildRequires:	skinlf
BuildRequires:	unzip
BuildRequires:	update-alternatives
BuildRequires:	xml-commons-apis
BuildRequires:	libxorg-x11-devel
Requires:		java >= 1.5
Requires:		jakarta-commons-logging
Requires:		jgoodies-looks
Requires:		jpackage-utils
Requires:		skinlf
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:		%{name}-%{version}-src.zip
Patch0:			%{name}-build.xml.diff

%description
FlexDock is a Java docking framework for use in cross-platform Swing
applications. It offers features you'd expect in any desktop docking
framework such as:

* Tabbed and Split Layouts
* Drag-n-Drop capability (native drag rubber band painting on some platforms)
* Floating windows
* Collapsible Containers to Save Real Estate
* Layout Persistence

It is released using the MIT license.

%package javadoc
Summary:	Javadoc for flexdock
Group:		Development/Java
PreReq:		coreutils

%description javadoc
Javadoc for flexdock.

%package demo
Summary:	Some examples for flexdock
Group:		Development/Java
Requires:	%{name} = %{version}
Requires:	fmj
Requires:	java >= 1.5
Requires:	jakarta-commons-logging
Requires:	jgoodies-looks
Requires:	skinlf

%description demo
Some examples for flexdock.

%package manual
Summary:	User documetation for flexdock
Group:		Documentation/Other

%description manual
Usermanual for flexdock.

%prep
%setup -q -c -n %{name}
%patch0

# cleanup
%__rm -rf lib
find . -name *.so  | xargs %__rm -f
find . -name *.dll | xargs %__rm -f
find . -name *.o   | xargs %__rm -f

dos2unix     README* LICENSE.txt
%__chmod 644 README* LICENSE.txt

%__sed -i -e 's|-L/usr/X11R6/lib|-L/usr/X11R6/%{_lib}|g' \
	build.xml

%build
export CLASSPATH=$(build-classpath jgoodies-looks)
%ant -Dbuild.sysclasspath=first \
	-Dsdk.home="%{_libdir}/jvm/java" \
	build.with.native jar javadoc

%install
# jars
%__install -dm 755 %{buildroot}%{_javadir}
%__install -pm 644 build/%{name}-%{version}.jar \
	%{buildroot}%{_javadir}
pushd %{buildroot}%{_javadir}
	for jar in *-%{version}*; do
		ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`
	done
popd

# javadoc
%__install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
%__cp -pr build/docs/api/* \
	%{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
%__install -dm 755 %{buildroot}%{_datadir}/%{name}
%__install -pm 644 build/%{name}-demo-%{version}.jar \
	%{buildroot}%{_datadir}/%{name}
%__install -pm 644 build.xml \
	%{buildroot}%{_datadir}/%{name}

# startscripts for demo-apps
%__cat > %{name}-demo.sh << EOF
#!/bin/bash
%java \
	-cp \`build-classpath commons-logging skinlf fmj jgoodies-looks %{name}\`:%{_datadir}/%{name}/%{name}-demo-%{version}.jar \
	org.flexdock.demos.AllDemos
EOF
%__install -dm 755 %{buildroot}%{_bindir}
%__install -pm 755 %{name}-demo.sh \
	%{buildroot}%{_bindir}

%clean
[ -d %{buildroot} -a "%{buildroot}" != "" ] && %__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE.txt README*
%{_javadir}/*.jar

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%{_bindir}/%{name}-demo.sh
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files manual
%defattr(-,root,root,-)
%doc docs/

