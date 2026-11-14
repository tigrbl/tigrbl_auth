// The build harness imports key.rs from the pinned wimsey checkout.
use std::io;
use std::path::Path;

use serde_json::{json, Value};
use wimsey_wpt::{txn_token_thumbprint, other_token_entry, wit_thumbprint, Validation, WptClaims};

type Result<T> = std::result::Result<T, Box<dyn std::error::Error + Send + Sync>>;

fn bridge(request: &Value) -> Result<Value> {
    let field = |name: &str| request[name].as_str().unwrap_or_default();
    let wit = field("wit");
    let audience = field("audience");
    let now = request["now"].as_u64().ok_or("missing clock")?;
    let transaction = request["transaction"].as_str();
    let other = request["context"].as_str();
    let context_header = "x-destination-access-token";
    let result = match field("command") {
        "sign" => {
            let key = key::load(Path::new(field("key")))?.signing_key()?;
            let claims = WptClaims {
                aud: audience.to_owned(),
                exp: now + 60,
                jti: field("jti").to_owned(),
                wth: wit_thumbprint(wit),
                tth: transaction.map(txn_token_thumbprint),
                oth: other.map(|value| [other_token_entry(context_header, value)].into()),
            };
            json!({"proof": wimsey_wpt::issue(&claims, &key)?})
        }
        "verify" => {
            let issuer = key::load(Path::new(field("key")))?.verifying_key()?;
            let credential = wimsey_wit::verify(wit, &issuer, &wimsey_wit::Validation::at(now))?;
            let mut validation = Validation::new(now, audience, wit).with_max_lifetime(300);
            if let Some(value) = transaction {
                validation = validation.with_txn_token(value);
            }
            if let Some(value) = other {
                validation = validation.with_other_token(context_header, value);
            }
            let proof = wimsey_wpt::verify(field("proof"), &credential.pop_key, &validation)?;
            if other.is_some() && !proof.claims.oth.as_ref().is_some_and(|claims| claims.contains_key(context_header)) {
                return Err("WPT additional token binding is missing".into());
            }
            json!({"sub": credential.claims.sub, "jti": proof.claims.jti, "exp": proof.claims.exp})
        }
        _ => return Err("unsupported command".into()),
    };
    Ok(result)
}

fn main() -> Result<()> {
    let request = serde_json::from_reader(io::stdin().lock())?;
    let response = match bridge(&request) {
        Ok(value) => value,
        Err(error) => json!({"denied": error.to_string()}),
    };
    println!("{response}");
    Ok(())
}
