Name:		    flexdock
Version:	    1.2.4
Release:	    2
Summary:	    Docking framework for Java Swing GUI apps
Group:		    Development/Java
License:	    MIT 
URL:		    https://forge.scilab.org/index.php/p/flexdock/
Source0:	    http://forge.scilab.org/index.php/p/flexdock/downloads/get/%{name}-%{version}.tar.gz
Patch1:		    flexdock-1.2.3-demos.patch
Patch2:		    flexdock-1.2.3-build.patch
BuildRequires:	pkgconfig(x11)
BuildRequires:	java-devel
BuildRequires:	ant
BuildRequires:	jpackage-utils
BuildRequires:	jgoodies-common
BuildRequires:	jgoodies-looks
BuildRequires:	skinlf

Requires:       java
Requires:       jpackage-utils
Requires:       jgoodies-common
Requires:       jgoodies-looks
Requires:       skinlf

BuildArch:      noarch


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

#-------------------
%package javadoc
Summary:	Javadoc for flexdock
Group:		Development/Java

%description javadoc
Javadoc for flexdock.

#-------------------
%package manual
Summary:	User documentation for flexdock
Group:		Development/Java

%description manual
User manual for flexdock.

#-------------------
%prep
%setup -q
%patch1 -p1
%patch2 -p1

echo "sdk.home=%{java_home}" > workingcopy.properties
find ./ -name \*.jar -exec rm {} \;
build-jar-repository -s -p lib skinlf jgoodies-looks jgoodies-common
rm src/java/demo/org/flexdock/demos/raw/jmf/MediaPanel.java
rm src/java/demo/org/flexdock/demos/raw/jmf/JMFDemo.java

for i in "LICENSE.txt README release-notes.txt" ;
do
    %{__sed} -i 's/\r//' $i
done

%build
ant jar

%install
# jars
mkdir -p %{buildroot}%{_javadir}
install -pm644 build/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr docs/* \
	%{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}


%files
%doc LICENSE.txt README release-notes.txt
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%doc docs/
