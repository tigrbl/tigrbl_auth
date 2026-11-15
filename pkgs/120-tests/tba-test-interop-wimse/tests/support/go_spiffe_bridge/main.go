// Loopback interoperability fixture for the released go-spiffe verifier.
package main

import (
	"context"
	"crypto/x509"
	"encoding/json"
	"fmt"
	"os"
	"time"

	"github.com/spiffe/go-spiffe/v2/bundle/x509bundle"
	"github.com/spiffe/go-spiffe/v2/spiffeid"
	"github.com/spiffe/go-spiffe/v2/svid/x509svid"
	"github.com/spiffe/go-spiffe/v2/workloadapi"
)

type verification struct {
	Certificate []byte `json:"certificate"`
	Anchor      string `json:"anchor"`
	Expected    string `json:"expected"`
}

func verify() error {
	var request verification
	if err := json.NewDecoder(os.Stdin).Decode(&request); err != nil {
		return err
	}
	expected, err := spiffeid.FromString(request.Expected)
	if err != nil {
		return err
	}
	bundle, err := x509bundle.Load(expected.TrustDomain(), request.Anchor)
	if err != nil {
		return err
	}
	leaf, err := x509.ParseCertificate(request.Certificate)
	if err != nil {
		return err
	}
	id, _, err := x509svid.Verify([]*x509.Certificate{leaf}, bundle)
	if err != nil {
		return err
	}
	if id != expected {
		return fmt.Errorf("unexpected SPIFFE peer identity %q", id)
	}
	return json.NewEncoder(os.Stdout).Encode(id.String())
}

func fetch(address string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	source, err := workloadapi.NewX509Source(ctx, workloadapi.WithClientOptions(workloadapi.WithAddr(address)))
	if err != nil {
		return err
	}
	defer source.Close()
	svid, err := source.GetX509SVID()
	if err != nil {
		return err
	}
	bundle, err := source.GetX509BundleForTrustDomain(svid.ID.TrustDomain())
	if err != nil {
		return err
	}
	if _, _, err := x509svid.Verify(svid.Certificates, bundle); err != nil {
		return err
	}
	return json.NewEncoder(os.Stdout).Encode(svid.ID.String())
}

func main() {
	var err error
	switch {
	case len(os.Args) == 2 && os.Args[1] == "verify":
		err = verify()
	case len(os.Args) == 3 && os.Args[1] == "fetch":
		err = fetch(os.Args[2])
	default:
		err = fmt.Errorf("expected verify or fetch <workload-api-address>")
	}
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
