%define major 60
%define libname %mklibname %name %major
%define libnamedev %mklibname %name -d
%define lib_name_orig libcoin
%define _disable_rebuild_configure %nil
%define	debug_package %nil

Summary:	Implementation of the Open Inventor API
Name:		coin
Version:	3.1.3
Release:	5
Source0:	http://ftp.coin3d.org/coin/src/all/Coin-%{version}.tar.gz
License:	GPLv2
Group:		System/Libraries
URL:		http://www.coin3d.org/
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(gl)
Patch0:		coin-3.1.3-missing-header.patch
Patch1:		clang.patch
Patch2:		coin-3.1.3-freetype251.patch

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

%description -n %{libnamedev}
This package contains the headers that programmers will need to develop
applications which will use Coin.

%prep
%setup -q -n Coin-%{version}
for file in AUTHORS THANKS
do
iconv -f ISO-8859-1 -t UTF-8 "$file" > "${file}.new"
mv "${file}.new" "$file"
done
%apply_patches

# fix prefix in coin-config
sed -i '/^prefix/c prefix="/usr/"' bin/coin-config

# fix compilation
sed -i '/^#include "fonts\/freetype.h"$/i #include <cstdlib>\n#include <cmath>' src/fonts/freetype.cpp

# fix http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=667139
sed -i '/^#include <Inventor\/C\/basic.h>$/i #include <Inventor/C/errors/debugerror.h>' include/Inventor/SbBasic.h

%build
CFLAGS="%{optflags} -DCOIN_INTERNAL"
CXXFLAGS="%{optflags} -DCOIN_INTERNAL"
export CC=gcc
export CXX=g++
%configure --enable-system-expat
%make

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{libnamedev}
%doc README FAQ AUTHORS NEWS RELNOTES THANKS
%{_bindir}/coin-config
%{_libdir}/*.so
%{_libdir}/pkgconfig/Coin.pc
%{_includedir}/*
%{_datadir}/Coin
%_datadir/aclocal
%{_mandir}/man1/*
