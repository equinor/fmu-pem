import {
  require_jsx_runtime
} from "./chunk-LPWVGVNP.js";
import {
  require_react
} from "./chunk-6FYWT56J.js";
import {
  __commonJS,
  __toESM
} from "./chunk-DC5AMYBS.js";

// node_modules/lodash/_listCacheClear.js
var require_listCacheClear = __commonJS({
  "node_modules/lodash/_listCacheClear.js"(exports2, module2) {
    function listCacheClear2() {
      this.__data__ = [];
      this.size = 0;
    }
    module2.exports = listCacheClear2;
  }
});

// node_modules/lodash/eq.js
var require_eq = __commonJS({
  "node_modules/lodash/eq.js"(exports2, module2) {
    function eq2(value, other) {
      return value === other || value !== value && other !== other;
    }
    module2.exports = eq2;
  }
});

// node_modules/lodash/_assocIndexOf.js
var require_assocIndexOf = __commonJS({
  "node_modules/lodash/_assocIndexOf.js"(exports2, module2) {
    var eq2 = require_eq();
    function assocIndexOf2(array, key) {
      var length = array.length;
      while (length--) {
        if (eq2(array[length][0], key)) {
          return length;
        }
      }
      return -1;
    }
    module2.exports = assocIndexOf2;
  }
});

// node_modules/lodash/_listCacheDelete.js
var require_listCacheDelete = __commonJS({
  "node_modules/lodash/_listCacheDelete.js"(exports2, module2) {
    var assocIndexOf2 = require_assocIndexOf();
    var arrayProto2 = Array.prototype;
    var splice2 = arrayProto2.splice;
    function listCacheDelete2(key) {
      var data = this.__data__, index = assocIndexOf2(data, key);
      if (index < 0) {
        return false;
      }
      var lastIndex = data.length - 1;
      if (index == lastIndex) {
        data.pop();
      } else {
        splice2.call(data, index, 1);
      }
      --this.size;
      return true;
    }
    module2.exports = listCacheDelete2;
  }
});

// node_modules/lodash/_listCacheGet.js
var require_listCacheGet = __commonJS({
  "node_modules/lodash/_listCacheGet.js"(exports2, module2) {
    var assocIndexOf2 = require_assocIndexOf();
    function listCacheGet2(key) {
      var data = this.__data__, index = assocIndexOf2(data, key);
      return index < 0 ? void 0 : data[index][1];
    }
    module2.exports = listCacheGet2;
  }
});

// node_modules/lodash/_listCacheHas.js
var require_listCacheHas = __commonJS({
  "node_modules/lodash/_listCacheHas.js"(exports2, module2) {
    var assocIndexOf2 = require_assocIndexOf();
    function listCacheHas2(key) {
      return assocIndexOf2(this.__data__, key) > -1;
    }
    module2.exports = listCacheHas2;
  }
});

// node_modules/lodash/_listCacheSet.js
var require_listCacheSet = __commonJS({
  "node_modules/lodash/_listCacheSet.js"(exports2, module2) {
    var assocIndexOf2 = require_assocIndexOf();
    function listCacheSet2(key, value) {
      var data = this.__data__, index = assocIndexOf2(data, key);
      if (index < 0) {
        ++this.size;
        data.push([key, value]);
      } else {
        data[index][1] = value;
      }
      return this;
    }
    module2.exports = listCacheSet2;
  }
});

// node_modules/lodash/_ListCache.js
var require_ListCache = __commonJS({
  "node_modules/lodash/_ListCache.js"(exports2, module2) {
    var listCacheClear2 = require_listCacheClear();
    var listCacheDelete2 = require_listCacheDelete();
    var listCacheGet2 = require_listCacheGet();
    var listCacheHas2 = require_listCacheHas();
    var listCacheSet2 = require_listCacheSet();
    function ListCache2(entries) {
      var index = -1, length = entries == null ? 0 : entries.length;
      this.clear();
      while (++index < length) {
        var entry = entries[index];
        this.set(entry[0], entry[1]);
      }
    }
    ListCache2.prototype.clear = listCacheClear2;
    ListCache2.prototype["delete"] = listCacheDelete2;
    ListCache2.prototype.get = listCacheGet2;
    ListCache2.prototype.has = listCacheHas2;
    ListCache2.prototype.set = listCacheSet2;
    module2.exports = ListCache2;
  }
});

// node_modules/lodash/_stackClear.js
var require_stackClear = __commonJS({
  "node_modules/lodash/_stackClear.js"(exports2, module2) {
    var ListCache2 = require_ListCache();
    function stackClear2() {
      this.__data__ = new ListCache2();
      this.size = 0;
    }
    module2.exports = stackClear2;
  }
});

// node_modules/lodash/_stackDelete.js
var require_stackDelete = __commonJS({
  "node_modules/lodash/_stackDelete.js"(exports2, module2) {
    function stackDelete2(key) {
      var data = this.__data__, result = data["delete"](key);
      this.size = data.size;
      return result;
    }
    module2.exports = stackDelete2;
  }
});

// node_modules/lodash/_stackGet.js
var require_stackGet = __commonJS({
  "node_modules/lodash/_stackGet.js"(exports2, module2) {
    function stackGet2(key) {
      return this.__data__.get(key);
    }
    module2.exports = stackGet2;
  }
});

// node_modules/lodash/_stackHas.js
var require_stackHas = __commonJS({
  "node_modules/lodash/_stackHas.js"(exports2, module2) {
    function stackHas2(key) {
      return this.__data__.has(key);
    }
    module2.exports = stackHas2;
  }
});

// node_modules/lodash/_freeGlobal.js
var require_freeGlobal = __commonJS({
  "node_modules/lodash/_freeGlobal.js"(exports2, module2) {
    var freeGlobal2 = typeof global == "object" && global && global.Object === Object && global;
    module2.exports = freeGlobal2;
  }
});

// node_modules/lodash/_root.js
var require_root = __commonJS({
  "node_modules/lodash/_root.js"(exports2, module2) {
    var freeGlobal2 = require_freeGlobal();
    var freeSelf2 = typeof self == "object" && self && self.Object === Object && self;
    var root2 = freeGlobal2 || freeSelf2 || Function("return this")();
    module2.exports = root2;
  }
});

// node_modules/lodash/_Symbol.js
var require_Symbol = __commonJS({
  "node_modules/lodash/_Symbol.js"(exports2, module2) {
    var root2 = require_root();
    var Symbol3 = root2.Symbol;
    module2.exports = Symbol3;
  }
});

// node_modules/lodash/_getRawTag.js
var require_getRawTag = __commonJS({
  "node_modules/lodash/_getRawTag.js"(exports2, module2) {
    var Symbol3 = require_Symbol();
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    var nativeObjectToString3 = objectProto19.toString;
    var symToStringTag3 = Symbol3 ? Symbol3.toStringTag : void 0;
    function getRawTag2(value) {
      var isOwn = hasOwnProperty16.call(value, symToStringTag3), tag = value[symToStringTag3];
      try {
        value[symToStringTag3] = void 0;
        var unmasked = true;
      } catch (e) {
      }
      var result = nativeObjectToString3.call(value);
      if (unmasked) {
        if (isOwn) {
          value[symToStringTag3] = tag;
        } else {
          delete value[symToStringTag3];
        }
      }
      return result;
    }
    module2.exports = getRawTag2;
  }
});

// node_modules/lodash/_objectToString.js
var require_objectToString = __commonJS({
  "node_modules/lodash/_objectToString.js"(exports2, module2) {
    var objectProto19 = Object.prototype;
    var nativeObjectToString3 = objectProto19.toString;
    function objectToString2(value) {
      return nativeObjectToString3.call(value);
    }
    module2.exports = objectToString2;
  }
});

// node_modules/lodash/_baseGetTag.js
var require_baseGetTag = __commonJS({
  "node_modules/lodash/_baseGetTag.js"(exports2, module2) {
    var Symbol3 = require_Symbol();
    var getRawTag2 = require_getRawTag();
    var objectToString2 = require_objectToString();
    var nullTag2 = "[object Null]";
    var undefinedTag2 = "[object Undefined]";
    var symToStringTag3 = Symbol3 ? Symbol3.toStringTag : void 0;
    function baseGetTag2(value) {
      if (value == null) {
        return value === void 0 ? undefinedTag2 : nullTag2;
      }
      return symToStringTag3 && symToStringTag3 in Object(value) ? getRawTag2(value) : objectToString2(value);
    }
    module2.exports = baseGetTag2;
  }
});

// node_modules/lodash/isObject.js
var require_isObject = __commonJS({
  "node_modules/lodash/isObject.js"(exports2, module2) {
    function isObject3(value) {
      var type = typeof value;
      return value != null && (type == "object" || type == "function");
    }
    module2.exports = isObject3;
  }
});

// node_modules/lodash/isFunction.js
var require_isFunction = __commonJS({
  "node_modules/lodash/isFunction.js"(exports2, module2) {
    var baseGetTag2 = require_baseGetTag();
    var isObject3 = require_isObject();
    var asyncTag2 = "[object AsyncFunction]";
    var funcTag4 = "[object Function]";
    var genTag3 = "[object GeneratorFunction]";
    var proxyTag2 = "[object Proxy]";
    function isFunction2(value) {
      if (!isObject3(value)) {
        return false;
      }
      var tag = baseGetTag2(value);
      return tag == funcTag4 || tag == genTag3 || tag == asyncTag2 || tag == proxyTag2;
    }
    module2.exports = isFunction2;
  }
});

// node_modules/lodash/_coreJsData.js
var require_coreJsData = __commonJS({
  "node_modules/lodash/_coreJsData.js"(exports2, module2) {
    var root2 = require_root();
    var coreJsData2 = root2["__core-js_shared__"];
    module2.exports = coreJsData2;
  }
});

// node_modules/lodash/_isMasked.js
var require_isMasked = __commonJS({
  "node_modules/lodash/_isMasked.js"(exports2, module2) {
    var coreJsData2 = require_coreJsData();
    var maskSrcKey2 = function() {
      var uid = /[^.]+$/.exec(coreJsData2 && coreJsData2.keys && coreJsData2.keys.IE_PROTO || "");
      return uid ? "Symbol(src)_1." + uid : "";
    }();
    function isMasked2(func) {
      return !!maskSrcKey2 && maskSrcKey2 in func;
    }
    module2.exports = isMasked2;
  }
});

// node_modules/lodash/_toSource.js
var require_toSource = __commonJS({
  "node_modules/lodash/_toSource.js"(exports2, module2) {
    var funcProto4 = Function.prototype;
    var funcToString4 = funcProto4.toString;
    function toSource2(func) {
      if (func != null) {
        try {
          return funcToString4.call(func);
        } catch (e) {
        }
        try {
          return func + "";
        } catch (e) {
        }
      }
      return "";
    }
    module2.exports = toSource2;
  }
});

// node_modules/lodash/_baseIsNative.js
var require_baseIsNative = __commonJS({
  "node_modules/lodash/_baseIsNative.js"(exports2, module2) {
    var isFunction2 = require_isFunction();
    var isMasked2 = require_isMasked();
    var isObject3 = require_isObject();
    var toSource2 = require_toSource();
    var reRegExpChar2 = /[\\^$.*+?()[\]{}|]/g;
    var reIsHostCtor2 = /^\[object .+?Constructor\]$/;
    var funcProto4 = Function.prototype;
    var objectProto19 = Object.prototype;
    var funcToString4 = funcProto4.toString;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    var reIsNative2 = RegExp(
      "^" + funcToString4.call(hasOwnProperty16).replace(reRegExpChar2, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"
    );
    function baseIsNative2(value) {
      if (!isObject3(value) || isMasked2(value)) {
        return false;
      }
      var pattern = isFunction2(value) ? reIsNative2 : reIsHostCtor2;
      return pattern.test(toSource2(value));
    }
    module2.exports = baseIsNative2;
  }
});

// node_modules/lodash/_getValue.js
var require_getValue = __commonJS({
  "node_modules/lodash/_getValue.js"(exports2, module2) {
    function getValue2(object, key) {
      return object == null ? void 0 : object[key];
    }
    module2.exports = getValue2;
  }
});

// node_modules/lodash/_getNative.js
var require_getNative = __commonJS({
  "node_modules/lodash/_getNative.js"(exports2, module2) {
    var baseIsNative2 = require_baseIsNative();
    var getValue2 = require_getValue();
    function getNative2(object, key) {
      var value = getValue2(object, key);
      return baseIsNative2(value) ? value : void 0;
    }
    module2.exports = getNative2;
  }
});

// node_modules/lodash/_Map.js
var require_Map = __commonJS({
  "node_modules/lodash/_Map.js"(exports2, module2) {
    var getNative2 = require_getNative();
    var root2 = require_root();
    var Map3 = getNative2(root2, "Map");
    module2.exports = Map3;
  }
});

// node_modules/lodash/_nativeCreate.js
var require_nativeCreate = __commonJS({
  "node_modules/lodash/_nativeCreate.js"(exports2, module2) {
    var getNative2 = require_getNative();
    var nativeCreate2 = getNative2(Object, "create");
    module2.exports = nativeCreate2;
  }
});

// node_modules/lodash/_hashClear.js
var require_hashClear = __commonJS({
  "node_modules/lodash/_hashClear.js"(exports2, module2) {
    var nativeCreate2 = require_nativeCreate();
    function hashClear2() {
      this.__data__ = nativeCreate2 ? nativeCreate2(null) : {};
      this.size = 0;
    }
    module2.exports = hashClear2;
  }
});

// node_modules/lodash/_hashDelete.js
var require_hashDelete = __commonJS({
  "node_modules/lodash/_hashDelete.js"(exports2, module2) {
    function hashDelete2(key) {
      var result = this.has(key) && delete this.__data__[key];
      this.size -= result ? 1 : 0;
      return result;
    }
    module2.exports = hashDelete2;
  }
});

// node_modules/lodash/_hashGet.js
var require_hashGet = __commonJS({
  "node_modules/lodash/_hashGet.js"(exports2, module2) {
    var nativeCreate2 = require_nativeCreate();
    var HASH_UNDEFINED4 = "__lodash_hash_undefined__";
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function hashGet2(key) {
      var data = this.__data__;
      if (nativeCreate2) {
        var result = data[key];
        return result === HASH_UNDEFINED4 ? void 0 : result;
      }
      return hasOwnProperty16.call(data, key) ? data[key] : void 0;
    }
    module2.exports = hashGet2;
  }
});

// node_modules/lodash/_hashHas.js
var require_hashHas = __commonJS({
  "node_modules/lodash/_hashHas.js"(exports2, module2) {
    var nativeCreate2 = require_nativeCreate();
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function hashHas2(key) {
      var data = this.__data__;
      return nativeCreate2 ? data[key] !== void 0 : hasOwnProperty16.call(data, key);
    }
    module2.exports = hashHas2;
  }
});

// node_modules/lodash/_hashSet.js
var require_hashSet = __commonJS({
  "node_modules/lodash/_hashSet.js"(exports2, module2) {
    var nativeCreate2 = require_nativeCreate();
    var HASH_UNDEFINED4 = "__lodash_hash_undefined__";
    function hashSet2(key, value) {
      var data = this.__data__;
      this.size += this.has(key) ? 0 : 1;
      data[key] = nativeCreate2 && value === void 0 ? HASH_UNDEFINED4 : value;
      return this;
    }
    module2.exports = hashSet2;
  }
});

// node_modules/lodash/_Hash.js
var require_Hash = __commonJS({
  "node_modules/lodash/_Hash.js"(exports2, module2) {
    var hashClear2 = require_hashClear();
    var hashDelete2 = require_hashDelete();
    var hashGet2 = require_hashGet();
    var hashHas2 = require_hashHas();
    var hashSet2 = require_hashSet();
    function Hash2(entries) {
      var index = -1, length = entries == null ? 0 : entries.length;
      this.clear();
      while (++index < length) {
        var entry = entries[index];
        this.set(entry[0], entry[1]);
      }
    }
    Hash2.prototype.clear = hashClear2;
    Hash2.prototype["delete"] = hashDelete2;
    Hash2.prototype.get = hashGet2;
    Hash2.prototype.has = hashHas2;
    Hash2.prototype.set = hashSet2;
    module2.exports = Hash2;
  }
});

// node_modules/lodash/_mapCacheClear.js
var require_mapCacheClear = __commonJS({
  "node_modules/lodash/_mapCacheClear.js"(exports2, module2) {
    var Hash2 = require_Hash();
    var ListCache2 = require_ListCache();
    var Map3 = require_Map();
    function mapCacheClear2() {
      this.size = 0;
      this.__data__ = {
        "hash": new Hash2(),
        "map": new (Map3 || ListCache2)(),
        "string": new Hash2()
      };
    }
    module2.exports = mapCacheClear2;
  }
});

// node_modules/lodash/_isKeyable.js
var require_isKeyable = __commonJS({
  "node_modules/lodash/_isKeyable.js"(exports2, module2) {
    function isKeyable2(value) {
      var type = typeof value;
      return type == "string" || type == "number" || type == "symbol" || type == "boolean" ? value !== "__proto__" : value === null;
    }
    module2.exports = isKeyable2;
  }
});

// node_modules/lodash/_getMapData.js
var require_getMapData = __commonJS({
  "node_modules/lodash/_getMapData.js"(exports2, module2) {
    var isKeyable2 = require_isKeyable();
    function getMapData2(map, key) {
      var data = map.__data__;
      return isKeyable2(key) ? data[typeof key == "string" ? "string" : "hash"] : data.map;
    }
    module2.exports = getMapData2;
  }
});

// node_modules/lodash/_mapCacheDelete.js
var require_mapCacheDelete = __commonJS({
  "node_modules/lodash/_mapCacheDelete.js"(exports2, module2) {
    var getMapData2 = require_getMapData();
    function mapCacheDelete2(key) {
      var result = getMapData2(this, key)["delete"](key);
      this.size -= result ? 1 : 0;
      return result;
    }
    module2.exports = mapCacheDelete2;
  }
});

// node_modules/lodash/_mapCacheGet.js
var require_mapCacheGet = __commonJS({
  "node_modules/lodash/_mapCacheGet.js"(exports2, module2) {
    var getMapData2 = require_getMapData();
    function mapCacheGet2(key) {
      return getMapData2(this, key).get(key);
    }
    module2.exports = mapCacheGet2;
  }
});

// node_modules/lodash/_mapCacheHas.js
var require_mapCacheHas = __commonJS({
  "node_modules/lodash/_mapCacheHas.js"(exports2, module2) {
    var getMapData2 = require_getMapData();
    function mapCacheHas2(key) {
      return getMapData2(this, key).has(key);
    }
    module2.exports = mapCacheHas2;
  }
});

// node_modules/lodash/_mapCacheSet.js
var require_mapCacheSet = __commonJS({
  "node_modules/lodash/_mapCacheSet.js"(exports2, module2) {
    var getMapData2 = require_getMapData();
    function mapCacheSet2(key, value) {
      var data = getMapData2(this, key), size = data.size;
      data.set(key, value);
      this.size += data.size == size ? 0 : 1;
      return this;
    }
    module2.exports = mapCacheSet2;
  }
});

// node_modules/lodash/_MapCache.js
var require_MapCache = __commonJS({
  "node_modules/lodash/_MapCache.js"(exports2, module2) {
    var mapCacheClear2 = require_mapCacheClear();
    var mapCacheDelete2 = require_mapCacheDelete();
    var mapCacheGet2 = require_mapCacheGet();
    var mapCacheHas2 = require_mapCacheHas();
    var mapCacheSet2 = require_mapCacheSet();
    function MapCache2(entries) {
      var index = -1, length = entries == null ? 0 : entries.length;
      this.clear();
      while (++index < length) {
        var entry = entries[index];
        this.set(entry[0], entry[1]);
      }
    }
    MapCache2.prototype.clear = mapCacheClear2;
    MapCache2.prototype["delete"] = mapCacheDelete2;
    MapCache2.prototype.get = mapCacheGet2;
    MapCache2.prototype.has = mapCacheHas2;
    MapCache2.prototype.set = mapCacheSet2;
    module2.exports = MapCache2;
  }
});

// node_modules/lodash/_stackSet.js
var require_stackSet = __commonJS({
  "node_modules/lodash/_stackSet.js"(exports2, module2) {
    var ListCache2 = require_ListCache();
    var Map3 = require_Map();
    var MapCache2 = require_MapCache();
    var LARGE_ARRAY_SIZE4 = 200;
    function stackSet2(key, value) {
      var data = this.__data__;
      if (data instanceof ListCache2) {
        var pairs = data.__data__;
        if (!Map3 || pairs.length < LARGE_ARRAY_SIZE4 - 1) {
          pairs.push([key, value]);
          this.size = ++data.size;
          return this;
        }
        data = this.__data__ = new MapCache2(pairs);
      }
      data.set(key, value);
      this.size = data.size;
      return this;
    }
    module2.exports = stackSet2;
  }
});

// node_modules/lodash/_Stack.js
var require_Stack = __commonJS({
  "node_modules/lodash/_Stack.js"(exports2, module2) {
    var ListCache2 = require_ListCache();
    var stackClear2 = require_stackClear();
    var stackDelete2 = require_stackDelete();
    var stackGet2 = require_stackGet();
    var stackHas2 = require_stackHas();
    var stackSet2 = require_stackSet();
    function Stack2(entries) {
      var data = this.__data__ = new ListCache2(entries);
      this.size = data.size;
    }
    Stack2.prototype.clear = stackClear2;
    Stack2.prototype["delete"] = stackDelete2;
    Stack2.prototype.get = stackGet2;
    Stack2.prototype.has = stackHas2;
    Stack2.prototype.set = stackSet2;
    module2.exports = Stack2;
  }
});

// node_modules/lodash/_arrayEach.js
var require_arrayEach = __commonJS({
  "node_modules/lodash/_arrayEach.js"(exports2, module2) {
    function arrayEach2(array, iteratee) {
      var index = -1, length = array == null ? 0 : array.length;
      while (++index < length) {
        if (iteratee(array[index], index, array) === false) {
          break;
        }
      }
      return array;
    }
    module2.exports = arrayEach2;
  }
});

// node_modules/lodash/_defineProperty.js
var require_defineProperty = __commonJS({
  "node_modules/lodash/_defineProperty.js"(exports2, module2) {
    var getNative2 = require_getNative();
    var defineProperty2 = function() {
      try {
        var func = getNative2(Object, "defineProperty");
        func({}, "", {});
        return func;
      } catch (e) {
      }
    }();
    module2.exports = defineProperty2;
  }
});

// node_modules/lodash/_baseAssignValue.js
var require_baseAssignValue = __commonJS({
  "node_modules/lodash/_baseAssignValue.js"(exports2, module2) {
    var defineProperty2 = require_defineProperty();
    function baseAssignValue2(object, key, value) {
      if (key == "__proto__" && defineProperty2) {
        defineProperty2(object, key, {
          "configurable": true,
          "enumerable": true,
          "value": value,
          "writable": true
        });
      } else {
        object[key] = value;
      }
    }
    module2.exports = baseAssignValue2;
  }
});

// node_modules/lodash/_assignValue.js
var require_assignValue = __commonJS({
  "node_modules/lodash/_assignValue.js"(exports2, module2) {
    var baseAssignValue2 = require_baseAssignValue();
    var eq2 = require_eq();
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function assignValue2(object, key, value) {
      var objValue = object[key];
      if (!(hasOwnProperty16.call(object, key) && eq2(objValue, value)) || value === void 0 && !(key in object)) {
        baseAssignValue2(object, key, value);
      }
    }
    module2.exports = assignValue2;
  }
});

// node_modules/lodash/_copyObject.js
var require_copyObject = __commonJS({
  "node_modules/lodash/_copyObject.js"(exports2, module2) {
    var assignValue2 = require_assignValue();
    var baseAssignValue2 = require_baseAssignValue();
    function copyObject2(source, props, object, customizer) {
      var isNew = !object;
      object || (object = {});
      var index = -1, length = props.length;
      while (++index < length) {
        var key = props[index];
        var newValue = customizer ? customizer(object[key], source[key], key, object, source) : void 0;
        if (newValue === void 0) {
          newValue = source[key];
        }
        if (isNew) {
          baseAssignValue2(object, key, newValue);
        } else {
          assignValue2(object, key, newValue);
        }
      }
      return object;
    }
    module2.exports = copyObject2;
  }
});

// node_modules/lodash/_baseTimes.js
var require_baseTimes = __commonJS({
  "node_modules/lodash/_baseTimes.js"(exports2, module2) {
    function baseTimes2(n, iteratee) {
      var index = -1, result = Array(n);
      while (++index < n) {
        result[index] = iteratee(index);
      }
      return result;
    }
    module2.exports = baseTimes2;
  }
});

// node_modules/lodash/isObjectLike.js
var require_isObjectLike = __commonJS({
  "node_modules/lodash/isObjectLike.js"(exports2, module2) {
    function isObjectLike2(value) {
      return value != null && typeof value == "object";
    }
    module2.exports = isObjectLike2;
  }
});

// node_modules/lodash/_baseIsArguments.js
var require_baseIsArguments = __commonJS({
  "node_modules/lodash/_baseIsArguments.js"(exports2, module2) {
    var baseGetTag2 = require_baseGetTag();
    var isObjectLike2 = require_isObjectLike();
    var argsTag5 = "[object Arguments]";
    function baseIsArguments2(value) {
      return isObjectLike2(value) && baseGetTag2(value) == argsTag5;
    }
    module2.exports = baseIsArguments2;
  }
});

// node_modules/lodash/isArguments.js
var require_isArguments = __commonJS({
  "node_modules/lodash/isArguments.js"(exports2, module2) {
    var baseIsArguments2 = require_baseIsArguments();
    var isObjectLike2 = require_isObjectLike();
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    var propertyIsEnumerable3 = objectProto19.propertyIsEnumerable;
    var isArguments2 = baseIsArguments2(/* @__PURE__ */ function() {
      return arguments;
    }()) ? baseIsArguments2 : function(value) {
      return isObjectLike2(value) && hasOwnProperty16.call(value, "callee") && !propertyIsEnumerable3.call(value, "callee");
    };
    module2.exports = isArguments2;
  }
});

// node_modules/lodash/isArray.js
var require_isArray = __commonJS({
  "node_modules/lodash/isArray.js"(exports2, module2) {
    var isArray2 = Array.isArray;
    module2.exports = isArray2;
  }
});

// node_modules/lodash/stubFalse.js
var require_stubFalse = __commonJS({
  "node_modules/lodash/stubFalse.js"(exports2, module2) {
    function stubFalse2() {
      return false;
    }
    module2.exports = stubFalse2;
  }
});

// node_modules/lodash/isBuffer.js
var require_isBuffer = __commonJS({
  "node_modules/lodash/isBuffer.js"(exports2, module2) {
    var root2 = require_root();
    var stubFalse2 = require_stubFalse();
    var freeExports4 = typeof exports2 == "object" && exports2 && !exports2.nodeType && exports2;
    var freeModule4 = freeExports4 && typeof module2 == "object" && module2 && !module2.nodeType && module2;
    var moduleExports4 = freeModule4 && freeModule4.exports === freeExports4;
    var Buffer3 = moduleExports4 ? root2.Buffer : void 0;
    var nativeIsBuffer2 = Buffer3 ? Buffer3.isBuffer : void 0;
    var isBuffer2 = nativeIsBuffer2 || stubFalse2;
    module2.exports = isBuffer2;
  }
});

// node_modules/lodash/_isIndex.js
var require_isIndex = __commonJS({
  "node_modules/lodash/_isIndex.js"(exports2, module2) {
    var MAX_SAFE_INTEGER4 = 9007199254740991;
    var reIsUint2 = /^(?:0|[1-9]\d*)$/;
    function isIndex2(value, length) {
      var type = typeof value;
      length = length == null ? MAX_SAFE_INTEGER4 : length;
      return !!length && (type == "number" || type != "symbol" && reIsUint2.test(value)) && (value > -1 && value % 1 == 0 && value < length);
    }
    module2.exports = isIndex2;
  }
});

// node_modules/lodash/isLength.js
var require_isLength = __commonJS({
  "node_modules/lodash/isLength.js"(exports2, module2) {
    var MAX_SAFE_INTEGER4 = 9007199254740991;
    function isLength2(value) {
      return typeof value == "number" && value > -1 && value % 1 == 0 && value <= MAX_SAFE_INTEGER4;
    }
    module2.exports = isLength2;
  }
});

// node_modules/lodash/_baseIsTypedArray.js
var require_baseIsTypedArray = __commonJS({
  "node_modules/lodash/_baseIsTypedArray.js"(exports2, module2) {
    var baseGetTag2 = require_baseGetTag();
    var isLength2 = require_isLength();
    var isObjectLike2 = require_isObjectLike();
    var argsTag5 = "[object Arguments]";
    var arrayTag4 = "[object Array]";
    var boolTag5 = "[object Boolean]";
    var dateTag5 = "[object Date]";
    var errorTag4 = "[object Error]";
    var funcTag4 = "[object Function]";
    var mapTag8 = "[object Map]";
    var numberTag6 = "[object Number]";
    var objectTag6 = "[object Object]";
    var regexpTag5 = "[object RegExp]";
    var setTag8 = "[object Set]";
    var stringTag6 = "[object String]";
    var weakMapTag4 = "[object WeakMap]";
    var arrayBufferTag5 = "[object ArrayBuffer]";
    var dataViewTag6 = "[object DataView]";
    var float32Tag4 = "[object Float32Array]";
    var float64Tag4 = "[object Float64Array]";
    var int8Tag4 = "[object Int8Array]";
    var int16Tag4 = "[object Int16Array]";
    var int32Tag4 = "[object Int32Array]";
    var uint8Tag4 = "[object Uint8Array]";
    var uint8ClampedTag4 = "[object Uint8ClampedArray]";
    var uint16Tag4 = "[object Uint16Array]";
    var uint32Tag4 = "[object Uint32Array]";
    var typedArrayTags2 = {};
    typedArrayTags2[float32Tag4] = typedArrayTags2[float64Tag4] = typedArrayTags2[int8Tag4] = typedArrayTags2[int16Tag4] = typedArrayTags2[int32Tag4] = typedArrayTags2[uint8Tag4] = typedArrayTags2[uint8ClampedTag4] = typedArrayTags2[uint16Tag4] = typedArrayTags2[uint32Tag4] = true;
    typedArrayTags2[argsTag5] = typedArrayTags2[arrayTag4] = typedArrayTags2[arrayBufferTag5] = typedArrayTags2[boolTag5] = typedArrayTags2[dataViewTag6] = typedArrayTags2[dateTag5] = typedArrayTags2[errorTag4] = typedArrayTags2[funcTag4] = typedArrayTags2[mapTag8] = typedArrayTags2[numberTag6] = typedArrayTags2[objectTag6] = typedArrayTags2[regexpTag5] = typedArrayTags2[setTag8] = typedArrayTags2[stringTag6] = typedArrayTags2[weakMapTag4] = false;
    function baseIsTypedArray2(value) {
      return isObjectLike2(value) && isLength2(value.length) && !!typedArrayTags2[baseGetTag2(value)];
    }
    module2.exports = baseIsTypedArray2;
  }
});

// node_modules/lodash/_baseUnary.js
var require_baseUnary = __commonJS({
  "node_modules/lodash/_baseUnary.js"(exports2, module2) {
    function baseUnary2(func) {
      return function(value) {
        return func(value);
      };
    }
    module2.exports = baseUnary2;
  }
});

// node_modules/lodash/_nodeUtil.js
var require_nodeUtil = __commonJS({
  "node_modules/lodash/_nodeUtil.js"(exports2, module2) {
    var freeGlobal2 = require_freeGlobal();
    var freeExports4 = typeof exports2 == "object" && exports2 && !exports2.nodeType && exports2;
    var freeModule4 = freeExports4 && typeof module2 == "object" && module2 && !module2.nodeType && module2;
    var moduleExports4 = freeModule4 && freeModule4.exports === freeExports4;
    var freeProcess2 = moduleExports4 && freeGlobal2.process;
    var nodeUtil2 = function() {
      try {
        var types = freeModule4 && freeModule4.require && freeModule4.require("util").types;
        if (types) {
          return types;
        }
        return freeProcess2 && freeProcess2.binding && freeProcess2.binding("util");
      } catch (e) {
      }
    }();
    module2.exports = nodeUtil2;
  }
});

// node_modules/lodash/isTypedArray.js
var require_isTypedArray = __commonJS({
  "node_modules/lodash/isTypedArray.js"(exports2, module2) {
    var baseIsTypedArray2 = require_baseIsTypedArray();
    var baseUnary2 = require_baseUnary();
    var nodeUtil2 = require_nodeUtil();
    var nodeIsTypedArray2 = nodeUtil2 && nodeUtil2.isTypedArray;
    var isTypedArray2 = nodeIsTypedArray2 ? baseUnary2(nodeIsTypedArray2) : baseIsTypedArray2;
    module2.exports = isTypedArray2;
  }
});

// node_modules/lodash/_arrayLikeKeys.js
var require_arrayLikeKeys = __commonJS({
  "node_modules/lodash/_arrayLikeKeys.js"(exports2, module2) {
    var baseTimes2 = require_baseTimes();
    var isArguments2 = require_isArguments();
    var isArray2 = require_isArray();
    var isBuffer2 = require_isBuffer();
    var isIndex2 = require_isIndex();
    var isTypedArray2 = require_isTypedArray();
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function arrayLikeKeys2(value, inherited) {
      var isArr = isArray2(value), isArg = !isArr && isArguments2(value), isBuff = !isArr && !isArg && isBuffer2(value), isType = !isArr && !isArg && !isBuff && isTypedArray2(value), skipIndexes = isArr || isArg || isBuff || isType, result = skipIndexes ? baseTimes2(value.length, String) : [], length = result.length;
      for (var key in value) {
        if ((inherited || hasOwnProperty16.call(value, key)) && !(skipIndexes && // Safari 9 has enumerable `arguments.length` in strict mode.
        (key == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
        isBuff && (key == "offset" || key == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
        isType && (key == "buffer" || key == "byteLength" || key == "byteOffset") || // Skip index properties.
        isIndex2(key, length)))) {
          result.push(key);
        }
      }
      return result;
    }
    module2.exports = arrayLikeKeys2;
  }
});

// node_modules/lodash/_isPrototype.js
var require_isPrototype = __commonJS({
  "node_modules/lodash/_isPrototype.js"(exports2, module2) {
    var objectProto19 = Object.prototype;
    function isPrototype2(value) {
      var Ctor = value && value.constructor, proto = typeof Ctor == "function" && Ctor.prototype || objectProto19;
      return value === proto;
    }
    module2.exports = isPrototype2;
  }
});

// node_modules/lodash/_overArg.js
var require_overArg = __commonJS({
  "node_modules/lodash/_overArg.js"(exports2, module2) {
    function overArg2(func, transform2) {
      return function(arg) {
        return func(transform2(arg));
      };
    }
    module2.exports = overArg2;
  }
});

// node_modules/lodash/_nativeKeys.js
var require_nativeKeys = __commonJS({
  "node_modules/lodash/_nativeKeys.js"(exports2, module2) {
    var overArg2 = require_overArg();
    var nativeKeys2 = overArg2(Object.keys, Object);
    module2.exports = nativeKeys2;
  }
});

// node_modules/lodash/_baseKeys.js
var require_baseKeys = __commonJS({
  "node_modules/lodash/_baseKeys.js"(exports2, module2) {
    var isPrototype2 = require_isPrototype();
    var nativeKeys2 = require_nativeKeys();
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function baseKeys2(object) {
      if (!isPrototype2(object)) {
        return nativeKeys2(object);
      }
      var result = [];
      for (var key in Object(object)) {
        if (hasOwnProperty16.call(object, key) && key != "constructor") {
          result.push(key);
        }
      }
      return result;
    }
    module2.exports = baseKeys2;
  }
});

// node_modules/lodash/isArrayLike.js
var require_isArrayLike = __commonJS({
  "node_modules/lodash/isArrayLike.js"(exports2, module2) {
    var isFunction2 = require_isFunction();
    var isLength2 = require_isLength();
    function isArrayLike2(value) {
      return value != null && isLength2(value.length) && !isFunction2(value);
    }
    module2.exports = isArrayLike2;
  }
});

// node_modules/lodash/keys.js
var require_keys = __commonJS({
  "node_modules/lodash/keys.js"(exports2, module2) {
    var arrayLikeKeys2 = require_arrayLikeKeys();
    var baseKeys2 = require_baseKeys();
    var isArrayLike2 = require_isArrayLike();
    function keys2(object) {
      return isArrayLike2(object) ? arrayLikeKeys2(object) : baseKeys2(object);
    }
    module2.exports = keys2;
  }
});

// node_modules/lodash/_baseAssign.js
var require_baseAssign = __commonJS({
  "node_modules/lodash/_baseAssign.js"(exports2, module2) {
    var copyObject2 = require_copyObject();
    var keys2 = require_keys();
    function baseAssign2(object, source) {
      return object && copyObject2(source, keys2(source), object);
    }
    module2.exports = baseAssign2;
  }
});

// node_modules/lodash/_nativeKeysIn.js
var require_nativeKeysIn = __commonJS({
  "node_modules/lodash/_nativeKeysIn.js"(exports2, module2) {
    function nativeKeysIn2(object) {
      var result = [];
      if (object != null) {
        for (var key in Object(object)) {
          result.push(key);
        }
      }
      return result;
    }
    module2.exports = nativeKeysIn2;
  }
});

// node_modules/lodash/_baseKeysIn.js
var require_baseKeysIn = __commonJS({
  "node_modules/lodash/_baseKeysIn.js"(exports2, module2) {
    var isObject3 = require_isObject();
    var isPrototype2 = require_isPrototype();
    var nativeKeysIn2 = require_nativeKeysIn();
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function baseKeysIn2(object) {
      if (!isObject3(object)) {
        return nativeKeysIn2(object);
      }
      var isProto = isPrototype2(object), result = [];
      for (var key in object) {
        if (!(key == "constructor" && (isProto || !hasOwnProperty16.call(object, key)))) {
          result.push(key);
        }
      }
      return result;
    }
    module2.exports = baseKeysIn2;
  }
});

// node_modules/lodash/keysIn.js
var require_keysIn = __commonJS({
  "node_modules/lodash/keysIn.js"(exports2, module2) {
    var arrayLikeKeys2 = require_arrayLikeKeys();
    var baseKeysIn2 = require_baseKeysIn();
    var isArrayLike2 = require_isArrayLike();
    function keysIn2(object) {
      return isArrayLike2(object) ? arrayLikeKeys2(object, true) : baseKeysIn2(object);
    }
    module2.exports = keysIn2;
  }
});

// node_modules/lodash/_baseAssignIn.js
var require_baseAssignIn = __commonJS({
  "node_modules/lodash/_baseAssignIn.js"(exports2, module2) {
    var copyObject2 = require_copyObject();
    var keysIn2 = require_keysIn();
    function baseAssignIn2(object, source) {
      return object && copyObject2(source, keysIn2(source), object);
    }
    module2.exports = baseAssignIn2;
  }
});

// node_modules/lodash/_cloneBuffer.js
var require_cloneBuffer = __commonJS({
  "node_modules/lodash/_cloneBuffer.js"(exports2, module2) {
    var root2 = require_root();
    var freeExports4 = typeof exports2 == "object" && exports2 && !exports2.nodeType && exports2;
    var freeModule4 = freeExports4 && typeof module2 == "object" && module2 && !module2.nodeType && module2;
    var moduleExports4 = freeModule4 && freeModule4.exports === freeExports4;
    var Buffer3 = moduleExports4 ? root2.Buffer : void 0;
    var allocUnsafe2 = Buffer3 ? Buffer3.allocUnsafe : void 0;
    function cloneBuffer2(buffer, isDeep) {
      if (isDeep) {
        return buffer.slice();
      }
      var length = buffer.length, result = allocUnsafe2 ? allocUnsafe2(length) : new buffer.constructor(length);
      buffer.copy(result);
      return result;
    }
    module2.exports = cloneBuffer2;
  }
});

// node_modules/lodash/_copyArray.js
var require_copyArray = __commonJS({
  "node_modules/lodash/_copyArray.js"(exports2, module2) {
    function copyArray2(source, array) {
      var index = -1, length = source.length;
      array || (array = Array(length));
      while (++index < length) {
        array[index] = source[index];
      }
      return array;
    }
    module2.exports = copyArray2;
  }
});

// node_modules/lodash/_arrayFilter.js
var require_arrayFilter = __commonJS({
  "node_modules/lodash/_arrayFilter.js"(exports2, module2) {
    function arrayFilter2(array, predicate) {
      var index = -1, length = array == null ? 0 : array.length, resIndex = 0, result = [];
      while (++index < length) {
        var value = array[index];
        if (predicate(value, index, array)) {
          result[resIndex++] = value;
        }
      }
      return result;
    }
    module2.exports = arrayFilter2;
  }
});

// node_modules/lodash/stubArray.js
var require_stubArray = __commonJS({
  "node_modules/lodash/stubArray.js"(exports2, module2) {
    function stubArray2() {
      return [];
    }
    module2.exports = stubArray2;
  }
});

// node_modules/lodash/_getSymbols.js
var require_getSymbols = __commonJS({
  "node_modules/lodash/_getSymbols.js"(exports2, module2) {
    var arrayFilter2 = require_arrayFilter();
    var stubArray2 = require_stubArray();
    var objectProto19 = Object.prototype;
    var propertyIsEnumerable3 = objectProto19.propertyIsEnumerable;
    var nativeGetSymbols3 = Object.getOwnPropertySymbols;
    var getSymbols2 = !nativeGetSymbols3 ? stubArray2 : function(object) {
      if (object == null) {
        return [];
      }
      object = Object(object);
      return arrayFilter2(nativeGetSymbols3(object), function(symbol) {
        return propertyIsEnumerable3.call(object, symbol);
      });
    };
    module2.exports = getSymbols2;
  }
});

// node_modules/lodash/_copySymbols.js
var require_copySymbols = __commonJS({
  "node_modules/lodash/_copySymbols.js"(exports2, module2) {
    var copyObject2 = require_copyObject();
    var getSymbols2 = require_getSymbols();
    function copySymbols2(source, object) {
      return copyObject2(source, getSymbols2(source), object);
    }
    module2.exports = copySymbols2;
  }
});

// node_modules/lodash/_arrayPush.js
var require_arrayPush = __commonJS({
  "node_modules/lodash/_arrayPush.js"(exports2, module2) {
    function arrayPush2(array, values) {
      var index = -1, length = values.length, offset = array.length;
      while (++index < length) {
        array[offset + index] = values[index];
      }
      return array;
    }
    module2.exports = arrayPush2;
  }
});

// node_modules/lodash/_getPrototype.js
var require_getPrototype = __commonJS({
  "node_modules/lodash/_getPrototype.js"(exports2, module2) {
    var overArg2 = require_overArg();
    var getPrototype2 = overArg2(Object.getPrototypeOf, Object);
    module2.exports = getPrototype2;
  }
});

// node_modules/lodash/_getSymbolsIn.js
var require_getSymbolsIn = __commonJS({
  "node_modules/lodash/_getSymbolsIn.js"(exports2, module2) {
    var arrayPush2 = require_arrayPush();
    var getPrototype2 = require_getPrototype();
    var getSymbols2 = require_getSymbols();
    var stubArray2 = require_stubArray();
    var nativeGetSymbols3 = Object.getOwnPropertySymbols;
    var getSymbolsIn2 = !nativeGetSymbols3 ? stubArray2 : function(object) {
      var result = [];
      while (object) {
        arrayPush2(result, getSymbols2(object));
        object = getPrototype2(object);
      }
      return result;
    };
    module2.exports = getSymbolsIn2;
  }
});

// node_modules/lodash/_copySymbolsIn.js
var require_copySymbolsIn = __commonJS({
  "node_modules/lodash/_copySymbolsIn.js"(exports2, module2) {
    var copyObject2 = require_copyObject();
    var getSymbolsIn2 = require_getSymbolsIn();
    function copySymbolsIn2(source, object) {
      return copyObject2(source, getSymbolsIn2(source), object);
    }
    module2.exports = copySymbolsIn2;
  }
});

// node_modules/lodash/_baseGetAllKeys.js
var require_baseGetAllKeys = __commonJS({
  "node_modules/lodash/_baseGetAllKeys.js"(exports2, module2) {
    var arrayPush2 = require_arrayPush();
    var isArray2 = require_isArray();
    function baseGetAllKeys2(object, keysFunc, symbolsFunc) {
      var result = keysFunc(object);
      return isArray2(object) ? result : arrayPush2(result, symbolsFunc(object));
    }
    module2.exports = baseGetAllKeys2;
  }
});

// node_modules/lodash/_getAllKeys.js
var require_getAllKeys = __commonJS({
  "node_modules/lodash/_getAllKeys.js"(exports2, module2) {
    var baseGetAllKeys2 = require_baseGetAllKeys();
    var getSymbols2 = require_getSymbols();
    var keys2 = require_keys();
    function getAllKeys2(object) {
      return baseGetAllKeys2(object, keys2, getSymbols2);
    }
    module2.exports = getAllKeys2;
  }
});

// node_modules/lodash/_getAllKeysIn.js
var require_getAllKeysIn = __commonJS({
  "node_modules/lodash/_getAllKeysIn.js"(exports2, module2) {
    var baseGetAllKeys2 = require_baseGetAllKeys();
    var getSymbolsIn2 = require_getSymbolsIn();
    var keysIn2 = require_keysIn();
    function getAllKeysIn2(object) {
      return baseGetAllKeys2(object, keysIn2, getSymbolsIn2);
    }
    module2.exports = getAllKeysIn2;
  }
});

// node_modules/lodash/_DataView.js
var require_DataView = __commonJS({
  "node_modules/lodash/_DataView.js"(exports2, module2) {
    var getNative2 = require_getNative();
    var root2 = require_root();
    var DataView2 = getNative2(root2, "DataView");
    module2.exports = DataView2;
  }
});

// node_modules/lodash/_Promise.js
var require_Promise = __commonJS({
  "node_modules/lodash/_Promise.js"(exports2, module2) {
    var getNative2 = require_getNative();
    var root2 = require_root();
    var Promise3 = getNative2(root2, "Promise");
    module2.exports = Promise3;
  }
});

// node_modules/lodash/_Set.js
var require_Set = __commonJS({
  "node_modules/lodash/_Set.js"(exports2, module2) {
    var getNative2 = require_getNative();
    var root2 = require_root();
    var Set3 = getNative2(root2, "Set");
    module2.exports = Set3;
  }
});

// node_modules/lodash/_WeakMap.js
var require_WeakMap = __commonJS({
  "node_modules/lodash/_WeakMap.js"(exports2, module2) {
    var getNative2 = require_getNative();
    var root2 = require_root();
    var WeakMap2 = getNative2(root2, "WeakMap");
    module2.exports = WeakMap2;
  }
});

// node_modules/lodash/_getTag.js
var require_getTag = __commonJS({
  "node_modules/lodash/_getTag.js"(exports2, module2) {
    var DataView2 = require_DataView();
    var Map3 = require_Map();
    var Promise3 = require_Promise();
    var Set3 = require_Set();
    var WeakMap2 = require_WeakMap();
    var baseGetTag2 = require_baseGetTag();
    var toSource2 = require_toSource();
    var mapTag8 = "[object Map]";
    var objectTag6 = "[object Object]";
    var promiseTag2 = "[object Promise]";
    var setTag8 = "[object Set]";
    var weakMapTag4 = "[object WeakMap]";
    var dataViewTag6 = "[object DataView]";
    var dataViewCtorString2 = toSource2(DataView2);
    var mapCtorString2 = toSource2(Map3);
    var promiseCtorString2 = toSource2(Promise3);
    var setCtorString2 = toSource2(Set3);
    var weakMapCtorString2 = toSource2(WeakMap2);
    var getTag2 = baseGetTag2;
    if (DataView2 && getTag2(new DataView2(new ArrayBuffer(1))) != dataViewTag6 || Map3 && getTag2(new Map3()) != mapTag8 || Promise3 && getTag2(Promise3.resolve()) != promiseTag2 || Set3 && getTag2(new Set3()) != setTag8 || WeakMap2 && getTag2(new WeakMap2()) != weakMapTag4) {
      getTag2 = function(value) {
        var result = baseGetTag2(value), Ctor = result == objectTag6 ? value.constructor : void 0, ctorString = Ctor ? toSource2(Ctor) : "";
        if (ctorString) {
          switch (ctorString) {
            case dataViewCtorString2:
              return dataViewTag6;
            case mapCtorString2:
              return mapTag8;
            case promiseCtorString2:
              return promiseTag2;
            case setCtorString2:
              return setTag8;
            case weakMapCtorString2:
              return weakMapTag4;
          }
        }
        return result;
      };
    }
    module2.exports = getTag2;
  }
});

// node_modules/lodash/_initCloneArray.js
var require_initCloneArray = __commonJS({
  "node_modules/lodash/_initCloneArray.js"(exports2, module2) {
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function initCloneArray2(array) {
      var length = array.length, result = new array.constructor(length);
      if (length && typeof array[0] == "string" && hasOwnProperty16.call(array, "index")) {
        result.index = array.index;
        result.input = array.input;
      }
      return result;
    }
    module2.exports = initCloneArray2;
  }
});

// node_modules/lodash/_Uint8Array.js
var require_Uint8Array = __commonJS({
  "node_modules/lodash/_Uint8Array.js"(exports2, module2) {
    var root2 = require_root();
    var Uint8Array3 = root2.Uint8Array;
    module2.exports = Uint8Array3;
  }
});

// node_modules/lodash/_cloneArrayBuffer.js
var require_cloneArrayBuffer = __commonJS({
  "node_modules/lodash/_cloneArrayBuffer.js"(exports2, module2) {
    var Uint8Array3 = require_Uint8Array();
    function cloneArrayBuffer2(arrayBuffer) {
      var result = new arrayBuffer.constructor(arrayBuffer.byteLength);
      new Uint8Array3(result).set(new Uint8Array3(arrayBuffer));
      return result;
    }
    module2.exports = cloneArrayBuffer2;
  }
});

// node_modules/lodash/_cloneDataView.js
var require_cloneDataView = __commonJS({
  "node_modules/lodash/_cloneDataView.js"(exports2, module2) {
    var cloneArrayBuffer2 = require_cloneArrayBuffer();
    function cloneDataView2(dataView, isDeep) {
      var buffer = isDeep ? cloneArrayBuffer2(dataView.buffer) : dataView.buffer;
      return new dataView.constructor(buffer, dataView.byteOffset, dataView.byteLength);
    }
    module2.exports = cloneDataView2;
  }
});

// node_modules/lodash/_cloneRegExp.js
var require_cloneRegExp = __commonJS({
  "node_modules/lodash/_cloneRegExp.js"(exports2, module2) {
    var reFlags2 = /\w*$/;
    function cloneRegExp2(regexp) {
      var result = new regexp.constructor(regexp.source, reFlags2.exec(regexp));
      result.lastIndex = regexp.lastIndex;
      return result;
    }
    module2.exports = cloneRegExp2;
  }
});

// node_modules/lodash/_cloneSymbol.js
var require_cloneSymbol = __commonJS({
  "node_modules/lodash/_cloneSymbol.js"(exports2, module2) {
    var Symbol3 = require_Symbol();
    var symbolProto4 = Symbol3 ? Symbol3.prototype : void 0;
    var symbolValueOf3 = symbolProto4 ? symbolProto4.valueOf : void 0;
    function cloneSymbol2(symbol) {
      return symbolValueOf3 ? Object(symbolValueOf3.call(symbol)) : {};
    }
    module2.exports = cloneSymbol2;
  }
});

// node_modules/lodash/_cloneTypedArray.js
var require_cloneTypedArray = __commonJS({
  "node_modules/lodash/_cloneTypedArray.js"(exports2, module2) {
    var cloneArrayBuffer2 = require_cloneArrayBuffer();
    function cloneTypedArray2(typedArray, isDeep) {
      var buffer = isDeep ? cloneArrayBuffer2(typedArray.buffer) : typedArray.buffer;
      return new typedArray.constructor(buffer, typedArray.byteOffset, typedArray.length);
    }
    module2.exports = cloneTypedArray2;
  }
});

// node_modules/lodash/_initCloneByTag.js
var require_initCloneByTag = __commonJS({
  "node_modules/lodash/_initCloneByTag.js"(exports2, module2) {
    var cloneArrayBuffer2 = require_cloneArrayBuffer();
    var cloneDataView2 = require_cloneDataView();
    var cloneRegExp2 = require_cloneRegExp();
    var cloneSymbol2 = require_cloneSymbol();
    var cloneTypedArray2 = require_cloneTypedArray();
    var boolTag5 = "[object Boolean]";
    var dateTag5 = "[object Date]";
    var mapTag8 = "[object Map]";
    var numberTag6 = "[object Number]";
    var regexpTag5 = "[object RegExp]";
    var setTag8 = "[object Set]";
    var stringTag6 = "[object String]";
    var symbolTag5 = "[object Symbol]";
    var arrayBufferTag5 = "[object ArrayBuffer]";
    var dataViewTag6 = "[object DataView]";
    var float32Tag4 = "[object Float32Array]";
    var float64Tag4 = "[object Float64Array]";
    var int8Tag4 = "[object Int8Array]";
    var int16Tag4 = "[object Int16Array]";
    var int32Tag4 = "[object Int32Array]";
    var uint8Tag4 = "[object Uint8Array]";
    var uint8ClampedTag4 = "[object Uint8ClampedArray]";
    var uint16Tag4 = "[object Uint16Array]";
    var uint32Tag4 = "[object Uint32Array]";
    function initCloneByTag2(object, tag, isDeep) {
      var Ctor = object.constructor;
      switch (tag) {
        case arrayBufferTag5:
          return cloneArrayBuffer2(object);
        case boolTag5:
        case dateTag5:
          return new Ctor(+object);
        case dataViewTag6:
          return cloneDataView2(object, isDeep);
        case float32Tag4:
        case float64Tag4:
        case int8Tag4:
        case int16Tag4:
        case int32Tag4:
        case uint8Tag4:
        case uint8ClampedTag4:
        case uint16Tag4:
        case uint32Tag4:
          return cloneTypedArray2(object, isDeep);
        case mapTag8:
          return new Ctor();
        case numberTag6:
        case stringTag6:
          return new Ctor(object);
        case regexpTag5:
          return cloneRegExp2(object);
        case setTag8:
          return new Ctor();
        case symbolTag5:
          return cloneSymbol2(object);
      }
    }
    module2.exports = initCloneByTag2;
  }
});

// node_modules/lodash/_baseCreate.js
var require_baseCreate = __commonJS({
  "node_modules/lodash/_baseCreate.js"(exports2, module2) {
    var isObject3 = require_isObject();
    var objectCreate2 = Object.create;
    var baseCreate2 = /* @__PURE__ */ function() {
      function object() {
      }
      return function(proto) {
        if (!isObject3(proto)) {
          return {};
        }
        if (objectCreate2) {
          return objectCreate2(proto);
        }
        object.prototype = proto;
        var result = new object();
        object.prototype = void 0;
        return result;
      };
    }();
    module2.exports = baseCreate2;
  }
});

// node_modules/lodash/_initCloneObject.js
var require_initCloneObject = __commonJS({
  "node_modules/lodash/_initCloneObject.js"(exports2, module2) {
    var baseCreate2 = require_baseCreate();
    var getPrototype2 = require_getPrototype();
    var isPrototype2 = require_isPrototype();
    function initCloneObject2(object) {
      return typeof object.constructor == "function" && !isPrototype2(object) ? baseCreate2(getPrototype2(object)) : {};
    }
    module2.exports = initCloneObject2;
  }
});

// node_modules/lodash/_baseIsMap.js
var require_baseIsMap = __commonJS({
  "node_modules/lodash/_baseIsMap.js"(exports2, module2) {
    var getTag2 = require_getTag();
    var isObjectLike2 = require_isObjectLike();
    var mapTag8 = "[object Map]";
    function baseIsMap2(value) {
      return isObjectLike2(value) && getTag2(value) == mapTag8;
    }
    module2.exports = baseIsMap2;
  }
});

// node_modules/lodash/isMap.js
var require_isMap = __commonJS({
  "node_modules/lodash/isMap.js"(exports2, module2) {
    var baseIsMap2 = require_baseIsMap();
    var baseUnary2 = require_baseUnary();
    var nodeUtil2 = require_nodeUtil();
    var nodeIsMap2 = nodeUtil2 && nodeUtil2.isMap;
    var isMap2 = nodeIsMap2 ? baseUnary2(nodeIsMap2) : baseIsMap2;
    module2.exports = isMap2;
  }
});

// node_modules/lodash/_baseIsSet.js
var require_baseIsSet = __commonJS({
  "node_modules/lodash/_baseIsSet.js"(exports2, module2) {
    var getTag2 = require_getTag();
    var isObjectLike2 = require_isObjectLike();
    var setTag8 = "[object Set]";
    function baseIsSet2(value) {
      return isObjectLike2(value) && getTag2(value) == setTag8;
    }
    module2.exports = baseIsSet2;
  }
});

// node_modules/lodash/isSet.js
var require_isSet = __commonJS({
  "node_modules/lodash/isSet.js"(exports2, module2) {
    var baseIsSet2 = require_baseIsSet();
    var baseUnary2 = require_baseUnary();
    var nodeUtil2 = require_nodeUtil();
    var nodeIsSet2 = nodeUtil2 && nodeUtil2.isSet;
    var isSet2 = nodeIsSet2 ? baseUnary2(nodeIsSet2) : baseIsSet2;
    module2.exports = isSet2;
  }
});

// node_modules/lodash/_baseClone.js
var require_baseClone = __commonJS({
  "node_modules/lodash/_baseClone.js"(exports2, module2) {
    var Stack2 = require_Stack();
    var arrayEach2 = require_arrayEach();
    var assignValue2 = require_assignValue();
    var baseAssign2 = require_baseAssign();
    var baseAssignIn2 = require_baseAssignIn();
    var cloneBuffer2 = require_cloneBuffer();
    var copyArray2 = require_copyArray();
    var copySymbols2 = require_copySymbols();
    var copySymbolsIn2 = require_copySymbolsIn();
    var getAllKeys2 = require_getAllKeys();
    var getAllKeysIn2 = require_getAllKeysIn();
    var getTag2 = require_getTag();
    var initCloneArray2 = require_initCloneArray();
    var initCloneByTag2 = require_initCloneByTag();
    var initCloneObject2 = require_initCloneObject();
    var isArray2 = require_isArray();
    var isBuffer2 = require_isBuffer();
    var isMap2 = require_isMap();
    var isObject3 = require_isObject();
    var isSet2 = require_isSet();
    var keys2 = require_keys();
    var keysIn2 = require_keysIn();
    var CLONE_DEEP_FLAG4 = 1;
    var CLONE_FLAT_FLAG3 = 2;
    var CLONE_SYMBOLS_FLAG4 = 4;
    var argsTag5 = "[object Arguments]";
    var arrayTag4 = "[object Array]";
    var boolTag5 = "[object Boolean]";
    var dateTag5 = "[object Date]";
    var errorTag4 = "[object Error]";
    var funcTag4 = "[object Function]";
    var genTag3 = "[object GeneratorFunction]";
    var mapTag8 = "[object Map]";
    var numberTag6 = "[object Number]";
    var objectTag6 = "[object Object]";
    var regexpTag5 = "[object RegExp]";
    var setTag8 = "[object Set]";
    var stringTag6 = "[object String]";
    var symbolTag5 = "[object Symbol]";
    var weakMapTag4 = "[object WeakMap]";
    var arrayBufferTag5 = "[object ArrayBuffer]";
    var dataViewTag6 = "[object DataView]";
    var float32Tag4 = "[object Float32Array]";
    var float64Tag4 = "[object Float64Array]";
    var int8Tag4 = "[object Int8Array]";
    var int16Tag4 = "[object Int16Array]";
    var int32Tag4 = "[object Int32Array]";
    var uint8Tag4 = "[object Uint8Array]";
    var uint8ClampedTag4 = "[object Uint8ClampedArray]";
    var uint16Tag4 = "[object Uint16Array]";
    var uint32Tag4 = "[object Uint32Array]";
    var cloneableTags2 = {};
    cloneableTags2[argsTag5] = cloneableTags2[arrayTag4] = cloneableTags2[arrayBufferTag5] = cloneableTags2[dataViewTag6] = cloneableTags2[boolTag5] = cloneableTags2[dateTag5] = cloneableTags2[float32Tag4] = cloneableTags2[float64Tag4] = cloneableTags2[int8Tag4] = cloneableTags2[int16Tag4] = cloneableTags2[int32Tag4] = cloneableTags2[mapTag8] = cloneableTags2[numberTag6] = cloneableTags2[objectTag6] = cloneableTags2[regexpTag5] = cloneableTags2[setTag8] = cloneableTags2[stringTag6] = cloneableTags2[symbolTag5] = cloneableTags2[uint8Tag4] = cloneableTags2[uint8ClampedTag4] = cloneableTags2[uint16Tag4] = cloneableTags2[uint32Tag4] = true;
    cloneableTags2[errorTag4] = cloneableTags2[funcTag4] = cloneableTags2[weakMapTag4] = false;
    function baseClone2(value, bitmask, customizer, key, object, stack) {
      var result, isDeep = bitmask & CLONE_DEEP_FLAG4, isFlat = bitmask & CLONE_FLAT_FLAG3, isFull = bitmask & CLONE_SYMBOLS_FLAG4;
      if (customizer) {
        result = object ? customizer(value, key, object, stack) : customizer(value);
      }
      if (result !== void 0) {
        return result;
      }
      if (!isObject3(value)) {
        return value;
      }
      var isArr = isArray2(value);
      if (isArr) {
        result = initCloneArray2(value);
        if (!isDeep) {
          return copyArray2(value, result);
        }
      } else {
        var tag = getTag2(value), isFunc = tag == funcTag4 || tag == genTag3;
        if (isBuffer2(value)) {
          return cloneBuffer2(value, isDeep);
        }
        if (tag == objectTag6 || tag == argsTag5 || isFunc && !object) {
          result = isFlat || isFunc ? {} : initCloneObject2(value);
          if (!isDeep) {
            return isFlat ? copySymbolsIn2(value, baseAssignIn2(result, value)) : copySymbols2(value, baseAssign2(result, value));
          }
        } else {
          if (!cloneableTags2[tag]) {
            return object ? value : {};
          }
          result = initCloneByTag2(value, tag, isDeep);
        }
      }
      stack || (stack = new Stack2());
      var stacked = stack.get(value);
      if (stacked) {
        return stacked;
      }
      stack.set(value, result);
      if (isSet2(value)) {
        value.forEach(function(subValue) {
          result.add(baseClone2(subValue, bitmask, customizer, subValue, value, stack));
        });
      } else if (isMap2(value)) {
        value.forEach(function(subValue, key2) {
          result.set(key2, baseClone2(subValue, bitmask, customizer, key2, value, stack));
        });
      }
      var keysFunc = isFull ? isFlat ? getAllKeysIn2 : getAllKeys2 : isFlat ? keysIn2 : keys2;
      var props = isArr ? void 0 : keysFunc(value);
      arrayEach2(props || value, function(subValue, key2) {
        if (props) {
          key2 = subValue;
          subValue = value[key2];
        }
        assignValue2(result, key2, baseClone2(subValue, bitmask, customizer, key2, value, stack));
      });
      return result;
    }
    module2.exports = baseClone2;
  }
});

// node_modules/lodash/cloneDeep.js
var require_cloneDeep = __commonJS({
  "node_modules/lodash/cloneDeep.js"(exports2, module2) {
    var baseClone2 = require_baseClone();
    var CLONE_DEEP_FLAG4 = 1;
    var CLONE_SYMBOLS_FLAG4 = 4;
    function cloneDeep2(value) {
      return baseClone2(value, CLONE_DEEP_FLAG4 | CLONE_SYMBOLS_FLAG4);
    }
    module2.exports = cloneDeep2;
  }
});

// node_modules/lodash/_setCacheAdd.js
var require_setCacheAdd = __commonJS({
  "node_modules/lodash/_setCacheAdd.js"(exports2, module2) {
    var HASH_UNDEFINED4 = "__lodash_hash_undefined__";
    function setCacheAdd2(value) {
      this.__data__.set(value, HASH_UNDEFINED4);
      return this;
    }
    module2.exports = setCacheAdd2;
  }
});

// node_modules/lodash/_setCacheHas.js
var require_setCacheHas = __commonJS({
  "node_modules/lodash/_setCacheHas.js"(exports2, module2) {
    function setCacheHas2(value) {
      return this.__data__.has(value);
    }
    module2.exports = setCacheHas2;
  }
});

// node_modules/lodash/_SetCache.js
var require_SetCache = __commonJS({
  "node_modules/lodash/_SetCache.js"(exports2, module2) {
    var MapCache2 = require_MapCache();
    var setCacheAdd2 = require_setCacheAdd();
    var setCacheHas2 = require_setCacheHas();
    function SetCache2(values) {
      var index = -1, length = values == null ? 0 : values.length;
      this.__data__ = new MapCache2();
      while (++index < length) {
        this.add(values[index]);
      }
    }
    SetCache2.prototype.add = SetCache2.prototype.push = setCacheAdd2;
    SetCache2.prototype.has = setCacheHas2;
    module2.exports = SetCache2;
  }
});

// node_modules/lodash/_arraySome.js
var require_arraySome = __commonJS({
  "node_modules/lodash/_arraySome.js"(exports2, module2) {
    function arraySome2(array, predicate) {
      var index = -1, length = array == null ? 0 : array.length;
      while (++index < length) {
        if (predicate(array[index], index, array)) {
          return true;
        }
      }
      return false;
    }
    module2.exports = arraySome2;
  }
});

// node_modules/lodash/_cacheHas.js
var require_cacheHas = __commonJS({
  "node_modules/lodash/_cacheHas.js"(exports2, module2) {
    function cacheHas2(cache, key) {
      return cache.has(key);
    }
    module2.exports = cacheHas2;
  }
});

// node_modules/lodash/_equalArrays.js
var require_equalArrays = __commonJS({
  "node_modules/lodash/_equalArrays.js"(exports2, module2) {
    var SetCache2 = require_SetCache();
    var arraySome2 = require_arraySome();
    var cacheHas2 = require_cacheHas();
    var COMPARE_PARTIAL_FLAG7 = 1;
    var COMPARE_UNORDERED_FLAG5 = 2;
    function equalArrays2(array, other, bitmask, customizer, equalFunc, stack) {
      var isPartial = bitmask & COMPARE_PARTIAL_FLAG7, arrLength = array.length, othLength = other.length;
      if (arrLength != othLength && !(isPartial && othLength > arrLength)) {
        return false;
      }
      var arrStacked = stack.get(array);
      var othStacked = stack.get(other);
      if (arrStacked && othStacked) {
        return arrStacked == other && othStacked == array;
      }
      var index = -1, result = true, seen = bitmask & COMPARE_UNORDERED_FLAG5 ? new SetCache2() : void 0;
      stack.set(array, other);
      stack.set(other, array);
      while (++index < arrLength) {
        var arrValue = array[index], othValue = other[index];
        if (customizer) {
          var compared = isPartial ? customizer(othValue, arrValue, index, other, array, stack) : customizer(arrValue, othValue, index, array, other, stack);
        }
        if (compared !== void 0) {
          if (compared) {
            continue;
          }
          result = false;
          break;
        }
        if (seen) {
          if (!arraySome2(other, function(othValue2, othIndex) {
            if (!cacheHas2(seen, othIndex) && (arrValue === othValue2 || equalFunc(arrValue, othValue2, bitmask, customizer, stack))) {
              return seen.push(othIndex);
            }
          })) {
            result = false;
            break;
          }
        } else if (!(arrValue === othValue || equalFunc(arrValue, othValue, bitmask, customizer, stack))) {
          result = false;
          break;
        }
      }
      stack["delete"](array);
      stack["delete"](other);
      return result;
    }
    module2.exports = equalArrays2;
  }
});

// node_modules/lodash/_mapToArray.js
var require_mapToArray = __commonJS({
  "node_modules/lodash/_mapToArray.js"(exports2, module2) {
    function mapToArray2(map) {
      var index = -1, result = Array(map.size);
      map.forEach(function(value, key) {
        result[++index] = [key, value];
      });
      return result;
    }
    module2.exports = mapToArray2;
  }
});

// node_modules/lodash/_setToArray.js
var require_setToArray = __commonJS({
  "node_modules/lodash/_setToArray.js"(exports2, module2) {
    function setToArray2(set2) {
      var index = -1, result = Array(set2.size);
      set2.forEach(function(value) {
        result[++index] = value;
      });
      return result;
    }
    module2.exports = setToArray2;
  }
});

// node_modules/lodash/_equalByTag.js
var require_equalByTag = __commonJS({
  "node_modules/lodash/_equalByTag.js"(exports2, module2) {
    var Symbol3 = require_Symbol();
    var Uint8Array3 = require_Uint8Array();
    var eq2 = require_eq();
    var equalArrays2 = require_equalArrays();
    var mapToArray2 = require_mapToArray();
    var setToArray2 = require_setToArray();
    var COMPARE_PARTIAL_FLAG7 = 1;
    var COMPARE_UNORDERED_FLAG5 = 2;
    var boolTag5 = "[object Boolean]";
    var dateTag5 = "[object Date]";
    var errorTag4 = "[object Error]";
    var mapTag8 = "[object Map]";
    var numberTag6 = "[object Number]";
    var regexpTag5 = "[object RegExp]";
    var setTag8 = "[object Set]";
    var stringTag6 = "[object String]";
    var symbolTag5 = "[object Symbol]";
    var arrayBufferTag5 = "[object ArrayBuffer]";
    var dataViewTag6 = "[object DataView]";
    var symbolProto4 = Symbol3 ? Symbol3.prototype : void 0;
    var symbolValueOf3 = symbolProto4 ? symbolProto4.valueOf : void 0;
    function equalByTag2(object, other, tag, bitmask, customizer, equalFunc, stack) {
      switch (tag) {
        case dataViewTag6:
          if (object.byteLength != other.byteLength || object.byteOffset != other.byteOffset) {
            return false;
          }
          object = object.buffer;
          other = other.buffer;
        case arrayBufferTag5:
          if (object.byteLength != other.byteLength || !equalFunc(new Uint8Array3(object), new Uint8Array3(other))) {
            return false;
          }
          return true;
        case boolTag5:
        case dateTag5:
        case numberTag6:
          return eq2(+object, +other);
        case errorTag4:
          return object.name == other.name && object.message == other.message;
        case regexpTag5:
        case stringTag6:
          return object == other + "";
        case mapTag8:
          var convert = mapToArray2;
        case setTag8:
          var isPartial = bitmask & COMPARE_PARTIAL_FLAG7;
          convert || (convert = setToArray2);
          if (object.size != other.size && !isPartial) {
            return false;
          }
          var stacked = stack.get(object);
          if (stacked) {
            return stacked == other;
          }
          bitmask |= COMPARE_UNORDERED_FLAG5;
          stack.set(object, other);
          var result = equalArrays2(convert(object), convert(other), bitmask, customizer, equalFunc, stack);
          stack["delete"](object);
          return result;
        case symbolTag5:
          if (symbolValueOf3) {
            return symbolValueOf3.call(object) == symbolValueOf3.call(other);
          }
      }
      return false;
    }
    module2.exports = equalByTag2;
  }
});

// node_modules/lodash/_equalObjects.js
var require_equalObjects = __commonJS({
  "node_modules/lodash/_equalObjects.js"(exports2, module2) {
    var getAllKeys2 = require_getAllKeys();
    var COMPARE_PARTIAL_FLAG7 = 1;
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function equalObjects2(object, other, bitmask, customizer, equalFunc, stack) {
      var isPartial = bitmask & COMPARE_PARTIAL_FLAG7, objProps = getAllKeys2(object), objLength = objProps.length, othProps = getAllKeys2(other), othLength = othProps.length;
      if (objLength != othLength && !isPartial) {
        return false;
      }
      var index = objLength;
      while (index--) {
        var key = objProps[index];
        if (!(isPartial ? key in other : hasOwnProperty16.call(other, key))) {
          return false;
        }
      }
      var objStacked = stack.get(object);
      var othStacked = stack.get(other);
      if (objStacked && othStacked) {
        return objStacked == other && othStacked == object;
      }
      var result = true;
      stack.set(object, other);
      stack.set(other, object);
      var skipCtor = isPartial;
      while (++index < objLength) {
        key = objProps[index];
        var objValue = object[key], othValue = other[key];
        if (customizer) {
          var compared = isPartial ? customizer(othValue, objValue, key, other, object, stack) : customizer(objValue, othValue, key, object, other, stack);
        }
        if (!(compared === void 0 ? objValue === othValue || equalFunc(objValue, othValue, bitmask, customizer, stack) : compared)) {
          result = false;
          break;
        }
        skipCtor || (skipCtor = key == "constructor");
      }
      if (result && !skipCtor) {
        var objCtor = object.constructor, othCtor = other.constructor;
        if (objCtor != othCtor && ("constructor" in object && "constructor" in other) && !(typeof objCtor == "function" && objCtor instanceof objCtor && typeof othCtor == "function" && othCtor instanceof othCtor)) {
          result = false;
        }
      }
      stack["delete"](object);
      stack["delete"](other);
      return result;
    }
    module2.exports = equalObjects2;
  }
});

// node_modules/lodash/_baseIsEqualDeep.js
var require_baseIsEqualDeep = __commonJS({
  "node_modules/lodash/_baseIsEqualDeep.js"(exports2, module2) {
    var Stack2 = require_Stack();
    var equalArrays2 = require_equalArrays();
    var equalByTag2 = require_equalByTag();
    var equalObjects2 = require_equalObjects();
    var getTag2 = require_getTag();
    var isArray2 = require_isArray();
    var isBuffer2 = require_isBuffer();
    var isTypedArray2 = require_isTypedArray();
    var COMPARE_PARTIAL_FLAG7 = 1;
    var argsTag5 = "[object Arguments]";
    var arrayTag4 = "[object Array]";
    var objectTag6 = "[object Object]";
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    function baseIsEqualDeep2(object, other, bitmask, customizer, equalFunc, stack) {
      var objIsArr = isArray2(object), othIsArr = isArray2(other), objTag = objIsArr ? arrayTag4 : getTag2(object), othTag = othIsArr ? arrayTag4 : getTag2(other);
      objTag = objTag == argsTag5 ? objectTag6 : objTag;
      othTag = othTag == argsTag5 ? objectTag6 : othTag;
      var objIsObj = objTag == objectTag6, othIsObj = othTag == objectTag6, isSameTag = objTag == othTag;
      if (isSameTag && isBuffer2(object)) {
        if (!isBuffer2(other)) {
          return false;
        }
        objIsArr = true;
        objIsObj = false;
      }
      if (isSameTag && !objIsObj) {
        stack || (stack = new Stack2());
        return objIsArr || isTypedArray2(object) ? equalArrays2(object, other, bitmask, customizer, equalFunc, stack) : equalByTag2(object, other, objTag, bitmask, customizer, equalFunc, stack);
      }
      if (!(bitmask & COMPARE_PARTIAL_FLAG7)) {
        var objIsWrapped = objIsObj && hasOwnProperty16.call(object, "__wrapped__"), othIsWrapped = othIsObj && hasOwnProperty16.call(other, "__wrapped__");
        if (objIsWrapped || othIsWrapped) {
          var objUnwrapped = objIsWrapped ? object.value() : object, othUnwrapped = othIsWrapped ? other.value() : other;
          stack || (stack = new Stack2());
          return equalFunc(objUnwrapped, othUnwrapped, bitmask, customizer, stack);
        }
      }
      if (!isSameTag) {
        return false;
      }
      stack || (stack = new Stack2());
      return equalObjects2(object, other, bitmask, customizer, equalFunc, stack);
    }
    module2.exports = baseIsEqualDeep2;
  }
});

// node_modules/lodash/_baseIsEqual.js
var require_baseIsEqual = __commonJS({
  "node_modules/lodash/_baseIsEqual.js"(exports2, module2) {
    var baseIsEqualDeep2 = require_baseIsEqualDeep();
    var isObjectLike2 = require_isObjectLike();
    function baseIsEqual2(value, other, bitmask, customizer, stack) {
      if (value === other) {
        return true;
      }
      if (value == null || other == null || !isObjectLike2(value) && !isObjectLike2(other)) {
        return value !== value && other !== other;
      }
      return baseIsEqualDeep2(value, other, bitmask, customizer, baseIsEqual2, stack);
    }
    module2.exports = baseIsEqual2;
  }
});

// node_modules/lodash/isEqual.js
var require_isEqual = __commonJS({
  "node_modules/lodash/isEqual.js"(exports2, module2) {
    var baseIsEqual2 = require_baseIsEqual();
    function isEqual2(value, other) {
      return baseIsEqual2(value, other);
    }
    module2.exports = isEqual2;
  }
});

// node_modules/lodash/_isFlattenable.js
var require_isFlattenable = __commonJS({
  "node_modules/lodash/_isFlattenable.js"(exports2, module2) {
    var Symbol3 = require_Symbol();
    var isArguments2 = require_isArguments();
    var isArray2 = require_isArray();
    var spreadableSymbol2 = Symbol3 ? Symbol3.isConcatSpreadable : void 0;
    function isFlattenable2(value) {
      return isArray2(value) || isArguments2(value) || !!(spreadableSymbol2 && value && value[spreadableSymbol2]);
    }
    module2.exports = isFlattenable2;
  }
});

// node_modules/lodash/_baseFlatten.js
var require_baseFlatten = __commonJS({
  "node_modules/lodash/_baseFlatten.js"(exports2, module2) {
    var arrayPush2 = require_arrayPush();
    var isFlattenable2 = require_isFlattenable();
    function baseFlatten2(array, depth, predicate, isStrict, result) {
      var index = -1, length = array.length;
      predicate || (predicate = isFlattenable2);
      result || (result = []);
      while (++index < length) {
        var value = array[index];
        if (depth > 0 && predicate(value)) {
          if (depth > 1) {
            baseFlatten2(value, depth - 1, predicate, isStrict, result);
          } else {
            arrayPush2(result, value);
          }
        } else if (!isStrict) {
          result[result.length] = value;
        }
      }
      return result;
    }
    module2.exports = baseFlatten2;
  }
});

// node_modules/lodash/_arrayMap.js
var require_arrayMap = __commonJS({
  "node_modules/lodash/_arrayMap.js"(exports2, module2) {
    function arrayMap2(array, iteratee) {
      var index = -1, length = array == null ? 0 : array.length, result = Array(length);
      while (++index < length) {
        result[index] = iteratee(array[index], index, array);
      }
      return result;
    }
    module2.exports = arrayMap2;
  }
});

// node_modules/lodash/isSymbol.js
var require_isSymbol = __commonJS({
  "node_modules/lodash/isSymbol.js"(exports2, module2) {
    var baseGetTag2 = require_baseGetTag();
    var isObjectLike2 = require_isObjectLike();
    var symbolTag5 = "[object Symbol]";
    function isSymbol2(value) {
      return typeof value == "symbol" || isObjectLike2(value) && baseGetTag2(value) == symbolTag5;
    }
    module2.exports = isSymbol2;
  }
});

// node_modules/lodash/_isKey.js
var require_isKey = __commonJS({
  "node_modules/lodash/_isKey.js"(exports2, module2) {
    var isArray2 = require_isArray();
    var isSymbol2 = require_isSymbol();
    var reIsDeepProp2 = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/;
    var reIsPlainProp2 = /^\w*$/;
    function isKey2(value, object) {
      if (isArray2(value)) {
        return false;
      }
      var type = typeof value;
      if (type == "number" || type == "symbol" || type == "boolean" || value == null || isSymbol2(value)) {
        return true;
      }
      return reIsPlainProp2.test(value) || !reIsDeepProp2.test(value) || object != null && value in Object(object);
    }
    module2.exports = isKey2;
  }
});

// node_modules/lodash/memoize.js
var require_memoize = __commonJS({
  "node_modules/lodash/memoize.js"(exports2, module2) {
    var MapCache2 = require_MapCache();
    var FUNC_ERROR_TEXT2 = "Expected a function";
    function memoize2(func, resolver) {
      if (typeof func != "function" || resolver != null && typeof resolver != "function") {
        throw new TypeError(FUNC_ERROR_TEXT2);
      }
      var memoized = function() {
        var args = arguments, key = resolver ? resolver.apply(this, args) : args[0], cache = memoized.cache;
        if (cache.has(key)) {
          return cache.get(key);
        }
        var result = func.apply(this, args);
        memoized.cache = cache.set(key, result) || cache;
        return result;
      };
      memoized.cache = new (memoize2.Cache || MapCache2)();
      return memoized;
    }
    memoize2.Cache = MapCache2;
    module2.exports = memoize2;
  }
});

// node_modules/lodash/_memoizeCapped.js
var require_memoizeCapped = __commonJS({
  "node_modules/lodash/_memoizeCapped.js"(exports2, module2) {
    var memoize2 = require_memoize();
    var MAX_MEMOIZE_SIZE2 = 500;
    function memoizeCapped2(func) {
      var result = memoize2(func, function(key) {
        if (cache.size === MAX_MEMOIZE_SIZE2) {
          cache.clear();
        }
        return key;
      });
      var cache = result.cache;
      return result;
    }
    module2.exports = memoizeCapped2;
  }
});

// node_modules/lodash/_stringToPath.js
var require_stringToPath = __commonJS({
  "node_modules/lodash/_stringToPath.js"(exports2, module2) {
    var memoizeCapped2 = require_memoizeCapped();
    var rePropName2 = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g;
    var reEscapeChar2 = /\\(\\)?/g;
    var stringToPath2 = memoizeCapped2(function(string) {
      var result = [];
      if (string.charCodeAt(0) === 46) {
        result.push("");
      }
      string.replace(rePropName2, function(match, number, quote, subString) {
        result.push(quote ? subString.replace(reEscapeChar2, "$1") : number || match);
      });
      return result;
    });
    module2.exports = stringToPath2;
  }
});

// node_modules/lodash/_baseToString.js
var require_baseToString = __commonJS({
  "node_modules/lodash/_baseToString.js"(exports2, module2) {
    var Symbol3 = require_Symbol();
    var arrayMap2 = require_arrayMap();
    var isArray2 = require_isArray();
    var isSymbol2 = require_isSymbol();
    var INFINITY6 = 1 / 0;
    var symbolProto4 = Symbol3 ? Symbol3.prototype : void 0;
    var symbolToString2 = symbolProto4 ? symbolProto4.toString : void 0;
    function baseToString2(value) {
      if (typeof value == "string") {
        return value;
      }
      if (isArray2(value)) {
        return arrayMap2(value, baseToString2) + "";
      }
      if (isSymbol2(value)) {
        return symbolToString2 ? symbolToString2.call(value) : "";
      }
      var result = value + "";
      return result == "0" && 1 / value == -INFINITY6 ? "-0" : result;
    }
    module2.exports = baseToString2;
  }
});

// node_modules/lodash/toString.js
var require_toString = __commonJS({
  "node_modules/lodash/toString.js"(exports2, module2) {
    var baseToString2 = require_baseToString();
    function toString2(value) {
      return value == null ? "" : baseToString2(value);
    }
    module2.exports = toString2;
  }
});

// node_modules/lodash/_castPath.js
var require_castPath = __commonJS({
  "node_modules/lodash/_castPath.js"(exports2, module2) {
    var isArray2 = require_isArray();
    var isKey2 = require_isKey();
    var stringToPath2 = require_stringToPath();
    var toString2 = require_toString();
    function castPath2(value, object) {
      if (isArray2(value)) {
        return value;
      }
      return isKey2(value, object) ? [value] : stringToPath2(toString2(value));
    }
    module2.exports = castPath2;
  }
});

// node_modules/lodash/_toKey.js
var require_toKey = __commonJS({
  "node_modules/lodash/_toKey.js"(exports2, module2) {
    var isSymbol2 = require_isSymbol();
    var INFINITY6 = 1 / 0;
    function toKey2(value) {
      if (typeof value == "string" || isSymbol2(value)) {
        return value;
      }
      var result = value + "";
      return result == "0" && 1 / value == -INFINITY6 ? "-0" : result;
    }
    module2.exports = toKey2;
  }
});

// node_modules/lodash/_baseGet.js
var require_baseGet = __commonJS({
  "node_modules/lodash/_baseGet.js"(exports2, module2) {
    var castPath2 = require_castPath();
    var toKey2 = require_toKey();
    function baseGet2(object, path) {
      path = castPath2(path, object);
      var index = 0, length = path.length;
      while (object != null && index < length) {
        object = object[toKey2(path[index++])];
      }
      return index && index == length ? object : void 0;
    }
    module2.exports = baseGet2;
  }
});

// node_modules/lodash/_baseIsMatch.js
var require_baseIsMatch = __commonJS({
  "node_modules/lodash/_baseIsMatch.js"(exports2, module2) {
    var Stack2 = require_Stack();
    var baseIsEqual2 = require_baseIsEqual();
    var COMPARE_PARTIAL_FLAG7 = 1;
    var COMPARE_UNORDERED_FLAG5 = 2;
    function baseIsMatch2(object, source, matchData, customizer) {
      var index = matchData.length, length = index, noCustomizer = !customizer;
      if (object == null) {
        return !length;
      }
      object = Object(object);
      while (index--) {
        var data = matchData[index];
        if (noCustomizer && data[2] ? data[1] !== object[data[0]] : !(data[0] in object)) {
          return false;
        }
      }
      while (++index < length) {
        data = matchData[index];
        var key = data[0], objValue = object[key], srcValue = data[1];
        if (noCustomizer && data[2]) {
          if (objValue === void 0 && !(key in object)) {
            return false;
          }
        } else {
          var stack = new Stack2();
          if (customizer) {
            var result = customizer(objValue, srcValue, key, object, source, stack);
          }
          if (!(result === void 0 ? baseIsEqual2(srcValue, objValue, COMPARE_PARTIAL_FLAG7 | COMPARE_UNORDERED_FLAG5, customizer, stack) : result)) {
            return false;
          }
        }
      }
      return true;
    }
    module2.exports = baseIsMatch2;
  }
});

// node_modules/lodash/_isStrictComparable.js
var require_isStrictComparable = __commonJS({
  "node_modules/lodash/_isStrictComparable.js"(exports2, module2) {
    var isObject3 = require_isObject();
    function isStrictComparable2(value) {
      return value === value && !isObject3(value);
    }
    module2.exports = isStrictComparable2;
  }
});

// node_modules/lodash/_getMatchData.js
var require_getMatchData = __commonJS({
  "node_modules/lodash/_getMatchData.js"(exports2, module2) {
    var isStrictComparable2 = require_isStrictComparable();
    var keys2 = require_keys();
    function getMatchData2(object) {
      var result = keys2(object), length = result.length;
      while (length--) {
        var key = result[length], value = object[key];
        result[length] = [key, value, isStrictComparable2(value)];
      }
      return result;
    }
    module2.exports = getMatchData2;
  }
});

// node_modules/lodash/_matchesStrictComparable.js
var require_matchesStrictComparable = __commonJS({
  "node_modules/lodash/_matchesStrictComparable.js"(exports2, module2) {
    function matchesStrictComparable2(key, srcValue) {
      return function(object) {
        if (object == null) {
          return false;
        }
        return object[key] === srcValue && (srcValue !== void 0 || key in Object(object));
      };
    }
    module2.exports = matchesStrictComparable2;
  }
});

// node_modules/lodash/_baseMatches.js
var require_baseMatches = __commonJS({
  "node_modules/lodash/_baseMatches.js"(exports2, module2) {
    var baseIsMatch2 = require_baseIsMatch();
    var getMatchData2 = require_getMatchData();
    var matchesStrictComparable2 = require_matchesStrictComparable();
    function baseMatches2(source) {
      var matchData = getMatchData2(source);
      if (matchData.length == 1 && matchData[0][2]) {
        return matchesStrictComparable2(matchData[0][0], matchData[0][1]);
      }
      return function(object) {
        return object === source || baseIsMatch2(object, source, matchData);
      };
    }
    module2.exports = baseMatches2;
  }
});

// node_modules/lodash/get.js
var require_get = __commonJS({
  "node_modules/lodash/get.js"(exports2, module2) {
    var baseGet2 = require_baseGet();
    function get2(object, path, defaultValue) {
      var result = object == null ? void 0 : baseGet2(object, path);
      return result === void 0 ? defaultValue : result;
    }
    module2.exports = get2;
  }
});

// node_modules/lodash/_baseHasIn.js
var require_baseHasIn = __commonJS({
  "node_modules/lodash/_baseHasIn.js"(exports2, module2) {
    function baseHasIn2(object, key) {
      return object != null && key in Object(object);
    }
    module2.exports = baseHasIn2;
  }
});

// node_modules/lodash/_hasPath.js
var require_hasPath = __commonJS({
  "node_modules/lodash/_hasPath.js"(exports2, module2) {
    var castPath2 = require_castPath();
    var isArguments2 = require_isArguments();
    var isArray2 = require_isArray();
    var isIndex2 = require_isIndex();
    var isLength2 = require_isLength();
    var toKey2 = require_toKey();
    function hasPath2(object, path, hasFunc) {
      path = castPath2(path, object);
      var index = -1, length = path.length, result = false;
      while (++index < length) {
        var key = toKey2(path[index]);
        if (!(result = object != null && hasFunc(object, key))) {
          break;
        }
        object = object[key];
      }
      if (result || ++index != length) {
        return result;
      }
      length = object == null ? 0 : object.length;
      return !!length && isLength2(length) && isIndex2(key, length) && (isArray2(object) || isArguments2(object));
    }
    module2.exports = hasPath2;
  }
});

// node_modules/lodash/hasIn.js
var require_hasIn = __commonJS({
  "node_modules/lodash/hasIn.js"(exports2, module2) {
    var baseHasIn2 = require_baseHasIn();
    var hasPath2 = require_hasPath();
    function hasIn2(object, path) {
      return object != null && hasPath2(object, path, baseHasIn2);
    }
    module2.exports = hasIn2;
  }
});

// node_modules/lodash/_baseMatchesProperty.js
var require_baseMatchesProperty = __commonJS({
  "node_modules/lodash/_baseMatchesProperty.js"(exports2, module2) {
    var baseIsEqual2 = require_baseIsEqual();
    var get2 = require_get();
    var hasIn2 = require_hasIn();
    var isKey2 = require_isKey();
    var isStrictComparable2 = require_isStrictComparable();
    var matchesStrictComparable2 = require_matchesStrictComparable();
    var toKey2 = require_toKey();
    var COMPARE_PARTIAL_FLAG7 = 1;
    var COMPARE_UNORDERED_FLAG5 = 2;
    function baseMatchesProperty2(path, srcValue) {
      if (isKey2(path) && isStrictComparable2(srcValue)) {
        return matchesStrictComparable2(toKey2(path), srcValue);
      }
      return function(object) {
        var objValue = get2(object, path);
        return objValue === void 0 && objValue === srcValue ? hasIn2(object, path) : baseIsEqual2(srcValue, objValue, COMPARE_PARTIAL_FLAG7 | COMPARE_UNORDERED_FLAG5);
      };
    }
    module2.exports = baseMatchesProperty2;
  }
});

// node_modules/lodash/identity.js
var require_identity = __commonJS({
  "node_modules/lodash/identity.js"(exports2, module2) {
    function identity2(value) {
      return value;
    }
    module2.exports = identity2;
  }
});

// node_modules/lodash/_baseProperty.js
var require_baseProperty = __commonJS({
  "node_modules/lodash/_baseProperty.js"(exports2, module2) {
    function baseProperty2(key) {
      return function(object) {
        return object == null ? void 0 : object[key];
      };
    }
    module2.exports = baseProperty2;
  }
});

// node_modules/lodash/_basePropertyDeep.js
var require_basePropertyDeep = __commonJS({
  "node_modules/lodash/_basePropertyDeep.js"(exports2, module2) {
    var baseGet2 = require_baseGet();
    function basePropertyDeep2(path) {
      return function(object) {
        return baseGet2(object, path);
      };
    }
    module2.exports = basePropertyDeep2;
  }
});

// node_modules/lodash/property.js
var require_property = __commonJS({
  "node_modules/lodash/property.js"(exports2, module2) {
    var baseProperty2 = require_baseProperty();
    var basePropertyDeep2 = require_basePropertyDeep();
    var isKey2 = require_isKey();
    var toKey2 = require_toKey();
    function property2(path) {
      return isKey2(path) ? baseProperty2(toKey2(path)) : basePropertyDeep2(path);
    }
    module2.exports = property2;
  }
});

// node_modules/lodash/_baseIteratee.js
var require_baseIteratee = __commonJS({
  "node_modules/lodash/_baseIteratee.js"(exports2, module2) {
    var baseMatches2 = require_baseMatches();
    var baseMatchesProperty2 = require_baseMatchesProperty();
    var identity2 = require_identity();
    var isArray2 = require_isArray();
    var property2 = require_property();
    function baseIteratee2(value) {
      if (typeof value == "function") {
        return value;
      }
      if (value == null) {
        return identity2;
      }
      if (typeof value == "object") {
        return isArray2(value) ? baseMatchesProperty2(value[0], value[1]) : baseMatches2(value);
      }
      return property2(value);
    }
    module2.exports = baseIteratee2;
  }
});

// node_modules/lodash/_createBaseFor.js
var require_createBaseFor = __commonJS({
  "node_modules/lodash/_createBaseFor.js"(exports2, module2) {
    function createBaseFor2(fromRight) {
      return function(object, iteratee, keysFunc) {
        var index = -1, iterable = Object(object), props = keysFunc(object), length = props.length;
        while (length--) {
          var key = props[fromRight ? length : ++index];
          if (iteratee(iterable[key], key, iterable) === false) {
            break;
          }
        }
        return object;
      };
    }
    module2.exports = createBaseFor2;
  }
});

// node_modules/lodash/_baseFor.js
var require_baseFor = __commonJS({
  "node_modules/lodash/_baseFor.js"(exports2, module2) {
    var createBaseFor2 = require_createBaseFor();
    var baseFor2 = createBaseFor2();
    module2.exports = baseFor2;
  }
});

// node_modules/lodash/_baseForOwn.js
var require_baseForOwn = __commonJS({
  "node_modules/lodash/_baseForOwn.js"(exports2, module2) {
    var baseFor2 = require_baseFor();
    var keys2 = require_keys();
    function baseForOwn2(object, iteratee) {
      return object && baseFor2(object, iteratee, keys2);
    }
    module2.exports = baseForOwn2;
  }
});

// node_modules/lodash/_createBaseEach.js
var require_createBaseEach = __commonJS({
  "node_modules/lodash/_createBaseEach.js"(exports2, module2) {
    var isArrayLike2 = require_isArrayLike();
    function createBaseEach2(eachFunc, fromRight) {
      return function(collection, iteratee) {
        if (collection == null) {
          return collection;
        }
        if (!isArrayLike2(collection)) {
          return eachFunc(collection, iteratee);
        }
        var length = collection.length, index = fromRight ? length : -1, iterable = Object(collection);
        while (fromRight ? index-- : ++index < length) {
          if (iteratee(iterable[index], index, iterable) === false) {
            break;
          }
        }
        return collection;
      };
    }
    module2.exports = createBaseEach2;
  }
});

// node_modules/lodash/_baseEach.js
var require_baseEach = __commonJS({
  "node_modules/lodash/_baseEach.js"(exports2, module2) {
    var baseForOwn2 = require_baseForOwn();
    var createBaseEach2 = require_createBaseEach();
    var baseEach2 = createBaseEach2(baseForOwn2);
    module2.exports = baseEach2;
  }
});

// node_modules/lodash/_baseMap.js
var require_baseMap = __commonJS({
  "node_modules/lodash/_baseMap.js"(exports2, module2) {
    var baseEach2 = require_baseEach();
    var isArrayLike2 = require_isArrayLike();
    function baseMap(collection, iteratee) {
      var index = -1, result = isArrayLike2(collection) ? Array(collection.length) : [];
      baseEach2(collection, function(value, key, collection2) {
        result[++index] = iteratee(value, key, collection2);
      });
      return result;
    }
    module2.exports = baseMap;
  }
});

// node_modules/lodash/_baseSortBy.js
var require_baseSortBy = __commonJS({
  "node_modules/lodash/_baseSortBy.js"(exports2, module2) {
    function baseSortBy(array, comparer) {
      var length = array.length;
      array.sort(comparer);
      while (length--) {
        array[length] = array[length].value;
      }
      return array;
    }
    module2.exports = baseSortBy;
  }
});

// node_modules/lodash/_compareAscending.js
var require_compareAscending = __commonJS({
  "node_modules/lodash/_compareAscending.js"(exports2, module2) {
    var isSymbol2 = require_isSymbol();
    function compareAscending(value, other) {
      if (value !== other) {
        var valIsDefined = value !== void 0, valIsNull = value === null, valIsReflexive = value === value, valIsSymbol = isSymbol2(value);
        var othIsDefined = other !== void 0, othIsNull = other === null, othIsReflexive = other === other, othIsSymbol = isSymbol2(other);
        if (!othIsNull && !othIsSymbol && !valIsSymbol && value > other || valIsSymbol && othIsDefined && othIsReflexive && !othIsNull && !othIsSymbol || valIsNull && othIsDefined && othIsReflexive || !valIsDefined && othIsReflexive || !valIsReflexive) {
          return 1;
        }
        if (!valIsNull && !valIsSymbol && !othIsSymbol && value < other || othIsSymbol && valIsDefined && valIsReflexive && !valIsNull && !valIsSymbol || othIsNull && valIsDefined && valIsReflexive || !othIsDefined && valIsReflexive || !othIsReflexive) {
          return -1;
        }
      }
      return 0;
    }
    module2.exports = compareAscending;
  }
});

// node_modules/lodash/_compareMultiple.js
var require_compareMultiple = __commonJS({
  "node_modules/lodash/_compareMultiple.js"(exports2, module2) {
    var compareAscending = require_compareAscending();
    function compareMultiple(object, other, orders) {
      var index = -1, objCriteria = object.criteria, othCriteria = other.criteria, length = objCriteria.length, ordersLength = orders.length;
      while (++index < length) {
        var result = compareAscending(objCriteria[index], othCriteria[index]);
        if (result) {
          if (index >= ordersLength) {
            return result;
          }
          var order = orders[index];
          return result * (order == "desc" ? -1 : 1);
        }
      }
      return object.index - other.index;
    }
    module2.exports = compareMultiple;
  }
});

// node_modules/lodash/_baseOrderBy.js
var require_baseOrderBy = __commonJS({
  "node_modules/lodash/_baseOrderBy.js"(exports2, module2) {
    var arrayMap2 = require_arrayMap();
    var baseGet2 = require_baseGet();
    var baseIteratee2 = require_baseIteratee();
    var baseMap = require_baseMap();
    var baseSortBy = require_baseSortBy();
    var baseUnary2 = require_baseUnary();
    var compareMultiple = require_compareMultiple();
    var identity2 = require_identity();
    var isArray2 = require_isArray();
    function baseOrderBy(collection, iteratees, orders) {
      if (iteratees.length) {
        iteratees = arrayMap2(iteratees, function(iteratee) {
          if (isArray2(iteratee)) {
            return function(value) {
              return baseGet2(value, iteratee.length === 1 ? iteratee[0] : iteratee);
            };
          }
          return iteratee;
        });
      } else {
        iteratees = [identity2];
      }
      var index = -1;
      iteratees = arrayMap2(iteratees, baseUnary2(baseIteratee2));
      var result = baseMap(collection, function(value, key, collection2) {
        var criteria = arrayMap2(iteratees, function(iteratee) {
          return iteratee(value);
        });
        return { "criteria": criteria, "index": ++index, "value": value };
      });
      return baseSortBy(result, function(object, other) {
        return compareMultiple(object, other, orders);
      });
    }
    module2.exports = baseOrderBy;
  }
});

// node_modules/lodash/_apply.js
var require_apply = __commonJS({
  "node_modules/lodash/_apply.js"(exports2, module2) {
    function apply2(func, thisArg, args) {
      switch (args.length) {
        case 0:
          return func.call(thisArg);
        case 1:
          return func.call(thisArg, args[0]);
        case 2:
          return func.call(thisArg, args[0], args[1]);
        case 3:
          return func.call(thisArg, args[0], args[1], args[2]);
      }
      return func.apply(thisArg, args);
    }
    module2.exports = apply2;
  }
});

// node_modules/lodash/_overRest.js
var require_overRest = __commonJS({
  "node_modules/lodash/_overRest.js"(exports2, module2) {
    var apply2 = require_apply();
    var nativeMax2 = Math.max;
    function overRest2(func, start, transform2) {
      start = nativeMax2(start === void 0 ? func.length - 1 : start, 0);
      return function() {
        var args = arguments, index = -1, length = nativeMax2(args.length - start, 0), array = Array(length);
        while (++index < length) {
          array[index] = args[start + index];
        }
        index = -1;
        var otherArgs = Array(start + 1);
        while (++index < start) {
          otherArgs[index] = args[index];
        }
        otherArgs[start] = transform2(array);
        return apply2(func, this, otherArgs);
      };
    }
    module2.exports = overRest2;
  }
});

// node_modules/lodash/constant.js
var require_constant = __commonJS({
  "node_modules/lodash/constant.js"(exports2, module2) {
    function constant2(value) {
      return function() {
        return value;
      };
    }
    module2.exports = constant2;
  }
});

// node_modules/lodash/_baseSetToString.js
var require_baseSetToString = __commonJS({
  "node_modules/lodash/_baseSetToString.js"(exports2, module2) {
    var constant2 = require_constant();
    var defineProperty2 = require_defineProperty();
    var identity2 = require_identity();
    var baseSetToString2 = !defineProperty2 ? identity2 : function(func, string) {
      return defineProperty2(func, "toString", {
        "configurable": true,
        "enumerable": false,
        "value": constant2(string),
        "writable": true
      });
    };
    module2.exports = baseSetToString2;
  }
});

// node_modules/lodash/_shortOut.js
var require_shortOut = __commonJS({
  "node_modules/lodash/_shortOut.js"(exports2, module2) {
    var HOT_COUNT2 = 800;
    var HOT_SPAN2 = 16;
    var nativeNow2 = Date.now;
    function shortOut2(func) {
      var count = 0, lastCalled = 0;
      return function() {
        var stamp = nativeNow2(), remaining = HOT_SPAN2 - (stamp - lastCalled);
        lastCalled = stamp;
        if (remaining > 0) {
          if (++count >= HOT_COUNT2) {
            return arguments[0];
          }
        } else {
          count = 0;
        }
        return func.apply(void 0, arguments);
      };
    }
    module2.exports = shortOut2;
  }
});

// node_modules/lodash/_setToString.js
var require_setToString = __commonJS({
  "node_modules/lodash/_setToString.js"(exports2, module2) {
    var baseSetToString2 = require_baseSetToString();
    var shortOut2 = require_shortOut();
    var setToString2 = shortOut2(baseSetToString2);
    module2.exports = setToString2;
  }
});

// node_modules/lodash/_baseRest.js
var require_baseRest = __commonJS({
  "node_modules/lodash/_baseRest.js"(exports2, module2) {
    var identity2 = require_identity();
    var overRest2 = require_overRest();
    var setToString2 = require_setToString();
    function baseRest2(func, start) {
      return setToString2(overRest2(func, start, identity2), func + "");
    }
    module2.exports = baseRest2;
  }
});

// node_modules/lodash/_isIterateeCall.js
var require_isIterateeCall = __commonJS({
  "node_modules/lodash/_isIterateeCall.js"(exports2, module2) {
    var eq2 = require_eq();
    var isArrayLike2 = require_isArrayLike();
    var isIndex2 = require_isIndex();
    var isObject3 = require_isObject();
    function isIterateeCall2(value, index, object) {
      if (!isObject3(object)) {
        return false;
      }
      var type = typeof index;
      if (type == "number" ? isArrayLike2(object) && isIndex2(index, object.length) : type == "string" && index in object) {
        return eq2(object[index], value);
      }
      return false;
    }
    module2.exports = isIterateeCall2;
  }
});

// node_modules/lodash/sortBy.js
var require_sortBy = __commonJS({
  "node_modules/lodash/sortBy.js"(exports2, module2) {
    var baseFlatten2 = require_baseFlatten();
    var baseOrderBy = require_baseOrderBy();
    var baseRest2 = require_baseRest();
    var isIterateeCall2 = require_isIterateeCall();
    var sortBy = baseRest2(function(collection, iteratees) {
      if (collection == null) {
        return [];
      }
      var length = iteratees.length;
      if (length > 1 && isIterateeCall2(collection, iteratees[0], iteratees[1])) {
        iteratees = [];
      } else if (length > 2 && isIterateeCall2(iteratees[0], iteratees[1], iteratees[2])) {
        iteratees = [iteratees[0]];
      }
      return baseOrderBy(collection, baseFlatten2(iteratees, 1), []);
    });
    module2.exports = sortBy;
  }
});

// node_modules/lodash/_baseFindIndex.js
var require_baseFindIndex = __commonJS({
  "node_modules/lodash/_baseFindIndex.js"(exports2, module2) {
    function baseFindIndex2(array, predicate, fromIndex, fromRight) {
      var length = array.length, index = fromIndex + (fromRight ? 1 : -1);
      while (fromRight ? index-- : ++index < length) {
        if (predicate(array[index], index, array)) {
          return index;
        }
      }
      return -1;
    }
    module2.exports = baseFindIndex2;
  }
});

// node_modules/lodash/_baseIsNaN.js
var require_baseIsNaN = __commonJS({
  "node_modules/lodash/_baseIsNaN.js"(exports2, module2) {
    function baseIsNaN2(value) {
      return value !== value;
    }
    module2.exports = baseIsNaN2;
  }
});

// node_modules/lodash/_strictIndexOf.js
var require_strictIndexOf = __commonJS({
  "node_modules/lodash/_strictIndexOf.js"(exports2, module2) {
    function strictIndexOf2(array, value, fromIndex) {
      var index = fromIndex - 1, length = array.length;
      while (++index < length) {
        if (array[index] === value) {
          return index;
        }
      }
      return -1;
    }
    module2.exports = strictIndexOf2;
  }
});

// node_modules/lodash/_baseIndexOf.js
var require_baseIndexOf = __commonJS({
  "node_modules/lodash/_baseIndexOf.js"(exports2, module2) {
    var baseFindIndex2 = require_baseFindIndex();
    var baseIsNaN2 = require_baseIsNaN();
    var strictIndexOf2 = require_strictIndexOf();
    function baseIndexOf2(array, value, fromIndex) {
      return value === value ? strictIndexOf2(array, value, fromIndex) : baseFindIndex2(array, baseIsNaN2, fromIndex);
    }
    module2.exports = baseIndexOf2;
  }
});

// node_modules/lodash/_arrayIncludes.js
var require_arrayIncludes = __commonJS({
  "node_modules/lodash/_arrayIncludes.js"(exports2, module2) {
    var baseIndexOf2 = require_baseIndexOf();
    function arrayIncludes2(array, value) {
      var length = array == null ? 0 : array.length;
      return !!length && baseIndexOf2(array, value, 0) > -1;
    }
    module2.exports = arrayIncludes2;
  }
});

// node_modules/lodash/_arrayIncludesWith.js
var require_arrayIncludesWith = __commonJS({
  "node_modules/lodash/_arrayIncludesWith.js"(exports2, module2) {
    function arrayIncludesWith2(array, value, comparator) {
      var index = -1, length = array == null ? 0 : array.length;
      while (++index < length) {
        if (comparator(value, array[index])) {
          return true;
        }
      }
      return false;
    }
    module2.exports = arrayIncludesWith2;
  }
});

// node_modules/lodash/noop.js
var require_noop = __commonJS({
  "node_modules/lodash/noop.js"(exports2, module2) {
    function noop2() {
    }
    module2.exports = noop2;
  }
});

// node_modules/lodash/_createSet.js
var require_createSet = __commonJS({
  "node_modules/lodash/_createSet.js"(exports2, module2) {
    var Set3 = require_Set();
    var noop2 = require_noop();
    var setToArray2 = require_setToArray();
    var INFINITY6 = 1 / 0;
    var createSet2 = !(Set3 && 1 / setToArray2(new Set3([, -0]))[1] == INFINITY6) ? noop2 : function(values) {
      return new Set3(values);
    };
    module2.exports = createSet2;
  }
});

// node_modules/lodash/_baseUniq.js
var require_baseUniq = __commonJS({
  "node_modules/lodash/_baseUniq.js"(exports2, module2) {
    var SetCache2 = require_SetCache();
    var arrayIncludes2 = require_arrayIncludes();
    var arrayIncludesWith2 = require_arrayIncludesWith();
    var cacheHas2 = require_cacheHas();
    var createSet2 = require_createSet();
    var setToArray2 = require_setToArray();
    var LARGE_ARRAY_SIZE4 = 200;
    function baseUniq2(array, iteratee, comparator) {
      var index = -1, includes = arrayIncludes2, length = array.length, isCommon = true, result = [], seen = result;
      if (comparator) {
        isCommon = false;
        includes = arrayIncludesWith2;
      } else if (length >= LARGE_ARRAY_SIZE4) {
        var set2 = iteratee ? null : createSet2(array);
        if (set2) {
          return setToArray2(set2);
        }
        isCommon = false;
        includes = cacheHas2;
        seen = new SetCache2();
      } else {
        seen = iteratee ? [] : result;
      }
      outer:
        while (++index < length) {
          var value = array[index], computed = iteratee ? iteratee(value) : value;
          value = comparator || value !== 0 ? value : 0;
          if (isCommon && computed === computed) {
            var seenIndex = seen.length;
            while (seenIndex--) {
              if (seen[seenIndex] === computed) {
                continue outer;
              }
            }
            if (iteratee) {
              seen.push(computed);
            }
            result.push(value);
          } else if (!includes(seen, computed, comparator)) {
            if (seen !== result) {
              seen.push(computed);
            }
            result.push(value);
          }
        }
      return result;
    }
    module2.exports = baseUniq2;
  }
});

// node_modules/lodash/uniq.js
var require_uniq = __commonJS({
  "node_modules/lodash/uniq.js"(exports2, module2) {
    var baseUniq2 = require_baseUniq();
    function uniq2(array) {
      return array && array.length ? baseUniq2(array) : [];
    }
    module2.exports = uniq2;
  }
});

// node_modules/lodash/uniqWith.js
var require_uniqWith = __commonJS({
  "node_modules/lodash/uniqWith.js"(exports2, module2) {
    var baseUniq2 = require_baseUniq();
    function uniqWith(array, comparator) {
      comparator = typeof comparator == "function" ? comparator : void 0;
      return array && array.length ? baseUniq2(array, void 0, comparator) : [];
    }
    module2.exports = uniqWith;
  }
});

// node_modules/lodash/defaults.js
var require_defaults = __commonJS({
  "node_modules/lodash/defaults.js"(exports2, module2) {
    var baseRest2 = require_baseRest();
    var eq2 = require_eq();
    var isIterateeCall2 = require_isIterateeCall();
    var keysIn2 = require_keysIn();
    var objectProto19 = Object.prototype;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    var defaults = baseRest2(function(object, sources) {
      object = Object(object);
      var index = -1;
      var length = sources.length;
      var guard = length > 2 ? sources[2] : void 0;
      if (guard && isIterateeCall2(sources[0], sources[1], guard)) {
        length = 1;
      }
      while (++index < length) {
        var source = sources[index];
        var props = keysIn2(source);
        var propsIndex = -1;
        var propsLength = props.length;
        while (++propsIndex < propsLength) {
          var key = props[propsIndex];
          var value = object[key];
          if (value === void 0 || eq2(value, objectProto19[key]) && !hasOwnProperty16.call(object, key)) {
            object[key] = source[key];
          }
        }
      }
      return object;
    });
    module2.exports = defaults;
  }
});

// node_modules/lodash/_baseIntersection.js
var require_baseIntersection = __commonJS({
  "node_modules/lodash/_baseIntersection.js"(exports2, module2) {
    var SetCache2 = require_SetCache();
    var arrayIncludes2 = require_arrayIncludes();
    var arrayIncludesWith2 = require_arrayIncludesWith();
    var arrayMap2 = require_arrayMap();
    var baseUnary2 = require_baseUnary();
    var cacheHas2 = require_cacheHas();
    var nativeMin2 = Math.min;
    function baseIntersection(arrays, iteratee, comparator) {
      var includes = comparator ? arrayIncludesWith2 : arrayIncludes2, length = arrays[0].length, othLength = arrays.length, othIndex = othLength, caches = Array(othLength), maxLength = Infinity, result = [];
      while (othIndex--) {
        var array = arrays[othIndex];
        if (othIndex && iteratee) {
          array = arrayMap2(array, baseUnary2(iteratee));
        }
        maxLength = nativeMin2(array.length, maxLength);
        caches[othIndex] = !comparator && (iteratee || length >= 120 && array.length >= 120) ? new SetCache2(othIndex && array) : void 0;
      }
      array = arrays[0];
      var index = -1, seen = caches[0];
      outer:
        while (++index < length && result.length < maxLength) {
          var value = array[index], computed = iteratee ? iteratee(value) : value;
          value = comparator || value !== 0 ? value : 0;
          if (!(seen ? cacheHas2(seen, computed) : includes(result, computed, comparator))) {
            othIndex = othLength;
            while (--othIndex) {
              var cache = caches[othIndex];
              if (!(cache ? cacheHas2(cache, computed) : includes(arrays[othIndex], computed, comparator))) {
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
    module2.exports = baseIntersection;
  }
});

// node_modules/lodash/isArrayLikeObject.js
var require_isArrayLikeObject = __commonJS({
  "node_modules/lodash/isArrayLikeObject.js"(exports2, module2) {
    var isArrayLike2 = require_isArrayLike();
    var isObjectLike2 = require_isObjectLike();
    function isArrayLikeObject2(value) {
      return isObjectLike2(value) && isArrayLike2(value);
    }
    module2.exports = isArrayLikeObject2;
  }
});

// node_modules/lodash/_castArrayLikeObject.js
var require_castArrayLikeObject = __commonJS({
  "node_modules/lodash/_castArrayLikeObject.js"(exports2, module2) {
    var isArrayLikeObject2 = require_isArrayLikeObject();
    function castArrayLikeObject(value) {
      return isArrayLikeObject2(value) ? value : [];
    }
    module2.exports = castArrayLikeObject;
  }
});

// node_modules/lodash/last.js
var require_last = __commonJS({
  "node_modules/lodash/last.js"(exports2, module2) {
    function last2(array) {
      var length = array == null ? 0 : array.length;
      return length ? array[length - 1] : void 0;
    }
    module2.exports = last2;
  }
});

// node_modules/lodash/intersectionWith.js
var require_intersectionWith = __commonJS({
  "node_modules/lodash/intersectionWith.js"(exports2, module2) {
    var arrayMap2 = require_arrayMap();
    var baseIntersection = require_baseIntersection();
    var baseRest2 = require_baseRest();
    var castArrayLikeObject = require_castArrayLikeObject();
    var last2 = require_last();
    var intersectionWith = baseRest2(function(arrays) {
      var comparator = last2(arrays), mapped = arrayMap2(arrays, castArrayLikeObject);
      comparator = typeof comparator == "function" ? comparator : void 0;
      if (comparator) {
        mapped.pop();
      }
      return mapped.length && mapped[0] === arrays[0] ? baseIntersection(mapped, void 0, comparator) : [];
    });
    module2.exports = intersectionWith;
  }
});

// node_modules/lodash/isPlainObject.js
var require_isPlainObject = __commonJS({
  "node_modules/lodash/isPlainObject.js"(exports2, module2) {
    var baseGetTag2 = require_baseGetTag();
    var getPrototype2 = require_getPrototype();
    var isObjectLike2 = require_isObjectLike();
    var objectTag6 = "[object Object]";
    var funcProto4 = Function.prototype;
    var objectProto19 = Object.prototype;
    var funcToString4 = funcProto4.toString;
    var hasOwnProperty16 = objectProto19.hasOwnProperty;
    var objectCtorString2 = funcToString4.call(Object);
    function isPlainObject2(value) {
      if (!isObjectLike2(value) || baseGetTag2(value) != objectTag6) {
        return false;
      }
      var proto = getPrototype2(value);
      if (proto === null) {
        return true;
      }
      var Ctor = hasOwnProperty16.call(proto, "constructor") && proto.constructor;
      return typeof Ctor == "function" && Ctor instanceof Ctor && funcToString4.call(Ctor) == objectCtorString2;
    }
    module2.exports = isPlainObject2;
  }
});

// node_modules/lodash/isBoolean.js
var require_isBoolean = __commonJS({
  "node_modules/lodash/isBoolean.js"(exports2, module2) {
    var baseGetTag2 = require_baseGetTag();
    var isObjectLike2 = require_isObjectLike();
    var boolTag5 = "[object Boolean]";
    function isBoolean(value) {
      return value === true || value === false || isObjectLike2(value) && baseGetTag2(value) == boolTag5;
    }
    module2.exports = isBoolean;
  }
});

// node_modules/json-schema-compare/src/index.js
var require_src = __commonJS({
  "node_modules/json-schema-compare/src/index.js"(exports2, module2) {
    var isEqual2 = require_isEqual();
    var sortBy = require_sortBy();
    var uniq2 = require_uniq();
    var uniqWith = require_uniqWith();
    var defaults = require_defaults();
    var intersectionWith = require_intersectionWith();
    var isPlainObject2 = require_isPlainObject();
    var isBoolean = require_isBoolean();
    var normalizeArray = (val) => Array.isArray(val) ? val : [val];
    var undef = (val) => val === void 0;
    var keys2 = (obj) => isPlainObject2(obj) || Array.isArray(obj) ? Object.keys(obj) : [];
    var has2 = (obj, key) => obj.hasOwnProperty(key);
    var stringArray = (arr) => sortBy(uniq2(arr));
    var undefEmpty = (val) => undef(val) || Array.isArray(val) && val.length === 0;
    var keyValEqual = (a, b, key, compare2) => b && has2(b, key) && a && has2(a, key) && compare2(a[key], b[key]);
    var undefAndZero = (a, b) => undef(a) && b === 0 || undef(b) && a === 0 || isEqual2(a, b);
    var falseUndefined = (a, b) => undef(a) && b === false || undef(b) && a === false || isEqual2(a, b);
    var emptySchema = (schema) => undef(schema) || isEqual2(schema, {}) || schema === true;
    var emptyObjUndef = (schema) => undef(schema) || isEqual2(schema, {});
    var isSchema = (val) => undef(val) || isPlainObject2(val) || val === true || val === false;
    function undefArrayEqual(a, b) {
      if (undefEmpty(a) && undefEmpty(b)) {
        return true;
      } else {
        return isEqual2(stringArray(a), stringArray(b));
      }
    }
    function unsortedNormalizedArray(a, b) {
      a = normalizeArray(a);
      b = normalizeArray(b);
      return isEqual2(stringArray(a), stringArray(b));
    }
    function schemaGroup(a, b, key, compare2) {
      var allProps = uniq2(keys2(a).concat(keys2(b)));
      if (emptyObjUndef(a) && emptyObjUndef(b)) {
        return true;
      } else if (emptyObjUndef(a) && keys2(b).length) {
        return false;
      } else if (emptyObjUndef(b) && keys2(a).length) {
        return false;
      }
      return allProps.every(function(key2) {
        var aVal = a[key2];
        var bVal = b[key2];
        if (Array.isArray(aVal) && Array.isArray(bVal)) {
          return isEqual2(stringArray(a), stringArray(b));
        } else if (Array.isArray(aVal) && !Array.isArray(bVal)) {
          return false;
        } else if (Array.isArray(bVal) && !Array.isArray(aVal)) {
          return false;
        }
        return keyValEqual(a, b, key2, compare2);
      });
    }
    function items(a, b, key, compare2) {
      if (isPlainObject2(a) && isPlainObject2(b)) {
        return compare2(a, b);
      } else if (Array.isArray(a) && Array.isArray(b)) {
        return schemaGroup(a, b, key, compare2);
      } else {
        return isEqual2(a, b);
      }
    }
    function unsortedArray(a, b, key, compare2) {
      var uniqueA = uniqWith(a, compare2);
      var uniqueB = uniqWith(b, compare2);
      var inter = intersectionWith(uniqueA, uniqueB, compare2);
      return inter.length === Math.max(uniqueA.length, uniqueB.length);
    }
    var comparers = {
      title: isEqual2,
      uniqueItems: falseUndefined,
      minLength: undefAndZero,
      minItems: undefAndZero,
      minProperties: undefAndZero,
      required: undefArrayEqual,
      enum: undefArrayEqual,
      type: unsortedNormalizedArray,
      items,
      anyOf: unsortedArray,
      allOf: unsortedArray,
      oneOf: unsortedArray,
      properties: schemaGroup,
      patternProperties: schemaGroup,
      dependencies: schemaGroup
    };
    var acceptsUndefined = [
      "properties",
      "patternProperties",
      "dependencies",
      "uniqueItems",
      "minLength",
      "minItems",
      "minProperties",
      "required"
    ];
    var schemaProps = ["additionalProperties", "additionalItems", "contains", "propertyNames", "not"];
    function compare(a, b, options) {
      options = defaults(options, {
        ignore: []
      });
      if (emptySchema(a) && emptySchema(b)) {
        return true;
      }
      if (!isSchema(a) || !isSchema(b)) {
        throw new Error("Either of the values are not a JSON schema.");
      }
      if (a === b) {
        return true;
      }
      if (isBoolean(a) && isBoolean(b)) {
        return a === b;
      }
      if (a === void 0 && b === false || b === void 0 && a === false) {
        return false;
      }
      if (undef(a) && !undef(b) || !undef(a) && undef(b)) {
        return false;
      }
      var allKeys = uniq2(Object.keys(a).concat(Object.keys(b)));
      if (options.ignore.length) {
        allKeys = allKeys.filter((k) => options.ignore.indexOf(k) === -1);
      }
      if (!allKeys.length) {
        return true;
      }
      function innerCompare(a2, b2) {
        return compare(a2, b2, options);
      }
      return allKeys.every(function(key) {
        var aValue = a[key];
        var bValue = b[key];
        if (schemaProps.indexOf(key) !== -1) {
          return compare(aValue, bValue, options);
        }
        var comparer = comparers[key];
        if (!comparer) {
          comparer = isEqual2;
        }
        if (isEqual2(aValue, bValue)) {
          return true;
        }
        if (acceptsUndefined.indexOf(key) === -1) {
          if (!has2(a, key) && has2(b, key) || has2(a, key) && !has2(b, key)) {
            return aValue === bValue;
          }
        }
        var result = comparer(aValue, bValue, key, innerCompare);
        if (!isBoolean(result)) {
          throw new Error("Comparer must return true or false");
        }
        return result;
      });
    }
    module2.exports = compare;
  }
});

// node_modules/validate.io-array/lib/index.js
var require_lib = __commonJS({
  "node_modules/validate.io-array/lib/index.js"(exports2, module2) {
    "use strict";
    function isArray2(value) {
      return Object.prototype.toString.call(value) === "[object Array]";
    }
    module2.exports = Array.isArray || isArray2;
  }
});

// node_modules/validate.io-number/lib/index.js
var require_lib2 = __commonJS({
  "node_modules/validate.io-number/lib/index.js"(exports2, module2) {
    "use strict";
    function isNumber2(value) {
      return (typeof value === "number" || Object.prototype.toString.call(value) === "[object Number]") && value.valueOf() === value.valueOf();
    }
    module2.exports = isNumber2;
  }
});

// node_modules/validate.io-integer/lib/index.js
var require_lib3 = __commonJS({
  "node_modules/validate.io-integer/lib/index.js"(exports2, module2) {
    "use strict";
    var isNumber2 = require_lib2();
    function isInteger(value) {
      return isNumber2(value) && value % 1 === 0;
    }
    module2.exports = isInteger;
  }
});

// node_modules/validate.io-integer-array/lib/index.js
var require_lib4 = __commonJS({
  "node_modules/validate.io-integer-array/lib/index.js"(exports2, module2) {
    "use strict";
    var isArray2 = require_lib();
    var isInteger = require_lib3();
    function isIntegerArray(value) {
      var len;
      if (!isArray2(value)) {
        return false;
      }
      len = value.length;
      if (!len) {
        return false;
      }
      for (var i = 0; i < len; i++) {
        if (!isInteger(value[i])) {
          return false;
        }
      }
      return true;
    }
    module2.exports = isIntegerArray;
  }
});

// node_modules/validate.io-function/lib/index.js
var require_lib5 = __commonJS({
  "node_modules/validate.io-function/lib/index.js"(exports2, module2) {
    "use strict";
    function isFunction2(value) {
      return typeof value === "function";
    }
    module2.exports = isFunction2;
  }
});

// node_modules/compute-gcd/lib/index.js
var require_lib6 = __commonJS({
  "node_modules/compute-gcd/lib/index.js"(exports2, module2) {
    "use strict";
    var isArray2 = require_lib();
    var isIntegerArray = require_lib4();
    var isFunction2 = require_lib5();
    var MAXINT = Math.pow(2, 31) - 1;
    function gcd(a, b) {
      var k = 1, t;
      if (a === 0) {
        return b;
      }
      if (b === 0) {
        return a;
      }
      while (a % 2 === 0 && b % 2 === 0) {
        a = a / 2;
        b = b / 2;
        k = k * 2;
      }
      while (a % 2 === 0) {
        a = a / 2;
      }
      while (b) {
        while (b % 2 === 0) {
          b = b / 2;
        }
        if (a > b) {
          t = b;
          b = a;
          a = t;
        }
        b = b - a;
      }
      return k * a;
    }
    function bitwise(a, b) {
      var k = 0, t;
      if (a === 0) {
        return b;
      }
      if (b === 0) {
        return a;
      }
      while ((a & 1) === 0 && (b & 1) === 0) {
        a >>>= 1;
        b >>>= 1;
        k++;
      }
      while ((a & 1) === 0) {
        a >>>= 1;
      }
      while (b) {
        while ((b & 1) === 0) {
          b >>>= 1;
        }
        if (a > b) {
          t = b;
          b = a;
          a = t;
        }
        b = b - a;
      }
      return a << k;
    }
    function compute() {
      var nargs = arguments.length, args, clbk, arr, len, a, b, i;
      args = new Array(nargs);
      for (i = 0; i < nargs; i++) {
        args[i] = arguments[i];
      }
      if (isIntegerArray(args)) {
        if (nargs === 2) {
          a = args[0];
          b = args[1];
          if (a < 0) {
            a = -a;
          }
          if (b < 0) {
            b = -b;
          }
          if (a <= MAXINT && b <= MAXINT) {
            return bitwise(a, b);
          } else {
            return gcd(a, b);
          }
        }
        arr = args;
      } else if (!isArray2(args[0])) {
        throw new TypeError("gcd()::invalid input argument. Must provide an array of integers. Value: `" + args[0] + "`.");
      } else if (nargs > 1) {
        arr = args[0];
        clbk = args[1];
        if (!isFunction2(clbk)) {
          throw new TypeError("gcd()::invalid input argument. Accessor must be a function. Value: `" + clbk + "`.");
        }
      } else {
        arr = args[0];
      }
      len = arr.length;
      if (len < 2) {
        return null;
      }
      if (clbk) {
        a = new Array(len);
        for (i = 0; i < len; i++) {
          a[i] = clbk(arr[i], i);
        }
        arr = a;
      }
      if (nargs < 3) {
        if (!isIntegerArray(arr)) {
          throw new TypeError("gcd()::invalid input argument. Accessed array values must be integers. Value: `" + arr + "`.");
        }
      }
      for (i = 0; i < len; i++) {
        a = arr[i];
        if (a < 0) {
          arr[i] = -a;
        }
      }
      a = arr[0];
      for (i = 1; i < len; i++) {
        b = arr[i];
        if (b <= MAXINT && a <= MAXINT) {
          a = bitwise(a, b);
        } else {
          a = gcd(a, b);
        }
      }
      return a;
    }
    module2.exports = compute;
  }
});

// node_modules/compute-lcm/lib/index.js
var require_lib7 = __commonJS({
  "node_modules/compute-lcm/lib/index.js"(exports2, module2) {
    "use strict";
    var gcd = require_lib6();
    var isArray2 = require_lib();
    var isIntegerArray = require_lib4();
    var isFunction2 = require_lib5();
    function lcm() {
      var nargs = arguments.length, args, clbk, arr, len, a, b, i;
      args = new Array(nargs);
      for (i = 0; i < nargs; i++) {
        args[i] = arguments[i];
      }
      if (isIntegerArray(args)) {
        if (nargs === 2) {
          a = args[0];
          b = args[1];
          if (a < 0) {
            a = -a;
          }
          if (b < 0) {
            b = -b;
          }
          if (a === 0 || b === 0) {
            return 0;
          }
          return a / gcd(a, b) * b;
        }
        arr = args;
      } else if (!isArray2(args[0])) {
        throw new TypeError("lcm()::invalid input argument. Must provide an array of integers. Value: `" + args[0] + "`.");
      } else if (nargs > 1) {
        arr = args[0];
        clbk = args[1];
        if (!isFunction2(clbk)) {
          throw new TypeError("lcm()::invalid input argument. Accessor must be a function. Value: `" + clbk + "`.");
        }
      } else {
        arr = args[0];
      }
      len = arr.length;
      if (len < 2) {
        return null;
      }
      if (clbk) {
        a = new Array(len);
        for (i = 0; i < len; i++) {
          a[i] = clbk(arr[i], i);
        }
        arr = a;
      }
      if (nargs < 3) {
        if (!isIntegerArray(arr)) {
          throw new TypeError("lcm()::invalid input argument. Accessed array values must be integers. Value: `" + arr + "`.");
        }
      }
      for (i = 0; i < len; i++) {
        a = arr[i];
        if (a < 0) {
          arr[i] = -a;
        }
      }
      a = arr[0];
      for (i = 1; i < len; i++) {
        b = arr[i];
        if (a === 0 || b === 0) {
          return 0;
        }
        a = a / gcd(a, b) * b;
      }
      return a;
    }
    module2.exports = lcm;
  }
});

// node_modules/lodash/_assignMergeValue.js
var require_assignMergeValue = __commonJS({
  "node_modules/lodash/_assignMergeValue.js"(exports2, module2) {
    var baseAssignValue2 = require_baseAssignValue();
    var eq2 = require_eq();
    function assignMergeValue2(object, key, value) {
      if (value !== void 0 && !eq2(object[key], value) || value === void 0 && !(key in object)) {
        baseAssignValue2(object, key, value);
      }
    }
    module2.exports = assignMergeValue2;
  }
});

// node_modules/lodash/_safeGet.js
var require_safeGet = __commonJS({
  "node_modules/lodash/_safeGet.js"(exports2, module2) {
    function safeGet2(object, key) {
      if (key === "constructor" && typeof object[key] === "function") {
        return;
      }
      if (key == "__proto__") {
        return;
      }
      return object[key];
    }
    module2.exports = safeGet2;
  }
});

// node_modules/lodash/toPlainObject.js
var require_toPlainObject = __commonJS({
  "node_modules/lodash/toPlainObject.js"(exports2, module2) {
    var copyObject2 = require_copyObject();
    var keysIn2 = require_keysIn();
    function toPlainObject2(value) {
      return copyObject2(value, keysIn2(value));
    }
    module2.exports = toPlainObject2;
  }
});

// node_modules/lodash/_baseMergeDeep.js
var require_baseMergeDeep = __commonJS({
  "node_modules/lodash/_baseMergeDeep.js"(exports2, module2) {
    var assignMergeValue2 = require_assignMergeValue();
    var cloneBuffer2 = require_cloneBuffer();
    var cloneTypedArray2 = require_cloneTypedArray();
    var copyArray2 = require_copyArray();
    var initCloneObject2 = require_initCloneObject();
    var isArguments2 = require_isArguments();
    var isArray2 = require_isArray();
    var isArrayLikeObject2 = require_isArrayLikeObject();
    var isBuffer2 = require_isBuffer();
    var isFunction2 = require_isFunction();
    var isObject3 = require_isObject();
    var isPlainObject2 = require_isPlainObject();
    var isTypedArray2 = require_isTypedArray();
    var safeGet2 = require_safeGet();
    var toPlainObject2 = require_toPlainObject();
    function baseMergeDeep2(object, source, key, srcIndex, mergeFunc, customizer, stack) {
      var objValue = safeGet2(object, key), srcValue = safeGet2(source, key), stacked = stack.get(srcValue);
      if (stacked) {
        assignMergeValue2(object, key, stacked);
        return;
      }
      var newValue = customizer ? customizer(objValue, srcValue, key + "", object, source, stack) : void 0;
      var isCommon = newValue === void 0;
      if (isCommon) {
        var isArr = isArray2(srcValue), isBuff = !isArr && isBuffer2(srcValue), isTyped = !isArr && !isBuff && isTypedArray2(srcValue);
        newValue = srcValue;
        if (isArr || isBuff || isTyped) {
          if (isArray2(objValue)) {
            newValue = objValue;
          } else if (isArrayLikeObject2(objValue)) {
            newValue = copyArray2(objValue);
          } else if (isBuff) {
            isCommon = false;
            newValue = cloneBuffer2(srcValue, true);
          } else if (isTyped) {
            isCommon = false;
            newValue = cloneTypedArray2(srcValue, true);
          } else {
            newValue = [];
          }
        } else if (isPlainObject2(srcValue) || isArguments2(srcValue)) {
          newValue = objValue;
          if (isArguments2(objValue)) {
            newValue = toPlainObject2(objValue);
          } else if (!isObject3(objValue) || isFunction2(objValue)) {
            newValue = initCloneObject2(srcValue);
          }
        } else {
          isCommon = false;
        }
      }
      if (isCommon) {
        stack.set(srcValue, newValue);
        mergeFunc(newValue, srcValue, srcIndex, customizer, stack);
        stack["delete"](srcValue);
      }
      assignMergeValue2(object, key, newValue);
    }
    module2.exports = baseMergeDeep2;
  }
});

// node_modules/lodash/_baseMerge.js
var require_baseMerge = __commonJS({
  "node_modules/lodash/_baseMerge.js"(exports2, module2) {
    var Stack2 = require_Stack();
    var assignMergeValue2 = require_assignMergeValue();
    var baseFor2 = require_baseFor();
    var baseMergeDeep2 = require_baseMergeDeep();
    var isObject3 = require_isObject();
    var keysIn2 = require_keysIn();
    var safeGet2 = require_safeGet();
    function baseMerge2(object, source, srcIndex, customizer, stack) {
      if (object === source) {
        return;
      }
      baseFor2(source, function(srcValue, key) {
        stack || (stack = new Stack2());
        if (isObject3(srcValue)) {
          baseMergeDeep2(object, source, key, srcIndex, baseMerge2, customizer, stack);
        } else {
          var newValue = customizer ? customizer(safeGet2(object, key), srcValue, key + "", object, source, stack) : void 0;
          if (newValue === void 0) {
            newValue = srcValue;
          }
          assignMergeValue2(object, key, newValue);
        }
      }, keysIn2);
    }
    module2.exports = baseMerge2;
  }
});

// node_modules/lodash/_customDefaultsMerge.js
var require_customDefaultsMerge = __commonJS({
  "node_modules/lodash/_customDefaultsMerge.js"(exports2, module2) {
    var baseMerge2 = require_baseMerge();
    var isObject3 = require_isObject();
    function customDefaultsMerge(objValue, srcValue, key, object, source, stack) {
      if (isObject3(objValue) && isObject3(srcValue)) {
        stack.set(srcValue, objValue);
        baseMerge2(objValue, srcValue, void 0, customDefaultsMerge, stack);
        stack["delete"](srcValue);
      }
      return objValue;
    }
    module2.exports = customDefaultsMerge;
  }
});

// node_modules/lodash/_createAssigner.js
var require_createAssigner = __commonJS({
  "node_modules/lodash/_createAssigner.js"(exports2, module2) {
    var baseRest2 = require_baseRest();
    var isIterateeCall2 = require_isIterateeCall();
    function createAssigner2(assigner) {
      return baseRest2(function(object, sources) {
        var index = -1, length = sources.length, customizer = length > 1 ? sources[length - 1] : void 0, guard = length > 2 ? sources[2] : void 0;
        customizer = assigner.length > 3 && typeof customizer == "function" ? (length--, customizer) : void 0;
        if (guard && isIterateeCall2(sources[0], sources[1], guard)) {
          customizer = length < 3 ? void 0 : customizer;
          length = 1;
        }
        object = Object(object);
        while (++index < length) {
          var source = sources[index];
          if (source) {
            assigner(object, source, index, customizer);
          }
        }
        return object;
      });
    }
    module2.exports = createAssigner2;
  }
});

// node_modules/lodash/mergeWith.js
var require_mergeWith = __commonJS({
  "node_modules/lodash/mergeWith.js"(exports2, module2) {
    var baseMerge2 = require_baseMerge();
    var createAssigner2 = require_createAssigner();
    var mergeWith = createAssigner2(function(object, source, srcIndex, customizer) {
      baseMerge2(object, source, srcIndex, customizer);
    });
    module2.exports = mergeWith;
  }
});

// node_modules/lodash/defaultsDeep.js
var require_defaultsDeep = __commonJS({
  "node_modules/lodash/defaultsDeep.js"(exports2, module2) {
    var apply2 = require_apply();
    var baseRest2 = require_baseRest();
    var customDefaultsMerge = require_customDefaultsMerge();
    var mergeWith = require_mergeWith();
    var defaultsDeep = baseRest2(function(args) {
      args.push(void 0, customDefaultsMerge);
      return apply2(mergeWith, void 0, args);
    });
    module2.exports = defaultsDeep;
  }
});

// node_modules/lodash/flatten.js
var require_flatten = __commonJS({
  "node_modules/lodash/flatten.js"(exports2, module2) {
    var baseFlatten2 = require_baseFlatten();
    function flatten2(array) {
      var length = array == null ? 0 : array.length;
      return length ? baseFlatten2(array, 1) : [];
    }
    module2.exports = flatten2;
  }
});

// node_modules/lodash/flattenDeep.js
var require_flattenDeep = __commonJS({
  "node_modules/lodash/flattenDeep.js"(exports2, module2) {
    var baseFlatten2 = require_baseFlatten();
    var INFINITY6 = 1 / 0;
    function flattenDeep2(array) {
      var length = array == null ? 0 : array.length;
      return length ? baseFlatten2(array, INFINITY6) : [];
    }
    module2.exports = flattenDeep2;
  }
});

// node_modules/lodash/intersection.js
var require_intersection = __commonJS({
  "node_modules/lodash/intersection.js"(exports2, module2) {
    var arrayMap2 = require_arrayMap();
    var baseIntersection = require_baseIntersection();
    var baseRest2 = require_baseRest();
    var castArrayLikeObject = require_castArrayLikeObject();
    var intersection = baseRest2(function(arrays) {
      var mapped = arrayMap2(arrays, castArrayLikeObject);
      return mapped.length && mapped[0] === arrays[0] ? baseIntersection(mapped) : [];
    });
    module2.exports = intersection;
  }
});

// node_modules/lodash/_baseIndexOfWith.js
var require_baseIndexOfWith = __commonJS({
  "node_modules/lodash/_baseIndexOfWith.js"(exports2, module2) {
    function baseIndexOfWith(array, value, fromIndex, comparator) {
      var index = fromIndex - 1, length = array.length;
      while (++index < length) {
        if (comparator(array[index], value)) {
          return index;
        }
      }
      return -1;
    }
    module2.exports = baseIndexOfWith;
  }
});

// node_modules/lodash/_basePullAll.js
var require_basePullAll = __commonJS({
  "node_modules/lodash/_basePullAll.js"(exports2, module2) {
    var arrayMap2 = require_arrayMap();
    var baseIndexOf2 = require_baseIndexOf();
    var baseIndexOfWith = require_baseIndexOfWith();
    var baseUnary2 = require_baseUnary();
    var copyArray2 = require_copyArray();
    var arrayProto2 = Array.prototype;
    var splice2 = arrayProto2.splice;
    function basePullAll(array, values, iteratee, comparator) {
      var indexOf = comparator ? baseIndexOfWith : baseIndexOf2, index = -1, length = values.length, seen = array;
      if (array === values) {
        values = copyArray2(values);
      }
      if (iteratee) {
        seen = arrayMap2(array, baseUnary2(iteratee));
      }
      while (++index < length) {
        var fromIndex = 0, value = values[index], computed = iteratee ? iteratee(value) : value;
        while ((fromIndex = indexOf(seen, computed, fromIndex, comparator)) > -1) {
          if (seen !== array) {
            splice2.call(seen, fromIndex, 1);
          }
          splice2.call(array, fromIndex, 1);
        }
      }
      return array;
    }
    module2.exports = basePullAll;
  }
});

// node_modules/lodash/pullAll.js
var require_pullAll = __commonJS({
  "node_modules/lodash/pullAll.js"(exports2, module2) {
    var basePullAll = require_basePullAll();
    function pullAll(array, values) {
      return array && array.length && values && values.length ? basePullAll(array, values) : array;
    }
    module2.exports = pullAll;
  }
});

// node_modules/lodash/_castFunction.js
var require_castFunction = __commonJS({
  "node_modules/lodash/_castFunction.js"(exports2, module2) {
    var identity2 = require_identity();
    function castFunction2(value) {
      return typeof value == "function" ? value : identity2;
    }
    module2.exports = castFunction2;
  }
});

// node_modules/lodash/forEach.js
var require_forEach = __commonJS({
  "node_modules/lodash/forEach.js"(exports2, module2) {
    var arrayEach2 = require_arrayEach();
    var baseEach2 = require_baseEach();
    var castFunction2 = require_castFunction();
    var isArray2 = require_isArray();
    function forEach2(collection, iteratee) {
      var func = isArray2(collection) ? arrayEach2 : baseEach2;
      return func(collection, castFunction2(iteratee));
    }
    module2.exports = forEach2;
  }
});

// node_modules/lodash/_baseDifference.js
var require_baseDifference = __commonJS({
  "node_modules/lodash/_baseDifference.js"(exports2, module2) {
    var SetCache2 = require_SetCache();
    var arrayIncludes2 = require_arrayIncludes();
    var arrayIncludesWith2 = require_arrayIncludesWith();
    var arrayMap2 = require_arrayMap();
    var baseUnary2 = require_baseUnary();
    var cacheHas2 = require_cacheHas();
    var LARGE_ARRAY_SIZE4 = 200;
    function baseDifference2(array, values, iteratee, comparator) {
      var index = -1, includes = arrayIncludes2, isCommon = true, length = array.length, result = [], valuesLength = values.length;
      if (!length) {
        return result;
      }
      if (iteratee) {
        values = arrayMap2(values, baseUnary2(iteratee));
      }
      if (comparator) {
        includes = arrayIncludesWith2;
        isCommon = false;
      } else if (values.length >= LARGE_ARRAY_SIZE4) {
        includes = cacheHas2;
        isCommon = false;
        values = new SetCache2(values);
      }
      outer:
        while (++index < length) {
          var value = array[index], computed = iteratee == null ? value : iteratee(value);
          value = comparator || value !== 0 ? value : 0;
          if (isCommon && computed === computed) {
            var valuesIndex = valuesLength;
            while (valuesIndex--) {
              if (values[valuesIndex] === computed) {
                continue outer;
              }
            }
            result.push(value);
          } else if (!includes(values, computed, comparator)) {
            result.push(value);
          }
        }
      return result;
    }
    module2.exports = baseDifference2;
  }
});

// node_modules/lodash/without.js
var require_without = __commonJS({
  "node_modules/lodash/without.js"(exports2, module2) {
    var baseDifference2 = require_baseDifference();
    var baseRest2 = require_baseRest();
    var isArrayLikeObject2 = require_isArrayLikeObject();
    var without = baseRest2(function(array, values) {
      return isArrayLikeObject2(array) ? baseDifference2(array, values) : [];
    });
    module2.exports = without;
  }
});

// node_modules/json-schema-merge-allof/src/common.js
var require_common = __commonJS({
  "node_modules/json-schema-merge-allof/src/common.js"(exports2, module2) {
    var flatten2 = require_flatten();
    var flattenDeep2 = require_flattenDeep();
    var isPlainObject2 = require_isPlainObject();
    var uniq2 = require_uniq();
    var uniqWith = require_uniqWith();
    var without = require_without();
    function deleteUndefinedProps(returnObject) {
      for (const prop in returnObject) {
        if (has2(returnObject, prop) && isEmptySchema(returnObject[prop])) {
          delete returnObject[prop];
        }
      }
      return returnObject;
    }
    var allUniqueKeys = (arr) => uniq2(flattenDeep2(arr.map(keys2)));
    var getValues = (schemas, key) => schemas.map((schema) => schema && schema[key]);
    var has2 = (obj, propName) => Object.prototype.hasOwnProperty.call(obj, propName);
    var keys2 = (obj) => {
      if (isPlainObject2(obj) || Array.isArray(obj)) {
        return Object.keys(obj);
      } else {
        return [];
      }
    };
    var notUndefined = (val) => val !== void 0;
    var isSchema = (val) => isPlainObject2(val) || val === true || val === false;
    var isEmptySchema = (obj) => !keys2(obj).length && obj !== false && obj !== true;
    var withoutArr = (arr, ...rest) => without.apply(null, [arr].concat(flatten2(rest)));
    module2.exports = {
      allUniqueKeys,
      deleteUndefinedProps,
      getValues,
      has: has2,
      isEmptySchema,
      isSchema,
      keys: keys2,
      notUndefined,
      uniqWith,
      withoutArr
    };
  }
});

// node_modules/json-schema-merge-allof/src/complex-resolvers/properties.js
var require_properties = __commonJS({
  "node_modules/json-schema-merge-allof/src/complex-resolvers/properties.js"(exports2, module2) {
    var compare = require_src();
    var forEach2 = require_forEach();
    var {
      allUniqueKeys,
      deleteUndefinedProps,
      getValues,
      keys: keys2,
      notUndefined,
      uniqWith,
      withoutArr
    } = require_common();
    function removeFalseSchemas(target) {
      forEach2(target, function(schema, prop) {
        if (schema === false) {
          delete target[prop];
        }
      });
    }
    function mergeSchemaGroup(group, mergeSchemas2) {
      const allKeys = allUniqueKeys(group);
      return allKeys.reduce(function(all, key) {
        const schemas = getValues(group, key);
        const compacted = uniqWith(schemas.filter(notUndefined), compare);
        all[key] = mergeSchemas2(compacted, key);
        return all;
      }, {});
    }
    module2.exports = {
      keywords: ["properties", "patternProperties", "additionalProperties"],
      resolver(values, parents, mergers, options) {
        if (!options.ignoreAdditionalProperties) {
          values.forEach(function(subSchema) {
            const otherSubSchemas = values.filter((s) => s !== subSchema);
            const ownKeys = keys2(subSchema.properties);
            const ownPatternKeys = keys2(subSchema.patternProperties);
            const ownPatterns = ownPatternKeys.map((k) => new RegExp(k));
            otherSubSchemas.forEach(function(other) {
              const allOtherKeys = keys2(other.properties);
              const keysMatchingPattern = allOtherKeys.filter((k) => ownPatterns.some((pk) => pk.test(k)));
              const additionalKeys = withoutArr(allOtherKeys, ownKeys, keysMatchingPattern);
              additionalKeys.forEach(function(key) {
                other.properties[key] = mergers.properties([
                  other.properties[key],
                  subSchema.additionalProperties
                ], key);
              });
            });
          });
          values.forEach(function(subSchema) {
            const otherSubSchemas = values.filter((s) => s !== subSchema);
            const ownPatternKeys = keys2(subSchema.patternProperties);
            if (subSchema.additionalProperties === false) {
              otherSubSchemas.forEach(function(other) {
                const allOtherPatterns = keys2(other.patternProperties);
                const additionalPatternKeys = withoutArr(allOtherPatterns, ownPatternKeys);
                additionalPatternKeys.forEach((key) => delete other.patternProperties[key]);
              });
            }
          });
        }
        const returnObject = {
          additionalProperties: mergers.additionalProperties(values.map((s) => s.additionalProperties)),
          patternProperties: mergeSchemaGroup(values.map((s) => s.patternProperties), mergers.patternProperties),
          properties: mergeSchemaGroup(values.map((s) => s.properties), mergers.properties)
        };
        if (returnObject.additionalProperties === false) {
          removeFalseSchemas(returnObject.properties);
        }
        return deleteUndefinedProps(returnObject);
      }
    };
  }
});

// node_modules/json-schema-merge-allof/src/complex-resolvers/items.js
var require_items = __commonJS({
  "node_modules/json-schema-merge-allof/src/complex-resolvers/items.js"(exports2, module2) {
    var compare = require_src();
    var forEach2 = require_forEach();
    var {
      allUniqueKeys,
      deleteUndefinedProps,
      has: has2,
      isSchema,
      notUndefined,
      uniqWith
    } = require_common();
    function removeFalseSchemasFromArray(target) {
      forEach2(target, function(schema, index) {
        if (schema === false) {
          target.splice(index, 1);
        }
      });
    }
    function getItemSchemas(subSchemas, key) {
      return subSchemas.map(function(sub) {
        if (!sub) {
          return void 0;
        }
        if (Array.isArray(sub.items)) {
          const schemaAtPos = sub.items[key];
          if (isSchema(schemaAtPos)) {
            return schemaAtPos;
          } else if (has2(sub, "additionalItems")) {
            return sub.additionalItems;
          }
        } else {
          return sub.items;
        }
        return void 0;
      });
    }
    function getAdditionalSchemas(subSchemas) {
      return subSchemas.map(function(sub) {
        if (!sub) {
          return void 0;
        }
        if (Array.isArray(sub.items)) {
          return sub.additionalItems;
        }
        return sub.items;
      });
    }
    function mergeItems(group, mergeSchemas2, items) {
      const allKeys = allUniqueKeys(items);
      return allKeys.reduce(function(all, key) {
        const schemas = getItemSchemas(group, key);
        const compacted = uniqWith(schemas.filter(notUndefined), compare);
        all[key] = mergeSchemas2(compacted, key);
        return all;
      }, []);
    }
    module2.exports = {
      keywords: ["items", "additionalItems"],
      resolver(values, parents, mergers) {
        const items = values.map((s) => s.items);
        const itemsCompacted = items.filter(notUndefined);
        const returnObject = {};
        if (itemsCompacted.every(isSchema)) {
          returnObject.items = mergers.items(items);
        } else {
          returnObject.items = mergeItems(values, mergers.items, items);
        }
        let schemasAtLastPos;
        if (itemsCompacted.every(Array.isArray)) {
          schemasAtLastPos = values.map((s) => s.additionalItems);
        } else if (itemsCompacted.some(Array.isArray)) {
          schemasAtLastPos = getAdditionalSchemas(values);
        }
        if (schemasAtLastPos) {
          returnObject.additionalItems = mergers.additionalItems(schemasAtLastPos);
        }
        if (returnObject.additionalItems === false && Array.isArray(returnObject.items)) {
          removeFalseSchemasFromArray(returnObject.items);
        }
        return deleteUndefinedProps(returnObject);
      }
    };
  }
});

// node_modules/json-schema-merge-allof/src/index.js
var require_src2 = __commonJS({
  "node_modules/json-schema-merge-allof/src/index.js"(exports2, module2) {
    var cloneDeep2 = require_cloneDeep();
    var compare = require_src();
    var computeLcm = require_lib7();
    var defaultsDeep = require_defaultsDeep();
    var flatten2 = require_flatten();
    var flattenDeep2 = require_flattenDeep();
    var intersection = require_intersection();
    var intersectionWith = require_intersectionWith();
    var isEqual2 = require_isEqual();
    var isPlainObject2 = require_isPlainObject();
    var pullAll = require_pullAll();
    var sortBy = require_sortBy();
    var uniq2 = require_uniq();
    var uniqWith = require_uniqWith();
    var propertiesResolver = require_properties();
    var itemsResolver = require_items();
    var contains = (arr, val) => arr.indexOf(val) !== -1;
    var isSchema = (val) => isPlainObject2(val) || val === true || val === false;
    var isFalse = (val) => val === false;
    var isTrue = (val) => val === true;
    var schemaResolver = (compacted, key, mergeSchemas2) => mergeSchemas2(compacted);
    var stringArray = (values) => sortBy(uniq2(flattenDeep2(values)));
    var notUndefined = (val) => val !== void 0;
    var allUniqueKeys = (arr) => uniq2(flattenDeep2(arr.map(keys2)));
    var first = (compacted) => compacted[0];
    var required = (compacted) => stringArray(compacted);
    var maximumValue = (compacted) => Math.max.apply(Math, compacted);
    var minimumValue = (compacted) => Math.min.apply(Math, compacted);
    var uniqueItems = (compacted) => compacted.some(isTrue);
    var examples = (compacted) => uniqWith(flatten2(compacted), isEqual2);
    function compareProp(key) {
      return function(a, b) {
        return compare({
          [key]: a
        }, { [key]: b });
      };
    }
    function getAllOf(schema) {
      let { allOf = [], ...copy } = schema;
      copy = isPlainObject2(schema) ? copy : schema;
      return [copy, ...allOf.map(getAllOf)];
    }
    function getValues(schemas, key) {
      return schemas.map((schema) => schema && schema[key]);
    }
    function tryMergeSchemaGroups(schemaGroups, mergeSchemas2) {
      return schemaGroups.map(function(schemas, index) {
        try {
          return mergeSchemas2(schemas, index);
        } catch (e) {
          return void 0;
        }
      }).filter(notUndefined);
    }
    function keys2(obj) {
      if (isPlainObject2(obj) || Array.isArray(obj)) {
        return Object.keys(obj);
      } else {
        return [];
      }
    }
    function getAnyOfCombinations(arrOfArrays, combinations) {
      combinations = combinations || [];
      if (!arrOfArrays.length) {
        return combinations;
      }
      const values = arrOfArrays.slice(0).shift();
      const rest = arrOfArrays.slice(1);
      if (combinations.length) {
        return getAnyOfCombinations(rest, flatten2(combinations.map((combination) => values.map((item) => [item].concat(combination)))));
      }
      return getAnyOfCombinations(rest, values.map((item) => item));
    }
    function throwIncompatible(values, paths) {
      let asJSON;
      try {
        asJSON = values.map(function(val) {
          return JSON.stringify(val, null, 2);
        }).join("\n");
      } catch (variable) {
        asJSON = values.join(", ");
      }
      throw new Error('Could not resolve values for path:"' + paths.join(".") + '". They are probably incompatible. Values: \n' + asJSON);
    }
    function callGroupResolver(complexKeywords, resolverName, schemas, mergeSchemas2, options, parents) {
      if (complexKeywords.length) {
        const resolverConfig = options.complexResolvers[resolverName];
        if (!resolverConfig || !resolverConfig.resolver) {
          throw new Error("No resolver found for " + resolverName);
        }
        const extractedKeywordsOnly = schemas.map((schema) => complexKeywords.reduce((all, key) => {
          if (schema[key] !== void 0) all[key] = schema[key];
          return all;
        }, {}));
        const unique = uniqWith(extractedKeywordsOnly, compare);
        const mergers = resolverConfig.keywords.reduce((all, key) => ({
          ...all,
          [key]: (schemas2, extraKey = []) => mergeSchemas2(schemas2, null, parents.concat(key, extraKey))
        }), {});
        const result = resolverConfig.resolver(unique, parents.concat(resolverName), mergers, options);
        if (!isPlainObject2(result)) {
          throwIncompatible(unique, parents.concat(resolverName));
        }
        return result;
      }
    }
    function createRequiredMetaArray(arr) {
      return { required: arr };
    }
    var schemaGroupProps = ["properties", "patternProperties", "definitions", "dependencies"];
    var schemaArrays = ["anyOf", "oneOf"];
    var schemaProps = [
      "additionalProperties",
      "additionalItems",
      "contains",
      "propertyNames",
      "not",
      "items"
    ];
    var defaultResolvers = {
      type(compacted) {
        if (compacted.some(Array.isArray)) {
          const normalized = compacted.map(function(val) {
            return Array.isArray(val) ? val : [val];
          });
          const common = intersection.apply(null, normalized);
          if (common.length === 1) {
            return common[0];
          } else if (common.length > 1) {
            return uniq2(common);
          }
        }
      },
      dependencies(compacted, paths, mergeSchemas2) {
        const allChildren = allUniqueKeys(compacted);
        return allChildren.reduce(function(all, childKey) {
          const childSchemas = getValues(compacted, childKey);
          let innerCompacted = uniqWith(childSchemas.filter(notUndefined), isEqual2);
          const innerArrays = innerCompacted.filter(Array.isArray);
          if (innerArrays.length) {
            if (innerArrays.length === innerCompacted.length) {
              all[childKey] = stringArray(innerCompacted);
            } else {
              const innerSchemas = innerCompacted.filter(isSchema);
              const arrayMetaScheams = innerArrays.map(createRequiredMetaArray);
              all[childKey] = mergeSchemas2(innerSchemas.concat(arrayMetaScheams), childKey);
            }
            return all;
          }
          innerCompacted = uniqWith(innerCompacted, compare);
          all[childKey] = mergeSchemas2(innerCompacted, childKey);
          return all;
        }, {});
      },
      oneOf(compacted, paths, mergeSchemas2) {
        const combinations = getAnyOfCombinations(cloneDeep2(compacted));
        const result = tryMergeSchemaGroups(combinations, mergeSchemas2);
        const unique = uniqWith(result, compare);
        if (unique.length) {
          return unique;
        }
      },
      not(compacted) {
        return { anyOf: compacted };
      },
      pattern(compacted) {
        return compacted.map((r) => "(?=" + r + ")").join("");
      },
      multipleOf(compacted) {
        let integers = compacted.slice(0);
        let factor = 1;
        while (integers.some((n) => !Number.isInteger(n))) {
          integers = integers.map((n) => n * 10);
          factor = factor * 10;
        }
        return computeLcm(integers) / factor;
      },
      enum(compacted) {
        const enums = intersectionWith.apply(null, compacted.concat(isEqual2));
        if (enums.length) {
          return sortBy(enums);
        }
      }
    };
    defaultResolvers.$id = first;
    defaultResolvers.$ref = first;
    defaultResolvers.$schema = first;
    defaultResolvers.additionalItems = schemaResolver;
    defaultResolvers.additionalProperties = schemaResolver;
    defaultResolvers.anyOf = defaultResolvers.oneOf;
    defaultResolvers.contains = schemaResolver;
    defaultResolvers.default = first;
    defaultResolvers.definitions = defaultResolvers.dependencies;
    defaultResolvers.description = first;
    defaultResolvers.examples = examples;
    defaultResolvers.exclusiveMaximum = minimumValue;
    defaultResolvers.exclusiveMinimum = maximumValue;
    defaultResolvers.items = itemsResolver;
    defaultResolvers.maximum = minimumValue;
    defaultResolvers.maxItems = minimumValue;
    defaultResolvers.maxLength = minimumValue;
    defaultResolvers.maxProperties = minimumValue;
    defaultResolvers.minimum = maximumValue;
    defaultResolvers.minItems = maximumValue;
    defaultResolvers.minLength = maximumValue;
    defaultResolvers.minProperties = maximumValue;
    defaultResolvers.properties = propertiesResolver;
    defaultResolvers.propertyNames = schemaResolver;
    defaultResolvers.required = required;
    defaultResolvers.title = first;
    defaultResolvers.uniqueItems = uniqueItems;
    var defaultComplexResolvers = {
      properties: propertiesResolver,
      items: itemsResolver
    };
    function merger(rootSchema, options, totalSchemas) {
      totalSchemas = totalSchemas || [];
      options = defaultsDeep(options, {
        ignoreAdditionalProperties: false,
        resolvers: defaultResolvers,
        complexResolvers: defaultComplexResolvers,
        deep: true
      });
      const complexResolvers = Object.entries(options.complexResolvers);
      function mergeSchemas2(schemas, base, parents) {
        schemas = cloneDeep2(schemas.filter(notUndefined));
        parents = parents || [];
        const merged2 = isPlainObject2(base) ? base : {};
        if (!schemas.length) {
          return;
        }
        if (schemas.some(isFalse)) {
          return false;
        }
        if (schemas.every(isTrue)) {
          return true;
        }
        schemas = schemas.filter(isPlainObject2);
        const allKeys = allUniqueKeys(schemas);
        if (options.deep && contains(allKeys, "allOf")) {
          return merger({
            allOf: schemas
          }, options, totalSchemas);
        }
        const complexKeysArr = complexResolvers.map(([mainKeyWord, resolverConf]) => allKeys.filter((k) => resolverConf.keywords.includes(k)));
        complexKeysArr.forEach((keys3) => pullAll(allKeys, keys3));
        allKeys.forEach(function(key) {
          const values = getValues(schemas, key);
          const compacted = uniqWith(values.filter(notUndefined), compareProp(key));
          if (compacted.length === 1 && contains(schemaArrays, key)) {
            merged2[key] = compacted[0].map((schema) => mergeSchemas2([schema], schema));
          } else if (compacted.length === 1 && !contains(schemaGroupProps, key) && !contains(schemaProps, key)) {
            merged2[key] = compacted[0];
          } else {
            const resolver = options.resolvers[key] || options.resolvers.defaultResolver;
            if (!resolver) throw new Error("No resolver found for key " + key + ". You can provide a resolver for this keyword in the options, or provide a default resolver.");
            const merger2 = (schemas2, extraKey = []) => mergeSchemas2(schemas2, null, parents.concat(key, extraKey));
            merged2[key] = resolver(compacted, parents.concat(key), merger2, options);
            if (merged2[key] === void 0) {
              throwIncompatible(compacted, parents.concat(key));
            } else if (merged2[key] === void 0) {
              delete merged2[key];
            }
          }
        });
        return complexResolvers.reduce((all, [resolverKeyword, config], index) => ({
          ...all,
          ...callGroupResolver(complexKeysArr[index], resolverKeyword, schemas, mergeSchemas2, options, parents)
        }), merged2);
      }
      const allSchemas = flattenDeep2(getAllOf(rootSchema));
      const merged = mergeSchemas2(allSchemas);
      return merged;
    }
    merger.options = {
      resolvers: defaultResolvers
    };
    module2.exports = merger;
  }
});

// node_modules/jsonpointer/jsonpointer.js
var require_jsonpointer = __commonJS({
  "node_modules/jsonpointer/jsonpointer.js"(exports2) {
    var hasExcape = /~/;
    var escapeMatcher = /~[01]/g;
    function escapeReplacer(m) {
      switch (m) {
        case "~1":
          return "/";
        case "~0":
          return "~";
      }
      throw new Error("Invalid tilde escape: " + m);
    }
    function untilde(str) {
      if (!hasExcape.test(str)) return str;
      return str.replace(escapeMatcher, escapeReplacer);
    }
    function setter(obj, pointer, value) {
      var part;
      var hasNextPart;
      for (var p = 1, len = pointer.length; p < len; ) {
        if (pointer[p] === "constructor" || pointer[p] === "prototype" || pointer[p] === "__proto__") return obj;
        part = untilde(pointer[p++]);
        hasNextPart = len > p;
        if (typeof obj[part] === "undefined") {
          if (Array.isArray(obj) && part === "-") {
            part = obj.length;
          }
          if (hasNextPart) {
            if (pointer[p] !== "" && pointer[p] < Infinity || pointer[p] === "-") obj[part] = [];
            else obj[part] = {};
          }
        }
        if (!hasNextPart) break;
        obj = obj[part];
      }
      var oldValue = obj[part];
      if (value === void 0) delete obj[part];
      else obj[part] = value;
      return oldValue;
    }
    function compilePointer(pointer) {
      if (typeof pointer === "string") {
        pointer = pointer.split("/");
        if (pointer[0] === "") return pointer;
        throw new Error("Invalid JSON pointer.");
      } else if (Array.isArray(pointer)) {
        for (const part of pointer) {
          if (typeof part !== "string" && typeof part !== "number") {
            throw new Error("Invalid JSON pointer. Must be of type string or number.");
          }
        }
        return pointer;
      }
      throw new Error("Invalid JSON pointer.");
    }
    function get2(obj, pointer) {
      if (typeof obj !== "object") throw new Error("Invalid input object.");
      pointer = compilePointer(pointer);
      var len = pointer.length;
      if (len === 1) return obj;
      for (var p = 1; p < len; ) {
        obj = obj[untilde(pointer[p++])];
        if (len === p) return obj;
        if (typeof obj !== "object" || obj === null) return void 0;
      }
    }
    function set2(obj, pointer, value) {
      if (typeof obj !== "object") throw new Error("Invalid input object.");
      pointer = compilePointer(pointer);
      if (pointer.length === 0) throw new Error("Invalid JSON pointer for set.");
      return setter(obj, pointer, value);
    }
    function compile(pointer) {
      var compiled = compilePointer(pointer);
      return {
        get: function(object) {
          return get2(object, compiled);
        },
        set: function(object, value) {
          return set2(object, compiled, value);
        }
      };
    }
    exports2.get = get2;
    exports2.set = set2;
    exports2.compile = compile;
  }
});

// node_modules/fast-uri/lib/scopedChars.js
var require_scopedChars = __commonJS({
  "node_modules/fast-uri/lib/scopedChars.js"(exports2, module2) {
    "use strict";
    var HEX = {
      0: 0,
      1: 1,
      2: 2,
      3: 3,
      4: 4,
      5: 5,
      6: 6,
      7: 7,
      8: 8,
      9: 9,
      a: 10,
      A: 10,
      b: 11,
      B: 11,
      c: 12,
      C: 12,
      d: 13,
      D: 13,
      e: 14,
      E: 14,
      f: 15,
      F: 15
    };
    module2.exports = {
      HEX
    };
  }
});

// node_modules/fast-uri/lib/utils.js
var require_utils = __commonJS({
  "node_modules/fast-uri/lib/utils.js"(exports2, module2) {
    "use strict";
    var { HEX } = require_scopedChars();
    var IPV4_REG = /^(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)$/u;
    function normalizeIPv4(host) {
      if (findToken(host, ".") < 3) {
        return { host, isIPV4: false };
      }
      const matches = host.match(IPV4_REG) || [];
      const [address] = matches;
      if (address) {
        return { host: stripLeadingZeros(address, "."), isIPV4: true };
      } else {
        return { host, isIPV4: false };
      }
    }
    function stringArrayToHexStripped(input, keepZero = false) {
      let acc = "";
      let strip = true;
      for (const c of input) {
        if (HEX[c] === void 0) return void 0;
        if (c !== "0" && strip === true) strip = false;
        if (!strip) acc += c;
      }
      if (keepZero && acc.length === 0) acc = "0";
      return acc;
    }
    function getIPV6(input) {
      let tokenCount = 0;
      const output = { error: false, address: "", zone: "" };
      const address = [];
      const buffer = [];
      let isZone = false;
      let endipv6Encountered = false;
      let endIpv6 = false;
      function consume() {
        if (buffer.length) {
          if (isZone === false) {
            const hex = stringArrayToHexStripped(buffer);
            if (hex !== void 0) {
              address.push(hex);
            } else {
              output.error = true;
              return false;
            }
          }
          buffer.length = 0;
        }
        return true;
      }
      for (let i = 0; i < input.length; i++) {
        const cursor = input[i];
        if (cursor === "[" || cursor === "]") {
          continue;
        }
        if (cursor === ":") {
          if (endipv6Encountered === true) {
            endIpv6 = true;
          }
          if (!consume()) {
            break;
          }
          tokenCount++;
          address.push(":");
          if (tokenCount > 7) {
            output.error = true;
            break;
          }
          if (i - 1 >= 0 && input[i - 1] === ":") {
            endipv6Encountered = true;
          }
          continue;
        } else if (cursor === "%") {
          if (!consume()) {
            break;
          }
          isZone = true;
        } else {
          buffer.push(cursor);
          continue;
        }
      }
      if (buffer.length) {
        if (isZone) {
          output.zone = buffer.join("");
        } else if (endIpv6) {
          address.push(buffer.join(""));
        } else {
          address.push(stringArrayToHexStripped(buffer));
        }
      }
      output.address = address.join("");
      return output;
    }
    function normalizeIPv6(host) {
      if (findToken(host, ":") < 2) {
        return { host, isIPV6: false };
      }
      const ipv6 = getIPV6(host);
      if (!ipv6.error) {
        let newHost = ipv6.address;
        let escapedHost = ipv6.address;
        if (ipv6.zone) {
          newHost += "%" + ipv6.zone;
          escapedHost += "%25" + ipv6.zone;
        }
        return { host: newHost, escapedHost, isIPV6: true };
      } else {
        return { host, isIPV6: false };
      }
    }
    function stripLeadingZeros(str, token) {
      let out = "";
      let skip = true;
      const l = str.length;
      for (let i = 0; i < l; i++) {
        const c = str[i];
        if (c === "0" && skip) {
          if (i + 1 <= l && str[i + 1] === token || i + 1 === l) {
            out += c;
            skip = false;
          }
        } else {
          if (c === token) {
            skip = true;
          } else {
            skip = false;
          }
          out += c;
        }
      }
      return out;
    }
    function findToken(str, token) {
      let ind = 0;
      for (let i = 0; i < str.length; i++) {
        if (str[i] === token) ind++;
      }
      return ind;
    }
    var RDS1 = /^\.\.?\//u;
    var RDS2 = /^\/\.(?:\/|$)/u;
    var RDS3 = /^\/\.\.(?:\/|$)/u;
    var RDS5 = /^\/?(?:.|\n)*?(?=\/|$)/u;
    function removeDotSegments(input) {
      const output = [];
      while (input.length) {
        if (input.match(RDS1)) {
          input = input.replace(RDS1, "");
        } else if (input.match(RDS2)) {
          input = input.replace(RDS2, "/");
        } else if (input.match(RDS3)) {
          input = input.replace(RDS3, "/");
          output.pop();
        } else if (input === "." || input === "..") {
          input = "";
        } else {
          const im = input.match(RDS5);
          if (im) {
            const s = im[0];
            input = input.slice(s.length);
            output.push(s);
          } else {
            throw new Error("Unexpected dot segment condition");
          }
        }
      }
      return output.join("");
    }
    function normalizeComponentEncoding(components, esc) {
      const func = esc !== true ? escape : unescape;
      if (components.scheme !== void 0) {
        components.scheme = func(components.scheme);
      }
      if (components.userinfo !== void 0) {
        components.userinfo = func(components.userinfo);
      }
      if (components.host !== void 0) {
        components.host = func(components.host);
      }
      if (components.path !== void 0) {
        components.path = func(components.path);
      }
      if (components.query !== void 0) {
        components.query = func(components.query);
      }
      if (components.fragment !== void 0) {
        components.fragment = func(components.fragment);
      }
      return components;
    }
    function recomposeAuthority(components) {
      const uriTokens = [];
      if (components.userinfo !== void 0) {
        uriTokens.push(components.userinfo);
        uriTokens.push("@");
      }
      if (components.host !== void 0) {
        let host = unescape(components.host);
        const ipV4res = normalizeIPv4(host);
        if (ipV4res.isIPV4) {
          host = ipV4res.host;
        } else {
          const ipV6res = normalizeIPv6(ipV4res.host);
          if (ipV6res.isIPV6 === true) {
            host = `[${ipV6res.escapedHost}]`;
          } else {
            host = components.host;
          }
        }
        uriTokens.push(host);
      }
      if (typeof components.port === "number" || typeof components.port === "string") {
        uriTokens.push(":");
        uriTokens.push(String(components.port));
      }
      return uriTokens.length ? uriTokens.join("") : void 0;
    }
    module2.exports = {
      recomposeAuthority,
      normalizeComponentEncoding,
      removeDotSegments,
      normalizeIPv4,
      normalizeIPv6,
      stringArrayToHexStripped
    };
  }
});

// node_modules/fast-uri/lib/schemes.js
var require_schemes = __commonJS({
  "node_modules/fast-uri/lib/schemes.js"(exports2, module2) {
    "use strict";
    var UUID_REG = /^[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}$/iu;
    var URN_REG = /([\da-z][\d\-a-z]{0,31}):((?:[\w!$'()*+,\-.:;=@]|%[\da-f]{2})+)/iu;
    function isSecure(wsComponents) {
      return typeof wsComponents.secure === "boolean" ? wsComponents.secure : String(wsComponents.scheme).toLowerCase() === "wss";
    }
    function httpParse(components) {
      if (!components.host) {
        components.error = components.error || "HTTP URIs must have a host.";
      }
      return components;
    }
    function httpSerialize(components) {
      const secure = String(components.scheme).toLowerCase() === "https";
      if (components.port === (secure ? 443 : 80) || components.port === "") {
        components.port = void 0;
      }
      if (!components.path) {
        components.path = "/";
      }
      return components;
    }
    function wsParse(wsComponents) {
      wsComponents.secure = isSecure(wsComponents);
      wsComponents.resourceName = (wsComponents.path || "/") + (wsComponents.query ? "?" + wsComponents.query : "");
      wsComponents.path = void 0;
      wsComponents.query = void 0;
      return wsComponents;
    }
    function wsSerialize(wsComponents) {
      if (wsComponents.port === (isSecure(wsComponents) ? 443 : 80) || wsComponents.port === "") {
        wsComponents.port = void 0;
      }
      if (typeof wsComponents.secure === "boolean") {
        wsComponents.scheme = wsComponents.secure ? "wss" : "ws";
        wsComponents.secure = void 0;
      }
      if (wsComponents.resourceName) {
        const [path, query] = wsComponents.resourceName.split("?");
        wsComponents.path = path && path !== "/" ? path : void 0;
        wsComponents.query = query;
        wsComponents.resourceName = void 0;
      }
      wsComponents.fragment = void 0;
      return wsComponents;
    }
    function urnParse(urnComponents, options) {
      if (!urnComponents.path) {
        urnComponents.error = "URN can not be parsed";
        return urnComponents;
      }
      const matches = urnComponents.path.match(URN_REG);
      if (matches) {
        const scheme = options.scheme || urnComponents.scheme || "urn";
        urnComponents.nid = matches[1].toLowerCase();
        urnComponents.nss = matches[2];
        const urnScheme = `${scheme}:${options.nid || urnComponents.nid}`;
        const schemeHandler = SCHEMES[urnScheme];
        urnComponents.path = void 0;
        if (schemeHandler) {
          urnComponents = schemeHandler.parse(urnComponents, options);
        }
      } else {
        urnComponents.error = urnComponents.error || "URN can not be parsed.";
      }
      return urnComponents;
    }
    function urnSerialize(urnComponents, options) {
      const scheme = options.scheme || urnComponents.scheme || "urn";
      const nid = urnComponents.nid.toLowerCase();
      const urnScheme = `${scheme}:${options.nid || nid}`;
      const schemeHandler = SCHEMES[urnScheme];
      if (schemeHandler) {
        urnComponents = schemeHandler.serialize(urnComponents, options);
      }
      const uriComponents = urnComponents;
      const nss = urnComponents.nss;
      uriComponents.path = `${nid || options.nid}:${nss}`;
      options.skipEscape = true;
      return uriComponents;
    }
    function urnuuidParse(urnComponents, options) {
      const uuidComponents = urnComponents;
      uuidComponents.uuid = uuidComponents.nss;
      uuidComponents.nss = void 0;
      if (!options.tolerant && (!uuidComponents.uuid || !UUID_REG.test(uuidComponents.uuid))) {
        uuidComponents.error = uuidComponents.error || "UUID is not valid.";
      }
      return uuidComponents;
    }
    function urnuuidSerialize(uuidComponents) {
      const urnComponents = uuidComponents;
      urnComponents.nss = (uuidComponents.uuid || "").toLowerCase();
      return urnComponents;
    }
    var http = {
      scheme: "http",
      domainHost: true,
      parse: httpParse,
      serialize: httpSerialize
    };
    var https = {
      scheme: "https",
      domainHost: http.domainHost,
      parse: httpParse,
      serialize: httpSerialize
    };
    var ws = {
      scheme: "ws",
      domainHost: true,
      parse: wsParse,
      serialize: wsSerialize
    };
    var wss = {
      scheme: "wss",
      domainHost: ws.domainHost,
      parse: ws.parse,
      serialize: ws.serialize
    };
    var urn = {
      scheme: "urn",
      parse: urnParse,
      serialize: urnSerialize,
      skipNormalize: true
    };
    var urnuuid = {
      scheme: "urn:uuid",
      parse: urnuuidParse,
      serialize: urnuuidSerialize,
      skipNormalize: true
    };
    var SCHEMES = {
      http,
      https,
      ws,
      wss,
      urn,
      "urn:uuid": urnuuid
    };
    module2.exports = SCHEMES;
  }
});

// node_modules/fast-uri/index.js
var require_fast_uri = __commonJS({
  "node_modules/fast-uri/index.js"(exports2, module2) {
    "use strict";
    var { normalizeIPv6, normalizeIPv4, removeDotSegments, recomposeAuthority, normalizeComponentEncoding } = require_utils();
    var SCHEMES = require_schemes();
    function normalize(uri, options) {
      if (typeof uri === "string") {
        uri = serialize(parse(uri, options), options);
      } else if (typeof uri === "object") {
        uri = parse(serialize(uri, options), options);
      }
      return uri;
    }
    function resolve(baseURI, relativeURI, options) {
      const schemelessOptions = Object.assign({ scheme: "null" }, options);
      const resolved = resolveComponents(parse(baseURI, schemelessOptions), parse(relativeURI, schemelessOptions), schemelessOptions, true);
      return serialize(resolved, { ...schemelessOptions, skipEscape: true });
    }
    function resolveComponents(base, relative, options, skipNormalization) {
      const target = {};
      if (!skipNormalization) {
        base = parse(serialize(base, options), options);
        relative = parse(serialize(relative, options), options);
      }
      options = options || {};
      if (!options.tolerant && relative.scheme) {
        target.scheme = relative.scheme;
        target.userinfo = relative.userinfo;
        target.host = relative.host;
        target.port = relative.port;
        target.path = removeDotSegments(relative.path || "");
        target.query = relative.query;
      } else {
        if (relative.userinfo !== void 0 || relative.host !== void 0 || relative.port !== void 0) {
          target.userinfo = relative.userinfo;
          target.host = relative.host;
          target.port = relative.port;
          target.path = removeDotSegments(relative.path || "");
          target.query = relative.query;
        } else {
          if (!relative.path) {
            target.path = base.path;
            if (relative.query !== void 0) {
              target.query = relative.query;
            } else {
              target.query = base.query;
            }
          } else {
            if (relative.path.charAt(0) === "/") {
              target.path = removeDotSegments(relative.path);
            } else {
              if ((base.userinfo !== void 0 || base.host !== void 0 || base.port !== void 0) && !base.path) {
                target.path = "/" + relative.path;
              } else if (!base.path) {
                target.path = relative.path;
              } else {
                target.path = base.path.slice(0, base.path.lastIndexOf("/") + 1) + relative.path;
              }
              target.path = removeDotSegments(target.path);
            }
            target.query = relative.query;
          }
          target.userinfo = base.userinfo;
          target.host = base.host;
          target.port = base.port;
        }
        target.scheme = base.scheme;
      }
      target.fragment = relative.fragment;
      return target;
    }
    function equal(uriA, uriB, options) {
      if (typeof uriA === "string") {
        uriA = unescape(uriA);
        uriA = serialize(normalizeComponentEncoding(parse(uriA, options), true), { ...options, skipEscape: true });
      } else if (typeof uriA === "object") {
        uriA = serialize(normalizeComponentEncoding(uriA, true), { ...options, skipEscape: true });
      }
      if (typeof uriB === "string") {
        uriB = unescape(uriB);
        uriB = serialize(normalizeComponentEncoding(parse(uriB, options), true), { ...options, skipEscape: true });
      } else if (typeof uriB === "object") {
        uriB = serialize(normalizeComponentEncoding(uriB, true), { ...options, skipEscape: true });
      }
      return uriA.toLowerCase() === uriB.toLowerCase();
    }
    function serialize(cmpts, opts) {
      const components = {
        host: cmpts.host,
        scheme: cmpts.scheme,
        userinfo: cmpts.userinfo,
        port: cmpts.port,
        path: cmpts.path,
        query: cmpts.query,
        nid: cmpts.nid,
        nss: cmpts.nss,
        uuid: cmpts.uuid,
        fragment: cmpts.fragment,
        reference: cmpts.reference,
        resourceName: cmpts.resourceName,
        secure: cmpts.secure,
        error: ""
      };
      const options = Object.assign({}, opts);
      const uriTokens = [];
      const schemeHandler = SCHEMES[(options.scheme || components.scheme || "").toLowerCase()];
      if (schemeHandler && schemeHandler.serialize) schemeHandler.serialize(components, options);
      if (components.path !== void 0) {
        if (!options.skipEscape) {
          components.path = escape(components.path);
          if (components.scheme !== void 0) {
            components.path = components.path.split("%3A").join(":");
          }
        } else {
          components.path = unescape(components.path);
        }
      }
      if (options.reference !== "suffix" && components.scheme) {
        uriTokens.push(components.scheme, ":");
      }
      const authority = recomposeAuthority(components);
      if (authority !== void 0) {
        if (options.reference !== "suffix") {
          uriTokens.push("//");
        }
        uriTokens.push(authority);
        if (components.path && components.path.charAt(0) !== "/") {
          uriTokens.push("/");
        }
      }
      if (components.path !== void 0) {
        let s = components.path;
        if (!options.absolutePath && (!schemeHandler || !schemeHandler.absolutePath)) {
          s = removeDotSegments(s);
        }
        if (authority === void 0) {
          s = s.replace(/^\/\//u, "/%2F");
        }
        uriTokens.push(s);
      }
      if (components.query !== void 0) {
        uriTokens.push("?", components.query);
      }
      if (components.fragment !== void 0) {
        uriTokens.push("#", components.fragment);
      }
      return uriTokens.join("");
    }
    var hexLookUp = Array.from({ length: 127 }, (_v, k) => /[^!"$&'()*+,\-.;=_`a-z{}~]/u.test(String.fromCharCode(k)));
    function nonSimpleDomain(value) {
      let code = 0;
      for (let i = 0, len = value.length; i < len; ++i) {
        code = value.charCodeAt(i);
        if (code > 126 || hexLookUp[code]) {
          return true;
        }
      }
      return false;
    }
    var URI_PARSE = /^(?:([^#/:?]+):)?(?:\/\/((?:([^#/?@]*)@)?(\[[^#/?\]]+\]|[^#/:?]*)(?::(\d*))?))?([^#?]*)(?:\?([^#]*))?(?:#((?:.|[\n\r])*))?/u;
    function parse(uri, opts) {
      const options = Object.assign({}, opts);
      const parsed = {
        scheme: void 0,
        userinfo: void 0,
        host: "",
        port: void 0,
        path: "",
        query: void 0,
        fragment: void 0
      };
      const gotEncoding = uri.indexOf("%") !== -1;
      let isIP = false;
      if (options.reference === "suffix") uri = (options.scheme ? options.scheme + ":" : "") + "//" + uri;
      const matches = uri.match(URI_PARSE);
      if (matches) {
        parsed.scheme = matches[1];
        parsed.userinfo = matches[3];
        parsed.host = matches[4];
        parsed.port = parseInt(matches[5], 10);
        parsed.path = matches[6] || "";
        parsed.query = matches[7];
        parsed.fragment = matches[8];
        if (isNaN(parsed.port)) {
          parsed.port = matches[5];
        }
        if (parsed.host) {
          const ipv4result = normalizeIPv4(parsed.host);
          if (ipv4result.isIPV4 === false) {
            const ipv6result = normalizeIPv6(ipv4result.host);
            parsed.host = ipv6result.host.toLowerCase();
            isIP = ipv6result.isIPV6;
          } else {
            parsed.host = ipv4result.host;
            isIP = true;
          }
        }
        if (parsed.scheme === void 0 && parsed.userinfo === void 0 && parsed.host === void 0 && parsed.port === void 0 && parsed.query === void 0 && !parsed.path) {
          parsed.reference = "same-document";
        } else if (parsed.scheme === void 0) {
          parsed.reference = "relative";
        } else if (parsed.fragment === void 0) {
          parsed.reference = "absolute";
        } else {
          parsed.reference = "uri";
        }
        if (options.reference && options.reference !== "suffix" && options.reference !== parsed.reference) {
          parsed.error = parsed.error || "URI is not a " + options.reference + " reference.";
        }
        const schemeHandler = SCHEMES[(options.scheme || parsed.scheme || "").toLowerCase()];
        if (!options.unicodeSupport && (!schemeHandler || !schemeHandler.unicodeSupport)) {
          if (parsed.host && (options.domainHost || schemeHandler && schemeHandler.domainHost) && isIP === false && nonSimpleDomain(parsed.host)) {
            try {
              parsed.host = URL.domainToASCII(parsed.host.toLowerCase());
            } catch (e) {
              parsed.error = parsed.error || "Host's domain name can not be converted to ASCII: " + e;
            }
          }
        }
        if (!schemeHandler || schemeHandler && !schemeHandler.skipNormalize) {
          if (gotEncoding && parsed.scheme !== void 0) {
            parsed.scheme = unescape(parsed.scheme);
          }
          if (gotEncoding && parsed.host !== void 0) {
            parsed.host = unescape(parsed.host);
          }
          if (parsed.path) {
            parsed.path = escape(unescape(parsed.path));
          }
          if (parsed.fragment) {
            parsed.fragment = encodeURI(decodeURIComponent(parsed.fragment));
          }
        }
        if (schemeHandler && schemeHandler.parse) {
          schemeHandler.parse(parsed, options);
        }
      } else {
        parsed.error = parsed.error || "URI can not be parsed.";
      }
      return parsed;
    }
    var fastUri = {
      SCHEMES,
      normalize,
      resolve,
      resolveComponents,
      equal,
      serialize,
      parse
    };
    module2.exports = fastUri;
    module2.exports.default = fastUri;
    module2.exports.fastUri = fastUri;
  }
});

// node_modules/react-is/cjs/react-is.development.js
var require_react_is_development = __commonJS({
  "node_modules/react-is/cjs/react-is.development.js"(exports2) {
    "use strict";
    if (true) {
      (function() {
        "use strict";
        var REACT_ELEMENT_TYPE = Symbol.for("react.element");
        var REACT_PORTAL_TYPE = Symbol.for("react.portal");
        var REACT_FRAGMENT_TYPE = Symbol.for("react.fragment");
        var REACT_STRICT_MODE_TYPE = Symbol.for("react.strict_mode");
        var REACT_PROFILER_TYPE = Symbol.for("react.profiler");
        var REACT_PROVIDER_TYPE = Symbol.for("react.provider");
        var REACT_CONTEXT_TYPE = Symbol.for("react.context");
        var REACT_SERVER_CONTEXT_TYPE = Symbol.for("react.server_context");
        var REACT_FORWARD_REF_TYPE = Symbol.for("react.forward_ref");
        var REACT_SUSPENSE_TYPE = Symbol.for("react.suspense");
        var REACT_SUSPENSE_LIST_TYPE = Symbol.for("react.suspense_list");
        var REACT_MEMO_TYPE = Symbol.for("react.memo");
        var REACT_LAZY_TYPE = Symbol.for("react.lazy");
        var REACT_OFFSCREEN_TYPE = Symbol.for("react.offscreen");
        var enableScopeAPI = false;
        var enableCacheElement = false;
        var enableTransitionTracing = false;
        var enableLegacyHidden = false;
        var enableDebugTracing = false;
        var REACT_MODULE_REFERENCE;
        {
          REACT_MODULE_REFERENCE = Symbol.for("react.module.reference");
        }
        function isValidElementType(type) {
          if (typeof type === "string" || typeof type === "function") {
            return true;
          }
          if (type === REACT_FRAGMENT_TYPE || type === REACT_PROFILER_TYPE || enableDebugTracing || type === REACT_STRICT_MODE_TYPE || type === REACT_SUSPENSE_TYPE || type === REACT_SUSPENSE_LIST_TYPE || enableLegacyHidden || type === REACT_OFFSCREEN_TYPE || enableScopeAPI || enableCacheElement || enableTransitionTracing) {
            return true;
          }
          if (typeof type === "object" && type !== null) {
            if (type.$$typeof === REACT_LAZY_TYPE || type.$$typeof === REACT_MEMO_TYPE || type.$$typeof === REACT_PROVIDER_TYPE || type.$$typeof === REACT_CONTEXT_TYPE || type.$$typeof === REACT_FORWARD_REF_TYPE || // This needs to include all possible module reference object
            // types supported by any Flight configuration anywhere since
            // we don't know which Flight build this will end up being used
            // with.
            type.$$typeof === REACT_MODULE_REFERENCE || type.getModuleId !== void 0) {
              return true;
            }
          }
          return false;
        }
        function typeOf(object) {
          if (typeof object === "object" && object !== null) {
            var $$typeof = object.$$typeof;
            switch ($$typeof) {
              case REACT_ELEMENT_TYPE:
                var type = object.type;
                switch (type) {
                  case REACT_FRAGMENT_TYPE:
                  case REACT_PROFILER_TYPE:
                  case REACT_STRICT_MODE_TYPE:
                  case REACT_SUSPENSE_TYPE:
                  case REACT_SUSPENSE_LIST_TYPE:
                    return type;
                  default:
                    var $$typeofType = type && type.$$typeof;
                    switch ($$typeofType) {
                      case REACT_SERVER_CONTEXT_TYPE:
                      case REACT_CONTEXT_TYPE:
                      case REACT_FORWARD_REF_TYPE:
                      case REACT_LAZY_TYPE:
                      case REACT_MEMO_TYPE:
                      case REACT_PROVIDER_TYPE:
                        return $$typeofType;
                      default:
                        return $$typeof;
                    }
                }
              case REACT_PORTAL_TYPE:
                return $$typeof;
            }
          }
          return void 0;
        }
        var ContextConsumer = REACT_CONTEXT_TYPE;
        var ContextProvider = REACT_PROVIDER_TYPE;
        var Element = REACT_ELEMENT_TYPE;
        var ForwardRef = REACT_FORWARD_REF_TYPE;
        var Fragment = REACT_FRAGMENT_TYPE;
        var Lazy = REACT_LAZY_TYPE;
        var Memo = REACT_MEMO_TYPE;
        var Portal = REACT_PORTAL_TYPE;
        var Profiler = REACT_PROFILER_TYPE;
        var StrictMode = REACT_STRICT_MODE_TYPE;
        var Suspense = REACT_SUSPENSE_TYPE;
        var SuspenseList = REACT_SUSPENSE_LIST_TYPE;
        var hasWarnedAboutDeprecatedIsAsyncMode = false;
        var hasWarnedAboutDeprecatedIsConcurrentMode = false;
        function isAsyncMode(object) {
          {
            if (!hasWarnedAboutDeprecatedIsAsyncMode) {
              hasWarnedAboutDeprecatedIsAsyncMode = true;
              console["warn"]("The ReactIs.isAsyncMode() alias has been deprecated, and will be removed in React 18+.");
            }
          }
          return false;
        }
        function isConcurrentMode(object) {
          {
            if (!hasWarnedAboutDeprecatedIsConcurrentMode) {
              hasWarnedAboutDeprecatedIsConcurrentMode = true;
              console["warn"]("The ReactIs.isConcurrentMode() alias has been deprecated, and will be removed in React 18+.");
            }
          }
          return false;
        }
        function isContextConsumer(object) {
          return typeOf(object) === REACT_CONTEXT_TYPE;
        }
        function isContextProvider(object) {
          return typeOf(object) === REACT_PROVIDER_TYPE;
        }
        function isElement(object) {
          return typeof object === "object" && object !== null && object.$$typeof === REACT_ELEMENT_TYPE;
        }
        function isForwardRef(object) {
          return typeOf(object) === REACT_FORWARD_REF_TYPE;
        }
        function isFragment(object) {
          return typeOf(object) === REACT_FRAGMENT_TYPE;
        }
        function isLazy(object) {
          return typeOf(object) === REACT_LAZY_TYPE;
        }
        function isMemo(object) {
          return typeOf(object) === REACT_MEMO_TYPE;
        }
        function isPortal(object) {
          return typeOf(object) === REACT_PORTAL_TYPE;
        }
        function isProfiler(object) {
          return typeOf(object) === REACT_PROFILER_TYPE;
        }
        function isStrictMode(object) {
          return typeOf(object) === REACT_STRICT_MODE_TYPE;
        }
        function isSuspense(object) {
          return typeOf(object) === REACT_SUSPENSE_TYPE;
        }
        function isSuspenseList(object) {
          return typeOf(object) === REACT_SUSPENSE_LIST_TYPE;
        }
        exports2.ContextConsumer = ContextConsumer;
        exports2.ContextProvider = ContextProvider;
        exports2.Element = Element;
        exports2.ForwardRef = ForwardRef;
        exports2.Fragment = Fragment;
        exports2.Lazy = Lazy;
        exports2.Memo = Memo;
        exports2.Portal = Portal;
        exports2.Profiler = Profiler;
        exports2.StrictMode = StrictMode;
        exports2.Suspense = Suspense;
        exports2.SuspenseList = SuspenseList;
        exports2.isAsyncMode = isAsyncMode;
        exports2.isConcurrentMode = isConcurrentMode;
        exports2.isContextConsumer = isContextConsumer;
        exports2.isContextProvider = isContextProvider;
        exports2.isElement = isElement;
        exports2.isForwardRef = isForwardRef;
        exports2.isFragment = isFragment;
        exports2.isLazy = isLazy;
        exports2.isMemo = isMemo;
        exports2.isPortal = isPortal;
        exports2.isProfiler = isProfiler;
        exports2.isStrictMode = isStrictMode;
        exports2.isSuspense = isSuspense;
        exports2.isSuspenseList = isSuspenseList;
        exports2.isValidElementType = isValidElementType;
        exports2.typeOf = typeOf;
      })();
    }
  }
});

// node_modules/react-is/index.js
var require_react_is = __commonJS({
  "node_modules/react-is/index.js"(exports2, module2) {
    "use strict";
    if (false) {
      module2.exports = null;
    } else {
      module2.exports = require_react_is_development();
    }
  }
});

// node_modules/@rjsf/utils/lib/isObject.js
function isObject(thing) {
  if (typeof thing !== "object" || thing === null) {
    return false;
  }
  if (typeof thing.lastModified === "number" && typeof File !== "undefined" && thing instanceof File) {
    return false;
  }
  if (typeof thing.getMonth === "function" && typeof Date !== "undefined" && thing instanceof Date) {
    return false;
  }
  return !Array.isArray(thing);
}

// node_modules/@rjsf/utils/lib/constants.js
var ADDITIONAL_PROPERTY_FLAG = "__additional_property";
var ADDITIONAL_PROPERTIES_KEY = "additionalProperties";
var ALL_OF_KEY = "allOf";
var ANY_OF_KEY = "anyOf";
var CONST_KEY = "const";
var DEFAULT_KEY = "default";
var DEPENDENCIES_KEY = "dependencies";
var ENUM_KEY = "enum";
var ERRORS_KEY = "__errors";
var ID_KEY = "$id";
var IF_KEY = "if";
var ITEMS_KEY = "items";
var JUNK_OPTION_ID = "_$junk_option_schema_id$_";
var NAME_KEY = "$name";
var ONE_OF_KEY = "oneOf";
var PATTERN_PROPERTIES_KEY = "patternProperties";
var PROPERTIES_KEY = "properties";
var READONLY_KEY = "readonly";
var REQUIRED_KEY = "required";
var SUBMIT_BTN_OPTIONS_KEY = "submitButtonOptions";
var REF_KEY = "$ref";
var SCHEMA_KEY = "$schema";
var DISCRIMINATOR_PATH = ["discriminator", "propertyName"];
var FORM_CONTEXT_NAME = "formContext";
var LOOKUP_MAP_NAME = "layoutGridLookupMap";
var RJSF_ADDITIONAL_PROPERTIES_FLAG = "__rjsf_additionalProperties";
var ROOT_SCHEMA_PREFIX = "__rjsf_rootSchema";
var UI_FIELD_KEY = "ui:field";
var UI_WIDGET_KEY = "ui:widget";
var UI_OPTIONS_KEY = "ui:options";
var UI_GLOBAL_OPTIONS_KEY = "ui:globalOptions";
var JSON_SCHEMA_DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema";

// node_modules/@rjsf/utils/lib/getUiOptions.js
function getUiOptions(uiSchema = {}, globalOptions = {}) {
  return Object.keys(uiSchema).filter((key) => key.indexOf("ui:") === 0).reduce((options, key) => {
    const value = uiSchema[key];
    if (key === UI_WIDGET_KEY && isObject(value)) {
      console.error("Setting options via ui:widget object is no longer supported, use ui:options instead");
      return options;
    }
    if (key === UI_OPTIONS_KEY && isObject(value)) {
      return { ...options, ...value };
    }
    return { ...options, [key.substring(3)]: value };
  }, { ...globalOptions });
}

// node_modules/lodash-es/_freeGlobal.js
var freeGlobal = typeof global == "object" && global && global.Object === Object && global;
var freeGlobal_default = freeGlobal;

// node_modules/lodash-es/_root.js
var freeSelf = typeof self == "object" && self && self.Object === Object && self;
var root = freeGlobal_default || freeSelf || Function("return this")();
var root_default = root;

// node_modules/lodash-es/_Symbol.js
var Symbol2 = root_default.Symbol;
var Symbol_default = Symbol2;

// node_modules/lodash-es/_getRawTag.js
var objectProto = Object.prototype;
var hasOwnProperty = objectProto.hasOwnProperty;
var nativeObjectToString = objectProto.toString;
var symToStringTag = Symbol_default ? Symbol_default.toStringTag : void 0;
function getRawTag(value) {
  var isOwn = hasOwnProperty.call(value, symToStringTag), tag = value[symToStringTag];
  try {
    value[symToStringTag] = void 0;
    var unmasked = true;
  } catch (e) {
  }
  var result = nativeObjectToString.call(value);
  if (unmasked) {
    if (isOwn) {
      value[symToStringTag] = tag;
    } else {
      delete value[symToStringTag];
    }
  }
  return result;
}
var getRawTag_default = getRawTag;

// node_modules/lodash-es/_objectToString.js
var objectProto2 = Object.prototype;
var nativeObjectToString2 = objectProto2.toString;
function objectToString(value) {
  return nativeObjectToString2.call(value);
}
var objectToString_default = objectToString;

// node_modules/lodash-es/_baseGetTag.js
var nullTag = "[object Null]";
var undefinedTag = "[object Undefined]";
var symToStringTag2 = Symbol_default ? Symbol_default.toStringTag : void 0;
function baseGetTag(value) {
  if (value == null) {
    return value === void 0 ? undefinedTag : nullTag;
  }
  return symToStringTag2 && symToStringTag2 in Object(value) ? getRawTag_default(value) : objectToString_default(value);
}
var baseGetTag_default = baseGetTag;

// node_modules/lodash-es/_overArg.js
function overArg(func, transform2) {
  return function(arg) {
    return func(transform2(arg));
  };
}
var overArg_default = overArg;

// node_modules/lodash-es/_getPrototype.js
var getPrototype = overArg_default(Object.getPrototypeOf, Object);
var getPrototype_default = getPrototype;

// node_modules/lodash-es/isObjectLike.js
function isObjectLike(value) {
  return value != null && typeof value == "object";
}
var isObjectLike_default = isObjectLike;

// node_modules/lodash-es/isPlainObject.js
var objectTag = "[object Object]";
var funcProto = Function.prototype;
var objectProto3 = Object.prototype;
var funcToString = funcProto.toString;
var hasOwnProperty2 = objectProto3.hasOwnProperty;
var objectCtorString = funcToString.call(Object);
function isPlainObject(value) {
  if (!isObjectLike_default(value) || baseGetTag_default(value) != objectTag) {
    return false;
  }
  var proto = getPrototype_default(value);
  if (proto === null) {
    return true;
  }
  var Ctor = hasOwnProperty2.call(proto, "constructor") && proto.constructor;
  return typeof Ctor == "function" && Ctor instanceof Ctor && funcToString.call(Ctor) == objectCtorString;
}
var isPlainObject_default = isPlainObject;

// node_modules/@rjsf/utils/lib/createErrorHandler.js
function createErrorHandler(formData) {
  const handler = {
    // We store the list of errors for this node in a property named __errors
    // to avoid name collision with a possible sub schema field named
    // 'errors' (see `utils.toErrorSchema`).
    [ERRORS_KEY]: [],
    addError(message) {
      this[ERRORS_KEY].push(message);
    }
  };
  if (Array.isArray(formData)) {
    return formData.reduce((acc, value, key) => {
      return { ...acc, [key]: createErrorHandler(value) };
    }, handler);
  }
  if (isPlainObject_default(formData)) {
    const formObject = formData;
    return Object.keys(formObject).reduce((acc, key) => {
      return { ...acc, [key]: createErrorHandler(formObject[key]) };
    }, handler);
  }
  return handler;
}

// node_modules/lodash-es/_listCacheClear.js
function listCacheClear() {
  this.__data__ = [];
  this.size = 0;
}
var listCacheClear_default = listCacheClear;

// node_modules/lodash-es/eq.js
function eq(value, other) {
  return value === other || value !== value && other !== other;
}
var eq_default = eq;

// node_modules/lodash-es/_assocIndexOf.js
function assocIndexOf(array, key) {
  var length = array.length;
  while (length--) {
    if (eq_default(array[length][0], key)) {
      return length;
    }
  }
  return -1;
}
var assocIndexOf_default = assocIndexOf;

// node_modules/lodash-es/_listCacheDelete.js
var arrayProto = Array.prototype;
var splice = arrayProto.splice;
function listCacheDelete(key) {
  var data = this.__data__, index = assocIndexOf_default(data, key);
  if (index < 0) {
    return false;
  }
  var lastIndex = data.length - 1;
  if (index == lastIndex) {
    data.pop();
  } else {
    splice.call(data, index, 1);
  }
  --this.size;
  return true;
}
var listCacheDelete_default = listCacheDelete;

// node_modules/lodash-es/_listCacheGet.js
function listCacheGet(key) {
  var data = this.__data__, index = assocIndexOf_default(data, key);
  return index < 0 ? void 0 : data[index][1];
}
var listCacheGet_default = listCacheGet;

// node_modules/lodash-es/_listCacheHas.js
function listCacheHas(key) {
  return assocIndexOf_default(this.__data__, key) > -1;
}
var listCacheHas_default = listCacheHas;

// node_modules/lodash-es/_listCacheSet.js
function listCacheSet(key, value) {
  var data = this.__data__, index = assocIndexOf_default(data, key);
  if (index < 0) {
    ++this.size;
    data.push([key, value]);
  } else {
    data[index][1] = value;
  }
  return this;
}
var listCacheSet_default = listCacheSet;

// node_modules/lodash-es/_ListCache.js
function ListCache(entries) {
  var index = -1, length = entries == null ? 0 : entries.length;
  this.clear();
  while (++index < length) {
    var entry = entries[index];
    this.set(entry[0], entry[1]);
  }
}
ListCache.prototype.clear = listCacheClear_default;
ListCache.prototype["delete"] = listCacheDelete_default;
ListCache.prototype.get = listCacheGet_default;
ListCache.prototype.has = listCacheHas_default;
ListCache.prototype.set = listCacheSet_default;
var ListCache_default = ListCache;

// node_modules/lodash-es/_stackClear.js
function stackClear() {
  this.__data__ = new ListCache_default();
  this.size = 0;
}
var stackClear_default = stackClear;

// node_modules/lodash-es/_stackDelete.js
function stackDelete(key) {
  var data = this.__data__, result = data["delete"](key);
  this.size = data.size;
  return result;
}
var stackDelete_default = stackDelete;

// node_modules/lodash-es/_stackGet.js
function stackGet(key) {
  return this.__data__.get(key);
}
var stackGet_default = stackGet;

// node_modules/lodash-es/_stackHas.js
function stackHas(key) {
  return this.__data__.has(key);
}
var stackHas_default = stackHas;

// node_modules/lodash-es/isObject.js
function isObject2(value) {
  var type = typeof value;
  return value != null && (type == "object" || type == "function");
}
var isObject_default = isObject2;

// node_modules/lodash-es/isFunction.js
var asyncTag = "[object AsyncFunction]";
var funcTag = "[object Function]";
var genTag = "[object GeneratorFunction]";
var proxyTag = "[object Proxy]";
function isFunction(value) {
  if (!isObject_default(value)) {
    return false;
  }
  var tag = baseGetTag_default(value);
  return tag == funcTag || tag == genTag || tag == asyncTag || tag == proxyTag;
}
var isFunction_default = isFunction;

// node_modules/lodash-es/_coreJsData.js
var coreJsData = root_default["__core-js_shared__"];
var coreJsData_default = coreJsData;

// node_modules/lodash-es/_isMasked.js
var maskSrcKey = function() {
  var uid = /[^.]+$/.exec(coreJsData_default && coreJsData_default.keys && coreJsData_default.keys.IE_PROTO || "");
  return uid ? "Symbol(src)_1." + uid : "";
}();
function isMasked(func) {
  return !!maskSrcKey && maskSrcKey in func;
}
var isMasked_default = isMasked;

// node_modules/lodash-es/_toSource.js
var funcProto2 = Function.prototype;
var funcToString2 = funcProto2.toString;
function toSource(func) {
  if (func != null) {
    try {
      return funcToString2.call(func);
    } catch (e) {
    }
    try {
      return func + "";
    } catch (e) {
    }
  }
  return "";
}
var toSource_default = toSource;

// node_modules/lodash-es/_baseIsNative.js
var reRegExpChar = /[\\^$.*+?()[\]{}|]/g;
var reIsHostCtor = /^\[object .+?Constructor\]$/;
var funcProto3 = Function.prototype;
var objectProto4 = Object.prototype;
var funcToString3 = funcProto3.toString;
var hasOwnProperty3 = objectProto4.hasOwnProperty;
var reIsNative = RegExp(
  "^" + funcToString3.call(hasOwnProperty3).replace(reRegExpChar, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$"
);
function baseIsNative(value) {
  if (!isObject_default(value) || isMasked_default(value)) {
    return false;
  }
  var pattern = isFunction_default(value) ? reIsNative : reIsHostCtor;
  return pattern.test(toSource_default(value));
}
var baseIsNative_default = baseIsNative;

// node_modules/lodash-es/_getValue.js
function getValue(object, key) {
  return object == null ? void 0 : object[key];
}
var getValue_default = getValue;

// node_modules/lodash-es/_getNative.js
function getNative(object, key) {
  var value = getValue_default(object, key);
  return baseIsNative_default(value) ? value : void 0;
}
var getNative_default = getNative;

// node_modules/lodash-es/_Map.js
var Map2 = getNative_default(root_default, "Map");
var Map_default = Map2;

// node_modules/lodash-es/_nativeCreate.js
var nativeCreate = getNative_default(Object, "create");
var nativeCreate_default = nativeCreate;

// node_modules/lodash-es/_hashClear.js
function hashClear() {
  this.__data__ = nativeCreate_default ? nativeCreate_default(null) : {};
  this.size = 0;
}
var hashClear_default = hashClear;

// node_modules/lodash-es/_hashDelete.js
function hashDelete(key) {
  var result = this.has(key) && delete this.__data__[key];
  this.size -= result ? 1 : 0;
  return result;
}
var hashDelete_default = hashDelete;

// node_modules/lodash-es/_hashGet.js
var HASH_UNDEFINED = "__lodash_hash_undefined__";
var objectProto5 = Object.prototype;
var hasOwnProperty4 = objectProto5.hasOwnProperty;
function hashGet(key) {
  var data = this.__data__;
  if (nativeCreate_default) {
    var result = data[key];
    return result === HASH_UNDEFINED ? void 0 : result;
  }
  return hasOwnProperty4.call(data, key) ? data[key] : void 0;
}
var hashGet_default = hashGet;

// node_modules/lodash-es/_hashHas.js
var objectProto6 = Object.prototype;
var hasOwnProperty5 = objectProto6.hasOwnProperty;
function hashHas(key) {
  var data = this.__data__;
  return nativeCreate_default ? data[key] !== void 0 : hasOwnProperty5.call(data, key);
}
var hashHas_default = hashHas;

// node_modules/lodash-es/_hashSet.js
var HASH_UNDEFINED2 = "__lodash_hash_undefined__";
function hashSet(key, value) {
  var data = this.__data__;
  this.size += this.has(key) ? 0 : 1;
  data[key] = nativeCreate_default && value === void 0 ? HASH_UNDEFINED2 : value;
  return this;
}
var hashSet_default = hashSet;

// node_modules/lodash-es/_Hash.js
function Hash(entries) {
  var index = -1, length = entries == null ? 0 : entries.length;
  this.clear();
  while (++index < length) {
    var entry = entries[index];
    this.set(entry[0], entry[1]);
  }
}
Hash.prototype.clear = hashClear_default;
Hash.prototype["delete"] = hashDelete_default;
Hash.prototype.get = hashGet_default;
Hash.prototype.has = hashHas_default;
Hash.prototype.set = hashSet_default;
var Hash_default = Hash;

// node_modules/lodash-es/_mapCacheClear.js
function mapCacheClear() {
  this.size = 0;
  this.__data__ = {
    "hash": new Hash_default(),
    "map": new (Map_default || ListCache_default)(),
    "string": new Hash_default()
  };
}
var mapCacheClear_default = mapCacheClear;

// node_modules/lodash-es/_isKeyable.js
function isKeyable(value) {
  var type = typeof value;
  return type == "string" || type == "number" || type == "symbol" || type == "boolean" ? value !== "__proto__" : value === null;
}
var isKeyable_default = isKeyable;

// node_modules/lodash-es/_getMapData.js
function getMapData(map, key) {
  var data = map.__data__;
  return isKeyable_default(key) ? data[typeof key == "string" ? "string" : "hash"] : data.map;
}
var getMapData_default = getMapData;

// node_modules/lodash-es/_mapCacheDelete.js
function mapCacheDelete(key) {
  var result = getMapData_default(this, key)["delete"](key);
  this.size -= result ? 1 : 0;
  return result;
}
var mapCacheDelete_default = mapCacheDelete;

// node_modules/lodash-es/_mapCacheGet.js
function mapCacheGet(key) {
  return getMapData_default(this, key).get(key);
}
var mapCacheGet_default = mapCacheGet;

// node_modules/lodash-es/_mapCacheHas.js
function mapCacheHas(key) {
  return getMapData_default(this, key).has(key);
}
var mapCacheHas_default = mapCacheHas;

// node_modules/lodash-es/_mapCacheSet.js
function mapCacheSet(key, value) {
  var data = getMapData_default(this, key), size = data.size;
  data.set(key, value);
  this.size += data.size == size ? 0 : 1;
  return this;
}
var mapCacheSet_default = mapCacheSet;

// node_modules/lodash-es/_MapCache.js
function MapCache(entries) {
  var index = -1, length = entries == null ? 0 : entries.length;
  this.clear();
  while (++index < length) {
    var entry = entries[index];
    this.set(entry[0], entry[1]);
  }
}
MapCache.prototype.clear = mapCacheClear_default;
MapCache.prototype["delete"] = mapCacheDelete_default;
MapCache.prototype.get = mapCacheGet_default;
MapCache.prototype.has = mapCacheHas_default;
MapCache.prototype.set = mapCacheSet_default;
var MapCache_default = MapCache;

// node_modules/lodash-es/_stackSet.js
var LARGE_ARRAY_SIZE = 200;
function stackSet(key, value) {
  var data = this.__data__;
  if (data instanceof ListCache_default) {
    var pairs = data.__data__;
    if (!Map_default || pairs.length < LARGE_ARRAY_SIZE - 1) {
      pairs.push([key, value]);
      this.size = ++data.size;
      return this;
    }
    data = this.__data__ = new MapCache_default(pairs);
  }
  data.set(key, value);
  this.size = data.size;
  return this;
}
var stackSet_default = stackSet;

// node_modules/lodash-es/_Stack.js
function Stack(entries) {
  var data = this.__data__ = new ListCache_default(entries);
  this.size = data.size;
}
Stack.prototype.clear = stackClear_default;
Stack.prototype["delete"] = stackDelete_default;
Stack.prototype.get = stackGet_default;
Stack.prototype.has = stackHas_default;
Stack.prototype.set = stackSet_default;
var Stack_default = Stack;

// node_modules/lodash-es/_setCacheAdd.js
var HASH_UNDEFINED3 = "__lodash_hash_undefined__";
function setCacheAdd(value) {
  this.__data__.set(value, HASH_UNDEFINED3);
  return this;
}
var setCacheAdd_default = setCacheAdd;

// node_modules/lodash-es/_setCacheHas.js
function setCacheHas(value) {
  return this.__data__.has(value);
}
var setCacheHas_default = setCacheHas;

// node_modules/lodash-es/_SetCache.js
function SetCache(values) {
  var index = -1, length = values == null ? 0 : values.length;
  this.__data__ = new MapCache_default();
  while (++index < length) {
    this.add(values[index]);
  }
}
SetCache.prototype.add = SetCache.prototype.push = setCacheAdd_default;
SetCache.prototype.has = setCacheHas_default;
var SetCache_default = SetCache;

// node_modules/lodash-es/_arraySome.js
function arraySome(array, predicate) {
  var index = -1, length = array == null ? 0 : array.length;
  while (++index < length) {
    if (predicate(array[index], index, array)) {
      return true;
    }
  }
  return false;
}
var arraySome_default = arraySome;

// node_modules/lodash-es/_cacheHas.js
function cacheHas(cache, key) {
  return cache.has(key);
}
var cacheHas_default = cacheHas;

// node_modules/lodash-es/_equalArrays.js
var COMPARE_PARTIAL_FLAG = 1;
var COMPARE_UNORDERED_FLAG = 2;
function equalArrays(array, other, bitmask, customizer, equalFunc, stack) {
  var isPartial = bitmask & COMPARE_PARTIAL_FLAG, arrLength = array.length, othLength = other.length;
  if (arrLength != othLength && !(isPartial && othLength > arrLength)) {
    return false;
  }
  var arrStacked = stack.get(array);
  var othStacked = stack.get(other);
  if (arrStacked && othStacked) {
    return arrStacked == other && othStacked == array;
  }
  var index = -1, result = true, seen = bitmask & COMPARE_UNORDERED_FLAG ? new SetCache_default() : void 0;
  stack.set(array, other);
  stack.set(other, array);
  while (++index < arrLength) {
    var arrValue = array[index], othValue = other[index];
    if (customizer) {
      var compared = isPartial ? customizer(othValue, arrValue, index, other, array, stack) : customizer(arrValue, othValue, index, array, other, stack);
    }
    if (compared !== void 0) {
      if (compared) {
        continue;
      }
      result = false;
      break;
    }
    if (seen) {
      if (!arraySome_default(other, function(othValue2, othIndex) {
        if (!cacheHas_default(seen, othIndex) && (arrValue === othValue2 || equalFunc(arrValue, othValue2, bitmask, customizer, stack))) {
          return seen.push(othIndex);
        }
      })) {
        result = false;
        break;
      }
    } else if (!(arrValue === othValue || equalFunc(arrValue, othValue, bitmask, customizer, stack))) {
      result = false;
      break;
    }
  }
  stack["delete"](array);
  stack["delete"](other);
  return result;
}
var equalArrays_default = equalArrays;

// node_modules/lodash-es/_Uint8Array.js
var Uint8Array2 = root_default.Uint8Array;
var Uint8Array_default = Uint8Array2;

// node_modules/lodash-es/_mapToArray.js
function mapToArray(map) {
  var index = -1, result = Array(map.size);
  map.forEach(function(value, key) {
    result[++index] = [key, value];
  });
  return result;
}
var mapToArray_default = mapToArray;

// node_modules/lodash-es/_setToArray.js
function setToArray(set2) {
  var index = -1, result = Array(set2.size);
  set2.forEach(function(value) {
    result[++index] = value;
  });
  return result;
}
var setToArray_default = setToArray;

// node_modules/lodash-es/_equalByTag.js
var COMPARE_PARTIAL_FLAG2 = 1;
var COMPARE_UNORDERED_FLAG2 = 2;
var boolTag = "[object Boolean]";
var dateTag = "[object Date]";
var errorTag = "[object Error]";
var mapTag = "[object Map]";
var numberTag = "[object Number]";
var regexpTag = "[object RegExp]";
var setTag = "[object Set]";
var stringTag = "[object String]";
var symbolTag = "[object Symbol]";
var arrayBufferTag = "[object ArrayBuffer]";
var dataViewTag = "[object DataView]";
var symbolProto = Symbol_default ? Symbol_default.prototype : void 0;
var symbolValueOf = symbolProto ? symbolProto.valueOf : void 0;
function equalByTag(object, other, tag, bitmask, customizer, equalFunc, stack) {
  switch (tag) {
    case dataViewTag:
      if (object.byteLength != other.byteLength || object.byteOffset != other.byteOffset) {
        return false;
      }
      object = object.buffer;
      other = other.buffer;
    case arrayBufferTag:
      if (object.byteLength != other.byteLength || !equalFunc(new Uint8Array_default(object), new Uint8Array_default(other))) {
        return false;
      }
      return true;
    case boolTag:
    case dateTag:
    case numberTag:
      return eq_default(+object, +other);
    case errorTag:
      return object.name == other.name && object.message == other.message;
    case regexpTag:
    case stringTag:
      return object == other + "";
    case mapTag:
      var convert = mapToArray_default;
    case setTag:
      var isPartial = bitmask & COMPARE_PARTIAL_FLAG2;
      convert || (convert = setToArray_default);
      if (object.size != other.size && !isPartial) {
        return false;
      }
      var stacked = stack.get(object);
      if (stacked) {
        return stacked == other;
      }
      bitmask |= COMPARE_UNORDERED_FLAG2;
      stack.set(object, other);
      var result = equalArrays_default(convert(object), convert(other), bitmask, customizer, equalFunc, stack);
      stack["delete"](object);
      return result;
    case symbolTag:
      if (symbolValueOf) {
        return symbolValueOf.call(object) == symbolValueOf.call(other);
      }
  }
  return false;
}
var equalByTag_default = equalByTag;

// node_modules/lodash-es/_arrayPush.js
function arrayPush(array, values) {
  var index = -1, length = values.length, offset = array.length;
  while (++index < length) {
    array[offset + index] = values[index];
  }
  return array;
}
var arrayPush_default = arrayPush;

// node_modules/lodash-es/isArray.js
var isArray = Array.isArray;
var isArray_default = isArray;

// node_modules/lodash-es/_baseGetAllKeys.js
function baseGetAllKeys(object, keysFunc, symbolsFunc) {
  var result = keysFunc(object);
  return isArray_default(object) ? result : arrayPush_default(result, symbolsFunc(object));
}
var baseGetAllKeys_default = baseGetAllKeys;

// node_modules/lodash-es/_arrayFilter.js
function arrayFilter(array, predicate) {
  var index = -1, length = array == null ? 0 : array.length, resIndex = 0, result = [];
  while (++index < length) {
    var value = array[index];
    if (predicate(value, index, array)) {
      result[resIndex++] = value;
    }
  }
  return result;
}
var arrayFilter_default = arrayFilter;

// node_modules/lodash-es/stubArray.js
function stubArray() {
  return [];
}
var stubArray_default = stubArray;

// node_modules/lodash-es/_getSymbols.js
var objectProto7 = Object.prototype;
var propertyIsEnumerable = objectProto7.propertyIsEnumerable;
var nativeGetSymbols = Object.getOwnPropertySymbols;
var getSymbols = !nativeGetSymbols ? stubArray_default : function(object) {
  if (object == null) {
    return [];
  }
  object = Object(object);
  return arrayFilter_default(nativeGetSymbols(object), function(symbol) {
    return propertyIsEnumerable.call(object, symbol);
  });
};
var getSymbols_default = getSymbols;

// node_modules/lodash-es/_baseTimes.js
function baseTimes(n, iteratee) {
  var index = -1, result = Array(n);
  while (++index < n) {
    result[index] = iteratee(index);
  }
  return result;
}
var baseTimes_default = baseTimes;

// node_modules/lodash-es/_baseIsArguments.js
var argsTag = "[object Arguments]";
function baseIsArguments(value) {
  return isObjectLike_default(value) && baseGetTag_default(value) == argsTag;
}
var baseIsArguments_default = baseIsArguments;

// node_modules/lodash-es/isArguments.js
var objectProto8 = Object.prototype;
var hasOwnProperty6 = objectProto8.hasOwnProperty;
var propertyIsEnumerable2 = objectProto8.propertyIsEnumerable;
var isArguments = baseIsArguments_default(/* @__PURE__ */ function() {
  return arguments;
}()) ? baseIsArguments_default : function(value) {
  return isObjectLike_default(value) && hasOwnProperty6.call(value, "callee") && !propertyIsEnumerable2.call(value, "callee");
};
var isArguments_default = isArguments;

// node_modules/lodash-es/stubFalse.js
function stubFalse() {
  return false;
}
var stubFalse_default = stubFalse;

// node_modules/lodash-es/isBuffer.js
var freeExports = typeof exports == "object" && exports && !exports.nodeType && exports;
var freeModule = freeExports && typeof module == "object" && module && !module.nodeType && module;
var moduleExports = freeModule && freeModule.exports === freeExports;
var Buffer = moduleExports ? root_default.Buffer : void 0;
var nativeIsBuffer = Buffer ? Buffer.isBuffer : void 0;
var isBuffer = nativeIsBuffer || stubFalse_default;
var isBuffer_default = isBuffer;

// node_modules/lodash-es/_isIndex.js
var MAX_SAFE_INTEGER = 9007199254740991;
var reIsUint = /^(?:0|[1-9]\d*)$/;
function isIndex(value, length) {
  var type = typeof value;
  length = length == null ? MAX_SAFE_INTEGER : length;
  return !!length && (type == "number" || type != "symbol" && reIsUint.test(value)) && (value > -1 && value % 1 == 0 && value < length);
}
var isIndex_default = isIndex;

// node_modules/lodash-es/isLength.js
var MAX_SAFE_INTEGER2 = 9007199254740991;
function isLength(value) {
  return typeof value == "number" && value > -1 && value % 1 == 0 && value <= MAX_SAFE_INTEGER2;
}
var isLength_default = isLength;

// node_modules/lodash-es/_baseIsTypedArray.js
var argsTag2 = "[object Arguments]";
var arrayTag = "[object Array]";
var boolTag2 = "[object Boolean]";
var dateTag2 = "[object Date]";
var errorTag2 = "[object Error]";
var funcTag2 = "[object Function]";
var mapTag2 = "[object Map]";
var numberTag2 = "[object Number]";
var objectTag2 = "[object Object]";
var regexpTag2 = "[object RegExp]";
var setTag2 = "[object Set]";
var stringTag2 = "[object String]";
var weakMapTag = "[object WeakMap]";
var arrayBufferTag2 = "[object ArrayBuffer]";
var dataViewTag2 = "[object DataView]";
var float32Tag = "[object Float32Array]";
var float64Tag = "[object Float64Array]";
var int8Tag = "[object Int8Array]";
var int16Tag = "[object Int16Array]";
var int32Tag = "[object Int32Array]";
var uint8Tag = "[object Uint8Array]";
var uint8ClampedTag = "[object Uint8ClampedArray]";
var uint16Tag = "[object Uint16Array]";
var uint32Tag = "[object Uint32Array]";
var typedArrayTags = {};
typedArrayTags[float32Tag] = typedArrayTags[float64Tag] = typedArrayTags[int8Tag] = typedArrayTags[int16Tag] = typedArrayTags[int32Tag] = typedArrayTags[uint8Tag] = typedArrayTags[uint8ClampedTag] = typedArrayTags[uint16Tag] = typedArrayTags[uint32Tag] = true;
typedArrayTags[argsTag2] = typedArrayTags[arrayTag] = typedArrayTags[arrayBufferTag2] = typedArrayTags[boolTag2] = typedArrayTags[dataViewTag2] = typedArrayTags[dateTag2] = typedArrayTags[errorTag2] = typedArrayTags[funcTag2] = typedArrayTags[mapTag2] = typedArrayTags[numberTag2] = typedArrayTags[objectTag2] = typedArrayTags[regexpTag2] = typedArrayTags[setTag2] = typedArrayTags[stringTag2] = typedArrayTags[weakMapTag] = false;
function baseIsTypedArray(value) {
  return isObjectLike_default(value) && isLength_default(value.length) && !!typedArrayTags[baseGetTag_default(value)];
}
var baseIsTypedArray_default = baseIsTypedArray;

// node_modules/lodash-es/_baseUnary.js
function baseUnary(func) {
  return function(value) {
    return func(value);
  };
}
var baseUnary_default = baseUnary;

// node_modules/lodash-es/_nodeUtil.js
var freeExports2 = typeof exports == "object" && exports && !exports.nodeType && exports;
var freeModule2 = freeExports2 && typeof module == "object" && module && !module.nodeType && module;
var moduleExports2 = freeModule2 && freeModule2.exports === freeExports2;
var freeProcess = moduleExports2 && freeGlobal_default.process;
var nodeUtil = function() {
  try {
    var types = freeModule2 && freeModule2.require && freeModule2.require("util").types;
    if (types) {
      return types;
    }
    return freeProcess && freeProcess.binding && freeProcess.binding("util");
  } catch (e) {
  }
}();
var nodeUtil_default = nodeUtil;

// node_modules/lodash-es/isTypedArray.js
var nodeIsTypedArray = nodeUtil_default && nodeUtil_default.isTypedArray;
var isTypedArray = nodeIsTypedArray ? baseUnary_default(nodeIsTypedArray) : baseIsTypedArray_default;
var isTypedArray_default = isTypedArray;

// node_modules/lodash-es/_arrayLikeKeys.js
var objectProto9 = Object.prototype;
var hasOwnProperty7 = objectProto9.hasOwnProperty;
function arrayLikeKeys(value, inherited) {
  var isArr = isArray_default(value), isArg = !isArr && isArguments_default(value), isBuff = !isArr && !isArg && isBuffer_default(value), isType = !isArr && !isArg && !isBuff && isTypedArray_default(value), skipIndexes = isArr || isArg || isBuff || isType, result = skipIndexes ? baseTimes_default(value.length, String) : [], length = result.length;
  for (var key in value) {
    if ((inherited || hasOwnProperty7.call(value, key)) && !(skipIndexes && // Safari 9 has enumerable `arguments.length` in strict mode.
    (key == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    isBuff && (key == "offset" || key == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    isType && (key == "buffer" || key == "byteLength" || key == "byteOffset") || // Skip index properties.
    isIndex_default(key, length)))) {
      result.push(key);
    }
  }
  return result;
}
var arrayLikeKeys_default = arrayLikeKeys;

// node_modules/lodash-es/_isPrototype.js
var objectProto10 = Object.prototype;
function isPrototype(value) {
  var Ctor = value && value.constructor, proto = typeof Ctor == "function" && Ctor.prototype || objectProto10;
  return value === proto;
}
var isPrototype_default = isPrototype;

// node_modules/lodash-es/_nativeKeys.js
var nativeKeys = overArg_default(Object.keys, Object);
var nativeKeys_default = nativeKeys;

// node_modules/lodash-es/_baseKeys.js
var objectProto11 = Object.prototype;
var hasOwnProperty8 = objectProto11.hasOwnProperty;
function baseKeys(object) {
  if (!isPrototype_default(object)) {
    return nativeKeys_default(object);
  }
  var result = [];
  for (var key in Object(object)) {
    if (hasOwnProperty8.call(object, key) && key != "constructor") {
      result.push(key);
    }
  }
  return result;
}
var baseKeys_default = baseKeys;

// node_modules/lodash-es/isArrayLike.js
function isArrayLike(value) {
  return value != null && isLength_default(value.length) && !isFunction_default(value);
}
var isArrayLike_default = isArrayLike;

// node_modules/lodash-es/keys.js
function keys(object) {
  return isArrayLike_default(object) ? arrayLikeKeys_default(object) : baseKeys_default(object);
}
var keys_default = keys;

// node_modules/lodash-es/_getAllKeys.js
function getAllKeys(object) {
  return baseGetAllKeys_default(object, keys_default, getSymbols_default);
}
var getAllKeys_default = getAllKeys;

// node_modules/lodash-es/_equalObjects.js
var COMPARE_PARTIAL_FLAG3 = 1;
var objectProto12 = Object.prototype;
var hasOwnProperty9 = objectProto12.hasOwnProperty;
function equalObjects(object, other, bitmask, customizer, equalFunc, stack) {
  var isPartial = bitmask & COMPARE_PARTIAL_FLAG3, objProps = getAllKeys_default(object), objLength = objProps.length, othProps = getAllKeys_default(other), othLength = othProps.length;
  if (objLength != othLength && !isPartial) {
    return false;
  }
  var index = objLength;
  while (index--) {
    var key = objProps[index];
    if (!(isPartial ? key in other : hasOwnProperty9.call(other, key))) {
      return false;
    }
  }
  var objStacked = stack.get(object);
  var othStacked = stack.get(other);
  if (objStacked && othStacked) {
    return objStacked == other && othStacked == object;
  }
  var result = true;
  stack.set(object, other);
  stack.set(other, object);
  var skipCtor = isPartial;
  while (++index < objLength) {
    key = objProps[index];
    var objValue = object[key], othValue = other[key];
    if (customizer) {
      var compared = isPartial ? customizer(othValue, objValue, key, other, object, stack) : customizer(objValue, othValue, key, object, other, stack);
    }
    if (!(compared === void 0 ? objValue === othValue || equalFunc(objValue, othValue, bitmask, customizer, stack) : compared)) {
      result = false;
      break;
    }
    skipCtor || (skipCtor = key == "constructor");
  }
  if (result && !skipCtor) {
    var objCtor = object.constructor, othCtor = other.constructor;
    if (objCtor != othCtor && ("constructor" in object && "constructor" in other) && !(typeof objCtor == "function" && objCtor instanceof objCtor && typeof othCtor == "function" && othCtor instanceof othCtor)) {
      result = false;
    }
  }
  stack["delete"](object);
  stack["delete"](other);
  return result;
}
var equalObjects_default = equalObjects;

// node_modules/lodash-es/_DataView.js
var DataView = getNative_default(root_default, "DataView");
var DataView_default = DataView;

// node_modules/lodash-es/_Promise.js
var Promise2 = getNative_default(root_default, "Promise");
var Promise_default = Promise2;

// node_modules/lodash-es/_Set.js
var Set2 = getNative_default(root_default, "Set");
var Set_default = Set2;

// node_modules/lodash-es/_WeakMap.js
var WeakMap = getNative_default(root_default, "WeakMap");
var WeakMap_default = WeakMap;

// node_modules/lodash-es/_getTag.js
var mapTag3 = "[object Map]";
var objectTag3 = "[object Object]";
var promiseTag = "[object Promise]";
var setTag3 = "[object Set]";
var weakMapTag2 = "[object WeakMap]";
var dataViewTag3 = "[object DataView]";
var dataViewCtorString = toSource_default(DataView_default);
var mapCtorString = toSource_default(Map_default);
var promiseCtorString = toSource_default(Promise_default);
var setCtorString = toSource_default(Set_default);
var weakMapCtorString = toSource_default(WeakMap_default);
var getTag = baseGetTag_default;
if (DataView_default && getTag(new DataView_default(new ArrayBuffer(1))) != dataViewTag3 || Map_default && getTag(new Map_default()) != mapTag3 || Promise_default && getTag(Promise_default.resolve()) != promiseTag || Set_default && getTag(new Set_default()) != setTag3 || WeakMap_default && getTag(new WeakMap_default()) != weakMapTag2) {
  getTag = function(value) {
    var result = baseGetTag_default(value), Ctor = result == objectTag3 ? value.constructor : void 0, ctorString = Ctor ? toSource_default(Ctor) : "";
    if (ctorString) {
      switch (ctorString) {
        case dataViewCtorString:
          return dataViewTag3;
        case mapCtorString:
          return mapTag3;
        case promiseCtorString:
          return promiseTag;
        case setCtorString:
          return setTag3;
        case weakMapCtorString:
          return weakMapTag2;
      }
    }
    return result;
  };
}
var getTag_default = getTag;

// node_modules/lodash-es/_baseIsEqualDeep.js
var COMPARE_PARTIAL_FLAG4 = 1;
var argsTag3 = "[object Arguments]";
var arrayTag2 = "[object Array]";
var objectTag4 = "[object Object]";
var objectProto13 = Object.prototype;
var hasOwnProperty10 = objectProto13.hasOwnProperty;
function baseIsEqualDeep(object, other, bitmask, customizer, equalFunc, stack) {
  var objIsArr = isArray_default(object), othIsArr = isArray_default(other), objTag = objIsArr ? arrayTag2 : getTag_default(object), othTag = othIsArr ? arrayTag2 : getTag_default(other);
  objTag = objTag == argsTag3 ? objectTag4 : objTag;
  othTag = othTag == argsTag3 ? objectTag4 : othTag;
  var objIsObj = objTag == objectTag4, othIsObj = othTag == objectTag4, isSameTag = objTag == othTag;
  if (isSameTag && isBuffer_default(object)) {
    if (!isBuffer_default(other)) {
      return false;
    }
    objIsArr = true;
    objIsObj = false;
  }
  if (isSameTag && !objIsObj) {
    stack || (stack = new Stack_default());
    return objIsArr || isTypedArray_default(object) ? equalArrays_default(object, other, bitmask, customizer, equalFunc, stack) : equalByTag_default(object, other, objTag, bitmask, customizer, equalFunc, stack);
  }
  if (!(bitmask & COMPARE_PARTIAL_FLAG4)) {
    var objIsWrapped = objIsObj && hasOwnProperty10.call(object, "__wrapped__"), othIsWrapped = othIsObj && hasOwnProperty10.call(other, "__wrapped__");
    if (objIsWrapped || othIsWrapped) {
      var objUnwrapped = objIsWrapped ? object.value() : object, othUnwrapped = othIsWrapped ? other.value() : other;
      stack || (stack = new Stack_default());
      return equalFunc(objUnwrapped, othUnwrapped, bitmask, customizer, stack);
    }
  }
  if (!isSameTag) {
    return false;
  }
  stack || (stack = new Stack_default());
  return equalObjects_default(object, other, bitmask, customizer, equalFunc, stack);
}
var baseIsEqualDeep_default = baseIsEqualDeep;

// node_modules/lodash-es/_baseIsEqual.js
function baseIsEqual(value, other, bitmask, customizer, stack) {
  if (value === other) {
    return true;
  }
  if (value == null || other == null || !isObjectLike_default(value) && !isObjectLike_default(other)) {
    return value !== value && other !== other;
  }
  return baseIsEqualDeep_default(value, other, bitmask, customizer, baseIsEqual, stack);
}
var baseIsEqual_default = baseIsEqual;

// node_modules/lodash-es/isEqualWith.js
function isEqualWith(value, other, customizer) {
  customizer = typeof customizer == "function" ? customizer : void 0;
  var result = customizer ? customizer(value, other) : void 0;
  return result === void 0 ? baseIsEqual_default(value, other, void 0, customizer) : !!result;
}
var isEqualWith_default = isEqualWith;

// node_modules/@rjsf/utils/lib/deepEquals.js
function deepEquals(a, b) {
  return isEqualWith_default(a, b, (obj, other) => {
    if (typeof obj === "function" && typeof other === "function") {
      return true;
    }
    return void 0;
  });
}

// node_modules/lodash-es/isSymbol.js
var symbolTag2 = "[object Symbol]";
function isSymbol(value) {
  return typeof value == "symbol" || isObjectLike_default(value) && baseGetTag_default(value) == symbolTag2;
}
var isSymbol_default = isSymbol;

// node_modules/lodash-es/_isKey.js
var reIsDeepProp = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/;
var reIsPlainProp = /^\w*$/;
function isKey(value, object) {
  if (isArray_default(value)) {
    return false;
  }
  var type = typeof value;
  if (type == "number" || type == "symbol" || type == "boolean" || value == null || isSymbol_default(value)) {
    return true;
  }
  return reIsPlainProp.test(value) || !reIsDeepProp.test(value) || object != null && value in Object(object);
}
var isKey_default = isKey;

// node_modules/lodash-es/memoize.js
var FUNC_ERROR_TEXT = "Expected a function";
function memoize(func, resolver) {
  if (typeof func != "function" || resolver != null && typeof resolver != "function") {
    throw new TypeError(FUNC_ERROR_TEXT);
  }
  var memoized = function() {
    var args = arguments, key = resolver ? resolver.apply(this, args) : args[0], cache = memoized.cache;
    if (cache.has(key)) {
      return cache.get(key);
    }
    var result = func.apply(this, args);
    memoized.cache = cache.set(key, result) || cache;
    return result;
  };
  memoized.cache = new (memoize.Cache || MapCache_default)();
  return memoized;
}
memoize.Cache = MapCache_default;
var memoize_default = memoize;

// node_modules/lodash-es/_memoizeCapped.js
var MAX_MEMOIZE_SIZE = 500;
function memoizeCapped(func) {
  var result = memoize_default(func, function(key) {
    if (cache.size === MAX_MEMOIZE_SIZE) {
      cache.clear();
    }
    return key;
  });
  var cache = result.cache;
  return result;
}
var memoizeCapped_default = memoizeCapped;

// node_modules/lodash-es/_stringToPath.js
var rePropName = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g;
var reEscapeChar = /\\(\\)?/g;
var stringToPath = memoizeCapped_default(function(string) {
  var result = [];
  if (string.charCodeAt(0) === 46) {
    result.push("");
  }
  string.replace(rePropName, function(match, number, quote, subString) {
    result.push(quote ? subString.replace(reEscapeChar, "$1") : number || match);
  });
  return result;
});
var stringToPath_default = stringToPath;

// node_modules/lodash-es/_arrayMap.js
function arrayMap(array, iteratee) {
  var index = -1, length = array == null ? 0 : array.length, result = Array(length);
  while (++index < length) {
    result[index] = iteratee(array[index], index, array);
  }
  return result;
}
var arrayMap_default = arrayMap;

// node_modules/lodash-es/_baseToString.js
var INFINITY = 1 / 0;
var symbolProto2 = Symbol_default ? Symbol_default.prototype : void 0;
var symbolToString = symbolProto2 ? symbolProto2.toString : void 0;
function baseToString(value) {
  if (typeof value == "string") {
    return value;
  }
  if (isArray_default(value)) {
    return arrayMap_default(value, baseToString) + "";
  }
  if (isSymbol_default(value)) {
    return symbolToString ? symbolToString.call(value) : "";
  }
  var result = value + "";
  return result == "0" && 1 / value == -INFINITY ? "-0" : result;
}
var baseToString_default = baseToString;

// node_modules/lodash-es/toString.js
function toString(value) {
  return value == null ? "" : baseToString_default(value);
}
var toString_default = toString;

// node_modules/lodash-es/_castPath.js
function castPath(value, object) {
  if (isArray_default(value)) {
    return value;
  }
  return isKey_default(value, object) ? [value] : stringToPath_default(toString_default(value));
}
var castPath_default = castPath;

// node_modules/lodash-es/_toKey.js
var INFINITY2 = 1 / 0;
function toKey(value) {
  if (typeof value == "string" || isSymbol_default(value)) {
    return value;
  }
  var result = value + "";
  return result == "0" && 1 / value == -INFINITY2 ? "-0" : result;
}
var toKey_default = toKey;

// node_modules/lodash-es/_baseGet.js
function baseGet(object, path) {
  path = castPath_default(path, object);
  var index = 0, length = path.length;
  while (object != null && index < length) {
    object = object[toKey_default(path[index++])];
  }
  return index && index == length ? object : void 0;
}
var baseGet_default = baseGet;

// node_modules/lodash-es/get.js
function get(object, path, defaultValue) {
  var result = object == null ? void 0 : baseGet_default(object, path);
  return result === void 0 ? defaultValue : result;
}
var get_default = get;

// node_modules/lodash-es/isEmpty.js
var mapTag4 = "[object Map]";
var setTag4 = "[object Set]";
var objectProto14 = Object.prototype;
var hasOwnProperty11 = objectProto14.hasOwnProperty;
function isEmpty(value) {
  if (value == null) {
    return true;
  }
  if (isArrayLike_default(value) && (isArray_default(value) || typeof value == "string" || typeof value.splice == "function" || isBuffer_default(value) || isTypedArray_default(value) || isArguments_default(value))) {
    return !value.length;
  }
  var tag = getTag_default(value);
  if (tag == mapTag4 || tag == setTag4) {
    return !value.size;
  }
  if (isPrototype_default(value)) {
    return !baseKeys_default(value).length;
  }
  for (var key in value) {
    if (hasOwnProperty11.call(value, key)) {
      return false;
    }
  }
  return true;
}
var isEmpty_default = isEmpty;

// node_modules/lodash-es/isNil.js
function isNil(value) {
  return value == null;
}
var isNil_default = isNil;

// node_modules/@rjsf/utils/lib/mergeObjects.js
function mergeObjects(obj1, obj2, concatArrays = false) {
  return Object.keys(obj2).reduce((acc, key) => {
    const left = obj1 ? obj1[key] : {}, right = obj2[key];
    if (obj1 && key in obj1 && isObject(right)) {
      acc[key] = mergeObjects(left, right, concatArrays);
    } else if (concatArrays && Array.isArray(left) && Array.isArray(right)) {
      let toMerge = right;
      if (concatArrays === "preventDuplicates") {
        toMerge = right.reduce((result, value) => {
          if (!left.includes(value)) {
            result.push(value);
          }
          return result;
        }, []);
      }
      acc[key] = left.concat(toMerge);
    } else {
      acc[key] = right;
    }
    return acc;
  }, Object.assign({}, obj1));
}

// node_modules/lodash-es/_baseHas.js
var objectProto15 = Object.prototype;
var hasOwnProperty12 = objectProto15.hasOwnProperty;
function baseHas(object, key) {
  return object != null && hasOwnProperty12.call(object, key);
}
var baseHas_default = baseHas;

// node_modules/lodash-es/_hasPath.js
function hasPath(object, path, hasFunc) {
  path = castPath_default(path, object);
  var index = -1, length = path.length, result = false;
  while (++index < length) {
    var key = toKey_default(path[index]);
    if (!(result = object != null && hasFunc(object, key))) {
      break;
    }
    object = object[key];
  }
  if (result || ++index != length) {
    return result;
  }
  length = object == null ? 0 : object.length;
  return !!length && isLength_default(length) && isIndex_default(key, length) && (isArray_default(object) || isArguments_default(object));
}
var hasPath_default = hasPath;

// node_modules/lodash-es/has.js
function has(object, path) {
  return object != null && hasPath_default(object, path, baseHas_default);
}
var has_default = has;

// node_modules/lodash-es/isEqual.js
function isEqual(value, other) {
  return baseIsEqual_default(value, other);
}
var isEqual_default = isEqual;

// node_modules/lodash-es/_defineProperty.js
var defineProperty = function() {
  try {
    var func = getNative_default(Object, "defineProperty");
    func({}, "", {});
    return func;
  } catch (e) {
  }
}();
var defineProperty_default = defineProperty;

// node_modules/lodash-es/_baseAssignValue.js
function baseAssignValue(object, key, value) {
  if (key == "__proto__" && defineProperty_default) {
    defineProperty_default(object, key, {
      "configurable": true,
      "enumerable": true,
      "value": value,
      "writable": true
    });
  } else {
    object[key] = value;
  }
}
var baseAssignValue_default = baseAssignValue;

// node_modules/lodash-es/_assignValue.js
var objectProto16 = Object.prototype;
var hasOwnProperty13 = objectProto16.hasOwnProperty;
function assignValue(object, key, value) {
  var objValue = object[key];
  if (!(hasOwnProperty13.call(object, key) && eq_default(objValue, value)) || value === void 0 && !(key in object)) {
    baseAssignValue_default(object, key, value);
  }
}
var assignValue_default = assignValue;

// node_modules/lodash-es/_baseSet.js
function baseSet(object, path, value, customizer) {
  if (!isObject_default(object)) {
    return object;
  }
  path = castPath_default(path, object);
  var index = -1, length = path.length, lastIndex = length - 1, nested = object;
  while (nested != null && ++index < length) {
    var key = toKey_default(path[index]), newValue = value;
    if (key === "__proto__" || key === "constructor" || key === "prototype") {
      return object;
    }
    if (index != lastIndex) {
      var objValue = nested[key];
      newValue = customizer ? customizer(objValue, key, nested) : void 0;
      if (newValue === void 0) {
        newValue = isObject_default(objValue) ? objValue : isIndex_default(path[index + 1]) ? [] : {};
      }
    }
    assignValue_default(nested, key, newValue);
    nested = nested[key];
  }
  return object;
}
var baseSet_default = baseSet;

// node_modules/lodash-es/set.js
function set(object, path, value) {
  return object == null ? object : baseSet_default(object, path, value);
}
var set_default = set;

// node_modules/lodash-es/identity.js
function identity(value) {
  return value;
}
var identity_default = identity;

// node_modules/lodash-es/_castFunction.js
function castFunction(value) {
  return typeof value == "function" ? value : identity_default;
}
var castFunction_default = castFunction;

// node_modules/lodash-es/_trimmedEndIndex.js
var reWhitespace = /\s/;
function trimmedEndIndex(string) {
  var index = string.length;
  while (index-- && reWhitespace.test(string.charAt(index))) {
  }
  return index;
}
var trimmedEndIndex_default = trimmedEndIndex;

// node_modules/lodash-es/_baseTrim.js
var reTrimStart = /^\s+/;
function baseTrim(string) {
  return string ? string.slice(0, trimmedEndIndex_default(string) + 1).replace(reTrimStart, "") : string;
}
var baseTrim_default = baseTrim;

// node_modules/lodash-es/toNumber.js
var NAN = 0 / 0;
var reIsBadHex = /^[-+]0x[0-9a-f]+$/i;
var reIsBinary = /^0b[01]+$/i;
var reIsOctal = /^0o[0-7]+$/i;
var freeParseInt = parseInt;
function toNumber(value) {
  if (typeof value == "number") {
    return value;
  }
  if (isSymbol_default(value)) {
    return NAN;
  }
  if (isObject_default(value)) {
    var other = typeof value.valueOf == "function" ? value.valueOf() : value;
    value = isObject_default(other) ? other + "" : other;
  }
  if (typeof value != "string") {
    return value === 0 ? value : +value;
  }
  value = baseTrim_default(value);
  var isBinary = reIsBinary.test(value);
  return isBinary || reIsOctal.test(value) ? freeParseInt(value.slice(2), isBinary ? 2 : 8) : reIsBadHex.test(value) ? NAN : +value;
}
var toNumber_default = toNumber;

// node_modules/lodash-es/toFinite.js
var INFINITY3 = 1 / 0;
var MAX_INTEGER = 17976931348623157e292;
function toFinite(value) {
  if (!value) {
    return value === 0 ? value : 0;
  }
  value = toNumber_default(value);
  if (value === INFINITY3 || value === -INFINITY3) {
    var sign = value < 0 ? -1 : 1;
    return sign * MAX_INTEGER;
  }
  return value === value ? value : 0;
}
var toFinite_default = toFinite;

// node_modules/lodash-es/toInteger.js
function toInteger(value) {
  var result = toFinite_default(value), remainder = result % 1;
  return result === result ? remainder ? result - remainder : result : 0;
}
var toInteger_default = toInteger;

// node_modules/lodash-es/times.js
var MAX_SAFE_INTEGER3 = 9007199254740991;
var MAX_ARRAY_LENGTH = 4294967295;
var nativeMin = Math.min;
function times(n, iteratee) {
  n = toInteger_default(n);
  if (n < 1 || n > MAX_SAFE_INTEGER3) {
    return [];
  }
  var index = MAX_ARRAY_LENGTH, length = nativeMin(n, MAX_ARRAY_LENGTH);
  iteratee = castFunction_default(iteratee);
  n -= MAX_ARRAY_LENGTH;
  var result = baseTimes_default(length, iteratee);
  while (++index < n) {
    iteratee(index);
  }
  return result;
}
var times_default = times;

// node_modules/lodash-es/_arrayEach.js
function arrayEach(array, iteratee) {
  var index = -1, length = array == null ? 0 : array.length;
  while (++index < length) {
    if (iteratee(array[index], index, array) === false) {
      break;
    }
  }
  return array;
}
var arrayEach_default = arrayEach;

// node_modules/lodash-es/_baseCreate.js
var objectCreate = Object.create;
var baseCreate = /* @__PURE__ */ function() {
  function object() {
  }
  return function(proto) {
    if (!isObject_default(proto)) {
      return {};
    }
    if (objectCreate) {
      return objectCreate(proto);
    }
    object.prototype = proto;
    var result = new object();
    object.prototype = void 0;
    return result;
  };
}();
var baseCreate_default = baseCreate;

// node_modules/lodash-es/_createBaseFor.js
function createBaseFor(fromRight) {
  return function(object, iteratee, keysFunc) {
    var index = -1, iterable = Object(object), props = keysFunc(object), length = props.length;
    while (length--) {
      var key = props[fromRight ? length : ++index];
      if (iteratee(iterable[key], key, iterable) === false) {
        break;
      }
    }
    return object;
  };
}
var createBaseFor_default = createBaseFor;

// node_modules/lodash-es/_baseFor.js
var baseFor = createBaseFor_default();
var baseFor_default = baseFor;

// node_modules/lodash-es/_baseForOwn.js
function baseForOwn(object, iteratee) {
  return object && baseFor_default(object, iteratee, keys_default);
}
var baseForOwn_default = baseForOwn;

// node_modules/lodash-es/_baseIsMatch.js
var COMPARE_PARTIAL_FLAG5 = 1;
var COMPARE_UNORDERED_FLAG3 = 2;
function baseIsMatch(object, source, matchData, customizer) {
  var index = matchData.length, length = index, noCustomizer = !customizer;
  if (object == null) {
    return !length;
  }
  object = Object(object);
  while (index--) {
    var data = matchData[index];
    if (noCustomizer && data[2] ? data[1] !== object[data[0]] : !(data[0] in object)) {
      return false;
    }
  }
  while (++index < length) {
    data = matchData[index];
    var key = data[0], objValue = object[key], srcValue = data[1];
    if (noCustomizer && data[2]) {
      if (objValue === void 0 && !(key in object)) {
        return false;
      }
    } else {
      var stack = new Stack_default();
      if (customizer) {
        var result = customizer(objValue, srcValue, key, object, source, stack);
      }
      if (!(result === void 0 ? baseIsEqual_default(srcValue, objValue, COMPARE_PARTIAL_FLAG5 | COMPARE_UNORDERED_FLAG3, customizer, stack) : result)) {
        return false;
      }
    }
  }
  return true;
}
var baseIsMatch_default = baseIsMatch;

// node_modules/lodash-es/_isStrictComparable.js
function isStrictComparable(value) {
  return value === value && !isObject_default(value);
}
var isStrictComparable_default = isStrictComparable;

// node_modules/lodash-es/_getMatchData.js
function getMatchData(object) {
  var result = keys_default(object), length = result.length;
  while (length--) {
    var key = result[length], value = object[key];
    result[length] = [key, value, isStrictComparable_default(value)];
  }
  return result;
}
var getMatchData_default = getMatchData;

// node_modules/lodash-es/_matchesStrictComparable.js
function matchesStrictComparable(key, srcValue) {
  return function(object) {
    if (object == null) {
      return false;
    }
    return object[key] === srcValue && (srcValue !== void 0 || key in Object(object));
  };
}
var matchesStrictComparable_default = matchesStrictComparable;

// node_modules/lodash-es/_baseMatches.js
function baseMatches(source) {
  var matchData = getMatchData_default(source);
  if (matchData.length == 1 && matchData[0][2]) {
    return matchesStrictComparable_default(matchData[0][0], matchData[0][1]);
  }
  return function(object) {
    return object === source || baseIsMatch_default(object, source, matchData);
  };
}
var baseMatches_default = baseMatches;

// node_modules/lodash-es/_baseHasIn.js
function baseHasIn(object, key) {
  return object != null && key in Object(object);
}
var baseHasIn_default = baseHasIn;

// node_modules/lodash-es/hasIn.js
function hasIn(object, path) {
  return object != null && hasPath_default(object, path, baseHasIn_default);
}
var hasIn_default = hasIn;

// node_modules/lodash-es/_baseMatchesProperty.js
var COMPARE_PARTIAL_FLAG6 = 1;
var COMPARE_UNORDERED_FLAG4 = 2;
function baseMatchesProperty(path, srcValue) {
  if (isKey_default(path) && isStrictComparable_default(srcValue)) {
    return matchesStrictComparable_default(toKey_default(path), srcValue);
  }
  return function(object) {
    var objValue = get_default(object, path);
    return objValue === void 0 && objValue === srcValue ? hasIn_default(object, path) : baseIsEqual_default(srcValue, objValue, COMPARE_PARTIAL_FLAG6 | COMPARE_UNORDERED_FLAG4);
  };
}
var baseMatchesProperty_default = baseMatchesProperty;

// node_modules/lodash-es/_baseProperty.js
function baseProperty(key) {
  return function(object) {
    return object == null ? void 0 : object[key];
  };
}
var baseProperty_default = baseProperty;

// node_modules/lodash-es/_basePropertyDeep.js
function basePropertyDeep(path) {
  return function(object) {
    return baseGet_default(object, path);
  };
}
var basePropertyDeep_default = basePropertyDeep;

// node_modules/lodash-es/property.js
function property(path) {
  return isKey_default(path) ? baseProperty_default(toKey_default(path)) : basePropertyDeep_default(path);
}
var property_default = property;

// node_modules/lodash-es/_baseIteratee.js
function baseIteratee(value) {
  if (typeof value == "function") {
    return value;
  }
  if (value == null) {
    return identity_default;
  }
  if (typeof value == "object") {
    return isArray_default(value) ? baseMatchesProperty_default(value[0], value[1]) : baseMatches_default(value);
  }
  return property_default(value);
}
var baseIteratee_default = baseIteratee;

// node_modules/lodash-es/transform.js
function transform(object, iteratee, accumulator) {
  var isArr = isArray_default(object), isArrLike = isArr || isBuffer_default(object) || isTypedArray_default(object);
  iteratee = baseIteratee_default(iteratee, 4);
  if (accumulator == null) {
    var Ctor = object && object.constructor;
    if (isArrLike) {
      accumulator = isArr ? new Ctor() : [];
    } else if (isObject_default(object)) {
      accumulator = isFunction_default(Ctor) ? baseCreate_default(getPrototype_default(object)) : {};
    } else {
      accumulator = {};
    }
  }
  (isArrLike ? arrayEach_default : baseForOwn_default)(object, function(value, index, object2) {
    return iteratee(accumulator, value, index, object2);
  });
  return accumulator;
}
var transform_default = transform;

// node_modules/lodash-es/_assignMergeValue.js
function assignMergeValue(object, key, value) {
  if (value !== void 0 && !eq_default(object[key], value) || value === void 0 && !(key in object)) {
    baseAssignValue_default(object, key, value);
  }
}
var assignMergeValue_default = assignMergeValue;

// node_modules/lodash-es/_cloneBuffer.js
var freeExports3 = typeof exports == "object" && exports && !exports.nodeType && exports;
var freeModule3 = freeExports3 && typeof module == "object" && module && !module.nodeType && module;
var moduleExports3 = freeModule3 && freeModule3.exports === freeExports3;
var Buffer2 = moduleExports3 ? root_default.Buffer : void 0;
var allocUnsafe = Buffer2 ? Buffer2.allocUnsafe : void 0;
function cloneBuffer(buffer, isDeep) {
  if (isDeep) {
    return buffer.slice();
  }
  var length = buffer.length, result = allocUnsafe ? allocUnsafe(length) : new buffer.constructor(length);
  buffer.copy(result);
  return result;
}
var cloneBuffer_default = cloneBuffer;

// node_modules/lodash-es/_cloneArrayBuffer.js
function cloneArrayBuffer(arrayBuffer) {
  var result = new arrayBuffer.constructor(arrayBuffer.byteLength);
  new Uint8Array_default(result).set(new Uint8Array_default(arrayBuffer));
  return result;
}
var cloneArrayBuffer_default = cloneArrayBuffer;

// node_modules/lodash-es/_cloneTypedArray.js
function cloneTypedArray(typedArray, isDeep) {
  var buffer = isDeep ? cloneArrayBuffer_default(typedArray.buffer) : typedArray.buffer;
  return new typedArray.constructor(buffer, typedArray.byteOffset, typedArray.length);
}
var cloneTypedArray_default = cloneTypedArray;

// node_modules/lodash-es/_copyArray.js
function copyArray(source, array) {
  var index = -1, length = source.length;
  array || (array = Array(length));
  while (++index < length) {
    array[index] = source[index];
  }
  return array;
}
var copyArray_default = copyArray;

// node_modules/lodash-es/_initCloneObject.js
function initCloneObject(object) {
  return typeof object.constructor == "function" && !isPrototype_default(object) ? baseCreate_default(getPrototype_default(object)) : {};
}
var initCloneObject_default = initCloneObject;

// node_modules/lodash-es/isArrayLikeObject.js
function isArrayLikeObject(value) {
  return isObjectLike_default(value) && isArrayLike_default(value);
}
var isArrayLikeObject_default = isArrayLikeObject;

// node_modules/lodash-es/_safeGet.js
function safeGet(object, key) {
  if (key === "constructor" && typeof object[key] === "function") {
    return;
  }
  if (key == "__proto__") {
    return;
  }
  return object[key];
}
var safeGet_default = safeGet;

// node_modules/lodash-es/_copyObject.js
function copyObject(source, props, object, customizer) {
  var isNew = !object;
  object || (object = {});
  var index = -1, length = props.length;
  while (++index < length) {
    var key = props[index];
    var newValue = customizer ? customizer(object[key], source[key], key, object, source) : void 0;
    if (newValue === void 0) {
      newValue = source[key];
    }
    if (isNew) {
      baseAssignValue_default(object, key, newValue);
    } else {
      assignValue_default(object, key, newValue);
    }
  }
  return object;
}
var copyObject_default = copyObject;

// node_modules/lodash-es/_nativeKeysIn.js
function nativeKeysIn(object) {
  var result = [];
  if (object != null) {
    for (var key in Object(object)) {
      result.push(key);
    }
  }
  return result;
}
var nativeKeysIn_default = nativeKeysIn;

// node_modules/lodash-es/_baseKeysIn.js
var objectProto17 = Object.prototype;
var hasOwnProperty14 = objectProto17.hasOwnProperty;
function baseKeysIn(object) {
  if (!isObject_default(object)) {
    return nativeKeysIn_default(object);
  }
  var isProto = isPrototype_default(object), result = [];
  for (var key in object) {
    if (!(key == "constructor" && (isProto || !hasOwnProperty14.call(object, key)))) {
      result.push(key);
    }
  }
  return result;
}
var baseKeysIn_default = baseKeysIn;

// node_modules/lodash-es/keysIn.js
function keysIn(object) {
  return isArrayLike_default(object) ? arrayLikeKeys_default(object, true) : baseKeysIn_default(object);
}
var keysIn_default = keysIn;

// node_modules/lodash-es/toPlainObject.js
function toPlainObject(value) {
  return copyObject_default(value, keysIn_default(value));
}
var toPlainObject_default = toPlainObject;

// node_modules/lodash-es/_baseMergeDeep.js
function baseMergeDeep(object, source, key, srcIndex, mergeFunc, customizer, stack) {
  var objValue = safeGet_default(object, key), srcValue = safeGet_default(source, key), stacked = stack.get(srcValue);
  if (stacked) {
    assignMergeValue_default(object, key, stacked);
    return;
  }
  var newValue = customizer ? customizer(objValue, srcValue, key + "", object, source, stack) : void 0;
  var isCommon = newValue === void 0;
  if (isCommon) {
    var isArr = isArray_default(srcValue), isBuff = !isArr && isBuffer_default(srcValue), isTyped = !isArr && !isBuff && isTypedArray_default(srcValue);
    newValue = srcValue;
    if (isArr || isBuff || isTyped) {
      if (isArray_default(objValue)) {
        newValue = objValue;
      } else if (isArrayLikeObject_default(objValue)) {
        newValue = copyArray_default(objValue);
      } else if (isBuff) {
        isCommon = false;
        newValue = cloneBuffer_default(srcValue, true);
      } else if (isTyped) {
        isCommon = false;
        newValue = cloneTypedArray_default(srcValue, true);
      } else {
        newValue = [];
      }
    } else if (isPlainObject_default(srcValue) || isArguments_default(srcValue)) {
      newValue = objValue;
      if (isArguments_default(objValue)) {
        newValue = toPlainObject_default(objValue);
      } else if (!isObject_default(objValue) || isFunction_default(objValue)) {
        newValue = initCloneObject_default(srcValue);
      }
    } else {
      isCommon = false;
    }
  }
  if (isCommon) {
    stack.set(srcValue, newValue);
    mergeFunc(newValue, srcValue, srcIndex, customizer, stack);
    stack["delete"](srcValue);
  }
  assignMergeValue_default(object, key, newValue);
}
var baseMergeDeep_default = baseMergeDeep;

// node_modules/lodash-es/_baseMerge.js
function baseMerge(object, source, srcIndex, customizer, stack) {
  if (object === source) {
    return;
  }
  baseFor_default(source, function(srcValue, key) {
    stack || (stack = new Stack_default());
    if (isObject_default(srcValue)) {
      baseMergeDeep_default(object, source, key, srcIndex, baseMerge, customizer, stack);
    } else {
      var newValue = customizer ? customizer(safeGet_default(object, key), srcValue, key + "", object, source, stack) : void 0;
      if (newValue === void 0) {
        newValue = srcValue;
      }
      assignMergeValue_default(object, key, newValue);
    }
  }, keysIn_default);
}
var baseMerge_default = baseMerge;

// node_modules/lodash-es/_apply.js
function apply(func, thisArg, args) {
  switch (args.length) {
    case 0:
      return func.call(thisArg);
    case 1:
      return func.call(thisArg, args[0]);
    case 2:
      return func.call(thisArg, args[0], args[1]);
    case 3:
      return func.call(thisArg, args[0], args[1], args[2]);
  }
  return func.apply(thisArg, args);
}
var apply_default = apply;

// node_modules/lodash-es/_overRest.js
var nativeMax = Math.max;
function overRest(func, start, transform2) {
  start = nativeMax(start === void 0 ? func.length - 1 : start, 0);
  return function() {
    var args = arguments, index = -1, length = nativeMax(args.length - start, 0), array = Array(length);
    while (++index < length) {
      array[index] = args[start + index];
    }
    index = -1;
    var otherArgs = Array(start + 1);
    while (++index < start) {
      otherArgs[index] = args[index];
    }
    otherArgs[start] = transform2(array);
    return apply_default(func, this, otherArgs);
  };
}
var overRest_default = overRest;

// node_modules/lodash-es/constant.js
function constant(value) {
  return function() {
    return value;
  };
}
var constant_default = constant;

// node_modules/lodash-es/_baseSetToString.js
var baseSetToString = !defineProperty_default ? identity_default : function(func, string) {
  return defineProperty_default(func, "toString", {
    "configurable": true,
    "enumerable": false,
    "value": constant_default(string),
    "writable": true
  });
};
var baseSetToString_default = baseSetToString;

// node_modules/lodash-es/_shortOut.js
var HOT_COUNT = 800;
var HOT_SPAN = 16;
var nativeNow = Date.now;
function shortOut(func) {
  var count = 0, lastCalled = 0;
  return function() {
    var stamp = nativeNow(), remaining = HOT_SPAN - (stamp - lastCalled);
    lastCalled = stamp;
    if (remaining > 0) {
      if (++count >= HOT_COUNT) {
        return arguments[0];
      }
    } else {
      count = 0;
    }
    return func.apply(void 0, arguments);
  };
}
var shortOut_default = shortOut;

// node_modules/lodash-es/_setToString.js
var setToString = shortOut_default(baseSetToString_default);
var setToString_default = setToString;

// node_modules/lodash-es/_baseRest.js
function baseRest(func, start) {
  return setToString_default(overRest_default(func, start, identity_default), func + "");
}
var baseRest_default = baseRest;

// node_modules/lodash-es/_isIterateeCall.js
function isIterateeCall(value, index, object) {
  if (!isObject_default(object)) {
    return false;
  }
  var type = typeof index;
  if (type == "number" ? isArrayLike_default(object) && isIndex_default(index, object.length) : type == "string" && index in object) {
    return eq_default(object[index], value);
  }
  return false;
}
var isIterateeCall_default = isIterateeCall;

// node_modules/lodash-es/_createAssigner.js
function createAssigner(assigner) {
  return baseRest_default(function(object, sources) {
    var index = -1, length = sources.length, customizer = length > 1 ? sources[length - 1] : void 0, guard = length > 2 ? sources[2] : void 0;
    customizer = assigner.length > 3 && typeof customizer == "function" ? (length--, customizer) : void 0;
    if (guard && isIterateeCall_default(sources[0], sources[1], guard)) {
      customizer = length < 3 ? void 0 : customizer;
      length = 1;
    }
    object = Object(object);
    while (++index < length) {
      var source = sources[index];
      if (source) {
        assigner(object, source, index, customizer);
      }
    }
    return object;
  });
}
var createAssigner_default = createAssigner;

// node_modules/lodash-es/merge.js
var merge = createAssigner_default(function(object, source, srcIndex) {
  baseMerge_default(object, source, srcIndex);
});
var merge_default = merge;

// node_modules/lodash-es/_isFlattenable.js
var spreadableSymbol = Symbol_default ? Symbol_default.isConcatSpreadable : void 0;
function isFlattenable(value) {
  return isArray_default(value) || isArguments_default(value) || !!(spreadableSymbol && value && value[spreadableSymbol]);
}
var isFlattenable_default = isFlattenable;

// node_modules/lodash-es/_baseFlatten.js
function baseFlatten(array, depth, predicate, isStrict, result) {
  var index = -1, length = array.length;
  predicate || (predicate = isFlattenable_default);
  result || (result = []);
  while (++index < length) {
    var value = array[index];
    if (depth > 0 && predicate(value)) {
      if (depth > 1) {
        baseFlatten(value, depth - 1, predicate, isStrict, result);
      } else {
        arrayPush_default(result, value);
      }
    } else if (!isStrict) {
      result[result.length] = value;
    }
  }
  return result;
}
var baseFlatten_default = baseFlatten;

// node_modules/lodash-es/flattenDeep.js
var INFINITY4 = 1 / 0;
function flattenDeep(array) {
  var length = array == null ? 0 : array.length;
  return length ? baseFlatten_default(array, INFINITY4) : [];
}
var flattenDeep_default = flattenDeep;

// node_modules/lodash-es/_baseFindIndex.js
function baseFindIndex(array, predicate, fromIndex, fromRight) {
  var length = array.length, index = fromIndex + (fromRight ? 1 : -1);
  while (fromRight ? index-- : ++index < length) {
    if (predicate(array[index], index, array)) {
      return index;
    }
  }
  return -1;
}
var baseFindIndex_default = baseFindIndex;

// node_modules/lodash-es/_baseIsNaN.js
function baseIsNaN(value) {
  return value !== value;
}
var baseIsNaN_default = baseIsNaN;

// node_modules/lodash-es/_strictIndexOf.js
function strictIndexOf(array, value, fromIndex) {
  var index = fromIndex - 1, length = array.length;
  while (++index < length) {
    if (array[index] === value) {
      return index;
    }
  }
  return -1;
}
var strictIndexOf_default = strictIndexOf;

// node_modules/lodash-es/_baseIndexOf.js
function baseIndexOf(array, value, fromIndex) {
  return value === value ? strictIndexOf_default(array, value, fromIndex) : baseFindIndex_default(array, baseIsNaN_default, fromIndex);
}
var baseIndexOf_default = baseIndexOf;

// node_modules/lodash-es/_arrayIncludes.js
function arrayIncludes(array, value) {
  var length = array == null ? 0 : array.length;
  return !!length && baseIndexOf_default(array, value, 0) > -1;
}
var arrayIncludes_default = arrayIncludes;

// node_modules/lodash-es/_arrayIncludesWith.js
function arrayIncludesWith(array, value, comparator) {
  var index = -1, length = array == null ? 0 : array.length;
  while (++index < length) {
    if (comparator(value, array[index])) {
      return true;
    }
  }
  return false;
}
var arrayIncludesWith_default = arrayIncludesWith;

// node_modules/lodash-es/noop.js
function noop() {
}
var noop_default = noop;

// node_modules/lodash-es/_createSet.js
var INFINITY5 = 1 / 0;
var createSet = !(Set_default && 1 / setToArray_default(new Set_default([, -0]))[1] == INFINITY5) ? noop_default : function(values) {
  return new Set_default(values);
};
var createSet_default = createSet;

// node_modules/lodash-es/_baseUniq.js
var LARGE_ARRAY_SIZE2 = 200;
function baseUniq(array, iteratee, comparator) {
  var index = -1, includes = arrayIncludes_default, length = array.length, isCommon = true, result = [], seen = result;
  if (comparator) {
    isCommon = false;
    includes = arrayIncludesWith_default;
  } else if (length >= LARGE_ARRAY_SIZE2) {
    var set2 = iteratee ? null : createSet_default(array);
    if (set2) {
      return setToArray_default(set2);
    }
    isCommon = false;
    includes = cacheHas_default;
    seen = new SetCache_default();
  } else {
    seen = iteratee ? [] : result;
  }
  outer:
    while (++index < length) {
      var value = array[index], computed = iteratee ? iteratee(value) : value;
      value = comparator || value !== 0 ? value : 0;
      if (isCommon && computed === computed) {
        var seenIndex = seen.length;
        while (seenIndex--) {
          if (seen[seenIndex] === computed) {
            continue outer;
          }
        }
        if (iteratee) {
          seen.push(computed);
        }
        result.push(value);
      } else if (!includes(seen, computed, comparator)) {
        if (seen !== result) {
          seen.push(computed);
        }
        result.push(value);
      }
    }
  return result;
}
var baseUniq_default = baseUniq;

// node_modules/lodash-es/uniq.js
function uniq(array) {
  return array && array.length ? baseUniq_default(array) : [];
}
var uniq_default = uniq;

// node_modules/@rjsf/utils/lib/schema/retrieveSchema.js
var import_json_schema_merge_allof = __toESM(require_src2(), 1);

// node_modules/@rjsf/utils/lib/findSchemaDefinition.js
var import_jsonpointer = __toESM(require_jsonpointer(), 1);

// node_modules/lodash-es/_baseAssign.js
function baseAssign(object, source) {
  return object && copyObject_default(source, keys_default(source), object);
}
var baseAssign_default = baseAssign;

// node_modules/lodash-es/_baseAssignIn.js
function baseAssignIn(object, source) {
  return object && copyObject_default(source, keysIn_default(source), object);
}
var baseAssignIn_default = baseAssignIn;

// node_modules/lodash-es/_copySymbols.js
function copySymbols(source, object) {
  return copyObject_default(source, getSymbols_default(source), object);
}
var copySymbols_default = copySymbols;

// node_modules/lodash-es/_getSymbolsIn.js
var nativeGetSymbols2 = Object.getOwnPropertySymbols;
var getSymbolsIn = !nativeGetSymbols2 ? stubArray_default : function(object) {
  var result = [];
  while (object) {
    arrayPush_default(result, getSymbols_default(object));
    object = getPrototype_default(object);
  }
  return result;
};
var getSymbolsIn_default = getSymbolsIn;

// node_modules/lodash-es/_copySymbolsIn.js
function copySymbolsIn(source, object) {
  return copyObject_default(source, getSymbolsIn_default(source), object);
}
var copySymbolsIn_default = copySymbolsIn;

// node_modules/lodash-es/_getAllKeysIn.js
function getAllKeysIn(object) {
  return baseGetAllKeys_default(object, keysIn_default, getSymbolsIn_default);
}
var getAllKeysIn_default = getAllKeysIn;

// node_modules/lodash-es/_initCloneArray.js
var objectProto18 = Object.prototype;
var hasOwnProperty15 = objectProto18.hasOwnProperty;
function initCloneArray(array) {
  var length = array.length, result = new array.constructor(length);
  if (length && typeof array[0] == "string" && hasOwnProperty15.call(array, "index")) {
    result.index = array.index;
    result.input = array.input;
  }
  return result;
}
var initCloneArray_default = initCloneArray;

// node_modules/lodash-es/_cloneDataView.js
function cloneDataView(dataView, isDeep) {
  var buffer = isDeep ? cloneArrayBuffer_default(dataView.buffer) : dataView.buffer;
  return new dataView.constructor(buffer, dataView.byteOffset, dataView.byteLength);
}
var cloneDataView_default = cloneDataView;

// node_modules/lodash-es/_cloneRegExp.js
var reFlags = /\w*$/;
function cloneRegExp(regexp) {
  var result = new regexp.constructor(regexp.source, reFlags.exec(regexp));
  result.lastIndex = regexp.lastIndex;
  return result;
}
var cloneRegExp_default = cloneRegExp;

// node_modules/lodash-es/_cloneSymbol.js
var symbolProto3 = Symbol_default ? Symbol_default.prototype : void 0;
var symbolValueOf2 = symbolProto3 ? symbolProto3.valueOf : void 0;
function cloneSymbol(symbol) {
  return symbolValueOf2 ? Object(symbolValueOf2.call(symbol)) : {};
}
var cloneSymbol_default = cloneSymbol;

// node_modules/lodash-es/_initCloneByTag.js
var boolTag3 = "[object Boolean]";
var dateTag3 = "[object Date]";
var mapTag5 = "[object Map]";
var numberTag3 = "[object Number]";
var regexpTag3 = "[object RegExp]";
var setTag5 = "[object Set]";
var stringTag3 = "[object String]";
var symbolTag3 = "[object Symbol]";
var arrayBufferTag3 = "[object ArrayBuffer]";
var dataViewTag4 = "[object DataView]";
var float32Tag2 = "[object Float32Array]";
var float64Tag2 = "[object Float64Array]";
var int8Tag2 = "[object Int8Array]";
var int16Tag2 = "[object Int16Array]";
var int32Tag2 = "[object Int32Array]";
var uint8Tag2 = "[object Uint8Array]";
var uint8ClampedTag2 = "[object Uint8ClampedArray]";
var uint16Tag2 = "[object Uint16Array]";
var uint32Tag2 = "[object Uint32Array]";
function initCloneByTag(object, tag, isDeep) {
  var Ctor = object.constructor;
  switch (tag) {
    case arrayBufferTag3:
      return cloneArrayBuffer_default(object);
    case boolTag3:
    case dateTag3:
      return new Ctor(+object);
    case dataViewTag4:
      return cloneDataView_default(object, isDeep);
    case float32Tag2:
    case float64Tag2:
    case int8Tag2:
    case int16Tag2:
    case int32Tag2:
    case uint8Tag2:
    case uint8ClampedTag2:
    case uint16Tag2:
    case uint32Tag2:
      return cloneTypedArray_default(object, isDeep);
    case mapTag5:
      return new Ctor();
    case numberTag3:
    case stringTag3:
      return new Ctor(object);
    case regexpTag3:
      return cloneRegExp_default(object);
    case setTag5:
      return new Ctor();
    case symbolTag3:
      return cloneSymbol_default(object);
  }
}
var initCloneByTag_default = initCloneByTag;

// node_modules/lodash-es/_baseIsMap.js
var mapTag6 = "[object Map]";
function baseIsMap(value) {
  return isObjectLike_default(value) && getTag_default(value) == mapTag6;
}
var baseIsMap_default = baseIsMap;

// node_modules/lodash-es/isMap.js
var nodeIsMap = nodeUtil_default && nodeUtil_default.isMap;
var isMap = nodeIsMap ? baseUnary_default(nodeIsMap) : baseIsMap_default;
var isMap_default = isMap;

// node_modules/lodash-es/_baseIsSet.js
var setTag6 = "[object Set]";
function baseIsSet(value) {
  return isObjectLike_default(value) && getTag_default(value) == setTag6;
}
var baseIsSet_default = baseIsSet;

// node_modules/lodash-es/isSet.js
var nodeIsSet = nodeUtil_default && nodeUtil_default.isSet;
var isSet = nodeIsSet ? baseUnary_default(nodeIsSet) : baseIsSet_default;
var isSet_default = isSet;

// node_modules/lodash-es/_baseClone.js
var CLONE_DEEP_FLAG = 1;
var CLONE_FLAT_FLAG = 2;
var CLONE_SYMBOLS_FLAG = 4;
var argsTag4 = "[object Arguments]";
var arrayTag3 = "[object Array]";
var boolTag4 = "[object Boolean]";
var dateTag4 = "[object Date]";
var errorTag3 = "[object Error]";
var funcTag3 = "[object Function]";
var genTag2 = "[object GeneratorFunction]";
var mapTag7 = "[object Map]";
var numberTag4 = "[object Number]";
var objectTag5 = "[object Object]";
var regexpTag4 = "[object RegExp]";
var setTag7 = "[object Set]";
var stringTag4 = "[object String]";
var symbolTag4 = "[object Symbol]";
var weakMapTag3 = "[object WeakMap]";
var arrayBufferTag4 = "[object ArrayBuffer]";
var dataViewTag5 = "[object DataView]";
var float32Tag3 = "[object Float32Array]";
var float64Tag3 = "[object Float64Array]";
var int8Tag3 = "[object Int8Array]";
var int16Tag3 = "[object Int16Array]";
var int32Tag3 = "[object Int32Array]";
var uint8Tag3 = "[object Uint8Array]";
var uint8ClampedTag3 = "[object Uint8ClampedArray]";
var uint16Tag3 = "[object Uint16Array]";
var uint32Tag3 = "[object Uint32Array]";
var cloneableTags = {};
cloneableTags[argsTag4] = cloneableTags[arrayTag3] = cloneableTags[arrayBufferTag4] = cloneableTags[dataViewTag5] = cloneableTags[boolTag4] = cloneableTags[dateTag4] = cloneableTags[float32Tag3] = cloneableTags[float64Tag3] = cloneableTags[int8Tag3] = cloneableTags[int16Tag3] = cloneableTags[int32Tag3] = cloneableTags[mapTag7] = cloneableTags[numberTag4] = cloneableTags[objectTag5] = cloneableTags[regexpTag4] = cloneableTags[setTag7] = cloneableTags[stringTag4] = cloneableTags[symbolTag4] = cloneableTags[uint8Tag3] = cloneableTags[uint8ClampedTag3] = cloneableTags[uint16Tag3] = cloneableTags[uint32Tag3] = true;
cloneableTags[errorTag3] = cloneableTags[funcTag3] = cloneableTags[weakMapTag3] = false;
function baseClone(value, bitmask, customizer, key, object, stack) {
  var result, isDeep = bitmask & CLONE_DEEP_FLAG, isFlat = bitmask & CLONE_FLAT_FLAG, isFull = bitmask & CLONE_SYMBOLS_FLAG;
  if (customizer) {
    result = object ? customizer(value, key, object, stack) : customizer(value);
  }
  if (result !== void 0) {
    return result;
  }
  if (!isObject_default(value)) {
    return value;
  }
  var isArr = isArray_default(value);
  if (isArr) {
    result = initCloneArray_default(value);
    if (!isDeep) {
      return copyArray_default(value, result);
    }
  } else {
    var tag = getTag_default(value), isFunc = tag == funcTag3 || tag == genTag2;
    if (isBuffer_default(value)) {
      return cloneBuffer_default(value, isDeep);
    }
    if (tag == objectTag5 || tag == argsTag4 || isFunc && !object) {
      result = isFlat || isFunc ? {} : initCloneObject_default(value);
      if (!isDeep) {
        return isFlat ? copySymbolsIn_default(value, baseAssignIn_default(result, value)) : copySymbols_default(value, baseAssign_default(result, value));
      }
    } else {
      if (!cloneableTags[tag]) {
        return object ? value : {};
      }
      result = initCloneByTag_default(value, tag, isDeep);
    }
  }
  stack || (stack = new Stack_default());
  var stacked = stack.get(value);
  if (stacked) {
    return stacked;
  }
  stack.set(value, result);
  if (isSet_default(value)) {
    value.forEach(function(subValue) {
      result.add(baseClone(subValue, bitmask, customizer, subValue, value, stack));
    });
  } else if (isMap_default(value)) {
    value.forEach(function(subValue, key2) {
      result.set(key2, baseClone(subValue, bitmask, customizer, key2, value, stack));
    });
  }
  var keysFunc = isFull ? isFlat ? getAllKeysIn_default : getAllKeys_default : isFlat ? keysIn_default : keys_default;
  var props = isArr ? void 0 : keysFunc(value);
  arrayEach_default(props || value, function(subValue, key2) {
    if (props) {
      key2 = subValue;
      subValue = value[key2];
    }
    assignValue_default(result, key2, baseClone(subValue, bitmask, customizer, key2, value, stack));
  });
  return result;
}
var baseClone_default = baseClone;

// node_modules/lodash-es/last.js
function last(array) {
  var length = array == null ? 0 : array.length;
  return length ? array[length - 1] : void 0;
}
var last_default = last;

// node_modules/lodash-es/_baseSlice.js
function baseSlice(array, start, end) {
  var index = -1, length = array.length;
  if (start < 0) {
    start = -start > length ? 0 : length + start;
  }
  end = end > length ? length : end;
  if (end < 0) {
    end += length;
  }
  length = start > end ? 0 : end - start >>> 0;
  start >>>= 0;
  var result = Array(length);
  while (++index < length) {
    result[index] = array[index + start];
  }
  return result;
}
var baseSlice_default = baseSlice;

// node_modules/lodash-es/_parent.js
function parent(object, path) {
  return path.length < 2 ? object : baseGet_default(object, baseSlice_default(path, 0, -1));
}
var parent_default = parent;

// node_modules/lodash-es/_baseUnset.js
function baseUnset(object, path) {
  path = castPath_default(path, object);
  object = parent_default(object, path);
  return object == null || delete object[toKey_default(last_default(path))];
}
var baseUnset_default = baseUnset;

// node_modules/lodash-es/_customOmitClone.js
function customOmitClone(value) {
  return isPlainObject_default(value) ? void 0 : value;
}
var customOmitClone_default = customOmitClone;

// node_modules/lodash-es/flatten.js
function flatten(array) {
  var length = array == null ? 0 : array.length;
  return length ? baseFlatten_default(array, 1) : [];
}
var flatten_default = flatten;

// node_modules/lodash-es/_flatRest.js
function flatRest(func) {
  return setToString_default(overRest_default(func, void 0, flatten_default), func + "");
}
var flatRest_default = flatRest;

// node_modules/lodash-es/omit.js
var CLONE_DEEP_FLAG2 = 1;
var CLONE_FLAT_FLAG2 = 2;
var CLONE_SYMBOLS_FLAG2 = 4;
var omit = flatRest_default(function(object, paths) {
  var result = {};
  if (object == null) {
    return result;
  }
  var isDeep = false;
  paths = arrayMap_default(paths, function(path) {
    path = castPath_default(path, object);
    isDeep || (isDeep = path.length > 1);
    return path;
  });
  copyObject_default(object, getAllKeysIn_default(object), result);
  if (isDeep) {
    result = baseClone_default(result, CLONE_DEEP_FLAG2 | CLONE_FLAT_FLAG2 | CLONE_SYMBOLS_FLAG2, customOmitClone_default);
  }
  var length = paths.length;
  while (length--) {
    baseUnset_default(result, paths[length]);
  }
  return result;
});
var omit_default = omit;

// node_modules/@rjsf/utils/lib/findSchemaDefinition.js
var import_fast_uri = __toESM(require_fast_uri(), 1);
function findEmbeddedSchemaRecursive(schema, ref) {
  if (ID_KEY in schema && import_fast_uri.default.equal(schema[ID_KEY], ref)) {
    return schema;
  }
  for (const subSchema of Object.values(schema)) {
    if (isObject_default(subSchema)) {
      const result = findEmbeddedSchemaRecursive(subSchema, ref);
      if (result !== void 0) {
        return result;
      }
    }
  }
  return void 0;
}
function splitKeyElementFromObject(key, object) {
  const value = object[key];
  const remaining = omit_default(object, [key]);
  return [remaining, value];
}
function findSchemaDefinitionRecursive($ref, rootSchema = {}, recurseList = [], baseURI = get_default(rootSchema, [ID_KEY])) {
  const ref = $ref || "";
  let current = void 0;
  if (ref.startsWith("#")) {
    const decodedRef = decodeURIComponent(ref.substring(1));
    if (baseURI === void 0 || ID_KEY in rootSchema && rootSchema[ID_KEY] === baseURI) {
      current = import_jsonpointer.default.get(rootSchema, decodedRef);
    } else if (rootSchema[SCHEMA_KEY] === JSON_SCHEMA_DRAFT_2020_12) {
      current = findEmbeddedSchemaRecursive(rootSchema, baseURI.replace(/\/$/, ""));
      if (current !== void 0) {
        current = import_jsonpointer.default.get(current, decodedRef);
      }
    }
  } else if (rootSchema[SCHEMA_KEY] === JSON_SCHEMA_DRAFT_2020_12) {
    const resolvedRef = baseURI ? import_fast_uri.default.resolve(baseURI, ref) : ref;
    const [refId, ...refAnchor] = resolvedRef.replace(/#\/?$/, "").split("#");
    current = findEmbeddedSchemaRecursive(rootSchema, refId.replace(/\/$/, ""));
    if (current !== void 0) {
      baseURI = current[ID_KEY];
      if (!isEmpty_default(refAnchor)) {
        current = import_jsonpointer.default.get(current, decodeURIComponent(refAnchor.join("#")));
      }
    }
  }
  if (current === void 0) {
    throw new Error(`Could not find a definition for ${$ref}.`);
  }
  const nextRef = current[REF_KEY];
  if (nextRef) {
    if (recurseList.includes(nextRef)) {
      if (recurseList.length === 1) {
        throw new Error(`Definition for ${$ref} is a circular reference`);
      }
      const [firstRef, ...restRefs] = recurseList;
      const circularPath = [...restRefs, ref, firstRef].join(" -> ");
      throw new Error(`Definition for ${firstRef} contains a circular reference through ${circularPath}`);
    }
    const [remaining, theRef] = splitKeyElementFromObject(REF_KEY, current);
    const subSchema = findSchemaDefinitionRecursive(theRef, rootSchema, [...recurseList, ref], baseURI);
    if (Object.keys(remaining).length > 0) {
      return { ...remaining, ...subSchema };
    }
    return subSchema;
  }
  return current;
}
function findSchemaDefinition($ref, rootSchema = {}, baseURI = get_default(rootSchema, [ID_KEY])) {
  const recurseList = [];
  return findSchemaDefinitionRecursive($ref, rootSchema, recurseList, baseURI);
}

// node_modules/lodash-es/isString.js
var stringTag5 = "[object String]";
function isString(value) {
  return typeof value == "string" || !isArray_default(value) && isObjectLike_default(value) && baseGetTag_default(value) == stringTag5;
}
var isString_default = isString;

// node_modules/@rjsf/utils/lib/getDiscriminatorFieldFromSchema.js
function getDiscriminatorFieldFromSchema(schema) {
  let discriminator;
  const maybeString = get_default(schema, DISCRIMINATOR_PATH);
  if (isString_default(maybeString)) {
    discriminator = maybeString;
  } else if (maybeString !== void 0) {
    console.warn(`Expecting discriminator to be a string, got "${typeof maybeString}" instead`);
  }
  return discriminator;
}

// node_modules/@rjsf/utils/lib/guessType.js
function guessType(value) {
  if (Array.isArray(value)) {
    return "array";
  }
  if (typeof value === "string") {
    return "string";
  }
  if (value == null) {
    return "null";
  }
  if (typeof value === "boolean") {
    return "boolean";
  }
  if (!isNaN(value)) {
    return "number";
  }
  if (typeof value === "object") {
    return "object";
  }
  return "string";
}

// node_modules/lodash-es/union.js
var union = baseRest_default(function(arrays) {
  return baseUniq_default(baseFlatten_default(arrays, 1, isArrayLikeObject_default, true));
});
var union_default = union;

// node_modules/@rjsf/utils/lib/getSchemaType.js
function getSchemaType(schema) {
  let { type } = schema;
  if (!type && schema.const) {
    return guessType(schema.const);
  }
  if (!type && schema.enum) {
    return "string";
  }
  if (!type && (schema.properties || schema.additionalProperties || schema.patternProperties)) {
    return "object";
  }
  if (Array.isArray(type)) {
    if (type.length === 2 && type.includes("null")) {
      type = type.find((type2) => type2 !== "null");
    } else {
      type = type[0];
    }
  }
  return type;
}

// node_modules/@rjsf/utils/lib/mergeSchemas.js
function mergeSchemas(obj1, obj2) {
  const acc = Object.assign({}, obj1);
  return Object.keys(obj2).reduce((acc2, key) => {
    const left = obj1 ? obj1[key] : {}, right = obj2[key];
    if (obj1 && key in obj1 && isObject(right)) {
      acc2[key] = mergeSchemas(left, right);
    } else if (obj1 && obj2 && (getSchemaType(obj1) === "object" || getSchemaType(obj2) === "object") && key === REQUIRED_KEY && Array.isArray(left) && Array.isArray(right)) {
      acc2[key] = union_default(left, right);
    } else {
      acc2[key] = right;
    }
    return acc2;
  }, acc);
}

// node_modules/lodash-es/isNumber.js
var numberTag5 = "[object Number]";
function isNumber(value) {
  return typeof value == "number" || isObjectLike_default(value) && baseGetTag_default(value) == numberTag5;
}
var isNumber_default = isNumber;

// node_modules/@rjsf/utils/lib/getOptionMatchingSimpleDiscriminator.js
function getOptionMatchingSimpleDiscriminator(formData, options, discriminatorField) {
  var _a;
  if (formData && discriminatorField) {
    const value = get_default(formData, discriminatorField);
    if (value === void 0) {
      return;
    }
    for (let i = 0; i < options.length; i++) {
      const option = options[i];
      const discriminator = get_default(option, [PROPERTIES_KEY, discriminatorField], {});
      if (discriminator.type === "object" || discriminator.type === "array") {
        continue;
      }
      if (discriminator.const === value) {
        return i;
      }
      if ((_a = discriminator.enum) === null || _a === void 0 ? void 0 : _a.includes(value)) {
        return i;
      }
    }
  }
  return;
}

// node_modules/@rjsf/utils/lib/schema/getFirstMatchingOption.js
function getFirstMatchingOption(validator, formData, options, rootSchema, discriminatorField) {
  if (formData === void 0) {
    return 0;
  }
  const simpleDiscriminatorMatch = getOptionMatchingSimpleDiscriminator(formData, options, discriminatorField);
  if (isNumber_default(simpleDiscriminatorMatch)) {
    return simpleDiscriminatorMatch;
  }
  for (let i = 0; i < options.length; i++) {
    const option = options[i];
    if (discriminatorField && has_default(option, [PROPERTIES_KEY, discriminatorField])) {
      const value = get_default(formData, discriminatorField);
      const discriminator = get_default(option, [PROPERTIES_KEY, discriminatorField], {});
      if (validator.isValid(discriminator, value, rootSchema)) {
        return i;
      }
    } else if (option[PROPERTIES_KEY]) {
      const requiresAnyOf = {
        anyOf: Object.keys(option[PROPERTIES_KEY]).map((key) => ({
          required: [key]
        }))
      };
      let augmentedSchema;
      if (option.anyOf) {
        const { ...shallowClone } = option;
        if (!shallowClone.allOf) {
          shallowClone.allOf = [];
        } else {
          shallowClone.allOf = shallowClone.allOf.slice();
        }
        shallowClone.allOf.push(requiresAnyOf);
        augmentedSchema = shallowClone;
      } else {
        augmentedSchema = Object.assign({}, option, requiresAnyOf);
      }
      delete augmentedSchema.required;
      if (validator.isValid(augmentedSchema, formData, rootSchema)) {
        return i;
      }
    } else if (validator.isValid(option, formData, rootSchema)) {
      return i;
    }
  }
  return 0;
}

// node_modules/@rjsf/utils/lib/schema/retrieveSchema.js
function retrieveSchema(validator, schema, rootSchema = {}, rawFormData, experimental_customMergeAllOf) {
  return retrieveSchemaInternal(validator, schema, rootSchema, rawFormData, void 0, void 0, experimental_customMergeAllOf)[0];
}
function resolveCondition(validator, schema, rootSchema, expandAllBranches, recurseList, formData, experimental_customMergeAllOf) {
  const { if: expression, then, else: otherwise, ...resolvedSchemaLessConditional } = schema;
  const conditionValue = validator.isValid(expression, formData || {}, rootSchema);
  let resolvedSchemas = [resolvedSchemaLessConditional];
  let schemas = [];
  if (expandAllBranches) {
    if (then && typeof then !== "boolean") {
      schemas = schemas.concat(retrieveSchemaInternal(validator, then, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf));
    }
    if (otherwise && typeof otherwise !== "boolean") {
      schemas = schemas.concat(retrieveSchemaInternal(validator, otherwise, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf));
    }
  } else {
    const conditionalSchema = conditionValue ? then : otherwise;
    if (conditionalSchema && typeof conditionalSchema !== "boolean") {
      schemas = schemas.concat(retrieveSchemaInternal(validator, conditionalSchema, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf));
    }
  }
  if (schemas.length) {
    resolvedSchemas = schemas.map((s) => mergeSchemas(resolvedSchemaLessConditional, s));
  }
  return resolvedSchemas.flatMap((s) => retrieveSchemaInternal(validator, s, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf));
}
function getAllPermutationsOfXxxOf(listOfLists) {
  const allPermutations = listOfLists.reduce((permutations, list) => {
    if (list.length > 1) {
      return list.flatMap((element) => times_default(permutations.length, (i) => [...permutations[i]].concat(element)));
    }
    permutations.forEach((permutation) => permutation.push(list[0]));
    return permutations;
  }, [[]]);
  return allPermutations;
}
function getMatchingPatternProperties(schema, key) {
  return Object.keys(schema.patternProperties).filter((pattern) => RegExp(pattern).test(key)).reduce((obj, pattern) => {
    set_default(obj, [pattern], schema.patternProperties[pattern]);
    return obj;
  }, {});
}
function resolveSchema(validator, schema, rootSchema, expandAllBranches, recurseList, formData, experimental_customMergeAllOf) {
  const updatedSchemas = resolveReference(validator, schema, rootSchema, expandAllBranches, recurseList, formData);
  if (updatedSchemas.length > 1 || updatedSchemas[0] !== schema) {
    return updatedSchemas;
  }
  if (DEPENDENCIES_KEY in schema) {
    const resolvedSchemas = resolveDependencies(validator, schema, rootSchema, expandAllBranches, recurseList, formData);
    return resolvedSchemas.flatMap((s) => {
      return retrieveSchemaInternal(validator, s, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf);
    });
  }
  if (ALL_OF_KEY in schema && Array.isArray(schema.allOf)) {
    const allOfSchemaElements = schema.allOf.map((allOfSubschema) => retrieveSchemaInternal(validator, allOfSubschema, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf));
    const allPermutations = getAllPermutationsOfXxxOf(allOfSchemaElements);
    return allPermutations.map((permutation) => ({
      ...schema,
      allOf: permutation
    }));
  }
  return [schema];
}
function resolveReference(validator, schema, rootSchema, expandAllBranches, recurseList, formData, experimental_customMergeAllOf) {
  const updatedSchema = resolveAllReferences(schema, rootSchema, recurseList);
  if (updatedSchema !== schema) {
    return retrieveSchemaInternal(validator, updatedSchema, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf);
  }
  return [schema];
}
function resolveAllReferences(schema, rootSchema, recurseList, baseURI) {
  if (!isObject(schema)) {
    return schema;
  }
  let resolvedSchema = schema;
  if (REF_KEY in resolvedSchema) {
    const { $ref, ...localSchema } = resolvedSchema;
    if (recurseList.includes($ref)) {
      return resolvedSchema;
    }
    recurseList.push($ref);
    const refSchema = findSchemaDefinition($ref, rootSchema, baseURI);
    resolvedSchema = { ...refSchema, ...localSchema };
    if (ID_KEY in resolvedSchema) {
      baseURI = resolvedSchema[ID_KEY];
    }
  }
  if (PROPERTIES_KEY in resolvedSchema) {
    const childrenLists = [];
    const updatedProps = transform_default(resolvedSchema[PROPERTIES_KEY], (result, value, key) => {
      const childList = [...recurseList];
      result[key] = resolveAllReferences(value, rootSchema, childList, baseURI);
      childrenLists.push(childList);
    }, {});
    merge_default(recurseList, uniq_default(flattenDeep_default(childrenLists)));
    resolvedSchema = { ...resolvedSchema, [PROPERTIES_KEY]: updatedProps };
  }
  if (ITEMS_KEY in resolvedSchema && !Array.isArray(resolvedSchema.items) && typeof resolvedSchema.items !== "boolean") {
    resolvedSchema = {
      ...resolvedSchema,
      items: resolveAllReferences(resolvedSchema.items, rootSchema, recurseList, baseURI)
    };
  }
  return deepEquals(schema, resolvedSchema) ? schema : resolvedSchema;
}
function stubExistingAdditionalProperties(validator, theSchema, rootSchema, aFormData, experimental_customMergeAllOf) {
  const schema = {
    ...theSchema,
    properties: { ...theSchema.properties }
  };
  const formData = aFormData && isObject(aFormData) ? aFormData : {};
  Object.keys(formData).forEach((key) => {
    if (key in schema.properties) {
      return;
    }
    if (PATTERN_PROPERTIES_KEY in schema) {
      const matchingProperties = getMatchingPatternProperties(schema, key);
      if (!isEmpty_default(matchingProperties)) {
        schema.properties[key] = retrieveSchema(validator, { allOf: Object.values(matchingProperties) }, rootSchema, get_default(formData, [key]), experimental_customMergeAllOf);
        set_default(schema.properties, [key, ADDITIONAL_PROPERTY_FLAG], true);
        return;
      }
    }
    if (ADDITIONAL_PROPERTIES_KEY in schema && schema.additionalProperties !== false) {
      let additionalProperties = {};
      if (typeof schema.additionalProperties !== "boolean") {
        if (REF_KEY in schema.additionalProperties) {
          additionalProperties = retrieveSchema(validator, { $ref: get_default(schema.additionalProperties, [REF_KEY]) }, rootSchema, formData, experimental_customMergeAllOf);
        } else if ("type" in schema.additionalProperties) {
          additionalProperties = { ...schema.additionalProperties };
        } else if (ANY_OF_KEY in schema.additionalProperties || ONE_OF_KEY in schema.additionalProperties) {
          additionalProperties = {
            type: "object",
            ...schema.additionalProperties
          };
        } else {
          additionalProperties = { type: guessType(get_default(formData, [key])) };
        }
      } else {
        additionalProperties = { type: guessType(get_default(formData, [key])) };
      }
      schema.properties[key] = additionalProperties;
      set_default(schema.properties, [key, ADDITIONAL_PROPERTY_FLAG], true);
    } else {
      schema.properties[key] = { type: "null" };
      set_default(schema.properties, [key, ADDITIONAL_PROPERTY_FLAG], true);
    }
  });
  return schema;
}
function retrieveSchemaInternal(validator, schema, rootSchema, rawFormData, expandAllBranches = false, recurseList = [], experimental_customMergeAllOf) {
  if (!isObject(schema)) {
    return [{}];
  }
  const resolvedSchemas = resolveSchema(validator, schema, rootSchema, expandAllBranches, recurseList, rawFormData, experimental_customMergeAllOf);
  return resolvedSchemas.flatMap((s) => {
    var _a;
    let resolvedSchema = s;
    if (IF_KEY in resolvedSchema) {
      return resolveCondition(validator, resolvedSchema, rootSchema, expandAllBranches, recurseList, rawFormData, experimental_customMergeAllOf);
    }
    if (ALL_OF_KEY in resolvedSchema) {
      if (expandAllBranches) {
        const { allOf, ...restOfSchema } = resolvedSchema;
        return [...allOf, restOfSchema];
      }
      try {
        const withContainsSchemas = [];
        const withoutContainsSchemas = [];
        (_a = resolvedSchema.allOf) === null || _a === void 0 ? void 0 : _a.forEach((s2) => {
          if (typeof s2 === "object" && s2.contains) {
            withContainsSchemas.push(s2);
          } else {
            withoutContainsSchemas.push(s2);
          }
        });
        if (withContainsSchemas.length) {
          resolvedSchema = { ...resolvedSchema, allOf: withoutContainsSchemas };
        }
        resolvedSchema = experimental_customMergeAllOf ? experimental_customMergeAllOf(resolvedSchema) : (0, import_json_schema_merge_allof.default)(resolvedSchema, {
          deep: false,
          resolvers: {
            $defs: import_json_schema_merge_allof.default.options.resolvers.definitions
          }
        });
        if (withContainsSchemas.length) {
          resolvedSchema.allOf = withContainsSchemas;
        }
      } catch (e) {
        console.warn("could not merge subschemas in allOf:\n", e);
        const { allOf, ...resolvedSchemaWithoutAllOf } = resolvedSchema;
        return resolvedSchemaWithoutAllOf;
      }
    }
    if (PROPERTIES_KEY in resolvedSchema && PATTERN_PROPERTIES_KEY in resolvedSchema) {
      resolvedSchema = Object.keys(resolvedSchema.properties).reduce((schema2, key) => {
        const matchingProperties = getMatchingPatternProperties(schema2, key);
        if (!isEmpty_default(matchingProperties)) {
          schema2.properties[key] = retrieveSchema(validator, { allOf: [schema2.properties[key], ...Object.values(matchingProperties)] }, rootSchema, get_default(rawFormData, [key]), experimental_customMergeAllOf);
        }
        return schema2;
      }, {
        ...resolvedSchema,
        properties: { ...resolvedSchema.properties }
      });
    }
    const hasAdditionalProperties = PATTERN_PROPERTIES_KEY in resolvedSchema || ADDITIONAL_PROPERTIES_KEY in resolvedSchema && resolvedSchema.additionalProperties !== false;
    if (hasAdditionalProperties) {
      return stubExistingAdditionalProperties(validator, resolvedSchema, rootSchema, rawFormData, experimental_customMergeAllOf);
    }
    return resolvedSchema;
  });
}
function resolveAnyOrOneOfSchemas(validator, schema, rootSchema, expandAllBranches, rawFormData) {
  let anyOrOneOf;
  const { oneOf, anyOf, ...remaining } = schema;
  if (Array.isArray(oneOf)) {
    anyOrOneOf = oneOf;
  } else if (Array.isArray(anyOf)) {
    anyOrOneOf = anyOf;
  }
  if (anyOrOneOf) {
    const formData = rawFormData === void 0 && expandAllBranches ? {} : rawFormData;
    const discriminator = getDiscriminatorFieldFromSchema(schema);
    anyOrOneOf = anyOrOneOf.map((s) => {
      return resolveAllReferences(s, rootSchema, []);
    });
    const option = getFirstMatchingOption(validator, formData, anyOrOneOf, rootSchema, discriminator);
    if (expandAllBranches) {
      return anyOrOneOf.map((item) => mergeSchemas(remaining, item));
    }
    schema = mergeSchemas(remaining, anyOrOneOf[option]);
  }
  return [schema];
}
function resolveDependencies(validator, schema, rootSchema, expandAllBranches, recurseList, formData, experimental_customMergeAllOf) {
  const { dependencies, ...remainingSchema } = schema;
  const resolvedSchemas = resolveAnyOrOneOfSchemas(validator, remainingSchema, rootSchema, expandAllBranches, formData);
  return resolvedSchemas.flatMap((resolvedSchema) => processDependencies(validator, dependencies, resolvedSchema, rootSchema, expandAllBranches, recurseList, formData, experimental_customMergeAllOf));
}
function processDependencies(validator, dependencies, resolvedSchema, rootSchema, expandAllBranches, recurseList, formData, experimental_customMergeAllOf) {
  let schemas = [resolvedSchema];
  for (const dependencyKey in dependencies) {
    if (!expandAllBranches && get_default(formData, [dependencyKey]) === void 0) {
      continue;
    }
    if (resolvedSchema.properties && !(dependencyKey in resolvedSchema.properties)) {
      continue;
    }
    const [remainingDependencies, dependencyValue] = splitKeyElementFromObject(dependencyKey, dependencies);
    if (Array.isArray(dependencyValue)) {
      schemas[0] = withDependentProperties(resolvedSchema, dependencyValue);
    } else if (isObject(dependencyValue)) {
      schemas = withDependentSchema(validator, resolvedSchema, rootSchema, dependencyKey, dependencyValue, expandAllBranches, recurseList, formData, experimental_customMergeAllOf);
    }
    return schemas.flatMap((schema) => processDependencies(validator, remainingDependencies, schema, rootSchema, expandAllBranches, recurseList, formData, experimental_customMergeAllOf));
  }
  return schemas;
}
function withDependentProperties(schema, additionallyRequired) {
  if (!additionallyRequired) {
    return schema;
  }
  const required = Array.isArray(schema.required) ? Array.from(/* @__PURE__ */ new Set([...schema.required, ...additionallyRequired])) : additionallyRequired;
  return { ...schema, required };
}
function withDependentSchema(validator, schema, rootSchema, dependencyKey, dependencyValue, expandAllBranches, recurseList, formData, experimental_customMergeAllOf) {
  const dependentSchemas = retrieveSchemaInternal(validator, dependencyValue, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf);
  return dependentSchemas.flatMap((dependent) => {
    const { oneOf, ...dependentSchema } = dependent;
    schema = mergeSchemas(schema, dependentSchema);
    if (oneOf === void 0) {
      return schema;
    }
    const resolvedOneOfs = oneOf.map((subschema) => {
      if (typeof subschema === "boolean" || !(REF_KEY in subschema)) {
        return [subschema];
      }
      return resolveReference(validator, subschema, rootSchema, expandAllBranches, recurseList, formData);
    });
    const allPermutations = getAllPermutationsOfXxxOf(resolvedOneOfs);
    return allPermutations.flatMap((resolvedOneOf) => withExactlyOneSubschema(validator, schema, rootSchema, dependencyKey, resolvedOneOf, expandAllBranches, recurseList, formData, experimental_customMergeAllOf));
  });
}
function withExactlyOneSubschema(validator, schema, rootSchema, dependencyKey, oneOf, expandAllBranches, recurseList, formData, experimental_customMergeAllOf) {
  const validSubschemas = oneOf.filter((subschema) => {
    if (typeof subschema === "boolean" || !subschema || !subschema.properties) {
      return false;
    }
    const { [dependencyKey]: conditionPropertySchema } = subschema.properties;
    if (conditionPropertySchema) {
      const conditionSchema = {
        type: "object",
        properties: {
          [dependencyKey]: conditionPropertySchema
        }
      };
      return validator.isValid(conditionSchema, formData, rootSchema) || expandAllBranches;
    }
    return false;
  });
  if (!expandAllBranches && validSubschemas.length !== 1) {
    console.warn("ignoring oneOf in dependencies because there isn't exactly one subschema that is valid");
    return [schema];
  }
  return validSubschemas.flatMap((s) => {
    const subschema = s;
    const [dependentSubschema] = splitKeyElementFromObject(dependencyKey, subschema.properties);
    const dependentSchema = { ...subschema, properties: dependentSubschema };
    const schemas = retrieveSchemaInternal(validator, dependentSchema, rootSchema, formData, expandAllBranches, recurseList, experimental_customMergeAllOf);
    return schemas.map((s2) => mergeSchemas(schema, s2));
  });
}

// node_modules/@rjsf/utils/lib/schema/findSelectedOptionInXxxOf.js
function findSelectedOptionInXxxOf(validator, rootSchema, schema, fallbackField, xxx, formData = {}, experimental_customMergeAllOf) {
  if (Array.isArray(schema[xxx])) {
    const discriminator = getDiscriminatorFieldFromSchema(schema);
    const selectorField = discriminator || fallbackField;
    const xxxOfs = schema[xxx].map((xxxOf) => retrieveSchema(validator, xxxOf, rootSchema, formData, experimental_customMergeAllOf));
    const data = get_default(formData, selectorField);
    if (data !== void 0) {
      return xxxOfs.find((xxx2) => {
        return isEqual_default(get_default(xxx2, [PROPERTIES_KEY, selectorField, DEFAULT_KEY], get_default(xxx2, [PROPERTIES_KEY, selectorField, CONST_KEY])), data);
      });
    }
  }
  return void 0;
}

// node_modules/@rjsf/utils/lib/schema/getFromSchema.js
function getFromSchemaInternal(validator, rootSchema, schema, path, experimental_customMergeAllOf) {
  let fieldSchema = schema;
  if (has_default(schema, REF_KEY)) {
    fieldSchema = retrieveSchema(validator, schema, rootSchema, void 0, experimental_customMergeAllOf);
  }
  if (isEmpty_default(path)) {
    return fieldSchema;
  }
  const pathList = Array.isArray(path) ? path : path.split(".");
  const [part, ...nestedPath] = pathList;
  if (part && has_default(fieldSchema, part)) {
    fieldSchema = get_default(fieldSchema, part);
    return getFromSchemaInternal(validator, rootSchema, fieldSchema, nestedPath, experimental_customMergeAllOf);
  }
  return void 0;
}
function getFromSchema(validator, rootSchema, schema, path, defaultValue, experimental_customMergeAllOf) {
  const result = getFromSchemaInternal(validator, rootSchema, schema, path, experimental_customMergeAllOf);
  if (result === void 0) {
    return defaultValue;
  }
  return result;
}

// node_modules/@rjsf/utils/lib/schema/findFieldInSchema.js
var NOT_FOUND_SCHEMA = { title: "!@#$_UNKNOWN_$#@!" };
function findFieldInSchema(validator, rootSchema, schema, path, formData = {}, experimental_customMergeAllOf) {
  const pathList = Array.isArray(path) ? [...path] : path.split(".");
  let parentField = schema;
  const fieldName = pathList.pop();
  if (pathList.length) {
    pathList.forEach((subPath) => {
      parentField = getFromSchema(validator, rootSchema, parentField, [PROPERTIES_KEY, subPath], {}, experimental_customMergeAllOf);
      if (has_default(parentField, ONE_OF_KEY)) {
        parentField = findSelectedOptionInXxxOf(validator, rootSchema, parentField, fieldName, ONE_OF_KEY, get_default(formData, subPath), experimental_customMergeAllOf);
      } else if (has_default(parentField, ANY_OF_KEY)) {
        parentField = findSelectedOptionInXxxOf(validator, rootSchema, parentField, fieldName, ANY_OF_KEY, get_default(formData, subPath), experimental_customMergeAllOf);
      }
    });
  }
  if (has_default(parentField, ONE_OF_KEY)) {
    parentField = findSelectedOptionInXxxOf(validator, rootSchema, parentField, fieldName, ONE_OF_KEY, formData, experimental_customMergeAllOf);
  } else if (has_default(parentField, ANY_OF_KEY)) {
    parentField = findSelectedOptionInXxxOf(validator, rootSchema, parentField, fieldName, ANY_OF_KEY, formData, experimental_customMergeAllOf);
  }
  let field = getFromSchema(validator, rootSchema, parentField, [PROPERTIES_KEY, fieldName], NOT_FOUND_SCHEMA, experimental_customMergeAllOf);
  if (field === NOT_FOUND_SCHEMA) {
    field = void 0;
  }
  const requiredArray = getFromSchema(validator, rootSchema, parentField, REQUIRED_KEY, [], experimental_customMergeAllOf);
  let isRequired;
  if (field && Array.isArray(requiredArray)) {
    isRequired = requiredArray.includes(fieldName);
  }
  return { field, isRequired };
}

// node_modules/lodash-es/_arrayReduce.js
function arrayReduce(array, iteratee, accumulator, initAccum) {
  var index = -1, length = array == null ? 0 : array.length;
  if (initAccum && length) {
    accumulator = array[++index];
  }
  while (++index < length) {
    accumulator = iteratee(accumulator, array[index], index, array);
  }
  return accumulator;
}
var arrayReduce_default = arrayReduce;

// node_modules/lodash-es/_createBaseEach.js
function createBaseEach(eachFunc, fromRight) {
  return function(collection, iteratee) {
    if (collection == null) {
      return collection;
    }
    if (!isArrayLike_default(collection)) {
      return eachFunc(collection, iteratee);
    }
    var length = collection.length, index = fromRight ? length : -1, iterable = Object(collection);
    while (fromRight ? index-- : ++index < length) {
      if (iteratee(iterable[index], index, iterable) === false) {
        break;
      }
    }
    return collection;
  };
}
var createBaseEach_default = createBaseEach;

// node_modules/lodash-es/_baseEach.js
var baseEach = createBaseEach_default(baseForOwn_default);
var baseEach_default = baseEach;

// node_modules/lodash-es/_baseReduce.js
function baseReduce(collection, iteratee, accumulator, initAccum, eachFunc) {
  eachFunc(collection, function(value, index, collection2) {
    accumulator = initAccum ? (initAccum = false, value) : iteratee(accumulator, value, index, collection2);
  });
  return accumulator;
}
var baseReduce_default = baseReduce;

// node_modules/lodash-es/reduce.js
function reduce(collection, iteratee, accumulator) {
  var func = isArray_default(collection) ? arrayReduce_default : baseReduce_default, initAccum = arguments.length < 3;
  return func(collection, baseIteratee_default(iteratee, 4), accumulator, initAccum, baseEach_default);
}
var reduce_default = reduce;

// node_modules/@rjsf/utils/lib/schema/getClosestMatchingOption.js
var JUNK_OPTION = {
  type: "object",
  $id: JUNK_OPTION_ID,
  properties: {
    __not_really_there__: {
      type: "number"
    }
  }
};
function calculateIndexScore(validator, rootSchema, schema, formData, experimental_customMergeAllOf) {
  let totalScore = 0;
  if (schema) {
    if (isObject_default(schema.properties)) {
      totalScore += reduce_default(schema.properties, (score, value, key) => {
        const formValue = get_default(formData, key);
        if (typeof value === "boolean") {
          return score;
        }
        if (has_default(value, REF_KEY)) {
          const newSchema = retrieveSchema(validator, value, rootSchema, formValue, experimental_customMergeAllOf);
          return score + calculateIndexScore(validator, rootSchema, newSchema, formValue || {}, experimental_customMergeAllOf);
        }
        if ((has_default(value, ONE_OF_KEY) || has_default(value, ANY_OF_KEY)) && formValue) {
          const key2 = has_default(value, ONE_OF_KEY) ? ONE_OF_KEY : ANY_OF_KEY;
          const discriminator = getDiscriminatorFieldFromSchema(value);
          return score + getClosestMatchingOption(validator, rootSchema, formValue, get_default(value, key2), -1, discriminator, experimental_customMergeAllOf);
        }
        if (value.type === "object") {
          if (isObject_default(formValue)) {
            score += 1;
          }
          return score + calculateIndexScore(validator, rootSchema, value, formValue, experimental_customMergeAllOf);
        }
        if (value.type === guessType(formValue)) {
          let newScore = score + 1;
          if (value.default) {
            newScore += formValue === value.default ? 1 : -1;
          } else if (value.const) {
            newScore += formValue === value.const ? 1 : -1;
          }
          return newScore;
        }
        return score;
      }, 0);
    } else if (isString_default(schema.type) && schema.type === guessType(formData)) {
      totalScore += 1;
    }
  }
  return totalScore;
}
function getClosestMatchingOption(validator, rootSchema, formData, options, selectedOption = -1, discriminatorField, experimental_customMergeAllOf) {
  const resolvedOptions = options.map((option) => {
    return resolveAllReferences(option, rootSchema, []);
  });
  const simpleDiscriminatorMatch = getOptionMatchingSimpleDiscriminator(formData, options, discriminatorField);
  if (isNumber_default(simpleDiscriminatorMatch)) {
    return simpleDiscriminatorMatch;
  }
  const allValidIndexes = resolvedOptions.reduce((validList, option, index) => {
    const testOptions = [JUNK_OPTION, option];
    const match = getFirstMatchingOption(validator, formData, testOptions, rootSchema, discriminatorField);
    if (match === 1) {
      validList.push(index);
    }
    return validList;
  }, []);
  if (allValidIndexes.length === 1) {
    return allValidIndexes[0];
  }
  if (!allValidIndexes.length) {
    times_default(resolvedOptions.length, (i) => allValidIndexes.push(i));
  }
  const scoreCount = /* @__PURE__ */ new Set();
  const { bestIndex } = allValidIndexes.reduce((scoreData, index) => {
    const { bestScore } = scoreData;
    const option = resolvedOptions[index];
    const score = calculateIndexScore(validator, rootSchema, option, formData, experimental_customMergeAllOf);
    scoreCount.add(score);
    if (score > bestScore) {
      return { bestIndex: index, bestScore: score };
    }
    return scoreData;
  }, { bestIndex: selectedOption, bestScore: 0 });
  if (scoreCount.size === 1 && selectedOption >= 0) {
    return selectedOption;
  }
  return bestIndex;
}

// node_modules/@rjsf/utils/lib/isFixedItems.js
function isFixedItems(schema) {
  return Array.isArray(schema.items) && schema.items.length > 0 && schema.items.every((item) => isObject(item));
}

// node_modules/@rjsf/utils/lib/mergeDefaultsWithFormData.js
function mergeDefaultsWithFormData(defaults, formData, mergeExtraArrayDefaults = false, defaultSupercedesUndefined = false, overrideFormDataWithDefaults = false) {
  if (Array.isArray(formData)) {
    const defaultsArray = Array.isArray(defaults) ? defaults : [];
    const overrideArray = overrideFormDataWithDefaults ? defaultsArray : formData;
    const overrideOppositeArray = overrideFormDataWithDefaults ? formData : defaultsArray;
    const mapped = overrideArray.map((value, idx) => {
      if (overrideOppositeArray[idx] !== void 0) {
        return mergeDefaultsWithFormData(defaultsArray[idx], formData[idx], mergeExtraArrayDefaults, defaultSupercedesUndefined, overrideFormDataWithDefaults);
      }
      return value;
    });
    if ((mergeExtraArrayDefaults || overrideFormDataWithDefaults) && mapped.length < overrideOppositeArray.length) {
      mapped.push(...overrideOppositeArray.slice(mapped.length));
    }
    return mapped;
  }
  if (isObject(formData)) {
    const acc = Object.assign({}, defaults);
    return Object.keys(formData).reduce((acc2, key) => {
      var _a, _b;
      const keyValue = get_default(formData, key);
      const keyExistsInDefaults = isObject(defaults) && key in defaults;
      const keyExistsInFormData = key in formData;
      const keyDefault = (_a = get_default(defaults, key)) !== null && _a !== void 0 ? _a : {};
      const defaultValueIsNestedObject = keyExistsInDefaults && Object.entries(keyDefault).some(([, v]) => isObject(v));
      const keyDefaultIsObject = keyExistsInDefaults && isObject(get_default(defaults, key));
      const keyHasFormDataObject = keyExistsInFormData && isObject(keyValue);
      if (keyDefaultIsObject && keyHasFormDataObject && !defaultValueIsNestedObject) {
        acc2[key] = {
          ...get_default(defaults, key),
          ...keyValue
        };
        return acc2;
      }
      acc2[key] = mergeDefaultsWithFormData(
        (_b = get_default(defaults, key)) !== null && _b !== void 0 ? _b : {},
        keyValue,
        mergeExtraArrayDefaults,
        defaultSupercedesUndefined,
        // overrideFormDataWithDefaults can be true only when the key value exists in defaults
        // Or if the key value doesn't exist in formData
        overrideFormDataWithDefaults && (keyExistsInDefaults || !keyExistsInFormData)
      );
      return acc2;
    }, acc);
  }
  if (defaultSupercedesUndefined && (!isNil_default(defaults) && isNil_default(formData) || typeof formData === "number" && isNaN(formData)) || overrideFormDataWithDefaults && !isNil_default(formData)) {
    return defaults;
  }
  return formData;
}

// node_modules/@rjsf/utils/lib/isConstant.js
function isConstant(schema) {
  return Array.isArray(schema.enum) && schema.enum.length === 1 || CONST_KEY in schema;
}

// node_modules/@rjsf/utils/lib/schema/isSelect.js
function isSelect(validator, theSchema, rootSchema = {}, experimental_customMergeAllOf) {
  const schema = retrieveSchema(validator, theSchema, rootSchema, void 0, experimental_customMergeAllOf);
  const altSchemas = schema.oneOf || schema.anyOf;
  if (Array.isArray(schema.enum)) {
    return true;
  }
  if (Array.isArray(altSchemas)) {
    return altSchemas.every((altSchemas2) => typeof altSchemas2 !== "boolean" && isConstant(altSchemas2));
  }
  return false;
}

// node_modules/@rjsf/utils/lib/schema/isMultiSelect.js
function isMultiSelect(validator, schema, rootSchema, experimental_customMergeAllOf) {
  if (!schema.uniqueItems || !schema.items || typeof schema.items === "boolean") {
    return false;
  }
  return isSelect(validator, schema.items, rootSchema, experimental_customMergeAllOf);
}

// node_modules/@rjsf/utils/lib/allowAdditionalItems.js
function allowAdditionalItems(schema) {
  if (schema.additionalItems === true) {
    console.warn("additionalItems=true is currently not supported");
  }
  return isObject(schema.additionalItems);
}

// node_modules/@rjsf/utils/lib/asNumber.js
function asNumber(value) {
  if (value === "") {
    return void 0;
  }
  if (value === null) {
    return null;
  }
  if (/\.$/.test(value)) {
    return value;
  }
  if (/\.0$/.test(value)) {
    return value;
  }
  if (/\.\d*0$/.test(value)) {
    return value;
  }
  const n = Number(value);
  const valid = typeof n === "number" && !Number.isNaN(n);
  return valid ? n : value;
}

// node_modules/@rjsf/utils/lib/canExpand.js
function canExpand(schema, uiSchema = {}, formData) {
  if (!(schema.additionalProperties || schema.patternProperties)) {
    return false;
  }
  const { expandable = true } = getUiOptions(uiSchema);
  if (expandable === false) {
    return expandable;
  }
  if (schema.maxProperties !== void 0 && formData) {
    return Object.keys(formData).length < schema.maxProperties;
  }
  return true;
}

// node_modules/@rjsf/utils/lib/dataURItoBlob.js
function dataURItoBlob(dataURILike) {
  var _a;
  if (dataURILike.indexOf("data:") === -1) {
    throw new Error("File is invalid: URI must be a dataURI");
  }
  const dataURI = dataURILike.slice(5);
  const splitted = dataURI.split(";base64,");
  if (splitted.length !== 2) {
    throw new Error("File is invalid: dataURI must be base64");
  }
  const [media, base64] = splitted;
  const [mime, ...mediaparams] = media.split(";");
  const type = mime || "";
  const name = decodeURI(
    // parse the parameters into key-value pairs, find a key, and extract a value
    // if no key is found, then the name is unknown
    ((_a = mediaparams.map((param) => param.split("=")).find(([key]) => key === "name")) === null || _a === void 0 ? void 0 : _a[1]) || "unknown"
  );
  try {
    const binary = atob(base64);
    const array = new Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      array[i] = binary.charCodeAt(i);
    }
    const blob = new window.Blob([new Uint8Array(array)], { type });
    return { blob, name };
  } catch (error) {
    throw new Error("File is invalid: " + error.message);
  }
}

// node_modules/@rjsf/utils/lib/pad.js
function pad(num, width) {
  let s = String(num);
  while (s.length < width) {
    s = "0" + s;
  }
  return s;
}

// node_modules/@rjsf/utils/lib/dateRangeOptions.js
function dateRangeOptions(start, stop) {
  if (start <= 0 && stop <= 0) {
    start = (/* @__PURE__ */ new Date()).getFullYear() + start;
    stop = (/* @__PURE__ */ new Date()).getFullYear() + stop;
  } else if (start < 0 || stop < 0) {
    throw new Error(`Both start (${start}) and stop (${stop}) must both be <= 0 or > 0, got one of each`);
  }
  if (start > stop) {
    return dateRangeOptions(stop, start).reverse();
  }
  const options = [];
  for (let i = start; i <= stop; i++) {
    options.push({ value: i, label: pad(i, 2) });
  }
  return options;
}

// node_modules/@rjsf/utils/lib/replaceStringParameters.js
function replaceStringParameters(inputString, params) {
  let output = inputString;
  if (Array.isArray(params)) {
    const parts = output.split(/(%\d)/);
    params.forEach((param, index) => {
      const partIndex = parts.findIndex((part) => part === `%${index + 1}`);
      if (partIndex >= 0) {
        parts[partIndex] = param;
      }
    });
    output = parts.join("");
  }
  return output;
}

// node_modules/@rjsf/utils/lib/englishStringTranslator.js
function englishStringTranslator(stringToTranslate, params) {
  return replaceStringParameters(stringToTranslate, params);
}

// node_modules/@rjsf/utils/lib/enumOptionsValueForIndex.js
function enumOptionsValueForIndex(valueIndex, allEnumOptions = [], emptyValue) {
  if (Array.isArray(valueIndex)) {
    return valueIndex.map((index2) => enumOptionsValueForIndex(index2, allEnumOptions)).filter((val) => val !== emptyValue);
  }
  const index = valueIndex === "" || valueIndex === null ? -1 : Number(valueIndex);
  const option = allEnumOptions[index];
  return option ? option.value : emptyValue;
}

// node_modules/@rjsf/utils/lib/enumOptionsDeselectValue.js
function enumOptionsDeselectValue(valueIndex, selected, allEnumOptions = []) {
  const value = enumOptionsValueForIndex(valueIndex, allEnumOptions);
  if (Array.isArray(selected)) {
    return selected.filter((v) => !deepEquals(v, value));
  }
  return deepEquals(value, selected) ? void 0 : selected;
}

// node_modules/@rjsf/utils/lib/enumOptionsIsSelected.js
function enumOptionsIsSelected(value, selected) {
  if (Array.isArray(selected)) {
    return selected.some((sel) => deepEquals(sel, value));
  }
  return deepEquals(selected, value);
}

// node_modules/@rjsf/utils/lib/enumOptionsIndexForValue.js
function enumOptionsIndexForValue(value, allEnumOptions = [], multiple = false) {
  const selectedIndexes = allEnumOptions.map((opt, index) => enumOptionsIsSelected(opt.value, value) ? String(index) : void 0).filter((opt) => typeof opt !== "undefined");
  if (!multiple) {
    return selectedIndexes[0];
  }
  return selectedIndexes;
}

// node_modules/@rjsf/utils/lib/enumOptionsSelectValue.js
function enumOptionsSelectValue(valueIndex, selected, allEnumOptions = []) {
  const value = enumOptionsValueForIndex(valueIndex, allEnumOptions);
  if (!isNil_default(value)) {
    const index = allEnumOptions.findIndex((opt) => value === opt.value);
    const all = allEnumOptions.map(({ value: val }) => val);
    const updated = selected.slice(0, index).concat(value, selected.slice(index));
    return updated.sort((a, b) => Number(all.indexOf(a) > all.indexOf(b)));
  }
  return selected;
}

// node_modules/lodash-es/cloneDeep.js
var CLONE_DEEP_FLAG3 = 1;
var CLONE_SYMBOLS_FLAG3 = 4;
function cloneDeep(value) {
  return baseClone_default(value, CLONE_DEEP_FLAG3 | CLONE_SYMBOLS_FLAG3);
}
var cloneDeep_default = cloneDeep;

// node_modules/lodash-es/setWith.js
function setWith(object, path, value, customizer) {
  customizer = typeof customizer == "function" ? customizer : void 0;
  return object == null ? object : baseSet_default(object, path, value, customizer);
}
var setWith_default = setWith;

// node_modules/@rjsf/utils/lib/ErrorSchemaBuilder.js
var ErrorSchemaBuilder = class {
  /** Construct an `ErrorSchemaBuilder` with an optional initial set of errors in an `ErrorSchema`.
   *
   * @param [initialSchema] - The optional set of initial errors, that will be cloned into the class
   */
  constructor(initialSchema) {
    this.errorSchema = {};
    this.resetAllErrors(initialSchema);
  }
  /** Returns the `ErrorSchema` that has been updated by the methods of the `ErrorSchemaBuilder`
   */
  get ErrorSchema() {
    return this.errorSchema;
  }
  /** Will get an existing `ErrorSchema` at the specified `pathOfError` or create and return one.
   *
   * @param [pathOfError] - The optional path into the `ErrorSchema` at which to add the error(s)
   * @returns - The error block for the given `pathOfError` or the root if not provided
   * @private
   */
  getOrCreateErrorBlock(pathOfError) {
    const hasPath2 = Array.isArray(pathOfError) && pathOfError.length > 0 || typeof pathOfError === "string";
    let errorBlock = hasPath2 ? get_default(this.errorSchema, pathOfError) : this.errorSchema;
    if (!errorBlock && pathOfError) {
      errorBlock = {};
      setWith_default(this.errorSchema, pathOfError, errorBlock, Object);
    }
    return errorBlock;
  }
  /** Resets all errors in the `ErrorSchemaBuilder` back to the `initialSchema` if provided, otherwise an empty set.
   *
   * @param [initialSchema] - The optional set of initial errors, that will be cloned into the class
   * @returns - The `ErrorSchemaBuilder` object for chaining purposes
   */
  resetAllErrors(initialSchema) {
    this.errorSchema = initialSchema ? cloneDeep_default(initialSchema) : {};
    return this;
  }
  /** Adds the `errorOrList` to the list of errors in the `ErrorSchema` at either the root level or the location within
   * the schema described by the `pathOfError`. For more information about how to specify the path see the
   * [eslint lodash plugin docs](https://github.com/wix/eslint-plugin-lodash/blob/master/docs/rules/path-style.md).
   *
   * @param errorOrList - The error or list of errors to add into the `ErrorSchema`
   * @param [pathOfError] - The optional path into the `ErrorSchema` at which to add the error(s)
   * @returns - The `ErrorSchemaBuilder` object for chaining purposes
   */
  addErrors(errorOrList, pathOfError) {
    const errorBlock = this.getOrCreateErrorBlock(pathOfError);
    let errorsList = get_default(errorBlock, ERRORS_KEY);
    if (!Array.isArray(errorsList)) {
      errorsList = [];
      errorBlock[ERRORS_KEY] = errorsList;
    }
    if (Array.isArray(errorOrList)) {
      set_default(errorBlock, ERRORS_KEY, [.../* @__PURE__ */ new Set([...errorsList, ...errorOrList])]);
    } else {
      set_default(errorBlock, ERRORS_KEY, [.../* @__PURE__ */ new Set([...errorsList, errorOrList])]);
    }
    return this;
  }
  /** Sets/replaces the `errorOrList` as the error(s) in the `ErrorSchema` at either the root level or the location
   * within the schema described by the `pathOfError`. For more information about how to specify the path see the
   * [eslint lodash plugin docs](https://github.com/wix/eslint-plugin-lodash/blob/master/docs/rules/path-style.md).
   *
   * @param errorOrList - The error or list of errors to set into the `ErrorSchema`
   * @param [pathOfError] - The optional path into the `ErrorSchema` at which to set the error(s)
   * @returns - The `ErrorSchemaBuilder` object for chaining purposes
   */
  setErrors(errorOrList, pathOfError) {
    const errorBlock = this.getOrCreateErrorBlock(pathOfError);
    const listToAdd = Array.isArray(errorOrList) ? [.../* @__PURE__ */ new Set([...errorOrList])] : [errorOrList];
    set_default(errorBlock, ERRORS_KEY, listToAdd);
    return this;
  }
  /** Clears the error(s) in the `ErrorSchema` at either the root level or the location within the schema described by
   * the `pathOfError`. For more information about how to specify the path see the
   * [eslint lodash plugin docs](https://github.com/wix/eslint-plugin-lodash/blob/master/docs/rules/path-style.md).
   *
   * @param [pathOfError] - The optional path into the `ErrorSchema` at which to clear the error(s)
   * @returns - The `ErrorSchemaBuilder` object for chaining purposes
   */
  clearErrors(pathOfError) {
    const errorBlock = this.getOrCreateErrorBlock(pathOfError);
    set_default(errorBlock, ERRORS_KEY, []);
    return this;
  }
};

// node_modules/@rjsf/utils/lib/getDateElementProps.js
function getDateElementProps(date, time, yearRange = [1900, (/* @__PURE__ */ new Date()).getFullYear() + 2], format = "YMD") {
  const { day, month, year, hour, minute, second } = date;
  const dayObj = { type: "day", range: [1, 31], value: day };
  const monthObj = { type: "month", range: [1, 12], value: month };
  const yearObj = { type: "year", range: yearRange, value: year };
  const dateElementProp = [];
  switch (format) {
    case "MDY":
      dateElementProp.push(monthObj, dayObj, yearObj);
      break;
    case "DMY":
      dateElementProp.push(dayObj, monthObj, yearObj);
      break;
    case "YMD":
    default:
      dateElementProp.push(yearObj, monthObj, dayObj);
  }
  if (time) {
    dateElementProp.push({ type: "hour", range: [0, 23], value: hour }, { type: "minute", range: [0, 59], value: minute }, { type: "second", range: [0, 59], value: second });
  }
  return dateElementProp;
}

// node_modules/@rjsf/utils/lib/rangeSpec.js
function rangeSpec(schema) {
  const spec = {};
  if (schema.multipleOf) {
    spec.step = schema.multipleOf;
  }
  if (schema.minimum || schema.minimum === 0) {
    spec.min = schema.minimum;
  }
  if (schema.maximum || schema.maximum === 0) {
    spec.max = schema.maximum;
  }
  return spec;
}

// node_modules/@rjsf/utils/lib/getInputProps.js
function getInputProps(schema, defaultType, options = {}, autoDefaultStepAny = true) {
  const inputProps = {
    type: defaultType || "text",
    ...rangeSpec(schema)
  };
  if (options.inputType) {
    inputProps.type = options.inputType;
  } else if (!defaultType) {
    if (schema.type === "number") {
      inputProps.type = "number";
      if (autoDefaultStepAny && inputProps.step === void 0) {
        inputProps.step = "any";
      }
    } else if (schema.type === "integer") {
      inputProps.type = "number";
      if (inputProps.step === void 0) {
        inputProps.step = 1;
      }
    }
  }
  if (options.autocomplete) {
    inputProps.autoComplete = options.autocomplete;
  }
  if (options.accept) {
    inputProps.accept = options.accept;
  }
  return inputProps;
}

// node_modules/@rjsf/utils/lib/getSubmitButtonOptions.js
var DEFAULT_OPTIONS = {
  props: {
    disabled: false
  },
  submitText: "Submit",
  norender: false
};
function getSubmitButtonOptions(uiSchema = {}) {
  const uiOptions = getUiOptions(uiSchema);
  if (uiOptions && uiOptions[SUBMIT_BTN_OPTIONS_KEY]) {
    const options = uiOptions[SUBMIT_BTN_OPTIONS_KEY];
    return { ...DEFAULT_OPTIONS, ...options };
  }
  return DEFAULT_OPTIONS;
}

// node_modules/@rjsf/utils/lib/getTemplate.js
function getTemplate(name, registry, uiOptions = {}) {
  const { templates } = registry;
  if (name === "ButtonTemplates") {
    return templates[name];
  }
  if (Object.hasOwn(uiOptions, name) && typeof uiOptions[name] === "string" && Object.hasOwn(templates, uiOptions[name])) {
    const key = uiOptions[name];
    return templates[key];
  }
  return (
    // Evaluating uiOptions[name] results in TS2590: Expression produces a union type that is too complex to represent
    // To avoid that, we cast uiOptions to `any` before accessing the name field
    uiOptions[name] || templates[name]
  );
}

// node_modules/nanoid/url-alphabet/index.js
var urlAlphabet = "useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict";

// node_modules/nanoid/index.browser.js
var nanoid = (size = 21) => {
  let id = "";
  let bytes = crypto.getRandomValues(new Uint8Array(size |= 0));
  while (size--) {
    id += urlAlphabet[bytes[size] & 63];
  }
  return id;
};

// node_modules/@rjsf/utils/lib/getTestIds.js
function getTestIds() {
  if (typeof process === "undefined" || get_default(process, "env.NODE_ENV") !== "test") {
    return {};
  }
  const ids = /* @__PURE__ */ new Map();
  return new Proxy({}, {
    get(_obj, prop) {
      if (!ids.has(prop)) {
        ids.set(prop, nanoid());
      }
      return ids.get(prop);
    }
  });
}

// node_modules/@rjsf/utils/lib/getWidget.js
var import_jsx_runtime = __toESM(require_jsx_runtime(), 1);
var import_react = __toESM(require_react(), 1);
var import_react_is = __toESM(require_react_is(), 1);
var widgetMap = {
  boolean: {
    checkbox: "CheckboxWidget",
    radio: "RadioWidget",
    select: "SelectWidget",
    hidden: "HiddenWidget"
  },
  string: {
    text: "TextWidget",
    password: "PasswordWidget",
    email: "EmailWidget",
    hostname: "TextWidget",
    ipv4: "TextWidget",
    ipv6: "TextWidget",
    uri: "URLWidget",
    "data-url": "FileWidget",
    radio: "RadioWidget",
    select: "SelectWidget",
    textarea: "TextareaWidget",
    hidden: "HiddenWidget",
    date: "DateWidget",
    datetime: "DateTimeWidget",
    "date-time": "DateTimeWidget",
    "alt-date": "AltDateWidget",
    "alt-datetime": "AltDateTimeWidget",
    time: "TimeWidget",
    color: "ColorWidget",
    file: "FileWidget"
  },
  number: {
    text: "TextWidget",
    select: "SelectWidget",
    updown: "UpDownWidget",
    range: "RangeWidget",
    radio: "RadioWidget",
    hidden: "HiddenWidget"
  },
  integer: {
    text: "TextWidget",
    select: "SelectWidget",
    updown: "UpDownWidget",
    range: "RangeWidget",
    radio: "RadioWidget",
    hidden: "HiddenWidget"
  },
  array: {
    select: "SelectWidget",
    checkboxes: "CheckboxesWidget",
    files: "FileWidget",
    hidden: "HiddenWidget"
  }
};
function mergeWidgetOptions(AWidget) {
  let MergedWidget = get_default(AWidget, "MergedWidget");
  if (!MergedWidget) {
    const defaultOptions = AWidget.defaultProps && AWidget.defaultProps.options || {};
    MergedWidget = ({ options, ...props }) => {
      return (0, import_jsx_runtime.jsx)(AWidget, { options: { ...defaultOptions, ...options }, ...props });
    };
    set_default(AWidget, "MergedWidget", MergedWidget);
  }
  return MergedWidget;
}
function getWidget(schema, widget, registeredWidgets = {}) {
  const type = getSchemaType(schema);
  if (typeof widget === "function" || widget && import_react_is.default.isForwardRef((0, import_react.createElement)(widget)) || import_react_is.default.isMemo(widget)) {
    return mergeWidgetOptions(widget);
  }
  if (typeof widget !== "string") {
    throw new Error(`Unsupported widget definition: ${typeof widget}`);
  }
  if (widget in registeredWidgets) {
    const registeredWidget = registeredWidgets[widget];
    return getWidget(schema, registeredWidget, registeredWidgets);
  }
  if (typeof type === "string") {
    if (!(type in widgetMap)) {
      throw new Error(`No widget for type '${type}'`);
    }
    if (widget in widgetMap[type]) {
      const registeredWidget = registeredWidgets[widgetMap[type][widget]];
      return getWidget(schema, registeredWidget, registeredWidgets);
    }
  }
  throw new Error(`No widget '${widget}' for type '${type}'`);
}

// node_modules/@rjsf/utils/lib/hashForSchema.js
function hashString(string) {
  let hash = 0;
  for (let i = 0; i < string.length; i += 1) {
    const chr = string.charCodeAt(i);
    hash = (hash << 5) - hash + chr;
    hash = hash & hash;
  }
  return hash.toString(16);
}
function sortedJSONStringify(object) {
  const allKeys = /* @__PURE__ */ new Set();
  JSON.stringify(object, (key, value) => (allKeys.add(key), value));
  return JSON.stringify(object, Array.from(allKeys).sort());
}
function hashObject(object) {
  return hashString(sortedJSONStringify(object));
}
function hashForSchema(schema) {
  return hashObject(schema);
}

// node_modules/@rjsf/utils/lib/hasWidget.js
function hasWidget(schema, widget, registeredWidgets = {}) {
  try {
    getWidget(schema, widget, registeredWidgets);
    return true;
  } catch (e) {
    const err = e;
    if (err.message && (err.message.startsWith("No widget") || err.message.startsWith("Unsupported widget"))) {
      return false;
    }
    throw e;
  }
}

// node_modules/@rjsf/utils/lib/idGenerators.js
function idGenerator(id, suffix) {
  const theId = isString_default(id) ? id : id[ID_KEY];
  return `${theId}__${suffix}`;
}
function descriptionId(id) {
  return idGenerator(id, "description");
}
function errorId(id) {
  return idGenerator(id, "error");
}
function examplesId(id) {
  return idGenerator(id, "examples");
}
function helpId(id) {
  return idGenerator(id, "help");
}
function titleId(id) {
  return idGenerator(id, "title");
}
function ariaDescribedByIds(id, includeExamples = false) {
  const examples = includeExamples ? ` ${examplesId(id)}` : "";
  return `${errorId(id)} ${descriptionId(id)} ${helpId(id)}${examples}`;
}
function optionId(id, optionIndex) {
  return `${id}-${optionIndex}`;
}
function buttonId(id, btn) {
  return idGenerator(id, btn);
}

// node_modules/@rjsf/utils/lib/isCustomWidget.js
function isCustomWidget(uiSchema = {}) {
  return (
    // TODO: Remove the `&& uiSchema['ui:widget'] !== 'hidden'` once we support hidden widgets for arrays.
    // https://rjsf-team.github.io/react-jsonschema-form/docs/usage/widgets/#hidden-widgets
    "widget" in getUiOptions(uiSchema) && getUiOptions(uiSchema)["widget"] !== "hidden"
  );
}

// node_modules/@rjsf/utils/lib/labelValue.js
function labelValue(label, hideLabel, fallback) {
  return hideLabel ? fallback : label;
}

// node_modules/@rjsf/utils/lib/localToUTC.js
function localToUTC(dateString) {
  return dateString ? new Date(dateString).toJSON() : void 0;
}

// node_modules/@rjsf/utils/lib/lookupFromFormContext.js
function lookupFromFormContext(regOrFc, toLookup, fallback) {
  const lookupPath = [LOOKUP_MAP_NAME];
  if (has_default(regOrFc, FORM_CONTEXT_NAME)) {
    lookupPath.unshift(FORM_CONTEXT_NAME);
  }
  return get_default(regOrFc, [...lookupPath, toLookup], fallback);
}

// node_modules/@rjsf/utils/lib/toConstant.js
function toConstant(schema) {
  if (ENUM_KEY in schema && Array.isArray(schema.enum) && schema.enum.length === 1) {
    return schema.enum[0];
  }
  if (CONST_KEY in schema) {
    return schema.const;
  }
  throw new Error("schema cannot be inferred as a constant");
}

// node_modules/@rjsf/utils/lib/optionsList.js
function optionsList(schema, uiSchema) {
  if (schema.enum) {
    let enumNames;
    if (uiSchema) {
      const { enumNames: uiEnumNames } = getUiOptions(uiSchema);
      enumNames = uiEnumNames;
    }
    return schema.enum.map((value, i) => {
      const label = (enumNames === null || enumNames === void 0 ? void 0 : enumNames[i]) || String(value);
      return { label, value };
    });
  }
  let altSchemas = void 0;
  let altUiSchemas = void 0;
  if (schema.anyOf) {
    altSchemas = schema.anyOf;
    altUiSchemas = uiSchema === null || uiSchema === void 0 ? void 0 : uiSchema.anyOf;
  } else if (schema.oneOf) {
    altSchemas = schema.oneOf;
    altUiSchemas = uiSchema === null || uiSchema === void 0 ? void 0 : uiSchema.oneOf;
  }
  let selectorField = getDiscriminatorFieldFromSchema(schema);
  if (uiSchema) {
    const { optionsSchemaSelector = selectorField } = getUiOptions(uiSchema);
    selectorField = optionsSchemaSelector;
  }
  return altSchemas && altSchemas.map((aSchemaDef, index) => {
    const { title } = getUiOptions(altUiSchemas === null || altUiSchemas === void 0 ? void 0 : altUiSchemas[index]);
    const aSchema = aSchemaDef;
    let value;
    let label = title;
    if (selectorField) {
      const innerSchema = get_default(aSchema, [PROPERTIES_KEY, selectorField], {});
      value = get_default(innerSchema, DEFAULT_KEY, get_default(innerSchema, CONST_KEY));
      label = label || (innerSchema === null || innerSchema === void 0 ? void 0 : innerSchema.title) || aSchema.title || String(value);
    } else {
      value = toConstant(aSchema);
      label = label || aSchema.title || String(value);
    }
    return {
      schema: aSchema,
      label,
      value
    };
  });
}

// node_modules/@rjsf/utils/lib/orderProperties.js
function orderProperties(properties, order) {
  if (!Array.isArray(order)) {
    return properties;
  }
  const arrayToHash = (arr) => arr.reduce((prev, curr) => {
    prev[curr] = true;
    return prev;
  }, {});
  const errorPropList = (arr) => arr.length > 1 ? `properties '${arr.join("', '")}'` : `property '${arr[0]}'`;
  const propertyHash = arrayToHash(properties);
  const orderFiltered = order.filter((prop) => prop === "*" || propertyHash[prop]);
  const orderHash = arrayToHash(orderFiltered);
  const rest = properties.filter((prop) => !orderHash[prop]);
  const restIndex = orderFiltered.indexOf("*");
  if (restIndex === -1) {
    if (rest.length) {
      throw new Error(`uiSchema order list does not contain ${errorPropList(rest)}`);
    }
    return orderFiltered;
  }
  if (restIndex !== orderFiltered.lastIndexOf("*")) {
    throw new Error("uiSchema order list contains more than one wildcard item");
  }
  const complete = [...orderFiltered];
  complete.splice(restIndex, 1, ...rest);
  return complete;
}

// node_modules/@rjsf/utils/lib/parseDateString.js
function parseDateString(dateString, includeTime = true) {
  if (!dateString) {
    return {
      year: -1,
      month: -1,
      day: -1,
      hour: includeTime ? -1 : 0,
      minute: includeTime ? -1 : 0,
      second: includeTime ? -1 : 0
    };
  }
  const date = new Date(dateString);
  if (Number.isNaN(date.getTime())) {
    throw new Error("Unable to parse date " + dateString);
  }
  return {
    year: date.getUTCFullYear(),
    month: date.getUTCMonth() + 1,
    // oh you, javascript.
    day: date.getUTCDate(),
    hour: includeTime ? date.getUTCHours() : 0,
    minute: includeTime ? date.getUTCMinutes() : 0,
    second: includeTime ? date.getUTCSeconds() : 0
  };
}

// node_modules/@rjsf/utils/lib/schemaRequiresTrueValue.js
function schemaRequiresTrueValue(schema) {
  if (schema.const) {
    return true;
  }
  if (schema.enum && schema.enum.length === 1 && schema.enum[0] === true) {
    return true;
  }
  if (schema.anyOf && schema.anyOf.length === 1) {
    return schemaRequiresTrueValue(schema.anyOf[0]);
  }
  if (schema.oneOf && schema.oneOf.length === 1) {
    return schemaRequiresTrueValue(schema.oneOf[0]);
  }
  if (schema.allOf) {
    const schemaSome = (subSchema) => schemaRequiresTrueValue(subSchema);
    return schema.allOf.some(schemaSome);
  }
  return false;
}

// node_modules/@rjsf/utils/lib/shouldRender.js
function shouldRender(component, nextProps, nextState) {
  const { props, state } = component;
  return !deepEquals(props, nextProps) || !deepEquals(state, nextState);
}

// node_modules/@rjsf/utils/lib/toDateString.js
function toDateString(dateObject, time = true) {
  const { year, month, day, hour = 0, minute = 0, second = 0 } = dateObject;
  const utcTime = Date.UTC(year, month - 1, day, hour, minute, second);
  const datetime = new Date(utcTime).toJSON();
  return time ? datetime : datetime.slice(0, 10);
}

// node_modules/@rjsf/utils/lib/toErrorList.js
function toErrorList(errorSchema, fieldPath = []) {
  if (!errorSchema) {
    return [];
  }
  let errorList = [];
  if (ERRORS_KEY in errorSchema) {
    errorList = errorList.concat(errorSchema[ERRORS_KEY].map((message) => {
      const property2 = `.${fieldPath.join(".")}`;
      return {
        property: property2,
        message,
        stack: `${property2} ${message}`
      };
    }));
  }
  return Object.keys(errorSchema).reduce((acc, key) => {
    if (key !== ERRORS_KEY) {
      const childSchema = errorSchema[key];
      if (isPlainObject_default(childSchema)) {
        acc = acc.concat(toErrorList(childSchema, [...fieldPath, key]));
      }
    }
    return acc;
  }, errorList);
}

// node_modules/lodash-es/toPath.js
function toPath(value) {
  if (isArray_default(value)) {
    return arrayMap_default(value, toKey_default);
  }
  return isSymbol_default(value) ? [value] : copyArray_default(stringToPath_default(toString_default(value)));
}
var toPath_default = toPath;

// node_modules/@rjsf/utils/lib/toErrorSchema.js
function toErrorSchema(errors) {
  const builder = new ErrorSchemaBuilder();
  if (errors.length) {
    errors.forEach((error) => {
      const { property: property2, message } = error;
      const path = property2 === "." ? [] : toPath_default(property2);
      if (path.length > 0 && path[0] === "") {
        path.splice(0, 1);
      }
      if (message) {
        builder.addErrors(message, path);
      }
    });
  }
  return builder.ErrorSchema;
}

// node_modules/@rjsf/utils/lib/unwrapErrorHandler.js
function unwrapErrorHandler(errorHandler) {
  return Object.keys(errorHandler).reduce((acc, key) => {
    if (key === "addError") {
      return acc;
    } else {
      const childSchema = errorHandler[key];
      if (isPlainObject_default(childSchema)) {
        return {
          ...acc,
          [key]: unwrapErrorHandler(childSchema)
        };
      }
      return { ...acc, [key]: childSchema };
    }
  }, {});
}

// node_modules/@rjsf/utils/lib/utcToLocal.js
function utcToLocal(jsonDate) {
  if (!jsonDate) {
    return "";
  }
  const date = new Date(jsonDate);
  const yyyy = pad(date.getFullYear(), 4);
  const MM = pad(date.getMonth() + 1, 2);
  const dd = pad(date.getDate(), 2);
  const hh = pad(date.getHours(), 2);
  const mm = pad(date.getMinutes(), 2);
  const ss = pad(date.getSeconds(), 2);
  const SSS = pad(date.getMilliseconds(), 3);
  return `${yyyy}-${MM}-${dd}T${hh}:${mm}:${ss}.${SSS}`;
}

// node_modules/@rjsf/utils/lib/validationDataMerge.js
function validationDataMerge(validationData, additionalErrorSchema) {
  if (!additionalErrorSchema) {
    return validationData;
  }
  const { errors: oldErrors, errorSchema: oldErrorSchema } = validationData;
  let errors = toErrorList(additionalErrorSchema);
  let errorSchema = additionalErrorSchema;
  if (!isEmpty_default(oldErrorSchema)) {
    errorSchema = mergeObjects(oldErrorSchema, additionalErrorSchema, true);
    errors = [...oldErrors].concat(errors);
  }
  return { errorSchema, errors };
}

// node_modules/@rjsf/utils/lib/withIdRefPrefix.js
function withIdRefPrefixObject(node) {
  for (const key in node) {
    const realObj = node;
    const value = realObj[key];
    if (key === REF_KEY && typeof value === "string" && value.startsWith("#")) {
      realObj[key] = ROOT_SCHEMA_PREFIX + value;
    } else {
      realObj[key] = withIdRefPrefix(value);
    }
  }
  return node;
}
function withIdRefPrefixArray(node) {
  for (let i = 0; i < node.length; i++) {
    node[i] = withIdRefPrefix(node[i]);
  }
  return node;
}
function withIdRefPrefix(schemaNode) {
  if (Array.isArray(schemaNode)) {
    return withIdRefPrefixArray([...schemaNode]);
  }
  if (isObject_default(schemaNode)) {
    return withIdRefPrefixObject({ ...schemaNode });
  }
  return schemaNode;
}

// node_modules/lodash-es/_basePickBy.js
function basePickBy(object, paths, predicate) {
  var index = -1, length = paths.length, result = {};
  while (++index < length) {
    var path = paths[index], value = baseGet_default(object, path);
    if (predicate(value, path)) {
      baseSet_default(result, castPath_default(path, object), value);
    }
  }
  return result;
}
var basePickBy_default = basePickBy;

// node_modules/lodash-es/pickBy.js
function pickBy(object, predicate) {
  if (object == null) {
    return {};
  }
  var props = arrayMap_default(getAllKeysIn_default(object), function(prop) {
    return [prop];
  });
  predicate = baseIteratee_default(predicate);
  return basePickBy_default(object, props, function(value, path) {
    return predicate(value, path[0]);
  });
}
var pickBy_default = pickBy;

// node_modules/lodash-es/_baseDifference.js
var LARGE_ARRAY_SIZE3 = 200;
function baseDifference(array, values, iteratee, comparator) {
  var index = -1, includes = arrayIncludes_default, isCommon = true, length = array.length, result = [], valuesLength = values.length;
  if (!length) {
    return result;
  }
  if (iteratee) {
    values = arrayMap_default(values, baseUnary_default(iteratee));
  }
  if (comparator) {
    includes = arrayIncludesWith_default;
    isCommon = false;
  } else if (values.length >= LARGE_ARRAY_SIZE3) {
    includes = cacheHas_default;
    isCommon = false;
    values = new SetCache_default(values);
  }
  outer:
    while (++index < length) {
      var value = array[index], computed = iteratee == null ? value : iteratee(value);
      value = comparator || value !== 0 ? value : 0;
      if (isCommon && computed === computed) {
        var valuesIndex = valuesLength;
        while (valuesIndex--) {
          if (values[valuesIndex] === computed) {
            continue outer;
          }
        }
        result.push(value);
      } else if (!includes(values, computed, comparator)) {
        result.push(value);
      }
    }
  return result;
}
var baseDifference_default = baseDifference;

// node_modules/lodash-es/difference.js
var difference = baseRest_default(function(array, values) {
  return isArrayLikeObject_default(array) ? baseDifference_default(array, baseFlatten_default(values, 1, isArrayLikeObject_default, true)) : [];
});
var difference_default = difference;

// node_modules/@rjsf/utils/lib/getChangedFields.js
function getChangedFields(a, b) {
  const aIsPlainObject = isPlainObject_default(a);
  const bIsPlainObject = isPlainObject_default(b);
  if (a === b || !aIsPlainObject && !bIsPlainObject) {
    return [];
  }
  if (aIsPlainObject && !bIsPlainObject) {
    return keys_default(a);
  } else if (!aIsPlainObject && bIsPlainObject) {
    return keys_default(b);
  } else {
    const unequalFields = keys_default(pickBy_default(a, (value, key) => !deepEquals(value, get_default(b, key))));
    const diffFields = difference_default(keys_default(b), keys_default(a));
    return [...unequalFields, ...diffFields];
  }
}

// node_modules/@rjsf/utils/lib/enums.js
var TranslatableString;
(function(TranslatableString2) {
  TranslatableString2["ArrayItemTitle"] = "Item";
  TranslatableString2["MissingItems"] = "Missing items definition";
  TranslatableString2["EmptyArray"] = "No items yet. Use the button below to add some.";
  TranslatableString2["YesLabel"] = "Yes";
  TranslatableString2["NoLabel"] = "No";
  TranslatableString2["CloseLabel"] = "Close";
  TranslatableString2["ErrorsLabel"] = "Errors";
  TranslatableString2["NewStringDefault"] = "New Value";
  TranslatableString2["AddButton"] = "Add";
  TranslatableString2["AddItemButton"] = "Add Item";
  TranslatableString2["CopyButton"] = "Copy";
  TranslatableString2["MoveDownButton"] = "Move down";
  TranslatableString2["MoveUpButton"] = "Move up";
  TranslatableString2["RemoveButton"] = "Remove";
  TranslatableString2["NowLabel"] = "Now";
  TranslatableString2["ClearLabel"] = "Clear";
  TranslatableString2["AriaDateLabel"] = "Select a date";
  TranslatableString2["PreviewLabel"] = "Preview";
  TranslatableString2["DecrementAriaLabel"] = "Decrease value by 1";
  TranslatableString2["IncrementAriaLabel"] = "Increase value by 1";
  TranslatableString2["UnknownFieldType"] = "Unknown field type %1";
  TranslatableString2["OptionPrefix"] = "Option %1";
  TranslatableString2["TitleOptionPrefix"] = "%1 option %2";
  TranslatableString2["KeyLabel"] = "%1 Key";
  TranslatableString2["InvalidObjectField"] = 'Invalid "%1" object field configuration: _%2_.';
  TranslatableString2["UnsupportedField"] = "Unsupported field schema.";
  TranslatableString2["UnsupportedFieldWithId"] = "Unsupported field schema for field `%1`.";
  TranslatableString2["UnsupportedFieldWithReason"] = "Unsupported field schema: _%1_.";
  TranslatableString2["UnsupportedFieldWithIdAndReason"] = "Unsupported field schema for field `%1`: _%2_.";
  TranslatableString2["FilesInfo"] = "**%1** (%2, %3 bytes)";
})(TranslatableString || (TranslatableString = {}));

// node_modules/lodash-es/forEach.js
function forEach(collection, iteratee) {
  var func = isArray_default(collection) ? arrayEach_default : baseEach_default;
  return func(collection, castFunction_default(iteratee));
}
var forEach_default = forEach;

// node_modules/@rjsf/utils/lib/constIsAjvDataReference.js
function constIsAjvDataReference(schema) {
  const schemaConst = schema[CONST_KEY];
  const schemaType = getSchemaType(schema);
  return isObject(schemaConst) && isString_default(schemaConst === null || schemaConst === void 0 ? void 0 : schemaConst.$data) && schemaType !== "object" && schemaType !== "array";
}

// node_modules/@rjsf/utils/lib/schema/getDefaultFormState.js
var PRIMITIVE_TYPES = ["string", "number", "integer", "boolean", "null"];
var AdditionalItemsHandling;
(function(AdditionalItemsHandling2) {
  AdditionalItemsHandling2[AdditionalItemsHandling2["Ignore"] = 0] = "Ignore";
  AdditionalItemsHandling2[AdditionalItemsHandling2["Invert"] = 1] = "Invert";
  AdditionalItemsHandling2[AdditionalItemsHandling2["Fallback"] = 2] = "Fallback";
})(AdditionalItemsHandling || (AdditionalItemsHandling = {}));
function getInnerSchemaForArrayItem(schema, additionalItems = AdditionalItemsHandling.Ignore, idx = -1) {
  if (idx >= 0) {
    if (Array.isArray(schema.items) && idx < schema.items.length) {
      const item = schema.items[idx];
      if (typeof item !== "boolean") {
        return item;
      }
    }
  } else if (schema.items && !Array.isArray(schema.items) && typeof schema.items !== "boolean") {
    return schema.items;
  }
  if (additionalItems !== AdditionalItemsHandling.Ignore && isObject(schema.additionalItems)) {
    return schema.additionalItems;
  }
  return {};
}
function maybeAddDefaultToObject(obj, key, computedDefault, includeUndefinedValues, isParentRequired, requiredFields = [], experimental_defaultFormStateBehavior = {}, isConst = false) {
  const { emptyObjectFields = "populateAllDefaults" } = experimental_defaultFormStateBehavior;
  if (includeUndefinedValues || isConst) {
    obj[key] = computedDefault;
  } else if (emptyObjectFields !== "skipDefaults") {
    const isSelfOrParentRequired = isParentRequired === void 0 ? requiredFields.includes(key) : isParentRequired;
    if (isObject(computedDefault)) {
      if (emptyObjectFields === "skipEmptyDefaults") {
        if (!isEmpty_default(computedDefault)) {
          obj[key] = computedDefault;
        }
      } else if ((!isEmpty_default(computedDefault) || requiredFields.includes(key)) && (isSelfOrParentRequired || emptyObjectFields !== "populateRequiredDefaults")) {
        obj[key] = computedDefault;
      }
    } else if (
      // Store computedDefault if it's a defined primitive (e.g., true) and satisfies certain conditions
      // Condition 1: computedDefault is not undefined
      // Condition 2: If emptyObjectFields is 'populateAllDefaults' or 'skipEmptyDefaults)
      // Or if isSelfOrParentRequired is 'true' and the key is a required field
      computedDefault !== void 0 && (emptyObjectFields === "populateAllDefaults" || emptyObjectFields === "skipEmptyDefaults" || isSelfOrParentRequired && requiredFields.includes(key))
    ) {
      obj[key] = computedDefault;
    }
  }
}
function computeDefaults(validator, rawSchema, computeDefaultsProps = {}) {
  const { parentDefaults, rawFormData, rootSchema = {}, includeUndefinedValues = false, _recurseList = [], experimental_defaultFormStateBehavior = void 0, experimental_customMergeAllOf = void 0, required, shouldMergeDefaultsIntoFormData = false } = computeDefaultsProps;
  let formData = isObject(rawFormData) ? rawFormData : {};
  const schema = isObject(rawSchema) ? rawSchema : {};
  let defaults = parentDefaults;
  let schemaToCompute = null;
  let experimental_dfsb_to_compute = experimental_defaultFormStateBehavior;
  let updatedRecurseList = _recurseList;
  if (schema[CONST_KEY] !== void 0 && (experimental_defaultFormStateBehavior === null || experimental_defaultFormStateBehavior === void 0 ? void 0 : experimental_defaultFormStateBehavior.constAsDefaults) !== "never" && !constIsAjvDataReference(schema)) {
    defaults = schema[CONST_KEY];
  } else if (isObject(defaults) && isObject(schema.default)) {
    defaults = mergeObjects(defaults, schema.default);
  } else if (DEFAULT_KEY in schema && !schema[ANY_OF_KEY] && !schema[ONE_OF_KEY] && !schema[REF_KEY]) {
    defaults = schema.default;
  } else if (REF_KEY in schema) {
    const refName = schema[REF_KEY];
    if (!_recurseList.includes(refName)) {
      updatedRecurseList = _recurseList.concat(refName);
      schemaToCompute = findSchemaDefinition(refName, rootSchema);
    }
    if (schemaToCompute && !defaults) {
      defaults = schema.default;
    }
    if (shouldMergeDefaultsIntoFormData && schemaToCompute && !isObject(rawFormData)) {
      formData = rawFormData;
    }
  } else if (DEPENDENCIES_KEY in schema) {
    const defaultFormData = {
      ...getDefaultBasedOnSchemaType(validator, schema, computeDefaultsProps, defaults),
      ...formData
    };
    const resolvedSchema = resolveDependencies(validator, schema, rootSchema, false, [], defaultFormData, experimental_customMergeAllOf);
    schemaToCompute = resolvedSchema[0];
  } else if (isFixedItems(schema)) {
    defaults = schema.items.map((itemSchema, idx) => computeDefaults(validator, itemSchema, {
      rootSchema,
      includeUndefinedValues,
      _recurseList,
      experimental_defaultFormStateBehavior,
      experimental_customMergeAllOf,
      parentDefaults: Array.isArray(parentDefaults) ? parentDefaults[idx] : void 0,
      rawFormData: formData,
      required,
      shouldMergeDefaultsIntoFormData
    }));
  } else if (ONE_OF_KEY in schema) {
    const { oneOf, ...remaining } = schema;
    if (oneOf.length === 0) {
      return void 0;
    }
    const discriminator = getDiscriminatorFieldFromSchema(schema);
    const { type = "null" } = remaining;
    if (!Array.isArray(type) && PRIMITIVE_TYPES.includes(type) && (experimental_dfsb_to_compute === null || experimental_dfsb_to_compute === void 0 ? void 0 : experimental_dfsb_to_compute.constAsDefaults) === "skipOneOf") {
      experimental_dfsb_to_compute = {
        ...experimental_dfsb_to_compute,
        constAsDefaults: "never"
      };
    }
    schemaToCompute = oneOf[getClosestMatchingOption(validator, rootSchema, rawFormData !== null && rawFormData !== void 0 ? rawFormData : schema.default, oneOf, 0, discriminator, experimental_customMergeAllOf)];
    schemaToCompute = mergeSchemas(remaining, schemaToCompute);
  } else if (ANY_OF_KEY in schema) {
    const { anyOf, ...remaining } = schema;
    if (anyOf.length === 0) {
      return void 0;
    }
    const discriminator = getDiscriminatorFieldFromSchema(schema);
    schemaToCompute = anyOf[getClosestMatchingOption(validator, rootSchema, rawFormData !== null && rawFormData !== void 0 ? rawFormData : schema.default, anyOf, 0, discriminator, experimental_customMergeAllOf)];
    schemaToCompute = mergeSchemas(remaining, schemaToCompute);
  }
  if (schemaToCompute) {
    return computeDefaults(validator, schemaToCompute, {
      rootSchema,
      includeUndefinedValues,
      _recurseList: updatedRecurseList,
      experimental_defaultFormStateBehavior: experimental_dfsb_to_compute,
      experimental_customMergeAllOf,
      parentDefaults: defaults,
      rawFormData: rawFormData !== null && rawFormData !== void 0 ? rawFormData : formData,
      required,
      shouldMergeDefaultsIntoFormData
    });
  }
  if (defaults === void 0) {
    defaults = schema.default;
  }
  const defaultBasedOnSchemaType = getDefaultBasedOnSchemaType(validator, schema, computeDefaultsProps, defaults);
  let defaultsWithFormData = defaultBasedOnSchemaType !== null && defaultBasedOnSchemaType !== void 0 ? defaultBasedOnSchemaType : defaults;
  if (shouldMergeDefaultsIntoFormData) {
    const { arrayMinItems = {} } = experimental_defaultFormStateBehavior || {};
    const { mergeExtraDefaults } = arrayMinItems;
    const matchingFormData = ensureFormDataMatchingSchema(validator, schema, rootSchema, rawFormData, experimental_defaultFormStateBehavior, experimental_customMergeAllOf);
    if (!isObject(rawFormData) || ALL_OF_KEY in schema) {
      defaultsWithFormData = mergeDefaultsWithFormData(defaultsWithFormData, matchingFormData, mergeExtraDefaults, true);
    }
  }
  return defaultsWithFormData;
}
function ensureFormDataMatchingSchema(validator, schema, rootSchema, formData, experimental_defaultFormStateBehavior, experimental_customMergeAllOf) {
  const isSelectField = !isConstant(schema) && isSelect(validator, schema, rootSchema, experimental_customMergeAllOf);
  let validFormData = formData;
  if (isSelectField) {
    const getOptionsList = optionsList(schema);
    const isValid = getOptionsList === null || getOptionsList === void 0 ? void 0 : getOptionsList.some((option) => deepEquals(option.value, formData));
    validFormData = isValid ? formData : void 0;
  }
  const constTakesPrecedence = schema[CONST_KEY] && (experimental_defaultFormStateBehavior === null || experimental_defaultFormStateBehavior === void 0 ? void 0 : experimental_defaultFormStateBehavior.constAsDefaults) === "always";
  if (constTakesPrecedence) {
    validFormData = schema.const;
  }
  return validFormData;
}
function getObjectDefaults(validator, rawSchema, { rawFormData, rootSchema = {}, includeUndefinedValues = false, _recurseList = [], experimental_defaultFormStateBehavior = void 0, experimental_customMergeAllOf = void 0, required, shouldMergeDefaultsIntoFormData } = {}, defaults) {
  {
    const formData = isObject(rawFormData) ? rawFormData : {};
    const schema = rawSchema;
    const retrievedSchema = (experimental_defaultFormStateBehavior === null || experimental_defaultFormStateBehavior === void 0 ? void 0 : experimental_defaultFormStateBehavior.allOf) === "populateDefaults" && ALL_OF_KEY in schema ? retrieveSchema(validator, schema, rootSchema, formData, experimental_customMergeAllOf) : schema;
    const parentConst = retrievedSchema[CONST_KEY];
    const objectDefaults = Object.keys(retrievedSchema.properties || {}).reduce((acc, key) => {
      var _a;
      const propertySchema = get_default(retrievedSchema, [PROPERTIES_KEY, key], {});
      const hasParentConst = isObject(parentConst) && parentConst[key] !== void 0;
      const hasConst = (isObject(propertySchema) && CONST_KEY in propertySchema || hasParentConst) && (experimental_defaultFormStateBehavior === null || experimental_defaultFormStateBehavior === void 0 ? void 0 : experimental_defaultFormStateBehavior.constAsDefaults) !== "never" && !constIsAjvDataReference(propertySchema);
      const computedDefault = computeDefaults(validator, propertySchema, {
        rootSchema,
        _recurseList,
        experimental_defaultFormStateBehavior,
        experimental_customMergeAllOf,
        includeUndefinedValues: includeUndefinedValues === true,
        parentDefaults: get_default(defaults, [key]),
        rawFormData: get_default(formData, [key]),
        required: (_a = retrievedSchema.required) === null || _a === void 0 ? void 0 : _a.includes(key),
        shouldMergeDefaultsIntoFormData
      });
      maybeAddDefaultToObject(acc, key, computedDefault, includeUndefinedValues, required, retrievedSchema.required, experimental_defaultFormStateBehavior, hasConst);
      return acc;
    }, {});
    if (retrievedSchema.additionalProperties) {
      const additionalPropertiesSchema = isObject(retrievedSchema.additionalProperties) ? retrievedSchema.additionalProperties : {};
      const keys2 = /* @__PURE__ */ new Set();
      if (isObject(defaults)) {
        Object.keys(defaults).filter((key) => !retrievedSchema.properties || !retrievedSchema.properties[key]).forEach((key) => keys2.add(key));
      }
      const formDataRequired = [];
      Object.keys(formData).filter((key) => !retrievedSchema.properties || !retrievedSchema.properties[key]).forEach((key) => {
        keys2.add(key);
        formDataRequired.push(key);
      });
      keys2.forEach((key) => {
        var _a;
        const computedDefault = computeDefaults(validator, additionalPropertiesSchema, {
          rootSchema,
          _recurseList,
          experimental_defaultFormStateBehavior,
          experimental_customMergeAllOf,
          includeUndefinedValues: includeUndefinedValues === true,
          parentDefaults: get_default(defaults, [key]),
          rawFormData: get_default(formData, [key]),
          required: (_a = retrievedSchema.required) === null || _a === void 0 ? void 0 : _a.includes(key),
          shouldMergeDefaultsIntoFormData
        });
        maybeAddDefaultToObject(objectDefaults, key, computedDefault, includeUndefinedValues, required, formDataRequired);
      });
    }
    return objectDefaults;
  }
}
function getArrayDefaults(validator, rawSchema, { rawFormData, rootSchema = {}, _recurseList = [], experimental_defaultFormStateBehavior = void 0, experimental_customMergeAllOf = void 0, required, shouldMergeDefaultsIntoFormData } = {}, defaults) {
  var _a, _b;
  const schema = rawSchema;
  const arrayMinItemsStateBehavior = (_a = experimental_defaultFormStateBehavior === null || experimental_defaultFormStateBehavior === void 0 ? void 0 : experimental_defaultFormStateBehavior.arrayMinItems) !== null && _a !== void 0 ? _a : {};
  const { populate: arrayMinItemsPopulate, mergeExtraDefaults: arrayMergeExtraDefaults } = arrayMinItemsStateBehavior;
  const neverPopulate = arrayMinItemsPopulate === "never";
  const ignoreMinItemsFlagSet = arrayMinItemsPopulate === "requiredOnly";
  const isPopulateAll = arrayMinItemsPopulate === "all" || !neverPopulate && !ignoreMinItemsFlagSet;
  const computeSkipPopulate = (_b = arrayMinItemsStateBehavior === null || arrayMinItemsStateBehavior === void 0 ? void 0 : arrayMinItemsStateBehavior.computeSkipPopulate) !== null && _b !== void 0 ? _b : () => false;
  const isSkipEmptyDefaults = (experimental_defaultFormStateBehavior === null || experimental_defaultFormStateBehavior === void 0 ? void 0 : experimental_defaultFormStateBehavior.emptyObjectFields) === "skipEmptyDefaults";
  const emptyDefault = isSkipEmptyDefaults ? void 0 : [];
  if (Array.isArray(defaults)) {
    defaults = defaults.map((item, idx) => {
      const schemaItem = getInnerSchemaForArrayItem(schema, AdditionalItemsHandling.Fallback, idx);
      return computeDefaults(validator, schemaItem, {
        rootSchema,
        _recurseList,
        experimental_defaultFormStateBehavior,
        experimental_customMergeAllOf,
        parentDefaults: item,
        required,
        shouldMergeDefaultsIntoFormData
      });
    });
  }
  if (Array.isArray(rawFormData)) {
    const schemaItem = getInnerSchemaForArrayItem(schema);
    if (neverPopulate) {
      defaults = rawFormData;
    } else {
      const itemDefaults = rawFormData.map((item, idx) => {
        return computeDefaults(validator, schemaItem, {
          rootSchema,
          _recurseList,
          experimental_defaultFormStateBehavior,
          experimental_customMergeAllOf,
          rawFormData: item,
          parentDefaults: get_default(defaults, [idx]),
          required,
          shouldMergeDefaultsIntoFormData
        });
      });
      const mergeExtraDefaults = (ignoreMinItemsFlagSet && required || isPopulateAll) && arrayMergeExtraDefaults;
      defaults = mergeDefaultsWithFormData(defaults, itemDefaults, mergeExtraDefaults);
    }
  }
  const hasConst = isObject(schema) && CONST_KEY in schema && (experimental_defaultFormStateBehavior === null || experimental_defaultFormStateBehavior === void 0 ? void 0 : experimental_defaultFormStateBehavior.constAsDefaults) !== "never";
  if (hasConst === false) {
    if (neverPopulate) {
      return defaults !== null && defaults !== void 0 ? defaults : emptyDefault;
    }
    if (ignoreMinItemsFlagSet && !required) {
      return defaults ? defaults : void 0;
    }
  }
  const defaultsLength = Array.isArray(defaults) ? defaults.length : 0;
  if (!schema.minItems || isMultiSelect(validator, schema, rootSchema, experimental_customMergeAllOf) || computeSkipPopulate(validator, schema, rootSchema) || schema.minItems <= defaultsLength) {
    return defaults ? defaults : emptyDefault;
  }
  const defaultEntries = defaults || [];
  const fillerSchema = getInnerSchemaForArrayItem(schema, AdditionalItemsHandling.Invert);
  const fillerDefault = fillerSchema.default;
  const fillerEntries = new Array(schema.minItems - defaultsLength).fill(computeDefaults(validator, fillerSchema, {
    parentDefaults: fillerDefault,
    rootSchema,
    _recurseList,
    experimental_defaultFormStateBehavior,
    experimental_customMergeAllOf,
    required,
    shouldMergeDefaultsIntoFormData
  }));
  return defaultEntries.concat(fillerEntries);
}
function getDefaultBasedOnSchemaType(validator, rawSchema, computeDefaultsProps = {}, defaults) {
  switch (getSchemaType(rawSchema)) {
    case "object": {
      return getObjectDefaults(validator, rawSchema, computeDefaultsProps, defaults);
    }
    case "array": {
      return getArrayDefaults(validator, rawSchema, computeDefaultsProps, defaults);
    }
  }
}
function getDefaultFormState(validator, theSchema, formData, rootSchema, includeUndefinedValues = false, experimental_defaultFormStateBehavior, experimental_customMergeAllOf) {
  if (!isObject(theSchema)) {
    throw new Error("Invalid schema: " + theSchema);
  }
  const schema = retrieveSchema(validator, theSchema, rootSchema, formData, experimental_customMergeAllOf);
  const defaults = computeDefaults(validator, schema, {
    rootSchema,
    includeUndefinedValues,
    experimental_defaultFormStateBehavior,
    experimental_customMergeAllOf,
    rawFormData: formData,
    shouldMergeDefaultsIntoFormData: true
  });
  if (schema.type !== "object" && isObject(schema.default)) {
    return {
      ...defaults,
      ...formData
    };
  }
  if (isObject(formData) || Array.isArray(formData)) {
    const { mergeDefaultsIntoFormData } = experimental_defaultFormStateBehavior || {};
    const defaultSupercedesUndefined = mergeDefaultsIntoFormData === "useDefaultIfFormDataUndefined";
    const result = mergeDefaultsWithFormData(
      defaults,
      formData,
      true,
      // set to true to add any additional default array entries.
      defaultSupercedesUndefined,
      true
    );
    return result;
  }
  return defaults;
}

// node_modules/@rjsf/utils/lib/schema/isFilesArray.js
function isFilesArray(validator, schema, uiSchema = {}, rootSchema, experimental_customMergeAllOf) {
  if (uiSchema[UI_WIDGET_KEY] === "files") {
    return true;
  }
  if (schema.items) {
    const itemsSchema = retrieveSchema(validator, schema.items, rootSchema, void 0, experimental_customMergeAllOf);
    return itemsSchema.type === "string" && itemsSchema.format === "data-url";
  }
  return false;
}

// node_modules/@rjsf/utils/lib/schema/getDisplayLabel.js
function getDisplayLabel(validator, schema, uiSchema = {}, rootSchema, globalOptions, experimental_customMergeAllOf) {
  const uiOptions = getUiOptions(uiSchema, globalOptions);
  const { label = true } = uiOptions;
  let displayLabel = !!label;
  const schemaType = getSchemaType(schema);
  if (schemaType === "array") {
    displayLabel = isMultiSelect(validator, schema, rootSchema, experimental_customMergeAllOf) || isFilesArray(validator, schema, uiSchema, rootSchema, experimental_customMergeAllOf) || isCustomWidget(uiSchema);
  }
  if (schemaType === "object") {
    displayLabel = false;
  }
  if (schemaType === "boolean" && !uiSchema[UI_WIDGET_KEY]) {
    displayLabel = false;
  }
  if (uiSchema[UI_FIELD_KEY]) {
    displayLabel = false;
  }
  return displayLabel;
}

// node_modules/@rjsf/utils/lib/schema/sanitizeDataForNewSchema.js
var NO_VALUE = Symbol("no Value");
function sanitizeDataForNewSchema(validator, rootSchema, newSchema, oldSchema, data = {}, experimental_customMergeAllOf) {
  let newFormData;
  if (has_default(newSchema, PROPERTIES_KEY)) {
    const removeOldSchemaData = {};
    if (has_default(oldSchema, PROPERTIES_KEY)) {
      const properties = get_default(oldSchema, PROPERTIES_KEY, {});
      Object.keys(properties).forEach((key) => {
        if (has_default(data, key)) {
          removeOldSchemaData[key] = void 0;
        }
      });
    }
    const keys2 = Object.keys(get_default(newSchema, PROPERTIES_KEY, {}));
    const nestedData = {};
    keys2.forEach((key) => {
      const formValue = get_default(data, key);
      let oldKeyedSchema = get_default(oldSchema, [PROPERTIES_KEY, key], {});
      let newKeyedSchema = get_default(newSchema, [PROPERTIES_KEY, key], {});
      if (has_default(oldKeyedSchema, REF_KEY)) {
        oldKeyedSchema = retrieveSchema(validator, oldKeyedSchema, rootSchema, formValue, experimental_customMergeAllOf);
      }
      if (has_default(newKeyedSchema, REF_KEY)) {
        newKeyedSchema = retrieveSchema(validator, newKeyedSchema, rootSchema, formValue, experimental_customMergeAllOf);
      }
      const oldSchemaTypeForKey = get_default(oldKeyedSchema, "type");
      const newSchemaTypeForKey = get_default(newKeyedSchema, "type");
      if (!oldSchemaTypeForKey || oldSchemaTypeForKey === newSchemaTypeForKey) {
        if (has_default(removeOldSchemaData, key)) {
          delete removeOldSchemaData[key];
        }
        if (newSchemaTypeForKey === "object" || newSchemaTypeForKey === "array" && Array.isArray(formValue)) {
          const itemData = sanitizeDataForNewSchema(validator, rootSchema, newKeyedSchema, oldKeyedSchema, formValue, experimental_customMergeAllOf);
          if (itemData !== void 0 || newSchemaTypeForKey === "array") {
            nestedData[key] = itemData;
          }
        } else {
          const newOptionDefault = get_default(newKeyedSchema, "default", NO_VALUE);
          const oldOptionDefault = get_default(oldKeyedSchema, "default", NO_VALUE);
          if (newOptionDefault !== NO_VALUE && newOptionDefault !== formValue) {
            if (oldOptionDefault === formValue) {
              removeOldSchemaData[key] = newOptionDefault;
            } else if (get_default(newKeyedSchema, "readOnly") === true) {
              removeOldSchemaData[key] = void 0;
            }
          }
          const newOptionConst = get_default(newKeyedSchema, "const", NO_VALUE);
          const oldOptionConst = get_default(oldKeyedSchema, "const", NO_VALUE);
          if (newOptionConst !== NO_VALUE && newOptionConst !== formValue) {
            removeOldSchemaData[key] = oldOptionConst === formValue ? newOptionConst : void 0;
          }
        }
      }
    });
    newFormData = {
      ...typeof data == "string" || Array.isArray(data) ? void 0 : data,
      ...removeOldSchemaData,
      ...nestedData
    };
  } else if (get_default(oldSchema, "type") === "array" && get_default(newSchema, "type") === "array" && Array.isArray(data)) {
    let oldSchemaItems = get_default(oldSchema, "items");
    let newSchemaItems = get_default(newSchema, "items");
    if (typeof oldSchemaItems === "object" && typeof newSchemaItems === "object" && !Array.isArray(oldSchemaItems) && !Array.isArray(newSchemaItems)) {
      if (has_default(oldSchemaItems, REF_KEY)) {
        oldSchemaItems = retrieveSchema(validator, oldSchemaItems, rootSchema, data, experimental_customMergeAllOf);
      }
      if (has_default(newSchemaItems, REF_KEY)) {
        newSchemaItems = retrieveSchema(validator, newSchemaItems, rootSchema, data, experimental_customMergeAllOf);
      }
      const oldSchemaType = get_default(oldSchemaItems, "type");
      const newSchemaType = get_default(newSchemaItems, "type");
      if (!oldSchemaType || oldSchemaType === newSchemaType) {
        const maxItems = get_default(newSchema, "maxItems", -1);
        if (newSchemaType === "object") {
          newFormData = data.reduce((newValue, aValue) => {
            const itemValue = sanitizeDataForNewSchema(validator, rootSchema, newSchemaItems, oldSchemaItems, aValue, experimental_customMergeAllOf);
            if (itemValue !== void 0 && (maxItems < 0 || newValue.length < maxItems)) {
              newValue.push(itemValue);
            }
            return newValue;
          }, []);
        } else {
          newFormData = maxItems > 0 && data.length > maxItems ? data.slice(0, maxItems) : data;
        }
      }
    } else if (typeof oldSchemaItems === "boolean" && typeof newSchemaItems === "boolean" && oldSchemaItems === newSchemaItems) {
      newFormData = data;
    }
  }
  return newFormData;
}

// node_modules/@rjsf/utils/lib/schema/toIdSchema.js
function toIdSchemaInternal(validator, schema, idPrefix, idSeparator, id, rootSchema, formData, _recurseList = [], experimental_customMergeAllOf) {
  const $id = id || idPrefix;
  const idSchema = { $id };
  if (typeof schema === "object") {
    if (REF_KEY in schema || DEPENDENCIES_KEY in schema || ALL_OF_KEY in schema) {
      const _schema = retrieveSchema(validator, schema, rootSchema, formData, experimental_customMergeAllOf);
      const sameSchemaIndex = _recurseList.findIndex((item) => deepEquals(item, _schema));
      if (sameSchemaIndex === -1) {
        return toIdSchemaInternal(validator, _schema, idPrefix, idSeparator, id, rootSchema, formData, _recurseList.concat(_schema), experimental_customMergeAllOf);
      }
    }
    if (ITEMS_KEY in schema && !get_default(schema, [ITEMS_KEY, REF_KEY])) {
      return toIdSchemaInternal(validator, get_default(schema, ITEMS_KEY), idPrefix, idSeparator, id, rootSchema, formData, _recurseList, experimental_customMergeAllOf);
    }
    if (getSchemaType(schema) === "object" && PROPERTIES_KEY in schema) {
      for (const name in schema.properties) {
        const field = schema[PROPERTIES_KEY][name];
        const fieldId = idSchema[ID_KEY] + idSeparator + name;
        idSchema[name] = toIdSchemaInternal(
          validator,
          field,
          idPrefix,
          idSeparator,
          fieldId,
          rootSchema,
          // It's possible that formData is not an object -- this can happen if an
          // array item has just been added, but not populated with data yet
          get_default(formData, [name]),
          _recurseList,
          experimental_customMergeAllOf
        );
      }
    }
  }
  return idSchema;
}
function toIdSchema(validator, schema, id, rootSchema, formData, idPrefix = "root", idSeparator = "_", experimental_customMergeAllOf) {
  return toIdSchemaInternal(validator, schema, idPrefix, idSeparator, id, rootSchema, formData, void 0, experimental_customMergeAllOf);
}

// node_modules/@rjsf/utils/lib/schema/toPathSchema.js
function toPathSchemaInternal(validator, schema, name, rootSchema, formData, _recurseList = [], experimental_customMergeAllOf) {
  if (REF_KEY in schema || DEPENDENCIES_KEY in schema || ALL_OF_KEY in schema) {
    const _schema = retrieveSchema(validator, schema, rootSchema, formData, experimental_customMergeAllOf);
    const sameSchemaIndex = _recurseList.findIndex((item) => deepEquals(item, _schema));
    if (sameSchemaIndex === -1) {
      return toPathSchemaInternal(validator, _schema, name, rootSchema, formData, _recurseList.concat(_schema), experimental_customMergeAllOf);
    }
  }
  let pathSchema = {
    [NAME_KEY]: name.replace(/^\./, "")
  };
  if (ONE_OF_KEY in schema || ANY_OF_KEY in schema) {
    const xxxOf = ONE_OF_KEY in schema ? schema.oneOf : schema.anyOf;
    const discriminator = getDiscriminatorFieldFromSchema(schema);
    const index = getClosestMatchingOption(validator, rootSchema, formData, xxxOf, 0, discriminator, experimental_customMergeAllOf);
    const _schema = xxxOf[index];
    pathSchema = {
      ...pathSchema,
      ...toPathSchemaInternal(validator, _schema, name, rootSchema, formData, _recurseList, experimental_customMergeAllOf)
    };
  }
  if (ADDITIONAL_PROPERTIES_KEY in schema && schema[ADDITIONAL_PROPERTIES_KEY] !== false) {
    set_default(pathSchema, RJSF_ADDITIONAL_PROPERTIES_FLAG, true);
  }
  if (ITEMS_KEY in schema && Array.isArray(formData)) {
    const { items: schemaItems, additionalItems: schemaAdditionalItems } = schema;
    if (Array.isArray(schemaItems)) {
      formData.forEach((element, i) => {
        if (schemaItems[i]) {
          pathSchema[i] = toPathSchemaInternal(validator, schemaItems[i], `${name}.${i}`, rootSchema, element, _recurseList, experimental_customMergeAllOf);
        } else if (schemaAdditionalItems) {
          pathSchema[i] = toPathSchemaInternal(validator, schemaAdditionalItems, `${name}.${i}`, rootSchema, element, _recurseList, experimental_customMergeAllOf);
        } else {
          console.warn(`Unable to generate path schema for "${name}.${i}". No schema defined for it`);
        }
      });
    } else {
      formData.forEach((element, i) => {
        pathSchema[i] = toPathSchemaInternal(validator, schemaItems, `${name}.${i}`, rootSchema, element, _recurseList, experimental_customMergeAllOf);
      });
    }
  } else if (PROPERTIES_KEY in schema) {
    for (const property2 in schema.properties) {
      const field = get_default(schema, [PROPERTIES_KEY, property2], {});
      pathSchema[property2] = toPathSchemaInternal(
        validator,
        field,
        `${name}.${property2}`,
        rootSchema,
        // It's possible that formData is not an object -- this can happen if an
        // array item has just been added, but not populated with data yet
        get_default(formData, [property2]),
        _recurseList,
        experimental_customMergeAllOf
      );
    }
  }
  return pathSchema;
}
function toPathSchema(validator, schema, name = "", rootSchema, formData, experimental_customMergeAllOf) {
  return toPathSchemaInternal(validator, schema, name, rootSchema, formData, void 0, experimental_customMergeAllOf);
}

// node_modules/@rjsf/utils/lib/createSchemaUtils.js
var SchemaUtils = class {
  /** Constructs the `SchemaUtils` instance with the given `validator` and `rootSchema` stored as instance variables
   *
   * @param validator - An implementation of the `ValidatorType` interface that will be forwarded to all the APIs
   * @param rootSchema - The root schema that will be forwarded to all the APIs
   * @param experimental_defaultFormStateBehavior - Configuration flags to allow users to override default form state behavior
   * @param [experimental_customMergeAllOf] - Optional function that allows for custom merging of `allOf` schemas
   */
  constructor(validator, rootSchema, experimental_defaultFormStateBehavior, experimental_customMergeAllOf) {
    this.rootSchema = rootSchema;
    this.validator = validator;
    this.experimental_defaultFormStateBehavior = experimental_defaultFormStateBehavior;
    this.experimental_customMergeAllOf = experimental_customMergeAllOf;
  }
  /** Returns the `ValidatorType` in the `SchemaUtilsType`
   *
   * @returns - The `ValidatorType`
   */
  getValidator() {
    return this.validator;
  }
  /** Determines whether either the `validator` and `rootSchema` differ from the ones associated with this instance of
   * the `SchemaUtilsType`. If either `validator` or `rootSchema` are falsy, then return false to prevent the creation
   * of a new `SchemaUtilsType` with incomplete properties.
   *
   * @param validator - An implementation of the `ValidatorType` interface that will be compared against the current one
   * @param rootSchema - The root schema that will be compared against the current one
   * @param [experimental_defaultFormStateBehavior] Optional configuration object, if provided, allows users to override default form state behavior
   * @param [experimental_customMergeAllOf] - Optional function that allows for custom merging of `allOf` schemas
   * @returns - True if the `SchemaUtilsType` differs from the given `validator` or `rootSchema`
   */
  doesSchemaUtilsDiffer(validator, rootSchema, experimental_defaultFormStateBehavior = {}, experimental_customMergeAllOf) {
    if (!validator || !rootSchema) {
      return false;
    }
    return this.validator !== validator || !deepEquals(this.rootSchema, rootSchema) || !deepEquals(this.experimental_defaultFormStateBehavior, experimental_defaultFormStateBehavior) || this.experimental_customMergeAllOf !== experimental_customMergeAllOf;
  }
  /** Finds the field specified by the `path` within the root or recursed `schema`. If there is no field for the specified
   * `path`, then the default `{ field: undefined, isRequired: undefined }` is returned. It determines whether a leaf
   * field is in the `required` list for its parent and if so, it is marked as required on return.
   *
   * @param schema - The current node within the JSON schema
   * @param path - The remaining keys in the path to the desired field
   * @param [formData] - The form data that is used to determine which oneOf option
   * @returns - An object that contains the field and its required state. If no field can be found then
   *            `{ field: undefined, isRequired: undefined }` is returned.
   */
  findFieldInSchema(schema, path, formData) {
    return findFieldInSchema(this.validator, this.rootSchema, schema, path, formData, this.experimental_customMergeAllOf);
  }
  /** Finds the oneOf option inside the `schema['any/oneOf']` list which has the `properties[selectorField].default` that
   * matches the `formData[selectorField]` value. For the purposes of this function, `selectorField` is either
   * `schema.discriminator.propertyName` or `fallbackField`.
   *
   * @param schema - The schema element in which to search for the selected oneOf option
   * @param fallbackField - The field to use as a backup selector field if the schema does not have a required field
   * @param xxx - Either `oneOf` or `anyOf`, defines which value is being sought
   * @param [formData={}] - The form data that is used to determine which oneOf option
   * @returns - The anyOf/oneOf option that matches the selector field in the schema or undefined if nothing is selected
   */
  findSelectedOptionInXxxOf(schema, fallbackField, xxx, formData) {
    return findSelectedOptionInXxxOf(this.validator, this.rootSchema, schema, fallbackField, xxx, formData, this.experimental_customMergeAllOf);
  }
  /** Returns the superset of `formData` that includes the given set updated to include any missing fields that have
   * computed to have defaults provided in the `schema`.
   *
   * @param schema - The schema for which the default state is desired
   * @param [formData] - The current formData, if any, onto which to provide any missing defaults
   * @param [includeUndefinedValues=false] - Optional flag, if true, cause undefined values to be added as defaults.
   *          If "excludeObjectChildren", pass `includeUndefinedValues` as false when computing defaults for any nested
   *          object properties.
   * @returns - The resulting `formData` with all the defaults provided
   */
  getDefaultFormState(schema, formData, includeUndefinedValues = false) {
    return getDefaultFormState(this.validator, schema, formData, this.rootSchema, includeUndefinedValues, this.experimental_defaultFormStateBehavior, this.experimental_customMergeAllOf);
  }
  /** Determines whether the combination of `schema` and `uiSchema` properties indicates that the label for the `schema`
   * should be displayed in a UI.
   *
   * @param schema - The schema for which the display label flag is desired
   * @param [uiSchema] - The UI schema from which to derive potentially displayable information
   * @param [globalOptions={}] - The optional Global UI Schema from which to get any fallback `xxx` options
   * @returns - True if the label should be displayed or false if it should not
   */
  getDisplayLabel(schema, uiSchema, globalOptions) {
    return getDisplayLabel(this.validator, schema, uiSchema, this.rootSchema, globalOptions, this.experimental_customMergeAllOf);
  }
  /** Determines which of the given `options` provided most closely matches the `formData`.
   * Returns the index of the option that is valid and is the closest match, or 0 if there is no match.
   *
   * The closest match is determined using the number of matching properties, and more heavily favors options with
   * matching readOnly, default, or const values.
   *
   * @param formData - The form data associated with the schema
   * @param options - The list of options that can be selected from
   * @param [selectedOption] - The index of the currently selected option, defaulted to -1 if not specified
   * @param [discriminatorField] - The optional name of the field within the options object whose value is used to
   *          determine which option is selected
   * @returns - The index of the option that is the closest match to the `formData` or the `selectedOption` if no match
   */
  getClosestMatchingOption(formData, options, selectedOption, discriminatorField) {
    return getClosestMatchingOption(this.validator, this.rootSchema, formData, options, selectedOption, discriminatorField, this.experimental_customMergeAllOf);
  }
  /** Given the `formData` and list of `options`, attempts to find the index of the first option that matches the data.
   * Always returns the first option if there is nothing that matches.
   *
   * @param formData - The current formData, if any, used to figure out a match
   * @param options - The list of options to find a matching options from
   * @param [discriminatorField] - The optional name of the field within the options object whose value is used to
   *          determine which option is selected
   * @returns - The firstindex of the matched option or 0 if none is available
   */
  getFirstMatchingOption(formData, options, discriminatorField) {
    return getFirstMatchingOption(this.validator, formData, options, this.rootSchema, discriminatorField);
  }
  getFromSchema(schema, path, defaultValue) {
    return getFromSchema(
      this.validator,
      this.rootSchema,
      schema,
      path,
      // @ts-expect-error TS2769: No overload matches this call
      defaultValue,
      this.experimental_customMergeAllOf
    );
  }
  /** Checks to see if the `schema` and `uiSchema` combination represents an array of files
   *
   * @param schema - The schema for which check for array of files flag is desired
   * @param [uiSchema] - The UI schema from which to check the widget
   * @returns - True if schema/uiSchema contains an array of files, otherwise false
   */
  isFilesArray(schema, uiSchema) {
    return isFilesArray(this.validator, schema, uiSchema, this.rootSchema, this.experimental_customMergeAllOf);
  }
  /** Checks to see if the `schema` combination represents a multi-select
   *
   * @param schema - The schema for which check for a multi-select flag is desired
   * @returns - True if schema contains a multi-select, otherwise false
   */
  isMultiSelect(schema) {
    return isMultiSelect(this.validator, schema, this.rootSchema, this.experimental_customMergeAllOf);
  }
  /** Checks to see if the `schema` combination represents a select
   *
   * @param schema - The schema for which check for a select flag is desired
   * @returns - True if schema contains a select, otherwise false
   */
  isSelect(schema) {
    return isSelect(this.validator, schema, this.rootSchema, this.experimental_customMergeAllOf);
  }
  /** Retrieves an expanded schema that has had all of its conditions, additional properties, references and
   * dependencies resolved and merged into the `schema` given a `rawFormData` that is used to do the potentially
   * recursive resolution.
   *
   * @param schema - The schema for which retrieving a schema is desired
   * @param [rawFormData] - The current formData, if any, to assist retrieving a schema
   * @returns - The schema having its conditions, additional properties, references and dependencies resolved
   */
  retrieveSchema(schema, rawFormData) {
    return retrieveSchema(this.validator, schema, this.rootSchema, rawFormData, this.experimental_customMergeAllOf);
  }
  /** Sanitize the `data` associated with the `oldSchema` so it is considered appropriate for the `newSchema`. If the
   * new schema does not contain any properties, then `undefined` is returned to clear all the form data. Due to the
   * nature of schemas, this sanitization happens recursively for nested objects of data. Also, any properties in the
   * old schemas that are non-existent in the new schema are set to `undefined`.
   *
   * @param [newSchema] - The new schema for which the data is being sanitized
   * @param [oldSchema] - The old schema from which the data originated
   * @param [data={}] - The form data associated with the schema, defaulting to an empty object when undefined
   * @returns - The new form data, with all the fields uniquely associated with the old schema set
   *      to `undefined`. Will return `undefined` if the new schema is not an object containing properties.
   */
  sanitizeDataForNewSchema(newSchema, oldSchema, data) {
    return sanitizeDataForNewSchema(this.validator, this.rootSchema, newSchema, oldSchema, data, this.experimental_customMergeAllOf);
  }
  /** Generates an `IdSchema` object for the `schema`, recursively
   *
   * @param schema - The schema for which the display label flag is desired
   * @param [id] - The base id for the schema
   * @param [formData] - The current formData, if any, onto which to provide any missing defaults
   * @param [idPrefix='root'] - The prefix to use for the id
   * @param [idSeparator='_'] - The separator to use for the path segments in the id
   * @returns - The `IdSchema` object for the `schema`
   */
  toIdSchema(schema, id, formData, idPrefix = "root", idSeparator = "_") {
    return toIdSchema(this.validator, schema, id, this.rootSchema, formData, idPrefix, idSeparator, this.experimental_customMergeAllOf);
  }
  /** Generates an `PathSchema` object for the `schema`, recursively
   *
   * @param schema - The schema for which the display label flag is desired
   * @param [name] - The base name for the schema
   * @param [formData] - The current formData, if any, onto which to provide any missing defaults
   * @returns - The `PathSchema` object for the `schema`
   */
  toPathSchema(schema, name, formData) {
    return toPathSchema(this.validator, schema, name, this.rootSchema, formData, this.experimental_customMergeAllOf);
  }
};
function createSchemaUtils(validator, rootSchema, experimental_defaultFormStateBehavior = {}, experimental_customMergeAllOf) {
  return new SchemaUtils(validator, rootSchema, experimental_defaultFormStateBehavior, experimental_customMergeAllOf);
}

export {
  isObject,
  allowAdditionalItems,
  asNumber,
  ADDITIONAL_PROPERTY_FLAG,
  ANY_OF_KEY,
  CONST_KEY,
  DEFAULT_KEY,
  ERRORS_KEY,
  ID_KEY,
  ITEMS_KEY,
  JUNK_OPTION_ID,
  NAME_KEY,
  ONE_OF_KEY,
  PROPERTIES_KEY,
  READONLY_KEY,
  SUBMIT_BTN_OPTIONS_KEY,
  REF_KEY,
  RJSF_ADDITIONAL_PROPERTIES_FLAG,
  ROOT_SCHEMA_PREFIX,
  UI_OPTIONS_KEY,
  UI_GLOBAL_OPTIONS_KEY,
  getUiOptions,
  canExpand,
  isPlainObject_default,
  createErrorHandler,
  isObject_default,
  isFunction_default,
  SetCache_default,
  cacheHas_default,
  baseUnary_default,
  isArrayLike_default,
  keys_default,
  deepEquals,
  arrayMap_default,
  get_default,
  has_default,
  isEqual_default,
  set_default,
  toInteger_default,
  hasIn_default,
  isArrayLikeObject_default,
  baseRest_default,
  baseIndexOf_default,
  arrayIncludes_default,
  arrayIncludesWith_default,
  noop_default,
  baseUnset_default,
  flatten_default,
  flatRest_default,
  omit_default,
  isEmpty_default,
  require_fast_uri,
  isString_default,
  getDiscriminatorFieldFromSchema,
  getSchemaType,
  mergeSchemas,
  retrieveSchema,
  isFixedItems,
  isNil_default,
  mergeObjects,
  optionsList,
  getDefaultFormState,
  isCustomWidget,
  createSchemaUtils,
  dataURItoBlob,
  dateRangeOptions,
  englishStringTranslator,
  enumOptionsValueForIndex,
  enumOptionsDeselectValue,
  enumOptionsIsSelected,
  enumOptionsIndexForValue,
  enumOptionsSelectValue,
  cloneDeep_default,
  getDateElementProps,
  getInputProps,
  getSubmitButtonOptions,
  getTemplate,
  nanoid,
  getTestIds,
  getWidget,
  hashObject,
  hashForSchema,
  hasWidget,
  descriptionId,
  errorId,
  examplesId,
  helpId,
  titleId,
  ariaDescribedByIds,
  optionId,
  buttonId,
  labelValue,
  localToUTC,
  lookupFromFormContext,
  orderProperties,
  parseDateString,
  schemaRequiresTrueValue,
  shouldRender,
  toDateString,
  toErrorList,
  toPath_default,
  toErrorSchema,
  unwrapErrorHandler,
  utcToLocal,
  validationDataMerge,
  withIdRefPrefix,
  basePickBy_default,
  getChangedFields,
  TranslatableString,
  forEach_default
};
/*! Bundled license information:

react-is/cjs/react-is.development.js:
  (**
   * @license React
   * react-is.development.js
   *
   * Copyright (c) Facebook, Inc. and its affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)
*/
//# sourceMappingURL=chunk-6WCUV5VP.js.map
