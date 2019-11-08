//
// Copyright (c) ZeroC, Inc. All rights reserved.
//
//
// Ice version 3.7.3
//
// <auto-generated>
//
// Generated from file `Connection.ice'
//
// Warning: do not edit this file.
//
// </auto-generated>
//

import Foundation
import PromiseKit

/// The batch compression option when flushing queued batch requests.
public enum CompressBatch: Swift.UInt8 {
    /// Yes Compress the batch requests.
    case Yes = 0
    /// No Don't compress the batch requests.
    case No = 1
    /// BasedOnProxy Compress the batch requests if at least one request was
    /// made on a compressed proxy.
    case BasedOnProxy = 2
    public init() {
        self = .Yes
    }
}

/// An `Ice.InputStream` extension to read `CompressBatch` enumerated values from the stream.
public extension InputStream {
    /// Read an enumerated value.
    ///
    /// - returns: `CompressBatch` - The enumarated value.
    func read() throws -> CompressBatch {
        let rawValue: Swift.UInt8 = try read(enumMaxValue: 2)
        guard let val = CompressBatch(rawValue: rawValue) else {
            throw MarshalException(reason: "invalid enum value")
        }
        return val
    }

    /// Read an optional enumerated value from the stream.
    ///
    /// - parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// - returns: `CompressBatch` - The enumerated value.
    func read(tag: Swift.Int32) throws -> CompressBatch? {
        guard try readOptional(tag: tag, expectedFormat: .Size) else {
            return nil
        }
        return try read() as CompressBatch
    }
}

/// An `Ice.OutputStream` extension to write `CompressBatch` enumerated values to the stream.
public extension OutputStream {
    /// Writes an enumerated value to the stream.
    ///
    /// parameter _: `CompressBatch` - The enumerator to write.
    func write(_ v: CompressBatch) {
        write(enum: v.rawValue, maxValue: 2)
    }

    /// Writes an optional enumerated value to the stream.
    ///
    /// parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// parameter _: `CompressBatch` - The enumerator to write.
    func write(tag: Swift.Int32, value: CompressBatch?) {
        guard let v = value else {
            return
        }
        write(tag: tag, val: v.rawValue, maxValue: 2)
    }
}

/// Specifies the close semantics for Active Connection Management.
public enum ACMClose: Swift.UInt8 {
    /// CloseOff Disables automatic connection closure.
    case CloseOff = 0
    /// CloseOnIdle Gracefully closes a connection that has been idle for the configured timeout period.
    case CloseOnIdle = 1
    /// CloseOnInvocation Forcefully closes a connection that has been idle for the configured timeout period,
    /// but only if the connection has pending invocations.
    case CloseOnInvocation = 2
    /// CloseOnInvocationAndIdle Combines the behaviors of CloseOnIdle and CloseOnInvocation.
    case CloseOnInvocationAndIdle = 3
    /// CloseOnIdleForceful Forcefully closes a connection that has been idle for the configured timeout period,
    /// regardless of whether the connection has pending invocations or dispatch.
    case CloseOnIdleForceful = 4
    public init() {
        self = .CloseOff
    }
}

/// An `Ice.InputStream` extension to read `ACMClose` enumerated values from the stream.
public extension InputStream {
    /// Read an enumerated value.
    ///
    /// - returns: `ACMClose` - The enumarated value.
    func read() throws -> ACMClose {
        let rawValue: Swift.UInt8 = try read(enumMaxValue: 4)
        guard let val = ACMClose(rawValue: rawValue) else {
            throw MarshalException(reason: "invalid enum value")
        }
        return val
    }

    /// Read an optional enumerated value from the stream.
    ///
    /// - parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// - returns: `ACMClose` - The enumerated value.
    func read(tag: Swift.Int32) throws -> ACMClose? {
        guard try readOptional(tag: tag, expectedFormat: .Size) else {
            return nil
        }
        return try read() as ACMClose
    }
}

/// An `Ice.OutputStream` extension to write `ACMClose` enumerated values to the stream.
public extension OutputStream {
    /// Writes an enumerated value to the stream.
    ///
    /// parameter _: `ACMClose` - The enumerator to write.
    func write(_ v: ACMClose) {
        write(enum: v.rawValue, maxValue: 4)
    }

