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

import { TranslatableString, englishStringTranslator, replaceStringParameters, getUiOptions, type TitleFieldProps, type ArrayFieldTemplateProps } from '@rjsf/utils';

function customStrings(stringToTranslate: TranslatableString, params?: string[]): string {
  if(stringToTranslate === TranslatableString.KeyLabel) {
    return replaceStringParameters('Key:', params);
  }
  return englishStringTranslator(stringToTranslate, params);
}

// VitePress flattens RJSF's default field titles, so render them as explicit headings.
function TitleFieldTemplate({ id, title, required }: Pick<TitleFieldProps, "id" | "title" | "required">) {
  if (!title) {
    return null;
  }
  return (
    <div
      id={id}
      className="rjsf-field-title"
      style={{
        fontSize: "1.15rem",
        fontWeight: 700,
        marginTop: "1.5rem",
        marginBottom: "0.5rem",
        paddingBottom: "0.25rem",
        borderBottom: "1px solid var(--vp-c-divider, #e2e2e3)",
      }}
    >
      {title}
      {required ? " *" : null}
    </div>
  );
}

// Arrays whose items are a discriminated `oneOf` (e.g. `pressure`) do not render
// their array-level title until the first item is added, unlike arrays of a
// single `$ref` (e.g. `zone_regions`). Give such arrays a template that always
// renders the title heading up front, matching the `zone_regions` appearance.
function TitledArrayFieldTemplate(props: ArrayFieldTemplateProps) {
  const {
    canAdd,
    className,
    disabled,
    fieldPathId,
    uiSchema,
    items,
    onAddClick,
    readonly,
    registry,
    required,
    schema,
    title,
  } = props;
  const uiOptions = getUiOptions(uiSchema);
  const displayTitle = uiOptions.title || title;
  const description = uiOptions.description || schema.description;
  const {
    ButtonTemplates: { AddButton },
  } = registry.templates;
  const baseId = fieldPathId?.$id ?? "array";
  return (
    <fieldset className={className} id={fieldPathId?.$id}>
      {displayTitle ? (
        <TitleFieldTemplate
          id={`${baseId}__title`}
          title={displayTitle}
          required={required}
        />
      ) : null}
      {description ? (
        <p className="field-description" style={{ marginBottom: "0.5rem" }}>
          {description}
        </p>
      ) : null}
      <div className="row array-item-list">
        {items &&
          items.map((element: any, index: number) =>
            React.isValidElement(element) ? (
              element
            ) : (
              <div key={element?.key ?? index}>{element?.children}</div>
            ),
          )}
      </div>
      {canAdd ? (
        <AddButton
          id={`${baseId}__add`}
          className="rjsf-array-item-add"
          onClick={onAddClick}
          disabled={disabled || readonly}
          uiSchema={uiSchema}
          registry={registry}
        />
      ) : null}
    </fieldset>
  );
}

export const YamlEdit = () => {
  const [validInput, setValidInput] = React.useState(false);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [snackbarOpen, setSnackbarOpen] = React.useState(false);

  // Each time user reads YAML from disk, we remount the Form component
  // by setting key to an integer increasing by 1 on each read. The Form component
  // otherwise does not react to change in initial formData.
  const [numberRead, setNumberRead] = React.useState(0)

  const [initialConfig, setInitialConfig] = React.useState(() => {
    const savedFormData = sessionStorage.getItem('formData');
    if (savedFormData) {
      try {
        return JSON.parse(savedFormData);
      } catch (error) {
        console.error('Failed to parse saved form data:', error);
        return {};
      }
    }
    return {};
  });

  const userInputRef = React.useRef(initialConfig);

  React.useEffect(() => {
    // Clear session storage when the user reloads same tab
    const handleBeforeUnload = () => {
      sessionStorage.removeItem('formData');
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

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
                setNumberRead(() => numberRead + 1);
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

      </div>
      <div className="flex justify-center my-20">
        <div className="p-10 shadow-lg rounded bg-slate-50 border-2 border-slate-50" style={{minWidth: 800}}>
          <Form
            key={numberRead}
            schema={pemSchema}
            validator={validator}
            formData={initialConfig}
            onChange={(event) => {
              userInputRef.current = event.formData;
              sessionStorage.setItem('formData', JSON.stringify(event.formData));

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
            omitExtraData
            liveOmit
            templates={{ TitleFieldTemplate }}
            uiSchema={{
              "ui:submitButtonOptions": { norender: true },
              "ui:globalOptions": {
                enableMarkdownInDescription: true,
              },
              // Hide discriminator fields from UI - users select via dropdown, not by editing these
              rock_matrix: {
                zone_regions: {
                  items: {
                    model: {
                      model_name: { "ui:widget": "hidden" },
                      parameters: {
                        // RegressionModels discriminators
                        sandstone: { mode: { "ui:widget": "hidden" } },
                        shale: { mode: { "ui:widget": "hidden" } },
                      },
                    },
                    pressure_sensitivity_model: {
                      sensitivity_type: { "ui:widget": "hidden" },
                      // RegressionPressureSensitivity nested discriminators
                      parameterisation: {
                        mode: { "ui:widget": "hidden" },
                        function: {
                          function_type: { "ui:widget": "hidden" },
                        },
                      },
                      // PhysicsModelPressureSensitivity discriminator
                      parameters: {
                        param_type: { "ui:widget": "hidden" },
                      },
                    },
                  },
                },
              },
              // The pressure array items are a discriminated `oneOf`; use a
              // template that always renders the array title heading up front.
              pressure: {
                "ui:ArrayFieldTemplate": TitledArrayFieldTemplate,
              },
            }}
            showErrorList={false}
            translateString={customStrings}
          />
        </div>
      </div>
    </div>
  );
}
