import {
  ADDITIONAL_PROPERTY_FLAG,
  ANY_OF_KEY,
  CONST_KEY,
  DEFAULT_KEY,
  ERRORS_KEY,
  ID_KEY,
  ITEMS_KEY,
  NAME_KEY,
  ONE_OF_KEY,
  PROPERTIES_KEY,
  READONLY_KEY,
  REF_KEY,
  RJSF_ADDITIONAL_PROPERTIES_FLAG,
  SUBMIT_BTN_OPTIONS_KEY,
  SetCache_default,
  TranslatableString,
  UI_GLOBAL_OPTIONS_KEY,
  UI_OPTIONS_KEY,
  allowAdditionalItems,
  ariaDescribedByIds,
  arrayIncludesWith_default,
  arrayIncludes_default,
  arrayMap_default,
  asNumber,
  baseIndexOf_default,
  basePickBy_default,
  baseRest_default,
  baseUnary_default,
  baseUnset_default,
  buttonId,
  cacheHas_default,
  canExpand,
  cloneDeep_default,
  createErrorHandler,
  createSchemaUtils,
  dataURItoBlob,
  dateRangeOptions,
  deepEquals,
  descriptionId,
  englishStringTranslator,
  enumOptionsDeselectValue,
  enumOptionsIndexForValue,
  enumOptionsIsSelected,
  enumOptionsSelectValue,
  enumOptionsValueForIndex,
  errorId,
  examplesId,
  flatRest_default,
  flatten_default,
  forEach_default,
  getChangedFields,
  getDateElementProps,
  getDiscriminatorFieldFromSchema,
  getInputProps,
  getSchemaType,
  getSubmitButtonOptions,
  getTemplate,
  getTestIds,
  getUiOptions,
  getWidget,
  get_default,
  hasIn_default,
  hasWidget,
  has_default,
  hashObject,
  helpId,
  isArrayLikeObject_default,
  isArrayLike_default,
  isCustomWidget,
  isEmpty_default,
  isEqual_default,
  isFixedItems,
  isFunction_default,
  isNil_default,
  isObject,
  isObject_default,
  isPlainObject_default,
  isString_default,
  keys_default,
  labelValue,
  localToUTC,
  lookupFromFormContext,
  mergeObjects,
  mergeSchemas,
  nanoid,
  noop_default,
  omit_default,
  optionId,
  optionsList,
  orderProperties,
  parseDateString,
  schemaRequiresTrueValue,
  set_default,
  shouldRender,
  titleId,
  toDateString,
  toErrorList,
  toInteger_default,
  toPath_default,
  unwrapErrorHandler,
  utcToLocal,
  validationDataMerge
} from "./chunk-6WCUV5VP.js";
import {
  require_jsx_runtime
} from "./chunk-LPWVGVNP.js";
import {
  require_react
} from "./chunk-6FYWT56J.js";
import {
  __publicField,
  __toESM
} from "./chunk-DC5AMYBS.js";

// node_modules/@rjsf/core/lib/components/Form.js
var import_jsx_runtime53 = __toESM(require_jsx_runtime(), 1);
var import_react22 = __toESM(require_react(), 1);

// node_modules/lodash-es/_basePick.js
function basePick(object, paths) {
  return basePickBy_default(object, paths, function(value, path) {
    return hasIn_default(object, path);
  });
}
var basePick_default = basePick;

// node_modules/lodash-es/pick.js
var pick = flatRest_default(function(object, paths) {
  return object == null ? {} : basePick_default(object, paths);
});
var pick_default = pick;

// node_modules/@rjsf/core/lib/components/fields/ArrayField.js
var import_jsx_runtime = __toESM(require_jsx_runtime(), 1);
var import_react = __toESM(require_react(), 1);
function generateRowId() {
  return nanoid();
}
function generateKeyedFormData(formData) {
  return !Array.isArray(formData) ? [] : formData.map((item) => {
    return {
      key: generateRowId(),
      item
    };
  });
}
function keyedToPlainFormData(keyedFormData) {
  if (Array.isArray(keyedFormData)) {
    return keyedFormData.map((keyedItem) => keyedItem.item);
  }
  return [];
}
var ArrayField = class extends import_react.Component {
  /** Constructs an `ArrayField` from the `props`, generating the initial keyed data from the `formData`
   *
   * @param props - The `FieldProps` for this template
   */
  constructor(props) {
    super(props);
    /** Returns the default form information for an item based on the schema for that item. Deals with the possibility
     * that the schema is fixed and allows additional items.
     */
    __publicField(this, "_getNewFormDataRow", () => {
      const { schema, registry } = this.props;
      const { schemaUtils } = registry;
      let itemSchema = schema.items;
      if (isFixedItems(schema) && allowAdditionalItems(schema)) {
        itemSchema = schema.additionalItems;
      }
      return schemaUtils.getDefaultFormState(itemSchema);
    });
    /** Callback handler for when the user clicks on the add button. Creates a new row of keyed form data at the end of
     * the list, adding it into the state, and then returning `onChange()` with the plain form data converted from the
     * keyed data
     *
     * @param event - The event for the click
     */
    __publicField(this, "onAddClick", (event) => {
      this._handleAddClick(event);
    });
    /** Callback handler for when the user clicks on the add button on an existing array element. Creates a new row of
     * keyed form data inserted at the `index`, adding it into the state, and then returning `onChange()` with the plain
     * form data converted from the keyed data
     *
     * @param index - The index at which the add button is clicked
     */
    __publicField(this, "onAddIndexClick", (index) => {
      return (event) => {
        this._handleAddClick(event, index);
      };
    });
    /** Callback handler for when the user clicks on the copy button on an existing array element. Clones the row of
     * keyed form data at the `index` into the next position in the state, and then returning `onChange()` with the plain
     * form data converted from the keyed data
     *
     * @param index - The index at which the copy button is clicked
     */
    __publicField(this, "onCopyIndexClick", (index) => {
      return (event) => {
        if (event) {
          event.preventDefault();
        }
        const { onChange, errorSchema } = this.props;
        const { keyedFormData } = this.state;
        let newErrorSchema;
        if (errorSchema) {
          newErrorSchema = {};
          for (const idx in errorSchema) {
            const i2 = parseInt(idx);
            if (i2 <= index) {
              set_default(newErrorSchema, [i2], errorSchema[idx]);
            } else if (i2 > index) {
              set_default(newErrorSchema, [i2 + 1], errorSchema[idx]);
            }
          }
        }
        const newKeyedFormDataRow = {
          key: generateRowId(),
          item: cloneDeep_default(keyedFormData[index].item)
        };
        const newKeyedFormData = [...keyedFormData];
        if (index !== void 0) {
          newKeyedFormData.splice(index + 1, 0, newKeyedFormDataRow);
        } else {
          newKeyedFormData.push(newKeyedFormDataRow);
        }
        this.setState({
          keyedFormData: newKeyedFormData,
          updatedKeyedFormData: true
        }, () => onChange(keyedToPlainFormData(newKeyedFormData), newErrorSchema));
      };
    });
    /** Callback handler for when the user clicks on the remove button on an existing array element. Removes the row of
     * keyed form data at the `index` in the state, and then returning `onChange()` with the plain form data converted
     * from the keyed data
     *
     * @param index - The index at which the remove button is clicked
     */
    __publicField(this, "onDropIndexClick", (index) => {
      return (event) => {
        if (event) {
          event.preventDefault();
        }
        const { onChange, errorSchema } = this.props;
        const { keyedFormData } = this.state;
        let newErrorSchema;
        if (errorSchema) {
          newErrorSchema = {};
          for (const idx in errorSchema) {
            const i2 = parseInt(idx);
            if (i2 < index) {
              set_default(newErrorSchema, [i2], errorSchema[idx]);
            } else if (i2 > index) {
              set_default(newErrorSchema, [i2 - 1], errorSchema[idx]);
            }
          }
        }
        const newKeyedFormData = keyedFormData.filter((_2, i2) => i2 !== index);
        this.setState({
          keyedFormData: newKeyedFormData,
          updatedKeyedFormData: true
        }, () => onChange(keyedToPlainFormData(newKeyedFormData), newErrorSchema));
      };
    });
    /** Callback handler for when the user clicks on one of the move item buttons on an existing array element. Moves the
     * row of keyed form data at the `index` to the `newIndex` in the state, and then returning `onChange()` with the
     * plain form data converted from the keyed data
     *
     * @param index - The index of the item to move
     * @param newIndex - The index to where the item is to be moved
     */
    __publicField(this, "onReorderClick", (index, newIndex) => {
      return (event) => {
        if (event) {
          event.preventDefault();
          event.currentTarget.blur();
        }
        const { onChange, errorSchema } = this.props;
        let newErrorSchema;
        if (errorSchema) {
          newErrorSchema = {};
          for (const idx in errorSchema) {
            const i2 = parseInt(idx);
            if (i2 == index) {
              set_default(newErrorSchema, [newIndex], errorSchema[index]);
            } else if (i2 == newIndex) {
              set_default(newErrorSchema, [index], errorSchema[newIndex]);
            } else {
              set_default(newErrorSchema, [idx], errorSchema[i2]);
            }
          }
        }
        const { keyedFormData } = this.state;
        function reOrderArray() {
          const _newKeyedFormData = keyedFormData.slice();
          _newKeyedFormData.splice(index, 1);
          _newKeyedFormData.splice(newIndex, 0, keyedFormData[index]);
          return _newKeyedFormData;
        }
        const newKeyedFormData = reOrderArray();
        this.setState({
          keyedFormData: newKeyedFormData
        }, () => onChange(keyedToPlainFormData(newKeyedFormData), newErrorSchema));
      };
    });
    /** Callback handler used to deal with changing the value of the data in the array at the `index`. Calls the
     * `onChange` callback with the updated form data
     *
     * @param index - The index of the item being changed
     */
    __publicField(this, "onChangeForIndex", (index) => {
      return (value, newErrorSchema, id) => {
        const { formData, onChange, errorSchema } = this.props;
        const arrayData = Array.isArray(formData) ? formData : [];
        const newFormData = arrayData.map((item, i2) => {
          const jsonValue = typeof value === "undefined" ? null : value;
          return index === i2 ? jsonValue : item;
        });
        onChange(newFormData, errorSchema && errorSchema && {
          ...errorSchema,
          [index]: newErrorSchema
        }, id);
      };
    });
    /** Callback handler used to change the value for a checkbox */
    __publicField(this, "onSelectChange", (value) => {
      const { onChange, idSchema } = this.props;
      onChange(value, void 0, idSchema && idSchema.$id);
    });
    const { formData = [] } = props;
    const keyedFormData = generateKeyedFormData(formData);
    this.state = {
      keyedFormData,
      updatedKeyedFormData: false
    };
  }
  /** React lifecycle method that is called when the props are about to change allowing the state to be updated. It
   * regenerates the keyed form data and returns it
   *
   * @param nextProps - The next set of props data
   * @param prevState - The previous set of state data
   */
  static getDerivedStateFromProps(nextProps, prevState) {
    if (prevState.updatedKeyedFormData) {
      return {
        updatedKeyedFormData: false
      };
    }
    const nextFormData = Array.isArray(nextProps.formData) ? nextProps.formData : [];
    const previousKeyedFormData = prevState.keyedFormData || [];
    const newKeyedFormData = nextFormData.length === previousKeyedFormData.length ? previousKeyedFormData.map((previousKeyedFormDatum, index) => {
      return {
        key: previousKeyedFormDatum.key,
        item: nextFormData[index]
      };
    }) : generateKeyedFormData(nextFormData);
    return {
      keyedFormData: newKeyedFormData
    };
  }
  /** Returns the appropriate title for an item by getting first the title from the schema.items, then falling back to
   * the description from the schema.items, and finally the string "Item"
   */
  get itemTitle() {
    const { schema, registry } = this.props;
    const { translateString } = registry;
    return get_default(schema, [ITEMS_KEY, "title"], get_default(schema, [ITEMS_KEY, "description"], translateString(TranslatableString.ArrayItemTitle)));
  }
  /** Determines whether the item described in the schema is always required, which is determined by whether any item
   * may be null.
   *
   * @param itemSchema - The schema for the item
   * @return - True if the item schema type does not contain the "null" type
   */
  isItemRequired(itemSchema) {
    if (Array.isArray(itemSchema.type)) {
      return !itemSchema.type.includes("null");
    }
    return itemSchema.type !== "null";
  }
  /** Determines whether more items can be added to the array. If the uiSchema indicates the array doesn't allow adding
   * then false is returned. Otherwise, if the schema indicates that there are a maximum number of items and the
   * `formData` matches that value, then false is returned, otherwise true is returned.
   *
   * @param formItems - The list of items in the form
   * @returns - True if the item is addable otherwise false
   */
  canAddItem(formItems) {
    const { schema, uiSchema, registry } = this.props;
    let { addable } = getUiOptions(uiSchema, registry.globalUiOptions);
    if (addable !== false) {
      if (schema.maxItems !== void 0) {
        addable = formItems.length < schema.maxItems;
      } else {
        addable = true;
      }
    }
    return addable;
  }
  /** Callback handler for when the user clicks on the add or add at index buttons. Creates a new row of keyed form data
   * either at the end of the list (when index is not specified) or inserted at the `index` when it is, adding it into
   * the state, and then returning `onChange()` with the plain form data converted from the keyed data
   *
   * @param event - The event for the click
   * @param [index] - The optional index at which to add the new data
   */
  _handleAddClick(event, index) {
    if (event) {
      event.preventDefault();
    }
    const { onChange, errorSchema } = this.props;
    const { keyedFormData } = this.state;
    let newErrorSchema;
    if (errorSchema) {
      newErrorSchema = {};
      for (const idx in errorSchema) {
        const i2 = parseInt(idx);
        if (index === void 0 || i2 < index) {
          set_default(newErrorSchema, [i2], errorSchema[idx]);
        } else if (i2 >= index) {
          set_default(newErrorSchema, [i2 + 1], errorSchema[idx]);
        }
      }
    }
    const newKeyedFormDataRow = {
      key: generateRowId(),
      item: this._getNewFormDataRow()
    };
    const newKeyedFormData = [...keyedFormData];
    if (index !== void 0) {
      newKeyedFormData.splice(index, 0, newKeyedFormDataRow);
    } else {
      newKeyedFormData.push(newKeyedFormDataRow);
    }
    this.setState({
      keyedFormData: newKeyedFormData,
      updatedKeyedFormData: true
    }, () => onChange(keyedToPlainFormData(newKeyedFormData), newErrorSchema));
  }
  /** Renders the `ArrayField` depending on the specific needs of the schema and uischema elements
   */
  render() {
    const { schema, uiSchema, idSchema, registry } = this.props;
    const { schemaUtils, translateString } = registry;
    if (!(ITEMS_KEY in schema)) {
      const uiOptions = getUiOptions(uiSchema);
      const UnsupportedFieldTemplate = getTemplate("UnsupportedFieldTemplate", registry, uiOptions);
      return (0, import_jsx_runtime.jsx)(UnsupportedFieldTemplate, { schema, idSchema, reason: translateString(TranslatableString.MissingItems), registry });
    }
    if (schemaUtils.isMultiSelect(schema)) {
      return this.renderMultiSelect();
    }
    if (isCustomWidget(uiSchema)) {
      return this.renderCustomWidget();
    }
    if (isFixedItems(schema)) {
      return this.renderFixedArray();
    }
    if (schemaUtils.isFilesArray(schema, uiSchema)) {
      return this.renderFiles();
    }
    return this.renderNormalArray();
  }
  /** Renders a normal array without any limitations of length
   */
  renderNormalArray() {
    const { schema, uiSchema = {}, errorSchema, idSchema, name, title, disabled = false, readonly = false, autofocus = false, required = false, registry, onBlur, onFocus, idPrefix, idSeparator = "_", rawErrors } = this.props;
    const { keyedFormData } = this.state;
    const fieldTitle = schema.title || title || name;
    const { schemaUtils, formContext } = registry;
    const uiOptions = getUiOptions(uiSchema);
    const _schemaItems = isObject_default(schema.items) ? schema.items : {};
    const itemsSchema = schemaUtils.retrieveSchema(_schemaItems);
    const formData = keyedToPlainFormData(this.state.keyedFormData);
    const canAdd = this.canAddItem(formData);
    const arrayProps = {
      canAdd,
      items: keyedFormData.map((keyedItem, index) => {
        const { key, item } = keyedItem;
        const itemCast = item;
        const itemSchema = schemaUtils.retrieveSchema(_schemaItems, itemCast);
        const itemErrorSchema = errorSchema ? errorSchema[index] : void 0;
        const itemIdPrefix = idSchema.$id + idSeparator + index;
        const itemIdSchema = schemaUtils.toIdSchema(itemSchema, itemIdPrefix, itemCast, idPrefix, idSeparator);
        return this.renderArrayFieldItem({
          key,
          index,
          name: name && `${name}-${index}`,
          title: fieldTitle ? `${fieldTitle}-${index + 1}` : void 0,
          canAdd,
          canMoveUp: index > 0,
          canMoveDown: index < formData.length - 1,
          itemSchema,
          itemIdSchema,
          itemErrorSchema,
          itemData: itemCast,
          itemUiSchema: uiSchema.items,
          autofocus: autofocus && index === 0,
          onBlur,
          onFocus,
          rawErrors,
          totalItems: keyedFormData.length
        });
      }),
      className: `rjsf-field rjsf-field-array rjsf-field-array-of-${itemsSchema.type}`,
      disabled,
      idSchema,
      uiSchema,
      onAddClick: this.onAddClick,
      readonly,
      required,
      schema,
      title: fieldTitle,
      formContext,
      formData,
      rawErrors,
      registry
    };
    const Template = getTemplate("ArrayFieldTemplate", registry, uiOptions);
    return (0, import_jsx_runtime.jsx)(Template, { ...arrayProps });
  }
  /** Renders an array using the custom widget provided by the user in the `uiSchema`
   */
  renderCustomWidget() {
    const { schema, idSchema, uiSchema, disabled = false, readonly = false, autofocus = false, required = false, hideError, placeholder, onBlur, onFocus, formData: items = [], registry, rawErrors, name } = this.props;
    const { widgets: widgets2, formContext, globalUiOptions, schemaUtils } = registry;
    const { widget, title: uiTitle, ...options } = getUiOptions(uiSchema, globalUiOptions);
    const Widget = getWidget(schema, widget, widgets2);
    const label = uiTitle ?? schema.title ?? name;
    const displayLabel = schemaUtils.getDisplayLabel(schema, uiSchema, globalUiOptions);
    return (0, import_jsx_runtime.jsx)(Widget, { id: idSchema.$id, name, multiple: true, onChange: this.onSelectChange, onBlur, onFocus, options, schema, uiSchema, registry, value: items, disabled, readonly, hideError, required, label, hideLabel: !displayLabel, placeholder, formContext, autofocus, rawErrors });
  }
  /** Renders an array as a set of checkboxes
   */
  renderMultiSelect() {
    const { schema, idSchema, uiSchema, formData: items = [], disabled = false, readonly = false, autofocus = false, required = false, placeholder, onBlur, onFocus, registry, rawErrors, name } = this.props;
    const { widgets: widgets2, schemaUtils, formContext, globalUiOptions } = registry;
    const itemsSchema = schemaUtils.retrieveSchema(schema.items, items);
    const enumOptions = optionsList(itemsSchema, uiSchema);
    const { widget = "select", title: uiTitle, ...options } = getUiOptions(uiSchema, globalUiOptions);
    const Widget = getWidget(schema, widget, widgets2);
    const label = uiTitle ?? schema.title ?? name;
    const displayLabel = schemaUtils.getDisplayLabel(schema, uiSchema, globalUiOptions);
    return (0, import_jsx_runtime.jsx)(Widget, { id: idSchema.$id, name, multiple: true, onChange: this.onSelectChange, onBlur, onFocus, options: { ...options, enumOptions }, schema, uiSchema, registry, value: items, disabled, readonly, required, label, hideLabel: !displayLabel, placeholder, formContext, autofocus, rawErrors });
  }
  /** Renders an array of files using the `FileWidget`
   */
  renderFiles() {
    const { schema, uiSchema, idSchema, name, disabled = false, readonly = false, autofocus = false, required = false, onBlur, onFocus, registry, formData: items = [], rawErrors } = this.props;
    const { widgets: widgets2, formContext, globalUiOptions, schemaUtils } = registry;
    const { widget = "files", title: uiTitle, ...options } = getUiOptions(uiSchema, globalUiOptions);
    const Widget = getWidget(schema, widget, widgets2);
    const label = uiTitle ?? schema.title ?? name;
    const displayLabel = schemaUtils.getDisplayLabel(schema, uiSchema, globalUiOptions);
    return (0, import_jsx_runtime.jsx)(Widget, { options, id: idSchema.$id, name, multiple: true, onChange: this.onSelectChange, onBlur, onFocus, schema, uiSchema, value: items, disabled, readonly, required, registry, formContext, autofocus, rawErrors, label, hideLabel: !displayLabel });
  }
  /** Renders an array that has a maximum limit of items
   */
  renderFixedArray() {
    const { schema, uiSchema = {}, formData = [], errorSchema, idPrefix, idSeparator = "_", idSchema, name, title, disabled = false, readonly = false, autofocus = false, required = false, registry, onBlur, onFocus, rawErrors } = this.props;
    const { keyedFormData } = this.state;
    let { formData: items = [] } = this.props;
    const fieldTitle = schema.title || title || name;
    const uiOptions = getUiOptions(uiSchema);
    const { schemaUtils, formContext } = registry;
    const _schemaItems = isObject_default(schema.items) ? schema.items : [];
    const itemSchemas = _schemaItems.map((item, index) => schemaUtils.retrieveSchema(item, formData[index]));
    const additionalSchema = isObject_default(schema.additionalItems) ? schemaUtils.retrieveSchema(schema.additionalItems, formData) : null;
    if (!items || items.length < itemSchemas.length) {
      items = items || [];
      items = items.concat(new Array(itemSchemas.length - items.length));
    }
    const canAdd = this.canAddItem(items) && !!additionalSchema;
    const arrayProps = {
      canAdd,
      className: "rjsf-field rjsf-field-array rjsf-field-array-fixed-items",
      disabled,
      idSchema,
      formData,
      items: keyedFormData.map((keyedItem, index) => {
        const { key, item } = keyedItem;
        const itemCast = item;
        const additional = index >= itemSchemas.length;
        const itemSchema = (additional && isObject_default(schema.additionalItems) ? schemaUtils.retrieveSchema(schema.additionalItems, itemCast) : itemSchemas[index]) || {};
        const itemIdPrefix = idSchema.$id + idSeparator + index;
        const itemIdSchema = schemaUtils.toIdSchema(itemSchema, itemIdPrefix, itemCast, idPrefix, idSeparator);
        const itemUiSchema = additional ? uiSchema.additionalItems || {} : Array.isArray(uiSchema.items) ? uiSchema.items[index] : uiSchema.items || {};
        const itemErrorSchema = errorSchema ? errorSchema[index] : void 0;
        return this.renderArrayFieldItem({
          key,
          index,
          name: name && `${name}-${index}`,
          title: fieldTitle ? `${fieldTitle}-${index + 1}` : void 0,
          canAdd,
          canRemove: additional,
          canMoveUp: index >= itemSchemas.length + 1,
          canMoveDown: additional && index < items.length - 1,
          itemSchema,
          itemData: itemCast,
          itemUiSchema,
          itemIdSchema,
          itemErrorSchema,
          autofocus: autofocus && index === 0,
          onBlur,
          onFocus,
          rawErrors,
          totalItems: keyedFormData.length
        });
      }),
      onAddClick: this.onAddClick,
      readonly,
      required,
      registry,
      schema,
      uiSchema,
      title: fieldTitle,
      formContext,
      errorSchema,
      rawErrors
    };
    const Template = getTemplate("ArrayFieldTemplate", registry, uiOptions);
    return (0, import_jsx_runtime.jsx)(Template, { ...arrayProps });
  }
  /** Renders the individual array item using a `SchemaField` along with the additional properties required to be send
   * back to the `ArrayFieldItemTemplate`.
   *
   * @param props - The props for the individual array item to be rendered
   */
  renderArrayFieldItem(props) {
    const { key, index, name, canAdd, canRemove = true, canMoveUp, canMoveDown, itemSchema, itemData, itemUiSchema, itemIdSchema, itemErrorSchema, autofocus, onBlur, onFocus, rawErrors, totalItems, title } = props;
    const { disabled, hideError, idPrefix, idSeparator, readonly, uiSchema, registry, formContext } = this.props;
    const { fields: { ArraySchemaField, SchemaField: SchemaField2 }, globalUiOptions } = registry;
    const ItemSchemaField = ArraySchemaField || SchemaField2;
    const { orderable = true, removable = true, copyable = false } = getUiOptions(uiSchema, globalUiOptions);
    const has = {
      moveUp: orderable && canMoveUp,
      moveDown: orderable && canMoveDown,
      copy: copyable && canAdd,
      remove: removable && canRemove,
      toolbar: false
    };
    has.toolbar = Object.keys(has).some((key2) => has[key2]);
    return {
      children: (0, import_jsx_runtime.jsx)(ItemSchemaField, { name, title, index, schema: itemSchema, uiSchema: itemUiSchema, formData: itemData, formContext, errorSchema: itemErrorSchema, idPrefix, idSeparator, idSchema: itemIdSchema, required: this.isItemRequired(itemSchema), onChange: this.onChangeForIndex(index), onBlur, onFocus, registry, disabled, readonly, hideError, autofocus, rawErrors }),
      buttonsProps: {
        idSchema: itemIdSchema,
        disabled,
        readonly,
        canAdd,
        hasCopy: has.copy,
        hasMoveUp: has.moveUp,
        hasMoveDown: has.moveDown,
        hasRemove: has.remove,
        index,
        totalItems,
        onAddIndexClick: this.onAddIndexClick,
        onCopyIndexClick: this.onCopyIndexClick,
        onDropIndexClick: this.onDropIndexClick,
        onReorderClick: this.onReorderClick,
        registry,
        schema: itemSchema,
        uiSchema: itemUiSchema
      },
      className: "rjsf-array-item",
      disabled,
      hasToolbar: has.toolbar,
      index,
      totalItems,
      key,
      readonly,
      registry,
      schema: itemSchema,
      uiSchema: itemUiSchema
    };
  }
};
var ArrayField_default = ArrayField;

