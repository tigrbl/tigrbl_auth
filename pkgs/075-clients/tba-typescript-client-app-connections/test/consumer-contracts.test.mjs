import assert from "node:assert/strict";
import { test } from "node:test";
import {
  AppConnectionsHttpError,
  createAppConnectionsClient,
  createJsonAppConnectionsTransport,
} from "../dist/index.js";

const techmodPath = request => "/api/mcp/authorize/" + encodeURIComponent(request);
const unuiPath = "/auth/mcp/authorize";
const decision = { approved: true, botId: "bot-1", scopes: ["journal:read"] };
const redirect = "https://registered.example/callback?code=example";

function wireTransport(baseUrl, fixtures) {
  const pending = [...fixtures];
  const transport = createJsonAppConnectionsTransport({
    baseUrl,
    getHeaders: () => ({ "x-test-browser-session": "fixture" }),
    fetch: async (url, init) => {
      const expected = pending.shift();
      assert.ok(expected, `Unexpected request ${init.method} ${url}`);
      assert.equal(url, expected.url);
      assert.equal(init.method, expected.method);
      assert.equal(init.cache, "no-store");
      assert.equal(init.redirect, "error");
      assert.equal(init.credentials, "same-origin");
      assert.equal(init.headers.get("x-test-browser-session"), "fixture");
      assert.equal(init.headers.get("accept"), "application/json");
      if (expected.signal) assert.equal(init.signal, expected.signal);
      if (expected.body) {
        assert.equal(init.headers.get("content-type"), "application/json");
        assert.deepEqual(JSON.parse(init.body), expected.body);
      } else {
        assert.equal(init.body, undefined);
      }
      return Response.json(expected.response, { status: expected.status ?? 200 });
    },
  });
  return { transport, done: () => assert.equal(pending.length, 0) };
}

test("Techmod opaque consent requests and account connections", async () => {
  const signal = new AbortController().signal;
  const request = "opaque request";
  const path = "/api/mcp/authorize/opaque%20request";
  const read = { id: "journal:read", label: "Read journal", status: "requested" };
  const bot = { id: "bot-1", name: "Reporter", permissions: [read], bylineLabel: "Reporter bot" };
  const { transport, done } = wireTransport("", [
    { url: path, method: "GET", signal, response: {
      clientId: "editor", clientName: "Editor", resource: "https://journal.example/mcp",
      permissions: [read], bots: [bot],
    } },
    { url: path, method: "POST", body: { approve: true, botId: "bot-1", scopes: ["journal:read"] },
      response: { redirectUrl: redirect } },
    { url: "/api/mcp/account", method: "GET", response: { enabled: true, bots: [bot], connections: [
      { id: "connection-1", clientName: "Editor", scopes: ["journal:read"], bot_id: "bot-1" },
    ] } },
    { url: "/api/mcp/connections/connection-1", method: "DELETE", response: { revoked: true } },
  ]);
  const client = createAppConnectionsClient({
    getConsent: key => ({ path: techmodPath(key), read: response => response }),
    decideConsent: (key, { approved, botId, scopes }) => ({
      path: techmodPath(key),
      body: { approve: approved, botId, scopes },
      read: response => response,
    }),
    listConnections: () => ({
      path: "/api/mcp/account",
      read: response => response.connections.map(({ bot_id, ...connection }) => ({ ...connection, botId: bot_id })),
    }),
    revokeConnection: id => ({ path: "/api/mcp/connections/" + encodeURIComponent(id), read: response => response.revoked }),
  }, transport);

  assert.deepEqual((await client.getConsent(request, signal)).bots, [bot]);
  assert.deepEqual(await client.decideConsent(request, decision), { redirectUrl: redirect });
  assert.deepEqual(await client.listConnections(), [
    { id: "connection-1", clientName: "Editor", scopes: ["journal:read"], botId: "bot-1" },
  ]);
  assert.equal(await client.revokeConnection("connection-1"), true);
  done();
});

