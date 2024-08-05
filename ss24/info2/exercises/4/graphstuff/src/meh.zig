const std = @import("std");

pub const GraphError = error{NodeNotFound};

const Node = struct {
    label: []const u8,
    marked: bool = false,
    accepting: bool = false,
};

const Edge = struct {
    label: []const u8,
    src: *Node,
    dst: *Node,
};

/// Deterministic Finite Automaton
const Dfa = struct {
    nodes: std.StringHashMap(Node),
    edges: std.ArrayList(Edge),
    initialState: *Node,

    pub fn create(allocator: std.mem.Allocator) std.mem.Allocator.Error!Dfa {
        return .{ .nodes = std.StringHashMap(Node).init(allocator), .edges = std.ArrayList(Edge).init(allocator) };
    }

    pub fn deinit(self: *Dfa) void {
        self.edges.deinit();
        self.nodes.deinit();
    }

    pub fn addNode(self: *Dfa, node: Node) !*Node {
        const entry = try self.nodes.getOrPutValue(node.label, node);
        return entry.value_ptr;
    }

    pub fn addEdge(self: *Dfa, src: *Node, dst: *Node, label: []const u8) !void {
        if (!self.nodes.contains(src.label) or !self.nodes.contains(dst.label)) return GraphError.NodeNotFound;
        std.log.warn("creating {s}-[{s}]>{s}", .{ src.label, label, dst.label });
        try self.edges.append(Edge{ .label = label, .src = src, .dst = dst });
    }

    pub fn getNode(self: *Dfa, label: []const u8) !?*Node {
        return *self.nodes.get(label);
    }

    pub fn dfs(self: *Dfa, start: *Node, visit: fn (*Node) void) !void {
        var stack = std.ArrayList(*Node).init(std.heap.page_allocator);
        defer stack.deinit();

        try stack.append(start);
        while (stack.items.len > 0) {
            const node = stack.pop();
            if (node.marked) continue;
            visit(node);

            for (self.edges.items) |edge| {
                if (edge.src == node and !edge.dst.marked) {
                    try stack.append(edge.dst);
                }
            }
        }
    }

    pub fn traverse(start: *Node, visit: fn (*Node) void) !void {
        _ = visit;
        _ = start;
    }
};

fn exampleVisitNodeFunction(node: *Node) void {
    std.log.warn("Visited {s}, accepting: {s}\n", .{ node.label, if (node.accepting) "True" else "False" });
    node.marked = true;
}

pub fn main() !void {}

test "simple test" {
    const alloc = std.testing.allocator;

    var g = try Dfa.create(alloc);
    defer g.deinit();

    const q0 = try g.addNode(Node{ .label = "q0" });
    const q1 = try g.addNode(Node{ .label = "q1", .accepting = true });
    const q2 = try g.addNode(Node{ .label = "q2", .accepting = true });

    try g.addEdge(q0, q1, "a");
    try g.addEdge(q0, q2, "b");
    try g.addEdge(q0, q2, "b");
    try g.addEdge(q1, q1, "a");
    try g.addEdge(q1, q2, "b");
    try g.addEdge(q2, q0, "a");
    try g.addEdge(q2, q1, "b");

    try g.dfs(q0, exampleVisitNodeFunction);
}
