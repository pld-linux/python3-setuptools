#
# Conditional build:
%bcond_with	apidocs		# Sphinx based documentation
%bcond_with	system_libs	# use system modules (appdirs, jaraco.text, packaging...) # TODO
%bcond_with	tests		# py.test tests (few failures)
%bcond_with	bootstrap	# no system modules, bootstrap egg-info without system setuptools

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
Version:	71.0.4
Release:	1.1
Epoch:		1
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/setuptools/
Source0:	https://files.pythonhosted.org/packages/source/s/setuptools/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	956e2402c95b2439c812808d006255cd
Patch0:		setuptools-missing.patch
Patch1:		multilib.patch
URL:		https://github.com/pypa/setuptools
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-modules >= 1:3.8
%{!?with_bootstrap:BuildRequires:	python3-setuptools >= 1:54}
%if %{with system_libs}
# versions from pkg_resources/_vendor/vendored.txt and setuptools/_vendor/vendored.txt
BuildRequires:	python3-importlib_metadata >= 6.0.0
BuildRequires:	python3-importlib_resources >= 5.10.2
BuildRequires:	python3-jaraco.text >= 3.7.0
BuildRequires:	python3-ordered-set >= 3.1.1
BuildRequires:	python3-platformdirs >= 2.6.2
BuildRequires:	python3-more_itertools >= 8.8.0
BuildRequires:	python3-packaging >= 23.1
BuildRequires:	python3-tomli >= 2.0.1
BuildRequires:	python3-typing_extensions >= 4.4.0
BuildRequires:	python3-zipp >= 3.7.0
%endif
BuildConflicts:	python3-distribute < 0.7
%if %{with tests}
BuildRequires:	python3-build
BuildRequires:	python3-coverage >= 4.5.1
BuildRequires:	python3-filelock >= 3.4.0
BuildRequires:	python3-importlib_metadata
BuildRequires:	python3-ini2toml >= 0.9
BuildRequires:	python3-jaraco.develop >= 7.21
BuildRequires:	python3-jaraco.envs >= 2.2
BuildRequires:	python3-jaraco.path >= 3.2.0
BuildRequires:	python3-mypy >= 1.9
BuildRequires:	python3-packaging >= 23.2
BuildRequires:	python3-pip >= 19.1
BuildRequires:	python3-pip_run >= 8.8
BuildRequires:	python3-pytest >= 6
BuildRequires:	python3-pytest-checkdocs >= 2.4
BuildRequires:	python3-pytest-cov >= 2.5.1
BuildRequires:	python3-pytest-enabler >= 2.2
BuildRequires:	python3-pytest-home
BuildRequires:	python3-pytest-mypy >= 0.9.1
BuildRequires:	python3-pytest-perf
BuildRequires:	python3-pytest-ruff >= 0.2.1
BuildRequires:	python3-pytest-timeout
BuildRequires:	python3-pytest-xdist >= 3
BuildRequires:	python3-virtualenv >= 13.0.0
BuildRequires:	python3-tomli
BuildRequires:	python3-tomli-w >= 1.0.0
BuildRequires:	python3-wheel
%endif
%if %{with apidocs}
BuildRequires:	python3-Sphinx >= 3.5
BuildRequires:	python3-Sphinx < 7.2.5
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco
BuildRequires:	python3-jaraco.packaging >= 9.3
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-pygments-github-lexers >= 0.0.5
BuildRequires:	python3-rst.linker >= 1.9
# specified but not required(?)
#BuildRequires:	python3-pygments-github-lexers >= 0.0.5
BuildRequires:	python3-setuptools >= 1:34
BuildRequires:	python3-sphinx-hoverxref
BuildRequires:	python3-sphinx-notfound-page >= 1
BuildRequires:	python3-sphinx-notfound-page < 2
BuildRequires:	python3-sphinx-reredirects
BuildRequires:	python3-sphinx_favicon
BuildRequires:	python3-sphinx_inline_tabs
BuildRequires:	python3-sphinxcontrib-towncrier
BuildRequires:	python3-tomli
%endif
%{!?with_bootstrap:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	unzip
Requires:	python3-modules >= 1:3.8
%if %{with system_libs}
# versions from pkg_resources/_vendor/vendored.txt and setuptools/_vendor/vendored.txt
Requires:	python3-importlib_metadata >= 6.0.0
Requires:	python3-importlib_resources >= 5.10.2
Requires:	python3-jaraco.text >= 3.7.0
Requires:	python3-ordered-set >= 3.1.1
Requires:	python3-platformdirs >= 2.6.2
Requires:	python3-more_itertools >= 8.8.0
Requires:	python3-packaging >= 23.1
Requires:	python3-tomli >= 2.0.1
Requires:	python3-typing_extensions >= 4.4.0
Requires:	python3-zipp >= 3.7.0
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
%patch -P 0 -p1
%patch -P 1 -p1

%if %{with system_libs}
exit 1 # TODO: unvendor modules from pkg_resources/_vendor
%endif

%build
%if %{with bootstrap}
%{__python3} setup.py egg_info
%endif

LC_ALL=C.UTF-8 \
%py3_build

%{?with_tests:%{__python3} -m pytest pkg_resources/tests setuptools/tests tests}

%if %{with apidocs}
cd docs
%{__python3} -m sphinx -W . build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install %{?with_bootstrap:--optimize=0}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst
%{py3_sitescriptdir}/_distutils_hack
%{py3_sitescriptdir}/distutils-precedence.pth
%{py3_sitescriptdir}/pkg_resources
%{py3_sitescriptdir}/setuptools
%{py3_sitescriptdir}/%{module}-%{version}*py*.egg-info

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,deprecated,development,references,userguide,*.html,*.js}
%endif
