%define major		1
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

Name:		polarssl
Summary:	An SSL library
Version:	1.1.4
Release:	1
License:	GPLv2+
Group:		System/Libraries
URL:		http://polarssl.org
Source0:	http://polarssl.org/code/releases/%{name}-%{version}-gpl.tgz
BuildRequires:	cmake
BuildRequires:	doxygen

%description
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains PolarSSL programs.

%package -n %{libname}
Summary:	PolarSSL library
Group:		System/Libraries

%description -n %{libname}
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains the library itself.

%package -n %{develname}
Summary:	PolarSSL development files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	polarssl-devel

%description -n %{develname}
PolarSSL is an SSL library written in ANSI C. PolarSSL makes it easy
for developers to include cryptographic and SSL/TLS capabilities in their
(embedded) products with as little hassle as possible. It is designed to be
readable, documented, tested, loosely coupled and portable.

This package contains development files.

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

%files
%doc ChangeLog README
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libpolarssl.so.%{major}*

%files -n %{develname}
%doc apidoc
%{_libdir}/libpolarssl.so
%{_includedir}/polarssl
