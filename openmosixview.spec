Summary:	openMosixview - a cluster-management GUI
Summary(pl):	openMosixview - graficzny interfejs do zarz±dzania klastrem
Name:		openmosixview
Version:	1.4
Release:	2
Group:		Applications/System
License:	GPL
Vendor:		Matt Rechenburg <mosixview@t-online.de>
Source0:	http://www.openmosixview.com/download/%{name}-%{version}.tar.gz
# Source0-md5:	2e8fe16860cc9581194bf14bb4896b1d
Source1:	openmosixcollector.init
Patch0:		%{name}-mosix.patch
URL:		http://www.openmosixview.com/
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	qt-devel >= 2.3.0
BuildRequires:	zlib-devel
Requires:	kernel-mosix
Requires:	%{name}-collector
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An openMosix-cluster management GUI.

openMosixview - the main monitoring+admistration application
openMosixprocs - a process-box for managing processes
openMosixanalyzer - for analyzing the data collected by the openMosixcollector
openMosixhistory - a process-history for your cluster
openMosixmigmon - for monitoring process migration
3dmosmon - a 3d view for monitoring your cluster

%description -l pl
Graficzny interfejs do zarz±dzania klastrem openMosix.

openMosixview - g³ówny program administracyjno-monitoruj±cy
openMosixprocs - narzêdzie do zarz±dzania procesami
openMosixanalyzer - program analizuj±cy dane zebrane przez openMosixcollector
openMosixhistory - program generuj±cy historiê procesów klastra
openMosixmigmon - program monitoruj±cy migracjê procesów
3dmosmon - program generuj±cy trójwymiarowy widok klastra

%package collector
Summary:	collecting daemon which logs cluster+node informations
Summary(pl):	demon zbieraj±cy informacje z nodów
Group:		Applications/System
PreReq:		rc-scripts
Requires(post,preun): /sbin/chkconfig

%description collector
openMosixcollector - collecting daemon which logs cluster+node
information.

%description -l pl collector
openMosixcollector -  demon zbieraj±cy informacje z wêz³ów.

%prep
%setup -q

%patch -p1

%build
TOPDIR=`pwd`
TOOLZ="openmosixcollector openmosixanalyzer openmosixhistory openmosixprocs openmosixmigmon 3dmon"

for i in ${TOOLZ}
do
	cd ${i}
	%configure2_13 
	cd ${TOPDIR}
done

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
TOOLZ="openmosixcollector openmosixanalyzer openmosixhistory openmosixprocs openmosixmigmon 3dmon"
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
