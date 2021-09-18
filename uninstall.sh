#!/usr/bin/env bash

set -eu pipefail
cd "$(dirname "$(realpath "${0}")")"

DATADIR=${DATADIR:-/usr/share}
LIBDIR=${LIBDIR:-/usr/lib}

# The actual executable
rm "${LIBDIR}"/arfedora-search-provider/arfedora-search-provider.py
rmdir "${LIBDIR}"/arfedora-search-provider

# Search provider definition
rm "${DATADIR}"/gnome-shell/search-providers/org.gnome.Arfedora.SearchProvider.ini

# Desktop file (for having an icon)
rm "${DATADIR}"/applications/org.gnome.Arfedora.SearchProvider.desktop

# DBus configuration (no-systemd)
rm "${DATADIR}"/dbus-1/services/org.gnome.Arfedora.SearchProvider.service

# DBus configuration (systemd)
rm "${LIBDIR}"/systemd/user/org.gnome.Arfedora.SearchProvider.service
