%define major 80
%define oldlibname %mklibname %name 80
%define libname %mklibname %name
%define libnamedev %mklibname %name -d
%define lib_name_orig libcoin

Summary:	Implementation of the Open Inventor API
Name:		coin
Version:	4.0.3
Release:	1
Source0:	https://github.com/coin3d/coin/releases/download/v%{version}/coin-%{version}-src.tar.gz
License:	GPLv2
Group:		System/Libraries
URL:		http://coin3d.github.io/
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	boost-devel
BuildRequires:	cmake ninja
BuildRequires:	doxygen
Patch0:		coin-fix-underlinking.patch
# Avoid cmake(superglu) dependency in -devel
Patch1:		coin-4.0.0-no-superglu-dependency.patch

%description 
Coin is an implementation of the Open Inventor API, fully backwards
compatible with SGI Open Inventor v2.1, and incorporating many new
features.

Coin is portable across Win32, Linux, SGI IRIX, Mac OS X, HP-UX, Sun
Solaris, IBM AIX, and other platforms.

#--------------------------------------------------------------------

%package -n %{libname}
Summary:	Main library for Coin
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
%rename %{oldlibname}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with Coin.

%files -n %{libname}
%{_libdir}/*.so.%{major}*

#--------------------------------------------------------------------

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

%files -n %{libnamedev}
%doc FAQ AUTHORS NEWS RELNOTES THANKS
%{_bindir}/coin-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/Coin.pc
%{_includedir}/*
%{_datadir}/Coin
%{_libdir}/cmake/Coin-%{version}

#--------------------------------------------------------------------

# (mandian) NOTE: coin-doc package is required by FreCAD
%package doc
Summary:	HTML developer documentation for Coin

%description doc
%{summary}.

%files doc
%{_docdir}/Coin/html/

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n coin

# Update doxygen configuration
doxygen -u docs/coin.doxygen.in

%cmake \
	-DCOIN_BUILD_DOCUMENTATION=TRUE \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