// node_modules/@rjsf/core/lib/components/fields/BooleanField.js
var import_jsx_runtime2 = __toESM(require_jsx_runtime(), 1);
function BooleanField(props) {
  const { schema, name, uiSchema, idSchema, formData, registry, required, disabled, readonly, hideError, autofocus, title, onChange, onFocus, onBlur, rawErrors } = props;
  const { title: schemaTitle } = schema;
  const { widgets: widgets2, formContext, translateString, globalUiOptions } = registry;
  const {
    widget = "checkbox",
    title: uiTitle,
    // Unlike the other fields, don't use `getDisplayLabel()` since it always returns false for the boolean type
    label: displayLabel = true,
    enumNames,
    ...options
  } = getUiOptions(uiSchema, globalUiOptions);
  const Widget = getWidget(schema, widget, widgets2);
  const yes = translateString(TranslatableString.YesLabel);
  const no = translateString(TranslatableString.NoLabel);
  let enumOptions;
  const label = uiTitle ?? schemaTitle ?? title ?? name;
  if (Array.isArray(schema.oneOf)) {
    enumOptions = optionsList({
      oneOf: schema.oneOf.map((option) => {
        if (isObject_default(option)) {
          return {
            ...option,
            title: option.title || (option.const === true ? yes : no)
          };
        }
        return void 0;
      }).filter((o2) => o2)
      // cast away the error that typescript can't grok is fixed
    }, uiSchema);
  } else {
    const enums = schema.enum ?? [true, false];
    if (!enumNames && enums.length === 2 && enums.every((v2) => typeof v2 === "boolean")) {
      enumOptions = [
        {
          value: enums[0],
          label: enums[0] ? yes : no
        },
        {
          value: enums[1],
          label: enums[1] ? yes : no
        }
      ];
    } else {
      enumOptions = optionsList({ enum: enums }, uiSchema);
    }
  }
  return (0, import_jsx_runtime2.jsx)(Widget, { options: { ...options, enumOptions }, schema, uiSchema, id: idSchema.$id, name, onChange, onFocus, onBlur, label, hideLabel: !displayLabel, value: formData, required, disabled, readonly, hideError, registry, formContext, autofocus, rawErrors });
}
var BooleanField_default = BooleanField;

// node_modules/@rjsf/core/lib/components/fields/LayoutGridField.js
var import_react2 = __toESM(require_react(), 1);
var import_jsx_runtime3 = __toESM(require_jsx_runtime(), 1);
var import_react3 = __toESM(require_react(), 1);

// node_modules/lodash-es/_baseValues.js
function baseValues(object, props) {
  return arrayMap_default(props, function(key) {
    return object[key];
  });
}
var baseValues_default = baseValues;

// node_modules/lodash-es/values.js
function values(object) {
  return object == null ? [] : baseValues_default(object, keys_default(object));
}
var values_default = values;

// node_modules/lodash-es/includes.js
var nativeMax = Math.max;
function includes(collection, value, fromIndex, guard) {
  collection = isArrayLike_default(collection) ? collection : values_default(collection);
  fromIndex = fromIndex && !guard ? toInteger_default(fromIndex) : 0;
  var length = collection.length;
  if (fromIndex < 0) {
    fromIndex = nativeMax(length + fromIndex, 0);
  }
  return isString_default(collection) ? fromIndex <= length && collection.indexOf(value, fromIndex) > -1 : !!length && baseIndexOf_default(collection, value, fromIndex) > -1;
}
var includes_default = includes;

// node_modules/lodash-es/_baseIntersection.js
var nativeMin = Math.min;
function baseIntersection(arrays, iteratee, comparator) {
  var includes2 = comparator ? arrayIncludesWith_default : arrayIncludes_default, length = arrays[0].length, othLength = arrays.length, othIndex = othLength, caches = Array(othLength), maxLength = Infinity, result = [];
  while (othIndex--) {
    var array = arrays[othIndex];
    if (othIndex && iteratee) {
      array = arrayMap_default(array, baseUnary_default(iteratee));
    }
    maxLength = nativeMin(array.length, maxLength);
    caches[othIndex] = !comparator && (iteratee || length >= 120 && array.length >= 120) ? new SetCache_default(othIndex && array) : void 0;
  }
  array = arrays[0];
  var index = -1, seen = caches[0];
  outer:
    while (++index < length && result.length < maxLength) {
      var value = array[index], computed = iteratee ? iteratee(value) : value;
      value = comparator || value !== 0 ? value : 0;
      if (!(seen ? cacheHas_default(seen, computed) : includes2(result, computed, comparator))) {
        othIndex = othLength;
        while (--othIndex) {
          var cache = caches[othIndex];
          if (!(cache ? cacheHas_default(cache, computed) : includes2(arrays[othIndex], computed, comparator))) {
            continue outer;
          }
        }
        if (seen) {
          seen.push(computed);
        }
        result.push(value);
      }
    }
  return result;
}
var baseIntersection_default = baseIntersection;

// node_modules/lodash-es/_castArrayLikeObject.js
function castArrayLikeObject(value) {
  return isArrayLikeObject_default(value) ? value : [];
}
var castArrayLikeObject_default = castArrayLikeObject;

// node_modules/lodash-es/intersection.js
var intersection = baseRest_default(function(arrays) {
  var mapped = arrayMap_default(arrays, castArrayLikeObject_default);
  return mapped.length && mapped[0] === arrays[0] ? baseIntersection_default(mapped) : [];
});
var intersection_default = intersection;

// node_modules/lodash-es/isUndefined.js
function isUndefined(value) {
  return value === void 0;
}
var isUndefined_default = isUndefined;

// node_modules/@rjsf/core/lib/components/fields/LayoutGridField.js
var GridType;
(function(GridType2) {
  GridType2["ROW"] = "ui:row";
  GridType2["COLUMN"] = "ui:col";
  GridType2["COLUMNS"] = "ui:columns";
  GridType2["CONDITION"] = "ui:condition";
})(GridType || (GridType = {}));
var Operators;
(function(Operators2) {
  Operators2["ALL"] = "all";
  Operators2["SOME"] = "some";
  Operators2["NONE"] = "none";
})(Operators || (Operators = {}));
var LOOKUP_REGEX = /^\$lookup=(.+)/;
var LAYOUT_GRID_UI_OPTION = "layoutGrid";
var LAYOUT_GRID_OPTION = `ui:${LAYOUT_GRID_UI_OPTION}`;
function getNonNullishValue(value, fallback) {
  return value ?? fallback;
}
var _LayoutGridField = class _LayoutGridField extends import_react3.PureComponent {
  /** Constructs an `LayoutGridField` with the given `props`
   *
   * @param props - The `LayoutGridField` for this template
   */
  constructor(props) {
    super(props);
    /** Generates an `onChange` handler for the field associated with the `dottedPath`. This handler will clone and update
     * the `formData` with the new `value` and the `errorSchema` if an `errSchema` is provided. After updating those two
     * elements, they will then be passed on to the `onChange` handler of the `LayoutFieldGrid`.
     *
     * @param dottedPath - The dotted-path to the field for which to generate the onChange handler
     * @returns - The `onChange` handling function for the `dottedPath` field
     */
    __publicField(this, "onFieldChange", (dottedPath) => {
      return (value, errSchema, id) => {
        const { onChange, errorSchema, formData } = this.props;
        const newFormData = cloneDeep_default(formData || {});
        let newErrorSchema = errorSchema;
        if (errSchema && errorSchema) {
          newErrorSchema = cloneDeep_default(errorSchema);
          set_default(newErrorSchema, dottedPath, errSchema);
        }
        set_default(newFormData, dottedPath, value);
        onChange(newFormData, newErrorSchema, id);
      };
    });
  }
  /** Computes the uiSchema for the field with `name` from the `uiProps` and `uiSchema` provided. The field UI Schema
   * will always contain a copy of the global options from the `uiSchema` (so they can be passed down) as well as
   * copying them into the local ui options. When the `forceReadonly` flag is true, then the field UI Schema is
   * updated to make "readonly" be true. When the `schemaReadonly` flag is true AND the field UI Schema does NOT have
   * the flag already provided, then we also make "readonly" true. We always make sure to return the final value of the
   * field UI Schema's "readonly" flag as `uiReadonly` along with the `fieldUiSchema` in the return value.
   *
   * @param field - The name of the field to pull the existing UI Schema for
   * @param uiProps - Any props that should be put into the field's uiSchema
   * @param [uiSchema] - The optional UI Schema from which to get the UI schema for the field
   * @param [schemaReadonly] - Optional flag indicating whether the schema indicates the field is readonly
   * @param [forceReadonly] - Optional flag indicating whether the Form itself is in readonly mode
   */
  static computeFieldUiSchema(field, uiProps, uiSchema, schemaReadonly, forceReadonly) {
    const globalUiOptions = get_default(uiSchema, [UI_GLOBAL_OPTIONS_KEY], {});
    const localUiSchema = get_default(uiSchema, field);
    const localUiOptions = { ...get_default(localUiSchema, [UI_OPTIONS_KEY], {}), ...uiProps, ...globalUiOptions };
    const fieldUiSchema = { ...localUiSchema };
    if (!isEmpty_default(localUiOptions)) {
      set_default(fieldUiSchema, [UI_OPTIONS_KEY], localUiOptions);
    }
    if (!isEmpty_default(globalUiOptions)) {
      set_default(fieldUiSchema, [UI_GLOBAL_OPTIONS_KEY], globalUiOptions);
    }
    let { readonly: uiReadonly } = getUiOptions(fieldUiSchema);
    if (forceReadonly === true || isUndefined_default(uiReadonly) && schemaReadonly === true) {
      uiReadonly = true;
      if (has_default(localUiOptions, READONLY_KEY)) {
        set_default(fieldUiSchema, [UI_OPTIONS_KEY, READONLY_KEY], true);
      } else {
        set_default(fieldUiSchema, `ui:${READONLY_KEY}`, true);
      }
    }
    return { fieldUiSchema, uiReadonly };
  }
  /** Given an `operator`, `datum` and `value` determines whether this condition is considered matching. Matching
   * depends on the `operator`. The `datum` and `value` are converted into arrays if they aren't already and then the
   * contents of the two arrays are compared using the `operator`. When `operator` is All, then the two arrays must be
   * equal to match. When `operator` is SOME then the intersection of the two arrays must have at least one value in
   * common to match. When `operator` is NONE then the intersection of the two arrays must not have any values in common
   * to match.
   *
   * @param [operator] - The optional operator for the condition
   * @param [datum] - The optional datum for the condition, this can be an item or a list of items of type unknown
   * @param [value='$0m3tH1nG Un3xP3cT3d'] The optional value for the condition, defaulting to a highly unlikely value
   *        to avoid comparing two undefined elements when `value` was forgotten in the condition definition.
   *        This can be an item or a list of items of type unknown
   * @returns - True if the condition matches, false otherwise
   */
  static conditionMatches(operator, datum, value = "$0m3tH1nG Un3xP3cT3d") {
    const data = flatten_default([datum]).sort();
    const values2 = flatten_default([value]).sort();
    switch (operator) {
      case Operators.ALL:
        return isEqual_default(data, values2);
      case Operators.SOME:
        return intersection_default(data, values2).length > 0;
      case Operators.NONE:
        return intersection_default(data, values2).length === 0;
      default:
        return false;
    }
  }
  /** From within the `layoutGridSchema` finds the `children` and any extra `gridProps` from the object keyed by
   * `schemaKey`. If the `children` contains extra `gridProps` and those props contain a `className` string, try to
   * lookup whether that `className` has a replacement value in the `registry` using the `FORM_CONTEXT_LOOKUP_BASE`.
   * When the `className` value contains multiple classNames separated by a space, the lookup will look for a
   * replacement value for each `className` and combine them into one.
   *
   * @param layoutGridSchema - The GridSchemaType instance from which to obtain the `schemaKey` children and extra props
   * @param schemaKey - A `GridType` value, used to get the children and extra props from within the `layoutGridSchema`
   * @param registry - The `@rjsf` Registry from which to look up `classNames` if they are present in the extra props
   * @returns - An object containing the list of `LayoutGridSchemaType` `children` and any extra `gridProps`
   * @throws - A `TypeError` when the `children` is not an array
   */
  static findChildrenAndProps(layoutGridSchema, schemaKey, registry) {
    let gridProps = {};
    let children = layoutGridSchema[schemaKey];
    if (isPlainObject_default(children)) {
      const { children: elements, className: toMapClassNames, ...otherProps } = children;
      children = elements;
      if (toMapClassNames) {
        const classes = toMapClassNames.split(" ");
        const className = classes.map((ele) => lookupFromFormContext(registry, ele, ele)).join(" ");
        gridProps = { ...otherProps, className };
      } else {
        gridProps = otherProps;
      }
    }
    if (!Array.isArray(children)) {
      throw new TypeError(`Expected array for "${schemaKey}" in ${JSON.stringify(layoutGridSchema)}`);
    }
    return { children, gridProps };
  }
  /** Generates an idSchema for the `schema` using `@rjsf`'s `toIdSchema` util, passing the `baseIdSchema`'s `$id` value
   * as the id prefix.
   *
   * @param schemaUtils - The `SchemaUtilsType` used to call `toIdSchema`
   * @param schema - The schema to generate the idSchema for
   * @param baseIdSchema - The IdSchema for the base
   * @param formData - The formData to pass the `toIdSchema`
   * @param [idSeparator] - The param to pass into the `toIdSchema` util which will use it to join the `idSchema` paths
   * @returns - The generated `idSchema` for the `schema`
   */
  static getIdSchema(schemaUtils, baseIdSchema, formData, schema = {}, idSeparator) {
    const baseId = get_default(baseIdSchema, ID_KEY);
    return schemaUtils.toIdSchema(schema, baseId, formData, baseId, idSeparator);
  }
  /** Given a `dottedPath` to a field in the `initialSchema`, iterate through each individual path in the schema until
   * the leaf path is found and returned (along with whether that leaf path `isRequired`) OR no schema exists for an
   * element in the path. If the leaf schema element happens to be a oneOf/anyOf then also return the oneOf/anyOf as
   * `options`.
   *
   * @param schemaUtils - The `SchemaUtilsType` used to call `retrieveSchema`
   * @param dottedPath - The dotted-path to the field for which to get the schema
   * @param initialSchema - The initial schema to start the search from
   * @param formData - The formData, useful for resolving a oneOf/anyOf selection in the path hierarchy
   * @param initialIdSchema - The initial idSchema to start the search from
   * @param [idSeparator] - The param to pass into the `toIdSchema` util which will use it to join the `idSchema` paths
   * @returns - An object containing the destination schema, isRequired and isReadonly flags for the field and options
   *            info if a oneOf/anyOf
   */
  static getSchemaDetailsForField(schemaUtils, dottedPath, initialSchema, formData, initialIdSchema, idSeparator) {
    let rawSchema = initialSchema;
    let idSchema = initialIdSchema;
    const parts = dottedPath.split(".");
    const leafPath = parts.pop();
    let schema = schemaUtils.retrieveSchema(rawSchema, formData);
    let innerData = formData;
    let isReadonly = schema.readOnly;
    parts.forEach((part) => {
      if (has_default(schema, PROPERTIES_KEY)) {
        rawSchema = get_default(schema, [PROPERTIES_KEY, part], {});
        idSchema = get_default(idSchema, part, {});
      } else if (schema && (has_default(schema, ONE_OF_KEY) || has_default(schema, ANY_OF_KEY))) {
        const xxx = has_default(schema, ONE_OF_KEY) ? ONE_OF_KEY : ANY_OF_KEY;
        const selectedSchema = schemaUtils.findSelectedOptionInXxxOf(schema, part, xxx, innerData);
        const selectedIdSchema = _LayoutGridField.getIdSchema(schemaUtils, idSchema, formData, selectedSchema, idSeparator);
        rawSchema = get_default(selectedSchema, [PROPERTIES_KEY, part], {});
        idSchema = get_default(selectedIdSchema, part, {});
      } else {
        rawSchema = {};
      }
      innerData = get_default(innerData, part, {});
      schema = schemaUtils.retrieveSchema(rawSchema, innerData);
      isReadonly = getNonNullishValue(schema.readOnly, isReadonly);
    });
    let optionsInfo;
    let isRequired = false;
    if (isEmpty_default(schema)) {
      schema = void 0;
    }
    if (schema && leafPath) {
      if (schema && (has_default(schema, ONE_OF_KEY) || has_default(schema, ANY_OF_KEY))) {
        const xxx = has_default(schema, ONE_OF_KEY) ? ONE_OF_KEY : ANY_OF_KEY;
        schema = schemaUtils.findSelectedOptionInXxxOf(schema, leafPath, xxx, innerData);
        const rawIdSchema = _LayoutGridField.getIdSchema(schemaUtils, idSchema, formData, schema, idSeparator);
        idSchema = mergeObjects(rawIdSchema, idSchema);
      }
      isRequired = schema !== void 0 && Array.isArray(schema.required) && includes_default(schema.required, leafPath);
      schema = get_default(schema, [PROPERTIES_KEY, leafPath]);
      schema = schema ? schemaUtils.retrieveSchema(schema) : schema;
      idSchema = get_default(idSchema, leafPath, {});
      isReadonly = getNonNullishValue(schema == null ? void 0 : schema.readOnly, isReadonly);
      if (schema && (has_default(schema, ONE_OF_KEY) || has_default(schema, ANY_OF_KEY))) {
        const xxx = has_default(schema, ONE_OF_KEY) ? ONE_OF_KEY : ANY_OF_KEY;
        const discriminator = getDiscriminatorFieldFromSchema(schema);
        optionsInfo = { options: schema[xxx], hasDiscriminator: !!discriminator };
      }
    }
    return { schema, isRequired, isReadonly, optionsInfo, idSchema };
  }
  /** Gets the custom render component from the `render`, by either determining that it is either already a function or
   * it is a non-function value that can be used to look up the function in the registry. If no function can be found,
   * null is returned.
   *
   * @param render - The potential render function or lookup name to one
   * @param registry - The `@rjsf` Registry from which to look up `classNames` if they are present in the extra props
   * @returns - Either a render function if available, or null if not
   */
  static getCustomRenderComponent(render, registry) {
    let customRenderer = render;
    if (isString_default(customRenderer)) {
      customRenderer = lookupFromFormContext(registry, customRenderer);
    }
    if (isFunction_default(customRenderer)) {
      return customRenderer;
    }
    return null;
  }
  /** Extract the `name`, and optional `render` and all other props from the `gridSchema`. We look up the `render` to
   * see if can be resolved to a UIComponent. If `name` does not exist and there is an optional `render` UIComponent, we
   * set the `rendered` component with only specified props for that component in the object.
   *
   * @param registry - The `@rjsf` Registry from which to look up `classNames` if they are present in the extra props
   * @param gridSchema - The string or object that represents the configuration for the grid field
   * @returns - The UIComponentPropsType computed from the gridSchema
   */
  static computeUIComponentPropsFromGridSchema(registry, gridSchema) {
    let name;
    let UIComponent = null;
    let uiProps = {};
    let rendered;
    if (isString_default(gridSchema) || isUndefined_default(gridSchema)) {
      name = gridSchema ?? "";
    } else {
      const { name: innerName = "", render, ...innerProps } = gridSchema;
      name = innerName;
      uiProps = innerProps;
      if (!isEmpty_default(uiProps)) {
        forEach_default(uiProps, (prop, key) => {
          if (isString_default(prop)) {
            const match = LOOKUP_REGEX.exec(prop);
            if (Array.isArray(match) && match.length > 1) {
              const name2 = match[1];
              uiProps[key] = lookupFromFormContext(registry, name2, name2);
            }
          }
        });
      }
      UIComponent = _LayoutGridField.getCustomRenderComponent(render, registry);
      if (!innerName && UIComponent) {
        rendered = (0, import_jsx_runtime3.jsx)(UIComponent, { ...innerProps, "data-testid": _LayoutGridField.TEST_IDS.uiComponent });
      }
    }
    return { name, UIComponent, uiProps, rendered };
  }
  /** Renders the `children` of the `GridType.CONDITION` if it passes. The `layoutGridSchema` for the
   * `GridType.CONDITION` is separated into the `children` and other `gridProps`. The `gridProps` are used to extract
   * the `operator`, `field` and `value` of the condition. If the condition matches, then all of the `children` are
   * rendered, otherwise null is returned.
   *
   * @param layoutGridSchema - The string or object that represents the configuration for the grid field
   * @returns - The rendered the children for the `GridType.CONDITION` or null
   */
  renderCondition(layoutGridSchema) {
    const { formData, registry } = this.props;
    const { children, gridProps } = _LayoutGridField.findChildrenAndProps(layoutGridSchema, GridType.CONDITION, registry);
    const { operator, field = "", value } = gridProps;
    const fieldData = get_default(formData, field, null);
    if (_LayoutGridField.conditionMatches(operator, fieldData, value)) {
      return this.renderChildren(children);
    }
    return null;
  }
  /** Renders a material-ui `GridTemplate` as an item. The `layoutGridSchema` for the `GridType.COLUMN` is separated
   * into the `children` and other `gridProps`. The `gridProps` will be spread onto the outer `GridTemplate`. Inside
   * the `GridTemplate` all the `children` are rendered.
   *
   * @param layoutGridSchema - The string or object that represents the configuration for the grid field
   * @returns - The rendered `GridTemplate` containing the children for the `GridType.COLUMN`
   */
  renderCol(layoutGridSchema) {
    const { registry, uiSchema } = this.props;
    const { children, gridProps } = _LayoutGridField.findChildrenAndProps(layoutGridSchema, GridType.COLUMN, registry);
    const uiOptions = getUiOptions(uiSchema);
    const GridTemplate2 = getTemplate("GridTemplate", registry, uiOptions);
    return (0, import_jsx_runtime3.jsx)(GridTemplate2, { column: true, "data-testid": _LayoutGridField.TEST_IDS.col, ...gridProps, children: this.renderChildren(children) });
  }
  /** Renders a material-ui `GridTemplate` as an item. The `layoutGridSchema` for the `GridType.COLUMNS` is separated
   * into the `children` and other `gridProps`. The `children` is iterated on and `gridProps` will be spread onto the
   * outer `GridTemplate`. Each child will have their own rendered `GridTemplate`.
   *
   * @param layoutGridSchema - The string or object that represents the configuration for the grid field
   * @returns - The rendered `GridTemplate` containing the children for the `GridType.COLUMNS`
   */
  renderColumns(layoutGridSchema) {
    const { registry, uiSchema } = this.props;
    const { children, gridProps } = _LayoutGridField.findChildrenAndProps(layoutGridSchema, GridType.COLUMNS, registry);
    const uiOptions = getUiOptions(uiSchema);
    const GridTemplate2 = getTemplate("GridTemplate", registry, uiOptions);
    return children.map((child) => (0, import_jsx_runtime3.jsx)(GridTemplate2, { column: true, "data-testid": _LayoutGridField.TEST_IDS.col, ...gridProps, children: this.renderChildren([child]) }, `column-${hashObject(child)}`));
  }
  /** Renders a material-ui `GridTemplate` as a container. The
   * `layoutGridSchema` for the `GridType.ROW` is separated into the `children` and other `gridProps`. The `gridProps`
   * will be spread onto the outer `GridTemplate`. Inside of the `GridTemplate` all of the `children` are rendered.
   *
   * @param layoutGridSchema - The string or object that represents the configuration for the grid field
   * @returns - The rendered `GridTemplate` containing the children for the `GridType.ROW`
   */
  renderRow(layoutGridSchema) {
    const { registry, uiSchema } = this.props;
    const { children, gridProps } = _LayoutGridField.findChildrenAndProps(layoutGridSchema, GridType.ROW, registry);
    const uiOptions = getUiOptions(uiSchema);
    const GridTemplate2 = getTemplate("GridTemplate", registry, uiOptions);
    return (0, import_jsx_runtime3.jsx)(GridTemplate2, { ...gridProps, "data-testid": _LayoutGridField.TEST_IDS.row, children: this.renderChildren(children) });
  }
  /** Iterates through all the `childrenLayoutGridSchema`, rendering a nested `LayoutGridField` for each item in the
   * list, passing all the props for the current `LayoutGridField` along, updating the `schema` by calling
   * `retrieveSchema()` on it to resolve any `$ref`s. In addition to the updated `schema`, each item in
   * `childrenLayoutGridSchema` is passed as `layoutGridSchema`.
   *
   * @param childrenLayoutGridSchema - The list of strings or objects that represents the configurations for the
   *          children fields
   * @returns - The nested `LayoutGridField`s
   */
  renderChildren(childrenLayoutGridSchema) {
    const { registry, schema: rawSchema, formData } = this.props;
    const { schemaUtils } = registry;
    const schema = schemaUtils.retrieveSchema(rawSchema, formData);
    return childrenLayoutGridSchema.map((layoutGridSchema) => (0, import_react2.createElement)(_LayoutGridField, { ...this.props, key: `layoutGrid-${hashObject(layoutGridSchema)}`, schema, layoutGridSchema }));
  }
  /** Renders the field described by `gridSchema`. If `gridSchema` is not an object, then is will be assumed
   * to be the dotted-path to the field in the schema. Otherwise, we extract the `name`, and optional `render` and all
   * other props. If `name` does not exist and there is an optional `render`, we return the `render` component with only
   * specified props for that component. If `name` exists, we take the name, the initial & root schemas and the formData
   * and get the destination schema, is required state and optional oneOf/anyOf options for it. If the destination
   * schema was located along with oneOf/anyOf options then a `LayoutMultiSchemaField` will be rendered with the
   * `uiSchema`, `errorSchema`, `idSchema` and `formData` drilled down to the dotted-path field, spreading any other
   * props from `gridSchema` into the `ui:options`. If the destination schema located without any oneOf/anyOf options,
   * then a `SchemaField` will be rendered with the same props as mentioned in the previous sentence. If no destination
   * schema was located, but a custom render component was found, then it will be rendered with many of the non-event
   * handling props. If none of the previous render paths are valid, then a null is returned.
   *
   * @param gridSchema - The string or object that represents the configuration for the grid field
   * @returns - One of `LayoutMultiSchemaField`, `SchemaField`, a custom render component or null, depending
   */
  renderField(gridSchema) {
    const {
      schema: initialSchema,
      uiSchema,
      errorSchema,
      idSchema,
      onBlur,
      onFocus,
      formData,
      readonly,
      registry,
      idSeparator,
      layoutGridSchema,
      // Used to pull this out of otherProps since we don't want to pass it through
      ...otherProps
    } = this.props;
    const { fields: fields2, schemaUtils } = registry;
    const { SchemaField: SchemaField2, LayoutMultiSchemaField: LayoutMultiSchemaField2 } = fields2;
    const uiComponentProps = _LayoutGridField.computeUIComponentPropsFromGridSchema(registry, gridSchema);
    if (uiComponentProps.rendered) {
      return uiComponentProps.rendered;
    }
    const { name, UIComponent, uiProps } = uiComponentProps;
    const { schema, isRequired, isReadonly, optionsInfo, idSchema: fieldIdSchema } = _LayoutGridField.getSchemaDetailsForField(schemaUtils, name, initialSchema, formData, idSchema, idSeparator);
    if (schema) {
      const Field = (optionsInfo == null ? void 0 : optionsInfo.hasDiscriminator) ? LayoutMultiSchemaField2 : SchemaField2;
      const { fieldUiSchema, uiReadonly } = _LayoutGridField.computeFieldUiSchema(name, uiProps, uiSchema, isReadonly, readonly);
      return (0, import_jsx_runtime3.jsx)(Field, { "data-testid": (optionsInfo == null ? void 0 : optionsInfo.hasDiscriminator) ? _LayoutGridField.TEST_IDS.layoutMultiSchemaField : _LayoutGridField.TEST_IDS.field, ...otherProps, name, required: isRequired, readonly: uiReadonly, schema, uiSchema: fieldUiSchema, errorSchema: get_default(errorSchema, name), idSchema: fieldIdSchema, idSeparator, formData: get_default(formData, name), onChange: this.onFieldChange(name), onBlur, onFocus, options: optionsInfo == null ? void 0 : optionsInfo.options, registry });
    }
    if (UIComponent) {
      return (0, import_jsx_runtime3.jsx)(UIComponent, { "data-testid": _LayoutGridField.TEST_IDS.uiComponent, ...otherProps, name, required: isRequired, formData, readOnly: !!isReadonly || readonly, errorSchema, uiSchema, schema: initialSchema, idSchema, idSeparator, onBlur, onFocus, registry, ...uiProps });
    }
    return null;
  }
  /** Renders the `LayoutGridField`. If there isn't a `layoutGridSchema` prop defined, then try pulling it out of the
   * `uiSchema` via `ui:LayoutGridField`. If `layoutGridSchema` is an object, then check to see if any of the properties
   * match one of the `GridType`s. If so, call the appropriate render function for the type. Otherwise, just call the
   * generic `renderField()` function with the `layoutGridSchema`.
   *
   * @returns - the rendered `LayoutGridField`
   */
  render() {
    const { uiSchema } = this.props;
    let { layoutGridSchema } = this.props;
    const uiOptions = getUiOptions(uiSchema);
    if (!layoutGridSchema && LAYOUT_GRID_UI_OPTION in uiOptions && isObject_default(uiOptions[LAYOUT_GRID_UI_OPTION])) {
      layoutGridSchema = uiOptions[LAYOUT_GRID_UI_OPTION];
    }
    if (isObject_default(layoutGridSchema)) {
      if (GridType.ROW in layoutGridSchema) {
        return this.renderRow(layoutGridSchema);
      }
      if (GridType.COLUMN in layoutGridSchema) {
        return this.renderCol(layoutGridSchema);
      }
      if (GridType.COLUMNS in layoutGridSchema) {
        return this.renderColumns(layoutGridSchema);
      }
      if (GridType.CONDITION in layoutGridSchema) {
        return this.renderCondition(layoutGridSchema);
      }
    }
    return this.renderField(layoutGridSchema);
  }
};
__publicField(_LayoutGridField, "defaultProps", {
  layoutGridSchema: void 0
});
__publicField(_LayoutGridField, "TEST_IDS", getTestIds());
var LayoutGridField = _LayoutGridField;

