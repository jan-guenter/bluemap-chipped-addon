/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.model;

import io.github.janguenter.bluemap.resource.athena.model.CubeFace;

import java.util.Map;

/** Exact persisted horizontal pane connection booleans. */
public record PaneConnections(boolean north, boolean east, boolean south, boolean west) {

    public static PaneConnections parse(Map<String, String> properties) {
        return new PaneConnections(
                exactBoolean(properties, "north"),
                exactBoolean(properties, "east"),
                exactBoolean(properties, "south"),
                exactBoolean(properties, "west")
        );
    }

    public boolean connected(CubeFace direction) {
        return switch (direction) {
            case NORTH -> north;
            case EAST -> east;
            case SOUTH -> south;
            case WEST -> west;
            default -> false;
        };
    }

    private static boolean exactBoolean(Map<String, String> properties, String name) {
        String value = properties.get(name);
        if ("true".equals(value)) {
            return true;
        }
        if ("false".equals(value)) {
            return false;
        }
        throw new IllegalArgumentException("pane property is missing or malformed: " + name);
    }
}
