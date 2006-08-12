# TODO:	1). fix 3dmon and put it in separate subpackage.
#	2). test all.

Summary:	openMosixview - a cluster-management GUI
Summary(pl):	openMosixview - graficzny interfejs do zarz±dzania klastrem
Name:		openmosixview
Version:	1.5
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://www.openmosixview.com/download/%{name}-%{version}.tar.gz
Source1:	openmosixcollector.init
Patch0:		%{name}-Makefiles_FLAGS.patch
URL:		http://www.openmosixview.com/
BuildRequires:	qt-devel >= 2.3.0
Requires:	%{name}-collector
Requires:	kernel-mosix >= 2.4.22-1
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
Summary:	Collecting daemon which logs cluster+node informations
Summary(pl):	Demon zbieraj±cy informacje z nodów
Group:		Applications/System
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description collector
openMosixcollector - collecting daemon which logs cluster+node
information.

%description collector -l pl
openMosixcollector - demon zbieraj±cy informacje z wêz³ów.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcflags}"

#%%cd 3dmon/
#%%./setup.standalone

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_bindir},%{_docdir}/%{name}-%{version}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openmosixcollector
install openmosixcollector/openmosixcollector $RPM_BUILD_ROOT%{_bindir}

install openmosixview/openmosixview $RPM_BUILD_ROOT%{_bindir}
install openmosixanalyzer/openmosixanalyzer $RPM_BUILD_ROOT%{_bindir}
install openmosixhistory/openmosixhistory $RPM_BUILD_ROOT%{_bindir}
install openmosixprocs/openmosixprocs $RPM_BUILD_ROOT%{_bindir}
install openmosixmigmon/openmosixmigmon $RPM_BUILD_ROOT%{_bindir}
install openmosixpidlog/openmosixpidlog $RPM_BUILD_ROOT%{_bindir}
#%%install 3dmon/3dmosmon/3dmosmon $RPM_BUILD_ROOT%{_bindir}
#%%install 3dmon/mosstatd/mosstatd $RPM_BUILD_ROOT%{_bindir}
#%%install /etc/init.d/mosstatd $RPM_BUILD_ROOT/etc/init.d


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
%doc AUTHORS README TODO docs/*
%attr(755,root,root) %{_bindir}/openmosixview
%attr(755,root,root) %{_bindir}/openmosixanalyzer
%attr(755,root,root) %{_bindir}/openmosixhistory
%attr(755,root,root) %{_bindir}/openmosixprocs
%attr(755,root,root) %{_bindir}/openmosixmigmon
%attr(755,root,root) %{_bindir}/openmosixpidlog
#%%attr(755,root,root) %{_bindir}/3dmosmon
#%%attr(755,root,root) %{_bindir}/mosstatd


%files collector
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/openmosixcollector
%attr(754,root,root) /etc/rc.d/init.d/openmosixcollector