// node_modules/@rjsf/core/lib/components/fields/LayoutHeaderField.js
var import_jsx_runtime4 = __toESM(require_jsx_runtime(), 1);
function LayoutHeaderField(props) {
  const { idSchema, title, schema, uiSchema, required, registry, name } = props;
  const options = getUiOptions(uiSchema, registry.globalUiOptions);
  const { title: uiTitle } = options;
  const { title: schemaTitle } = schema;
  const fieldTitle = uiTitle || title || schemaTitle || name;
  if (!fieldTitle) {
    return null;
  }
  const TitleFieldTemplate = getTemplate("TitleFieldTemplate", registry, options);
  return (0, import_jsx_runtime4.jsx)(TitleFieldTemplate, { id: titleId(idSchema), title: fieldTitle, required, schema, uiSchema, registry });
}

// node_modules/@rjsf/core/lib/components/fields/LayoutMultiSchemaField.js
var import_jsx_runtime5 = __toESM(require_jsx_runtime(), 1);
var import_react4 = __toESM(require_react(), 1);
function getSelectedOption(options, selectorField, value) {
  const defaultValue = "!@#!@$@#$!@$#";
  const schemaOptions = options.map(({ schema }) => schema);
  return schemaOptions.find((option) => {
    const selector = get_default(option, [PROPERTIES_KEY, selectorField]);
    const result = get_default(selector, DEFAULT_KEY, get_default(selector, CONST_KEY, defaultValue));
    return result === value;
  });
}
function computeEnumOptions(schema, options, schemaUtils, uiSchema, formData) {
  const realOptions = options.map((opt) => schemaUtils.retrieveSchema(opt, formData));
  let tempSchema = schema;
  if (has_default(schema, ONE_OF_KEY)) {
    tempSchema = { ...schema, [ONE_OF_KEY]: realOptions };
  } else if (has_default(schema, ANY_OF_KEY)) {
    tempSchema = { ...schema, [ANY_OF_KEY]: realOptions };
  }
  const enumOptions = optionsList(tempSchema, uiSchema);
  if (!enumOptions) {
    throw new Error(`No enumOptions were computed from the schema ${JSON.stringify(tempSchema)}`);
  }
  return enumOptions;
}
function LayoutMultiSchemaField(props) {
  var _a;
  const { name, baseType, disabled = false, formData, idSchema, onBlur, onChange, options, onFocus, registry, uiSchema, schema, formContext, autofocus, readonly, required, errorSchema, hideError = false } = props;
  const { widgets: widgets2, schemaUtils, globalUiOptions } = registry;
  const [enumOptions, setEnumOptions] = (0, import_react4.useState)(computeEnumOptions(schema, options, schemaUtils, uiSchema, formData));
  const id = get_default(idSchema, ID_KEY);
  const discriminator = getDiscriminatorFieldFromSchema(schema);
  const FieldErrorTemplate2 = getTemplate("FieldErrorTemplate", registry, options);
  const FieldTemplate2 = getTemplate("FieldTemplate", registry, options);
  const schemaHash = hashObject(schema);
  const optionsHash = hashObject(options);
  const uiSchemaHash = uiSchema ? hashObject(uiSchema) : "";
  const formDataHash = formData ? hashObject(formData) : "";
  (0, import_react4.useEffect)(() => {
    setEnumOptions(computeEnumOptions(schema, options, schemaUtils, uiSchema, formData));
  }, [schemaHash, optionsHash, schemaUtils, uiSchemaHash, formDataHash]);
  const { widget = discriminator ? "radio" : "select", title = "", placeholder = "", optionsSchemaSelector: selectorField = discriminator, hideError: uiSchemaHideError, ...uiOptions } = getUiOptions(uiSchema);
  if (!selectorField) {
    throw new Error("No selector field provided for the LayoutMultiSchemaField");
  }
  const selectedOption = get_default(formData, selectorField);
  let optionSchema = get_default((_a = enumOptions[0]) == null ? void 0 : _a.schema, [PROPERTIES_KEY, selectorField], {});
  const option = getSelectedOption(enumOptions, selectorField, selectedOption);
  optionSchema = (optionSchema == null ? void 0 : optionSchema.type) ? optionSchema : { ...optionSchema, type: (option == null ? void 0 : option.type) || baseType };
  const Widget = getWidget(optionSchema, widget, widgets2);
  const hideFieldError = uiSchemaHideError === void 0 ? hideError : Boolean(uiSchemaHideError);
  const rawErrors = get_default(errorSchema, [ERRORS_KEY], []);
  const fieldErrorSchema = omit_default(errorSchema, [ERRORS_KEY]);
  const displayLabel = schemaUtils.getDisplayLabel(schema, uiSchema, globalUiOptions);
  const onOptionChange = (opt) => {
    const newOption = getSelectedOption(enumOptions, selectorField, opt);
    const oldOption = getSelectedOption(enumOptions, selectorField, selectedOption);
    let newFormData = schemaUtils.sanitizeDataForNewSchema(newOption, oldOption, formData);
    if (newFormData && newOption) {
      newFormData = schemaUtils.getDefaultFormState(newOption, newFormData, "excludeObjectChildren");
    }
    if (newFormData) {
      set_default(newFormData, selectorField, opt);
    }
    onChange(newFormData, void 0, id);
  };
  const widgetOptions = { enumOptions, ...uiOptions };
  const errors = !hideFieldError && rawErrors.length > 0 ? (0, import_jsx_runtime5.jsx)(FieldErrorTemplate2, { idSchema, schema, errors: rawErrors, registry }) : void 0;
  const ignored = (value) => noop_default;
  return (0, import_jsx_runtime5.jsx)(FieldTemplate2, { id, schema, label: (title || schema.title) ?? "", disabled: disabled || Array.isArray(enumOptions) && isEmpty_default(enumOptions), uiSchema, formContext, required, readonly: !!readonly, registry, displayLabel, errors, onChange, onDropPropertyClick: ignored, onKeyChange: ignored, children: (0, import_jsx_runtime5.jsx)(Widget, { id, name, schema, label: (title || schema.title) ?? "", disabled: disabled || Array.isArray(enumOptions) && isEmpty_default(enumOptions), uiSchema, formContext, autofocus, readonly, required, registry, multiple: false, rawErrors, hideError: hideFieldError, hideLabel: !displayLabel, errorSchema: fieldErrorSchema, placeholder, onChange: onOptionChange, onBlur, onFocus, value: selectedOption, options: widgetOptions }) });
}

// node_modules/@rjsf/core/lib/components/fields/MultiSchemaField.js
var import_jsx_runtime6 = __toESM(require_jsx_runtime(), 1);
var import_react5 = __toESM(require_react(), 1);
var AnyOfField = class extends import_react5.Component {
  /** Constructs an `AnyOfField` with the given `props` to initialize the initially selected option in state
   *
   * @param props - The `FieldProps` for this template
   */
  constructor(props) {
    super(props);
    /** Callback handler to remember what the currently selected option is. In addition to that the `formData` is updated
     * to remove properties that are not part of the newly selected option schema, and then the updated data is passed to
     * the `onChange` handler.
     *
     * @param option - The new option value being selected
     */
    __publicField(this, "onOptionChange", (option) => {
      const { selectedOption, retrievedOptions } = this.state;
      const { formData, onChange, registry } = this.props;
      const { schemaUtils } = registry;
      const intOption = option !== void 0 ? parseInt(option, 10) : -1;
      if (intOption === selectedOption) {
        return;
      }
      const newOption = intOption >= 0 ? retrievedOptions[intOption] : void 0;
      const oldOption = selectedOption >= 0 ? retrievedOptions[selectedOption] : void 0;
      let newFormData = schemaUtils.sanitizeDataForNewSchema(newOption, oldOption, formData);
      if (newOption) {
        newFormData = schemaUtils.getDefaultFormState(newOption, newFormData, "excludeObjectChildren");
      }
      this.setState({ selectedOption: intOption }, () => {
        onChange(newFormData, void 0, this.getFieldId());
      });
    });
    const { formData, options, registry: { schemaUtils } } = this.props;
    const retrievedOptions = options.map((opt) => schemaUtils.retrieveSchema(opt, formData));
    this.state = {
      retrievedOptions,
      selectedOption: this.getMatchingOption(0, formData, retrievedOptions)
    };
  }
  /** React lifecycle method that is called when the props and/or state for this component is updated. It recomputes the
   * currently selected option based on the overall `formData`
   *
   * @param prevProps - The previous `FieldProps` for this template
   * @param prevState - The previous `AnyOfFieldState` for this template
   */
  componentDidUpdate(prevProps, prevState) {
    const { formData, options, idSchema } = this.props;
    const { selectedOption } = this.state;
    let newState = this.state;
    if (!deepEquals(prevProps.options, options)) {
      const { registry: { schemaUtils } } = this.props;
      const retrievedOptions = options.map((opt) => schemaUtils.retrieveSchema(opt, formData));
      newState = { selectedOption, retrievedOptions };
    }
    if (!deepEquals(formData, prevProps.formData) && idSchema.$id === prevProps.idSchema.$id) {
      const { retrievedOptions } = newState;
      const matchingOption = this.getMatchingOption(selectedOption, formData, retrievedOptions);
      if (prevState && matchingOption !== selectedOption) {
        newState = { selectedOption: matchingOption, retrievedOptions };
      }
    }
    if (newState !== this.state) {
      this.setState(newState);
    }
  }
  /** Determines the best matching option for the given `formData` and `options`.
   *
   * @param formData - The new formData
   * @param options - The list of options to choose from
   * @return - The index of the `option` that best matches the `formData`
   */
  getMatchingOption(selectedOption, formData, options) {
    const { schema, registry: { schemaUtils } } = this.props;
    const discriminator = getDiscriminatorFieldFromSchema(schema);
    const option = schemaUtils.getClosestMatchingOption(formData, options, selectedOption, discriminator);
    return option;
  }
  getFieldId() {
    const { idSchema, schema } = this.props;
    return `${idSchema.$id}${schema.oneOf ? "__oneof_select" : "__anyof_select"}`;
  }
  /** Renders the `AnyOfField` selector along with a `SchemaField` for the value of the `formData`
   */
  render() {
    const { name, disabled = false, errorSchema = {}, formContext, onBlur, onFocus, readonly, registry, schema, uiSchema } = this.props;
    const { widgets: widgets2, fields: fields2, translateString, globalUiOptions, schemaUtils } = registry;
    const { SchemaField: _SchemaField } = fields2;
    const MultiSchemaFieldTemplate2 = getTemplate("MultiSchemaFieldTemplate", registry, globalUiOptions);
    const { selectedOption, retrievedOptions } = this.state;
    const { widget = "select", placeholder, autofocus, autocomplete, title = schema.title, ...uiOptions } = getUiOptions(uiSchema, globalUiOptions);
    const Widget = getWidget({ type: "number" }, widget, widgets2);
    const rawErrors = get_default(errorSchema, ERRORS_KEY, []);
    const fieldErrorSchema = omit_default(errorSchema, [ERRORS_KEY]);
    const displayLabel = schemaUtils.getDisplayLabel(schema, uiSchema, globalUiOptions);
    const option = selectedOption >= 0 ? retrievedOptions[selectedOption] || null : null;
    let optionSchema;
    if (option) {
      const { required } = schema;
      optionSchema = required ? mergeSchemas({ required }, option) : option;
    }
    let optionsUiSchema = [];
    if (ONE_OF_KEY in schema && uiSchema && ONE_OF_KEY in uiSchema) {
      if (Array.isArray(uiSchema[ONE_OF_KEY])) {
        optionsUiSchema = uiSchema[ONE_OF_KEY];
      } else {
        console.warn(`uiSchema.oneOf is not an array for "${title || name}"`);
      }
    } else if (ANY_OF_KEY in schema && uiSchema && ANY_OF_KEY in uiSchema) {
      if (Array.isArray(uiSchema[ANY_OF_KEY])) {
        optionsUiSchema = uiSchema[ANY_OF_KEY];
      } else {
        console.warn(`uiSchema.anyOf is not an array for "${title || name}"`);
      }
    }
    let optionUiSchema = uiSchema;
    if (selectedOption >= 0 && optionsUiSchema.length > selectedOption) {
      optionUiSchema = optionsUiSchema[selectedOption];
    }
    const translateEnum = title ? TranslatableString.TitleOptionPrefix : TranslatableString.OptionPrefix;
    const translateParams = title ? [title] : [];
    const enumOptions = retrievedOptions.map((opt, index) => {
      const { title: uiTitle = opt.title } = getUiOptions(optionsUiSchema[index]);
      return {
        label: uiTitle || translateString(translateEnum, translateParams.concat(String(index + 1))),
        value: index
      };
    });
    const selector = (0, import_jsx_runtime6.jsx)(Widget, { id: this.getFieldId(), name: `${name}${schema.oneOf ? "__oneof_select" : "__anyof_select"}`, schema: { type: "number", default: 0 }, onChange: this.onOptionChange, onBlur, onFocus, disabled: disabled || isEmpty_default(enumOptions), multiple: false, rawErrors, errorSchema: fieldErrorSchema, value: selectedOption >= 0 ? selectedOption : void 0, options: { enumOptions, ...uiOptions }, registry, formContext, placeholder, autocomplete, autofocus, label: title ?? name, hideLabel: !displayLabel, readonly });
    const optionsSchemaField = optionSchema && optionSchema.type !== "null" && (0, import_jsx_runtime6.jsx)(_SchemaField, { ...this.props, schema: optionSchema, uiSchema: optionUiSchema }) || null;
    return (0, import_jsx_runtime6.jsx)(MultiSchemaFieldTemplate2, { schema, registry, uiSchema, selector, optionSchemaField: optionsSchemaField });
  }
};
var MultiSchemaField_default = AnyOfField;

// node_modules/@rjsf/core/lib/components/fields/NumberField.js
var import_jsx_runtime7 = __toESM(require_jsx_runtime(), 1);
var import_react6 = __toESM(require_react(), 1);
var trailingCharMatcherWithPrefix = /\.([0-9]*0)*$/;
var trailingCharMatcher = /[0.]0*$/;
function NumberField(props) {
  const { registry, onChange, formData, value: initialValue } = props;
  const [lastValue, setLastValue] = (0, import_react6.useState)(initialValue);
  const { StringField: StringField2 } = registry.fields;
  let value = formData;
  const handleChange = (0, import_react6.useCallback)((value2, errorSchema, id) => {
    setLastValue(value2);
    if (`${value2}`.charAt(0) === ".") {
      value2 = `0${value2}`;
    }
    const processed = typeof value2 === "string" && value2.match(trailingCharMatcherWithPrefix) ? asNumber(value2.replace(trailingCharMatcher, "")) : asNumber(value2);
    onChange(processed, errorSchema, id);
  }, [onChange]);
  if (typeof lastValue === "string" && typeof value === "number") {
    const re2 = new RegExp(`^(${String(value).replace(".", "\\.")})?\\.?0*$`);
    if (lastValue.match(re2)) {
      value = lastValue;
    }
  }
  return (0, import_jsx_runtime7.jsx)(StringField2, { ...props, formData: value, onChange: handleChange });
}
var NumberField_default = NumberField;

// node_modules/@rjsf/core/lib/components/fields/ObjectField.js
var import_jsx_runtime8 = __toESM(require_jsx_runtime(), 1);
var import_react7 = __toESM(require_react(), 1);

