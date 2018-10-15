%define		cairo_ver	1.10.0
%define		qt4_ver		4.7.0
Summary:	PDF rendering library
Summary(pl.UTF-8):	Biblioteka renderująca PDF
Name:		poppler0.61
Version:	0.61.0
Release:	2
License:	GPL v2+
Group:		Libraries
Source0:	https://poppler.freedesktop.org/poppler-%{version}.tar.xz
# Source0-md5:	9feff3fb5e2302bb915e9a55da182c57
Patch0:		%{name}-gtkdocdir.patch
URL:		https://poppler.freedesktop.org/
BuildRequires:	QtCore-devel >= %{qt4_ver}
BuildRequires:	QtGui-devel >= %{qt4_ver}
BuildRequires:	QtTest-devel >= %{qt4_ver}
BuildRequires:	QtXml-devel >= %{qt4_ver}
BuildRequires:	cairo-devel >= %{cairo_ver}
BuildRequires:	cmake >= 3.1.0
BuildRequires:	curl-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	fontconfig-devel >= 2.0.0
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	gettext-tools
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtiff-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	nss-devel >= 3
BuildRequires:	openjpeg2-devel >= 2
BuildRequires:	pkgconfig >= 1:0.18
# wanted cairo backends
BuildRequires:	pkgconfig(cairo-pdf) >= %{cairo_ver}
BuildRequires:	pkgconfig(cairo-ps) >= %{cairo_ver}
BuildRequires:	pkgconfig(cairo-svg) >= %{cairo_ver}
%{?with_qt5:BuildRequires:	qt5-build >= %{qt5_ver}}
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	which
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	openjpeg2 >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A common PDF rendering library for integrating PDF viewing into
desktop applications (based on the xpdf-3.0 code base).

Minimal compatibility package to support legacy applications which
still require Qt4 API.

%description -l pl.UTF-8
Wspólna biblioteka renderująca PDF do integrowania oglądania PDF w
aplikacjach desktopowych (oparta na kodzie xpdf-3.0).

Mały pakiet zapewniający wsparcie dla starszych aplikacji które wciąż
wymagają API Qt4.

%package devel
Summary:	Poppler header files
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Poppler
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel
Requires:	lcms2-devel >= 2
Requires:	libstdc++-devel >= 6:4.7
Requires:	nss-devel >= 3
Conflicts:	poppler-devel

%description devel
Header files for the Poppler library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Poppler.

%package qt4
Summary:	Qt4 wrapper for poppler
Summary(pl.UTF-8):	Wrapper Qt4 dla popplera
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	QtCore >= %{qt4_ver}
Requires:	QtGui >= %{qt4_ver}
Requires:	QtXml >= %{qt4_ver}
Provides:	poppler-Qt = %{version}-%{release}
Provides:	poppler-qt4 = %{version}-%{release}
Obsoletes:	poppler-Qt < 0.24.4-2
Obsoletes:	poppler-qt
Obsoletes:	poppler-qt4 < 0.61.0

%description qt4
Qt4 wrapper for poppler.

%description qt4 -l pl.UTF-8
Wrapper Qt4 dla popplera.

%package qt4-devel
Summary:	Header files for Qt4 wrapper for poppler
Summary(pl.UTF-8):	Pliki nagłówkowe wrappera Qt4 dla popplera
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-qt4 = %{version}-%{release}
Requires:	QtCore-devel >= %{qt4_ver}
Requires:	QtGui-devel >= %{qt4_ver}
Requires:	QtXml-devel >= %{qt4_ver}
Provides:	poppler-Qt-devel = %{version}-%{release}
Provides:	poppler-qt4-devel = %{version}-%{release}
Obsoletes:	poppler-Qt-devel < 0.24.4-2
Obsoletes:	poppler-qt-devel
Obsoletes:	poppler-qt4-devel < 0.61.0

%description qt4-devel
Header files for Qt4 wrapper for poppler.

%description qt4-devel -l pl.UTF-8
Pliki nagłówkowe wrapper Qt4 dla popplera.

%prep
%setup -q -n poppler-%{version}
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DENABLE_GTK_TESTS=OFF \
	-DENABLE_LIBCURL=ON \
	-DENABLE_GTK_DOC=OFF \
	-DWITH_CAIRO=ON \
	-DENABLE_CPP=OFF \
	-DENABLE_GLIB=OFF \
	-DENABLE_QT4=ON \
	-DENABLE_QT5=OFF \
	-DENABLE_UTILS=OFF \
	-DENABLE_XPDF_HEADERS=ON \
	-DENABLE_ZLIB=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	qt4 -p /sbin/ldconfig
%postun	qt4 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README*
%attr(755,root,root) %{_libdir}/libpoppler.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpoppler.so.72

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpoppler.so
%dir %{_includedir}/poppler
%{_includedir}/poppler/poppler-config.h
%{_includedir}/poppler/[ABCDEFGHJLMNOPRSTUVX]*.h
%{_includedir}/poppler/fofi
%{_includedir}/poppler/goo
%{_includedir}/poppler/splash
%{_pkgconfigdir}/poppler.pc
%{_pkgconfigdir}/poppler-cairo.pc
%{_pkgconfigdir}/poppler-splash.pc

%files qt4
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpoppler-qt4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpoppler-qt4.so.4

%files qt4-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpoppler-qt4.so
%{_includedir}/poppler/qt4
%{_pkgconfigdir}/poppler-qt4.pc
