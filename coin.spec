%define major 80
%define libname %mklibname %name %major
%define libnamedev %mklibname %name -d
%define lib_name_orig libcoin

Summary:	Implementation of the Open Inventor API
Name:		coin
Version:	4.0.0
Release:	1
Source0:	https://github.com/coin3d/coin/releases/download/Coin-%{version}/coin-%{version}-src.tar.gz
License:	GPLv2
Group:		System/Libraries
URL:		http://coin3d.github.io/
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	boost-devel
BuildRequires:	cmake ninja
Patch0:		coin-fix-underlinking.patch

%description 
Coin is an implementation of the Open Inventor API, fully backwards
compatible with SGI Open Inventor v2.1, and incorporating many new
features.

Coin is portable across Win32, Linux, SGI IRIX, Mac OS X, HP-UX, Sun
Solaris, IBM AIX, and other platforms.

%package -n %{libname}
Summary:	Main library for Coin
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with Coin.

%package -n %{libnamedev}
Summary:	Headers for developing programs that will use Coin
Group:		Development/C++
Requires:	%{libname} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}coin40-devel
Obsoletes:	%{_lib}coin60-devel

%description -n %{libnamedev}
This package contains the headers that programmers will need to develop
applications which will use Coin.

%prep
%autosetup -p1 -n coin
%cmake -G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/*.so.%{version}

%files -n %{libnamedev}
%doc README FAQ AUTHORS NEWS RELNOTES THANKS
%{_bindir}/coin-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/Coin.pc
%{_includedir}/*
%{_datadir}/Coin
%{_libdir}/cmake/Coin-4.0.0
%{_infodir}/Coin4
