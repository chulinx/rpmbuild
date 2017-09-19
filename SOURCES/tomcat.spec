Name:			tomcat	
Version:        7.0.81
Release:		5%{?dist}
Summary:		tomcat. 

Vendor:         Mitake, Inc.
Packager:       zhangxiang <zhangxiang@mitake.com.cn>
Group:			mitake
License:		GPLv2
URL:			http://www.mitake.com/
Source0:        %{name}-%{version}.tar.gz	
Source1:        tomcat
Source2:        mysql-connector-java-5.1.34.jar
BuildRoot:		%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Provides:		 mitake_tomcat

Requires(pre):  jdk_export = 1.8
Conflicts:      jdk_export = 1.7

%description
   tomcat

%prep
%setup -q


%build


%install
rm -rf %{buildroot}
%{__install} -p -d -m 0755  %{buildroot}/usr/local/tomcat-7.0.81
cp -r * %{buildroot}/usr/local/tomcat-7.0.81/
%{__install} -p -D -m 0640 %{SOURCE1} %{buildroot}/etc/init.d/tomcat
%{__install} -p -D -m 0640 %{SOURCE2} %{buildroot}/usr/local/tomcat-7.0.81/lib/mysql-connector-java-5.1.34.jar

%clean
rm -rf %{buildroot}

%pre

%post
if [ $1 == 1 ]; then
   ln -s /usr/local/tomcat-7.0.81/  /usr/local/tomcat >>/dev/null 2>&1
   chkconfig --add tomcat >>/dev/null 2>&1
   netstat -nplt |grep 8080 >>/dev/null 2>&1
   if [ $? == 0  ]; then
	  echo "8080 port is used ,Please config other Port! "
   else
	  /etc/init.d/tomcat start 
	  StatusCode=curl -I -m 10 -o /dev/null -s -w %{http_code} 127.0.0.1:8080
	  if [ $StatusCode == 200  ];then
		echo "Tomcat is Installd Sucessfull!"
   fi
fi

%preun
if [ $1 == 0 ]; then 
  /etc/init.d/tomcat stop >>/dev/null 2>&1
  chkconfig --del tomcat >>/dev/null 2>&1
  rm -rf /usr/local/tomcat >>/dev/null 2>&1
  rm -rf /usr/local/tomcat-7.0.81  >>/dev/null 2>&1
fi


%files
%defattr(-,mds,mds,-)
/usr/local/tomcat-7.0.81/
%attr(0755,mds,mds) /etc/init.d/tomcat

%changelog
* Wed Aug 30  2017 mitake.com.cn <zhangxiang@mitake.com.cn> - tomcat
- Initial version
- Update 7.0.61--7.0.81
