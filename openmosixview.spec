Summary:	openMosixview is a cluster-management GUI
Summary(pl):	openMosixview to graficzny interfejs do zarz±dzania clustrem
Name:		openmosixview
Version:	1.4
Release:	0.2
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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
an openMosix-cluster management GUI

openMosixview - the main monitoring+admistration application
openMosixprocs - a process-box for managing processes
openMosixcollector - collecting daemon which logs cluster+node informations
openMosixanalyzer - for analyzing the data collected by the openMosixcollector
openMosixhistory - a process-history for your cluster
openMosixmigmon - for monitoring process migration
3dmosmon - a 3d view for monitoring your cluster

%description -l pl
graficzny interfejs do zarz±dzania clustrem openMosix

openMosixview - g³ówny program administracyjno/monitoruj±cy
openMosixprocs - 
openMosixcollector -  demon zbieraj±cy informacje z nodów
openMosixanalyzer - program analizuj±cy dane zebrane przez openMosixcollector
openMosixhistory - program generuj±cy historie procesów Twojego clustra
openMosixmigmon - program monitoruj±cy migracje procesów
3dmosmon - program generuj±cy trójwymiarowy widok Twojego clustra


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

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d/

TOPDIR=`pwd`
TOOLZ="openmosixcollector openmosixanalyzer openmosixhistory openmosixprocs openmosixmigmon"
for i in ${TOOLZ}
do
        cd ${i}
	%{__make} DESTDIR=$RPM_BUILD_ROOT install
        cd ${TOPDIR}
done

install %{SOURCE1} /etc/rc.d/init.d/openmosixcollector

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/chkconfig --add openmosixcollector
if [ -f /var/lock/subsys/openmosixcollector ]; then
        /etc/rc.d/init.d/openmosixcollector restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/openmosixcollector start\" to start openmosixcollector." 1>&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/openmosixcollector ]; then
                /etc/rc.d/init.d/openmosixcollector stop 1>&2
        fi
        /sbin/chkconfig --del openmosixcollector
fi


%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /etc/rc.d/init.d/openmosixcollector
