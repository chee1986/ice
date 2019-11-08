//
// Copyright (c) ZeroC, Inc. All rights reserved.
//
//
// Ice version 3.7.3
//
// <auto-generated>
//
// Generated from file `ConnectionInfo.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

/* eslint-disable */
/* jshint ignore: start */

/* slice2js browser-bundle-skip */
(function(module, require, exports)
{
/* slice2js browser-bundle-skip-end */
/* slice2js browser-bundle-skip */
    const _ModuleRegistry = require("../Ice/ModuleRegistry").Ice._ModuleRegistry;
    const Ice = _ModuleRegistry.require(module,
    [
        "../Ice/Object",
        "../Ice/Value",
        "../Ice/ObjectPrx",
        "../Ice/Long",
        "../Ice/HashMap",
        "../Ice/HashUtil",
        "../Ice/ArrayUtil",
        "../Ice/StreamHelpers",
        "../Ice/Connection"
    ]).Ice;

    const Slice = Ice.Slice;
/* slice2js browser-bundle-skip-end */
/* slice2js browser-bundle-skip */

    let IceSSL = _ModuleRegistry.module("IceSSL");
/* slice2js browser-bundle-skip-end */

    /**
     * Provides access to the connection details of an SSL connection
     *
     **/
    IceSSL.ConnectionInfo = class extends Ice.ConnectionInfo
    {
        constructor(underlying, incoming, adapterName, connectionId, cipher = "", certs = null, verified = false)
        {
            super(underlying, incoming, adapterName, connectionId);
            this.cipher = cipher;
            this.certs = certs;
            this.verified = verified;
        }
    };

/* slice2js browser-bundle-skip */
    exports.IceSSL = IceSSL;
/* slice2js browser-bundle-skip-end */
/* slice2js browser-bundle-skip */
}
(typeof(global) !== "undefined" && typeof(global.process) !== "undefined" ? module : undefined,
 typeof(global) !== "undefined" && typeof(global.process) !== "undefined" ? require :
 (typeof WorkerGlobalScope !== "undefined" && self instanceof WorkerGlobalScope) ? self.Ice._require : window.Ice._require,
 typeof(global) !== "undefined" && typeof(global.process) !== "undefined" ? exports :
 (typeof WorkerGlobalScope !== "undefined" && self instanceof WorkerGlobalScope) ? self : window));
/* slice2js browser-bundle-skip-end */
