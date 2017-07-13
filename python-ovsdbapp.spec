%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif


%global library ovsdbapp
%global module ovsdbapp

Name:       python-%{library}
Version:    XXX
Release:    XXX
Summary:    Python OVSDB Application Library
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    http://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

%package -n python2-%{library}
Summary:    Python OVSDB Application Library
Requires:   python-openvswitch
Requires:   python-pbr
%{?python_provide:%python_provide python2-%{library}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  git
BuildRequires:  python-mock
BuildRequires:  python-openvswitch
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository

%description -n python2-%{library}
A library for writing Open vSwitch OVSDB-based applications.


%package -n python2-%{library}-tests
Summary:   Python OVSDB Application Library Tests
Requires:  python2-%{library} = %{version}-%{release}
Requires:  python-mock
Requires:  python-oslotest
Requires:  python-testrepository

%description -n python2-%{library}-tests
Python OVSDB Application Library tests.

This package contains Python OVSDB Application Library test files.

# NOTE(twilson) the project needs documentation
#%package -n python-%{library}-doc
#Summary:    Python OVSDB Application Library documentation
#
#BuildRequires: python-sphinx
#BuildRequires: python-oslo-sphinx
#
#%description -n python-%{library}-doc
#Python OVSDB Application Library.
#
#This package contains the documentation.

%if 0%{?with_python3}
%package -n python3-%{library}
Summary:    Python OVSDB Application Library
Requires:   python3-openvswitch
Requires:   python3-pbr
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-openvswitch
BuildRequires:  python3-testrepository

%description -n python3-%{library}
Python OVSDB Application Library.


%package -n python3-%{library}-tests
Summary:    Python OVSDB Application Library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-mock
Requires:   python3-oslotest
Requires:   python3-testrepository

%description -n python3-%{library}-tests
Python OVSDB Application Library tests.

This package contains Python OVSDB Application Library test files.

%endif # with_python3


%description
Python OVSDB Application Library.


%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourselves
rm -f *requirements.txt

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
OS_TEST_PATH=./ovsdbapp/tests/unit %{__python3} setup.py test
rm -rf .testrepository
%endif
OS_TEST_PATH=./ovsdbapp/tests/unit %{__python2} setup.py test

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
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/ovsdbapp/commit/?id=6417850d893d19ce760d06dad9a3e65f3491ce8e
