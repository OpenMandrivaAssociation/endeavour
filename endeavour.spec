%define name    endeavour
%define version 2.8.2
%define release %mkrel 2
%define API    2
 
Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    Graphical file manager
Group:      Graphical desktop/Other
License:    GPL
URL:        http://wolfpack.twu.net/Endeavour2
Source0:    http://wolfpack.twu.net/users/wolfpack/%{name}-%{version}.tar.bz2
Patch:      %{name}-2.8.2-gcc-fix.patch
BuildRequires:  X11-devel
BuildRequires:  gtk+-devel
BuildRequires:  imlib-devel
#enable zip support
BuildRequires:  libzip-devel
#enable video mode extentions
BuildRequires:  libxxf86vm-devel
Obsoletes:  libendeavour2
Provides:    libendeavour2
 
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
export CFLAGS="%optflags" 
./configure Linux -v --disable=arch-i686 --libdir=-L%{_libdir}
make    PREFIX=%{_prefix} \
    MAN_DIR=/usr/share/man/man1 \
    EDV_INCLUDE_DIR=%{_includedir}/%{name}%{API} \
    EDV_LIB_DIR=%{_libdir} \
    EDV_BIN_DIR=%{_libdir}/%{name}%{API} \
    all
 

%install
rm -rf %{buildroot}
make    PREFIX=%{buildroot}%{_prefix} \
    MAN_DIR=%{buildroot}/usr/share/man/man1 \
    EDV_INCLUDE_DIR=%{buildroot}%{_includedir}/%{name}%{API} \
    EDV_LIB_DIR=%{buildroot}%{_libdir} \
    EDV_BIN_DIR=%{buildroot}%{_libdir}/%{name}%{API} \
    install

#rn symlink pointing to build
rm -f %{buildroot}%{_libdir}/libendeavour2.so 
#install lib
install -m 755 endeavour2/lib/libendeavour2.so %{buildroot}%{_libdir}
#devloper say this lk is needed
mkdir %{buildroot}%{_libdir}/endeavour2/lib
ln -s %{_libdir}/libendeavour2.so %{buildroot}%{_libdir}/endeavour2/lib

#fix man location
mv %{buildroot}/usr/man/man1/* %{buildroot}%{_mandir}/man1
rm -rfd %{buildroot}/usr/man

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

%post
%update_menus
%{update_desktop_database}

%postun
%clean_menus
%{clean_desktop_database}
 
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
%{_libdir}/*.so
%{_iconsdir}/%{name}%{API}*
 

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/%{name}%{API}
%{_bindir}/%{name}%{API}-config 
%{_mandir}/man1/*config*

