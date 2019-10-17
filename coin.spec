%define major 60
%define libname %mklibname %name %major
%define libnamedev %mklibname %name -d
%define lib_name_orig libcoin
%define _disable_rebuild_configure %nil
%define	debug_package %nil

%global libopenal_SONAME libopenal.so.1
%global libsimage_SONAME libsimage.so.2


Summary:	Implementation of the Open Inventor API
Name:		coin
Version:	3.1.3
Release:	7
Source0:	http://ftp.coin3d.org/coin/src/all/Coin-%{version}.tar.gz
License:	GPLv2
Group:		System/Libraries
URL:		http://www.coin3d.org/
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(gl)
BuildRequires:	boost-devel
Patch0:		clang.patch
Patch1:		0001-simage-soname.patch
Patch2:		0002-openal-soname.patch
Patch3:		0003-man3.patch
Patch4:		0004-doxygen.patch
Patch5:		0005-gcc-4.7.patch
Patch6:		0006-inttypes.patch
Patch7:		0007-Convert-to-utf-8.patch
Patch8:		0008-Convert-to-utf-8.patch
Patch9:		0009-Convert-to-utf-8.patch
Patch10:	0010-GCC-4.8.0-fixes.patch
Patch11:	0011-Fix-SoCamera-manpage.patch
Patch12:	0012-memhandler-initialization.patch
Patch13:	0013-Use-NULL-instead-of-0.patch
Patch14:	patch-hg-11603.patch


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
#for file in AUTHORS THANKS
#do
#iconv -f ISO-8859-1 -t UTF-8 "$file" > "${file}.new"
#mv "${file}.new" "$file"
#done
%apply_patches

# fix prefix in coin-config
sed -i '/^prefix/c prefix="/usr/"' bin/coin-config

# fix compilation
sed -i '/^#include "fonts\/freetype.h"$/i #include <cstdlib>\n#include <cmath>' src/fonts/freetype.cpp

# fix http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=667139
sed -i '/^#include <Inventor\/C\/basic.h>$/i #include <Inventor/C/errors/debugerror.h>' include/Inventor/SbBasic.h

find . \( -name '*.h' -o -name '*.cpp' -o -name '*.c' \) -a -executable -exec chmod -x {} \;

sed -i -e 's,@LIBSIMAGE_SONAME@,"%{libsimage_SONAME}",' \
  src/glue/simage_wrapper.cpp
sed -i -e 's,@LIBOPENAL_SONAME@,"%{libopenal_SONAME}",' \
  src/glue/openal_wrapper.cpp

# get rid of bundled boost headers
rm -rf include/boost

%build
CFLAGS="%{optflags} -DCOIN_INTERNAL"
CXXFLAGS="%{optflags} -DCOIN_INTERNAL"
#export CC=gcc
#export CXX=g++
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