// node_modules/markdown-to-jsx/dist/index.modern.js
var e = __toESM(require_react());
function t() {
  return t = Object.assign ? Object.assign.bind() : function(e2) {
    for (var t2 = 1; t2 < arguments.length; t2++) {
      var n2 = arguments[t2];
      for (var r2 in n2) Object.prototype.hasOwnProperty.call(n2, r2) && (e2[r2] = n2[r2]);
    }
    return e2;
  }, t.apply(this, arguments);
}
var n = ["children", "options"];
var r = { blockQuote: "0", breakLine: "1", breakThematic: "2", codeBlock: "3", codeFenced: "4", codeInline: "5", footnote: "6", footnoteReference: "7", gfmTask: "8", heading: "9", headingSetext: "10", htmlBlock: "11", htmlComment: "12", htmlSelfClosing: "13", image: "14", link: "15", linkAngleBraceStyleDetector: "16", linkBareUrlDetector: "17", linkMailtoDetector: "18", newlineCoalescer: "19", orderedList: "20", paragraph: "21", ref: "22", refImage: "23", refLink: "24", table: "25", tableSeparator: "26", text: "27", textBolded: "28", textEmphasized: "29", textEscaped: "30", textMarked: "31", textStrikethroughed: "32", unorderedList: "33" };
var i;
!function(e2) {
  e2[e2.MAX = 0] = "MAX", e2[e2.HIGH = 1] = "HIGH", e2[e2.MED = 2] = "MED", e2[e2.LOW = 3] = "LOW", e2[e2.MIN = 4] = "MIN";
}(i || (i = {}));
var l = ["allowFullScreen", "allowTransparency", "autoComplete", "autoFocus", "autoPlay", "cellPadding", "cellSpacing", "charSet", "classId", "colSpan", "contentEditable", "contextMenu", "crossOrigin", "encType", "formAction", "formEncType", "formMethod", "formNoValidate", "formTarget", "frameBorder", "hrefLang", "inputMode", "keyParams", "keyType", "marginHeight", "marginWidth", "maxLength", "mediaGroup", "minLength", "noValidate", "radioGroup", "readOnly", "rowSpan", "spellCheck", "srcDoc", "srcLang", "srcSet", "tabIndex", "useMap"].reduce((e2, t2) => (e2[t2.toLowerCase()] = t2, e2), { class: "className", for: "htmlFor" });
var o = { amp: "&", apos: "'", gt: ">", lt: "<", nbsp: " ", quot: "“" };
var a = ["style", "script"];
var c = ["src", "href", "data", "formAction", "srcDoc", "action"];
var s = /([-A-Z0-9_:]+)(?:\s*=\s*(?:(?:"((?:\\.|[^"])*)")|(?:'((?:\\.|[^'])*)')|(?:\{((?:\\.|{[^}]*?}|[^}])*)\})))?/gi;
var d = /mailto:/i;
var u = /\n{2,}$/;
var p = /^(\s*>[\s\S]*?)(?=\n\n|$)/;
var f = /^ *> ?/gm;
var h = /^(?:\[!([^\]]*)\]\n)?([\s\S]*)/;
var m = /^ {2,}\n/;
var g = /^(?:( *[-*_])){3,} *(?:\n *)+\n/;
var y = /^(?: {1,3})?(`{3,}|~{3,}) *(\S+)? *([^\n]*?)?\n([\s\S]*?)(?:\1\n?|$)/;
var k = /^(?: {4}[^\n]+\n*)+(?:\n *)+\n?/;
var x = /^(`+)((?:\\`|(?!\1)`|[^`])+)\1/;
var b = /^(?:\n *)*\n/;
var v = /\r\n?/g;
var C = /^\[\^([^\]]+)](:(.*)((\n+ {4,}.*)|(\n(?!\[\^).+))*)/;
var $ = /^\[\^([^\]]+)]/;
var S = /\f/g;
var w = /^---[ \t]*\n(.|\n)*\n---[ \t]*\n/;
var E = /^\s*?\[(x|\s)\]/;
var z = /^ *(#{1,6}) *([^\n]+?)(?: +#*)?(?:\n *)*(?:\n|$)/;
var L = /^ *(#{1,6}) +([^\n]+?)(?: +#*)?(?:\n *)*(?:\n|$)/;
var A = /^([^\n]+)\n *(=|-){3,} *(?:\n *)+\n/;
var O = /^ *(?!<[a-z][^ >/]* ?\/>)<([a-z][^ >/]*) ?((?:[^>]*[^/])?)>\n?(\s*(?:<\1[^>]*?>[\s\S]*?<\/\1>|(?!<\1\b)[\s\S])*?)<\/\1>(?!<\/\1>)\n*/i;
var T = /&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-fA-F]{1,6});/gi;
var B = /^<!--[\s\S]*?(?:-->)/;
var M = /^(data|aria|x)-[a-z_][a-z\d_.-]*$/;
var R = /^ *<([a-z][a-z0-9:]*)(?:\s+((?:<.*?>|[^>])*))?\/?>(?!<\/\1>)(\s*\n)?/i;
var I = /^\{.*\}$/;
var D = /^(https?:\/\/[^\s<]+[^<.,:;"')\]\s])/;
var U = /^<([^ >]+@[^ >]+)>/;
var N = /^<([^ >]+:\/[^ >]+)>/;
var j = /-([a-z])?/gi;
var H = /^(\|.*)\n(?: *(\|? *[-:]+ *\|[-| :]*)\n((?:.*\|.*\n)*))?\n?/;
var P = /^[^\n]+(?:  \n|\n{2,})/;
var _ = /^\[([^\]]*)\]:\s+<?([^\s>]+)>?\s*("([^"]*)")?/;
var F = /^!\[([^\]]*)\] ?\[([^\]]*)\]/;
var W = /^\[([^\]]*)\] ?\[([^\]]*)\]/;
var G = /(\n|^[-*]\s|^#|^ {2,}|^-{2,}|^>\s)/;
var Z = /\t/g;
var q = /(^ *\||\| *$)/g;
var Q = /^ *:-+: *$/;
var V = /^ *:-+ *$/;
var X = /^ *-+: *$/;
var J = "((?:\\[.*?\\][([].*?[)\\]]|<.*?>(?:.*?<.*?>)?|`.*?`|\\\\\\1|[\\s\\S])+?)";
var K = new RegExp(`^([*_])\\1${J}\\1\\1(?!\\1)`);
var Y = new RegExp(`^([*_])${J}\\1(?!\\1)`);
var ee = new RegExp(`^(==)${J}\\1`);
var te = new RegExp(`^(~~)${J}\\1`);
var ne = /^\\([^0-9A-Za-z\s])/;
var re = /\\([^0-9A-Za-z\s])/g;
var ie = /^(?: |[\s\S](?:(?!  |[0-9]\.)[^=*_~\-\n<`\\\[! ])*)/;
var le = /^\n+/;
var oe = /^([ \t]*)/;
var ae = /\\([^\\])/g;
var ce = /(?:^|\n)( *)$/;
var se = "(?:\\d+\\.)";
var de = "(?:[*+-])";
function ue(e2) {
  return "( *)(" + (1 === e2 ? se : de) + ") +";
}
var pe = ue(1);
var fe = ue(2);
function he(e2) {
  return new RegExp("^" + (1 === e2 ? pe : fe));
}
var me = he(1);
var ge = he(2);
function ye(e2) {
  return new RegExp("^" + (1 === e2 ? pe : fe) + "[^\\n]*(?:\\n(?!\\1" + (1 === e2 ? se : de) + " )[^\\n]*)*(\\n|$)", "gm");
}
var ke = ye(1);
var xe = ye(2);
function be(e2) {
  const t2 = 1 === e2 ? se : de;
  return new RegExp("^( *)(" + t2 + ") [\\s\\S]+?(?:\\n{2,}(?! )(?!\\1" + t2 + " (?!" + t2 + " ))\\n*|\\s*\\n*$)");
}
var ve = be(1);
var Ce = be(2);
function $e(e2, t2) {
  const n2 = 1 === t2, i2 = n2 ? ve : Ce, l2 = n2 ? ke : xe, o2 = n2 ? me : ge;
  return { match: Be(function(e3, t3) {
    const n3 = ce.exec(t3.prevCapture);
    return n3 && (t3.list || !t3.inline && !t3.simple) ? i2.exec(e3 = n3[1] + e3) : null;
  }), order: 1, parse(e3, t3, r2) {
    const i3 = n2 ? +e3[2] : void 0, a2 = e3[0].replace(u, "\n").match(l2);
    let c2 = false;
    return { items: a2.map(function(e4, n3) {
      const i4 = o2.exec(e4)[0].length, l3 = new RegExp("^ {1," + i4 + "}", "gm"), s2 = e4.replace(l3, "").replace(o2, ""), d2 = n3 === a2.length - 1, u2 = -1 !== s2.indexOf("\n\n") || d2 && c2;
      c2 = u2;
      const p2 = r2.inline, f2 = r2.list;
      let h2;
      r2.list = true, u2 ? (r2.inline = false, h2 = Ee(s2) + "\n\n") : (r2.inline = true, h2 = Ee(s2));
      const m2 = t3(h2, r2);
      return r2.inline = p2, r2.list = f2, m2;
    }), ordered: n2, start: i3 };
  }, render: (t3, n3, i3) => e2(t3.ordered ? "ol" : "ul", { key: i3.key, start: t3.type === r.orderedList ? t3.start : void 0 }, t3.items.map(function(t4, r2) {
    return e2("li", { key: r2 }, n3(t4, i3));
  })) };
}
var Se = new RegExp(`^\\[((?:\\[[^\\]]*\\]|[^\\[\\]]|\\](?=[^\\[]*\\]))*)\\]\\(\\s*<?((?:\\([^)]*\\)|[^\\s\\\\]|\\\\.)*?)>?(?:\\s+['"]([\\s\\S]*?)['"])?\\s*\\)`);
var we = /^!\[(.*?)\]\( *((?:\([^)]*\)|[^() ])*) *"?([^)"]*)?"?\)/;
function Ee(e2) {
  let t2 = e2.length;
  for (; t2 > 0 && e2[t2 - 1] <= " "; ) t2--;
  return e2.slice(0, t2);
}
function ze(e2) {
  return e2.replace(/[ÀÁÂÃÄÅàáâãäåæÆ]/g, "a").replace(/[çÇ]/g, "c").replace(/[ðÐ]/g, "d").replace(/[ÈÉÊËéèêë]/g, "e").replace(/[ÏïÎîÍíÌì]/g, "i").replace(/[Ññ]/g, "n").replace(/[øØœŒÕõÔôÓóÒò]/g, "o").replace(/[ÜüÛûÚúÙù]/g, "u").replace(/[ŸÿÝý]/g, "y").replace(/[^a-z0-9- ]/gi, "").replace(/ /gi, "-").toLowerCase();
}
function Le(e2) {
  return X.test(e2) ? "right" : Q.test(e2) ? "center" : V.test(e2) ? "left" : null;
}
function Ae(e2, t2, n2, r2) {
  const i2 = n2.inTable;
  n2.inTable = true;
  let l2 = [[]], o2 = "";
  function a2() {
    if (!o2) return;
    const e3 = l2[l2.length - 1];
    e3.push.apply(e3, t2(o2, n2)), o2 = "";
  }
  return e2.trim().split(/(`[^`]*`|\\\||\|)/).filter(Boolean).forEach((e3, t3, n3) => {
    "|" === e3.trim() && (a2(), r2) ? 0 !== t3 && t3 !== n3.length - 1 && l2.push([]) : o2 += e3;
  }), a2(), n2.inTable = i2, l2;
}
function Oe(e2, t2, n2) {
  n2.inline = true;
  const i2 = e2[2] ? e2[2].replace(q, "").split("|").map(Le) : [], l2 = e2[3] ? function(e3, t3, n3) {
    return e3.trim().split("\n").map(function(e4) {
      return Ae(e4, t3, n3, true);
    });
  }(e2[3], t2, n2) : [], o2 = Ae(e2[1], t2, n2, !!l2.length);
  return n2.inline = false, l2.length ? { align: i2, cells: l2, header: o2, type: r.table } : { children: o2, type: r.paragraph };
}
function Te(e2, t2) {
  return null == e2.align[t2] ? {} : { textAlign: e2.align[t2] };
}
function Be(e2) {
  return e2.inline = 1, e2;
}
function Me(e2) {
  return Be(function(t2, n2) {
    return n2.inline ? e2.exec(t2) : null;
  });
}
function Re(e2) {
  return Be(function(t2, n2) {
    return n2.inline || n2.simple ? e2.exec(t2) : null;
  });
}
function Ie(e2) {
  return function(t2, n2) {
    return n2.inline || n2.simple ? null : e2.exec(t2);
  };
}
function De(e2) {
  return Be(function(t2) {
    return e2.exec(t2);
  });
}
var Ue = /(javascript|vbscript|data(?!:image)):/i;
function Ne(e2) {
  try {
    const t2 = decodeURIComponent(e2).replace(/[^A-Za-z0-9/:]/g, "");
    if (Ue.test(t2)) return null;
  } catch (e3) {
    return null;
  }
  return e2;
}
function je(e2) {
  return e2.replace(ae, "$1");
}
function He(e2, t2, n2) {
  const r2 = n2.inline || false, i2 = n2.simple || false;
  n2.inline = true, n2.simple = true;
  const l2 = e2(t2, n2);
  return n2.inline = r2, n2.simple = i2, l2;
}
function Pe(e2, t2, n2) {
  const r2 = n2.inline || false, i2 = n2.simple || false;
  n2.inline = false, n2.simple = true;
  const l2 = e2(t2, n2);
  return n2.inline = r2, n2.simple = i2, l2;
}
function _e(e2, t2, n2) {
  const r2 = n2.inline || false;
  n2.inline = false;
  const i2 = e2(t2, n2);
  return n2.inline = r2, i2;
}
var Fe = (e2, t2, n2) => ({ children: He(t2, e2[2], n2) });
function We() {
  return {};
}
function Ge() {
  return null;
}
function Ze(...e2) {
  return e2.filter(Boolean).join(" ");
}
function qe(e2, t2, n2) {
  let r2 = e2;
  const i2 = t2.split(".");
  for (; i2.length && (r2 = r2[i2[0]], void 0 !== r2); ) i2.shift();
  return r2 || n2;
}
function Qe(n2 = "", i2 = {}) {
  i2.overrides = i2.overrides || {}, i2.sanitizer = i2.sanitizer || Ne, i2.slugify = i2.slugify || ze, i2.namedCodesToUnicode = i2.namedCodesToUnicode ? t({}, o, i2.namedCodesToUnicode) : o, i2.createElement = i2.createElement || e.createElement;
  const u2 = [p, y, k, i2.enforceAtxHeadings ? L : z, A, H, ve, Ce], q2 = [...u2, P, O, B, R];
  function Q2(e2, n3, ...r2) {
    const l2 = qe(i2.overrides, `${e2}.props`, {});
    return i2.createElement(function(e3, t2) {
      const n4 = qe(t2, e3);
      return n4 ? "function" == typeof n4 || "object" == typeof n4 && "render" in n4 ? n4 : qe(t2, `${e3}.component`, e3) : e3;
    }(e2, i2.overrides), t({}, n3, l2, { className: Ze(null == n3 ? void 0 : n3.className, l2.className) || void 0 }), ...r2);
  }
  function V2(e2) {
    e2 = e2.replace(w, "");
    let t2 = false;
    i2.forceInline ? t2 = true : i2.forceBlock || (t2 = false === G.test(e2));
    const n3 = de2(se2(t2 ? e2 : `${Ee(e2).replace(le, "")}

`, { inline: t2 }));
    for (; "string" == typeof n3[n3.length - 1] && !n3[n3.length - 1].trim(); ) n3.pop();
    if (null === i2.wrapper) return n3;
    const r2 = i2.wrapper || (t2 ? "span" : "div");
    let l2;
    if (n3.length > 1 || i2.forceWrapper) l2 = n3;
    else {
      if (1 === n3.length) return l2 = n3[0], "string" == typeof l2 ? Q2("span", { key: "outer" }, l2) : l2;
      l2 = null;
    }
    return i2.createElement(r2, { key: "outer" }, l2);
  }
  function X2(e2, t2) {
    const n3 = t2.match(s);
    return n3 ? n3.reduce(function(t3, n4) {
      const r2 = n4.indexOf("=");
      if (-1 !== r2) {
        const o2 = function(e3) {
          return -1 !== e3.indexOf("-") && null === e3.match(M) && (e3 = e3.replace(j, function(e4, t4) {
            return t4.toUpperCase();
          })), e3;
        }(n4.slice(0, r2)).trim(), a2 = function(e3) {
          const t4 = e3[0];
          return ('"' === t4 || "'" === t4) && e3.length >= 2 && e3[e3.length - 1] === t4 ? e3.slice(1, -1) : e3;
        }(n4.slice(r2 + 1).trim()), s2 = l[o2] || o2;
        if ("ref" === s2) return t3;
        const d2 = t3[s2] = function(e3, t4, n5, r3) {
          return "style" === t4 ? function(e4) {
            const t5 = [];
            let n6 = "", r4 = false, i3 = false, l2 = "";
            if (!e4) return t5;
            for (let o4 = 0; o4 < e4.length; o4++) {
              const a3 = e4[o4];
              if ('"' !== a3 && "'" !== a3 || r4 || (i3 ? a3 === l2 && (i3 = false, l2 = "") : (i3 = true, l2 = a3)), "(" === a3 && n6.endsWith("url") ? r4 = true : ")" === a3 && r4 && (r4 = false), ";" !== a3 || i3 || r4) n6 += a3;
              else {
                const e5 = n6.trim();
                if (e5) {
                  const n7 = e5.indexOf(":");
                  if (n7 > 0) {
                    const r5 = e5.slice(0, n7).trim(), i4 = e5.slice(n7 + 1).trim();
                    t5.push([r5, i4]);
                  }
                }
                n6 = "";
              }
            }
            const o3 = n6.trim();
            if (o3) {
              const e5 = o3.indexOf(":");
              if (e5 > 0) {
                const n7 = o3.slice(0, e5).trim(), r5 = o3.slice(e5 + 1).trim();
                t5.push([n7, r5]);
              }
            }
            return t5;
          }(n5).reduce(function(t5, [n6, i3]) {
            return t5[n6.replace(/(-[a-z])/g, (e4) => e4[1].toUpperCase())] = r3(i3, e3, n6), t5;
          }, {}) : -1 !== c.indexOf(t4) ? r3(n5, e3, t4) : (n5.match(I) && (n5 = n5.slice(1, n5.length - 1)), "true" === n5 || "false" !== n5 && n5);
        }(e2, o2, a2, i2.sanitizer);
        "string" == typeof d2 && (O.test(d2) || R.test(d2)) && (t3[s2] = V2(d2.trim()));
      } else "style" !== n4 && (t3[l[n4] || n4] = true);
      return t3;
    }, {}) : null;
  }
  const J2 = [], ae2 = {}, ce2 = { [r.blockQuote]: { match: Ie(p), order: 1, parse(e2, t2, n3) {
    const [, r2, i3] = e2[0].replace(f, "").match(h);
    return { alert: r2, children: t2(i3, n3) };
  }, render(e2, t2, n3) {
    const l2 = { key: n3.key };
    return e2.alert && (l2.className = "markdown-alert-" + i2.slugify(e2.alert.toLowerCase(), ze), e2.children.unshift({ attrs: {}, children: [{ type: r.text, text: e2.alert }], noInnerParse: true, type: r.htmlBlock, tag: "header" })), Q2("blockquote", l2, t2(e2.children, n3));
  } }, [r.breakLine]: { match: De(m), order: 1, parse: We, render: (e2, t2, n3) => Q2("br", { key: n3.key }) }, [r.breakThematic]: { match: Ie(g), order: 1, parse: We, render: (e2, t2, n3) => Q2("hr", { key: n3.key }) }, [r.codeBlock]: { match: Ie(k), order: 0, parse: (e2) => ({ lang: void 0, text: Ee(e2[0].replace(/^ {4}/gm, "")).replace(re, "$1") }), render: (e2, n3, r2) => Q2("pre", { key: r2.key }, Q2("code", t({}, e2.attrs, { className: e2.lang ? `lang-${e2.lang}` : "" }), e2.text)) }, [r.codeFenced]: { match: Ie(y), order: 0, parse: (e2) => ({ attrs: X2("code", e2[3] || ""), lang: e2[2] || void 0, text: e2[4], type: r.codeBlock }) }, [r.codeInline]: { match: Re(x), order: 3, parse: (e2) => ({ text: e2[2].replace(re, "$1") }), render: (e2, t2, n3) => Q2("code", { key: n3.key }, e2.text) }, [r.footnote]: { match: Ie(C), order: 0, parse: (e2) => (J2.push({ footnote: e2[2], identifier: e2[1] }), {}), render: Ge }, [r.footnoteReference]: { match: Me($), order: 1, parse: (e2) => ({ target: `#${i2.slugify(e2[1], ze)}`, text: e2[1] }), render: (e2, t2, n3) => Q2("a", { key: n3.key, href: i2.sanitizer(e2.target, "a", "href") }, Q2("sup", { key: n3.key }, e2.text)) }, [r.gfmTask]: { match: Me(E), order: 1, parse: (e2) => ({ completed: "x" === e2[1].toLowerCase() }), render: (e2, t2, n3) => Q2("input", { checked: e2.completed, key: n3.key, readOnly: true, type: "checkbox" }) }, [r.heading]: { match: Ie(i2.enforceAtxHeadings ? L : z), order: 1, parse: (e2, t2, n3) => ({ children: He(t2, e2[2], n3), id: i2.slugify(e2[2], ze), level: e2[1].length }), render: (e2, t2, n3) => Q2(`h${e2.level}`, { id: e2.id, key: n3.key }, t2(e2.children, n3)) }, [r.headingSetext]: { match: Ie(A), order: 0, parse: (e2, t2, n3) => ({ children: He(t2, e2[1], n3), level: "=" === e2[2] ? 1 : 2, type: r.heading }) }, [r.htmlBlock]: { match: De(O), order: 1, parse(e2, t2, n3) {
    const [, r2] = e2[3].match(oe), i3 = new RegExp(`^${r2}`, "gm"), l2 = e2[3].replace(i3, ""), o2 = (c2 = l2, q2.some((e3) => e3.test(c2)) ? _e : He);
    var c2;
    const s2 = e2[1].toLowerCase(), d2 = -1 !== a.indexOf(s2), u3 = (d2 ? s2 : e2[1]).trim(), p2 = { attrs: X2(u3, e2[2]), noInnerParse: d2, tag: u3 };
    return n3.inAnchor = n3.inAnchor || "a" === s2, d2 ? p2.text = e2[3] : p2.children = o2(t2, l2, n3), n3.inAnchor = false, p2;
  }, render: (e2, n3, r2) => Q2(e2.tag, t({ key: r2.key }, e2.attrs), e2.text || (e2.children ? n3(e2.children, r2) : "")) }, [r.htmlSelfClosing]: { match: De(R), order: 1, parse(e2) {
    const t2 = e2[1].trim();
    return { attrs: X2(t2, e2[2] || ""), tag: t2 };
  }, render: (e2, n3, r2) => Q2(e2.tag, t({}, e2.attrs, { key: r2.key })) }, [r.htmlComment]: { match: De(B), order: 1, parse: () => ({}), render: Ge }, [r.image]: { match: Re(we), order: 1, parse: (e2) => ({ alt: e2[1], target: je(e2[2]), title: e2[3] }), render: (e2, t2, n3) => Q2("img", { key: n3.key, alt: e2.alt || void 0, title: e2.title || void 0, src: i2.sanitizer(e2.target, "img", "src") }) }, [r.link]: { match: Me(Se), order: 3, parse: (e2, t2, n3) => ({ children: Pe(t2, e2[1], n3), target: je(e2[2]), title: e2[3] }), render: (e2, t2, n3) => Q2("a", { key: n3.key, href: i2.sanitizer(e2.target, "a", "href"), title: e2.title }, t2(e2.children, n3)) }, [r.linkAngleBraceStyleDetector]: { match: Me(N), order: 0, parse: (e2) => ({ children: [{ text: e2[1], type: r.text }], target: e2[1], type: r.link }) }, [r.linkBareUrlDetector]: { match: Be((e2, t2) => t2.inAnchor || i2.disableAutoLink ? null : Me(D)(e2, t2)), order: 0, parse: (e2) => ({ children: [{ text: e2[1], type: r.text }], target: e2[1], title: void 0, type: r.link }) }, [r.linkMailtoDetector]: { match: Me(U), order: 0, parse(e2) {
    let t2 = e2[1], n3 = e2[1];
    return d.test(n3) || (n3 = "mailto:" + n3), { children: [{ text: t2.replace("mailto:", ""), type: r.text }], target: n3, type: r.link };
  } }, [r.orderedList]: $e(Q2, 1), [r.unorderedList]: $e(Q2, 2), [r.newlineCoalescer]: { match: Ie(b), order: 3, parse: We, render: () => "\n" }, [r.paragraph]: { match: Be(function(e2, t2) {
    if (t2.inline || t2.simple) return null;
    let n3 = "";
    e2.split("\n").every((e3) => (e3 += "\n", !u2.some((t3) => t3.test(e3)) && (n3 += e3, !!e3.trim())));
    const r2 = Ee(n3);
    return "" == r2 ? null : [n3, , r2];
  }), order: 3, parse: Fe, render: (e2, t2, n3) => Q2("p", { key: n3.key }, t2(e2.children, n3)) }, [r.ref]: { match: Me(_), order: 0, parse: (e2) => (ae2[e2[1]] = { target: e2[2], title: e2[4] }, {}), render: Ge }, [r.refImage]: { match: Re(F), order: 0, parse: (e2) => ({ alt: e2[1] || void 0, ref: e2[2] }), render: (e2, t2, n3) => ae2[e2.ref] ? Q2("img", { key: n3.key, alt: e2.alt, src: i2.sanitizer(ae2[e2.ref].target, "img", "src"), title: ae2[e2.ref].title }) : null }, [r.refLink]: { match: Me(W), order: 0, parse: (e2, t2, n3) => ({ children: t2(e2[1], n3), fallbackChildren: e2[0], ref: e2[2] }), render: (e2, t2, n3) => ae2[e2.ref] ? Q2("a", { key: n3.key, href: i2.sanitizer(ae2[e2.ref].target, "a", "href"), title: ae2[e2.ref].title }, t2(e2.children, n3)) : Q2("span", { key: n3.key }, e2.fallbackChildren) }, [r.table]: { match: Ie(H), order: 1, parse: Oe, render(e2, t2, n3) {
    const r2 = e2;
    return Q2("table", { key: n3.key }, Q2("thead", null, Q2("tr", null, r2.header.map(function(e3, i3) {
      return Q2("th", { key: i3, style: Te(r2, i3) }, t2(e3, n3));
    }))), Q2("tbody", null, r2.cells.map(function(e3, i3) {
      return Q2("tr", { key: i3 }, e3.map(function(e4, i4) {
        return Q2("td", { key: i4, style: Te(r2, i4) }, t2(e4, n3));
      }));
    })));
  } }, [r.text]: { match: De(ie), order: 4, parse: (e2) => ({ text: e2[0].replace(T, (e3, t2) => i2.namedCodesToUnicode[t2] ? i2.namedCodesToUnicode[t2] : e3) }), render: (e2) => e2.text }, [r.textBolded]: { match: Re(K), order: 2, parse: (e2, t2, n3) => ({ children: t2(e2[2], n3) }), render: (e2, t2, n3) => Q2("strong", { key: n3.key }, t2(e2.children, n3)) }, [r.textEmphasized]: { match: Re(Y), order: 3, parse: (e2, t2, n3) => ({ children: t2(e2[2], n3) }), render: (e2, t2, n3) => Q2("em", { key: n3.key }, t2(e2.children, n3)) }, [r.textEscaped]: { match: Re(ne), order: 1, parse: (e2) => ({ text: e2[1], type: r.text }) }, [r.textMarked]: { match: Re(ee), order: 3, parse: Fe, render: (e2, t2, n3) => Q2("mark", { key: n3.key }, t2(e2.children, n3)) }, [r.textStrikethroughed]: { match: Re(te), order: 3, parse: Fe, render: (e2, t2, n3) => Q2("del", { key: n3.key }, t2(e2.children, n3)) } };
  true === i2.disableParsingRawHTML && (delete ce2[r.htmlBlock], delete ce2[r.htmlSelfClosing]);
  const se2 = function(e2) {
    let t2 = Object.keys(e2);
    function n3(r2, i3) {
      let l2, o2, a2 = [], c2 = "", s2 = "";
      for (i3.prevCapture = i3.prevCapture || ""; r2; ) {
        let d2 = 0;
        for (; d2 < t2.length; ) {
          if (c2 = t2[d2], l2 = e2[c2], i3.inline && !l2.match.inline) {
            d2++;
            continue;
          }
          const u3 = l2.match(r2, i3);
          if (u3) {
            s2 = u3[0], i3.prevCapture += s2, r2 = r2.substring(s2.length), o2 = l2.parse(u3, n3, i3), null == o2.type && (o2.type = c2), a2.push(o2);
            break;
          }
          d2++;
        }
      }
      return i3.prevCapture = "", a2;
    }
    return t2.sort(function(t3, n4) {
      let r2 = e2[t3].order, i3 = e2[n4].order;
      return r2 !== i3 ? r2 - i3 : t3 < n4 ? -1 : 1;
    }), function(e3, t3) {
      return n3(function(e4) {
        return e4.replace(v, "\n").replace(S, "").replace(Z, "    ");
      }(e3), t3);
    };
  }(ce2), de2 = (ue2 = /* @__PURE__ */ function(e2, t2) {
    return function(n3, r2, i3) {
      const l2 = e2[n3.type].render;
      return t2 ? t2(() => l2(n3, r2, i3), n3, r2, i3) : l2(n3, r2, i3);
    };
  }(ce2, i2.renderRule), function e2(t2, n3 = {}) {
    if (Array.isArray(t2)) {
      const r2 = n3.key, i3 = [];
      let l2 = false;
      for (let r3 = 0; r3 < t2.length; r3++) {
        n3.key = r3;
        const o2 = e2(t2[r3], n3), a2 = "string" == typeof o2;
        a2 && l2 ? i3[i3.length - 1] += o2 : null !== o2 && i3.push(o2), l2 = a2;
      }
      return n3.key = r2, i3;
    }
    return ue2(t2, e2, n3);
  });
  var ue2;
  const pe2 = V2(n2);
  return J2.length ? Q2("div", null, pe2, Q2("footer", { key: "footer" }, J2.map(function(e2) {
    return Q2("div", { id: i2.slugify(e2.identifier, ze), key: e2.identifier }, e2.identifier, de2(se2(e2.footnote, { inline: true })));
  }))) : pe2;
}
var index_modern_default = (t2) => {
  let { children: r2 = "", options: i2 } = t2, l2 = function(e2, t3) {
    if (null == e2) return {};
    var n2, r3, i3 = {}, l3 = Object.keys(e2);
    for (r3 = 0; r3 < l3.length; r3++) t3.indexOf(n2 = l3[r3]) >= 0 || (i3[n2] = e2[n2]);
    return i3;
  }(t2, n);
  return e.cloneElement(Qe(r2, i2), l2);
};

