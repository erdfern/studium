const std = @import("std");

/// Represents a state in the DFA.
pub const State = usize;

/// Represents an input symbol in the alphabet;
pub const Symbol = u8;

const StateTransition = struct { state: State, symbol: Symbol };

/// A DFA
pub const Dfa = struct { states: []State, alphabet: []Symbol, transitions: std.AutoHashMap(StateTransition, State), start_state: State, accept_states: []State };

/// Initialize a DFA
pub fn initDFA(symbols: []const Symbol, states: []State, start_state: State, accept_states: []State, allocator: *std.mem.Allocator) Dfa {
    return .{
        .alphabet = symbols,
        .states = states,
        .start_state = start_state,
        .accept_states = accept_states,
        .transitions = std.AutoHashMap(StateTransition, State).init(allocator),
    };
}

pub fn main() !void {}

test "simple test" {}
