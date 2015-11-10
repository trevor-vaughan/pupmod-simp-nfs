Summary: NFS Puppet Module
Name: pupmod-nfs
Version: 4.1.0
Release: 14
License: Apache License, Version 2.0
Group: Applications/System
Source: %{name}-%{version}-%{release}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires: pupmod-augeasproviders_sysctl
Requires: pupmod-autofs >= 4.1.0
Requires: pupmod-common >= 4.1.0-6
Requires: pupmod-simplib >= 1.0.0-0
Requires: pupmod-simpcat >= 4.0.0-0
Requires: pupmod-stunnel >= 4.2.0-0
Requires: pupmod-sysctl >= 4.1.0-2
Requires: puppet >= 3.3.0
Buildarch: noarch
Requires: simp-bootstrap >= 4.2.0
Obsoletes: pupmod-nfs-test

Prefix: /etc/puppet/environments/simp/modules

%description
This puppet module supports the configuration of NFS.
NFSv4 is preferred, but v2 and v3 are supported.

Additionally, the module contains support for wrapping NFSv4 traffic in stunnel.

%prep
%setup -q

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{prefix}/nfs

dirs='files lib manifests templates'
for dir in $dirs; do
  test -d $dir && cp -r $dir %{buildroot}/%{prefix}/nfs
done

mkdir -p %{buildroot}/usr/share/simp/tests/modules/nfs

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{prefix}/nfs

%files
%defattr(0640,root,puppet,0750)
%{prefix}/nfs

%post
#!/bin/sh

if [ -d %{prefix}/nfs/plugins ]; then
  /bin/mv %{prefix}/nfs/plugins %{prefix}/nfs/plugins.bak
fi

%postun
# Post uninstall stuff

%changelog
* Mon Nov 09 2015 Chris Tessmer <chris.tessmer@onypoint.com> - 4.1.0-14
- migration to simplib and simpcat (lib/ only)

* Mon Nov 02 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-13
- Updated the dependency chain for the NFS client kernel module load ordering.

* Thu Feb 19 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-12
- Migrated to the new 'simp' environment.

* Fri Jan 16 2015 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-11
- Changed puppet-server requirement to puppet

* Wed Oct 22 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-10
- Update to account for the stunnel module updates in 4.2.0-0

* Fri Sep 19 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-9
- Added some necessary fixes to nfs::server_names

* Fri Sep 19 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-8
- Updated the module to be compatible with both RHEL6 and RHEL7. The
  main issue was the translation of service names between the two
  systems.
- The anongid/anonuid options were changed to 65534 since the NFS
  server daemon no longer recognizes -1 and will hang if you use those
  options.

* Wed Aug 27 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-7
- Updated to use the new sysctl::value define.

* Mon Jul 21 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-6
- Updated to use /var/nfs/home for nfs::create_home_dirs in SIMP>=5

* Sun Jun 22 2014 Kendall Moore <kmoore@keywcorp.com> - 4.1.0-5
- Removed MD5 file checksums for FIPS compliance.

* Thu May 29 2014 Nick Markowski <nmarkowski@keywcorp.com> - 4.1.0-4
- Set sysctl sunrpc table entries only if secure_nfs is enabled.  Both
  values depend on the rpcgssd service.

* Mon May 05 2014 Kendall Moore <kmoore@keywcorp.com> - 4.1.0-3
- Updated referecnes to newly named global LDAP variables.
- Refactored /etc/sysconfig/nfs to be managed only once instead of by both server and client.

* Mon Mar 17 2014 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.1.0-2
- Added a tcpwrappers::allow statement allowing ALL NFS connections if Stunnel
  is used. This may be a bug in Red Hat itself. I'm not positive.
- Updated the export_home comment section to include a section of Hiera
  Variables.
- Modified the home_client defaults to hard,intr instead of soft.
- Fixed the create_home_directories script so that it wouldn't attempt to
  archive the ARCHIVED directory multiple times. Also added date stamping to
  the ARCHIVED directories in case a user is archived multiple times.

* Tue Mar 04 2014 Kendall Moore <kmoore@keywcorp.com> - 4.1.0-1
- Refactored manifests to pass all lint tests for hiera and puppet 3.
- Added rspec tests for test coverage.

* Wed Feb 12 2014 Kendall Moore <kmoore@keywcorp.com> - 4.1.0-0
- Updated all boolean strings to native booleans.

* Wed Jan 15 2014 Adam Yohrling <ayohrling@onyxpoint.com> - 4.1.0-0
- Add a class 'nfs::server::create_home_dirs' which allows for the
  simple creation of NFS home directories on an NFS server from an
  LDAP database.
- Added the option to turn on nfs::server::create_home_dirs in
  stock::export_home.

* Mon Oct 07 2013 Nick Markowski <nmarkowski@keywcorp.com> - 4.0.0-2
- Updated template to reference instance variables with @

* Wed Oct 02 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-1
- Use 'versioncmp' for all version comparisons.

* Wed Jul 31 2013 Trevor Vaughan <tvaughan@onyxpoint.com> - 4.0.0-0
- Updated the documentation for nfs::server::conf
- Added support for the NFSD_V4_GRACE option
- Removed the options $secure_nfs_mods and $rpcmtab since they have
  been deprecated