// node_modules/lodash-es/unset.js
function unset(object, path) {
  return object == null ? true : baseUnset_default(object, path);
}
var unset_default = unset;

// node_modules/@rjsf/core/lib/components/fields/ObjectField.js
var ObjectField = class extends import_react7.Component {
  constructor() {
    super(...arguments);
    /** Set up the initial state */
    __publicField(this, "state", {
      wasPropertyKeyModified: false,
      additionalProperties: {}
    });
    /** Returns the `onPropertyChange` handler for the `name` field. Handles the special case where a user is attempting
     * to clear the data for a field added as an additional property. Calls the `onChange()` handler with the updated
     * formData.
     *
     * @param name - The name of the property
     * @param addedByAdditionalProperties - Flag indicating whether this property is an additional property
     * @returns - The onPropertyChange callback for the `name` property
     */
    __publicField(this, "onPropertyChange", (name, addedByAdditionalProperties = false) => {
      return (value, newErrorSchema, id) => {
        const { formData, onChange, errorSchema } = this.props;
        if (value === void 0 && addedByAdditionalProperties) {
          value = "";
        }
        const newFormData = { ...formData, [name]: value };
        onChange(newFormData, errorSchema && errorSchema && {
          ...errorSchema,
          [name]: newErrorSchema
        }, id);
      };
    });
    /** Returns a callback to handle the onDropPropertyClick event for the given `key` which removes the old `key` data
     * and calls the `onChange` callback with it
     *
     * @param key - The key for which the drop callback is desired
     * @returns - The drop property click callback
     */
    __publicField(this, "onDropPropertyClick", (key) => {
      return (event) => {
        event.preventDefault();
        const { onChange, formData } = this.props;
        const copiedFormData = { ...formData };
        unset_default(copiedFormData, key);
        onChange(copiedFormData);
      };
    });
    /** Computes the next available key name from the `preferredKey`, indexing through the already existing keys until one
     * that is already not assigned is found.
     *
     * @param preferredKey - The preferred name of a new key
     * @param [formData] - The form data in which to check if the desired key already exists
     * @returns - The name of the next available key from `preferredKey`
     */
    __publicField(this, "getAvailableKey", (preferredKey, formData) => {
      const { uiSchema, registry } = this.props;
      const { duplicateKeySuffixSeparator = "-" } = getUiOptions(uiSchema, registry.globalUiOptions);
      let index = 0;
      let newKey = preferredKey;
      while (has_default(formData, newKey)) {
        newKey = `${preferredKey}${duplicateKeySuffixSeparator}${++index}`;
      }
      return newKey;
    });
    /** Returns a callback function that deals with the rename of a key for an additional property for a schema. That
     * callback will attempt to rename the key and move the existing data to that key, calling `onChange` when it does.
     *
     * @param oldValue - The old value of a field
     * @returns - The key change callback function
     */
    __publicField(this, "onKeyChange", (oldValue) => {
      return (value, newErrorSchema) => {
        if (oldValue === value) {
          return;
        }
        const { formData, onChange, errorSchema } = this.props;
        value = this.getAvailableKey(value, formData);
        const newFormData = {
          ...formData
        };
        const newKeys = { [oldValue]: value };
        const keyValues = Object.keys(newFormData).map((key) => {
          const newKey = newKeys[key] || key;
          return { [newKey]: newFormData[key] };
        });
        const renamedObj = Object.assign({}, ...keyValues);
        this.setState({ wasPropertyKeyModified: true });
        onChange(renamedObj, errorSchema && errorSchema && {
          ...errorSchema,
          [value]: newErrorSchema
        });
      };
    });
    /** Handles the adding of a new additional property on the given `schema`. Calls the `onChange` callback once the new
     * default data for that field has been added to the formData.
     *
     * @param schema - The schema element to which the new property is being added
     */
    __publicField(this, "handleAddClick", (schema) => () => {
      if (!(schema.additionalProperties || schema.patternProperties)) {
        return;
      }
      const { formData, onChange, registry } = this.props;
      const newFormData = { ...formData };
      const newKey = this.getAvailableKey("newKey", newFormData);
      if (schema.patternProperties) {
        set_default(newFormData, newKey, null);
      } else {
        let type = void 0;
        let constValue = void 0;
        let defaultValue = void 0;
        if (isObject_default(schema.additionalProperties)) {
          type = schema.additionalProperties.type;
          constValue = schema.additionalProperties.const;
          defaultValue = schema.additionalProperties.default;
          let apSchema = schema.additionalProperties;
          if (REF_KEY in apSchema) {
            const { schemaUtils } = registry;
            apSchema = schemaUtils.retrieveSchema({ $ref: apSchema[REF_KEY] }, formData);
            type = apSchema.type;
            constValue = apSchema.const;
            defaultValue = apSchema.default;
          }
          if (!type && (ANY_OF_KEY in apSchema || ONE_OF_KEY in apSchema)) {
            type = "object";
          }
        }
        const newValue = constValue ?? defaultValue ?? this.getDefaultValue(type);
        set_default(newFormData, newKey, newValue);
      }
      onChange(newFormData);
    });
  }
  /** Returns a flag indicating whether the `name` field is required in the object schema
   *
   * @param name - The name of the field to check for required-ness
   * @returns - True if the field `name` is required, false otherwise
   */
  isRequired(name) {
    const { schema } = this.props;
    return Array.isArray(schema.required) && schema.required.indexOf(name) !== -1;
  }
  /** Returns a default value to be used for a new additional schema property of the given `type`
   *
   * @param type - The type of the new additional schema property
   */
  getDefaultValue(type) {
    const { registry: { translateString } } = this.props;
    switch (type) {
      case "array":
        return [];
      case "boolean":
        return false;
      case "null":
        return null;
      case "number":
        return 0;
      case "object":
        return {};
      case "string":
      default:
        return translateString(TranslatableString.NewStringDefault);
    }
  }
  /** Renders the `ObjectField` from the given props
   */
  render() {
    const { schema: rawSchema, uiSchema = {}, formData, errorSchema, idSchema, name, required = false, disabled, readonly, hideError, idPrefix, idSeparator, onBlur, onFocus, registry, title } = this.props;
    const { fields: fields2, formContext, schemaUtils, translateString, globalUiOptions } = registry;
    const { SchemaField: SchemaField2 } = fields2;
    const schema = schemaUtils.retrieveSchema(rawSchema, formData);
    const uiOptions = getUiOptions(uiSchema, globalUiOptions);
    const { properties: schemaProperties = {} } = schema;
    const templateTitle = uiOptions.title ?? schema.title ?? title ?? name;
    const description = uiOptions.description ?? schema.description;
    let orderedProperties;
    try {
      const properties = Object.keys(schemaProperties);
      orderedProperties = orderProperties(properties, uiOptions.order);
    } catch (err) {
      return (0, import_jsx_runtime8.jsxs)("div", { children: [(0, import_jsx_runtime8.jsx)("p", { className: "rjsf-config-error", style: { color: "red" }, children: (0, import_jsx_runtime8.jsx)(index_modern_default, { options: { disableParsingRawHTML: true }, children: translateString(TranslatableString.InvalidObjectField, [name || "root", err.message]) }) }), (0, import_jsx_runtime8.jsx)("pre", { children: JSON.stringify(schema) })] });
    }
    const Template = getTemplate("ObjectFieldTemplate", registry, uiOptions);
    const templateProps = {
      // getDisplayLabel() always returns false for object types, so just check the `uiOptions.label`
      title: uiOptions.label === false ? "" : templateTitle,
      description: uiOptions.label === false ? void 0 : description,
      properties: orderedProperties.map((name2) => {
        const addedByAdditionalProperties = has_default(schema, [PROPERTIES_KEY, name2, ADDITIONAL_PROPERTY_FLAG]);
        const fieldUiSchema = addedByAdditionalProperties ? uiSchema.additionalProperties : uiSchema[name2];
        const hidden = getUiOptions(fieldUiSchema).widget === "hidden";
        const fieldIdSchema = get_default(idSchema, [name2], {});
        return {
          content: (0, import_jsx_runtime8.jsx)(SchemaField2, { name: name2, required: this.isRequired(name2), schema: get_default(schema, [PROPERTIES_KEY, name2], {}), uiSchema: fieldUiSchema, errorSchema: get_default(errorSchema, name2), idSchema: fieldIdSchema, idPrefix, idSeparator, formData: get_default(formData, name2), formContext, wasPropertyKeyModified: this.state.wasPropertyKeyModified, onKeyChange: this.onKeyChange(name2), onChange: this.onPropertyChange(name2, addedByAdditionalProperties), onBlur, onFocus, registry, disabled, readonly, hideError, onDropPropertyClick: this.onDropPropertyClick }, name2),
          name: name2,
          readonly,
          disabled,
          required,
          hidden
        };
      }),
      readonly,
      disabled,
      required,
      idSchema,
      uiSchema,
      errorSchema,
      schema,
      formData,
      formContext,
      registry
    };
    return (0, import_jsx_runtime8.jsx)(Template, { ...templateProps, onAddClick: this.handleAddClick });
  }
};
var ObjectField_default = ObjectField;

// node_modules/@rjsf/core/lib/components/fields/SchemaField.js
var import_jsx_runtime9 = __toESM(require_jsx_runtime(), 1);
var import_react8 = __toESM(require_react(), 1);
var COMPONENT_TYPES = {
  array: "ArrayField",
  boolean: "BooleanField",
  integer: "NumberField",
  number: "NumberField",
  object: "ObjectField",
  string: "StringField",
  null: "NullField"
};
function getFieldComponent(schema, uiOptions, idSchema, registry) {
  const field = uiOptions.field;
  const { fields: fields2, translateString } = registry;
  if (typeof field === "function") {
    return field;
  }
  if (typeof field === "string" && field in fields2) {
    return fields2[field];
  }
  const schemaType = getSchemaType(schema);
  const type = Array.isArray(schemaType) ? schemaType[0] : schemaType || "";
  const schemaId = schema.$id;
  let componentName = COMPONENT_TYPES[type];
  if (schemaId && schemaId in fields2) {
    componentName = schemaId;
  }
  if (!componentName && (schema.anyOf || schema.oneOf)) {
    return () => null;
  }
  return componentName in fields2 ? fields2[componentName] : () => {
    const UnsupportedFieldTemplate = getTemplate("UnsupportedFieldTemplate", registry, uiOptions);
    return (0, import_jsx_runtime9.jsx)(UnsupportedFieldTemplate, { schema, idSchema, reason: translateString(TranslatableString.UnknownFieldType, [String(schema.type)]), registry });
  };
}
function SchemaFieldRender(props) {
  const { schema: _schema, idSchema: _idSchema, uiSchema, formData, errorSchema, idPrefix, idSeparator, name, onChange, onKeyChange, onDropPropertyClick, required, registry, wasPropertyKeyModified = false } = props;
  const { formContext, schemaUtils, globalUiOptions } = registry;
  const uiOptions = getUiOptions(uiSchema, globalUiOptions);
  const FieldTemplate2 = getTemplate("FieldTemplate", registry, uiOptions);
  const DescriptionFieldTemplate = getTemplate("DescriptionFieldTemplate", registry, uiOptions);
  const FieldHelpTemplate2 = getTemplate("FieldHelpTemplate", registry, uiOptions);
  const FieldErrorTemplate2 = getTemplate("FieldErrorTemplate", registry, uiOptions);
  const schema = schemaUtils.retrieveSchema(_schema, formData);
  const fieldId = _idSchema[ID_KEY];
  const idSchema = mergeObjects(schemaUtils.toIdSchema(schema, fieldId, formData, idPrefix, idSeparator), _idSchema);
  const handleFieldComponentChange = (0, import_react8.useCallback)((formData2, newErrorSchema, id2) => {
    const theId = id2 || fieldId;
    return onChange(formData2, newErrorSchema, theId);
  }, [fieldId, onChange]);
  const FieldComponent = getFieldComponent(schema, uiOptions, idSchema, registry);
  const disabled = Boolean(uiOptions.disabled ?? props.disabled);
  const readonly = Boolean(uiOptions.readonly ?? (props.readonly || props.schema.readOnly || schema.readOnly));
  const uiSchemaHideError = uiOptions.hideError;
  const hideError = uiSchemaHideError === void 0 ? props.hideError : Boolean(uiSchemaHideError);
  const autofocus = Boolean(uiOptions.autofocus ?? props.autofocus);
  if (Object.keys(schema).length === 0) {
    return null;
  }
  const displayLabel = schemaUtils.getDisplayLabel(schema, uiSchema, globalUiOptions);
  const { __errors, ...fieldErrorSchema } = errorSchema || {};
  const fieldUiSchema = omit_default(uiSchema, ["ui:classNames", "classNames", "ui:style"]);
  if (UI_OPTIONS_KEY in fieldUiSchema) {
    fieldUiSchema[UI_OPTIONS_KEY] = omit_default(fieldUiSchema[UI_OPTIONS_KEY], ["classNames", "style"]);
  }
  const field = (0, import_jsx_runtime9.jsx)(FieldComponent, { ...props, onChange: handleFieldComponentChange, idSchema, schema, uiSchema: fieldUiSchema, disabled, readonly, hideError, autofocus, errorSchema: fieldErrorSchema, formContext, rawErrors: __errors });
  const id = idSchema[ID_KEY];
  let label;
  if (wasPropertyKeyModified) {
    label = name;
  } else {
    label = ADDITIONAL_PROPERTY_FLAG in schema ? name : uiOptions.title || props.schema.title || schema.title || props.title || name;
  }
  const description = uiOptions.description || props.schema.description || schema.description || "";
  const help = uiOptions.help;
  const hidden = uiOptions.widget === "hidden";
  const classNames = ["rjsf-field", `rjsf-field-${getSchemaType(schema)}`];
  if (!hideError && __errors && __errors.length > 0) {
    classNames.push("rjsf-field-error");
  }
  if (uiOptions.classNames) {
    classNames.push(uiOptions.classNames);
  }
  const helpComponent = (0, import_jsx_runtime9.jsx)(FieldHelpTemplate2, { help, idSchema, schema, uiSchema, hasErrors: !hideError && __errors && __errors.length > 0, registry });
  const errorsComponent = hideError || (schema.anyOf || schema.oneOf) && !schemaUtils.isSelect(schema) ? void 0 : (0, import_jsx_runtime9.jsx)(FieldErrorTemplate2, { errors: __errors, errorSchema, idSchema, schema, uiSchema, registry });
  const fieldProps = {
    description: (0, import_jsx_runtime9.jsx)(DescriptionFieldTemplate, { id: descriptionId(id), description, schema, uiSchema, registry }),
    rawDescription: description,
    help: helpComponent,
    rawHelp: typeof help === "string" ? help : void 0,
    errors: errorsComponent,
    rawErrors: hideError ? void 0 : __errors,
    id,
    label,
    hidden,
    onChange,
    onKeyChange,
    onDropPropertyClick,
    required,
    disabled,
    readonly,
    hideError,
    displayLabel,
    classNames: classNames.join(" ").trim(),
    style: uiOptions.style,
    formContext,
    formData,
    schema,
    uiSchema,
    registry
  };
  const _AnyOfField = registry.fields.AnyOfField;
  const _OneOfField = registry.fields.OneOfField;
  const isReplacingAnyOrOneOf = (uiSchema == null ? void 0 : uiSchema["ui:field"]) && (uiSchema == null ? void 0 : uiSchema["ui:fieldReplacesAnyOrOneOf"]) === true;
  return (0, import_jsx_runtime9.jsx)(FieldTemplate2, { ...fieldProps, children: (0, import_jsx_runtime9.jsxs)(import_jsx_runtime9.Fragment, { children: [field, schema.anyOf && !isReplacingAnyOrOneOf && !schemaUtils.isSelect(schema) && (0, import_jsx_runtime9.jsx)(_AnyOfField, { name, disabled, readonly, hideError, errorSchema, formData, formContext, idPrefix, idSchema, idSeparator, onBlur: props.onBlur, onChange: props.onChange, onFocus: props.onFocus, options: schema.anyOf.map((_schema2) => schemaUtils.retrieveSchema(isObject_default(_schema2) ? _schema2 : {}, formData)), registry, required, schema, uiSchema }), schema.oneOf && !isReplacingAnyOrOneOf && !schemaUtils.isSelect(schema) && (0, import_jsx_runtime9.jsx)(_OneOfField, { name, disabled, readonly, hideError, errorSchema, formData, formContext, idPrefix, idSchema, idSeparator, onBlur: props.onBlur, onChange: props.onChange, onFocus: props.onFocus, options: schema.oneOf.map((_schema2) => schemaUtils.retrieveSchema(isObject_default(_schema2) ? _schema2 : {}, formData)), registry, required, schema, uiSchema })] }) });
}
var SchemaField = class extends import_react8.Component {
  shouldComponentUpdate(nextProps) {
    return !deepEquals(this.props, nextProps);
  }
  render() {
    return (0, import_jsx_runtime9.jsx)(SchemaFieldRender, { ...this.props });
  }
};
var SchemaField_default = SchemaField;

// node_modules/@rjsf/core/lib/components/fields/StringField.js
var import_jsx_runtime10 = __toESM(require_jsx_runtime(), 1);
function StringField(props) {
  const { schema, name, uiSchema, idSchema, formData, required, disabled = false, readonly = false, autofocus = false, onChange, onBlur, onFocus, registry, rawErrors, hideError } = props;
  const { title, format } = schema;
  const { widgets: widgets2, formContext, schemaUtils, globalUiOptions } = registry;
  const enumOptions = schemaUtils.isSelect(schema) ? optionsList(schema, uiSchema) : void 0;
  let defaultWidget = enumOptions ? "select" : "text";
  if (format && hasWidget(schema, format, widgets2)) {
    defaultWidget = format;
  }
  const { widget = defaultWidget, placeholder = "", title: uiTitle, ...options } = getUiOptions(uiSchema);
  const displayLabel = schemaUtils.getDisplayLabel(schema, uiSchema, globalUiOptions);
  const label = uiTitle ?? title ?? name;
  const Widget = getWidget(schema, widget, widgets2);
  return (0, import_jsx_runtime10.jsx)(Widget, { options: { ...options, enumOptions }, schema, uiSchema, id: idSchema.$id, name, label, hideLabel: !displayLabel, hideError, value: formData, onChange, onBlur, onFocus, required, disabled, readonly, formContext, autofocus, registry, placeholder, rawErrors });
}
var StringField_default = StringField;

// node_modules/@rjsf/core/lib/components/fields/NullField.js
var import_react9 = __toESM(require_react(), 1);
function NullField(props) {
  const { formData, onChange } = props;
  (0, import_react9.useEffect)(() => {
    if (formData === void 0) {
      onChange(null);
    }
  }, [formData, onChange]);
  return null;
}
var NullField_default = NullField;

// node_modules/@rjsf/core/lib/components/fields/index.js
function fields() {
  return {
    AnyOfField: MultiSchemaField_default,
    ArrayField: ArrayField_default,
    // ArrayField falls back to SchemaField if ArraySchemaField is not defined, which it isn't by default
    BooleanField: BooleanField_default,
    LayoutGridField,
    LayoutHeaderField,
    LayoutMultiSchemaField,
    NumberField: NumberField_default,
    ObjectField: ObjectField_default,
    OneOfField: MultiSchemaField_default,
    SchemaField: SchemaField_default,
    StringField: StringField_default,
    NullField: NullField_default
  };
}
var fields_default = fields;

// node_modules/@rjsf/core/lib/components/templates/ArrayFieldDescriptionTemplate.js
var import_jsx_runtime11 = __toESM(require_jsx_runtime(), 1);
function ArrayFieldDescriptionTemplate(props) {
  const { idSchema, description, registry, schema, uiSchema } = props;
  const options = getUiOptions(uiSchema, registry.globalUiOptions);
  const { label: displayLabel = true } = options;
  if (!description || !displayLabel) {
    return null;
  }
  const DescriptionFieldTemplate = getTemplate("DescriptionFieldTemplate", registry, options);
  return (0, import_jsx_runtime11.jsx)(DescriptionFieldTemplate, { id: descriptionId(idSchema), description, schema, uiSchema, registry });
}

// node_modules/@rjsf/core/lib/components/templates/ArrayFieldItemTemplate.js
var import_jsx_runtime12 = __toESM(require_jsx_runtime(), 1);
function ArrayFieldItemTemplate(props) {
  const { children, className, buttonsProps, hasToolbar, registry, uiSchema } = props;
  const uiOptions = getUiOptions(uiSchema);
  const ArrayFieldItemButtonsTemplate2 = getTemplate("ArrayFieldItemButtonsTemplate", registry, uiOptions);
  const btnStyle = {
    flex: 1,
    paddingLeft: 6,
    paddingRight: 6,
    fontWeight: "bold"
  };
  return (0, import_jsx_runtime12.jsxs)("div", { className, children: [(0, import_jsx_runtime12.jsx)("div", { className: hasToolbar ? "col-xs-9" : "col-xs-12", children }), hasToolbar && (0, import_jsx_runtime12.jsx)("div", { className: "col-xs-3 array-item-toolbox", children: (0, import_jsx_runtime12.jsx)("div", { className: "btn-group", style: {
    display: "flex",
    justifyContent: "space-around"
  }, children: (0, import_jsx_runtime12.jsx)(ArrayFieldItemButtonsTemplate2, { ...buttonsProps, style: btnStyle }) }) })] });
}

// node_modules/@rjsf/core/lib/components/templates/ArrayFieldItemButtonsTemplate.js
var import_jsx_runtime13 = __toESM(require_jsx_runtime(), 1);
var import_react10 = __toESM(require_react(), 1);
function ArrayFieldItemButtonsTemplate(props) {
  const { disabled, hasCopy, hasMoveDown, hasMoveUp, hasRemove, idSchema, index, onCopyIndexClick, onDropIndexClick, onReorderClick, readonly, registry, uiSchema } = props;
  const { CopyButton: CopyButton2, MoveDownButton: MoveDownButton2, MoveUpButton: MoveUpButton2, RemoveButton: RemoveButton2 } = registry.templates.ButtonTemplates;
  const onCopyClick = (0, import_react10.useMemo)(() => onCopyIndexClick(index), [index, onCopyIndexClick]);
  const onRemoveClick = (0, import_react10.useMemo)(() => onDropIndexClick(index), [index, onDropIndexClick]);
  const onArrowUpClick = (0, import_react10.useMemo)(() => onReorderClick(index, index - 1), [index, onReorderClick]);
  const onArrowDownClick = (0, import_react10.useMemo)(() => onReorderClick(index, index + 1), [index, onReorderClick]);
  return (0, import_jsx_runtime13.jsxs)(import_jsx_runtime13.Fragment, { children: [(hasMoveUp || hasMoveDown) && (0, import_jsx_runtime13.jsx)(MoveUpButton2, { id: buttonId(idSchema, "moveUp"), className: "rjsf-array-item-move-up", disabled: disabled || readonly || !hasMoveUp, onClick: onArrowUpClick, uiSchema, registry }), (hasMoveUp || hasMoveDown) && (0, import_jsx_runtime13.jsx)(MoveDownButton2, { id: buttonId(idSchema, "moveDown"), className: "rjsf-array-item-move-down", disabled: disabled || readonly || !hasMoveDown, onClick: onArrowDownClick, uiSchema, registry }), hasCopy && (0, import_jsx_runtime13.jsx)(CopyButton2, { id: buttonId(idSchema, "copy"), className: "rjsf-array-item-copy", disabled: disabled || readonly, onClick: onCopyClick, uiSchema, registry }), hasRemove && (0, import_jsx_runtime13.jsx)(RemoveButton2, { id: buttonId(idSchema, "remove"), className: "rjsf-array-item-remove", disabled: disabled || readonly, onClick: onRemoveClick, uiSchema, registry })] });
}

