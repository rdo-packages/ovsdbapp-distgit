%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library ovsdbapp
%global module ovsdbapp

%global common_desc \
A library for writing Open vSwitch OVSDB-based applications.

%global common_desc_tests \
Python OVSDB Application Library tests. \
This package contains Python OVSDB Application Library test files.

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    Python OVSDB Application Library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python2-%{library}
Summary:    Python OVSDB Application Library
Requires:   python2-fixtures
Requires:   python2-openvswitch
Requires:   python2-pbr
Requires:   python2-six
Requires:   python2-oslo-utils >= 3.33.0
%if 0%{?fedora} > 0
Requires:   python2-netaddr
%else
Requires:   python-netaddr
%endif
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-mock
BuildRequires:  python2-openvswitch
BuildRequires:  python2-oslotest
BuildRequires:  python2-stestr
%if 0%{?fedora} > 0
BuildRequires:  python2-netaddr
BuildRequires:  python2-testrepository
%else
BuildRequires:  python-netaddr
BuildRequires:  python-testrepository
%endif

%description -n python2-%{library}
%{common_desc}


%package -n python2-%{library}-tests
Summary:   Python OVSDB Application Library Tests
Requires:  python2-%{library} = %{version}-%{release}
Requires:  python2-mock
Requires:  python2-oslotest
%if 0%{?fedora} > 0
Requires:  python2-testrepository
%else
Requires:  python-testrepository
%endif

%description -n python2-%{library}-tests
%{common_desc_tests}

# NOTE(twilson) the project needs documentation
#%package -n python-%{library}-doc
#Summary:    Python OVSDB Application Library documentation
#
#BuildRequires: python2-sphinx
#BuildRequires: python2-oslo-sphinx
#
#%description -n python-%{library}-doc
#Python OVSDB Application Library.
#
#This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    Python OVSDB Application Library
Requires:   python3-fixtures
Requires:   python3-netaddr
Requires:   python3-openvswitch
Requires:   python3-pbr
Requires:   python3-six
Requires:   python3-oslo-utils >= 3.33.0
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-mock
BuildRequires:  python3-netaddr
BuildRequires:  python3-oslotest
BuildRequires:  python3-openvswitch
BuildRequires:  python3-stestr
BuildRequires:  python3-testrepository

%description -n python3-%{library}
%{common_desc}


%package -n python3-%{library}-tests
Summary:    Python OVSDB Application Library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-mock
Requires:   python3-oslotest
Requires:   python3-testrepository
Requires:   python3-stestr

%description -n python3-%{library}-tests
%{common_desc_tests}

%endif # with_python3


%description
%{common_desc}


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourselves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
#%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
#rm -rf html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%if 0%{?with_python3}
OS_TEST_PATH=./ovsdbapp/tests/unit stestr-3 run
rm -rf .testrepository
%endif
OS_TEST_PATH=./ovsdbapp/tests/unit stestr-3 run

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files -n python2-%{library}-tests
%{python2_sitelib}/%{module}/tests

#%files -n python-%{library}-doc
#%license LICENSE
#%doc html README.rst

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-*.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{library}-tests
%{python3_sitelib}/%{module}/tests
%endif # with_python3

%changelog
