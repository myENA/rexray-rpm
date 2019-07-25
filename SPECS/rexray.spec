## package settings
%define debug_package  %{nil}

Name:           rexray
Version:        0.11.4
Release:        0%{?dist}
Summary:        REX-Ray - Openly serious about storage

Group:          System Environment/Daemons
License:        Apache License, version 2.0
URL:            https://www.rexray.io

Source0:        https://dl.bintray.com/%{name}/%{name}/stable/%{version}/%{name}-Linux-x86_64-%{version}.tar.gz
Source2:        %{name}.service
Source3:        %{name}.sysconfig
Source4:        config.yml

BuildRequires:  systemd-units

Requires(pre):      shadow-utils
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
REX-Ray is the leading container storage orchestration engine
enabling persistence for cloud native workloads.

%package config
Summary:    Configuration files for %{name}
Group:      System Environment/Daemons
Requires:   rexray

%description config
Example configuration for %{name}.

%prep
%setup -q -c

%build

%install
## directories
%{__install} -d -m 0750 %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d -m 0750 %{buildroot}%{_sysconfdir}/%{name}/tls
%{__install} -d -m 0750 %{buildroot}%{_localstatedir}/lib/%{name}
%{__install} -d -m 0750 %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -d -m 0750 %{buildroot}%{_localstatedir}/run/%{name}


## sytem files and config
%{__install} -p -D -m 0640 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0640 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -p -D -m 0640 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}/config.yml

## main binary
%{__install} -p -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}

%pre

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root,-)
%{_unitdir}/%{name}.service
%{_bindir}/%{name}
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/log/%{name}
%dir %{_localstatedir}/run/%{name}

%files config
%defattr(0644,root,root,0755)
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/tls
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.yml

%changelog