    /// Writes an optional enumerated value to the stream.
    ///
    /// parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// parameter _: `ACMClose` - The enumerator to write.
    func write(tag: Swift.Int32, value: ACMClose?) {
        guard let v = value else {
            return
        }
        write(tag: tag, val: v.rawValue, maxValue: 4)
    }
}

/// Specifies the heartbeat semantics for Active Connection Management.
public enum ACMHeartbeat: Swift.UInt8 {
    /// HeartbeatOff Disables heartbeats.
    case HeartbeatOff = 0
    /// HeartbeatOnDispatch Send a heartbeat at regular intervals if the connection is
    /// idle and only if there are pending dispatch.
    case HeartbeatOnDispatch = 1
    /// HeartbeatOnIdle Send a heartbeat at regular intervals when the connection is idle.
    case HeartbeatOnIdle = 2
    /// HeartbeatAlways Send a heartbeat at regular intervals until the connection is closed.
    case HeartbeatAlways = 3
    public init() {
        self = .HeartbeatOff
    }
}

/// An `Ice.InputStream` extension to read `ACMHeartbeat` enumerated values from the stream.
public extension InputStream {
    /// Read an enumerated value.
    ///
    /// - returns: `ACMHeartbeat` - The enumarated value.
    func read() throws -> ACMHeartbeat {
        let rawValue: Swift.UInt8 = try read(enumMaxValue: 3)
        guard let val = ACMHeartbeat(rawValue: rawValue) else {
            throw MarshalException(reason: "invalid enum value")
        }
        return val
    }

    /// Read an optional enumerated value from the stream.
    ///
    /// - parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// - returns: `ACMHeartbeat` - The enumerated value.
    func read(tag: Swift.Int32) throws -> ACMHeartbeat? {
        guard try readOptional(tag: tag, expectedFormat: .Size) else {
            return nil
        }
        return try read() as ACMHeartbeat
    }
}

/// An `Ice.OutputStream` extension to write `ACMHeartbeat` enumerated values to the stream.
public extension OutputStream {
    /// Writes an enumerated value to the stream.
    ///
    /// parameter _: `ACMHeartbeat` - The enumerator to write.
    func write(_ v: ACMHeartbeat) {
        write(enum: v.rawValue, maxValue: 3)
    }

    /// Writes an optional enumerated value to the stream.
    ///
    /// parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// parameter _: `ACMHeartbeat` - The enumerator to write.
    func write(tag: Swift.Int32, value: ACMHeartbeat?) {
        guard let v = value else {
            return
        }
        write(tag: tag, val: v.rawValue, maxValue: 3)
    }
}

/// A collection of Active Connection Management configuration settings.
public struct ACM: Swift.Hashable {
    /// A timeout value in seconds.
    public var timeout: Swift.Int32 = 0
    /// The close semantics.
    public var close: ACMClose = .CloseOff
    /// The heartbeat semantics.
    public var heartbeat: ACMHeartbeat = .HeartbeatOff

    public init() {}

    public init(timeout: Swift.Int32, close: ACMClose, heartbeat: ACMHeartbeat) {
        self.timeout = timeout
        self.close = close
        self.heartbeat = heartbeat
    }
}

/// Determines the behavior when manually closing a connection.
public enum ConnectionClose: Swift.UInt8 {
    /// Forcefully Close the connection immediately without sending a close connection protocol message to the peer
    /// and waiting for the peer to acknowledge it.
    case Forcefully = 0
    /// Gracefully Close the connection by notifying the peer but do not wait for pending outgoing invocations
    /// to complete. On the server side, the connection will not be closed until all incoming invocations have
    /// completed.
    case Gracefully = 1
    /// GracefullyWithWait Wait for all pending invocations to complete before closing the connection.
    case GracefullyWithWait = 2
    public init() {
        self = .Forcefully
    }
}

/// An `Ice.InputStream` extension to read `ConnectionClose` enumerated values from the stream.
public extension InputStream {
    /// Read an enumerated value.
    ///
    /// - returns: `ConnectionClose` - The enumarated value.
    func read() throws -> ConnectionClose {
        let rawValue: Swift.UInt8 = try read(enumMaxValue: 2)
        guard let val = ConnectionClose(rawValue: rawValue) else {
            throw MarshalException(reason: "invalid enum value")
        }
        return val
    }

