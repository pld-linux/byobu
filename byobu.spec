Summary:	A set of useful profiles and a profile-switcher for GNU screen
Summary(hu.UTF-8):	Hasznos profilok és profilváltó gyűjteménye a GNU screen-hez
Summary(pl.UTF-8):	Zestaw przydatnych profili oraz przełącznik profili dla GNU screena
Name:		byobu
Version:	5.111
Release:	1
License:	GPL v3
Group:		Applications/System
Source0:	https://code.launchpad.net/byobu/trunk/%{version}/+download/%{name}_%{version}.orig.tar.gz
# Source0-md5:	286151043876bf9f7e884f95f706aa73
Patch0:		desktop.patch
URL:		https://launchpad.net/byobu
BuildRequires:	gettext-tools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.596
Requires:	desktop-file-utils
Requires:	python >= 1:2.5
Requires:	python-snack
Suggests:	screen
Suggests:	tmux >= 1.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautocompressdoc '*.txt'

%define		_libexecdir	%{_prefix}/lib

%description
Byobu is an elegant enhancement of the otherwise functional, plain,
practical GNU Screen. Byobu includes an enhanced profile and
configuration utilities for the GNU screen window manager, such as
toggle-able system status notifications.

%description -l hu.UTF-8
Byobu egy elegáns kiterjesztése az amúgy használható, egyszerű,
praktikus GNU screen-nek. A Byobu tartalmaz egy kiterjesztett profilt
és konfigurációs eszközöket a GNU screen ablakkezelőhöz, pl. a
ki/bekapcsolható rendszer státusz jelentéseket.

%description -l pl.UTF-8
Byobu to eleganckie rozszerzenie dla funkcjonalnego, zwykłego,
praktycznego GNU screena. Byobu zawiera rozszerzony profil oraz
narzędzia konfiguracyjne dla zarządcy okien, jakim jest GNU screen
- takie jak przełączane powiadomienia o stanie systemu.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e '
	s#/share/doc/byobu#/share/doc/%{name}-%{version}#
' usr/share/byobu/keybindings/*

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
%configure
%{__make}

for po in po/*.po; do
	lang=${po#po/}
	lang=${lang%.po}
	mkdir -p locale/${lang}/LC_MESSAGES/
	msgfmt ${po} -o locale/${lang}/LC_MESSAGES/%{name}.mo
done

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	CP="cp -p" \
	DESTDIR=$RPM_BUILD_ROOT

# some debian hackery, just use the "current" one for pld
install -d $RPM_BUILD_ROOT%{_desktopdir}
mv $RPM_BUILD_ROOT{%{_datadir}/%{name}/desktop,%{_desktopdir}}/%{name}.desktop

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

install -d $RPM_BUILD_ROOT%{_localedir}
cp -a locale/* $RPM_BUILD_ROOT%{_localedir}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%doc usr/share/doc/byobu/*.txt
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/backend
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/socketdir
%attr(755,root,root) %{_bindir}/byobu
%attr(755,root,root) %{_bindir}/byobu-config
%attr(755,root,root) %{_bindir}/byobu-ctrl-a
%attr(755,root,root) %{_bindir}/byobu-disable
%attr(755,root,root) %{_bindir}/byobu-disable-prompt
%attr(755,root,root) %{_bindir}/byobu-enable
%attr(755,root,root) %{_bindir}/byobu-enable-prompt
%attr(755,root,root) %{_bindir}/byobu-export
%attr(755,root,root) %{_bindir}/byobu-janitor
%attr(755,root,root) %{_bindir}/byobu-keybindings
%attr(755,root,root) %{_bindir}/byobu-launch
%attr(755,root,root) %{_bindir}/byobu-launcher
%attr(755,root,root) %{_bindir}/byobu-launcher-install
%attr(755,root,root) %{_bindir}/byobu-launcher-uninstall
%attr(755,root,root) %{_bindir}/byobu-layout
%attr(755,root,root) %{_bindir}/byobu-prompt
%attr(755,root,root) %{_bindir}/byobu-quiet
%attr(755,root,root) %{_bindir}/byobu-reconnect-sockets
%attr(755,root,root) %{_bindir}/byobu-screen
%attr(755,root,root) %{_bindir}/byobu-select-backend
%attr(755,root,root) %{_bindir}/byobu-select-profile
%attr(755,root,root) %{_bindir}/byobu-select-session
%attr(755,root,root) %{_bindir}/byobu-shell
%attr(755,root,root) %{_bindir}/byobu-silent
%attr(755,root,root) %{_bindir}/byobu-status
%attr(755,root,root) %{_bindir}/byobu-status-detail
%attr(755,root,root) %{_bindir}/byobu-tmux
%attr(755,root,root) %{_bindir}/byobu-ugraph
%attr(755,root,root) %{_bindir}/byobu-ulevel
%attr(755,root,root) %{_bindir}/col1
%attr(755,root,root) %{_bindir}/ctail
%attr(755,root,root) %{_bindir}/manifest
%attr(755,root,root) %{_bindir}/purge-old-kernels
%attr(755,root,root) %{_bindir}/vigpg
%attr(755,root,root) %{_bindir}/wifi-status
%{_mandir}/man1/*.1*
/etc/profile.d/Z97-byobu.sh
%{_datadir}/dbus-1/services/us.kirkland.terminals.byobu.service
%{_desktopdir}/%{name}.desktop
# preserve +x bits where needed
%defattr(-,root,root,-)
%{_libexecdir}/%{name}
%{_datadir}/%{name}
