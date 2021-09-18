#!/usr/bin/env bash

set -eu pipefail
cd "$(dirname "$(realpath "${0}")")"

DATADIR=${DATADIR:-/usr/share}
LIBDIR=${LIBDIR:-/usr/lib}

# The actual executable
install -Dm 0755 arfedora-search-provider.py "${LIBDIR}"/arfedora-search-provider/arfedora-search-provider.py

# Search provider definition
install -Dm 0644 conf/org.gnome.Arfedora.SearchProvider.ini "${DATADIR}"/gnome-shell/search-providers/org.gnome.Arfedora.SearchProvider.ini

# Desktop file (for having an icon)
install -Dm 0644 conf/org.gnome.Arfedora.SearchProvider.desktop "${DATADIR}"/applications/org.gnome.Arfedora.SearchProvider.desktop

# DBus configuration (no-systemd)
install -Dm 0644 conf/org.gnome.Arfedora.SearchProvider.service.dbus "${DATADIR}"/dbus-1/services/org.gnome.Arfedora.SearchProvider.service

# DBus configuration (systemd)
install -Dm 0644 conf/org.gnome.Arfedora.SearchProvider.service.systemd "${LIBDIR}"/systemd/user/org.gnome.Arfedora.SearchProvider.service