    /// Read an optional enumerated value from the stream.
    ///
    /// - parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// - returns: `ConnectionClose` - The enumerated value.
    func read(tag: Swift.Int32) throws -> ConnectionClose? {
        guard try readOptional(tag: tag, expectedFormat: .Size) else {
            return nil
        }
        return try read() as ConnectionClose
    }
}

/// An `Ice.OutputStream` extension to write `ConnectionClose` enumerated values to the stream.
public extension OutputStream {
    /// Writes an enumerated value to the stream.
    ///
    /// parameter _: `ConnectionClose` - The enumerator to write.
    func write(_ v: ConnectionClose) {
        write(enum: v.rawValue, maxValue: 2)
    }

    /// Writes an optional enumerated value to the stream.
    ///
    /// parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// parameter _: `ConnectionClose` - The enumerator to write.
    func write(tag: Swift.Int32, value: ConnectionClose?) {
        guard let v = value else {
            return
        }
        write(tag: tag, val: v.rawValue, maxValue: 2)
    }
}

/// A collection of HTTP headers.
public typealias HeaderDict = [Swift.String: Swift.String]

/// Helper class to read and write `HeaderDict` dictionary values from
/// `Ice.InputStream` and `Ice.OutputStream`.
public struct HeaderDictHelper {
    /// Read a `HeaderDict` dictionary from the stream.
    ///
    /// - parameter istr: `Ice.InputStream` - The stream to read from.
    ///
    /// - returns: `HeaderDict` - The dictionary read from the stream.
    public static func read(from istr: InputStream) throws -> HeaderDict {
        let sz = try Swift.Int(istr.readSize())
        var v = HeaderDict()
        for _ in 0 ..< sz {
            let key: Swift.String = try istr.read()
            let value: Swift.String = try istr.read()
            v[key] = value
        }
        return v
    }

    /// Read an optional `HeaderDict?` dictionary from the stream.
    ///
    /// - parameter istr: `Ice.InputStream` - The stream to read from.
    ///
    /// - parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// - returns: `HeaderDict` - The dictionary read from the stream.
    public static func read(from istr: InputStream, tag: Swift.Int32) throws -> HeaderDict? {
        guard try istr.readOptional(tag: tag, expectedFormat: .FSize) else {
            return nil
        }
        try istr.skip(4)
        return try read(from: istr)
    }

    /// Wite a `HeaderDict` dictionary to the stream.
    ///
    /// - parameter ostr: `Ice.OuputStream` - The stream to write to.
    ///
    /// - parameter value: `HeaderDict` - The dictionary value to write to the stream.
    public static func write(to ostr: OutputStream, value v: HeaderDict) {
        ostr.write(size: v.count)
        for (key, value) in v {
            ostr.write(key)
            ostr.write(value)
        }
    }

    /// Wite an optional `HeaderDict?` dictionary to the stream.
    ///
    /// - parameter ostr: `Ice.OuputStream` - The stream to write to.
    ///
    /// - parameter tag: `Int32` - The numeric tag associated with the value.
    ///
    /// - parameter value: `HeaderDict` - The dictionary value to write to the stream.
    public static func write(to ostr: OutputStream, tag: Swift.Int32, value v: HeaderDict?) {
        guard let val = v else {
            return
        }
        if ostr.writeOptional(tag: tag, format: .FSize) {
            let pos = ostr.startSize()
            write(to: ostr, value: val)
            ostr.endSize(position: pos)
        }
    }
}

/// Base class providing access to the connection details.
public protocol ConnectionInfo: Swift.AnyObject {
    /// The information of the underyling transport or null if there's
    /// no underlying transport.
    var underlying: ConnectionInfo? { get set }
    /// Whether or not the connection is an incoming or outgoing
    /// connection.
    var incoming: Swift.Bool { get set }
    /// The name of the adapter associated with the connection.
    var adapterName: Swift.String { get set }
    /// The connection id.
    var connectionId: Swift.String { get set }
}

/// An application can implement this interface to receive notifications when
/// a connection closes.
///
/// This method is called by the the connection when the connection
/// is closed. If the callback needs more information about the closure,
/// it can call Connection.throwException.
///
/// - parameter _: `Connection?` The connection that closed.
public typealias CloseCallback = (Connection?) -> Swift.Void

