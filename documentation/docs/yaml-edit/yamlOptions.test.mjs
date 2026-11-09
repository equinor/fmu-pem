import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import YAML from "yaml";

import { configYamlOptions } from "./yamlOptions.mjs";

test("parses underscore-separated decimal numbers, including nested values", () => {
  const parsed = YAML.parse(
    `bulk_modulus: 25_000_000_000.0
count: 1_000
values: [-1_234.5, +1_000, 1_250.0e+3, 0.000_001]
`,
    configYamlOptions,
  );
  assert.deepEqual(parsed, {
    bulk_modulus: 25_000_000_000,
    count: 1000,
    values: [-1234.5, 1000, 1_250_000, 0.000001],
  });
  assert.deepEqual(
    YAML.parse(YAML.stringify(parsed, configYamlOptions), configYamlOptions),
    parsed,
  );
});

test("preserves strings and YAML 1.2 scalar behavior through export and reload", () => {
  const parsed = YAML.parse(
    `quoted: "25_000_000_000.0"
single_quoted: '1_000'
file_name: grid_1_000.roff
label: shale_matrix
enabled: true
disabled: False
word: on
date: 2026-11-09
leading_zero: 012
time: 12:34:56
`,
    configYamlOptions,
  );
  assert.deepEqual(parsed, {
    quoted: "25_000_000_000.0",
    single_quoted: "1_000",
    file_name: "grid_1_000.roff",
    label: "shale_matrix",
    enabled: true,
    disabled: false,
    word: "on",
    date: "2026-11-09",
    leading_zero: 12,
    time: "12:34:56",
  });
  assert.deepEqual(
    YAML.parse(YAML.stringify(parsed, configYamlOptions), configYamlOptions),
    parsed,
  );
});

test("loads mineral moduli from the condensate example as numbers", () => {
  const source = readFileSync(
    new URL(
      "../../../tests/data/sim2seis/model/pem_config_condensate.yml",
      import.meta.url,
    ),
    "utf8",
  );
  const parsed = YAML.parse(source, configYamlOptions);
  assert.equal(parsed.rock_matrix.minerals.shale.bulk_modulus, 25_000_000_000);
  assert.equal(parsed.rock_matrix.minerals.quartz.shear_modulus, 44_000_000_000);
  for (const mineral of Object.values(parsed.rock_matrix.minerals)) {
    assert.equal(typeof mineral.bulk_modulus, "number");
    assert.equal(typeof mineral.shear_modulus, "number");
  }
});
