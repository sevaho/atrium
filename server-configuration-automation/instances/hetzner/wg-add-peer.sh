#!/usr/bin/env nix-shell
#!nix-shell -i bash -p wireguard-tools qrencode
# Usage: ./wg-add-peer.sh <name> <ip>    e.g. ./wg-add-peer.sh phone 10.234.0.3
# Adds the peer to host_vars and shows a QR code with the full client config.
# The private key only lives in memory and in the QR code, never on disk.
#
# Steps:
#   1. ./wg-add-peer.sh phone 10.234.0.3    (in your own terminal, the QR holds the private key)
#   2. WireGuard app: + > Scan from QR code, name it asicserver
#   3. clear && printf '\e[3J'              (wipe the QR from scrollback)
#   4. make up                              (server accepts the new peer)
#
# Next free IP: highest address in host_vars/hetzner/vars.yml + 1.
# Lost device: remove its entry from vars.yml and run make up.
set -euo pipefail

name=${1:?usage: $0 <name> <ip>, e.g. $0 phone 10.234.0.3}
ip=${2:?usage: $0 <name> <ip>, e.g. $0 phone 10.234.0.3}
vars=host_vars/hetzner/vars.yml

if grep -qE "name: $name$|address: $ip/32$" "$vars"; then
  echo "peer $name or $ip already exists in $vars" >&2
  exit 1
fi

priv=$(wg genkey)
pub=$(wg pubkey <<< "$priv")

cat >> "$vars" <<EOF
  - name: $name
    public_key: $pub
    address: $ip/32
EOF

qrencode -t ansiutf8 <<EOF
[Interface]
PrivateKey = $priv
Address = $ip/32

[Peer]
PublicKey = kUQ/H9aY5cJUH0wCprZsJ533XgaHRUXR7qT/ITn5fFI=
Endpoint = 188.40.132.107:51820
AllowedIPs = 10.234.0.0/24
PersistentKeepalive = 25
EOF

echo "Added $name ($ip). Scan the code, run 'clear && printf \"\\e[3J\"', then 'make up'."