/// An application can implement this interface to receive notifications when
/// a connection receives a heartbeat message.
///
/// This method is called by the the connection when a heartbeat is
/// received from the peer.
///
/// - parameter _: `Connection?` The connection on which a heartbeat was received.
public typealias HeartbeatCallback = (Connection?) -> Swift.Void

/// The user-level interface to a connection.
public protocol Connection: Swift.AnyObject, Swift.CustomStringConvertible {
    /// Manually close the connection using the specified closure mode.
    ///
    /// - parameter _: `ConnectionClose` Determines how the connection will be closed.
    func close(_ mode: ConnectionClose) throws

    /// Create a special proxy that always uses this connection. This
    /// can be used for callbacks from a server to a client if the
    /// server cannot directly establish a connection to the client,
    /// for example because of firewalls. In this case, the server
    /// would create a proxy using an already established connection
    /// from the client.
    ///
    /// - parameter _: `Identity` The identity for which a proxy is to be created.
    ///
    /// - returns: `ObjectPrx` - A proxy that matches the given identity and uses this
    /// connection.
    func createProxy(_ id: Identity) throws -> ObjectPrx

    /// Explicitly set an object adapter that dispatches requests that
    /// are received over this connection. A client can invoke an
    /// operation on a server using a proxy, and then set an object
    /// adapter for the outgoing connection that is used by the proxy
    /// in order to receive callbacks. This is useful if the server
    /// cannot establish a connection back to the client, for example
    /// because of firewalls.
    ///
    /// - parameter _: `ObjectAdapter?` The object adapter that should be used by this
    /// connection to dispatch requests. The object adapter must be
    /// activated. When the object adapter is deactivated, it is
    /// automatically removed from the connection. Attempts to use a
    /// deactivated object adapter raise ObjectAdapterDeactivatedException
    func setAdapter(_ adapter: ObjectAdapter?) throws

    /// Get the object adapter that dispatches requests for this
    /// connection.
    ///
    /// - returns: `ObjectAdapter?` - The object adapter that dispatches requests for the
    /// connection, or null if no adapter is set.
    func getAdapter() -> ObjectAdapter?

    /// Get the endpoint from which the connection was created.
    ///
    /// - returns: `Endpoint` - The endpoint from which the connection was created.
    func getEndpoint() -> Endpoint

    /// Flush any pending batch requests for this connection.
    /// This means all batch requests invoked on fixed proxies
    /// associated with the connection.
    ///
    /// - parameter _: `CompressBatch` Specifies whether or not the queued batch requests
    /// should be compressed before being sent over the wire.
    func flushBatchRequests(_ compress: CompressBatch) throws

    /// Flush any pending batch requests for this connection.
    /// This means all batch requests invoked on fixed proxies
    /// associated with the connection.
    ///
    /// - parameter _: `CompressBatch` Specifies whether or not the queued batch requests
    /// should be compressed before being sent over the wire.
    ///
    /// - parameter sentOn: `Dispatch.DispatchQueue?` - Optional dispatch queue used to
    ///   dispatch the sent callback.
    ///
    /// - parameter sentFlags: `Dispatch.DispatchWorkItemFlags?` - Optional dispatch flags used
    ///   to dispatch the sent callback
    ///
    /// - parameter sent: `((Swift.Bool) -> Swift.Void)` - Optional sent callback.
    ///
    /// - returns: `PromiseKit.Promise<>` - The result of the operation
    func flushBatchRequestsAsync(_ compress: CompressBatch, sentOn: Dispatch.DispatchQueue?,
                                 sentFlags: Dispatch.DispatchWorkItemFlags?,
                                 sent: ((Swift.Bool) -> Swift.Void)?) -> PromiseKit.Promise<Swift.Void>

    /// Set a close callback on the connection. The callback is called by the
    /// connection when it's closed. The callback is called from the
    /// Ice thread pool associated with the connection. If the callback needs
    /// more information about the closure, it can call Connection.throwException.
    ///
    /// - parameter _: `CloseCallback?` The close callback object.
    func setCloseCallback(_ callback: CloseCallback?) throws

    /// Set a heartbeat callback on the connection. The callback is called by the
    /// connection when a heartbeat is received. The callback is called
    /// from the Ice thread pool associated with the connection.
    ///
    /// - parameter _: `HeartbeatCallback?` The heartbeat callback object.
    func setHeartbeatCallback(_ callback: HeartbeatCallback?)

