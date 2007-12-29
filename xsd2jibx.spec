%define gcj_support 1
%define section free

Name:           xsd2jibx
Version:        0.2b
Release:        %mkrel 0.0.4
Epoch:          0
Summary:        Generating Code and Binding from Schema
License:        BSD
Group:          Development/Java
URL:            http://jibx.sourceforge.net/xsd2jibx/index.html
Source0:        http://superb-east.dl.sourceforge.net/sourceforge/jibx/xsd2jibx-beta2b.zip
Source1:        xsd2jibx.sh
Source2:        http://jibx.cvs.sourceforge.net/*checkout*/jibx/xsd2jibx/new-build.xml
Requires:       ant
Requires:       jakarta-commons-lang
Requires:       jakarta-commons-logging
Requires:       jibx
Requires:       ws-jaxme
Requires:       log4j
Requires:       xpp3
BuildRequires:  ant
BuildRequires:  jakarta-commons-lang
BuildRequires:  jakarta-commons-logging
BuildRequires:  jibx
BuildRequires:  ws-jaxme
BuildRequires:  log4j
BuildRequires:  xpp3
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRequires:  java-rpmbuild
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Xsd2Jibx gives you a way to generate an initial set of Java classes, 
and the corresponding JiBX binding definition, from a W3C XML Schema 
input document. The generated classes and binding give you a 
starting point for working with XML documents matching the schema, 
which you can then refactor as appropriate to suit your needs.

The big difference from other data binding frameworks that generate 
code from schemas is that in the Xsd2Jibx case the generated code is 
under your control. You can modify the code, changing the binding 
definition if necessary, while continuing to work with documents 
matching the original schema. You can also keep working with the 
original generated classes even as the schema evolves, so long as 
you can compensate for the schema changes in the binding definition.

Xsd2Jibx is lagging behind the current JiBX code, and the generated 
bindings are not representative of current best practices. A 
replacement for Xsd2Jibx is being developed as part of the JiBX 1.2 
release.

%package javadoc
Summary:        Javadoc documentation for %{name}
Group:          Development/Java

%description javadoc
Javadoc documentation for %{name}.

%prep
%setup -q -n %{name}
%{__cp} -a %{SOURCE2} build.xml
%{__mkdir_p} api
%{_bindir}/find . -name '*.jar' | %{_bindir}/xargs -t %{__rm}
%{_bindir}/find . -name '*.css' | %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%build
export CLASSPATH=$(build-classpath commons-lang commons-logging jaxme/ws-jaxmejs log4j xpp3 ant jibx bcel)
export OPT_JAR_LIST=:
%{ant} -Djibxhome=.
pushd src/main
%{javadoc} -d ../../api `%{_bindir}/find . -name '*.java'`
popd

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}

%{__cp} -a lib/xsd2jibx.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -a %{SOURCE1} %{buildroot}%{_bindir}/xsd2jibx

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc docs/*
%attr(0755,root,root) %{_bindir}/xsd2jibx
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
