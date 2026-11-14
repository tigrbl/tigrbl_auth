// Links the request signer from the pinned Cofide proof of concept.
package main

import (
	"crypto/ecdsa"
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/cofide/wimse-s2s-httpsig-poc/wimse/shared"
	"github.com/go-jose/go-jose/v4"
	"github.com/yaronf/httpsign"
)

type request struct {
	Command, Method, Authority, Target, Nonce, PrivateKey string
	Expires int64
	Headers map[string]string
	Fields []string
	PublicKey jose.JSONWebKey
}

func run(input request) (map[string]string, error) {
	req, err := http.NewRequest(input.Method, "https://" + input.Authority + input.Target, nil)
	if err != nil {
		return nil, err
	}
	req.RequestURI = input.Target
	for name, value := range input.Headers {
		req.Header.Set(name, value)
	}
	switch input.Command {
	case "sign":
		signer, err := shared.GetWITHTTPSigner(input.PrivateKey, input.Fields, shared.WithNonce(input.Nonce),
			func(config *httpsign.SignConfig) {
				config.SetExpires(input.Expires).SignAlg(false).SetKeyID("wimse")
			})
		if err != nil {
			return nil, err
		}
		sigInput, sig, err := httpsign.SignRequest("wimse", *signer, req)
		return map[string]string{"signature-input": sigInput, "signature": sig}, err
	case "verify":
		public, ok := input.PublicKey.Key.(*ecdsa.PublicKey)
		if !ok {
			return nil, fmt.Errorf("expected a P-256 proof key")
		}
		verifier, err := httpsign.NewP256Verifier(*public, httpsign.NewVerifyConfig().SetKeyID("wimse"),
			httpsign.Headers(input.Fields...))
		if err != nil {
			return nil, err
		}
		return map[string]string{}, httpsign.VerifyRequest("wimse", *verifier, req)
	default:
		return nil, fmt.Errorf("unsupported operation")
	}
}

func main() {
	var input request
	if err := json.NewDecoder(os.Stdin).Decode(&input); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	result, err := run(input)
	if err != nil {
		result = map[string]string{"denied": err.Error()}
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
}
