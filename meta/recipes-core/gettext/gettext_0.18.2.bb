SUMMARY = "Utilities and libraries for producing multi-lingual messages."
DESCRIPTION = "Gettext offers to programmers, translators, and even users, a well integrated set of tools and documentation. Specifically, the GNU `gettext' utilities are a set of tools that provides a framework to help other GNU packages produce multi-lingual messages. These tools include a set of conventions about how programs should be written to support message catalogs, a directory and file naming organization for the message catalogs themselves, a runtime library supporting the retrieval of translated messages, and a few stand-alone programs to massage in various ways the sets of translatable strings, or already translated strings."
HOMEPAGE = "http://www.gnu.org/software/gettext/gettext.html"
SECTION = "libs"
LICENSE = "GPLv3+ & LGPL-2.1+"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

PR = "r0"
DEPENDS = "gettext-native virtual/libiconv ncurses expat"
DEPENDS_class-native = "gettext-minimal-native"
PROVIDES = "virtual/libintl virtual/gettext"
PROVIDES_class-native = "virtual/gettext-native"
RCONFLICTS_${PN} = "proxy-libintl"
SRC_URI = "${GNU_MIRROR}/gettext/gettext-${PV}.tar.gz \
	   file://parallel.patch \
          "

LDFLAGS_prepend_libc-uclibc = " -lrt -lpthread "

SRC_URI[md5sum] = "0c86e5af70c195ab8bd651d17d783928"
SRC_URI[sha256sum] = "516a6370b3b3f46e2fc5a5e222ff5ecd76f3089bc956a7587a6e4f89de17714c"

inherit autotools

EXTRA_OECONF += "--without-lispdir \
                 --disable-csharp \
                 --disable-libasprintf \
                 --disable-java \
                 --disable-native-java \
                 --disable-openmp \
                 --disable-acl \
                 --with-included-glib \
                 --with-libncurses-prefix=${STAGING_LIBDIR}/.. \
                 --without-emacs \
                 --without-cvs \
                 --without-git \
                 --with-included-libxml \
                 --with-included-libcroco \
                 --with-included-libunistring \
                "

acpaths = '-I ${S}/gettext-runtime/m4 \
           -I ${S}/gettext-tools/m4'


# these lack the .x behind the .so, but shouldn't be in the -dev package
# Otherwise you get the following results:
# 7.4M    glibc/images/ep93xx/Angstrom-console-image-glibc-ipk-2008.1-test-20080104-ep93xx.rootfs.tar.gz
# 25M     uclibc/images/ep93xx/Angstrom-console-image-uclibc-ipk-2008.1-test-20080104-ep93xx.rootfs.tar.gz
# because gettext depends on gettext-dev, which pulls in more -dev packages:
# 15228   KiB /ep93xx/libstdc++-dev_4.2.2-r2_ep93xx.ipk
# 1300    KiB /ep93xx/uclibc-dev_0.9.29-r8_ep93xx.ipk
# 140     KiB /armv4t/gettext-dev_0.14.1-r6_armv4t.ipk
# 4       KiB /ep93xx/libgcc-s-dev_4.2.2-r2_ep93xx.ipk

PACKAGES =+ "libgettextlib libgettextsrc"
FILES_libgettextlib = "${libdir}/libgettextlib-*.so*"
FILES_libgettextsrc = "${libdir}/libgettextsrc-*.so*"

PACKAGES =+ "gettext-runtime gettext-runtime-dev gettext-runtime-doc"

FILES_${PN} += "${libdir}/${BPN}/*"

FILES_gettext-runtime = "${bindir}/gettext \
                         ${bindir}/ngettext \
                         ${bindir}/envsubst \
                         ${bindir}/gettext.sh \
                         ${libdir}/libasprintf.so* \
                         ${libdir}/GNU.Gettext.dll \
                        "
FILES_gettext-runtime_append_libc-uclibc = " ${libdir}/libintl.so.* \
                                             ${libdir}/charset.alias \
                                           "
FILES_gettext-runtime-dev += "${libdir}/libasprintf.a \
                      ${includedir}/autosprintf.h \
                     "
FILES_gettext-runtime-dev_append_libc-uclibc = " ${libdir}/libintl.so \
                                                 ${includedir}/libintl.h \
                                               "
FILES_gettext-runtime-doc = "${mandir}/man1/gettext.* \
                             ${mandir}/man1/ngettext.* \
                             ${mandir}/man1/envsubst.* \
                             ${mandir}/man1/.* \
                             ${mandir}/man3/* \
                             ${docdir}/gettext/gettext.* \
                             ${docdir}/gettext/ngettext.* \
                             ${docdir}/gettext/envsubst.* \
                             ${docdir}/gettext/*.3.html \
                             ${datadir}/gettext/ABOUT-NLS \
                             ${docdir}/gettext/csharpdoc/* \
                             ${docdir}/libasprintf/autosprintf.html \
                             ${infodir}/autosprintf.info \
                            "

do_install_append() {
    rm -f ${D}${libdir}/preloadable_libintl.so
}

do_install_append_class-native () {
	rm ${D}${datadir}/aclocal/*
	rm ${D}${datadir}/gettext/config.rpath
	rm ${D}${datadir}/gettext/po/Makefile.in.in
	rm ${D}${datadir}/gettext/po/remove-potcdate.sin
}

BBCLASSEXTEND = "native nativesdk"