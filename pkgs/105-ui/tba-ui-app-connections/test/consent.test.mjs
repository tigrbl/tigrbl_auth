import assert from "node:assert/strict";
import { test } from "node:test";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { ConsentIdentityControls, defaultConsentScopes } from "../dist/index.js";

const read = { id: "read", label: "Read", status: "requested" };
const editorial = { id: "editorial", label: "Editorial", status: "requested", explicit: true };
const write = { id: "write", label: "Write", status: "available_to_request" };
const props = {
  accountName: "Editor",
  permissions: [read, editorial, write],
  bots: [{ id: "bot-1", name: "Reporter", permissions: [read] }],
  value: { botId: "bot-1", scopes: ["read", "editorial"] },
  title: "Permissions",
};

test("consent defaults exclude scopes requiring explicit approval", () => {
  assert.deepEqual(defaultConsentScopes(props.permissions), ["read"]);
});

test("selecting a bot clears account scopes the bot did not request", () => {
  const changes = [];
  const controls = ConsentIdentityControls({
    ...props,
    value: { ...props.value, botId: "" },
    onChange: selection => changes.push(selection),
  });
  controls.props.children[0].props.onChange("bot-1");
  assert.deepEqual(changes, [{ botId: "bot-1", scopes: ["read"] }]);
});

test("refreshing a bot cannot retain previously selected scopes it no longer requests", () => {
  const changes = [];
  const controls = ConsentIdentityControls({
    ...props,
    onChange: selection => changes.push(selection),
  });
  const matrix = controls.props.children[1];
  assert.deepEqual(matrix.props.selected, ["read"]);
  matrix.props.onChange(["read", "editorial"]);
  assert.deepEqual(changes, [{ botId: "bot-1", scopes: ["read"] }]);
});

test("the selected identity displays only its own permission matrix", () => {
  const markup = renderToStaticMarkup(createElement(ConsentIdentityControls, {
    ...props, onChange: () => {},
  }));
  assert.match(markup, /Reporter · Bot/);
  assert.match(markup, /Read/);
  assert.doesNotMatch(markup, /Editorial|Write/);
  assert.doesNotMatch(renderToStaticMarkup(createElement(ConsentIdentityControls, {
    ...props, value: { ...props.value, botId: "missing" }, onChange: () => {},
  })), /Editorial|Write|Read/);
});
