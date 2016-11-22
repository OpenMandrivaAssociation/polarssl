%define major	7
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Summary:	An SSL library
Name:		polarssl
Version:	1.3.9
Release:	0
License:	GPLv2+
Group:		System/Libraries
Url:		https://polarssl.org
Source0:	https://polarssl.org/code/releases/%{name}-%{version}-gpl.tgz

BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libpkcs11-helper-1)
BuildRequires:	pkgconfig(zlib)

%description
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains PolarSSL programs.

%files
%{_bindir}/*
%doc README.rst
%doc ChangeLog
%doc LICENSE

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
%{_libdir}/lib%{name}.so.*
%doc LICENSE

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
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%doc apidoc
%doc LICENSE

#----------------------------------------------------------------------------

%prep
%setup -q

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
	-DCMAKE_BUILD_TYPE:STRING="Release" \
	-DUSE_SHARED_POLARSSL_LIBRARY:BOOL=ON \
	-DUSE_STATIC_POLARSSL_LIBRARY:BOOL=OFF \
	-DENABLE_PROGRAMS:BOOL=ON \
	-DENABLE_TESTING:BOOL=ON \
	-DENABLE_ZLIB_SUPPORT:BOOL=ON \
	-DUSE_PKCS11_HELPER_LIBRARY:BOOL=ON \
	-DLINK_WITH_PTHREAD:BOOL=ON
%make

# doc
%make apidoc

%install
%makeinstall_std -C build

# fix files name
for file in benchmark md5sum sha1sum
do
	mv %{buildroot}%{_bindir}/${file} %{buildroot}%{_bindir}/${file}.polarssl
done

%check
# tests
LD_LIBRARY_PATH=%{buildroot}%{_libdir} %make -C build test

