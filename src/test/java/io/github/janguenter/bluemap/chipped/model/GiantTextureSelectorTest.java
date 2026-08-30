/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chipped.model;

import static org.junit.jupiter.api.Assertions.assertEquals;

import io.github.janguenter.bluemap.resource.athena.model.CubeFace;
import org.junit.jupiter.api.Test;

class GiantTextureSelectorTest {

    @Test
    void originFaceFlipsMatchExactOracle() {
        assertTiles(0, 0, 0, 1, 2, 2, 1, 1, 3);
    }

    @Test
    void negativeCoordinatesUseLongAbsoluteValuesBeforeFlips() {
        assertTiles(-1, -1, -1, 4, 3, 3, 4, 4, 2);
        int value = GiantTextureSelector.select(
                CubeFace.SOUTH, Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MIN_VALUE
        );
        assertEquals(1, value);
    }

    private static void assertTiles(
            int x, int y, int z,
            int west, int east, int north, int south, int up, int down
    ) {
        assertEquals(west, GiantTextureSelector.select(CubeFace.WEST, x, y, z));
        assertEquals(east, GiantTextureSelector.select(CubeFace.EAST, x, y, z));
        assertEquals(north, GiantTextureSelector.select(CubeFace.NORTH, x, y, z));
        assertEquals(south, GiantTextureSelector.select(CubeFace.SOUTH, x, y, z));
        assertEquals(up, GiantTextureSelector.select(CubeFace.UP, x, y, z));
        assertEquals(down, GiantTextureSelector.select(CubeFace.DOWN, x, y, z));
    }
}
