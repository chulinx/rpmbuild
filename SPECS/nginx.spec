Name:           nginx
Version:        1.8.1
Release:        7%{?dist}
Summary:        nginx-1.8.1.tar.gz rpmbuild to nginx.1.8.1.rpm
License:        GPLv2
URL:            http://nginx.org
Source0:        %{name}-%{version}.tar.gz
Source1:	nginx
Source2: 	nginx.conf                    
Source3: 	fastcgi
Packager:	Mitake-zlx{chulinx@163.com}
Vendor:		Mitake-zlx
BuildRequires:  gcc,openssl,openssl-devel,pcre-devel,pcre,zlib,zlib-devel
Requires:       openssl,openssl-devel,pcre-devel,pcre,zlib,zlib-devel
%description
 Custom a rpm by yourself!Build nginx-1.8.1.tar.gz to nginx-1.8.1.rpm
%prep
%setup -q
%build
./configure
./configure \
--prefix=/usr/local/nginx \
--user=www \
--group=www \
--with-http_ssl_module \
--with-http_flv_module \
--with-http_stub_status_module \
--with-http_gzip_static_module \
--http-client-body-temp-path=/var/tmp/nginx/client/ \
--http-proxy-temp-path=/var/tmp/nginx/proxy/ \
--http-fastcgi-temp-path=/var/tmp/nginx/fcgi/ \
--http-uwsgi-temp-path=/var/tmp/nginx/uwsgi \
--http-scgi-temp-path=/var/tmp/nginx/scgi \
--with-pcre
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install DESTDIR=%{buildroot}
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/nginx
%{__install} -p -D %{SOURCE2} %{buildroot}/usr/local/nginx/conf/nginx.conf
%{__install} -p -D %{SOURCE3} %{buildroot}/usr/local/nginx/conf/fastcgi_params
%pre
if [ $1 == 1 ];then                                                         
    /usr/sbin/useradd  -s /bin/false -r  nginx 2>/dev/null || :
fi
%post
if [ $1 == 1 ];then
        /sbin/chkconfig --add %{name}
        /sbin/chkconfig %{name} on
        mkdir /usr/local/nginx/conf/conf.d/
	ln -s /usr/local/nginx/sbin/nginx /usr/sbin/nginx
        echo '
net.ipv4.tcp_max_syn_backlog = 65536
net.core.netdev_max_backlog =  32768
net.core.somaxconn = 32768
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 2
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_mem = 94500000 915000000927000000
net.ipv4.tcp_max_orphans = 3276800
#net.ipv4.tcp_fin_timeout = 30
#net.ipv4.tcp_keepalive_time = 120
net.ipv4.ip_local_port_range = 1024  65535' >> /etc/sysctl.conf
sysctl -p 2>&1 /dev/null
fi
%preun
if [ $1 == 0 ];then
        /etc/init.d/%{name} stop > /dev/null 2>&1
	/sbin/chkconfig --del %{name}
        rm -fr /usr/local/nginx/conf/conf.d/
	rm -f /usr/sbin/nginx
	/usr/sbin/userdel nginx 2>/dev/null || :
fi
%postun
%clean
rm -rf %{buildroot}
%files
%defattr(-,root,root,0755)
/usr/local/nginx/
%attr(0755,root,root) /etc/rc.d/init.d/nginx
%config(noreplace) /usr/local/nginx/conf/nginx.conf
%config(noreplace) /usr/local/nginx/conf/fastcgi_params
%doc
%changelog
 *  Mon Aug 28 2017 Mitake <chulinx@163.com> - 1.8.1
- Initial version
