/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chipped.model;

import io.github.janguenter.bluemap.resource.athena.model.CubeFace;

/** Exact stable 2x2 absolute-coordinate tile selector from the Athena behavior oracle. */
public final class GiantTextureSelector {

    private static final int WIDTH = 2;
    private static final int HEIGHT = 2;

    private GiantTextureSelector() {
    }

    public static int select(CubeFace face, int worldX, int worldY, int worldZ) {
        long x = absolute(worldX);
        long y = absolute(worldY);
        long z = absolute(worldZ);
        if (face == CubeFace.EAST) {
            z = Math.abs(z - WIDTH - 1L);
        }
        if (face == CubeFace.NORTH) {
            x = Math.abs(x - WIDTH - 1L);
        }
        if (face == CubeFace.DOWN) {
            z = Math.abs(z - WIDTH - 1L);
        }

        long index = switch (face) {
            case EAST, WEST -> 1L + (z % WIDTH) + (y % HEIGHT) * HEIGHT;
            case NORTH, SOUTH -> 1L + (x % WIDTH) + (y % HEIGHT) * HEIGHT;
            case DOWN, UP -> 1L + (x % WIDTH) + (z % HEIGHT) * HEIGHT;
        };
        return Math.toIntExact(index);
    }

    private static long absolute(int value) {
        return Math.abs((long) value);
    }
}
