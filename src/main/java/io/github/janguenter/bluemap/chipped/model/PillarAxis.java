/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.model;

import io.github.janguenter.bluemap.resource.athena.model.CubeFace;

/** Persisted pillar axis and its exact Athena first/second chain directions. */
public enum PillarAxis {
    X(new CubeFace.Vec(-1, 0, 0), new CubeFace.Vec(1, 0, 0)),
    Y(new CubeFace.Vec(0, 1, 0), new CubeFace.Vec(0, -1, 0)),
    Z(new CubeFace.Vec(0, 0, -1), new CubeFace.Vec(0, 0, 1));

    private final CubeFace.Vec first;
    private final CubeFace.Vec second;

    PillarAxis(CubeFace.Vec first, CubeFace.Vec second) {
        this.first = first;
        this.second = second;
    }

    public CubeFace.Vec first() {
        return first;
    }

    public CubeFace.Vec second() {
        return second;
    }

    public boolean isCap(CubeFace face) {
        CubeFace.Vec normal = face.normal();
        return switch (this) {
            case X -> normal.x() != 0;
            case Y -> normal.y() != 0;
            case Z -> normal.z() != 0;
        };
    }

    /** Clockwise quarter turns in the emitter's face-local UV convention. */
    public int uvRotation(CubeFace face) {
        if (isCap(face)) {
            return 0;
        }
        return switch (this) {
            case X -> switch (face) {
                case UP, DOWN, SOUTH -> 1;
                case NORTH -> -1;
                default -> 0;
            };
            case Y -> 0;
            case Z -> switch (face) {
                case DOWN -> 2;
                case EAST -> -1;
                case WEST -> 1;
                default -> 0;
            };
        };
    }

    public static PillarAxis parse(String raw) {
        return switch (raw) {
            case "x" -> X;
            case "y" -> Y;
            case "z" -> Z;
            case null, default -> throw new IllegalArgumentException(
                    "pillar axis is missing or malformed"
            );
        };
    }
}
