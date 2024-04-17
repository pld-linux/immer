#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Postmodern immutable and persistent data structures for C++
Summary(pl.UTF-8):	Postmodernistyczne niezmienne i trwałe struktury danych dla C++
Name:		immer
Version:	0.8.1
Release:	1
License:	Boost v1.0
Group:		Libraries
#Source0Download: https://github.com/arximboldi/immer/releases
Source0:	https://github.com/arximboldi/immer/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	387ebc10056f015a9db13cb551c737a1
%define	theme_gitref	b5adfa2a6def8aa55d95dedc4e1bfde214a5e36c
Source1:	https://github.com/arximboldi/sinusoidal-sphinx-theme/archive/%{theme_gitref}/sinusoidal-sphinx-theme-%{theme_gitref}.tar.gz
# Source1-md5:	8873555af1d9f75d42a440fb1c60bd07
URL:		https://github.com/arximboldi/immer
BuildRequires:	boost-devel >= 1.56
BuildRequires:	cmake >= 3.5.1
BuildRequires:	gc-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
%{?with_apidocs:BuildRequires:	sphinx-pdg-3 >= 1.3}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# header-only library, but cmake files location is arch-dependent
%define		_enable_debug_packages	0

%description
Immer is a library of persistent and immutable data structures
written in C++. These enable whole new kinds of architectures for
interactive and concurrent programs of striking simplicity,
correctness, and performance.

%description -l pl.UTF-8
Immer to biblioteka trwałych i niezmiennych struktur danych napisana w
C++. Pozwalają one na nowe rodzaje architektury dla programów
interaktywnych i współbieżnych, odznaczające się prostotą,
poprawnością i wydajnością.

%package devel
Summary:	Postmodern immutable and persistent data structures for C++
Summary(pl.UTF-8):	Postmodernistyczne niezmienne i trwałe struktury danych dla C++
Group:		Development/Libraries
Requires:	libstdc++-devel >= 6:5

%description devel
immer is a library of persistent and immutable data structures
written in C++. These enable whole new kinds of architectures for
interactive and concurrent programs of striking simplicity,
correctness, and performance.

%description devel -l pl.UTF-8
immer to biblioteka trwałych i niezmiennych struktur danych napisana w
C++. Pozwalają one na nowe rodzaje architektury dla programów
interaktywnych i współbieżnych, odznaczające się prostotą,
poprawnością i wydajnością.

%package apidocs
Summary:	API documentation for Immer library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Immer
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Immer library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Immer.

%prep
%setup -q

tar xf %{SOURCE1} -C tools/sinusoidal-sphinx-theme --strip-components=1

%build
install -d build
cd build
%cmake .. \
	-Dimmer_BUILD_EXAMPLES=OFF \
	-Dimmer_BUILD_TESTS=OFF

%{__make}
cd ..

%if %{with apidocs}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE README.rst
%{_includedir}/immer
%{_libdir}/cmake/Immer

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{_static,*.html,*.js}
%endif
