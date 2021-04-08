#
# Conditional build:
%bcond_without	apidocs		# Sphinx based documentation
%bcond_with	system_libs	# use system modules (appdirs, packaging, pyparsing, six) # TODO
%bcond_with	tests		# py.test tests (few failures)
%bcond_with	bootstrap	# convenience alias for without: apidocs,system_libs,tests

%if %{with bootstrap}
%undefine	with_apidocs
%undefine	with_system_libs
%undefine	with_tests
%endif

%define		module		setuptools
%define		pypi_name	setuptools
Summary:	A collection of enhancements to the Python distutils
Summary(pl.UTF-8):	Zestaw rozszerzeń dla pythonowych distutils
Name:		python3-setuptools
Version:	54.2.0
Release:	1
Epoch:		1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/setuptools/
Source0:	https://files.pythonhosted.org/packages/source/s/setuptools/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	09f693b5d5ca8bf4fdb1da82f8110a9c
URL:		https://github.com/pypa/setuptools
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-modules >= 1:3.4
%if %{with system_libs}
# versions from pkg_resources/_vendor/vendored.txt
BuildRequires:	python3-appdirs >= 1.4.3
BuildRequires:	python3-packaging >= 19.2
BuildRequires:	python3-pyparsing >= 2.2.1
BuildRequires:	python3-six >= 1.10.0
%endif
BuildConflicts:	python3-distribute < 0.7
%if %{with tests}
BuildRequires:	python3-coverage >= 4.5.1
# FIXME: patch to use unittest.mock
#BuildRequires:	python3-mock
%if "%{py3_ver}" >= "3.6"
BuildRequires:	python3-paver
%endif
BuildRequires:	python3-pip >= 19.1
BuildRequires:	python3-pytest >= 3.7
BuildRequires:	python3-pytest-cov >= 2.5.1
BuildRequires:	python3-pytest-fixture-config
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-pytest-virtualenv >= 1.2.7
BuildRequires:	python3-virtualenv >= 13.0.0
BuildRequires:	python3-wheel
%endif
%if %{with apidocs}
BuildRequires:	python3-jaraco
BuildRequires:	python3-jaraco.packaging >= 6.1
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	python3-setuptools >= 34
BuildRequires:	python3-tox
BuildRequires:	sphinx-pdg-3 >= 1.4
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
Requires:	python3-modules
%if %{with system_libs}
# versions from pkg_resources/_vendor/vendored.txt
Requires:	python3-appdirs >= 1.4.0
Requires:	python3-packaging >= 16.8
Requires:	python3-pyparsing >= 2.1.10
Requires:	python3-six >= 1.10.0
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
setuptools is a collection of enhancements to the Python distutils
that allow you to more easily build and distribute Python 2.x
packages, especially ones that have dependencies on other packages.

%description -l pl.UTF-8
setuptools to zestaw rozszerzeń do pythonowych distutils umożliwiający
łatwiejsze budowanie i rozprowadzanie pakietów Pythona 2.x,
szczególnie tych mających zależności od innych pakietów.

Ten pakiet zawiera składniki uruchomieniowe setuptools, potrzebne do
uruchamiania kodu wymagającego pkg_resources.py, przeznaczone dla
Pythona 2.x.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%if %{with system_libs}
exit 1 # TODO: unvendor modules from pkg_resources/_vendor
%endif

%build
LC_ALL=C.UTF-8 \
%py3_build

%{?with_tests:%{__python3} -m pytest pkg_resources/tests setuptools/tests tests}

%if %{with apidocs}
%{_bindir}/tox -e docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}//distutils-precedence.pth
%{py3_sitescriptdir}/_distutils_hack
%{py3_sitescriptdir}/pkg_resources
%{py3_sitescriptdir}/setuptools
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
