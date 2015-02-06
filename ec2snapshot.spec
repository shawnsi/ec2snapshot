Name:           ec2snapshot
Version:        0.0.3
Release:        1%{?dist}
Summary:        EBS Snapshots for EC2 Instances

License:        MIT
Source0:        ec2snapshot-%{version}.tar.gz

Requires:       python-boto python-setuptools
BuildRequires:  python-setuptools
BuildArch:      noarch

%description
EBS Snapshots for EC2 Instances

%prep
%setup -q -c -n ec2snapshot-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%files
/usr/bin/ec2snapshot
%{python_sitelib}/ec2snapshot*
%{python_sitelib}/ec2snapshot-*.egg-info

%changelog
* Fri Feb 06 2015 Shawn Siefkas <shawn.siefkas@meredith.com> - 0.0.3-1
- Connection to the appropriate ec2 region API endpoint

* Tue Feb 03 2015 Shawn Siefkas <shawn.siefkas@meredith.com> - 0.0.2-1
- Initial Spec File
