Summary:	A set of useful profiles and a profile-switcher for GNU screen
Summary(hu.UTF-8):	Hasznos profilok és profilváltó gyűjteménye a GNU screen-hez
Summary(pl.UTF-8):	Zestaw przydatnych profili oraz przełącznik profili dla GNU screena
Name:		byobu
Version:	2.36
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://code.launchpad.net/byobu/trunk/2.36/+download/%{name}_%{version}.orig.tar.gz
# Source0-md5:	6dd84835ec1e7b3b4bf7f7e2da952896
URL:		https://code.launchpad.net/byobu
BuildRequires:	gettext-tools
BuildRequires:	rpm-pythonprov
Requires:	newt
Requires:	python >= 1:2.5
Requires:	screen
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -n %{name}_%{version}.orig

%build
profiles_generator/generate

%install
rm -rf $RPM_BUILD_ROOT

debian/rules install-po
install -d $RPM_BUILD_ROOT%{_libdir}/byobu
install -d $RPM_BUILD_ROOT%{_datadir}/locale
install -d $RPM_BUILD_ROOT%{_datadir}/byobu/profiles
install -d $RPM_BUILD_ROOT%{_datadir}/byobu/keybindings
install -d $RPM_BUILD_ROOT%{_datadir}/byobu/windows
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/byobu
install -d $RPM_BUILD_ROOT%{_mandir}/man1
%{__cp} bin/* $RPM_BUILD_ROOT%{_libdir}/byobu
%{__cp} -r po/locale/* $RPM_BUILD_ROOT%{_datadir}/locale
%{__cp} profiles/{byoburc,common,NONE,black,dark,light} $RPM_BUILD_ROOT%{_datadir}/byobu/profiles
ln -sf f-keys $RPM_BUILD_ROOT%{_datadir}/byobu/keybindings/common
%{__cp} keybindings/{f-keys,none} $RPM_BUILD_ROOT%{_datadir}/byobu/keybindings
%{__cp} windows/common $RPM_BUILD_ROOT%{_datadir}/byobu/windows
%{__cp} byobu byobu-{select-profile,config,launcher,janitor,export,status,status-detail} \
	motd+shell $RPM_BUILD_ROOT%{_bindir}
%{__cp} byobu-launcher-{,un}install $RPM_BUILD_ROOT%{_datadir}/byobu
%{__cp} profiles/*_* $RPM_BUILD_ROOT%{_datadir}/byobu/profiles
%{__cp} statusrc $RPM_BUILD_ROOT%{_sysconfdir}/byobu
%{__cp} *.1 $RPM_BUILD_ROOT%{_mandir}/man1

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/motd+shell
%attr(755,root,root) %{_bindir}/byobu-launcher
%attr(755,root,root) %{_bindir}/byobu-janitor
%attr(755,root,root) %{_bindir}/byobu
%attr(755,root,root) %{_bindir}/byobu-config
%attr(755,root,root) %{_bindir}/byobu-export
%attr(755,root,root) %{_bindir}/byobu-status
%attr(755,root,root) %{_bindir}/byobu-status-detail
%attr(755,root,root) %{_bindir}/byobu-select-profile
%{_libdir}/byobu
%{_datadir}/byobu
%{_sysconfdir}/byobu
%doc README doc/help.txt debian/changelog
%{_mandir}/man1/*
