import React from "react";
import Form from "@rjsf/core";
import YAML from "yaml";
import validator from "@rjsf/validator-ajv8";

import { pemSchema } from "./schema";

import {
  Button,
  Icon,
  Dialog,
  TextField,
  Snackbar,
  Switch
} from "@equinor/eds-core-react";

import { copy } from "@equinor/eds-icons";

import { TranslatableString, englishStringTranslator, replaceStringParameters } from '@rjsf/utils';

// Workaround since the signature of translateString from rjsf does not provide us information about where we are in the schema
const whereAreWeInSchema = {
  inMineralSection: false,
  inDiffCalculationSection: false,
} 
function domainSpecificStrings(stringToTranslate: TranslatableString, params?: string[]): string {
  if(stringToTranslate === TranslatableString.KeyLabel && params && params.length > 0 && params[0].length > 0) {
    if(params[0] === "PemConfig"){
      whereAreWeInSchema.inMineralSection = false; // Reset the state when we are in the top level;
    } else if(params[0] === "Minerals") {
      whereAreWeInSchema.inMineralSection = true; // We are in the mineral section
    } else if(params[0] === "VolumeFractions") {
      whereAreWeInSchema.inMineralSection = true; // We are finished with the mineral section
    } else if(params[0] === "Diff Calculation") {
      whereAreWeInSchema.inDiffCalculationSection = true; // We are in the diff calculation section
    }

    if(whereAreWeInSchema.inMineralSection){
      return replaceStringParameters('Mineral:', params); // Add "Name" onto the end of the WrapIfAdditionalTemplate key label
    }
    if(whereAreWeInSchema.inDiffCalculationSection){
      return replaceStringParameters('Parameter:', params); // Add "Name" onto the end of the WrapIfAdditionalTemplate key label
    }
  }
  
  return englishStringTranslator(stringToTranslate, params); // Fallback to the default english
}

export const YamlEdit = () => {
  const [validInput, setValidInput] = React.useState(false);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [snackbarOpen, setSnackbarOpen] = React.useState(false);
  const [populateDefault, setPopulateDefault] = React.useState(true);

  const [initialConfig, setInitialConfig] = React.useState({});

  const userInputRef = React.useRef({});

  const yamlOutput =
    (validInput ? "" : "# This YAML file is not complete/valid\n\n") +
    YAML.stringify(userInputRef.current);

  return (
    <div>
      <div className="flex w-full justify-center my-10 gap-10">
        <button
          className="flex gap-2 font-bold items-center shadow p-1 rounded-lg bg-gray-100 hover:bg-gray-50 dark:bg-gray-800"
          onClick={() => {
            const input = document.createElement("input");
            input.type = "file";
            input.accept=".yml,.yaml"

            input.onchange = (e) => {
              if(e.target == null || !(e.target instanceof HTMLInputElement) || e.target.files == null){
                return
              }
              const file = e.target.files[0];
              const reader = new FileReader();
              reader.readAsText(file);

              reader.onload = (readerEvent) => {
                if(readerEvent.target == null){
                  console.error("No data target")
                  return
                }
                const content = readerEvent.target.result as string;
                setInitialConfig(YAML.parse(content));
              };
            };
            input.click();
          }}
        >
          Load config (YAML)
        </button>
        <button
          className="flex gap-2 font-bold items-center shadow p-1 rounded-lg bg-gray-100 hover:bg-gray-50" onClick={() => setDialogOpen(true)}>
          Config output (YAML)
        </button>
        <Dialog
          open={dialogOpen}
          onClose={() => {
            setDialogOpen(false);
            setSnackbarOpen(false);
          }}
          isDismissable={true}
          style={{width: 1000, maxHeight: "90vh"}}
        >
          <Dialog.Header>
            <Dialog.Title>YAML output</Dialog.Title>
          </Dialog.Header>
          <Dialog.CustomContent>
            <TextField
              id="yaml-content"
              multiline={true}
              placeholder={yamlOutput}
              rowsMax={35}
              readOnly={true}
            />
            <Button
              type="button"
              onClick={() => {
                navigator.clipboard.writeText(yamlOutput);
                setSnackbarOpen(true);
              }}
              className="mt-4"
            >
              <Icon data={copy} size={16}></Icon>
              Copy to clipboard
            </Button>
            <Snackbar
              open={snackbarOpen}
              onClose={() => setSnackbarOpen(false)}
            >
              YAML configuration file copied to clipboard
            </Snackbar>
          </Dialog.CustomContent>
        </Dialog>
        <Switch label="Populate with default values" checked={populateDefault} onChange={(e) => setPopulateDefault(e.target.checked)} />

      </div> 
      <div className="flex justify-center my-20">
        <div className="p-10 shadow-lg rounded bg-slate-50 border-2 border-slate-50" style={{minWidth: 800}}>
          <Form
            schema={pemSchema}
            validator={validator}
            formData={initialConfig}
            experimental_defaultFormStateBehavior={{
              emptyObjectFields: populateDefault ? "populateAllDefaults" : "skipDefaults",
            }}
            onChange={(event) => {
              userInputRef.current = event.formData;
              if (
                event.errors.length === 0 &&
                // @ts-ignore
                event.schemaValidationErrors !== undefined
              ) {
                setValidInput(true);
              } else {
                setValidInput(false);
              }
            }}
            liveValidate
            uiSchema={{
              "ui:submitButtonOptions": { norender: true },
              "ui:globalOptions": {
                enableMarkdownInDescription: true,
              },
            }}
            showErrorList={false}
            translateString={domainSpecificStrings}
          />
        </div>
      </div>
    </div>
  );
}