// node_modules/@rjsf/core/lib/components/templates/ArrayFieldTemplate.js
var import_jsx_runtime14 = __toESM(require_jsx_runtime(), 1);
function ArrayFieldTemplate(props) {
  const { canAdd, className, disabled, idSchema, uiSchema, items, onAddClick, readonly, registry, required, schema, title } = props;
  const uiOptions = getUiOptions(uiSchema);
  const ArrayFieldDescriptionTemplate2 = getTemplate("ArrayFieldDescriptionTemplate", registry, uiOptions);
  const ArrayFieldItemTemplate2 = getTemplate("ArrayFieldItemTemplate", registry, uiOptions);
  const ArrayFieldTitleTemplate2 = getTemplate("ArrayFieldTitleTemplate", registry, uiOptions);
  const { ButtonTemplates: { AddButton: AddButton2 } } = registry.templates;
  return (0, import_jsx_runtime14.jsxs)("fieldset", { className, id: idSchema.$id, children: [(0, import_jsx_runtime14.jsx)(ArrayFieldTitleTemplate2, { idSchema, title: uiOptions.title || title, required, schema, uiSchema, registry }), (0, import_jsx_runtime14.jsx)(ArrayFieldDescriptionTemplate2, { idSchema, description: uiOptions.description || schema.description, schema, uiSchema, registry }), (0, import_jsx_runtime14.jsx)("div", { className: "row array-item-list", children: items && items.map(({ key, ...itemProps }) => (0, import_jsx_runtime14.jsx)(ArrayFieldItemTemplate2, { ...itemProps }, key)) }), canAdd && (0, import_jsx_runtime14.jsx)(AddButton2, { id: buttonId(idSchema, "add"), className: "rjsf-array-item-add", onClick: onAddClick, disabled: disabled || readonly, uiSchema, registry })] });
}

// node_modules/@rjsf/core/lib/components/templates/ArrayFieldTitleTemplate.js
var import_jsx_runtime15 = __toESM(require_jsx_runtime(), 1);
function ArrayFieldTitleTemplate(props) {
  const { idSchema, title, schema, uiSchema, required, registry } = props;
  const options = getUiOptions(uiSchema, registry.globalUiOptions);
  const { label: displayLabel = true } = options;
  if (!title || !displayLabel) {
    return null;
  }
  const TitleFieldTemplate = getTemplate("TitleFieldTemplate", registry, options);
  return (0, import_jsx_runtime15.jsx)(TitleFieldTemplate, { id: titleId(idSchema), title, required, schema, uiSchema, registry });
}

// node_modules/@rjsf/core/lib/components/templates/BaseInputTemplate.js
var import_jsx_runtime16 = __toESM(require_jsx_runtime(), 1);
var import_react11 = __toESM(require_react(), 1);
function BaseInputTemplate(props) {
  const {
    id,
    name,
    // remove this from ...rest
    value,
    readonly,
    disabled,
    autofocus,
    onBlur,
    onFocus,
    onChange,
    onChangeOverride,
    options,
    schema,
    uiSchema,
    formContext,
    registry,
    rawErrors,
    type,
    hideLabel,
    // remove this from ...rest
    hideError,
    // remove this from ...rest
    ...rest
  } = props;
  if (!id) {
    console.log("No id for", props);
    throw new Error(`no id for props ${JSON.stringify(props)}`);
  }
  const inputProps = {
    ...rest,
    ...getInputProps(schema, type, options)
  };
  let inputValue;
  if (inputProps.type === "number" || inputProps.type === "integer") {
    inputValue = value || value === 0 ? value : "";
  } else {
    inputValue = value == null ? "" : value;
  }
  const _onChange = (0, import_react11.useCallback)(({ target: { value: value2 } }) => onChange(value2 === "" ? options.emptyValue : value2), [onChange, options]);
  const _onBlur = (0, import_react11.useCallback)(({ target }) => onBlur(id, target && target.value), [onBlur, id]);
  const _onFocus = (0, import_react11.useCallback)(({ target }) => onFocus(id, target && target.value), [onFocus, id]);
  return (0, import_jsx_runtime16.jsxs)(import_jsx_runtime16.Fragment, { children: [(0, import_jsx_runtime16.jsx)("input", { id, name: id, className: "form-control", readOnly: readonly, disabled, autoFocus: autofocus, value: inputValue, ...inputProps, list: schema.examples ? examplesId(id) : void 0, onChange: onChangeOverride || _onChange, onBlur: _onBlur, onFocus: _onFocus, "aria-describedby": ariaDescribedByIds(id, !!schema.examples) }), Array.isArray(schema.examples) && (0, import_jsx_runtime16.jsx)("datalist", { id: examplesId(id), children: schema.examples.concat(schema.default && !schema.examples.includes(schema.default) ? [schema.default] : []).map((example) => {
    return (0, import_jsx_runtime16.jsx)("option", { value: example }, example);
  }) }, `datalist_${id}`)] });
}

// node_modules/@rjsf/core/lib/components/templates/ButtonTemplates/SubmitButton.js
var import_jsx_runtime17 = __toESM(require_jsx_runtime(), 1);
function SubmitButton({ uiSchema }) {
  const { submitText, norender, props: submitButtonProps = {} } = getSubmitButtonOptions(uiSchema);
  if (norender) {
    return null;
  }
  return (0, import_jsx_runtime17.jsx)("div", { children: (0, import_jsx_runtime17.jsx)("button", { type: "submit", ...submitButtonProps, className: `btn btn-info ${submitButtonProps.className || ""}`, children: submitText }) });
}

// node_modules/@rjsf/core/lib/components/templates/ButtonTemplates/AddButton.js
var import_jsx_runtime19 = __toESM(require_jsx_runtime(), 1);

// node_modules/@rjsf/core/lib/components/templates/ButtonTemplates/IconButton.js
var import_jsx_runtime18 = __toESM(require_jsx_runtime(), 1);
function IconButton(props) {
  const { iconType = "default", icon, className, uiSchema, registry, ...otherProps } = props;
  return (0, import_jsx_runtime18.jsx)("button", { type: "button", className: `btn btn-${iconType} ${className}`, ...otherProps, children: (0, import_jsx_runtime18.jsx)("i", { className: `glyphicon glyphicon-${icon}` }) });
}
function CopyButton(props) {
  const { registry: { translateString } } = props;
  return (0, import_jsx_runtime18.jsx)(IconButton, { title: translateString(TranslatableString.CopyButton), ...props, icon: "copy" });
}
function MoveDownButton(props) {
  const { registry: { translateString } } = props;
  return (0, import_jsx_runtime18.jsx)(IconButton, { title: translateString(TranslatableString.MoveDownButton), ...props, icon: "arrow-down" });
}
function MoveUpButton(props) {
  const { registry: { translateString } } = props;
  return (0, import_jsx_runtime18.jsx)(IconButton, { title: translateString(TranslatableString.MoveUpButton), ...props, icon: "arrow-up" });
}
function RemoveButton(props) {
  const { registry: { translateString } } = props;
  return (0, import_jsx_runtime18.jsx)(IconButton, { title: translateString(TranslatableString.RemoveButton), ...props, iconType: "danger", icon: "remove" });
}

// node_modules/@rjsf/core/lib/components/templates/ButtonTemplates/AddButton.js
function AddButton({ className, onClick, disabled, registry }) {
  const { translateString } = registry;
  return (0, import_jsx_runtime19.jsx)("div", { className: "row", children: (0, import_jsx_runtime19.jsx)("p", { className: `col-xs-3 col-xs-offset-9 text-right ${className}`, children: (0, import_jsx_runtime19.jsx)(IconButton, { iconType: "info", icon: "plus", className: "btn-add col-xs-12", title: translateString(TranslatableString.AddButton), onClick, disabled, registry }) }) });
}

// node_modules/@rjsf/core/lib/components/templates/ButtonTemplates/index.js
function buttonTemplates() {
  return {
    SubmitButton,
    AddButton,
    CopyButton,
    MoveDownButton,
    MoveUpButton,
    RemoveButton
  };
}
var ButtonTemplates_default = buttonTemplates;

// node_modules/@rjsf/core/lib/components/templates/DescriptionField.js
var import_jsx_runtime21 = __toESM(require_jsx_runtime(), 1);

// node_modules/@rjsf/core/lib/components/RichDescription.js
var import_jsx_runtime20 = __toESM(require_jsx_runtime(), 1);
var TEST_IDS = getTestIds();
function RichDescription({ description, registry, uiSchema = {} }) {
  const { globalUiOptions } = registry;
  const uiOptions = getUiOptions(uiSchema, globalUiOptions);
  if (uiOptions.enableMarkdownInDescription && typeof description === "string") {
    return (0, import_jsx_runtime20.jsx)(index_modern_default, { options: { disableParsingRawHTML: true }, "data-testid": TEST_IDS.markdown, children: description });
  }
  return description;
}
RichDescription.TEST_IDS = TEST_IDS;

// node_modules/@rjsf/core/lib/components/templates/DescriptionField.js
function DescriptionField(props) {
  const { id, description, registry, uiSchema } = props;
  if (!description) {
    return null;
  }
  return (0, import_jsx_runtime21.jsx)("div", { id, className: "field-description", children: (0, import_jsx_runtime21.jsx)(RichDescription, { description, registry, uiSchema }) });
}

// node_modules/@rjsf/core/lib/components/templates/ErrorList.js
var import_jsx_runtime22 = __toESM(require_jsx_runtime(), 1);
function ErrorList({ errors, registry }) {
  const { translateString } = registry;
  return (0, import_jsx_runtime22.jsxs)("div", { className: "panel panel-danger errors", children: [(0, import_jsx_runtime22.jsx)("div", { className: "panel-heading", children: (0, import_jsx_runtime22.jsx)("h3", { className: "panel-title", children: translateString(TranslatableString.ErrorsLabel) }) }), (0, import_jsx_runtime22.jsx)("ul", { className: "list-group", children: errors.map((error, i2) => {
    return (0, import_jsx_runtime22.jsx)("li", { className: "list-group-item text-danger", children: error.stack }, i2);
  }) })] });
}

// node_modules/@rjsf/core/lib/components/templates/FieldTemplate/FieldTemplate.js
var import_jsx_runtime24 = __toESM(require_jsx_runtime(), 1);

// node_modules/@rjsf/core/lib/components/templates/FieldTemplate/Label.js
var import_jsx_runtime23 = __toESM(require_jsx_runtime(), 1);
var REQUIRED_FIELD_SYMBOL = "*";
function Label(props) {
  const { label, required, id } = props;
  if (!label) {
    return null;
  }
  return (0, import_jsx_runtime23.jsxs)("label", { className: "control-label", htmlFor: id, children: [label, required && (0, import_jsx_runtime23.jsx)("span", { className: "required", children: REQUIRED_FIELD_SYMBOL })] });
}

// node_modules/@rjsf/core/lib/components/templates/FieldTemplate/FieldTemplate.js
function FieldTemplate(props) {
  const { id, label, children, errors, help, description, hidden, required, displayLabel, registry, uiSchema } = props;
  const uiOptions = getUiOptions(uiSchema);
  const WrapIfAdditionalTemplate2 = getTemplate("WrapIfAdditionalTemplate", registry, uiOptions);
  if (hidden) {
    return (0, import_jsx_runtime24.jsx)("div", { className: "hidden", children });
  }
  return (0, import_jsx_runtime24.jsxs)(WrapIfAdditionalTemplate2, { ...props, children: [displayLabel && (0, import_jsx_runtime24.jsx)(Label, { label, required, id }), displayLabel && description ? description : null, children, errors, help] });
}

// node_modules/@rjsf/core/lib/components/templates/FieldTemplate/index.js
var FieldTemplate_default = FieldTemplate;

// node_modules/@rjsf/core/lib/components/templates/FieldErrorTemplate.js
var import_jsx_runtime25 = __toESM(require_jsx_runtime(), 1);
function FieldErrorTemplate(props) {
  const { errors = [], idSchema } = props;
  if (errors.length === 0) {
    return null;
  }
  const id = errorId(idSchema);
  return (0, import_jsx_runtime25.jsx)("div", { children: (0, import_jsx_runtime25.jsx)("ul", { id, className: "error-detail bs-callout bs-callout-info", children: errors.filter((elem) => !!elem).map((error, index) => {
    return (0, import_jsx_runtime25.jsx)("li", { className: "text-danger", children: error }, index);
  }) }) });
}

// node_modules/@rjsf/core/lib/components/templates/FieldHelpTemplate.js
var import_jsx_runtime26 = __toESM(require_jsx_runtime(), 1);
function FieldHelpTemplate(props) {
  const { idSchema, help } = props;
  if (!help) {
    return null;
  }
  const id = helpId(idSchema);
  if (typeof help === "string") {
    return (0, import_jsx_runtime26.jsx)("p", { id, className: "help-block", children: help });
  }
  return (0, import_jsx_runtime26.jsx)("div", { id, className: "help-block", children: help });
}

// node_modules/@rjsf/core/lib/components/templates/GridTemplate.js
var import_jsx_runtime27 = __toESM(require_jsx_runtime(), 1);
function GridTemplate(props) {
  const { children, column, className, ...rest } = props;
  return (0, import_jsx_runtime27.jsx)("div", { className, ...rest, children });
}

// node_modules/@rjsf/core/lib/components/templates/MultiSchemaFieldTemplate.js
var import_jsx_runtime28 = __toESM(require_jsx_runtime(), 1);
function MultiSchemaFieldTemplate(props) {
  const { selector, optionSchemaField } = props;
  return (0, import_jsx_runtime28.jsxs)("div", { className: "panel panel-default panel-body", children: [(0, import_jsx_runtime28.jsx)("div", { className: "form-group", children: selector }), optionSchemaField] });
}

// node_modules/@rjsf/core/lib/components/templates/ObjectFieldTemplate.js
var import_jsx_runtime29 = __toESM(require_jsx_runtime(), 1);
function ObjectFieldTemplate(props) {
  const { description, disabled, formData, idSchema, onAddClick, properties, readonly, registry, required, schema, title, uiSchema } = props;
  const options = getUiOptions(uiSchema);
  const TitleFieldTemplate = getTemplate("TitleFieldTemplate", registry, options);
  const DescriptionFieldTemplate = getTemplate("DescriptionFieldTemplate", registry, options);
  const { ButtonTemplates: { AddButton: AddButton2 } } = registry.templates;
  return (0, import_jsx_runtime29.jsxs)("fieldset", { id: idSchema.$id, children: [title && (0, import_jsx_runtime29.jsx)(TitleFieldTemplate, { id: titleId(idSchema), title, required, schema, uiSchema, registry }), description && (0, import_jsx_runtime29.jsx)(DescriptionFieldTemplate, { id: descriptionId(idSchema), description, schema, uiSchema, registry }), properties.map((prop) => prop.content), canExpand(schema, uiSchema, formData) && (0, import_jsx_runtime29.jsx)(AddButton2, { id: buttonId(idSchema, "add"), className: "rjsf-object-property-expand", onClick: onAddClick(schema), disabled: disabled || readonly, uiSchema, registry })] });
}

// node_modules/@rjsf/core/lib/components/templates/TitleField.js
var import_jsx_runtime30 = __toESM(require_jsx_runtime(), 1);
var REQUIRED_FIELD_SYMBOL2 = "*";
function TitleField(props) {
  const { id, title, required } = props;
  return (0, import_jsx_runtime30.jsxs)("legend", { id, children: [title, required && (0, import_jsx_runtime30.jsx)("span", { className: "required", children: REQUIRED_FIELD_SYMBOL2 })] });
}

// node_modules/@rjsf/core/lib/components/templates/UnsupportedField.js
var import_jsx_runtime31 = __toESM(require_jsx_runtime(), 1);
function UnsupportedField(props) {
  const { schema, idSchema, reason, registry } = props;
  const { translateString } = registry;
  let translateEnum = TranslatableString.UnsupportedField;
  const translateParams = [];
  if (idSchema && idSchema.$id) {
    translateEnum = TranslatableString.UnsupportedFieldWithId;
    translateParams.push(idSchema.$id);
  }
  if (reason) {
    translateEnum = translateEnum === TranslatableString.UnsupportedField ? TranslatableString.UnsupportedFieldWithReason : TranslatableString.UnsupportedFieldWithIdAndReason;
    translateParams.push(reason);
  }
  return (0, import_jsx_runtime31.jsxs)("div", { className: "unsupported-field", children: [(0, import_jsx_runtime31.jsx)("p", { children: (0, import_jsx_runtime31.jsx)(index_modern_default, { options: { disableParsingRawHTML: true }, children: translateString(translateEnum, translateParams) }) }), schema && (0, import_jsx_runtime31.jsx)("pre", { children: JSON.stringify(schema, null, 2) })] });
}
var UnsupportedField_default = UnsupportedField;

// node_modules/@rjsf/core/lib/components/templates/WrapIfAdditionalTemplate.js
var import_jsx_runtime32 = __toESM(require_jsx_runtime(), 1);
function WrapIfAdditionalTemplate(props) {
  const { id, classNames, style, disabled, label, onKeyChange, onDropPropertyClick, readonly, required, schema, hideError, rawErrors, children, uiSchema, registry } = props;
  const { templates: templates2, translateString } = registry;
  const { RemoveButton: RemoveButton2 } = templates2.ButtonTemplates;
  const keyLabel = translateString(TranslatableString.KeyLabel, [label]);
  const additional = ADDITIONAL_PROPERTY_FLAG in schema;
  const classNamesList = ["form-group", classNames];
  if (!hideError && rawErrors && rawErrors.length > 0) {
    classNamesList.push("has-error has-danger");
  }
  const uiClassNames = classNamesList.join(" ").trim();
  if (!additional) {
    return (0, import_jsx_runtime32.jsx)("div", { className: uiClassNames, style, children });
  }
  return (0, import_jsx_runtime32.jsx)("div", { className: uiClassNames, style, children: (0, import_jsx_runtime32.jsxs)("div", { className: "row", children: [(0, import_jsx_runtime32.jsx)("div", { className: "col-xs-5 form-additional", children: (0, import_jsx_runtime32.jsxs)("div", { className: "form-group", children: [(0, import_jsx_runtime32.jsx)(Label, { label: keyLabel, required, id: `${id}-key` }), (0, import_jsx_runtime32.jsx)("input", { className: "form-control", type: "text", id: `${id}-key`, onBlur: ({ target }) => onKeyChange(target && target.value), defaultValue: label })] }) }), (0, import_jsx_runtime32.jsx)("div", { className: "form-additional form-group col-xs-5", children }), (0, import_jsx_runtime32.jsx)("div", { className: "col-xs-2", children: (0, import_jsx_runtime32.jsx)(RemoveButton2, { id: buttonId(id, "remove"), className: "rjsf-object-property-remove btn-block", style: { border: "0" }, disabled: disabled || readonly, onClick: onDropPropertyClick(label), uiSchema, registry }) })] }) });
}

// node_modules/@rjsf/core/lib/components/templates/index.js
function templates() {
  return {
    ArrayFieldDescriptionTemplate,
    ArrayFieldItemTemplate,
    ArrayFieldItemButtonsTemplate,
    ArrayFieldTemplate,
    ArrayFieldTitleTemplate,
    ButtonTemplates: ButtonTemplates_default(),
    BaseInputTemplate,
    DescriptionFieldTemplate: DescriptionField,
    ErrorListTemplate: ErrorList,
    FieldTemplate: FieldTemplate_default,
    FieldErrorTemplate,
    FieldHelpTemplate,
    GridTemplate,
    MultiSchemaFieldTemplate,
    ObjectFieldTemplate,
    TitleFieldTemplate: TitleField,
    UnsupportedFieldTemplate: UnsupportedField_default,
    WrapIfAdditionalTemplate
  };
}
var templates_default = templates;

// node_modules/@rjsf/core/lib/components/widgets/AltDateWidget.js
var import_jsx_runtime33 = __toESM(require_jsx_runtime(), 1);
var import_react12 = __toESM(require_react(), 1);
function readyForChange(state) {
  return Object.values(state).every((value) => value !== -1);
}
function DateElement({ type, range, value, select, rootId, name, disabled, readonly, autofocus, registry, onBlur, onFocus }) {
  const id = rootId + "_" + type;
  const { SelectWidget: SelectWidget2 } = registry.widgets;
  return (0, import_jsx_runtime33.jsx)(SelectWidget2, { schema: { type: "integer" }, id, name, className: "form-control", options: { enumOptions: dateRangeOptions(range[0], range[1]) }, placeholder: type, value, disabled, readonly, autofocus, onChange: (value2) => select(type, value2), onBlur, onFocus, registry, label: "", "aria-describedby": ariaDescribedByIds(rootId) });
}
function AltDateWidget({ time = false, disabled = false, readonly = false, autofocus = false, options, id, name, registry, onBlur, onFocus, onChange, value }) {
  const { translateString } = registry;
  const [lastValue, setLastValue] = (0, import_react12.useState)(value);
  const [state, setState] = (0, import_react12.useReducer)((state2, action) => {
    return { ...state2, ...action };
  }, parseDateString(value, time));
  (0, import_react12.useEffect)(() => {
    const stateValue = toDateString(state, time);
    if (readyForChange(state) && stateValue !== value) {
      onChange(stateValue);
    } else if (lastValue !== value) {
      setLastValue(value);
      setState(parseDateString(value, time));
    }
  }, [time, value, onChange, state, lastValue]);
  const handleChange = (0, import_react12.useCallback)((property, value2) => {
    setState({ [property]: value2 });
  }, []);
  const handleSetNow = (0, import_react12.useCallback)((event) => {
    event.preventDefault();
    if (disabled || readonly) {
      return;
    }
    const nextState = parseDateString((/* @__PURE__ */ new Date()).toJSON(), time);
    onChange(toDateString(nextState, time));
  }, [disabled, readonly, time]);
  const handleClear = (0, import_react12.useCallback)((event) => {
    event.preventDefault();
    if (disabled || readonly) {
      return;
    }
    onChange(void 0);
  }, [disabled, readonly, onChange]);
  return (0, import_jsx_runtime33.jsxs)("ul", { className: "list-inline", children: [getDateElementProps(state, time, options.yearsRange, options.format).map((elemProps, i2) => (0, import_jsx_runtime33.jsx)("li", { className: "list-inline-item", children: (0, import_jsx_runtime33.jsx)(DateElement, { rootId: id, name, select: handleChange, ...elemProps, disabled, readonly, registry, onBlur, onFocus, autofocus: autofocus && i2 === 0 }) }, i2)), (options.hideNowButton !== "undefined" ? !options.hideNowButton : true) && (0, import_jsx_runtime33.jsx)("li", { className: "list-inline-item", children: (0, import_jsx_runtime33.jsx)("a", { href: "#", className: "btn btn-info btn-now", onClick: handleSetNow, children: translateString(TranslatableString.NowLabel) }) }), (options.hideClearButton !== "undefined" ? !options.hideClearButton : true) && (0, import_jsx_runtime33.jsx)("li", { className: "list-inline-item", children: (0, import_jsx_runtime33.jsx)("a", { href: "#", className: "btn btn-warning btn-clear", onClick: handleClear, children: translateString(TranslatableString.ClearLabel) }) })] });
}
var AltDateWidget_default = AltDateWidget;

// node_modules/@rjsf/core/lib/components/widgets/AltDateTimeWidget.js
var import_jsx_runtime34 = __toESM(require_jsx_runtime(), 1);
function AltDateTimeWidget({ time = true, ...props }) {
  const { AltDateWidget: AltDateWidget2 } = props.registry.widgets;
  return (0, import_jsx_runtime34.jsx)(AltDateWidget2, { time, ...props });
}
var AltDateTimeWidget_default = AltDateTimeWidget;

