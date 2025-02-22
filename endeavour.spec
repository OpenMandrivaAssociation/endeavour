%define name    endeavour
%define version 3.1.2
%define major   %{version}
%define release %mkrel 6
%define API    2

%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
 
Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    Graphical file manager
Group:      Graphical desktop/Other
License:    GPL
URL:        https://wolfpack.twu.net/Endeavour2
Source:     http://wolfpack.twu.net/users/wolfpack/%{name}-%{version}.tar.bz2
Patch0:     endeavour-3.1.2-fix-build-error.patch
Patch1:     endeavour-3.1.2-fix-lib64-build.patch
Patch2:		endeavour-3.1.2-libzip-0.10.patch
Patch3:		endeavour-3.1.2-link.patch
BuildRequires:  libx11-devel
BuildRequires:	libxpm-devel
BuildRequires:	libxxf86vm-devel
BuildRequires:  gtk+-devel
BuildRequires:  imlib-devel
BuildRequires:  libzip-devel
BuildRequires:  libtar-devel
BuildRequires:  libxar-devel
BuildRequires:  bzip2-devel
BuildRequires:  ungif-devel
BuildRequires:	jpeg-devel
BuildRequires:	mng-devel
BuildRequires:	png-devel
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
 

%package -n %{libname}
Summary:    Shared libraries for %{name}
Group:      System/Libraries
 
%description -n %{libname}
Shared libraries for %{name}.

%package -n %{develname}
Summary:    Development header files for %{name}
Group:      Development/C
Provides:   %{name}-devel = %{version}-%{release}
Requires:   %{libname} = %{version}-%{release}
Obsoletes:  %{name}-devel < 3.1.2
 
%description -n %{develname}
Libraries, include files and other resources you can use to develop
%{name} applications.

%prep
%setup -q 
%patch0 -p 1
%patch1 -p 1
%patch2 -p 0 -b .zip
%patch3 -p0 -b .link

%build
export CFLAGS="%optflags -fPIC %ldflags"
%ifarch x86_64
%define platform Linux64
%else
%define platform Linux
%endif
./configure %{platform} \
    --CFLAGS="%optflags %ldflags" \
    -v \
    --disable=arch-i686 \
    --enable-debug \
    --libdir=-L%{_libdir}

make \
    PREFIX=%{_prefix} \
    LIB_DIR=%{_libdir} \
    MAN_DIR=/usr/share/man/man1 \
    EDV_INCLUDE_DIR=%{_includedir}/%{name}%{API} \
    EDV_LIB_DIR=%{_libdir}/%{name}%{API} \
    EDV_BIN_DIR=%{_libdir}/%{name}%{API} \
    EDV_ARCH_DIR=%{_libdir}/%{name}%{API} \
    MAJOR=%{major} \
    CC="gcc %ldflags" \
    CPP="g++ %ldflags" \
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
    LDCONFIG=/bin/true \
    MAJOR=%{major} \
    install

# symlink shared library
pushd %{buildroot}%{_libdir}
ln -sf libendeavour2-base-%{major}.so libendeavour2-base.so
popd

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
Categories=GTK;FileManager;Graphics;
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
%{_datadir}/applications/*.desktop
%{_datadir}/%{name}%{API}
%{_iconsdir}/%{name}%{API}*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libendeavour2-base-%{major}.so

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/%{name}%{API}
%{_bindir}/endeavour2-base-config
%{_libdir}/libendeavour2-base.so
