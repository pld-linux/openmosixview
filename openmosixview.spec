Summary:	openMosixview is a cluster-management GUI
Summary(pl):	openMosixview to graficzny interfejs do zarządzania clustrem
Name:		openmosixview
Version:	1.4
Release:	0.3
Group:		Applications/System
License:	GPL
Vendor:		Matt Rechenburg <mosixview@t-online.de>
Source0:	http://www.openmosixview.com/download/%{name}-%{version}.tar.gz
Source1:	openmosixcollector.init
Url:		http://www.openmosixview.com
BuildRequires:	qt-devel >= 2.3.0
BuildRequires:	zlib-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libpng-devel
Requires:	%{name}-collector
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
an openMosix-cluster management GUI

openMosixview - the main monitoring+admistration application
openMosixprocs - a process-box for managing processes
openMosixanalyzer - for analyzing the data collected by the openMosixcollector
openMosixhistory - a process-history for your cluster
openMosixmigmon - for monitoring process migration
3dmosmon - a 3d view for monitoring your cluster

%description -l pl
graficzny interfejs do zarządzania clustrem openMosix

openMosixview - główny program administracyjno/monitorujący
openMosixprocs - 
openMosixanalyzer - program analizujący dane zebrane przez openMosixcollector
openMosixhistory - program generujący historie procesów Twojego clustra
openMosixmigmon - program monitorujący migracje procesów
3dmosmon - program generujący trójwymiarowy widok Twojego clustra

%package collector
Summary:	collecting daemon which logs cluster+node informations
Summary(pl):	demon zbierający informacje z nodów
Group:		Applications/System
Requires(post,preun): /sbin/chkconfig

%description collector
openMosixcollector - collecting daemon which logs cluster+node informations

%description -l pl collector
openMosixcollector -  demon zbierający informacje z nodów

%prep
%setup -q

TOPDIR=`pwd`
TOOLZ="openmosixcollector openmosixanalyzer openmosixhistory openmosixprocs openmosixmigmon"

for i in ${TOOLZ}
do
	cd ${i}
	%configure2_13 
	cd ${TOPDIR}
done


%build
rm -rf $RPM_BUILD_ROOT

TOPDIR=`pwd`
TOOLZ="openmosixcollector openmosixanalyzer openmosixhistory openmosixprocs openmosixmigmon"
for i in ${TOOLZ}
do
        cd ${i}
	%{__make}
	cd ${TOPDIR}
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d/ \
	   $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

TOPDIR=`pwd`
TOOLZ="openmosixcollector openmosixanalyzer openmosixhistory openmosixprocs openmosixmigmon"
for i in ${TOOLZ}
do
        cd ${i}
	%{__make} DESTDIR=$RPM_BUILD_ROOT install
        cd ${TOPDIR}
	if [ ${i} != "openmosixcollector" ]
	then
		mv $RPM_BUILD_ROOT/usr/doc/${i} $RPM_BUILD_ROOT%{_docdir}/${i}
	fi
done

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openmosixcollector

%clean
rm -rf $RPM_BUILD_ROOT

%post collector
/sbin/chkconfig --add openmosixcollector
if [ -f /var/lock/subsys/openmosixcollector ]; then
        /etc/rc.d/init.d/openmosixcollector restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/openmosixcollector start\" to start openmosixcollector." 1>&2
fi

%preun collector
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/openmosixcollector ]; then
                /etc/rc.d/init.d/openmosixcollector stop 1>&2
        fi
        /sbin/chkconfig --del openmosixcollector
fi


%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog TODO 
%attr(755,root,root) %{_bindir}/openmosixanalyzer
%attr(755,root,root) %{_bindir}/openmosixhistory
%attr(755,root,root) %{_bindir}/openmosixmigmon
%attr(755,root,root) %{_bindir}/openmosixprocs
%{_docdir}/*/*.html

%files collector
%attr(755,root,root) %{_bindir}/openmosixcollector
%attr(755,root,root) /etc/rc.d/init.d/openmosixcollector
