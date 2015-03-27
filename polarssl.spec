%define major	5
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d
%define static	%mklibname %{name} -s

Summary:	An SSL library
Name:		polarssl
Version:	1.3.9
Release:	1
License:	GPLv2+
Group:		System/Libraries
Url:		http://polarssl.org
Source0:	http://polarssl.org/code/releases/polarssl-1.3.9-gpl.tgz
Patch1:		polarssl-1.3.4-static.patch
Patch2:		polarssl-1.3.4-cflags.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpkcs11-helper-1)

%description
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains PolarSSL programs.

%files
%doc ChangeLog
%{_bindir}/*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	PolarSSL library
Group:		System/Libraries

%description -n %{libname}
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains the library itself.

%files -n %{libname}
%{_libdir}/libpolarssl.so.%{major}*
%{_libdir}/libpolarssl.so.%{version}

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	PolarSSL development files
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	polarssl-devel = %{EVRD}

%description -n %{devname}
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains development files.

%files -n %{devname}
%doc apidoc
%{_libdir}/libpolarssl.so
%{_includedir}/polarssl

#----------------------------------------------------------------------------
%package -n %{static}
Summary:	PolarSSL development files
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	polarssl-static-devel = %{EVRD}

%description -n %{static}
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains development files.

%files -n %{static}
%{_libdir}/libpolarssl.a

%prep
%setup -q
%apply_patches

enable_polarssl_option() {
    local myopt="$@"
    # check that config.h syntax is the same at version bump
    sed -i \
        -e "s://#define ${myopt}:#define ${myopt}:" \
        include/polarssl/config.h || die
}

enable_polarssl_option POLARSSL_ZLIB_SUPPORT
enable_polarssl_option POLARSSL_HAVEGE_C

%build

%cmake \
	-DUSE_SHARED_POLARSSL_LIBRARY=ON \
	-DENABLE_ZLIB_SUPPORT=ON \
	-DUSE_PKCS11_HELPER_LIBRARY=ON
%make
%make apidoc

%check
LD_LIBRARY_PATH=$PWD/library ctest --output-on-failure -V

%install
%makeinstall_std -C build

for file in benchmark md5sum sha1sum
do
	mv %{buildroot}%{_bindir}/${file} %{buildroot}%{_bindir}/${file}.polarssl
done