- Added the ports '111' and $rquotad_port to the list of ports to be
  opened by iptables in the non-stunnel version. This is due to the
  fact that the 'quota' command has not been modified to use the
  single interface instance of NFSv4.

* Mon Jan 07 2013 Kendall Moore <kmoore@keywcorp.com> - 2.0.0-11
- Create a Cucumber test which sets up the base segments for NFS server and client
  services.

* Thu Dec 13 2012 Maintenance
2.0.0-10
- Updated to require pupmod-common >= 2.1.1-2 so that upgrading an old
  system works properly.

* Tue Jun 26 2012 Maintenance
2.0.0-9
- Ensure that nfs-utils is installed before we try to do things with services.

* Thu Jun 07 2012 Maintenance
2.0.0-8
- Ensure that Arrays in templates are flattened.
- Call facts as instance variables.
- Updated the sysctl calls to maintain proper ordering with the service
  statements.
- Fixed the domain setting in /etc/idmapd.conf and fixed the way stunnel works.
  This fixes both the 'nobody' issue and issues with mounts via stunnel
  occasionally failing.
- Moved mit-tests to /usr/share/simp...
- Updated pp files to better meet Puppet's recommended style guide.

* Fri Mar 02 2012 Maintenance
2.0.0-7
- Improved test stubs.

* Tue Dec 20 2011 Maintenance
2.0.0-6
- Updated the spec file to not require a separate file list.
- Scoped all of the top level variables.
- Changed all instances of 'ipaddress' to 'primary_ipaddress'
- Fixed several bugs that cropped up when trying to use stunnel with the stock
  home_client.pp as well as some bugs relating to when the server was trying to
  connect with itself. The stock classes should "just work" now.

* Wed Nov 02 2011 Maintenance
2.0.0-5
- Added a parameterized class to handle the configuration of idmapd. In RHEL5
  this was not necessary as the defaults handled most cases. In RHEL6, the
  defaults do not suffice for the stock class.
- Added a variable $portmap_name to the nfs class to be able to differentiate
  between the RHEL5 and RHEL6 versions.
- Fixed the NFS stock home client to actually call the client stanza.
- Fixed the NFS client to enable the NFSv4 callback port.

* Mon Oct 10 2011 Maintenance
2.0.0-4
- Updated to put quotes around everything that need it in a comparison
  statement so that puppet > 2.5 doesn't explode with an undef error.

* Fri Aug 12 2011 Maintenance
2.0.0-3
- Added a new init script to properly set the sysctl values for
  sunrpc.tcp_slot_table_entries and sunrpc.udp_slot_table_entries prior to NFS
  starting to work around a deficiency in Red Hat.
- Ensure that the sysctl values that are set in nfs::server::conf notify all
  services that rely on those values.
- Updated to have a cleaner status command for nfslock.

* Wed May 25 2011 Maintenance - 2.0.0-2
- Ensure that anonuid and anongid are set to -1 by default.

* Wed Apr 13 2011 Maintenance - 2.0.0-1
- Removed the original stock classes and moved them to pupmod since they were
  for clustering.
- Added stock classes for setting up an NFS server and client for home
  directory mounts using autofs.
- Now properly nail up the NFS callback port for NFSv4
- Now set sunrpc_udp_slot_table_entries and sunrpc_tcp_slot_table_entries to
  128 by default.
- Changed all instances of defined(Class['foo']) to defined('foo') per the
  directions from the Puppet mailing list.
- Exports should be joined with "\n"
- Updated to use concat_build and concat_fragment types

* Tue Jan 11 2011 Maintenance
2.0.0-0
- Refactored for SIMP-2.0.0-alpha release

* Mon Jan 10 2011 Maintenance - 1-7
- Exports entries should not be joined with a hard return!

* Fri Dec 10 2010 Maintenance - 1-6
- Moved nfs::stunnel::client to nfs::client::stunnel::connect
- Added support and default configurations for NFSv3 over stunnel
- Added nfs::stock::stunnel_server and nfs::stock::stunnel_client as nfs setup
  for basic clustering.

* Tue Oct 26 2010 Maintenance - 1-5
- Converting all spec files to check for directories prior to copy.

* Tue Oct 26 2010 Maintenance - 1.0-4
- No files directory in source caused an RPM build failure.

* Thu Sep 09 2010 Maintenance
1.0-3
- Replaced tcpwrappers::tcpwrappers_allow with tcpwrappers::allow.

* Mon Jul 19 2010 Maintenance
1.0-2
- Fix for NFSv4 over Stunnel clients.
- Fix for using custom NFS server export.

* Wed Jul 14 2010 Maintenance
1.0-1
- Fix for NFSv4 over Stunnel.

* Wed May 19 2010 Maintenance
1.0-0
- Refactor and doc update.
- Fixed an issue with starting nfslock resulting from the nfslock
application always returning 0.
- Updated the rpcidmapd service to take into account the case where the
sunrpc filesystem is not mounted
- Added support for NFSv3 over Stunnel.
- Added stunnel_server and stunnel_client classes in stock namespace that
will set up a basic nfs over stunnel server/client to make clustering work.

* Thu Feb 18 2010 Maintenance
0.1-0
- Initial module creation. Supports NFS v2,3,4. Supports NFSv4 over Stunnel
  natively.
  Does not yet support automatic Kerberos use.
