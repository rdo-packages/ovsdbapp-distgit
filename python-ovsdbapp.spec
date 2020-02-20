# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library ovsdbapp
%global module ovsdbapp
%global with_doc 1

%global common_desc \
A library for writing Open vSwitch OVSDB-based applications.

%global common_desc_tests \
Python OVSDB Application Library tests. \
This package contains Python OVSDB Application Library test files.

Name:       python-%{library}
Version:    0.17.2
Release:    1%{?dist}
Summary:    Python OVSDB Application Library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python%{pyver}-%{library}
Summary:    Python OVSDB Application Library
%{?python_provide:%python_provide python%{pyver}-%{library}}
Requires:   python%{pyver}-openvswitch
Requires:   python%{pyver}-pbr
Requires:   python%{pyver}-six
Requires:   python%{pyver}-netaddr >= 0.7.18

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-openvswitch
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-netaddr >= 0.7.18
BuildRequires:  python%{pyver}-testrepository

%description -n python%{pyver}-%{library}
%{common_desc}


%package -n python%{pyver}-%{library}-tests
Summary:   Python OVSDB Application Library Tests
Requires:  python%{pyver}-%{library} = %{version}-%{release}
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-testrepository

%description -n python%{pyver}-%{library}-tests
%{common_desc_tests}

%if 0%{?with_doc}
%package -n python-%{library}-doc
Summary:    Python OVSDB Application Library documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme

%description -n python-%{library}-doc
%{common_desc}

This package contains the documentation.
%endif

%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourselves
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
PYTHON=%{pyver_bin} OS_TEST_PATH=./ovsdbapp/tests/unit stestr-%{pyver} run

%files -n python%{pyver}-%{library}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/%{module}-*.egg-info
%exclude %{pyver_sitelib}/%{module}/tests

%files -n python%{pyver}-%{library}-tests
%{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{library}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Wed Feb 19 2020 RDO <dev@lists.rdoproject.org> 0.17.2-1
- Update to 0.17.2

* Mon Dec 16 2019 RDO <dev@lists.rdoproject.org> 0.17.1-1
- Update to 0.17.1

* Fri Sep 20 2019 RDO <dev@lists.rdoproject.org> 0.17.0-1
- Update to 0.17.0

