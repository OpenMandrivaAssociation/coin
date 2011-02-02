%define name coin
%define version 2.4.6
%define release %mkrel 7

%define major   40
%define libname %mklibname %name %major
%define libnamedev %mklibname %name -d
%define lib_name_orig libcoin

Summary: Implementation of the Open Inventor API
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ftp.coin3d.org/coin/src/all/Coin-%{version}.tar.gz
License: GPL
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
URL: http://www.coin3d.org/
BuildRequires: libx11-devel
BuildRequires: mesagl-devel

%description 
Coin is an implementation of the Open Inventor API, fully backwards
compatible with SGI Open Inventor v2.1, and incorporating many new
features.

Coin is portable across Win32, Linux, SGI IRIX, Mac OS X, HP-UX, Sun
Solaris, IBM AIX, and other platforms.

%package -n %{libname}
Summary: Main library for Coin
Group: System/Libraries
Provides: %{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with Coin.

%package -n %{libnamedev}
Summary: Headers for developing programs that will use Coin
Group: Development/C++
Requires: %{libname} = %{version}
Provides: %{lib_name_orig}-devel = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %{_lib}coin40-devel

%description -n %{libnamedev}
This package contains the headers that programmers will need to develop
applications which will use Coin.

%prep
%setup -q -n Coin-%{version}

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{libname}
%defattr(-,root,root,0755)
%{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root,0755)
%doc README FAQ AUTHORS NEWS RELNOTES THANKS
%{_bindir}/coin-config
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_datadir}/Coin
%_datadir/aclocal
%{_mandir}/man1/*
