%define major		2
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	An SSL library
Name:		polarssl
Version:	1.2.8
Release:	1
License:	GPLv2+
Group:		System/Libraries
Url:		http://polarssl.org
Source0:	http://polarssl.org/code/releases/%{name}-%{version}-gpl.tgz
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	pkcs11-helper-devel

%description
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains PolarSSL programs.

%files
%doc ChangeLog README
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

%prep
%setup -q

%build
%cmake \
	-DUSE_SHARED_POLARSSL_LIBRARY:BOOL=ON \
	-DUSE_PKCS11_HELPER_LIBRARY:BOOL=ON
%make
%make apidoc

%install
%makeinstall_std -C build

for file in benchmark md5sum sha1sum
do
	mv %{buildroot}%{_bindir}/${file} %{buildroot}%{_bindir}/${file}.polarssl
done

