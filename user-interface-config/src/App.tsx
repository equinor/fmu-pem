import Form from "@rjsf/core";

import YAML from "yaml";
import validator from "@rjsf/validator-ajv8";

import {
  Button,
  Icon,
  Dialog,
  TextField,
  Snackbar,
  Switch
} from "@equinor/eds-core-react";
import { upload, file_description, copy } from "@equinor/eds-icons";

import { pemSchema } from "./schema";
import React from "react";

function App() {
  const [validInput, setValidInput] = React.useState(false);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [snackbarOpen, setSnackbarOpen] = React.useState(false);
  const [populateDefault, setPopulateDefault] = React.useState(false);

  const [initialConfig, setInitialConfig] = React.useState({});

  const userInputRef = React.useRef({});

  const yamlOutput =
    (validInput ? "" : "# This YAML file is not complete/valid\n\n") +
    YAML.stringify(userInputRef.current);

  return (
    <div className="min-h-screen min-w-screen bg-slate-100">
      <div className="bg-slate-700 p-4 flex gap-20 items-center shadow-md">
        <div className="text-white">
          Create, update or change a <span className="font-bold">fmu-pem</span>{" "}
          configuration file. You can load an existing configuration file as
          starting point.
        </div>
      </div>
      <div className="flex w-full justify-center my-10 gap-10">
        <Button
          as="button"
          color="secondary"
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
          <Icon data={upload} size={16}></Icon>
          Load existing configuration file (YAML)
        </Button>
        <Button as="button" color="primary" onClick={() => setDialogOpen(true)}>
          <Icon data={file_description} size={16}></Icon>
          Configuration file output (YAML)
        </Button>
        <Dialog
          open={dialogOpen}
          onClose={() => {
            setDialogOpen(false);
            setSnackbarOpen(false);
          }}
          isDismissable={true}
          className="w-100"
        >
          <Dialog.Header>
            <Dialog.Title>YAML output</Dialog.Title>
          </Dialog.Header>
          <Dialog.CustomContent className="min-w-[600px]">
            <TextField
              id="yaml-content"
              multiline={true}
              placeholder={yamlOutput}
              rowsMax={50}
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
        <Switch label="Populate with default values" onChange={(e) => setPopulateDefault(e.target.checked)} />

      </div>
      <div className="flex justify-center my-20">
        <div className="p-10 shadow-lg rounded bg-slate-50 min-w-[800px]">
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
            }}
            showErrorList={false}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
