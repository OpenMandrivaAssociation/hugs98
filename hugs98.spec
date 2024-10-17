Summary:	Hugs 98: The Nottingham and Yale Haskell system
Name:		hugs98
Version:	20060920
%define real_ver Sep2006
Release:	%mkrel 7
Source0:	http://cvs.haskell.org/Hugs/downloads/hugs98-%{real_ver}.tar.bz2
Source2:	http://haskell.cs.yale.edu/haskell-mode/haskell-mode-1.44.tar.bz2
Url:		https://www.haskell.org/hugs/
License:	Artistic
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ncurses-devel readline-devel
BuildRequires:  docbook-utils docbook-dtd44-xml
Group:		Development/Other
Provides: haskell-compiler
Provides: haskell-interactive

%description
A Haskell interpreter and programming environment for developing cool
Haskell programs.

This release is largely conformant with Haskell 98, including
monad and record syntax, newtypes, strictness annotations, and
modules.  In addition, it comes packaged with the libraries defined
in the most recent version of the Haskell Library Report and with
extension libraries which are compatible with GHC 3.0.

%prep
%setup -q -n %{name}-%{real_ver}

#restore %{name}
%setup -q -n %{name}-%{real_ver} -T -D

%build
%configure --with-readline --libdir %{_datadir} # force to install in /usr/share/hugs instead of /usr/lib/hugs
%make OPTFLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install_all_but_docs
make -C docs DESTDIR=${RPM_BUILD_ROOT} install_man

install -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/
(cd $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp ; 
 tar xfj %{SOURCE2} ;
 # fix errors
 perl -pi -e 's/\(enum-from-to/(haskell-enum-from-to/g' *.el
)

install -d $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d/%{name}.el
(autoload 'haskell-mode "haskell-mode" "Major mode for editing Haskell scripts." t)
(autoload 'literate-haskell-mode "haskell-mode" "Major mode for editing literate Haskell scripts." t)
(add-hook 'haskell-mode-hook 'turn-on-haskell-font-lock)
(add-hook 'haskell-mode-hook 'turn-on-haskell-decl-scan)
(add-hook 'haskell-mode-hook 'turn-on-haskell-doc-mode)
(add-hook 'haskell-mode-hook 'turn-on-haskell-indent)
(add-hook 'haskell-mode-hook 'turn-on-haskell-hugs)
(add-to-list 'auto-mode-alist '("\\\\.[hg]s$"  . haskell-mode))
(add-to-list 'auto-mode-alist '("\\\\.hi$"     . haskell-mode))
(add-to-list 'auto-mode-alist '("\\\\.l[hg]s$" . literate-haskell-mode))
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc Credits
%doc License
%doc Readme
%doc docs/ffi-notes.txt
%doc docs/libraries-notes.txt
%doc docs/machugs-notes.txt
%doc docs/server.html
%doc docs/server.tex
%doc docs/winhugs-notes.txt
%doc docs/users_guide/users_guide
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/hugs
%dir %{_datadir}/hsc2hs-0.67
%{_datadir}/hsc2hs-0.67/template-hsc.h
%{_datadir}/emacs/site-lisp/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*


