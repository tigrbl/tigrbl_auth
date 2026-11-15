import { createHash, createPrivateKey, createPublicKey } from 'node:crypto';
import { readFileSync, writeFileSync, copyFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

if (process.argv[2] === 'build') {
  const [, , , checkout, directory] = process.argv;
  const ts = (await import(pathToFileURL(join(checkout, 'node_modules/typescript/lib/typescript.js')))).default;
  const source = join(checkout, 'packages/server/src/identity');
  writeFileSync(join(directory, 'package.json'), '{"type":"module"}');
  for (const name of ['wimse', 'types', 'http-signature', 'structured-fields']) {
    const input = readFileSync(join(source, name + '.ts'), 'utf8');
    const compiled = ts.transpileModule(input, {
      compilerOptions: { module: ts.ModuleKind.ES2022, target: ts.ScriptTarget.ES2022 },
      reportDiagnostics: true,
    });
    if (compiled.diagnostics.some(item => item.category === ts.DiagnosticCategory.Error)) {
      throw new Error('Unable to compile the pinned Cred identity module ' + name);
    }
    writeFileSync(join(directory, name + '.js'), compiled.outputText);
  }
  const demo = join(checkout, 'scripts/hackathon/lib');
  const caller = readFileSync(join(demo, 'client.mjs'), 'utf8');
  writeFileSync(join(directory, 'client.mjs'), caller + '\nexport { signJws };\n');
  copyFileSync(join(demo, 'issuers.mjs'), join(directory, 'issuers.mjs'));
} else {
  const input = JSON.parse(readFileSync(0, 'utf8'));
  const digest = value => createHash('sha256').update(value, 'ascii').digest('base64url');
  let result;
  const trustConfig = () => ({
    trustDomains: Object.fromEntries(Object.entries(input.trust).map(([domain, keys]) =>
      [domain, new Map(keys.map(jwk => [jwk.kid, { key: createPublicKey({ key: jwk, format: 'jwk' }), alg: jwk.alg }]))])),
    now: () => input.now,
    clockSkewSec: 0,
  });
  if (input.command === 'sign-http') {
    const { signWimseRequest } = await import('./http-signature.js');
    const privateKey = createPrivateKey({ key: input.key, format: 'jwk' });
    result = { headers: signWimseRequest({
      method: input.method, path: input.path, headers: input.headers,
      wit: input.wit, privateKey, alg: input.key.alg, audience: input.audience, created: input.now,
    }) };
  } else if (input.command === 'verify-http') {
    const { verifyWimseRequestSignature } = await import('./http-signature.js');
    const { IdentityRefusal } = await import('./types.js');
    try {
      const proof = verifyWimseRequestSignature(
        { method: input.method, path: input.path, headers: input.headers },
        { ...trustConfig(), audiences: [input.audience] },
      );
      result = proof ? { sub: proof.wit.subject, nonce: proof.nonce, exp: proof.expires }
        : { denied: 'no tagged WIMSE signature' };
    } catch (error) {
      if (!(error instanceof IdentityRefusal)) throw error;
      result = { denied: error.code + ': ' + error.detail };
    }
  } else if (input.command === 'sign') {
    const { signJws } = await import('./client.mjs');
    const key = createPrivateKey({ key: input.key, format: 'jwk' });
    const claims = { aud: input.audience, exp: input.now + 60, jti: input.jti, wth: digest(input.wit) };
    if (input.transaction !== null) claims.tth = digest(input.transaction);
    if (input.context !== null) claims.oth = { [input.context_header]: digest(input.context.trim()) };
    result = { proof: signJws({ alg: input.key.alg, typ: 'wpt+jwt' }, claims, key) };
  } else if (input.command === 'verify') {
    const { verifyWit, verifyWpt } = await import('./wimse.js');
    const { IdentityRefusal } = await import('./types.js');
    try {
      const cfg = trustConfig();
      const wit = verifyWit(input.wit, cfg);
      const proof = verifyWpt(input.proof, wit, { headers: input.headers, targetUri: input.audience }, cfg);
      if (input.headers[input.context_header] !== undefined &&
          !Object.hasOwn(proof.claims.oth ?? {}, input.context_header)) {
        throw new IdentityRefusal('wimse', 'wpt_oth_missing', 'required context token has no binding');
      }
      result = { sub: wit.subject, jti: proof.jti, exp: proof.exp };
    } catch (error) {
      if (!(error instanceof IdentityRefusal)) throw error;
      result = { denied: error.code + ': ' + error.detail };
    }
  } else {
    throw new Error('Unknown bridge operation');
  }
  process.stdout.write(JSON.stringify(result) + '\n');
}