// node_modules/@rjsf/core/lib/components/widgets/CheckboxWidget.js
var import_jsx_runtime35 = __toESM(require_jsx_runtime(), 1);
var import_react13 = __toESM(require_react(), 1);
function CheckboxWidget({ schema, uiSchema, options, id, value, disabled, readonly, label, hideLabel, autofocus = false, onBlur, onFocus, onChange, registry }) {
  const DescriptionFieldTemplate = getTemplate("DescriptionFieldTemplate", registry, options);
  const required = schemaRequiresTrueValue(schema);
  const handleChange = (0, import_react13.useCallback)((event) => onChange(event.target.checked), [onChange]);
  const handleBlur = (0, import_react13.useCallback)((event) => onBlur(id, event.target.checked), [onBlur, id]);
  const handleFocus = (0, import_react13.useCallback)((event) => onFocus(id, event.target.checked), [onFocus, id]);
  const description = options.description ?? schema.description;
  return (0, import_jsx_runtime35.jsxs)("div", { className: `checkbox ${disabled || readonly ? "disabled" : ""}`, children: [!hideLabel && description && (0, import_jsx_runtime35.jsx)(DescriptionFieldTemplate, { id: descriptionId(id), description, schema, uiSchema, registry }), (0, import_jsx_runtime35.jsxs)("label", { children: [(0, import_jsx_runtime35.jsx)("input", { type: "checkbox", id, name: id, checked: typeof value === "undefined" ? false : value, required, disabled: disabled || readonly, autoFocus: autofocus, onChange: handleChange, onBlur: handleBlur, onFocus: handleFocus, "aria-describedby": ariaDescribedByIds(id) }), labelValue((0, import_jsx_runtime35.jsx)("span", { children: label }), hideLabel)] })] });
}
var CheckboxWidget_default = CheckboxWidget;

// node_modules/@rjsf/core/lib/components/widgets/CheckboxesWidget.js
var import_jsx_runtime36 = __toESM(require_jsx_runtime(), 1);
var import_react14 = __toESM(require_react(), 1);
function CheckboxesWidget({ id, disabled, options: { inline = false, enumOptions, enumDisabled, emptyValue }, value, autofocus = false, readonly, onChange, onBlur, onFocus }) {
  const checkboxesValues = Array.isArray(value) ? value : [value];
  const handleBlur = (0, import_react14.useCallback)(({ target }) => onBlur(id, enumOptionsValueForIndex(target && target.value, enumOptions, emptyValue)), [onBlur, id]);
  const handleFocus = (0, import_react14.useCallback)(({ target }) => onFocus(id, enumOptionsValueForIndex(target && target.value, enumOptions, emptyValue)), [onFocus, id]);
  return (0, import_jsx_runtime36.jsx)("div", { className: "checkboxes", id, children: Array.isArray(enumOptions) && enumOptions.map((option, index) => {
    const checked = enumOptionsIsSelected(option.value, checkboxesValues);
    const itemDisabled = Array.isArray(enumDisabled) && enumDisabled.indexOf(option.value) !== -1;
    const disabledCls = disabled || itemDisabled || readonly ? "disabled" : "";
    const handleChange = (event) => {
      if (event.target.checked) {
        onChange(enumOptionsSelectValue(index, checkboxesValues, enumOptions));
      } else {
        onChange(enumOptionsDeselectValue(index, checkboxesValues, enumOptions));
      }
    };
    const checkbox = (0, import_jsx_runtime36.jsxs)("span", { children: [(0, import_jsx_runtime36.jsx)("input", { type: "checkbox", id: optionId(id, index), name: id, checked, value: String(index), disabled: disabled || itemDisabled || readonly, autoFocus: autofocus && index === 0, onChange: handleChange, onBlur: handleBlur, onFocus: handleFocus, "aria-describedby": ariaDescribedByIds(id) }), (0, import_jsx_runtime36.jsx)("span", { children: option.label })] });
    return inline ? (0, import_jsx_runtime36.jsx)("label", { className: `checkbox-inline ${disabledCls}`, children: checkbox }, index) : (0, import_jsx_runtime36.jsx)("div", { className: `checkbox ${disabledCls}`, children: (0, import_jsx_runtime36.jsx)("label", { children: checkbox }) }, index);
  }) });
}
var CheckboxesWidget_default = CheckboxesWidget;

