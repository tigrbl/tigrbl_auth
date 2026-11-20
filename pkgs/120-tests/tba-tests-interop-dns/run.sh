#!/bin/sh
set -eu

test_dir=$(mktemp -d)
cd "$test_dir"
umask 077
export KRB5_CONFIG="$test_dir/krb5.conf"
export KRB5_KDC_PROFILE="$test_dir/kdc.conf"
export KRB5CCNAME="FILE:$test_dir/client.ccache"
export KRB5_KTNAME="FILE:$test_dir/dns.keytab"
export PYTHONDONTWRITEBYTECODE=1

cat > "$KRB5_CONFIG" <<'EOF'
[libdefaults]
 default_realm = DNS-PEER.TEST
 dns_lookup_kdc = false
 dns_lookup_realm = false
 dns_canonicalize_hostname = false
 rdns = false
[realms]
 DNS-PEER.TEST = {
   kdc = 127.0.0.1:1088
 }
EOF

cat > "$KRB5_KDC_PROFILE" <<EOF
[kdcdefaults]
 kdc_listen = 127.0.0.1:1088
 kdc_tcp_listen = 127.0.0.1:1088
[realms]
 DNS-PEER.TEST = {
   database_name = $test_dir/principal
   key_stash_file = $test_dir/stash
   max_life = 1h
 }
EOF

master_password=$(od -An -N24 -tx1 /dev/urandom | tr -d ' \n')
kdb5_util -r DNS-PEER.TEST create -s -P "$master_password"
unset master_password
kadmin.local -r DNS-PEER.TEST -q 'addprinc -randkey DNS/ns.interop.test@DNS-PEER.TEST'
kadmin.local -r DNS-PEER.TEST -q 'addprinc -randkey client@DNS-PEER.TEST'
kadmin.local -r DNS-PEER.TEST -q "ktadd -k $test_dir/dns.keytab DNS/ns.interop.test@DNS-PEER.TEST"
kadmin.local -r DNS-PEER.TEST -q "ktadd -k $test_dir/client.keytab client@DNS-PEER.TEST"

cat > named.conf <<EOF
options {
    directory "$test_dir";
    listen-on port 1053 { 127.0.0.1; };
    listen-on-v6 { none; };
    recursion no;
    pid-file "$test_dir/named.pid";
    session-keyfile "$test_dir/session.key";
    tkey-gssapi-keytab "$test_dir/dns.keytab";
};
zone "interop.test" {
    type primary;
    file "db.interop";
    update-policy { grant "client@DNS-PEER.TEST" name allowed.interop.test. A; };
};
EOF
cat > db.interop <<'EOF'
$TTL 300
@ SOA ns hostmaster 1 1800 600 86400 60
  NS ns
ns A 127.0.0.1
EOF

krb5kdc -n -r DNS-PEER.TEST > kdc.log 2>&1 &
kdc_pid=$!
named -g -n 2 -c "$test_dir/named.conf" > named.log 2>&1 &
named_pid=$!
trap 'kill "$named_pid" "$kdc_pid" 2>/dev/null || true' EXIT

for attempt in 1 2 3 4 5; do
    if kinit -k -t "$test_dir/client.keytab" client@DNS-PEER.TEST > kinit.log 2>&1; then
        break
    fi
    if [ "$attempt" = 5 ]; then
        cat kdc.log kinit.log
        exit 1
    fi
    sleep 1
done

uv pip install --offline --no-index --find-links /wheels --no-deps --python /opt/dns-peer/bin/python \
    tba-primitives-dns-name==0.4.0.dev2 tba-codec-dns==0.4.0.dev2 \
    tba-concrete-dns-zone==0.4.0.dev2 tba-provider-dns-resolver==0.4.0.dev2 tba-protocol-dns==0.4.0.dev2

if ! uv run --no-project --offline --python /opt/dns-peer/bin/python /opt/dns-interop/probe.py; then
    cat named.log
    exit 1
fi
