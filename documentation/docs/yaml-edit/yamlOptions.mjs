import YAML from "yaml";

// Accept Python-style decimal separators without enabling YAML 1.1 booleans,
// timestamps, octal numbers, or sexagesimal numbers.
export const configYamlOptions = {
  customTags: new YAML.Schema({ schema: "yaml-1.1" }).tags.filter(
    (tag) =>
      (tag.tag === "tag:yaml.org,2002:int" ||
        tag.tag === "tag:yaml.org,2002:float") &&
      (tag.format === undefined || tag.format === "EXP"),
  ),
};
