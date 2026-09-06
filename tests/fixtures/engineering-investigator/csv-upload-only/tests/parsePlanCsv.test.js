import test from "node:test";
import assert from "node:assert/strict";
import { parsePlanCsv } from "../src/imports/parsePlanCsv.js";

const enc = (s) => new TextEncoder().encode(s);

test("parses a well-formed sheet", () => {
  const { rows, errors } = parsePlanCsv(
    enc("plan_code,name,monthly_price,seats\nteam,Team,49,10\n"),
  );
  assert.deepEqual(errors, []);
  assert.deepEqual(rows, [{ planCode: "team", name: "Team", monthlyPrice: 49, seats: 10 }]);
});

test("reports every bad row, not just the first", () => {
  const { rows, errors } = parsePlanCsv(
    enc("plan_code,name,monthly_price,seats\n,A,1,1\nb,B,x,1\nc,C,1,1\n"),
  );
  assert.equal(rows.length, 1);
  assert.equal(errors.length, 2);
});

test("rejects a sheet with missing columns", () => {
  const { errors } = parsePlanCsv(enc("plan_code,name\nteam,Team\n"));
  assert.match(errors[0], /missing columns/);
});