// node_modules/@rjsf/core/lib/components/widgets/ColorWidget.js
var import_jsx_runtime37 = __toESM(require_jsx_runtime(), 1);
function ColorWidget(props) {
  const { disabled, readonly, options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  return (0, import_jsx_runtime37.jsx)(BaseInputTemplate2, { type: "color", ...props, disabled: disabled || readonly });
}

// node_modules/@rjsf/core/lib/components/widgets/DateWidget.js
var import_jsx_runtime38 = __toESM(require_jsx_runtime(), 1);
var import_react15 = __toESM(require_react(), 1);
function DateWidget(props) {
  const { onChange, options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  const handleChange = (0, import_react15.useCallback)((value) => onChange(value || void 0), [onChange]);
  return (0, import_jsx_runtime38.jsx)(BaseInputTemplate2, { type: "date", ...props, onChange: handleChange });
}

// node_modules/@rjsf/core/lib/components/widgets/DateTimeWidget.js
var import_jsx_runtime39 = __toESM(require_jsx_runtime(), 1);
function DateTimeWidget(props) {
  const { onChange, value, options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  return (0, import_jsx_runtime39.jsx)(BaseInputTemplate2, { type: "datetime-local", ...props, value: utcToLocal(value), onChange: (value2) => onChange(localToUTC(value2)) });
}

// node_modules/@rjsf/core/lib/components/widgets/EmailWidget.js
var import_jsx_runtime40 = __toESM(require_jsx_runtime(), 1);
function EmailWidget(props) {
  const { options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  return (0, import_jsx_runtime40.jsx)(BaseInputTemplate2, { type: "email", ...props });
}

// node_modules/@rjsf/core/lib/components/widgets/FileWidget.js
var import_jsx_runtime41 = __toESM(require_jsx_runtime(), 1);
var import_react16 = __toESM(require_react(), 1);
function addNameToDataURL(dataURL, name) {
  if (dataURL === null) {
    return null;
  }
  return dataURL.replace(";base64", `;name=${encodeURIComponent(name)};base64`);
}
function processFile(file) {
  const { name, size, type } = file;
  return new Promise((resolve, reject) => {
    const reader = new window.FileReader();
    reader.onerror = reject;
    reader.onload = (event) => {
      var _a;
      if (typeof ((_a = event.target) == null ? void 0 : _a.result) === "string") {
        resolve({
          dataURL: addNameToDataURL(event.target.result, name),
          name,
          size,
          type
        });
      } else {
        resolve({
          dataURL: null,
          name,
          size,
          type
        });
      }
    };
    reader.readAsDataURL(file);
  });
}
function processFiles(files) {
  return Promise.all(Array.from(files).map(processFile));
}
function FileInfoPreview({ fileInfo, registry }) {
  const { translateString } = registry;
  const { dataURL, type, name } = fileInfo;
  if (!dataURL) {
    return null;
  }
  if (["image/jpeg", "image/png"].includes(type)) {
    return (0, import_jsx_runtime41.jsx)("img", { src: dataURL, style: { maxWidth: "100%" }, className: "file-preview" });
  }
  return (0, import_jsx_runtime41.jsxs)(import_jsx_runtime41.Fragment, { children: [" ", (0, import_jsx_runtime41.jsx)("a", { download: `preview-${name}`, href: dataURL, className: "file-download", children: translateString(TranslatableString.PreviewLabel) })] });
}
function FilesInfo({ filesInfo, registry, preview, onRemove, options }) {
  if (filesInfo.length === 0) {
    return null;
  }
  const { translateString } = registry;
  const { RemoveButton: RemoveButton2 } = getTemplate("ButtonTemplates", registry, options);
  return (0, import_jsx_runtime41.jsx)("ul", { className: "file-info", children: filesInfo.map((fileInfo, key) => {
    const { name, size, type } = fileInfo;
    const handleRemove = () => onRemove(key);
    return (0, import_jsx_runtime41.jsxs)("li", { children: [(0, import_jsx_runtime41.jsx)(index_modern_default, { children: translateString(TranslatableString.FilesInfo, [name, type, String(size)]) }), preview && (0, import_jsx_runtime41.jsx)(FileInfoPreview, { fileInfo, registry }), (0, import_jsx_runtime41.jsx)(RemoveButton2, { onClick: handleRemove, registry })] }, key);
  }) });
}
function extractFileInfo(dataURLs) {
  return dataURLs.reduce((acc, dataURL) => {
    if (!dataURL) {
      return acc;
    }
    try {
      const { blob, name } = dataURItoBlob(dataURL);
      return [
        ...acc,
        {
          dataURL,
          name,
          size: blob.size,
          type: blob.type
        }
      ];
    } catch {
      return acc;
    }
  }, []);
}
function FileWidget(props) {
  const { disabled, readonly, required, multiple, onChange, value, options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  const handleChange = (0, import_react16.useCallback)((event) => {
    if (!event.target.files) {
      return;
    }
    processFiles(event.target.files).then((filesInfoEvent) => {
      const newValue = filesInfoEvent.map((fileInfo) => fileInfo.dataURL);
      if (multiple) {
        onChange(value.concat(newValue));
      } else {
        onChange(newValue[0]);
      }
    });
  }, [multiple, value, onChange]);
  const filesInfo = (0, import_react16.useMemo)(() => extractFileInfo(Array.isArray(value) ? value : [value]), [value]);
  const rmFile = (0, import_react16.useCallback)((index) => {
    if (multiple) {
      const newValue = value.filter((_2, i2) => i2 !== index);
      onChange(newValue);
    } else {
      onChange(void 0);
    }
  }, [multiple, value, onChange]);
  return (0, import_jsx_runtime41.jsxs)("div", { children: [(0, import_jsx_runtime41.jsx)(BaseInputTemplate2, { ...props, disabled: disabled || readonly, type: "file", required: value ? false : required, onChangeOverride: handleChange, value: "", accept: options.accept ? String(options.accept) : void 0 }), (0, import_jsx_runtime41.jsx)(FilesInfo, { filesInfo, onRemove: rmFile, registry, preview: options.filePreview, options })] });
}
var FileWidget_default = FileWidget;

// node_modules/@rjsf/core/lib/components/widgets/HiddenWidget.js
var import_jsx_runtime42 = __toESM(require_jsx_runtime(), 1);
function HiddenWidget({ id, value }) {
  return (0, import_jsx_runtime42.jsx)("input", { type: "hidden", id, name: id, value: typeof value === "undefined" ? "" : value });
}
var HiddenWidget_default = HiddenWidget;

// node_modules/@rjsf/core/lib/components/widgets/PasswordWidget.js
var import_jsx_runtime43 = __toESM(require_jsx_runtime(), 1);
function PasswordWidget(props) {
  const { options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  return (0, import_jsx_runtime43.jsx)(BaseInputTemplate2, { type: "password", ...props });
}

// node_modules/@rjsf/core/lib/components/widgets/RadioWidget.js
var import_jsx_runtime44 = __toESM(require_jsx_runtime(), 1);
var import_react17 = __toESM(require_react(), 1);
function RadioWidget({ options, value, required, disabled, readonly, autofocus = false, onBlur, onFocus, onChange, id }) {
  const { enumOptions, enumDisabled, inline, emptyValue } = options;
  const handleBlur = (0, import_react17.useCallback)(({ target }) => onBlur(id, enumOptionsValueForIndex(target && target.value, enumOptions, emptyValue)), [onBlur, enumOptions, emptyValue, id]);
  const handleFocus = (0, import_react17.useCallback)(({ target }) => onFocus(id, enumOptionsValueForIndex(target && target.value, enumOptions, emptyValue)), [onFocus, enumOptions, emptyValue, id]);
  return (0, import_jsx_runtime44.jsx)("div", { className: "field-radio-group", id, role: "radiogroup", children: Array.isArray(enumOptions) && enumOptions.map((option, i2) => {
    const checked = enumOptionsIsSelected(option.value, value);
    const itemDisabled = Array.isArray(enumDisabled) && enumDisabled.indexOf(option.value) !== -1;
    const disabledCls = disabled || itemDisabled || readonly ? "disabled" : "";
    const handleChange = () => onChange(option.value);
    const radio = (0, import_jsx_runtime44.jsxs)("span", { children: [(0, import_jsx_runtime44.jsx)("input", { type: "radio", id: optionId(id, i2), checked, name: id, required, value: String(i2), disabled: disabled || itemDisabled || readonly, autoFocus: autofocus && i2 === 0, onChange: handleChange, onBlur: handleBlur, onFocus: handleFocus, "aria-describedby": ariaDescribedByIds(id) }), (0, import_jsx_runtime44.jsx)("span", { children: option.label })] });
    return inline ? (0, import_jsx_runtime44.jsx)("label", { className: `radio-inline ${disabledCls}`, children: radio }, i2) : (0, import_jsx_runtime44.jsx)("div", { className: `radio ${disabledCls}`, children: (0, import_jsx_runtime44.jsx)("label", { children: radio }) }, i2);
  }) });
}
var RadioWidget_default = RadioWidget;

// node_modules/@rjsf/core/lib/components/widgets/RangeWidget.js
var import_jsx_runtime45 = __toESM(require_jsx_runtime(), 1);
function RangeWidget(props) {
  const { value, registry: { templates: { BaseInputTemplate: BaseInputTemplate2 } } } = props;
  return (0, import_jsx_runtime45.jsxs)("div", { className: "field-range-wrapper", children: [(0, import_jsx_runtime45.jsx)(BaseInputTemplate2, { type: "range", ...props }), (0, import_jsx_runtime45.jsx)("span", { className: "range-view", children: value })] });
}

// node_modules/@rjsf/core/lib/components/widgets/RatingWidget.js
var import_jsx_runtime46 = __toESM(require_jsx_runtime(), 1);
var import_react18 = __toESM(require_react(), 1);
function RatingWidget({ id, value, required, disabled, readonly, autofocus, onChange, onFocus, onBlur, schema, options }) {
  const { stars = 5, shape = "star" } = options;
  const numStars = schema.maximum ? Math.min(schema.maximum, 5) : Math.min(Math.max(stars, 1), 5);
  const min = schema.minimum || 0;
  const handleStarClick = (0, import_react18.useCallback)((starValue) => {
    if (!disabled && !readonly) {
      onChange(starValue);
    }
  }, [onChange, disabled, readonly]);
  const handleFocus = (0, import_react18.useCallback)((event) => {
    if (onFocus) {
      const starValue = Number(event.target.dataset.value);
      onFocus(id, starValue);
    }
  }, [onFocus, id]);
  const handleBlur = (0, import_react18.useCallback)((event) => {
    if (onBlur) {
      const starValue = Number(event.target.dataset.value);
      onBlur(id, starValue);
    }
  }, [onBlur, id]);
  const getSymbol = (isFilled) => {
    if (shape === "heart") {
      return isFilled ? "♥" : "♡";
    }
    return isFilled ? "★" : "☆";
  };
  return (0, import_jsx_runtime46.jsx)(import_jsx_runtime46.Fragment, { children: (0, import_jsx_runtime46.jsxs)("div", { className: "rating-widget", style: {
    display: "inline-flex",
    fontSize: "1.5rem",
    cursor: disabled || readonly ? "default" : "pointer"
  }, children: [[...Array(numStars)].map((_2, index) => {
    const starValue = min + index;
    const isFilled = starValue <= value;
    return (0, import_jsx_runtime46.jsx)("span", { onClick: () => handleStarClick(starValue), onFocus: handleFocus, onBlur: handleBlur, "data-value": starValue, tabIndex: disabled || readonly ? -1 : 0, role: "radio", "aria-checked": starValue === value, "aria-label": `${starValue} ${shape === "heart" ? "heart" : "star"}${starValue === 1 ? "" : "s"}`, style: {
      color: isFilled ? "#FFD700" : "#ccc",
      padding: "0 0.2rem",
      transition: "color 0.2s",
      userSelect: "none"
    }, children: getSymbol(isFilled) }, index);
  }), (0, import_jsx_runtime46.jsx)("input", { type: "hidden", id, name: id, value: value || "", required, disabled: disabled || readonly, "aria-hidden": "true" })] }) });
}

// node_modules/@rjsf/core/lib/components/widgets/SelectWidget.js
var import_jsx_runtime47 = __toESM(require_jsx_runtime(), 1);
var import_react19 = __toESM(require_react(), 1);
function getValue(event, multiple) {
  if (multiple) {
    return Array.from(event.target.options).slice().filter((o2) => o2.selected).map((o2) => o2.value);
  }
  return event.target.value;
}
function SelectWidget({ schema, id, options, value, required, disabled, readonly, multiple = false, autofocus = false, onChange, onBlur, onFocus, placeholder }) {
  const { enumOptions, enumDisabled, emptyValue: optEmptyVal } = options;
  const emptyValue = multiple ? [] : "";
  const handleFocus = (0, import_react19.useCallback)((event) => {
    const newValue = getValue(event, multiple);
    return onFocus(id, enumOptionsValueForIndex(newValue, enumOptions, optEmptyVal));
  }, [onFocus, id, multiple, enumOptions, optEmptyVal]);
  const handleBlur = (0, import_react19.useCallback)((event) => {
    const newValue = getValue(event, multiple);
    return onBlur(id, enumOptionsValueForIndex(newValue, enumOptions, optEmptyVal));
  }, [onBlur, id, multiple, enumOptions, optEmptyVal]);
  const handleChange = (0, import_react19.useCallback)((event) => {
    const newValue = getValue(event, multiple);
    return onChange(enumOptionsValueForIndex(newValue, enumOptions, optEmptyVal));
  }, [onChange, multiple, enumOptions, optEmptyVal]);
  const selectedIndexes = enumOptionsIndexForValue(value, enumOptions, multiple);
  const showPlaceholderOption = !multiple && schema.default === void 0;
  return (0, import_jsx_runtime47.jsxs)("select", { id, name: id, multiple, role: "combobox", className: "form-control", value: typeof selectedIndexes === "undefined" ? emptyValue : selectedIndexes, required, disabled: disabled || readonly, autoFocus: autofocus, onBlur: handleBlur, onFocus: handleFocus, onChange: handleChange, "aria-describedby": ariaDescribedByIds(id), children: [showPlaceholderOption && (0, import_jsx_runtime47.jsx)("option", { value: "", children: placeholder }), Array.isArray(enumOptions) && enumOptions.map(({ value: value2, label }, i2) => {
    const disabled2 = enumDisabled && enumDisabled.indexOf(value2) !== -1;
    return (0, import_jsx_runtime47.jsx)("option", { value: String(i2), disabled: disabled2, children: label }, i2);
  })] });
}
var SelectWidget_default = SelectWidget;

// node_modules/@rjsf/core/lib/components/widgets/TextareaWidget.js
var import_jsx_runtime48 = __toESM(require_jsx_runtime(), 1);
var import_react20 = __toESM(require_react(), 1);
function TextareaWidget({ id, options = {}, placeholder, value, required, disabled, readonly, autofocus = false, onChange, onBlur, onFocus }) {
  const handleChange = (0, import_react20.useCallback)(({ target: { value: value2 } }) => onChange(value2 === "" ? options.emptyValue : value2), [onChange, options.emptyValue]);
  const handleBlur = (0, import_react20.useCallback)(({ target }) => onBlur(id, target && target.value), [onBlur, id]);
  const handleFocus = (0, import_react20.useCallback)(({ target }) => onFocus(id, target && target.value), [id, onFocus]);
  return (0, import_jsx_runtime48.jsx)("textarea", { id, name: id, className: "form-control", value: value ? value : "", placeholder, required, disabled, readOnly: readonly, autoFocus: autofocus, rows: options.rows, onBlur: handleBlur, onFocus: handleFocus, onChange: handleChange, "aria-describedby": ariaDescribedByIds(id) });
}
TextareaWidget.defaultProps = {
  autofocus: false,
  options: {}
};
var TextareaWidget_default = TextareaWidget;

// node_modules/@rjsf/core/lib/components/widgets/TextWidget.js
var import_jsx_runtime49 = __toESM(require_jsx_runtime(), 1);
function TextWidget(props) {
  const { options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  return (0, import_jsx_runtime49.jsx)(BaseInputTemplate2, { ...props });
}

// node_modules/@rjsf/core/lib/components/widgets/TimeWidget.js
var import_jsx_runtime50 = __toESM(require_jsx_runtime(), 1);
var import_react21 = __toESM(require_react(), 1);
function TimeWidget(props) {
  const { onChange, options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  const handleChange = (0, import_react21.useCallback)((value) => onChange(value ? `${value}:00` : void 0), [onChange]);
  return (0, import_jsx_runtime50.jsx)(BaseInputTemplate2, { type: "time", ...props, onChange: handleChange });
}

// node_modules/@rjsf/core/lib/components/widgets/URLWidget.js
var import_jsx_runtime51 = __toESM(require_jsx_runtime(), 1);
function URLWidget(props) {
  const { options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  return (0, import_jsx_runtime51.jsx)(BaseInputTemplate2, { type: "url", ...props });
}

// node_modules/@rjsf/core/lib/components/widgets/UpDownWidget.js
var import_jsx_runtime52 = __toESM(require_jsx_runtime(), 1);
function UpDownWidget(props) {
  const { options, registry } = props;
  const BaseInputTemplate2 = getTemplate("BaseInputTemplate", registry, options);
  return (0, import_jsx_runtime52.jsx)(BaseInputTemplate2, { type: "number", ...props });
}

// node_modules/@rjsf/core/lib/components/widgets/index.js
function widgets() {
  return {
    AltDateWidget: AltDateWidget_default,
    AltDateTimeWidget: AltDateTimeWidget_default,
    CheckboxWidget: CheckboxWidget_default,
    CheckboxesWidget: CheckboxesWidget_default,
    ColorWidget,
    DateWidget,
    DateTimeWidget,
    EmailWidget,
    FileWidget: FileWidget_default,
    HiddenWidget: HiddenWidget_default,
    PasswordWidget,
    RadioWidget: RadioWidget_default,
    RangeWidget,
    RatingWidget,
    SelectWidget: SelectWidget_default,
    TextWidget,
    TextareaWidget: TextareaWidget_default,
    TimeWidget,
    UpDownWidget,
    URLWidget
  };
}
var widgets_default = widgets;

// node_modules/@rjsf/core/lib/getDefaultRegistry.js
function getDefaultRegistry() {
  return {
    fields: fields_default(),
    templates: templates_default(),
    widgets: widgets_default(),
    rootSchema: {},
    formContext: {},
    translateString: englishStringTranslator
  };
}

// node_modules/@rjsf/core/lib/components/Form.js
var Form = class extends import_react22.Component {
  /** Constructs the `Form` from the `props`. Will setup the initial state from the props. It will also call the
   * `onChange` handler if the initially provided `formData` is modified to add missing default values as part of the
   * state construction.
   *
   * @param props - The initial props for the `Form`
   */
  constructor(props) {
    super(props);
    /** The ref used to hold the `form` element, this needs to be `any` because `tagName` or `_internalFormWrapper` can
     * provide any possible type here
     */
    __publicField(this, "formElement");
    /** Returns the `formData` with only the elements specified in the `fields` list
     *
     * @param formData - The data for the `Form`
     * @param fields - The fields to keep while filtering
     */
    __publicField(this, "getUsedFormData", (formData, fields2) => {
      if (fields2.length === 0 && typeof formData !== "object") {
        return formData;
      }
      const data = pick_default(formData, fields2);
      if (Array.isArray(formData)) {
        return Object.keys(data).map((key) => data[key]);
      }
      return data;
    });
    /** Returns the list of field names from inspecting the `pathSchema` as well as using the `formData`
     *
     * @param pathSchema - The `PathSchema` object for the form
     * @param [formData] - The form data to use while checking for empty objects/arrays
     */
    __publicField(this, "getFieldNames", (pathSchema, formData) => {
      const getAllPaths = (_obj, acc = [], paths = [[]]) => {
        Object.keys(_obj).forEach((key) => {
          if (typeof _obj[key] === "object") {
            const newPaths = paths.map((path) => [...path, key]);
            if (_obj[key][RJSF_ADDITIONAL_PROPERTIES_FLAG] && _obj[key][NAME_KEY] !== "") {
              acc.push(_obj[key][NAME_KEY]);
            } else {
              getAllPaths(_obj[key], acc, newPaths);
            }
          } else if (key === NAME_KEY && _obj[key] !== "") {
            paths.forEach((path) => {
              const formValue = get_default(formData, path);
              if (typeof formValue !== "object" || isEmpty_default(formValue) || Array.isArray(formValue) && formValue.every((val) => typeof val !== "object")) {
                acc.push(path);
              }
            });
          }
        });
        return acc;
      };
      return getAllPaths(pathSchema);
    });
    /** Returns the `formData` after filtering to remove any extra data not in a form field
     *
     * @param formData - The data for the `Form`
     * @returns The `formData` after omitting extra data
     */
    __publicField(this, "omitExtraData", (formData) => {
      const { schema, schemaUtils } = this.state;
      const retrievedSchema = schemaUtils.retrieveSchema(schema, formData);
      const pathSchema = schemaUtils.toPathSchema(retrievedSchema, "", formData);
      const fieldNames = this.getFieldNames(pathSchema, formData);
      const newFormData = this.getUsedFormData(formData, fieldNames);
      return newFormData;
    });
    /** Function to handle changes made to a field in the `Form`. This handler receives an entirely new copy of the
     * `formData` along with a new `ErrorSchema`. It will first update the `formData` with any missing default fields and
     * then, if `omitExtraData` and `liveOmit` are turned on, the `formData` will be filtered to remove any extra data not
     * in a form field. Then, the resulting formData will be validated if required. The state will be updated with the new
     * updated (potentially filtered) `formData`, any errors that resulted from validation. Finally the `onChange`
     * callback will be called if specified with the updated state.
     *
     * @param formData - The new form data from a change to a field
     * @param newErrorSchema - The new `ErrorSchema` based on the field change
     * @param id - The id of the field that caused the change
     */
    __publicField(this, "onChange", (formData, newErrorSchema, id) => {
      const { extraErrors, omitExtraData, liveOmit, noValidate, liveValidate, onChange } = this.props;
      const { schemaUtils, schema } = this.state;
      let retrievedSchema = this.state.retrievedSchema;
      if (isObject(formData) || Array.isArray(formData)) {
        const newState = this.getStateFromProps(this.props, formData);
        formData = newState.formData;
        retrievedSchema = newState.retrievedSchema;
      }
      const mustValidate = !noValidate && liveValidate;
      let state = { formData, schema };
      let newFormData = formData;
      if (omitExtraData === true && liveOmit === true) {
        newFormData = this.omitExtraData(formData);
        state = {
          formData: newFormData
        };
      }
      if (mustValidate) {
        const schemaValidation = this.validate(newFormData, schema, schemaUtils, retrievedSchema);
        let errors = schemaValidation.errors;
        let errorSchema = schemaValidation.errorSchema;
        const schemaValidationErrors = errors;
        const schemaValidationErrorSchema = errorSchema;
        if (extraErrors) {
          const merged = validationDataMerge(schemaValidation, extraErrors);
          errorSchema = merged.errorSchema;
          errors = merged.errors;
        }
        if (newErrorSchema) {
          const filteredErrors = this.filterErrorsBasedOnSchema(newErrorSchema, retrievedSchema, newFormData);
          errorSchema = mergeObjects(errorSchema, filteredErrors, "preventDuplicates");
        }
        state = {
          formData: newFormData,
          errors,
          errorSchema,
          schemaValidationErrors,
          schemaValidationErrorSchema
        };
      } else if (!noValidate && newErrorSchema) {
        const errorSchema = extraErrors ? mergeObjects(newErrorSchema, extraErrors, "preventDuplicates") : newErrorSchema;
        state = {
          formData: newFormData,
          errorSchema,
          errors: toErrorList(errorSchema)
        };
      }
      this.setState(state, () => onChange && onChange({ ...this.state, ...state }, id));
    });
    /**
     * Callback function to handle reset form data.
     * - Reset all fields with default values.
     * - Reset validations and errors
     *
     */
    __publicField(this, "reset", () => {
      const { onChange } = this.props;
      const newState = this.getStateFromProps(this.props, void 0);
      const newFormData = newState.formData;
      const state = {
        formData: newFormData,
        errorSchema: {},
        errors: [],
        schemaValidationErrors: [],
        schemaValidationErrorSchema: {}
      };
      this.setState(state, () => onChange && onChange({ ...this.state, ...state }));
    });
    /** Callback function to handle when a field on the form is blurred. Calls the `onBlur` callback for the `Form` if it
     * was provided.
     *
     * @param id - The unique `id` of the field that was blurred
     * @param data - The data associated with the field that was blurred
     */
    __publicField(this, "onBlur", (id, data) => {
      const { onBlur } = this.props;
      if (onBlur) {
        onBlur(id, data);
      }
    });
    /** Callback function to handle when a field on the form is focused. Calls the `onFocus` callback for the `Form` if it
     * was provided.
     *
     * @param id - The unique `id` of the field that was focused
     * @param data - The data associated with the field that was focused
     */
    __publicField(this, "onFocus", (id, data) => {
      const { onFocus } = this.props;
      if (onFocus) {
        onFocus(id, data);
      }
    });
    /** Callback function to handle when the form is submitted. First, it prevents the default event behavior. Nothing
     * happens if the target and currentTarget of the event are not the same. It will omit any extra data in the
     * `formData` in the state if `omitExtraData` is true. It will validate the resulting `formData`, reporting errors
     * via the `onError()` callback unless validation is disabled. Finally, it will add in any `extraErrors` and then call
     * back the `onSubmit` callback if it was provided.
     *
     * @param event - The submit HTML form event
     */
    __publicField(this, "onSubmit", (event) => {
      event.preventDefault();
      if (event.target !== event.currentTarget) {
        return;
      }
      event.persist();
      const { omitExtraData, extraErrors, noValidate, onSubmit } = this.props;
      let { formData: newFormData } = this.state;
      if (omitExtraData === true) {
        newFormData = this.omitExtraData(newFormData);
      }
      if (noValidate || this.validateFormWithFormData(newFormData)) {
        const errorSchema = extraErrors || {};
        const errors = extraErrors ? toErrorList(extraErrors) : [];
        this.setState({
          formData: newFormData,
          errors,
          errorSchema,
          schemaValidationErrors: [],
          schemaValidationErrorSchema: {}
        }, () => {
          if (onSubmit) {
            onSubmit({ ...this.state, formData: newFormData, status: "submitted" }, event);
          }
        });
      }
    });
    /** Provides a function that can be used to programmatically submit the `Form` */
    __publicField(this, "submit", () => {
      if (this.formElement.current) {
        const submitCustomEvent = new CustomEvent("submit", {
          cancelable: true
        });
        submitCustomEvent.preventDefault();
        this.formElement.current.dispatchEvent(submitCustomEvent);
        this.formElement.current.requestSubmit();
      }
    });
    /** Validates the form using the given `formData`. For use on form submission or on programmatic validation.
     * If `onError` is provided, then it will be called with the list of errors.
     *
     * @param formData - The form data to validate
     * @returns - True if the form is valid, false otherwise.
     */
    __publicField(this, "validateFormWithFormData", (formData) => {
      const { extraErrors, extraErrorsBlockSubmit, focusOnFirstError, onError } = this.props;
      const { errors: prevErrors } = this.state;
      const schemaValidation = this.validate(formData);
      let errors = schemaValidation.errors;
      let errorSchema = schemaValidation.errorSchema;
      const schemaValidationErrors = errors;
      const schemaValidationErrorSchema = errorSchema;
      const hasError = errors.length > 0 || extraErrors && extraErrorsBlockSubmit;
      if (hasError) {
        if (extraErrors) {
          const merged = validationDataMerge(schemaValidation, extraErrors);
          errorSchema = merged.errorSchema;
          errors = merged.errors;
        }
        if (focusOnFirstError) {
          if (typeof focusOnFirstError === "function") {
            focusOnFirstError(errors[0]);
          } else {
            this.focusOnError(errors[0]);
          }
        }
        this.setState({
          errors,
          errorSchema,
          schemaValidationErrors,
          schemaValidationErrorSchema
        }, () => {
          if (onError) {
            onError(errors);
          } else {
            console.error("Form validation failed", errors);
          }
        });
      } else if (prevErrors.length > 0) {
        this.setState({
          errors: [],
          errorSchema: {},
          schemaValidationErrors: [],
          schemaValidationErrorSchema: {}
        });
      }
      return !hasError;
    });
    if (!props.validator) {
      throw new Error("A validator is required for Form functionality to work");
    }
    this.state = this.getStateFromProps(props, props.formData);
    if (this.props.onChange && !deepEquals(this.state.formData, this.props.formData)) {
      this.props.onChange(this.state);
    }
    this.formElement = (0, import_react22.createRef)();
  }
  /**
   * `getSnapshotBeforeUpdate` is a React lifecycle method that is invoked right before the most recently rendered
   * output is committed to the DOM. It enables your component to capture current values (e.g., scroll position) before
   * they are potentially changed.
   *
   * In this case, it checks if the props have changed since the last render. If they have, it computes the next state
   * of the component using `getStateFromProps` method and returns it along with a `shouldUpdate` flag set to `true` IF
   * the `nextState` and `prevState` are different, otherwise `false`. This ensures that we have the most up-to-date
   * state ready to be applied in `componentDidUpdate`.
   *
   * If `formData` hasn't changed, it simply returns an object with `shouldUpdate` set to `false`, indicating that a
   * state update is not necessary.
   *
   * @param prevProps - The previous set of props before the update.
   * @param prevState - The previous state before the update.
   * @returns Either an object containing the next state and a flag indicating that an update should occur, or an object
   *        with a flag indicating that an update is not necessary.
   */
  getSnapshotBeforeUpdate(prevProps, prevState) {
    if (!deepEquals(this.props, prevProps)) {
      const formDataChangedFields = getChangedFields(this.props.formData, prevProps.formData);
      const isSchemaChanged = !deepEquals(prevProps.schema, this.props.schema);
      const isFormDataChanged = formDataChangedFields.length > 0 || !deepEquals(prevProps.formData, this.props.formData);
      const nextState = this.getStateFromProps(
        this.props,
        this.props.formData,
        // If the `schema` has changed, we need to update the retrieved schema.
        // Or if the `formData` changes, for example in the case of a schema with dependencies that need to
        //  match one of the subSchemas, the retrieved schema must be updated.
        isSchemaChanged || isFormDataChanged ? void 0 : this.state.retrievedSchema,
        isSchemaChanged,
        formDataChangedFields
      );
      const shouldUpdate = !deepEquals(nextState, prevState);
      return { nextState, shouldUpdate };
    }
    return { shouldUpdate: false };
  }
  /**
   * `componentDidUpdate` is a React lifecycle method that is invoked immediately after updating occurs. This method is
   * not called for the initial render.
   *
   * Here, it checks if an update is necessary based on the `shouldUpdate` flag received from `getSnapshotBeforeUpdate`.
   * If an update is required, it applies the next state and, if needed, triggers the `onChange` handler to inform about
   * changes.
   *
   * @param _ - The previous set of props.
   * @param prevState - The previous state of the component before the update.
   * @param snapshot - The value returned from `getSnapshotBeforeUpdate`.
   */
  componentDidUpdate(_2, prevState, snapshot) {
    if (snapshot.shouldUpdate) {
      const { nextState } = snapshot;
      if (!deepEquals(nextState.formData, this.props.formData) && !deepEquals(nextState.formData, prevState.formData) && this.props.onChange) {
        this.props.onChange(nextState);
      }
      this.setState(nextState);
    }
  }
  /** Extracts the updated state from the given `props` and `inputFormData`. As part of this process, the
   * `inputFormData` is first processed to add any missing required defaults. After that, the data is run through the
   * validation process IF required by the `props`.
   *
   * @param props - The props passed to the `Form`
   * @param inputFormData - The new or current data for the `Form`
   * @param retrievedSchema - An expanded schema, if not provided, it will be retrieved from the `schema` and `formData`.
   * @param isSchemaChanged - A flag indicating whether the schema has changed.
   * @param formDataChangedFields - The changed fields of `formData`
   * @returns - The new state for the `Form`
   */
  getStateFromProps(props, inputFormData, retrievedSchema, isSchemaChanged = false, formDataChangedFields = []) {
    var _a;
    const state = this.state || {};
    const schema = "schema" in props ? props.schema : this.props.schema;
    const uiSchema = ("uiSchema" in props ? props.uiSchema : this.props.uiSchema) || {};
    const edit = typeof inputFormData !== "undefined";
    const liveValidate = "liveValidate" in props ? props.liveValidate : this.props.liveValidate;
    const mustValidate = edit && !props.noValidate && liveValidate;
    const rootSchema = schema;
    const experimental_defaultFormStateBehavior = "experimental_defaultFormStateBehavior" in props ? props.experimental_defaultFormStateBehavior : this.props.experimental_defaultFormStateBehavior;
    const experimental_customMergeAllOf = "experimental_customMergeAllOf" in props ? props.experimental_customMergeAllOf : this.props.experimental_customMergeAllOf;
    let schemaUtils = state.schemaUtils;
    if (!schemaUtils || schemaUtils.doesSchemaUtilsDiffer(props.validator, rootSchema, experimental_defaultFormStateBehavior, experimental_customMergeAllOf)) {
      schemaUtils = createSchemaUtils(props.validator, rootSchema, experimental_defaultFormStateBehavior, experimental_customMergeAllOf);
    }
    const formData = schemaUtils.getDefaultFormState(schema, inputFormData);
    const _retrievedSchema = this.updateRetrievedSchema(retrievedSchema ?? schemaUtils.retrieveSchema(schema, formData));
    const getCurrentErrors = () => {
      if (props.noValidate || isSchemaChanged) {
        return { errors: [], errorSchema: {} };
      } else if (!props.liveValidate) {
        return {
          errors: state.schemaValidationErrors || [],
          errorSchema: state.schemaValidationErrorSchema || {}
        };
      }
      return {
        errors: state.errors || [],
        errorSchema: state.errorSchema || {}
      };
    };
    let errors;
    let errorSchema;
    let schemaValidationErrors = state.schemaValidationErrors;
    let schemaValidationErrorSchema = state.schemaValidationErrorSchema;
    if (mustValidate) {
      const schemaValidation = this.validate(formData, schema, schemaUtils, _retrievedSchema);
      errors = schemaValidation.errors;
      if (retrievedSchema === void 0) {
        errorSchema = schemaValidation.errorSchema;
      } else {
        errorSchema = mergeObjects((_a = this.state) == null ? void 0 : _a.errorSchema, schemaValidation.errorSchema, "preventDuplicates");
      }
      schemaValidationErrors = errors;
      schemaValidationErrorSchema = errorSchema;
    } else {
      const currentErrors = getCurrentErrors();
      errors = currentErrors.errors;
      errorSchema = currentErrors.errorSchema;
      if (formDataChangedFields.length > 0) {
        const newErrorSchema = formDataChangedFields.reduce((acc, key) => {
          acc[key] = void 0;
          return acc;
        }, {});
        errorSchema = schemaValidationErrorSchema = mergeObjects(currentErrors.errorSchema, newErrorSchema, "preventDuplicates");
      }
    }
    if (props.extraErrors) {
      const merged = validationDataMerge({ errorSchema, errors }, props.extraErrors);
      errorSchema = merged.errorSchema;
      errors = merged.errors;
    }
    const idSchema = schemaUtils.toIdSchema(_retrievedSchema, uiSchema["ui:rootFieldId"], formData, props.idPrefix, props.idSeparator);
    const nextState = {
      schemaUtils,
      schema,
      uiSchema,
      idSchema,
      formData,
      edit,
      errors,
      errorSchema,
      schemaValidationErrors,
      schemaValidationErrorSchema,
      retrievedSchema: _retrievedSchema
    };
    return nextState;
  }
  /** React lifecycle method that is used to determine whether component should be updated.
   *
   * @param nextProps - The next version of the props
   * @param nextState - The next version of the state
   * @returns - True if the component should be updated, false otherwise
   */
  shouldComponentUpdate(nextProps, nextState) {
    return shouldRender(this, nextProps, nextState);
  }
  /** Gets the previously raised customValidate errors.
   *
   * @returns the previous customValidate errors
   */
  getPreviousCustomValidateErrors() {
    const { customValidate, uiSchema } = this.props;
    const prevFormData = this.state.formData;
    let customValidateErrors = {};
    if (typeof customValidate === "function") {
      const errorHandler = customValidate(prevFormData, createErrorHandler(prevFormData), uiSchema);
      const userErrorSchema = unwrapErrorHandler(errorHandler);
      customValidateErrors = userErrorSchema;
    }
    return customValidateErrors;
  }
  /** Validates the `formData` against the `schema` using the `altSchemaUtils` (if provided otherwise it uses the
   * `schemaUtils` in the state), returning the results.
   *
   * @param formData - The new form data to validate
   * @param schema - The schema used to validate against
   * @param altSchemaUtils - The alternate schemaUtils to use for validation
   */
  validate(formData, schema = this.props.schema, altSchemaUtils, retrievedSchema) {
    const schemaUtils = altSchemaUtils ? altSchemaUtils : this.state.schemaUtils;
    const { customValidate, transformErrors, uiSchema } = this.props;
    const resolvedSchema = retrievedSchema ?? schemaUtils.retrieveSchema(schema, formData);
    return schemaUtils.getValidator().validateFormData(formData, resolvedSchema, customValidate, transformErrors, uiSchema);
  }
  /** Renders any errors contained in the `state` in using the `ErrorList`, if not disabled by `showErrorList`. */
  renderErrors(registry) {
    const { errors, errorSchema, schema, uiSchema } = this.state;
    const { formContext } = this.props;
    const options = getUiOptions(uiSchema);
    const ErrorListTemplate = getTemplate("ErrorListTemplate", registry, options);
    if (errors && errors.length) {
      return (0, import_jsx_runtime53.jsx)(ErrorListTemplate, { errors, errorSchema: errorSchema || {}, schema, uiSchema, formContext, registry });
    }
    return null;
  }
  // Filtering errors based on your retrieved schema to only show errors for properties in the selected branch.
  filterErrorsBasedOnSchema(schemaErrors, resolvedSchema, formData) {
    const { retrievedSchema, schemaUtils } = this.state;
    const _retrievedSchema = resolvedSchema ?? retrievedSchema;
    const pathSchema = schemaUtils.toPathSchema(_retrievedSchema, "", formData);
    const fieldNames = this.getFieldNames(pathSchema, formData);
    const filteredErrors = pick_default(schemaErrors, fieldNames);
    if ((resolvedSchema == null ? void 0 : resolvedSchema.type) !== "object" && (resolvedSchema == null ? void 0 : resolvedSchema.type) !== "array") {
      filteredErrors.__errors = schemaErrors.__errors;
    }
    const prevCustomValidateErrors = this.getPreviousCustomValidateErrors();
    const filterPreviousCustomErrors = (errors = [], prevCustomErrors) => {
      if (errors.length === 0) {
        return errors;
      }
      return errors.filter((error) => {
        return !prevCustomErrors.includes(error);
      });
    };
    const filterNilOrEmptyErrors = (errors, previousCustomValidateErrors = {}) => {
      forEach_default(errors, (errorAtKey, errorKey) => {
        const prevCustomValidateErrorAtKey = previousCustomValidateErrors[errorKey];
        if (isNil_default(errorAtKey) || Array.isArray(errorAtKey) && errorAtKey.length === 0) {
          delete errors[errorKey];
        } else if (isObject(errorAtKey) && isObject(prevCustomValidateErrorAtKey) && Array.isArray(prevCustomValidateErrorAtKey == null ? void 0 : prevCustomValidateErrorAtKey.__errors)) {
          errors[errorKey] = filterPreviousCustomErrors(errorAtKey.__errors, prevCustomValidateErrorAtKey.__errors);
        } else if (typeof errorAtKey === "object" && !Array.isArray(errorAtKey.__errors)) {
          filterNilOrEmptyErrors(errorAtKey, previousCustomValidateErrors[errorKey]);
        }
      });
      return errors;
    };
    return filterNilOrEmptyErrors(filteredErrors, prevCustomValidateErrors);
  }
  /**
   * If the retrievedSchema has changed the new retrievedSchema is returned.
   * Otherwise, the old retrievedSchema is returned to persist reference.
   * -  This ensures that AJV retrieves the schema from the cache when it has not changed,
   *    avoiding the performance cost of recompiling the schema.
   *
   * @param retrievedSchema The new retrieved schema.
   * @returns The new retrieved schema if it has changed, else the old retrieved schema.
   */
  updateRetrievedSchema(retrievedSchema) {
    var _a;
    const isTheSame = deepEquals(retrievedSchema, (_a = this.state) == null ? void 0 : _a.retrievedSchema);
    return isTheSame ? this.state.retrievedSchema : retrievedSchema;
  }
  /** Returns the registry for the form */
  getRegistry() {
    var _a;
    const { translateString: customTranslateString, uiSchema = {} } = this.props;
    const { schemaUtils } = this.state;
    const { fields: fields2, templates: templates2, widgets: widgets2, formContext, translateString } = getDefaultRegistry();
    return {
      fields: { ...fields2, ...this.props.fields },
      templates: {
        ...templates2,
        ...this.props.templates,
        ButtonTemplates: {
          ...templates2.ButtonTemplates,
          ...(_a = this.props.templates) == null ? void 0 : _a.ButtonTemplates
        }
      },
      widgets: { ...widgets2, ...this.props.widgets },
      rootSchema: this.props.schema,
      formContext: this.props.formContext || formContext,
      schemaUtils,
      translateString: customTranslateString || translateString,
      globalUiOptions: uiSchema[UI_GLOBAL_OPTIONS_KEY]
    };
  }
  /** Attempts to focus on the field associated with the `error`. Uses the `property` field to compute path of the error
   * field, then, using the `idPrefix` and `idSeparator` converts that path into an id. Then the input element with that
   * id is attempted to be found using the `formElement` ref. If it is located, then it is focused.
   *
   * @param error - The error on which to focus
   */
  focusOnError(error) {
    const { idPrefix = "root", idSeparator = "_" } = this.props;
    const { property } = error;
    const path = toPath_default(property);
    if (path[0] === "") {
      path[0] = idPrefix;
    } else {
      path.unshift(idPrefix);
    }
    const elementId = path.join(idSeparator);
    let field = this.formElement.current.elements[elementId];
    if (!field) {
      field = this.formElement.current.querySelector(`input[id^="${elementId}"`);
    }
    if (field && field.length) {
      field = field[0];
    }
    if (field) {
      field.focus();
    }
  }
  /** Programmatically validate the form.  If `omitExtraData` is true, the `formData` will first be filtered to remove
   * any extra data not in a form field. If `onError` is provided, then it will be called with the list of errors the
   * same way as would happen on form submission.
   *
   * @returns - True if the form is valid, false otherwise.
   */
  validateForm() {
    const { omitExtraData } = this.props;
    let { formData: newFormData } = this.state;
    if (omitExtraData === true) {
      newFormData = this.omitExtraData(newFormData);
    }
    return this.validateFormWithFormData(newFormData);
  }
  /** Renders the `Form` fields inside the <form> | `tagName` or `_internalFormWrapper`, rendering any errors if
   * needed along with the submit button or any children of the form.
   */
  render() {
    const { children, id, idPrefix, idSeparator, className = "", tagName, name, method, target, action, autoComplete, enctype, acceptCharset, noHtml5Validate = false, disabled, readonly, formContext, showErrorList = "top", _internalFormWrapper } = this.props;
    const { schema, uiSchema, formData, errorSchema, idSchema } = this.state;
    const registry = this.getRegistry();
    const { SchemaField: _SchemaField } = registry.fields;
    const { SubmitButton: SubmitButton2 } = registry.templates.ButtonTemplates;
    const as = _internalFormWrapper ? tagName : void 0;
    const FormTag = _internalFormWrapper || tagName || "form";
    let { [SUBMIT_BTN_OPTIONS_KEY]: submitOptions = {} } = getUiOptions(uiSchema);
    if (disabled) {
      submitOptions = { ...submitOptions, props: { ...submitOptions.props, disabled: true } };
    }
    const submitUiSchema = { [UI_OPTIONS_KEY]: { [SUBMIT_BTN_OPTIONS_KEY]: submitOptions } };
    return (0, import_jsx_runtime53.jsxs)(FormTag, { className: className ? className : "rjsf", id, name, method, target, action, autoComplete, encType: enctype, acceptCharset, noValidate: noHtml5Validate, onSubmit: this.onSubmit, as, ref: this.formElement, children: [showErrorList === "top" && this.renderErrors(registry), (0, import_jsx_runtime53.jsx)(_SchemaField, { name: "", schema, uiSchema, errorSchema, idSchema, idPrefix, idSeparator, formContext, formData, onChange: this.onChange, onBlur: this.onBlur, onFocus: this.onFocus, registry, disabled, readonly }), children ? children : (0, import_jsx_runtime53.jsx)(SubmitButton2, { uiSchema: submitUiSchema, registry }), showErrorList === "bottom" && this.renderErrors(registry)] });
  }
};

// node_modules/@rjsf/core/lib/withTheme.js
var import_jsx_runtime54 = __toESM(require_jsx_runtime(), 1);
var import_react23 = __toESM(require_react(), 1);
function withTheme(themeProps) {
  return (0, import_react23.forwardRef)(({ fields: fields2, widgets: widgets2, templates: templates2, ...directProps }, ref) => {
    var _a;
    fields2 = { ...themeProps == null ? void 0 : themeProps.fields, ...fields2 };
    widgets2 = { ...themeProps == null ? void 0 : themeProps.widgets, ...widgets2 };
    templates2 = {
      ...themeProps == null ? void 0 : themeProps.templates,
      ...templates2,
      ButtonTemplates: {
        ...(_a = themeProps == null ? void 0 : themeProps.templates) == null ? void 0 : _a.ButtonTemplates,
        ...templates2 == null ? void 0 : templates2.ButtonTemplates
      }
    };
    return (0, import_jsx_runtime54.jsx)(Form, { ...themeProps, ...directProps, fields: fields2, widgets: widgets2, templates: templates2, ref });
  });
}

// node_modules/@rjsf/core/lib/index.js
var lib_default = Form;
export {
  RichDescription,
  lib_default as default,
  getDefaultRegistry,
  withTheme
};
//# sourceMappingURL=@rjsf_core.js.map