test("UNUI query consent, denial, and connection timestamps", async () => {
  const input = { client_id: "forum-editor", state: "forum request" };
  const read = { id: "forum:read", label: "Read forum", status: "requested" };
  const bot = { id: "bot-2", name: "Forum helper", category_ids: ["support"], permissions: [read] };
  const denied = "https://registered.example/callback?error=access_denied";
  const expiresAt = "2026-12-01T00:00:00+00:00";
  const { transport, done } = wireTransport("/forum-api/", [
    { url: "/forum-api/auth/mcp/authorize?client_id=forum-editor&state=forum+request", method: "GET", response: {
      client: { client_id: "forum-editor", client_name: "Forum editor", redirect_uri: "https://registered.example/callback" },
      resource: "https://forum.example/mcp", scopes: ["forum:read"], permissions: [read], bots: [bot],
      connection_lifetime_days: 30,
    } },
    { url: "/forum-api/auth/mcp/authorize", method: "POST",
      body: { ...input, approved: true, bot_id: "bot-2", approved_scopes: ["forum:read"] },
      response: { redirect_url: redirect } },
    { url: "/forum-api/auth/mcp/authorize", method: "POST",
      body: { ...input, approved: false, bot_id: null, approved_scopes: [] },
      response: { redirect_url: denied } },
    { url: "/forum-api/auth/mcp/connections", method: "GET", response: { connections: [
      { id: "connection-2", client_name: "Forum editor", scopes: ["forum:read"], bot_id: null, expires_at: expiresAt },
    ] } },
    { url: "/forum-api/auth/mcp/connections/connection-2", method: "DELETE", response: { revoked: true } },
  ]);
  const client = createAppConnectionsClient({
    getConsent: parameters => ({
      path: unuiPath + "?" + new URLSearchParams(parameters),
      read: ({ client, ...consent }) => ({
        ...consent,
        clientName: client.client_name,
        clientId: client.client_id,
        redirectUri: client.redirect_uri,
      }),
    }),
    decideConsent: (parameters, { approved, botId, scopes }) => ({
      path: unuiPath,
      body: { ...parameters, approved, bot_id: botId, approved_scopes: scopes },
      read: ({ redirect_url }) => ({ redirectUrl: redirect_url }),
    }),
    listConnections: () => ({
      path: "/auth/mcp/connections",
      read: ({ connections }) => connections.map(({ client_name, bot_id, ...connection }) => ({
        ...connection, clientName: client_name, botId: bot_id,
      })),
    }),
    revokeConnection: id => ({ path: "/auth/mcp/connections/" + encodeURIComponent(id), read: response => response.revoked }),
  }, transport);

  const consent = await client.getConsent(input);
  assert.deepEqual(consent.bots, [bot]);
  assert.equal(consent.redirectUri, "https://registered.example/callback");
  assert.equal(consent.connection_lifetime_days, 30);
  assert.deepEqual(await client.decideConsent(input, { approved: true, botId: "bot-2", scopes: ["forum:read"] }), {
    redirectUrl: redirect,
  });
  assert.deepEqual(await client.decideConsent(input, { approved: false, botId: null, scopes: [] }), {
    redirectUrl: denied,
  });
  assert.deepEqual(await client.listConnections(), [
    { id: "connection-2", clientName: "Forum editor", scopes: ["forum:read"], botId: null, expires_at: expiresAt },
  ]);
  assert.equal(await client.revokeConnection("connection-2"), true);
  done();
});

test("HTTP errors preserve status and provider message", async () => {
  const { transport, done } = wireTransport("", [{
    url: "/auth/mcp/connections/missing", method: "DELETE", status: 404,
    response: { error: "not_found", error_description: "Connection not found" },
  }]);
  await assert.rejects(transport({ path: "/auth/mcp/connections/missing", method: "DELETE" }), error => {
    assert.ok(error instanceof AppConnectionsHttpError);
    assert.equal(error.status, 404);
    assert.equal(error.message, "Connection not found");
    return true;
  });
  done();
});

test("transport rejects requests outside the configured API path", async () => {
  const { transport, done } = wireTransport("", []);
  for (const path of ["https://outside.example/path", "//outside.example/path", "/\\outside.example/path"]) {
    await assert.rejects(transport({ path, method: "GET" }), TypeError);
  }
  done();
});