    /// Send a heartbeat message.
    func heartbeat() throws

    /// Send a heartbeat message.
    ///
    /// - parameter sentOn: `Dispatch.DispatchQueue?` - Optional dispatch queue used to
    ///   dispatch the sent callback.
    ///
    /// - parameter sentFlags: `Dispatch.DispatchWorkItemFlags?` - Optional dispatch flags used
    ///   to dispatch the sent callback
    ///
    /// - parameter sent: `((Swift.Bool) -> Swift.Void)` - Optional sent callback.
    ///
    /// - returns: `PromiseKit.Promise<>` - The result of the operation
    func heartbeatAsync(sentOn: Dispatch.DispatchQueue?, sentFlags: Dispatch.DispatchWorkItemFlags?,
                        sent: ((Swift.Bool) -> Swift.Void)?) -> PromiseKit.Promise<Swift.Void>

    /// Set the active connection management parameters.
    ///
    /// - parameter timeout: `Swift.Int32?` The timeout value in seconds, must be &gt;= 0.
    ///
    /// - parameter close: `ACMClose?` The close condition
    ///
    /// - parameter heartbeat: `ACMHeartbeat?` The hertbeat condition
    func setACM(timeout: Swift.Int32?, close: ACMClose?, heartbeat: ACMHeartbeat?)

    /// Get the ACM parameters.
    ///
    /// - returns: `ACM` - The ACM parameters.
    func getACM() -> ACM

    /// Return the connection type. This corresponds to the endpoint
    /// type, i.e., "tcp", "udp", etc.
    ///
    /// - returns: `Swift.String` - The type of the connection.
    func type() -> Swift.String

    /// Get the timeout for the connection.
    ///
    /// - returns: `Swift.Int32` - The connection's timeout.
    func timeout() -> Swift.Int32

    /// Return a description of the connection as human readable text,
    /// suitable for logging or error messages.
    ///
    /// - returns: `Swift.String` - The description of the connection as human readable
    /// text.
    func toString() -> Swift.String

    /// Returns the connection information.
    ///
    /// - returns: `ConnectionInfo` - The connection information.
    func getInfo() throws -> ConnectionInfo

    /// Set the connection buffer receive/send size.
    ///
    /// - parameter rcvSize: `Swift.Int32` The connection receive buffer size.
    ///
    /// - parameter sndSize: `Swift.Int32` The connection send buffer size.
    func setBufferSize(rcvSize: Swift.Int32, sndSize: Swift.Int32) throws

    /// Throw an exception indicating the reason for connection closure. For example,
    /// CloseConnectionException is raised if the connection was closed gracefully,
    /// whereas ConnectionManuallyClosedException is raised if the connection was
    /// manually closed by the application. This operation does nothing if the connection is
    /// not yet closed.
    func throwException() throws
}

/// Provides access to the connection details of an IP connection
public protocol IPConnectionInfo: ConnectionInfo {
    /// The local address.
    var localAddress: Swift.String { get set }
    /// The local port.
    var localPort: Swift.Int32 { get set }
    /// The remote address.
    var remoteAddress: Swift.String { get set }
    /// The remote port.
    var remotePort: Swift.Int32 { get set }
}

/// Provides access to the connection details of a TCP connection
public protocol TCPConnectionInfo: IPConnectionInfo {
    /// The connection buffer receive size.
    var rcvSize: Swift.Int32 { get set }
    /// The connection buffer send size.
    var sndSize: Swift.Int32 { get set }
}

/// Provides access to the connection details of a UDP connection
public protocol UDPConnectionInfo: IPConnectionInfo {
    /// The multicast address.
    var mcastAddress: Swift.String { get set }
    /// The multicast port.
    var mcastPort: Swift.Int32 { get set }
    /// The connection buffer receive size.
    var rcvSize: Swift.Int32 { get set }
    /// The connection buffer send size.
    var sndSize: Swift.Int32 { get set }
}

/// Provides access to the connection details of a WebSocket connection
public protocol WSConnectionInfo: ConnectionInfo {
    /// The headers from the HTTP upgrade request.
    var headers: HeaderDict { get set }
}
