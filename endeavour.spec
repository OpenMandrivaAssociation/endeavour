%define name    endeavour
%define version 2.8.5
%define release %mkrel 1
%define API    2
 
Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    Graphical file manager
Group:      Graphical desktop/Other
License:    GPL
URL:        http://wolfpack.twu.net/Endeavour2
Source0:    http://wolfpack.twu.net/users/wolfpack/%{name}-%{version}.tar.bz2
Patch:      %{name}-2.8.5-gcc.patch
BuildRequires:  X11-devel
BuildRequires:  gtk+-devel
BuildRequires:  imlib-devel
BuildRequires:  libzip-devel
BuildRequires:  libtar-devel
BuildRequires:  libxar-devel
BuildRequires:  bzip2-devel
BuildRequires:  libxxf86vm-static-devel
Obsoletes:  libendeavour2
Provides:    libendeavour2
BuildRoot:  %_tmppath/%{name}-%{version}
 
%description
Endeavour Mark II is a complete file management suite that comes
with a File Browser, Image Browser, Archiver, Recycled Objects 
system, and a set of file & disk management utility programs. 

Featuring: 
 
  *  Two pane tree & list style File Browser. 
  *  Image Browser with thumbs list and a pan & zoom image viewer. 
  *  Archiver for viewing, creating, and extracting packages. 
  *  Commercial quality user-interface design. 
  *  Convient drag & drop operations. 
  *  Drag & drop downloading with the WGet Front End. 
  *  Extended MIME Types support with external import/export support  
  *  for other MIME Type file formats. 
  *  Fully customizable tool bars and list headings. 
  *  A recycled objects system. 
  *  Device and disk utility programs: 
  *  Download - Front end for the GNU WGet 
  *  HEdit - Hex editor 
  *  SysInfo - CPU Display 
  *  ZipTool - Front end for ZipTools
 

%package -n %{name}-devel
Summary:        Development header files for %{name}
Group:          Development/C
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:     libendeavour2-devel
Provides:       libendeavour2-devel
 
%description -n %{name}-devel
Libraries, include files and other resources you can use to develop
%{name} applications.

%prep
%setup -q 
%patch -p 1

%build
export CFLAGS="%optflags -fPIC"
./configure Linux -v --disable=arch-i686 --libdir=-L%{_libdir}
make \
    PREFIX=%{_prefix} \
    LIB_DIR=%{_libdir} \
    MAN_DIR=/usr/share/man/man1 \
    EDV_INCLUDE_DIR=%{_includedir}/%{name}%{API} \
    EDV_LIB_DIR=%{_libdir}/%{name}%{API} \
    EDV_BIN_DIR=%{_libdir}/%{name}%{API} \
    EDV_ARCH_DIR=%{_libdir}/%{name}%{API} \
    all
 

%install
rm -rf %{buildroot}
make \
    PREFIX=%{buildroot}%{_prefix} \
    LIB_DIR=%{buildroot}%{_libdir} \
    MAN_DIR=%{buildroot}/usr/share/man/man1 \
    MAN1_DIR=%{buildroot}/usr/share/man/man1 \
    EDV_INCLUDE_DIR=%{buildroot}%{_includedir}/%{name}%{API} \
    EDV_LIB_DIR=%{buildroot}%{_libdir}/%{name}%{API} \
    EDV_BIN_DIR=%{buildroot}%{_libdir}/%{name}%{API} \
    EDV_ARCH_DIR=%{buildroot}%{_libdir}/%{name}%{API} \
    install

# remove useless symlink
rm -f %{buildroot}%{_libdir}/libendeavour2.so 

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Endeavour
Comment=Graphical file manager
Exec=%{_bindir}/%{name}%{API}
Icon=%{_iconsdir}/%{name}.png
Terminal=false
Type=Application 
StartupNotify=true
Categories=GTK;FileManager;X-MandrivaLinux-System-FileTools;
EOF

rm -f %{buildroot}%{_libdir}/%{name}2/{LICENSE,README}

%if %mdkversion < 200900
%post
%update_menus
%{update_desktop_database}
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%{clean_desktop_database}
%endif
 
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS HACKING INSTALL LANGUAGE LICENSE README TODO
%{_bindir}/%{name}%{API}
%{_libdir}/%{name}%{API}
%{_mandir}/man1/*
%exclude %{_mandir}/man1/*config*
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}%{API}
#%{_libdir}/*.so
%{_iconsdir}/%{name}%{API}*
 

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/%{name}%{API}
%{_bindir}/%{name}%{API}-config 
%{_mandir}/man1/*config*
